# 🎫 抢票脚本 V5.0 - 完整使用教程

![Damaihelper Star History](https://api.star-history.com/svg?repos=Guyungy/damaihelper&type=Date)

> **专业的多平台抢票自动化工具**，支持大麦网、淘票票、缤玩岛等主流票务平台。通过Selenium和Appium技术模拟真实用户操作，大幅提升抢票成功率。

## 📋 目录

- [🚀 快速开始](#-快速开始)
- [🛠️ 环境准备](#️-环境准备)
- [⚙️ 配置文件详解](#️-配置文件详解)
- [🖥️ 运行方式](#️-运行方式)
- [🎯 使用教程](#-使用教程)
- [📱 平台特定配置](#-平台特定配置)
- [🔧 故障排除](#-故障排除)
- [⚠️ 安全注意事项](#️-安全注意事项)

---

## 🚀 快速开始

### 🎯 5分钟快速上手

**适合有Python基础的用户**

```bash
# 1. 克隆项目
git clone https://github.com/Guyungy/damaihelper.git
cd damaihelper

# 2. 安装依赖
pip install -r requirements.txt

# 3. 下载ChromeDriver
# 访问：http://chromedriver.storage.googleapis.com/index.html
# 下载与Chrome版本匹配的驱动，放在项目根目录

# 4. 配置文件（必须！）
# 编辑 config/config.json，填入你的信息和目标URL

# 5. 运行程序
python GUI.py  # 图形界面（推荐新手）
# 或者
python ticket_script.py  # 命令行
```

### 📋 使用前必读

1. **账户准备**：确保大麦网账户已完成实名认证并添加观影人
2. **目标URL**：必须是手机端链接（`https://m.damai.cn/`开头）
3. **时间设置**：抢票时间建议比开售时间早2-3秒
4. **首次运行**：需要手动登录保存Cookie

---

## 🛠️ 环境准备

### 步骤1：系统要求检查

| 系统 | 要求 | 检查命令 |
|------|------|----------|
| **操作系统** | Windows 10+/Mac 10.13+/Linux | - |
| **Python版本** | 3.7+ | `python --version` |
| **Chrome浏览器** | 最新版本 | `google-chrome --version` |
| **内存** | 至少4GB | - |
| **网络** | 稳定连接 | - |

**如果不符合要求，请先升级系统或安装软件**

### 步骤2：项目下载

#### 方法一：Git克隆（推荐）
```bash
# 确保已安装Git
git --version

# 克隆项目到本地
git clone https://github.com/Guyungy/damaihelper.git
cd damaihelper
```

#### 方法二：ZIP下载
1. 访问：https://github.com/Guyungy/damaihelper
2. 点击绿色的"Code"按钮
3. 选择"Download ZIP"
4. 解压到合适的位置（建议：`C:\damaihelper`）

### 步骤3：Python依赖安装

#### Windows用户
```bash
# 进入项目目录
cd damaihelper

# 安装依赖
pip install -r requirements.txt

# 如果遇到问题，使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# Windows一键环境搭建
./win一件运行.bat
```

#### Mac/Linux用户
```bash
# 进入项目目录
cd damaihelper

# 安装Python依赖
pip3 install -r requirements.txt

# 安装额外的系统依赖
# Mac用户
brew install tesseract  # OCR文字识别

# Linux用户 (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install chromium-browser
```

### 步骤4：ChromeDriver配置

#### 4.1 检查Chrome版本
1. 打开Chrome浏览器
2. 点击右上角三个点 → 设置 → 关于Chrome
3. 记录版本号（例如：120.0.6099.130）

#### 4.2 下载匹配的ChromeDriver
1. 访问：http://chromedriver.storage.googleapis.com/index.html
2. 找到对应版本文件夹
3. 下载系统对应的文件：
   - Windows：`chromedriver_win32.zip`
   - Mac：`chromedriver_mac64.zip`
   - Linux：`chromedriver_linux64.zip`

#### 4.3 配置ChromeDriver路径

##### Windows配置
```bash
# 1. 解压下载的文件
# 2. 将 chromedriver.exe 放在项目根目录
# 3. 测试是否正常
chromedriver.exe --version

# 4. 或者在配置文件中指定绝对路径
"driver_path": "C:\\damaihelper\\chromedriver.exe"
```

##### Mac/Linux配置
```bash
# 方法一：放在项目目录（推荐）
unzip chromedriver_mac64.zip
chmod +x chromedriver
mv chromedriver ./

# 方法二：放到系统PATH
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# 测试
chromedriver --version
```

### 步骤5：环境验证

```bash
# 创建测试脚本
python -c "
import selenium
print('✅ Selenium安装成功:', selenium.__version__)

try:
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.quit()
    print('✅ ChromeDriver配置成功')
except Exception as e:
    print('❌ ChromeDriver配置失败:', e)
"

# 如果都显示✅，说明环境配置完成
```

---

## ⚙️ 配置文件详解

### 步骤1：准备账户信息

#### 1.1 完成实名认证
1. 登录大麦网：https://www.damai.cn/
2. 进入"我的" → "实名认证"
3. 上传身份证照片完成认证
4. 等待审核通过（通常1-2小时）

#### 1.2 添加观影人信息
1. 进入大麦网APP → "我的" → "实名观影人"
2. 点击"添加观影人"
3. 填写观影人信息（姓名、身份证号）
4. 记录观影人序号（从1开始）

### 步骤2：获取目标演出信息

#### 2.1 找到正确的URL
```
✅ 正确格式：https://m.damai.cn/damai/detail/item.html?itemId=714001339730
❌ 错误格式：https://www.damai.cn/ （PC端链接）

获取方法：
1. 手机浏览器打开大麦网
2. 搜索目标演出
3. 进入购票页面
4. 复制完整URL（确保有itemId参数）
```

#### 2.2 确定抢票参数
- **日期序号**：查看演出有几个日期，记住想要的日期序号
- **场次序号**：查看当天有几个场次，记住想要的场次序号
- **价格档位**：查看有几个价格档位，记住想要的档位序号

### 步骤3：配置主要参数

#### 3.1 基础配置模板
```json
{
    "date": [14, 15, 16],
    "sess": [1, 2, 3],
    "price": [1, 2, 3, 4, 5],
    "ticket_num": 2,
    "viewer_person": [1, 2],
    "target_url": "https://m.damai.cn/damai/detail/item.html?itemId=714001339730",
    "auto_buy": true,
    "auto_buy_time": "08:29:57",
    "retry_interval": 3
}
```

#### 3.2 参数详细说明

| 参数 | 类型 | 说明 | 示例 | 必填 |
|------|------|------|------|------|
| `date` | 数组 | 日期优先级，按顺序尝试 | `[14, 15, 16]` | ✅ |
| `sess` | 数组 | 场次优先级，1最优 | `[1, 2, 3]` | ✅ |
| `price` | 数组 | 价格档位优先级 | `[1, 2, 3, 4]` | ✅ |
| `ticket_num` | 数字 | 购票数量 | `2` | ✅ |
| `viewer_person` | 数组 | 观影人序号列表 | `[1, 2]` | ✅ |
| `target_url` | 字符串 | 目标页面链接 | `"https://m.damai.cn/..."` | ✅ |
| `auto_buy` | 布尔值 | 是否自动抢票 | `true` | ✅ |
| `auto_buy_time` | 字符串 | 抢票时间 | `"08:29:57"` | ✅ |
| `retry_interval` | 数字 | 重试间隔(秒) | `3` | ✅ |

#### 3.3 高级配置选项

```json
{
    "driver_path": "C:\\damaihelper\\chromedriver.exe",
    "damai_url": "https://www.damai.cn/",
    "proxy": {
        "enabled": true,
        "proxy_ip": "192.168.1.100",
        "proxy_port": "8080",
        "proxy_type": "HTTPS",
        "proxy_list": [
            "192.168.1.100:8080",
            "203.0.113.50:3128",
            "198.51.100.1:1080"
        ]
    },
    "captcha": {
        "enabled": true,
        "method": "OCR",
        "ocr_service": "baidu"
    }
}
```

### 步骤4：多账户配置

```json
{
    "accounts": [
        {
            "username": "user1@damai.com",
            "password": "password1",
            "auto_buy_time": "08:30:00",
            "viewer_person": [1, 2],
            "target_url": "https://m.damai.cn/damai/detail/item.html?itemId=714001339730"
        },
        {
            "username": "user2@damai.com",
            "password": "password2",
            "auto_buy_time": "08:31:00",
            "viewer_person": [3, 4],
            "target_url": "https://m.damai.cn/damai/detail/item.html?itemId=714001339730"
        }
    ]
}
```

### 步骤5：配置文件验证

```bash
# 测试配置文件是否正确
python scripts/test_config.py

# 预期输出：
# 正在加载配置文件...
# ✅ 配置文件加载成功！
# 📋 账户数量: 2
# 🎫 购票数量: 2
# ⏰ 自动抢票时间: 08:30:00
# 🔄 重试间隔: 3秒
```

---

## 🖥️ 运行方式

### 方式一：图形界面模式（推荐新手）

#### 步骤1：启动GUI
```bash
python GUI.py
```

#### 步骤2：界面操作流程
1. **登录信息区**：
   - 填入票务页面URL
   - 设置抢票时间（格式：HH:MM:SS）

2. **场次管理区**：
   - 选择想要的场次（可多选）
   - 优先选择最想要的场次

3. **代理设置区**：
   - 可选择是否启用代理IP
   - 填入代理IP和端口

4. **任务控制区**：
   - 勾选"启用自动抢票"
   - 点击"开始抢票"按钮

5. **监控状态**：
   - 观察状态栏和进度条
   - 查看日志区域的详细输出

#### 步骤3：配置保存和加载
- **保存配置**：文件 → 保存配置
- **加载配置**：文件 → 加载配置
- 配置文件保存为`config.json`

### 方式二：命令行模式（传统）

#### 步骤1：基本运行
```bash
# 进入项目根目录
cd damaihelper

# 运行抢票脚本
python ticket_script.py
```

#### 步骤2：多账户运行
```bash
# 多账户抢票
python ticket_script.py --multi-account

# 使用自定义配置文件
python ticket_script.py --config custom_config.json
```

#### 步骤3：首次登录
1. 浏览器自动打开并跳转到登录页面
2. **手动扫码登录**（推荐）或使用账号密码登录
3. 登录成功后，脚本自动保存Cookie
4. 下次运行无需重新登录

### 方式三：现代模块化模式

#### 步骤1：模块化运行
```bash
# 运行模块化架构
python scripts/main.py
```

#### 步骤2：优势说明
- **更好的错误处理**：详细的错误日志和异常处理
- **模块化设计**：各功能独立，便于维护和扩展
- **多线程支持**：更好的并发处理能力
- **配置验证**：自动验证配置文件格式

---

## 🎯 使用教程

### 完整抢票流程

#### 阶段1：抢票前24小时 - 准备工作

1. **环境搭建**（1小时）
   ```bash
   # 1.1 下载项目
   git clone https://github.com/Guyungy/damaihelper.git
   cd damaihelper

   # 1.2 安装依赖
   pip install -r requirements.txt

   # 1.3 下载ChromeDriver
   # 访问：http://chromedriver.storage.googleapis.com/index.html
   # 下载与Chrome版本匹配的驱动

   # 1.4 环境测试
   python scripts/test_config.py
   ```

2. **账户准备**（10分钟）
   - 完成实名认证（如未完成）
   - 添加观影人信息
   - 记录观影人序号

3. **获取信息**（15分钟）
   - 获取目标演出URL
   - 确定开售时间
   - 分析日期、场次、价格档位

#### 阶段2：抢票前1小时 - 配置测试

1. **配置文件设置**（10分钟）
   ```json
   {
       "date": [14],
       "sess": [1, 2],
       "price": [1, 2, 3],
       "ticket_num": 1,
       "viewer_person": [1],
       "target_url": "https://m.damai.cn/damai/detail/item.html?itemId=XXXXX",
       "auto_buy": true,
       "auto_buy_time": "08:29:57",
       "retry_interval": 3
   }
   ```

2. **配置验证**（5分钟）
   ```bash
   # 验证配置文件
   python scripts/test_config.py

   # 测试运行（非抢票时间）
   python GUI.py
   # 点击"开始抢票"测试连接
   ```

3. **登录测试**（10分钟）
   - 运行脚本测试登录
   - 确保Cookie正常保存
   - 验证目标页面可访问

#### 阶段3：抢票前10分钟 - 最后准备

1. **启动程序**（2分钟）
   ```bash
   # 选择运行方式
   python GUI.py  # 推荐
   # 或
   python ticket_script.py
   ```

2. **最终检查**（5分钟）
   - [ ] 配置文件正确
   - [ ] ChromeDriver版本匹配
   - [ ] 网络连接稳定
   - [ ] 账户登录状态正常
   - [ ] 抢票时间设置正确

3. **等待开始**（3分钟）
   - 监控程序状态
   - 观察时间倒计时
   - 确保浏览器已启动

#### 阶段4：抢票进行中 - 监控执行

1. **启动抢票**
   ```bash
   # 在抢票时间前2-3秒点击开始
   # GUI界面：点击"开始抢票"按钮
   # 命令行：脚本会自动在指定时间开始
   ```

2. **监控过程**
   - **浏览器操作**：观察浏览器自动操作
   - **状态监控**：查看GUI状态栏或命令行输出
   - **日志观察**：关注错误和警告信息

3. **抢票阶段**
   - **0-30%**：页面加载和初始化
   - **30-70%**：场次选择和票价选择
   - **70-90%**：观影人选择和订单确认
   - **90-100%**：跳转到支付页面

#### 阶段5：抢票成功 - 后续处理

1. **立即处理**（重要！）
   ```
   ⚠️  注意：抢票成功后必须在15分钟内完成支付！
   ⚠️  超时未支付，票会被释放！
   ```

2. **支付步骤**（10分钟）
   - 检查订单信息
   - 选择支付方式
   - 完成支付
   - 保存订单截图

3. **清理工作**（5分钟）
   - 关闭抢票程序
   - 清理浏览器窗口
   - 保存票据信息

### 使用技巧和最佳实践

#### 🎯 提高成功率的技巧

1. **时间设置优化**
   ```json
   {
       "auto_buy_time": "08:29:57",  // 提前3秒
       "retry_interval": 1           // 最快重试间隔
   }
   ```

2. **选择策略优化**
   ```json
   {
       "date": [14, 15, 16],        // 多个日期
       "sess": [1, 2, 3, 4],       // 多个场次
       "price": [1, 2, 3, 4, 5],    // 多个价格档位
       "ticket_num": 1              // 单张票成功率更高
   }
   ```

3. **网络优化**
   ```json
   {
       "proxy": {
           "enabled": true,
           "proxy_list": [
               "高速代理IP1:8080",
               "高速代理IP2:8080"
           ]
       }
   }
   ```

#### 🔄 多账户策略

1. **时间错开**
   ```json
   {
       "accounts": [
           {
               "auto_buy_time": "08:29:57"  // 账户1
           },
           {
               "auto_buy_time": "08:30:02"  // 账户2，错开5秒
           }
       ]
   }
   ```

2. **不同优先级**
   ```json
   {
       "accounts": [
           {
               "sess": [1, 2],     // 账户1：优先场次1
               "price": [1, 2]    // 账户1：优先价格1
           },
           {
               "sess": [3, 4],     // 账户2：优先场次3
               "price": [3, 4]    // 账户2：优先价格3
           }
       ]
   }
   ```

---

## 📱 平台特定配置

### 大麦网配置（最常用）

#### 基本配置
```json
{
    "platform": "damai",
    "damai_url": "https://www.damai.cn/",
    "target_url": "https://m.damai.cn/damai/detail/item.html?itemId=714001339730",
    "login": {
        "method": "scan",           // 扫码登录（推荐）
        "qr_code": true,
        "sms_fallback": true        // 短信登录备用
    },
    "captcha": {
        "enabled": true,
        "method": "OCR",
        "ocr_service": "baidu",
        "manual_fallback": true    // OCR失败时手动输入
    }
}
```

#### 反检测配置
```json
{
    "anti_detection": {
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
        "viewport": {"width": 375, "height": 667},
        "random_delay": {"min": 100, "max": 500},
        "mouse_simulation": true,
        "keyboard_simulation": true
    }
}
```

### 淘票票配置

#### 基本配置
```json
{
    "platform": "taopiaopiao",
    "target_url": "https://m.taopiaopiao.com/damai/detail/item.html?itemId=987654321",
    "login": {
        "method": "sms",           // 短信验证登录
        "phone_number": "13800000000",
        "auto_sms": true
    },
    "captcha": {
        "enabled": false           // 淘票票通常无验证码
    },
    "platform_specific": {
        "app_name": "淘票票",
        "package": "com.taobao.movie"
    }
}
```

### 缤玩岛配置

#### 基本配置
```json
{
    "platform": "binwandao",
    "target_url": "https://m.binwandao.com/event/detail/itemId=6789012345",
    "login": {
        "method": "scan",           // 扫码登录
        "login_url": "https://m.binwandao.com/login"
    },
    "captcha": {
        "enabled": true,
        "method": "manual",        // 手动处理验证码
        "manual_prompt": true
    },
    "proxy": {
        "enabled": false           // 缤玩岛不建议使用代理
    }
}
```

---

## 🔧 故障排除

### 常见错误及解决方案

#### 1. 环境问题

##### ChromeDriver版本不匹配
```bash
# 错误信息：
# ChromeDriver version mismatch

# 解决步骤：
1. 检查Chrome版本：google-chrome --version
2. 下载匹配版本的ChromeDriver
3. 替换项目中的chromedriver文件

# 验证修复：
chromedriver --version  # 应该显示与Chrome匹配的版本
```

##### Python依赖缺失
```bash
# 错误信息：
# ModuleNotFoundError: No module named 'selenium'

# 解决方案：
pip install -r requirements.txt

# 如果pip安装失败：
pip install selenium==4.1.0 apscheduler==3.8.0 pytesseract==0.3.8 pillow==8.4.0

# 国内用户使用镜像：
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 2. 配置问题

##### 配置文件找不到
```bash
# 错误信息：
# FileNotFoundError: config.json

# 解决方案：
1. 确保在项目根目录运行脚本
2. 检查config/config.json文件是否存在
3. 验证文件路径和权限

# 验证方法：
ls -la config/config.json
```

##### JSON格式错误
```bash
# 错误信息：
# JSONDecodeError: Expecting ',' delimiter

# 解决方案：
1. 使用在线JSON验证工具检查格式
2. 检查逗号、引号、括号是否正确
3. 确保文件编码为UTF-8

# 常见错误：
❌ {"key": "value" "key2": "value2"}  // 缺少逗号
✅ {"key": "value", "key2": "value2"}  // 正确
```

#### 3. 登录问题

##### Cookie过期
```bash
# 错误信息：
# Login failed / Session expired

# 解决方案：
1. 删除旧的Cookie文件
   rm cookies.pkl

2. 重新运行脚本并手动登录
   python ticket_script.py

3. 登录成功后会自动保存新的Cookie
```

##### 登录页面变化
```bash
# 错误信息：
# Element not found: login_button

# 解决方案：
1. 更新页面元素定位器
2. 检查登录方式是否改变
3. 可能需要手动登录一次
```

#### 4. 抢票问题

##### 元素定位失败
```bash
# 错误信息：
# NoSuchElementException: Unable to locate element

# 解决方案：
1. 检查target_url是否正确
2. 确认使用手机端URL（m.damai.cn）
3. 等待页面完全加载
4. 检查页面结构是否变化

# 调试方法：
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 显式等待元素
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "buy-button"))
)
```

##### 页面跳转错误
```bash
# 错误信息：
# Timeout loading page

# 解决方案：
1. 检查网络连接
2. 验证URL是否有效
3. 增加页面加载超时时间
4. 检查是否有网络代理限制
```

### 性能优化建议

#### 1. 网络优化
```json
{
    "network": {
        "timeout": 30,
        "retry_times": 3,
        "connection_pool_size": 10,
        "keep_alive": true
    }
}
```

#### 2. 浏览器优化
```json
{
    "chrome_options": {
        "disable_images": true,
        "disable_css": false,
        "disable_javascript": false,
        "headless": false,           // 调试时设为false
        "disable_gpu": false,
        "no_sandbox": true,
        "disable_dev_shm_usage": true
    }
}
```

#### 3. 并发优化
```json
{
    "concurrency": {
        "max_workers": 3,
        "account_interval": 5,       // 账户间隔（秒）
        "request_interval": 0.5       // 请求间隔（秒）
    }
}
```

---

## ⚠️ 安全注意事项

### 合规使用指南

#### ✅ 允许的操作
- 个人合法购票需求
- 学习自动化技术
- 提高购票效率
- 非商业目的使用

#### ❌ 禁止的操作
- 高频率恶意请求
- 商业用途倒票
- 违反平台服务条款
- 影响平台正常运行
- 账户间的恶意竞争

### 安全使用建议

#### 1. 账户安全
```json
{
    "security": {
        "use_dedicated_account": true,    // 使用专用账户
        "enable_2fa": true,               // 启用二次验证
        "password_strength": "strong",     // 使用强密码
        "avoid_shared_accounts": true      // 避免共享账户
    }
}
```

#### 2. 频率控制
```json
{
    "rate_limiting": {
        "requests_per_minute": 10,        // 每分钟请求数
        "account_interval": 30,           // 账户间隔（秒）
        "daily_limit": 100,              // 每日请求上限
        "respect_server_limits": true      // 遵守服务器限制
    }
}
```

#### 3. 数据保护
```json
{
    "data_protection": {
        "encrypt_config": false,          // 配置文件加密（开发中）
        "mask_sensitive_data": true,      // 日志中隐藏敏感信息
        "cleanup_temp_files": true,       // 清理临时文件
        "secure_cookie_storage": true     // 安全的Cookie存储
    }
}
```

### 法律和道德责任

#### 使用限制
1. **仅限个人使用**：不得用于商业倒票
2. **遵守平台规则**：遵守各平台使用条款
3. **尊重他人权益**：不得恶意影响他人抢票
4. **风险自担**：使用本工具产生的任何后果由用户自行承担

#### 免责声明
```
本工具仅用于个人学习和合法购票需求。

开发者不承担以下责任：
- 账户被封禁的风险
- 抢票失败的损失
- 违反平台规定的后果
- 商业用途的法律责任

用户使用本工具即表示同意：
1. 仅用于合法个人购票
2. 遵守平台服务条款
3. 自行承担使用风险
4. 不进行商业倒票活动
```

### 最佳实践建议

#### 1. 账户管理
- 使用专门用于抢票的账户
- 定期更换密码，增强安全性
- 为不同平台使用不同账户
- 避免在公共网络下操作

#### 2. 技术优化
- 使用稳定的网络环境
- 定期更新ChromeDriver版本
- 监控目标平台页面变化
- 备份重要的配置文件

#### 3. 风险控制
- 不要在关键时刻才测试
- 准备多个备用方案
- 避免同时运行多个实例
- 及时关注平台反爬策略更新

---

## 📞 技术支持

### 获取帮助
- **GitHub Issues**: https://github.com/Guyungy/damaihelper/issues
- **项目文档**: 查看项目根目录的`CLAUDE.md`
- **配置示例**: 查看`config/`目录的示例文件

### 贡献指南
欢迎提交Bug报告、功能建议和代码贡献！

### 更新记录
- **2024年12月**: 增加渠道切换功能，修复页面刷新和按钮定位问题
- **2024年4月**: 增加选座购买功能和代理IP池
- **2023年9月**: 优化抢票算法，支持时间段设置

---

## 🎉 结语

**抢票助手 V5.0** 旨在为用户提供高效、稳定的抢票解决方案。通过合理配置和使用，可以显著提高抢票成功率。

**记住**：
- ⏰ **提前准备**：充分的环境准备和配置测试
- 🎯 **合理配置**：根据实际情况优化参数
- 🔒 **合规使用**：遵守平台规则，仅用于个人需求
- 🚀 **持续优化**：根据使用效果不断调整策略

**祝您抢票成功！** 🎫✨

---

**免责声明**：本工具仅用于个人学习软件界面设计和合法购票需求。如他人用本仓库代码用于商业用途，侵犯到大麦网等平台利益，本人不承担任何责任。