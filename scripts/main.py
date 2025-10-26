import json
import os
import time
from appium_simulator import start_simulation
from selenium_driver import start_selenium_driver
from multi_account_manager import manage_multiple_accounts
from scheduler import schedule_tasks
from captcha_solver import solve_captcha

def load_config():
    # 获取项目根目录路径，无论从哪个目录运行脚本都能正确找到配置文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    config_path = os.path.join(project_root, 'config', 'config.json')

    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    config = load_config()

    # 从配置中获取票务设置（兼容实际配置文件结构）
    ticket_settings = {
        'date': config.get('date', []),
        'sess': config.get('sess', []),
        'price': config.get('price', []),
        'ticket_num': config.get('ticket_num', 1),
        'viewer_person': config.get('viewer_person', []),
        'auto_buy': config.get('auto_buy', False),
        'auto_buy_time': config.get('auto_buy_time', '08:30:00'),
        'retry_interval': config.get('retry_interval', 5),
        'proxy': config.get('proxy', {}).get('enabled', False),
        'damai_url': config.get('damai_url', ''),
        'target_url': config.get('target_url', '')
    }

    accounts = config.get('accounts', [])

    # 处理代理池
    if ticket_settings['proxy']:
        print("使用代理IP池")
        # 初始化代理池

    # 调度抢票任务
    schedule_tasks(ticket_settings['retry_interval'], ticket_settings['auto_buy_time'])

    # 启动抢票操作
    for i, account_info in enumerate(accounts):
        account_id = account_info.get('username', f'account_{i}')
        print(f"开始为账户 {account_id} 执行抢票任务")
        manage_multiple_accounts(account_info, ticket_settings)

    # 结束抢票任务
    print("抢票任务已完成！")

if __name__ == '__main__':
    main()
