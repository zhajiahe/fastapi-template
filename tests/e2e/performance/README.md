# 对话接口性能测试

使用 Locust 对 FastAPI 对话接口进行负载测试，模拟不同并发用户数量下的性能表现。

## 测试场景

- **1用户**: 基准性能测试，验证基本功能
- **5用户**: 中等并发负载测试
- **10用户**: 高并发压力测试

## 快速开始

### 1. 启动 FastAPI 服务

确保你的 FastAPI 服务正在运行：

```bash
# 开发模式
make dev

# 或直接启动
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 运行完整测试套件

```bash
# 运行所有场景的性能测试
python tests/e2e/performance/run_performance_tests.py

# 指定自定义服务地址
python tests/e2e/performance/run_performance_tests.py --base-url http://localhost:8001
```

### 3. 运行单个场景测试

```bash
# 1用户测试
python tests/e2e/performance/run_performance_tests.py --scenario 1

# 5用户测试
python tests/e2e/performance/run_performance_tests.py --scenario 5

# 10用户测试
python tests/e2e/performance/run_performance_tests.py --scenario 10 --run-time 3m
```

## 测试内容

每个测试用户会执行以下操作：

1. **登录**: 获取访问令牌
2. **创建会话**: 初始化对话线程
3. **非流式对话** (权重 3): 发送普通对话请求
4. **流式对话** (权重 2): 发送流式对话请求
5. **停止对话** (权重 1): 偶尔停止进行中的对话

## 配置说明

### 环境变量

- `PERF_TEST_BASE_URL`: API 基础URL (默认: http://localhost:8000)

### 测试参数

通过命令行参数自定义测试：

- `--base-url`: 指定API服务地址
- `--scenario`: 选择测试场景 (1/5/10/all)
- `--run-time`: 指定单场景运行时间

## 使用 Locust Web 界面

如果你想使用 Locust 的 Web 界面进行交互式测试：

```bash
# 启动 Locust Web 界面
locust -f tests/e2e/performance/chat_performance_test.py --config tests/e2e/performance/locust.conf

# 然后在浏览器中访问 http://localhost:8089
```

## 输出结果

测试完成后会生成：

- **控制台输出**: 实时性能指标和统计信息
- **HTML报告**: `tests/e2e/performance/report.html` (如果启用)
- **CSV数据**: `tests/e2e/performance/results/` 目录 (如果启用)

### 关键性能指标

- **RPS (Requests per Second)**: 每秒请求数
- **Response Time**: 响应时间 (平均值、95%、99%)
- **Failure Rate**: 失败率
- **Users**: 并发用户数

## 故障排除

### 服务连接问题

确保 FastAPI 服务正在运行且可访问：

```bash
# 检查服务健康状态
curl http://localhost:8000/health

# 检查对话接口
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=admin&password=admin123"
```

### 数据库性能

如果测试期间出现数据库性能问题：

1. 确保使用适当的数据库连接池配置
2. 考虑使用内存数据库进行测试 (`SQLALCHEMY_DATABASE_URL=sqlite+aiosqlite:///:memory:`)
3. 检查数据库连接数限制

### 内存和CPU监控

在测试期间监控系统资源：

```bash
# Linux/Mac
top -p $(pgrep -f uvicorn)
htop

# 或使用 Python 工具
pip install psutil
python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%, Memory: {psutil.virtual_memory().percent}%')"
```

## 扩展测试

### 添加更多测试场景

编辑 `run_performance_tests.py` 中的 `scenarios` 列表：

```python
scenarios = [
    {"users": 1, "run_time": "30s", "description": "单用户基准测试"},
    {"users": 20, "run_time": "5m", "description": "20用户压力测试"},
    {"users": 50, "run_time": "10m", "description": "50用户极限测试"},
]
```

### 自定义用户行为

修改 `ChatUser` 类的任务权重和逻辑：

```python
@task(5)  # 提高权重
def custom_task(self):
    # 自定义测试逻辑
    pass
```

## 集成到 CI/CD

将性能测试集成到 CI/CD 流水线：

```yaml
# .github/workflows/performance.yml
name: Performance Tests
on: [push, pull_request]

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          uv sync
      - name: Run performance tests
        run: |
          python tests/e2e/performance/run_performance_tests.py --scenario all
```

## 注意事项

1. **测试环境**: 在隔离的测试环境中运行，避免影响生产数据
2. **资源监控**: 高并发测试可能消耗大量系统资源
3. **基准对比**: 记录基准性能数据，用于对比优化效果
4. **渐进式测试**: 从低并发开始，逐步增加用户数量
5. **结果分析**: 关注失败率和响应时间的变化趋势
