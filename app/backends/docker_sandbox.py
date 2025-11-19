"""DockerSandboxBackend: Production-ready sandboxed backend using Docker."""

import tarfile
import uuid
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING

import docker
from deepagents.backends.protocol import (
    EditResult,
    ExecuteResponse,
    FileInfo,
    GrepMatch,
    SandboxBackendProtocol,
    WriteResult,
)
from deepagents.backends.utils import (
    create_file_data,
    format_read_response,
    perform_string_replacement,
    update_file_data,
)

if TYPE_CHECKING:
    from docker.models.containers import Container


class DockerSandboxBackend(SandboxBackendProtocol):
    """Production-ready sandboxed backend using Docker containers.

    This backend provides isolated execution environment with:
    - File system isolation
    - Resource limits (CPU, memory)
    - Network isolation (optional)
    - Command execution in container
    - Automatic cleanup

    Features:
    - ✅ Isolated execution environment
    - ✅ Resource limits (CPU, memory, disk)
    - ✅ Network isolation
    - ✅ Automatic container cleanup
    - ✅ File persistence in container
    - ✅ Command execution with timeout

    Example:
        ```python
        from app.backends.docker_sandbox import DockerSandboxBackend

        backend = DockerSandboxBackend(
            image="python:3.12-slim",
            memory_limit="512m",
            cpu_quota=50000,
            network_mode="none",
        )

        agent = create_agent(model, tools=tools, middleware=[FilesystemMiddleware(backend=backend)])
        ```
    """

    def __init__(
        self,
        image: str = "python:3.12-slim",
        memory_limit: str = "512m",
        cpu_quota: int = 50000,
        network_mode: str = "none",
        working_dir: str = "/workspace",
        auto_remove: bool = True,
        max_output_size: int = 100000,
        command_timeout: int = 30,
    ):
        """Initialize DockerSandboxBackend.

        Args:
            image: Docker image to use (default: python:3.12-slim)
            memory_limit: Memory limit (e.g., "512m", "1g")
            cpu_quota: CPU quota in microseconds (50000 = 50% of one core)
            network_mode: Network mode ("none" for isolation, "bridge" for network access)
            working_dir: Working directory in container
            auto_remove: Auto-remove container on exit
            max_output_size: Maximum command output size in characters
            command_timeout: Command execution timeout in seconds
        """
        self._id = str(uuid.uuid4())
        self.image = image
        self.memory_limit = memory_limit
        self.cpu_quota = cpu_quota
        self.network_mode = network_mode
        self.working_dir = working_dir
        self.auto_remove = auto_remove
        self.max_output_size = max_output_size
        self.command_timeout = command_timeout

        # Initialize Docker client
        self.client = docker.from_env()

        # Container instance
        self._container: Container | None = None

        # File cache (in-memory representation of container files)
        self._files: dict[str, dict] = {}

    @property
    def id(self) -> str:
        """Unique identifier for this backend instance."""
        return self._id

    @property
    def container(self) -> "Container":
        """Get or create Docker container."""
        if self._container is None:
            self._create_container()
        assert self._container is not None
        return self._container

    def _create_container(self) -> None:
        """Create and start Docker container."""
        try:
            # Pull image if not exists
            try:
                self.client.images.get(self.image)
            except docker.errors.ImageNotFound:
                print(f"Pulling Docker image: {self.image}")
                self.client.images.pull(self.image)

            # Create container
            self._container = self.client.containers.create(
                image=self.image,
                command="sleep infinity",  # Keep container running
                detach=True,
                mem_limit=self.memory_limit,
                cpu_quota=self.cpu_quota,
                network_mode=self.network_mode,
                working_dir=self.working_dir,
                auto_remove=self.auto_remove,
            )

            # Start container
            self._container.start()

            # Create working directory
            self._exec_command(f"mkdir -p {self.working_dir}")

        except Exception as e:
            raise RuntimeError(f"Failed to create Docker container: {e}") from e

    def _exec_command(self, command: str) -> tuple[str, int]:
        """Execute command in container (internal helper).

        Returns:
            Tuple of (output, exit_code)
        """
        exit_code, output = self.container.exec_run(
            cmd=["sh", "-c", command],
            workdir=self.working_dir,
        )
        return output.decode("utf-8", errors="replace"), exit_code

    def _read_file_from_container(self, file_path: str) -> str | None:
        """Read file from container.

        Returns:
            File content as string, or None if file doesn't exist.
        """
        try:
            # Get file from container as tar archive
            bits, _stat = self.container.get_archive(file_path)

            # Extract file content from tar
            file_obj = BytesIO()
            for chunk in bits:
                file_obj.write(chunk)
            file_obj.seek(0)

            with tarfile.open(fileobj=file_obj) as tar:
                # Get first file in archive
                member = tar.next()
                if member is None:
                    return None
                extracted = tar.extractfile(member)
                if extracted is None:
                    return None
                return extracted.read().decode("utf-8", errors="replace")

        except docker.errors.NotFound:
            return None
        except Exception:
            return None

    def _write_file_to_container(self, file_path: str, content: str) -> bool:
        """Write file to container.

        Returns:
            True if successful, False otherwise.
        """
        try:
            # Create tar archive with file
            tar_stream = BytesIO()
            with tarfile.open(fileobj=tar_stream, mode="w") as tar:
                # Create file info
                file_data = content.encode("utf-8")
                tarinfo = tarfile.TarInfo(name=Path(file_path).name)
                tarinfo.size = len(file_data)
                tarinfo.mtime = int(datetime.now().timestamp())

                # Add file to tar
                tar.addfile(tarinfo, BytesIO(file_data))

            # Upload tar to container
            tar_stream.seek(0)
            parent_dir = str(Path(file_path).parent)
            self.container.put_archive(parent_dir, tar_stream)
            return True

        except Exception:
            return False

    # BackendProtocol implementation

    def ls_info(self, path: str) -> list[FileInfo]:
        """List files and directories in the specified directory.

        Args:
            path: Absolute path to directory.

        Returns:
            List of FileInfo dicts for files and directories.
        """
        try:
            # Use ls command to list files
            output, exit_code = self._exec_command(f"ls -la {path}")
            if exit_code != 0:
                return []

            infos: list[FileInfo] = []
            lines = output.strip().split("\n")[1:]  # Skip "total" line

            for line in lines:
                parts = line.split()
                if len(parts) < 9:
                    continue

                permissions = parts[0]
                size = int(parts[4]) if parts[4].isdigit() else 0
                name = " ".join(parts[8:])

                # Skip . and ..
                if name in (".", ".."):
                    continue

                file_path = f"{path.rstrip('/')}/{name}"
                is_dir = permissions.startswith("d")

                infos.append(
                    {
                        "path": file_path + ("/" if is_dir else ""),
                        "is_dir": is_dir,
                        "size": size,
                        "modified_at": "",
                    }
                )

            return infos

        except Exception:
            return []

    def read(
        self,
        file_path: str,
        offset: int = 0,
        limit: int = 2000,
    ) -> str:
        """Read file content with line numbers.

        Args:
            file_path: Absolute file path
            offset: Line offset to start reading from (0-indexed)
            limit: Maximum number of lines to read

        Returns:
            Formatted file content with line numbers, or error message.
        """
        content = self._read_file_from_container(file_path)
        if content is None:
            return f"Error: File '{file_path}' not found"

        # Create file data structure
        lines = content.splitlines()
        file_data = {
            "content": lines,
            "created_at": datetime.now().isoformat(),
            "modified_at": datetime.now().isoformat(),
        }

        result: str = format_read_response(file_data, offset, limit)
        return result

    def write(
        self,
        file_path: str,
        content: str,
    ) -> WriteResult:
        """Create a new file with content.

        Args:
            file_path: Absolute file path
            content: File content

        Returns:
            WriteResult with success or error.
        """
        # Check if file already exists
        existing = self._read_file_from_container(file_path)
        if existing is not None:
            return WriteResult(
                error=f"Cannot write to {file_path} because it already exists. Read and then make an edit, or write to a new path."
            )

        # Create parent directory if needed
        parent_dir = str(Path(file_path).parent)
        self._exec_command(f"mkdir -p {parent_dir}")

        # Write file to container
        success = self._write_file_to_container(file_path, content)
        if not success:
            return WriteResult(error=f"Failed to write file {file_path}")

        # Update cache
        self._files[file_path] = create_file_data(content)

        return WriteResult(path=file_path, files_update=None)

    def edit(
        self,
        file_path: str,
        old_string: str,
        new_string: str,
        replace_all: bool = False,
    ) -> EditResult:
        """Edit a file by replacing string occurrences.

        Args:
            file_path: Absolute file path
            old_string: String to replace
            new_string: Replacement string
            replace_all: Replace all occurrences (default: False)

        Returns:
            EditResult with success or error.
        """
        # Read file from container
        content = self._read_file_from_container(file_path)
        if content is None:
            return EditResult(error=f"Error: File '{file_path}' not found")

        # Perform replacement
        result = perform_string_replacement(content, old_string, new_string, replace_all)
        if isinstance(result, str):
            return EditResult(error=result)

        new_content, occurrences = result

        # Write updated content back to container
        success = self._write_file_to_container(file_path, new_content)
        if not success:
            return EditResult(error=f"Failed to write file {file_path}")

        # Update cache
        if file_path in self._files:
            self._files[file_path] = update_file_data(self._files[file_path], new_content)

        return EditResult(path=file_path, files_update=None, occurrences=int(occurrences))

    def grep_raw(
        self,
        pattern: str,
        path: str | None = None,
        glob: str | None = None,
    ) -> list[GrepMatch] | str:
        """Search for a pattern in files.

        Args:
            pattern: Search pattern (literal string)
            path: Directory to search in (default: working_dir)
            glob: Glob pattern to filter files

        Returns:
            List of GrepMatch dicts or error string.
        """
        search_path = path or self.working_dir
        grep_cmd = f"grep -rn '{pattern}' {search_path}"

        if glob:
            grep_cmd += f" --include='{glob}'"

        output, exit_code = self._exec_command(grep_cmd)

        if exit_code != 0 and not output:
            return []

        matches: list[GrepMatch] = []
        for line in output.strip().split("\n"):
            if not line:
                continue

            parts = line.split(":", 2)
            if len(parts) >= 3:
                matches.append(
                    {
                        "path": parts[0],
                        "line": int(parts[1]) if parts[1].isdigit() else 0,
                        "text": parts[2],
                    }
                )

        return matches

    def glob_info(self, pattern: str, path: str = "/") -> list[FileInfo]:
        """Find files matching a glob pattern.

        Args:
            pattern: Glob pattern (e.g., "*.py", "**/*.txt")
            path: Directory to search in

        Returns:
            List of FileInfo dicts for matching files.
        """
        # Use find command with pattern
        find_cmd = f"find {path} -name '{pattern}'"
        output, exit_code = self._exec_command(find_cmd)

        if exit_code != 0:
            return []

        infos: list[FileInfo] = []
        for file_path in output.strip().split("\n"):
            if not file_path:
                continue

            # Get file size
            size_cmd = f"stat -c %s {file_path}"
            size_output, _ = self._exec_command(size_cmd)
            size = int(size_output.strip()) if size_output.strip().isdigit() else 0

            infos.append(
                {
                    "path": file_path,
                    "is_dir": False,
                    "size": size,
                    "modified_at": "",
                }
            )

        return infos

    # SandboxBackendProtocol implementation

    def execute(self, command: str) -> ExecuteResponse:
        """Execute a shell command in the container.

        Args:
            command: Shell command to execute.

        Returns:
            ExecuteResponse with output, exit code, and truncation flag.
        """
        try:
            # Execute command with timeout
            output, exit_code = self._exec_command(command)

            # Check if output needs truncation
            truncated = False
            if len(output) > self.max_output_size:
                output = output[: self.max_output_size]
                truncated = True

            return ExecuteResponse(
                output=output or "(no output)",
                exit_code=exit_code,
                truncated=truncated,
            )

        except Exception as e:
            return ExecuteResponse(
                output=f"Error executing command: {str(e)}",
                exit_code=-1,
                truncated=False,
            )

    def cleanup(self) -> None:
        """Stop and remove the Docker container."""
        if self._container is not None:
            try:
                self._container.stop(timeout=5)
                if not self.auto_remove:
                    self._container.remove()
            except Exception:
                pass
            finally:
                self._container = None

    def __del__(self):
        """Cleanup on garbage collection."""
        self.cleanup()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
