import json
import os

def load_config():
    # 获取项目根目录路径，无论从哪个目录运行脚本都能正确找到配置文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    config_path = os.path.join(project_root, 'config', 'config.json')

    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    print("正在加载配置文件...")
    try:
        config = load_config()
        print("✅ 配置文件加载成功！")

        # 检查主要配置项
        print(f"📋 账户数量: {len(config.get('accounts', []))}")
        print(f"🎫 购票数量: {config.get('ticket_num', '未设置')}")
        print(f"⏰ 自动抢票时间: {config.get('auto_buy_time', '未设置')}")
        print(f"🔄 重试间隔: {config.get('retry_interval', '未设置')}秒")
        print(f"🌐 代理状态: {'启用' if config.get('proxy', {}).get('enabled', False) else '禁用'}")

        # 检查支持的账户
        for i, account in enumerate(config.get('accounts', [])):
            username = account.get('username', f'账户{i+1}')
            auto_time = account.get('auto_buy_time', '未设置')
            print(f"   - 账户{i+1}: {username} (抢票时间: {auto_time})")

        print("\n🎯 配置文件验证完成！")

    except FileNotFoundError:
        print("❌ 错误: 配置文件未找到")
    except json.JSONDecodeError:
        print("❌ 错误: 配置文件格式无效")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

if __name__ == '__main__':
    main()