[根目录](../../CLAUDE.md) > **logs**

# Logs 模块文档

## 模块职责

**logs模块**是damaihelper的日志记录和监控系统，负责记录抢票过程中的所有重要事件、错误信息和运行状态。该模块为系统故障诊断、性能监控和运行分析提供关键数据支持。

## 入口与启动

### 日志文件结构
- **`error_log.txt`** - 错误和异常日志记录
- **`script_log.txt`** - 脚本运行过程日志
- **`debug_log.txt`** - 调试信息日志（可选）

### 日志初始化
```python
import logging
import os
from datetime import datetime

def setup_logging():
    """配置日志系统"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 配置错误日志
    error_handler = logging.FileHandler(f"{log_dir}/error_log.txt")
    error_handler.setLevel(logging.ERROR)

    # 配置脚本运行日志
    script_handler = logging.FileHandler(f"{log_dir}/script_log.txt")
    script_handler.setLevel(logging.INFO)

    # 配置控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
```

## 对外接口

### 日志记录接口

#### 1. 错误日志记录
```python
def log_error(error_message, exception=None):
    """记录错误信息"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] ERROR: {error_message}"

    if exception:
        log_entry += f"\nException: {str(exception)}"
        log_entry += f"\nTraceback: {traceback.format_exc()}"

    with open("logs/error_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry + "\n\n")

    print(log_entry)  # 同时输出到控制台
```

#### 2. 运行日志记录
```python
def log_script_event(event_type, message, details=None):
    """记录脚本运行事件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {event_type}: {message}"

    if details:
        log_entry += f"\nDetails: {details}"

    with open("logs/script_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

    print(log_entry)
```

#### 3. 抢票过程日志
```python
def log_ticket_process(account_id, status, details=None):
    """记录抢票过程状态"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] ACCOUNT-{account_id}: {status}"

    if details:
        log_entry += f" - {details}"

    with open("logs/script_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")
```

### 日志查询接口

#### 1. 错误统计
```python
def get_error_statistics(days=7):
    """获取最近N天的错误统计"""
    from datetime import datetime, timedelta

    cutoff_date = datetime.now() - timedelta(days=days)
    error_count = 0
    error_types = {}

    with open("logs/error_log.txt", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip() and line.startswith("["):
                try:
                    log_date = datetime.strptime(line[1:20], "%Y-%m-%d %H:%M:%S")
                    if log_date >= cutoff_date:
                        error_count += 1
                        # 统计错误类型
                        if "WebDriverException" in line:
                            error_types["WebDriver"] = error_types.get("WebDriver", 0) + 1
                        elif "TimeoutException" in line:
                            error_types["Timeout"] = error_types.get("Timeout", 0) + 1
                        elif "NetworkException" in line:
                            error_types["Network"] = error_types.get("Network", 0) + 1
                except ValueError:
                    continue

    return {
        "total_errors": error_count,
        "error_types": error_types,
        "period_days": days
    }
```

#### 2. 运行状态查询
```python
def get_recent_activities(limit=50):
    """获取最近的运行活动记录"""
    activities = []

    with open("logs/script_log.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in reversed(lines[-limit:]):
            if line.strip() and line.startswith("["):
                activities.append(line.strip())

    return list(reversed(activities))
```

## 关键依赖与配置

### 日志配置参数
```python
LOGGING_CONFIG = {
    "log_level": "INFO",          # 日志级别: DEBUG, INFO, WARNING, ERROR
    "max_file_size": "10MB",      # 单个日志文件最大大小
    "backup_count": 5,            # 保留的日志文件备份数量
    "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "encoding": "utf-8"
}
```

### 日志文件轮转
```python
from logging.handlers import RotatingFileHandler

def setup_rotating_logs():
    """设置日志文件轮转"""
    error_handler = RotatingFileHandler(
        "logs/error_log.txt",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )

    script_handler = RotatingFileHandler(
        "logs/script_log.txt",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
```

## 数据模型

### 日志条目模型 (Log Entry Model)
```json
{
  "timestamp": "2025-10-26 20:48:01",
  "level": "ERROR|INFO|DEBUG|WARNING",
  "module": "selenium_driver|multi_account_manager|scheduler",
  "account_id": "user1@damai.com",
  "event_type": "LOGIN_SUCCESS|TICKET_ACQUIRED|ERROR_OCCURRED",
  "message": "用户登录成功",
  "details": {
    "platform": "damai",
    "target_url": "https://m.damai.cn/...",
    "execution_time": "2.3s",
    "user_agent": "Mozilla/5.0..."
  }
}
```

### 错误日志模型 (Error Log Model)
```json
{
  "timestamp": "2025-10-26 20:48:01",
  "error_type": "WebDriverException|TimeoutException|NetworkException",
  "error_message": "无法定位页面元素",
  "stack_trace": "...",
  "context": {
    "url": "https://m.damai.cn/damai/detail/item.html",
    "element_selector": ".buy-button",
    "retry_count": 3
  }
}
```

### 性能监控模型 (Performance Model)
```json
{
  "timestamp": "2025-10-26 20:48:01",
  "operation": "page_load|element_click|form_submit",
  "execution_time": 2.3,
  "success": true,
  "platform": "damai",
  "account_id": "user1@damai.com"
}
```

## 测试与质量

### 日志功能测试
```python
import unittest
import os
import tempfile

class TestLoggingSystem(unittest.TestCase):
    def setUp(self):
        """测试前准备"""
        self.test_log_dir = tempfile.mkdtemp()

    def test_error_logging(self):
        """测试错误日志记录"""
        log_error("测试错误消息")
        self.assertTrue(os.path.exists("logs/error_log.txt"))

    def test_script_logging(self):
        """测试脚本运行日志记录"""
        log_script_event("TEST", "测试事件", {"key": "value"})
        self.assertTrue(os.path.exists("logs/script_log.txt"))

    def tearDown(self):
        """测试后清理"""
        # 清理测试日志文件
        pass
```

### 日志分析测试
```python
def test_error_statistics():
    """测试错误统计功能"""
    # 创建测试日志数据
    create_test_log_data()

    stats = get_error_statistics(days=1)
    assert "total_errors" in stats
    assert "error_types" in stats
    assert isinstance(stats["total_errors"], int)
```

## 常见问题 (FAQ)

### Q1: 日志文件过大如何处理？
A1:
1. 配置日志文件轮转（RotatingFileHandler）
2. 设置最大文件大小（如10MB）
3. 自动删除旧日志文件
4. 定期归档历史日志

### Q2: 如何查看实时日志？
A2:
```bash
# 查看错误日志
tail -f logs/error_log.txt

# 查看运行日志
tail -f logs/script_log.txt

# 同时查看两个日志
tail -f logs/*.log
```

### Q3: 日志权限问题怎么办？
A3:
1. 确保logs目录存在且有写权限
2. 检查文件所有者和用户组
3. 避免在生产环境中使用root权限运行

### Q4: 如何过滤特定类型的日志？
A4:
```bash
# 过滤WebDriver错误
grep "WebDriver" logs/error_log.txt

# 查看特定账户的日志
grep "user1@damai.com" logs/script_log.txt

# 查看今天的日志
grep "$(date +%Y-%m-%d)" logs/*.txt
```

### Q5: 日志时间戳不准确怎么办？
A5:
1. 检查系统时区设置
2. 使用UTC时间戳记录
3. 在显示时转换为本地时间
4. 确保服务器时间同步

## 相关文件清单

### 核心日志文件
- `error_log.txt` - 系统错误和异常日志
- `script_log.txt` - 脚本运行过程日志
- `debug_log.txt` - 详细调试信息（按需启用）

### 日志配置和管理
- `log_config.json` - 日志系统配置（待实现）
- `log_rotate.conf` - 日志轮转配置（待实现）
- `log_cleaner.py` - 日志清理脚本（待实现）

### 日志分析工具
- `log_analyzer.py` - 日志分析工具（待实现）
- `error_reporter.py` - 错误报告生成器（待实现）
- `performance_monitor.py` - 性能监控工具（待实现）

### 监控和告警
- `alert_config.json` - 告警配置（待实现）
- `notification_sender.py` - 通知发送器（待实现）

## 变更记录 (Changelog)

- **2025-10-26**: 自适应初始化架构师完成日志模块文档化，定义日志数据模型
- **2024-12月**: 优化错误日志格式，增加上下文信息
- **2024-04-01**: 新增性能监控日志
- **2023-09-15**: 初始化基础日志系统

---

**模块覆盖率**: 100% (2/2 文件已分析)
**下次扫描重点**:
- 实际日志内容分析
- 日志轮转和归档机制
- 性能监控指标定义
- 实时日志查看工具开发