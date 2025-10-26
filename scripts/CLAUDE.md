[根目录](../../CLAUDE.md) > **scripts**

# Scripts 模块文档

## 模块职责

**scripts模块**是damaihelper的现代化核心组件系统，负责协调和管理抢票自动化过程中的各个功能模块。该模块采用模块化设计，将原本集中在单脚本中的功能拆分为独立的、可维护的组件。

## 入口与启动

### 主要入口文件
- **`main.py`** - 模块化架构的统一入口点
  - 协调各个子模块的工作流程
  - 加载和管理配置文件
  - 处理代理池初始化
  - 协调多账户抢票任务

### 启动流程
```python
def main():
    config = load_config()                    # 加载配置
    accounts = config['accounts']             # 获取账户信息
    ticket_settings = config['ticket_settings'] # 获取票务设置

    # 处理代理池
    if ticket_settings['proxy']:
        # 初始化代理池

    # 调度抢票任务
    schedule_tasks(ticket_settings['retry_interval'], ticket_settings['auto_buy_time'])

    # 启动抢票操作
    for account_id, account_info in accounts.items():
        manage_multiple_accounts(account_info, ticket_settings)
```

## 对外接口

### 核心模块接口

#### 1. Selenium WebDriver管理
**文件**: `selenium_driver.py`
**主要接口**:
```python
def start_selenium_driver(target_url):
    # 启动Chrome浏览器并访问目标页面
    driver = webdriver.Chrome(executable_path='path/to/chromedriver')
    driver.get(target_url)
    return driver
```

#### 2. 多账户管理
**文件**: `multi_account_manager.py`
**主要接口**:
```python
def manage_multiple_accounts(account_info, ticket_settings):
    target_url = account_info['target_url']
    driver = start_selenium_driver(target_url)
    # 执行登录和抢票流程
```

#### 3. 定时任务调度
**文件**: `scheduler.py`
**主要接口**:
```python
def schedule_tasks(retry_interval, auto_buy_time):
    scheduler = BlockingScheduler()
    # 定时执行抢票任务
    scheduler.add_job(func=buy_ticket, trigger='cron', hour=auto_buy_time.split(':')[0], minute=auto_buy_time.split(':')[1])
    # 设置重试间隔
    scheduler.add_job(func=retry_buy, trigger='interval', seconds=retry_interval)
```

#### 4. 验证码识别
**文件**: `captcha_solver.py`
**主要接口**:
```python
def solve_captcha(image_path):
    # 使用OCR识别验证码
    image = Image.open(image_path)
    captcha_text = pytesseract.image_to_string(image)
    return captcha_text
```

#### 5. 移动端模拟
**文件**: `appium_simulator.py`
**主要接口**:
```python
def start_simulation(account_info):
    # 初始化Appium驱动
    desired_caps = {
        "platformName": "Android",
        "deviceName": "device",
        "appPackage": "com.damai.android",
        "appActivity": ".activity.MainActivity",
    }
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
```

## 关键依赖与配置

### Python依赖
```python
# requirements.txt
selenium==4.1.0           # 浏览器自动化
appium-python-client==2.0.0  # 移动设备模拟
apscheduler==3.8.0        # 定时任务调度
pytesseract==0.3.8        # OCR验证码识别
pillow==8.4.0            # 图像处理
```

### 配置文件依赖
- `config/config.json` - 主配置文件，包含账户和票务参数
- `config/platform_config.json` - 平台特定配置
- `config/proxy_pool.json` - 代理IP池配置

### 外部服务依赖
- **ChromeDriver** - Selenium WebDriver驱动程序
- **Appium Server** - 移动端自动化服务
- **Tesseract OCR** - 验证码文本识别引擎
- **代理服务器** - IP轮换和反检测

## 数据模型

### 账户信息模型
```python
account_info = {
    "username": "user@example.com",
    "password": "password",
    "target_url": "https://m.damai.cn/...",
    "auto_buy_time": "08:30:00",
    "viewer_person": [1, 2]
}
```

### 票务设置模型
```python
ticket_settings = {
    "retry_interval": 5,      # 重试间隔(秒)
    "auto_buy": True,         # 是否自动抢票
    "auto_buy_time": "08:30:00",  # 自动抢票时间
    "proxy": True,            # 是否使用代理
    "date": [14, 15, 16],     # 日期优先级
    "session": [1, 2, 3],     # 场次优先级
    "price": [1, 2, 3, 4, 5, 6, 7],  # 价格优先级
    "ticket_num": 2,          # 购票数量
    "viewer_person": [2, 3]   # 观影人优先级
}
```

### 代理配置模型
```python
proxy_config = {
    "enabled": True,
    "proxy_ip": "192.168.1.100",
    "proxy_port": "8080",
    "proxy_type": "HTTPS",
    "proxy_list": [
        "192.168.1.100:8080",
        "203.0.113.50:3128",
        "198.51.100.1:1080"
    ]
}
```

## 测试与质量

### 当前测试状态
- **单元测试**: ❌ 未实现
- **集成测试**: ❌ 未实现
- **功能测试**: ✅ 通过手动验证
- **代码质量**: ⚠️ 需要改进错误处理和日志记录

### 建议的测试策略

#### 1. 单元测试
```python
# tests/test_selenium_driver.py
def test_start_selenium_driver():
    driver = start_selenium_driver("https://www.example.com")
    assert driver is not None
    assert "example.com" in driver.current_url
    driver.quit()

# tests/test_scheduler.py
def test_schedule_tasks():
    with patch('apscheduler.schedulers.blocking.BlockingScheduler') as mock_scheduler:
        schedule_tasks(5, "08:30:00")
        mock_scheduler.assert_called_once()
```

#### 2. 集成测试
```python
# tests/test_integration.py
def test_full_workflow():
    # 测试完整的抢票流程
    config = load_test_config()
    result = run_ticket_acquisition(config)
    assert result['status'] in ['success', 'failed']
```

### 代码质量改进建议

#### 1. 错误处理增强
```python
def start_selenium_driver(target_url):
    try:
        driver = webdriver.Chrome(executable_path='path/to/chromedriver')
        driver.get(target_url)
        return driver
    except WebDriverException as e:
        logger.error(f"WebDriver启动失败: {e}")
        raise DriverInitializationError(f"无法启动Chrome驱动: {e}")
    except Exception as e:
        logger.error(f"未知错误: {e}")
        raise
```

#### 2. 配置验证
```python
def validate_config(config):
    """验证配置文件格式和必填字段"""
    required_fields = ['accounts', 'ticket_settings']
    for field in required_fields:
        if field not in config:
            raise ConfigValidationError(f"缺少必填配置项: {field}")
```

## 常见问题 (FAQ)

### Q1: ChromeDriver路径如何配置？
A1: 需要在`config.json`中设置正确的`driver_path`，或确保ChromeDriver在系统PATH中。

### Q2: 多账户抢票是否会冲突？
A2: 模块通过独立的WebDriver会话管理每个账户，避免会话冲突，但建议为不同账户设置不同的代理IP。

### Q3: 定时任务不执行怎么办？
A3: 检查`auto_buy_time`格式是否正确(HH:MM:SS)，确保APScheduler服务正常启动。

### Q4: 验证码识别失败率高？
A4: 可以配置多个OCR服务作为备份，或切换到手动处理模式。

### Q5: 如何添加新的票务平台？
A5: 参考`config/platform_config.json`中的现有平台配置模板，添加新平台的登录方式和页面元素定位策略。

## 相关文件清单

### 核心模块文件
- `main.py` - 主入口和协调器
- `selenium_driver.py` - 浏览器自动化驱动
- `multi_account_manager.py` - 多账户管理
- `scheduler.py` - 定时任务调度
- `captcha_solver.py` - 验证码识别
- `appium_simulator.py` - 移动端模拟

### 配置和依赖文件
- `../config/config.json` - 主配置文件
- `../config/platform_config.json` - 平台配置
- `../requirements.txt` - Python依赖

### 日志和输出文件
- `../logs/` - 日志输出目录
- `../cookies.pkl` - Cookie持久化文件

### 外部工具和服务
- `chromedriver.exe` - Chrome驱动程序
- Appium Server - 移动端自动化服务
- Tesseract OCR - 文本识别引擎

## 变更记录 (Changelog)

- **2025-10-26**: 自适应初始化架构师完成模块文档化，生成详细接口和数据模型
- **2024-12月**: 增强多账户管理和调度稳定性
- **2024-04-01**: 新增Appium移动端模拟支持
- **2023-09-15**: 优化调度器和验证码处理机制

---

**模块覆盖率**: 100% (6/6 文件已完整分析)
**下次扫描重点**: 配置文件依赖验证、外部服务连接测试