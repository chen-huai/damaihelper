#!/usr/bin/env python3
"""
Web版本的抢票助手GUI
当tkinter无法正常工作时使用此版本
"""

import json
import threading
import time
from flask import Flask, render_template_string, request, jsonify
import webbrowser
import os

app = Flask(__name__)

# 配置数据
config_data = {
    "url": "",
    "time": "",
    "proxy_ip": "",
    "proxy_port": "",
    "auto_buy": False,
    "sessions": [],
    "status": "未开始",
    "progress": 0,
    "logs": []
}

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>抢票助手 V5.0 - Web版</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; color: white; margin-bottom: 30px; }
        .header h1 { font-size: 3em; margin-bottom: 10px; }
        .card { background: white; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); padding: 30px; margin-bottom: 20px; }
        .card h2 { color: #333; margin-bottom: 20px; font-size: 1.5em; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 14px; }
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus { border-color: #667eea; outline: none; }
        .checkbox-group { display: flex; align-items: center; margin-bottom: 15px; }
        .checkbox-group input { margin-right: 10px; }
        .button { background: #667eea; color: white; border: none; padding: 12px 30px; border-radius: 5px; cursor: pointer; font-size: 16px; margin-right: 10px; }
        .button:hover { background: #5a67d8; }
        .button.stop { background: #e74c3c; }
        .button.stop:hover { background: #c0392b; }
        .button.retry { background: #f39c12; }
        .button.retry:hover { background: #e67e22; }
        .status-bar { background: #f8f9fa; border-radius: 5px; padding: 15px; margin-bottom: 20px; }
        .progress-container { margin-top: 10px; }
        .progress-bar { width: 100%; height: 20px; background: #ecf0f1; border-radius: 10px; overflow: hidden; }
        .progress-fill { height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); transition: width 0.3s ease; }
        .log-container { height: 300px; overflow-y: auto; background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; font-family: monospace; }
        .log-entry { margin-bottom: 5px; padding: 2px 0; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .full-width { grid-column: 1 / -1; }
        @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎫 抢票助手 V5.0</h1>
            <p>Web版界面 - 适用于GUI无法启动的情况</p>
        </div>

        <div class="status-bar">
            <h3>📊 当前状态: <span id="status">{{ status }}</span></h3>
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" id="progress" style="width: {{ progress }}%"></div>
                </div>
                <p>进度: <span id="progress-text">{{ progress }}%</span></p>
            </div>
        </div>

        <div class="grid">
            <!-- 登录信息 -->
            <div class="card">
                <h2>🔐 登录信息</h2>
                <div class="form-group">
                    <label for="url">票务页面 URL</label>
                    <input type="text" id="url" value="{{ url }}" placeholder="https://m.damai.cn/damai/detail/item.html?itemId=...">
                </div>
                <div class="form-group">
                    <label for="time">抢票时间 (HH:MM:SS)</label>
                    <input type="text" id="time" value="{{ time }}" placeholder="08:29:57">
                </div>
            </div>

            <!-- 任务控制 -->
            <div class="card">
                <h2>⚙️ 任务控制</h2>
                <div class="checkbox-group">
                    <input type="checkbox" id="auto_buy" {% if auto_buy %}checked{% endif %}>
                    <label for="auto_buy">启用自动抢票</label>
                </div>
                <div style="margin-top: 20px;">
                    <button class="button" onclick="startTask()">🚀 开始抢票</button>
                    <button class="button stop" onclick="stopTask()">⏹ 停止任务</button>
                    <button class="button retry" onclick="retryTask()">🔄 重试任务</button>
                </div>
            </div>

            <!-- 场次管理 -->
            <div class="card">
                <h2>🎭 场次管理</h2>
                <div class="form-group">
                    <label>选择场次（可多选）</label>
                    <div style="max-height: 200px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
                        {% for i in range(1, 21) %}
                        <div class="checkbox-group">
                            <input type="checkbox" id="session_{{ i }}" {% if i in sessions %}checked{% endif %}>
                            <label for="session_{{ i }}">场次 {{ i }}</label>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>

            <!-- 代理设置 -->
            <div class="card">
                <h2>🌐 代理设置</h2>
                <div class="checkbox-group">
                    <input type="checkbox" id="proxy_enabled">
                    <label for="proxy_enabled">启用代理 IP</label>
                </div>
                <div class="form-group">
                    <label for="proxy_ip">代理 IP</label>
                    <input type="text" id="proxy_ip" value="{{ proxy_ip }}" placeholder="192.168.1.100">
                </div>
                <div class="form-group">
                    <label for="proxy_port">代理端口</label>
                    <input type="text" id="proxy_port" value="{{ proxy_port }}" placeholder="8080">
                </div>
            </div>
        </div>

        <!-- 配置管理 -->
        <div class="card full-width">
            <h2>💾 配置管理</h2>
            <div style="margin-top: 20px;">
                <button class="button" onclick="saveConfig()">💾 保存配置</button>
                <button class="button" onclick="loadConfig()">📁 加载配置</button>
            </div>
        </div>

        <!-- 日志区域 -->
        <div class="card full-width">
            <h2>📝 日志输出</h2>
            <div class="log-container" id="log-container">
                {% for log in logs %}
                <div class="log-entry">{{ log }}</div>
                {% endfor %}
            </div>
        </div>
    </div>

    <script>
        // 自动刷新状态和日志
        setInterval(updateStatus, 2000);

        function updateStatus() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('status').textContent = data.status;
                    document.getElementById('progress').style.width = data.progress + '%';
                    document.getElementById('progress-text').textContent = data.progress + '%';

                    // 更新日志
                    const logContainer = document.getElementById('log-container');
                    data.logs.slice(-10).forEach(log => {
                        const logEntry = document.createElement('div');
                        logEntry.className = 'log-entry';
                        logEntry.textContent = log;
                        logContainer.appendChild(logEntry);
                    });
                    logContainer.scrollTop = logContainer.scrollHeight;
                });
        }

        function startTask() {
            const config = getConfig();
            fetch('/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(config)
            });
        }

        function stopTask() {
            fetch('/stop', {method: 'POST'});
        }

        function retryTask() {
            fetch('/retry', {method: 'POST'});
        }

        function saveConfig() {
            const config = getConfig();
            fetch('/save_config', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(config)
            }).then(() => alert('配置已保存！'));
        }

        function loadConfig() {
            fetch('/load_config', {method: 'POST'})
                .then(response => response.json())
                .then(config => {
                    document.getElementById('url').value = config.url || '';
                    document.getElementById('time').value = config.time || '';
                    document.getElementById('proxy_ip').value = config.proxy_ip || '';
                    document.getElementById('proxy_port').value = config.proxy_port || '';
                    document.getElementById('auto_buy').checked = config.auto_buy || false;

                    // 设置场次选择
                    for (let i = 1; i <= 20; i++) {
                        const checkbox = document.getElementById('session_' + i);
                        if (checkbox) {
                            checkbox.checked = config.sessions.includes(i);
                        }
                    }

                    alert('配置已加载！');
                });
        }

        function getConfig() {
            const sessions = [];
            for (let i = 1; i <= 20; i++) {
                const checkbox = document.getElementById('session_' + i);
                if (checkbox && checkbox.checked) {
                    sessions.push(i);
                }
            }

            return {
                url: document.getElementById('url').value,
                time: document.getElementById('time').value,
                proxy_ip: document.getElementById('proxy_ip').value,
                proxy_port: document.getElementById('proxy_port').value,
                auto_buy: document.getElementById('auto_buy').checked,
                sessions: sessions
            };
        }
    </script>
</body>
</html>
"""

def add_log(message):
    """添加日志"""
    config_data["logs"].append(f"[{time.strftime('%H:%M:%S')}] {message}")
    if len(config_data["logs"]) > 100:  # 保持最多100条日志
        config_data["logs"] = config_data["logs"][-100:]

def simulate_task():
    """模拟抢票任务"""
    add_log("任务开始！")
    config_data["status"] = "抢票进行中"

    for i in range(1, 101):
        time.sleep(0.1)
        config_data["progress"] = i
        if i == 50:
            add_log("正在选择场次...")
        elif i == 80:
            add_log("正在确认订单...")

    add_log("任务完成！")
    config_data["status"] = "任务完成"
    config_data["progress"] = 0

@app.route('/')
def index():
    """主页面"""
    return render_template_string(HTML_TEMPLATE, **config_data)

@app.route('/status')
def get_status():
    """获取状态"""
    return jsonify({
        "status": config_data["status"],
        "progress": config_data["progress"],
        "logs": config_data["logs"]
    })

@app.route('/start', methods=['POST'])
def start_task():
    """开始任务"""
    if config_data["status"] != "抢票进行中":
        # 更新配置
        config_data.update(request.get_json())
        # 启动任务线程
        thread = threading.Thread(target=simulate_task)
        thread.daemon = True
        thread.start()
    return jsonify({"success": True})

@app.route('/stop', methods=['POST'])
def stop_task():
    """停止任务"""
    config_data["status"] = "任务已停止"
    config_data["progress"] = 0
    add_log("任务已停止！")
    return jsonify({"success": True})

@app.route('/retry', methods=['POST'])
def retry_task():
    """重试任务"""
    add_log("正在重试任务...")
    return start_task()

@app.route('/save_config', methods=['POST'])
def save_config():
    """保存配置"""
    try:
        config_file = "config.json"
        save_data = request.get_json()
        # 添加一些默认配置
        full_config = {
            "url": save_data.get("url", ""),
            "time": save_data.get("time", ""),
            "auto_buy": save_data.get("auto_buy", False),
            "sess": save_data.get("sessions", []),
            "proxy": {
                "enabled": bool(save_data.get("proxy_ip", "")),
                "proxy_ip": save_data.get("proxy_ip", ""),
                "proxy_port": save_data.get("proxy_port", "")
            }
        }

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(full_config, f, indent=2, ensure_ascii=False)

        add_log("配置已保存到 config.json")
        return jsonify({"success": True})
    except Exception as e:
        add_log(f"保存配置失败: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/load_config', methods=['POST'])
def load_config():
    """加载配置"""
    try:
        config_file = "config.json"
        if os.path.exists(config_file):
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)

            # 转换格式以适配前端
            frontend_config = {
                "url": config.get("url", ""),
                "time": config.get("time", ""),
                "auto_buy": config.get("auto_buy", False),
                "sessions": config.get("sess", []),
                "proxy_ip": config.get("proxy", {}).get("proxy_ip", ""),
                "proxy_port": config.get("proxy", {}).get("proxy_port", "")
            }

            add_log("配置已加载成功")
            return jsonify(frontend_config)
        else:
            add_log("配置文件未找到")
            return jsonify({})
    except Exception as e:
        add_log(f"加载配置失败: {e}")
        return jsonify({})

def main():
    """主函数"""
    print("🚀 正在启动抢票助手Web版...")
    print("=" * 50)
    print("Web版界面功能:")
    print("✅ 完整的图形化界面")
    print("✅ 实时状态监控")
    print("✅ 配置保存/加载")
    print("✅ 日志实时显示")
    print("=" * 50)

    # 添加初始日志
    add_log("Web界面启动成功")
    add_log("欢迎使用抢票助手 V5.0")

    # 自动打开浏览器
    def open_browser():
        time.sleep(1)  # 等待服务器启动
        webbrowser.open("http://localhost:5000")

    thread = threading.Thread(target=open_browser)
    thread.daemon = True
    thread.start()

    print("🌐 Web界面地址: http://localhost:5000")
    print("📱 也可以从手机访问: http://你的IP地址:5000")
    print("⏹ 按 Ctrl+C 停止服务")
    print("=" * 50)

    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 用户中断服务，正在关闭...")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("💡 解决方案:")
        print("1. 检查端口5000是否被占用")
        print("2. 尝试使用: python web_gui.py")
        print("3. 回到命令行模式: python ticket_script.py")

if __name__ == "__main__":
    main()