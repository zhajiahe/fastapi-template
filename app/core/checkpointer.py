"""
LangGraph 检查点管理

管理对话状态的持久化
"""

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from loguru import logger

# 全局 checkpointer 实例和上下文管理器
checkpointer: AsyncSqliteSaver | None = None
_checkpointer_cm = None


async def init_checkpointer(db_path: str = "checkpoints.db") -> AsyncSqliteSaver:
    """
    初始化异步 SQLite 检查点保存器

    Args:
        db_path: SQLite 数据库路径

    Returns:
        AsyncSqliteSaver: 检查点保存器实例
    """
    global checkpointer, _checkpointer_cm

    try:
        # 创建上下文管理器并进入
        _checkpointer_cm = AsyncSqliteSaver.from_conn_string(db_path)
        checkpointer = await _checkpointer_cm.__aenter__()
        logger.info(f"✅ Checkpointer initialized: {db_path}")
        return checkpointer
    except Exception as e:
        logger.error(f"❌ Failed to initialize checkpointer: {e}")
        raise


async def close_checkpointer():
    """关闭检查点保存器连接"""
    global checkpointer, _checkpointer_cm

    if checkpointer and _checkpointer_cm:
        try:
            # 正确退出上下文管理器
            await _checkpointer_cm.__aexit__(None, None, None)
            checkpointer = None
            _checkpointer_cm = None
            logger.info("✅ Checkpointer connection closed")
        except Exception as e:
            logger.error(f"❌ Failed to close checkpointer: {e}")


def get_checkpointer() -> AsyncSqliteSaver:
    """
    获取全局检查点保存器实例

    Returns:
        AsyncSqliteSaver: 检查点保存器实例

    Raises:
        RuntimeError: 如果检查点保存器未初始化
    """
    if checkpointer is None:
        raise RuntimeError("Checkpointer not initialized. Call init_checkpointer() first.")
    return checkpointer


async def delete_thread_checkpoints(thread_id: str) -> None:
    """
    删除指定线程的所有检查点

    Args:
        thread_id: 线程ID

    Raises:
        RuntimeError: 如果检查点保存器未初始化
    """
    if checkpointer is None:
        raise RuntimeError("Checkpointer not initialized. Call init_checkpointer() first.")

    try:
        await checkpointer.adelete_thread(thread_id)
        logger.info(f"✅ Deleted checkpoints for thread: {thread_id}")
    except Exception as e:
        logger.error(f"❌ Failed to delete checkpoints for thread {thread_id}: {e}")
        raise
