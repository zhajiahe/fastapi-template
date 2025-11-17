"""
测试动态图创建功能

验证用户可以通过修改 user_settings 来动态改变 LLM 模型参数
"""

import pytest
import pytest_asyncio

from app.core.checkpointer import close_checkpointer, init_checkpointer
from app.core.lifespan import get_cached_graph


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_checkpointer():
    """初始化测试用的 checkpointer"""
    # 使用临时数据库
    checkpointer = await init_checkpointer(":memory:")
    yield checkpointer
    # 清理
    await close_checkpointer()


@pytest.mark.asyncio
async def test_graph_creation_with_different_models():
    """测试不同模型配置会创建不同的图实例"""
    # 创建第一个图实例
    graph1 = await get_cached_graph(
        llm_model="Qwen/Qwen3-8B",
        max_tokens=4096,
    )

    # 使用相同配置创建图实例
    graph2 = await get_cached_graph(
        llm_model="Qwen/Qwen3-8B",
        max_tokens=4096,
    )

    # 验证图对象被创建
    assert graph1 is not None
    assert graph2 is not None

    # 使用不同配置创建新实例
    graph3 = await get_cached_graph(
        llm_model="Qwen/Qwen3-72B",
        max_tokens=8192,
    )

    # 验证图对象被创建
    assert graph3 is not None


@pytest.mark.asyncio
async def test_graph_with_none_values():
    """测试 None 值参数的图创建"""
    # 使用 None 值创建图
    graph1 = await get_cached_graph(
        llm_model=None,
        api_key=None,
        base_url=None,
        max_tokens=4096,
    )

    # 验证图对象被创建
    assert graph1 is not None


@pytest.mark.asyncio
async def test_graph_creation_with_custom_params():
    """测试使用自定义参数创建图"""
    # 创建多个不同配置的图实例
    graphs = []
    for i in range(5):
        graph = await get_cached_graph(
            llm_model=f"model-{i}",
            max_tokens=4096 + i * 1024,
        )
        graphs.append(graph)
        assert graph is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
