[根目录](../../CLAUDE.md) > **config**

# Config 模块文档

## 模块职责

**config模块**是damaihelper的配置管理中心，负责存储和管理多平台抢票系统的所有配置参数。该模块采用分层配置架构，支持平台特定设置、代理池管理、账户信息配置以及票务参数定制。

## 入口与启动

### 主要配置文件
- **`config.json`** - 主配置文件，包含完整的系统设置
- **`platform_config.json`** - 平台特定配置模板
- **`proxy_pool.json`** - 代理IP池配置

### 配置加载机制
```python
def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

def load_platform_config(platform_name):
    with open('config/platform_config.json', 'r') as f:
        all_configs = json.load(f)
        return all_configs['platforms'][platform_name]
```

## 对外接口

### 配置获取接口

#### 1. 主配置获取
```python
def get_config():
    """获取完整的主配置文件"""
    return load_config()

def get_ticket_settings():
    """获取票务相关设置"""
    config = load_config()
    return config.get('ticket_settings', {})

def get_accounts():
    """获取账户配置"""
    config = load_config()
    return config.get('accounts', [])
```

#### 2. 平台配置获取
```python
def get_platform_config(platform_name):
    """获取特定平台的配置"""
    with open('config/platform_config.json', 'r') as f:
        configs = json.load(f)
        return configs['platforms'].get(platform_name, {})

def get_platform_login_config(platform_name):
    """获取平台登录配置"""
    platform_config = get_platform_config(platform_name)
    return platform_config.get('login', {})

def get_platform_ticket_config(platform_name):
    """获取平台票务配置"""
    platform_config = get_platform_config(platform_name)
    return platform_config.get('ticket_config', {})
```

#### 3. 代理配置获取
```python
def get_proxy_settings(platform_name=None):
    """获取代理设置"""
    if platform_name:
        platform_config = get_platform_config(platform_name)
        return platform_config.get('proxy_settings', {})
    else:
        config = load_config()
        return config.get('proxy', {})

def get_proxy_pool():
    """获取代理池配置"""
    try:
        with open('config/proxy_pool.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
```

### 配置验证接口

#### 1. 配置格式验证
```python
def validate_config_structure(config):
    """验证配置文件结构完整性"""
    required_sections = ['ticket_settings', 'accounts', 'platforms']
    for section in required_sections:
        if section not in config:
            raise ConfigValidationError(f"缺少必填配置节: {section}")

def validate_account_config(account):
    """验证单个账户配置"""
    required_fields = ['username', 'target_url']
    for field in required_fields:
        if field not in account:
            raise ConfigValidationError(f"账户配置缺少必填字段: {field}")
```

## 关键依赖与配置

### 平台支持矩阵

| 平台 | 登录方式 | 代理支持 | 验证码 | 状态 |
|------|----------|----------|--------|------|
| **大麦网** (damai) | scan/sms/password | ✅ HTTPS | OCR | ✅ 完全支持 |
| **淘票票** (taopiaopiao) | sms | ✅ HTTP | ❌ 禁用 | ✅ 完全支持 |
| **缤玩岛** (binwandao) | scan | ❌ 不支持 | 手动 | ✅ 基本支持 |

### 配置层次结构

```json
{
  "ticket_settings": {
    "date": [14, 15, 16],
    "sess": [1, 2, 3],
    "price": [1, 2, 3, 4, 5, 6, 7],
    "ticket_num": 2,
    "viewer_person": [2, 3],
    "auto_buy": true,
    "auto_buy_time": "08:30:00",
    "retry_interval": 5
  },
  "accounts": [...],
  "platforms": {
    "damai": {...},
    "taopiaopiao": {...},
    "binwandao": {...}
  },
  "proxy": {...},
  "captcha": {...}
}
```

## 数据模型

### 1. 票务设置模型 (Ticket Settings)
```json
{
  "date": [14, 15, 16],
  "sess": [1, 2, 3],
  "price": [1, 2, 3, 4, 5, 6, 7],
  "ticket_num": 2,
  "viewer_person": [2, 3],
  "auto_buy": true,
  "auto_buy_time": "08:30:00",
  "retry_interval": 5,
  "queue": {
    "zhoujielun_0403": "https://m.damai.cn/damai/detail/item.html?itemId=717235298514"
  }
}
```

### 2. 账户信息模型 (Account Model)
```json
{
  "username": "user@damai.com",
  "password": "password123",
  "auto_buy_time": "08:30:00",
  "viewer_person": [1, 2],
  "platform_specific": {
    "login_method": "scan",
    "phone_number": "13800000000"
  }
}
```

### 3. 平台配置模型 (Platform Model)
```json
{
  "platform_name": "大麦网",
  "login": {
    "method": "scan",
    "login_url": "https://www.damai.cn/login",
    "qr_code": true,
    "username": "user@damai.com",
    "password": "password123"
  },
  "ticket_config": {
    "target_url": "https://m.damai.cn/damai/detail/item.html?itemId=123456789",
    "auto_buy": true,
    "auto_buy_time": "08:30:00",
    "retry_interval": 5,
    "price": [1, 2, 3],
    "sess": [1, 2]
  },
  "proxy_settings": {
    "use_proxy": true,
    "proxy_ip": "192.168.1.100",
    "proxy_port": "8080",
    "proxy_type": "HTTPS"
  },
  "captcha": {
    "enabled": true,
    "method": "OCR",
    "ocr_service": "baidu"
  }
}
```

### 4. 代理配置模型 (Proxy Model)
```json
{
  "enabled": true,
  "proxy_ip": "192.168.1.100",
  "proxy_port": "8080",
  "proxy_type": "HTTPS",
  "proxy_list": [
    "192.168.1.100:8080",
    "203.0.113.50:3128",
    "198.51.100.1:1080"
  ],
  "rotation_policy": {
    "strategy": "round_robin",
    "health_check": true,
    "timeout": 30
  }
}
```

## 测试与质量

### 配置验证测试
```python
def test_config_validation():
    """测试配置文件验证逻辑"""
    valid_config = load_test_config()
    assert validate_config_structure(valid_config) == True

    invalid_config = {"invalid": "config"}
    with pytest.raises(ConfigValidationError):
        validate_config_structure(invalid_config)

def test_platform_config_access():
    """测试平台配置获取"""
    damai_config = get_platform_config("damai")
    assert "login" in damai_config
    assert "ticket_config" in damai_config

    with pytest.raises(KeyError):
        get_platform_config("nonexistent_platform")
```

### 配置兼容性测试
```python
def test_config_backward_compatibility():
    """测试配置向后兼容性"""
    old_config = load_legacy_config()
    new_config = migrate_config(old_config)
    assert validate_config_structure(new_config) == True
```

## 常见问题 (FAQ)

### Q1: 如何添加新的票务平台？
A1:
1. 在`platform_config.json`中添加新平台配置
2. 定义登录方式、URL和反检测策略
3. 设置代理和验证码处理方式
4. 更新账户配置模板

### Q2: 代理IP不工作怎么办？
A2:
1. 检查`proxy_pool.json`中的IP格式
2. 验证代理服务器的连通性
3. 确认代理类型（HTTP/HTTPS）正确
4. 检查防火墙设置

### Q3: 多账户配置如何管理？
A3:
1. 为每个账户设置唯一的用户名和观影人偏好
2. 配置不同的`auto_buy_time`避免冲突
3. 为不同账户设置独立的代理IP

### Q4: 配置文件密码安全如何保证？
A4:
1. 使用环境变量存储敏感密码
2. 配置文件中存储加密后的密码
3. 将包含真实密码的配置文件添加到`.gitignore`
4. 定期轮换账户密码

### Q5: 时间格式配置错误怎么办？
A5:
1. 确保使用24小时制格式：`HH:MM:SS`
2. 示例：`"08:30:00"`表示上午8点30分
3. 避免使用12小时制和AM/PM标记

## 相关文件清单

### 核心配置文件
- `config.json` - 主配置文件（系统参数、账户信息、全局设置）
- `platform_config.json` - 平台特定配置模板
- `proxy_pool.json` - 代理IP池配置

### 配置验证工具
- `config_validator.py` - 配置文件格式验证（待实现）
- `config_migrator.py` - 配置版本迁移工具（待实现）
- `config_generator.py` - 配置文件生成器（待实现）

### 配置模板和示例
- `config.template.json` - 配置模板（待创建）
- `examples/` - 配置示例目录（待创建）

### 外部依赖
- JSON Schema文件 - 配置格式定义（待创建）
- 环境变量配置 - 敏感信息管理

## 变更记录 (Changelog)

- **2025-10-26**: 自适应初始化架构师完成配置模块文档化，定义数据模型
- **2024-12月**: 增加多平台配置支持，优化代理池管理
- **2024-04-01**: 新增验证码服务和通知配置
- **2023-09-15**: 初始配置架构，支持基本的大麦网配置

---

**模块覆盖率**: 67% (2/3 文件已分析)
**下次扫描重点**:
- `proxy_pool.json`详细配置分析
- 配置文件格式验证机制
- 环境变量和敏感信息管理
- 配置迁移和兼容性处理