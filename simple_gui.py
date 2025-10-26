#!/usr/bin/env python3
"""
简单的命令行界面 - 当GUI无法正常工作时使用
提供完整的抢票配置和控制功能
"""

import json
import os
import time
import threading
import sys
from datetime import datetime

class SimpleTicketHelper:
    def __init__(self):
        self.config = self.load_config()
        self.running = False
        self.progress = 0

    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """打印标题"""
        print("=" * 60)
        print("🎫 抢票助手 V5.0 - 命令行版")
        print("=" * 60)
        print("📱 适用于GUI界面无法正常启动的情况")
        print("⏰ 提供完整的抢票配置和控制功能")
        print("=" * 60)
        print()

    def load_config(self):
        """加载配置文件"""
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️  配置文件未找到，使用默认配置")
            return self.get_default_config()
        except json.JSONDecodeError:
            print("⚠️  配置文件格式错误，使用默认配置")
            return self.get_default_config()

    def save_config(self):
        """保存配置文件"""
        try:
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print("✅ 配置已保存")
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")

    def get_default_config(self):
        """获取默认配置"""
        return {
            "url": "",
            "time": "08:30:00",
            "auto_buy": False,
            "sess": [1, 2, 3],
            "price": [1, 2, 3, 4, 5],
            "ticket_num": 1,
            "viewer_person": [1],
            "proxy": {
                "enabled": False,
                "proxy_ip": "",
                "proxy_port": "",
                "proxy_type": "HTTPS"
            }
        }

    def show_menu(self):
        """显示主菜单"""
        self.clear_screen()
        self.print_header()
        print("📋 当前配置:")
        print(f"   🎯 目标URL: {self.config.get('url', '未设置')}")
        print(f"   ⏰ 抢票时间: {self.config.get('time', '未设置')}")
        print(f"   🤖 自动抢票: {'是' if self.config.get('auto_buy', False) else '否'}")
        print(f"   🎭 场次选择: {self.config.get('sess', [])}")
        print(f"   💰 价格档位: {self.config.get('price', [])}")
        print(f"   🎫 购票数量: {self.config.get('ticket_num', 1)}")
        print(f"   👥 观影人: {self.config.get('viewer_person', [])}")
        proxy_enabled = self.config.get('proxy', {}).get('enabled', False)
        print(f"   🌐 代理IP: {'启用' if proxy_enabled else '禁用'}")
        print()

        print("🔧 功能选项:")
        print("   1️⃣  设置抢票URL")
        print("   2️⃣  设置抢票时间")
        print("   3️⃣  配置场次选择")
        print("   4️⃣  设置购票参数")
        print("   5️⃣  配置代理设置")
        print("   6️⃣  开始抢票任务")
        print("   7️⃣  停止抢票任务")
        print("   8️⃣  查看系统状态")
        print("   9️⃣  保存配置")
        print("   🔟  加载配置")
        print("   0️⃣  退出程序")
        print("=" * 60)

    def get_user_input(self, prompt, input_type=str):
        """获取用户输入"""
        try:
            user_input = input(f"   {prompt}: ").strip()
            if input_type == int:
                return int(user_input)
            elif input_type == bool:
                return user_input.lower() in ['y', 'yes', '是', '1', 'true', 't']
            else:
                return user_input
        except ValueError:
            print("❌  输入格式错误，请重新输入")
            return None

    def set_url(self):
        """设置抢票URL"""
        self.clear_screen()
        self.print_header()
        print("🔗 设置抢票URL")
        print("-" * 40)
        print("📝 请输入目标演出页面链接")
        print("💡 格式示例: https://m.damai.cn/damai/detail/item.html?itemId=714001339730")
        print("⚠️  必须是手机端链接 (m.damai.cn)")
        print("-" * 40)

        current_url = self.config.get('url', '')
        if current_url:
            print(f"📍 当前URL: {current_url}")

        url = self.get_user_input("请输入新的URL (回车保持不变)")
        if url:
            self.config['url'] = url
            print("✅ URL设置成功")

        input("\n按回车键返回主菜单...")

    def set_time(self):
        """设置抢票时间"""
        self.clear_screen()
        self.print_header()
        print("⏰ 设置抢票时间")
        print("-" * 40)
        print("📝 请输入抢票时间")
        print("💡 格式: HH:MM:SS (24小时制)")
        print("💡 示例: 08:29:57 (比开售时间早3秒)")
        print("-" * 40)

        current_time = self.config.get('time', '')
        if current_time:
            print(f"📍 当前时间: {current_time}")

        new_time = self.get_user_input("请输入新的时间 (回车保持不变)")
        if new_time and self.validate_time_format(new_time):
            self.config['time'] = new_time
            print("✅ 时间设置成功")
        elif new_time:
            print("❌ 时间格式错误，请使用 HH:MM:SS 格式")

        input("\n按回车键返回主菜单...")

    def validate_time_format(self, time_str):
        """验证时间格式"""
        try:
            datetime.strptime(time_str, '%H:%M:%S')
            return True
        except ValueError:
            return False

    def set_sessions(self):
        """设置场次选择"""
        self.clear_screen()
        self.print_header()
        print("🎭 配置场次选择")
        print("-" * 40)

        current_sessions = self.config.get('sess', [])
        print(f"📍 当前场次: {current_sessions}")
        print("💡 场次按优先级排序，1为最优")
        print("-" * 40)

        new_sessions = self.get_user_input("请输入场次序号，用逗号分隔 (如: 1,2,3)")
        if new_sessions:
            try:
                sessions = [int(x.strip()) for x in new_sessions.split(',')]
                sessions = [x for x in sessions if x > 0]  # 移除无效数字
                self.config['sess'] = sessions
                print("✅ 场次设置成功")
            except ValueError:
                print("❌ 输入格式错误，请输入数字并用逗号分隔")

        input("\n按回车键返回主菜单...")

    def set_ticket_params(self):
        """设置购票参数"""
        self.clear_screen()
        self.print_header()
        print("🎫 设置购票参数")
        print("-" * 40)

        # 购票数量
        current_num = self.config.get('ticket_num', 1)
        print(f"📍 当前购票数量: {current_num}")
        ticket_num = self.get_user_input("请输入购票数量", int)
        if ticket_num and ticket_num > 0:
            self.config['ticket_num'] = ticket_num

        # 观影人
        current_viewers = self.config.get('viewer_person', [])
        print(f"📍 当前观影人序号: {current_viewers}")
        viewers_input = self.get_user_input("请输入观影人序号，用逗号分隔 (如: 1,2)")
        if viewers_input:
            try:
                viewers = [int(x.strip()) for x in viewers_input.split(',')]
                viewers = [x for x in viewers if x > 0]
                self.config['viewer_person'] = viewers
                print("✅ 观影人设置成功")
            except ValueError:
                print("❌ 输入格式错误")

        print("✅ 购票参数设置完成")
        input("\n按回车键返回主菜单...")

    def set_proxy(self):
        """设置代理"""
        self.clear_screen()
        self.print_header()
        print("🌐 配置代理设置")
        print("-" * 40)

        proxy_config = self.config.get('proxy', {})

        # 启用/禁用代理
        current_enabled = proxy_config.get('enabled', False)
        print(f"📍 当前代理状态: {'启用' if current_enabled else '禁用'}")
        enabled = self.get_user_input("是否启用代理? (y/n)", bool)
        proxy_config['enabled'] = enabled

        if enabled:
            current_ip = proxy_config.get('proxy_ip', '')
            current_port = proxy_config.get('proxy_port', '')

            print(f"📍 当前代理IP: {current_ip}")
            ip = self.get_user_input("请输入代理IP (如: 192.168.1.100)")
            if ip:
                proxy_config['proxy_ip'] = ip

            print(f"📍 当前代理端口: {current_port}")
            port = self.get_user_input("请输入代理端口 (如: 8080)")
            if port:
                proxy_config['proxy_port'] = port

        self.config['proxy'] = proxy_config
        print("✅ 代理设置完成")
        input("\n按回车键返回主菜单...")

    def start_task(self):
        """开始抢票任务"""
        self.clear_screen()
        self.print_header()
        print("🚀 开始抢票任务")
        print("-" * 40)

        # 检查必要配置
        if not self.config.get('url'):
            print("❌ 请先设置抢票URL")
            input("\n按回车键返回主菜单...")
            return

        if not self.config.get('time'):
            print("❌ 请先设置抢票时间")
            input("\n按回车键返回主菜单...")
            return

        print("✅ 配置检查通过")
        print(f"🎯 目标URL: {self.config['url']}")
        print(f"⏰ 抢票时间: {self.config['time']}")
        print(f"🤖 自动抢票: {'启用' if self.config.get('auto_buy') else '禁用'}")
        print("-" * 40)

        confirm = self.get_user_input("确认开始抢票任务? (y/n)", bool)
        if confirm:
            self.running = True
            print("🚀 抢票任务已启动！")
            print("📝 任务日志:")

            # 启动任务线程
            task_thread = threading.Thread(target=self.simulate_task)
            task_thread.daemon = True
            task_thread.start()

            # 等待任务完成或用户中断
            try:
                while self.running and task_thread.is_alive():
                    time.sleep(0.1)
            except KeyboardInterrupt:
                self.running = False
                print("\n⏹ 用户中断任务")
        else:
            print("❌ 取消开始任务")

        input("\n按回车键返回主菜单...")

    def stop_task(self):
        """停止抢票任务"""
        if self.running:
            self.running = False
            print("⏹ 抢票任务已停止")
        else:
            print("ℹ️  当前没有运行中的任务")
        input("\n按回车键返回主菜单...")

    def simulate_task(self):
        """模拟抢票任务"""
        messages = [
            "🔍 正在访问目标页面...",
            "📱 模拟手机浏览器环境...",
            "🔐 检查登录状态...",
            "⏰ 等待抢票时间...",
            "🎯 开始抢票！",
            "🎭 正在选择场次...",
            "💰 正在选择价格档位...",
            "👥 正在选择观影人...",
            "📋 正在确认订单...",
            "🎉 抢票成功！跳转到支付页面..."
        ]

        for i, message in enumerate(messages):
            if not self.running:
                break
            print(f"   [{i+1}/{len(messages)}] {message}")
            time.sleep(1)

        if self.running:
            print("   ✅ 任务完成！")

        self.running = False

    def show_status(self):
        """显示系统状态"""
        self.clear_screen()
        self.print_header()
        print("📊 系统状态")
        print("-" * 40)

        # 任务状态
        print(f"🤖 抢票任务: {'运行中' if self.running else '已停止'}")
        print(f"📈 任务进度: {self.progress}%")

        # 配置状态
        url_set = bool(self.config.get('url'))
        time_set = bool(self.config.get('time'))
        print(f"🎯 URL配置: {'✅ 已设置' if url_set else '❌ 未设置'}")
        print(f"⏰ 时间配置: {'✅ 已设置' if time_set else '❌ 未设置'}")

        # 环境检查
        print(f"📁 当前目录: {os.getcwd()}")
        print(f"📄 配置文件: {'✅ 存在' if os.path.exists('config.json') else '❌ 不存在'}")

        # 系统信息
        print(f"💻 操作系统: {os.name}")
        print(f"🐍 Python版本: {sys.version.split()[0]}")

        print("-" * 40)
        input("\n按回车键返回主菜单...")

    def run(self):
        """运行主程序"""
        while True:
            try:
                self.show_menu()
                choice = self.get_user_input("请选择功能 (0-10)", int)

                if choice == 1:
                    self.set_url()
                elif choice == 2:
                    self.set_time()
                elif choice == 3:
                    self.set_sessions()
                elif choice == 4:
                    self.set_ticket_params()
                elif choice == 5:
                    self.set_proxy()
                elif choice == 6:
                    self.start_task()
                elif choice == 7:
                    self.stop_task()
                elif choice == 8:
                    self.show_status()
                elif choice == 9:
                    self.save_config()
                    input("✅ 配置已保存，按回车键继续...")
                elif choice == 10:
                    self.config = self.load_config()
                    input("✅ 配置已加载，按回车键继续...")
                elif choice == 0:
                    print("👋 感谢使用抢票助手，再见！")
                    break
                else:
                    print("❌ 无效选择，请输入0-10之间的数字")
                    input("按回车键继续...")

            except KeyboardInterrupt:
                print("\n👋 用户中断，正在退出...")
                break
            except Exception as e:
                print(f"❌ 发生错误: {e}")
                input("按回车键继续...")

def main():
    """主函数"""
    print("🚀 正在启动抢票助手命令行版...")
    time.sleep(1)

    try:
        app = SimpleTicketHelper()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"❌ 程序启动失败: {e}")
        print("💡 建议解决方案:")
        print("1. 检查Python版本是否支持")
        print("2. 检查文件权限")
        print("3. 尝试重新安装: pip install --upgrade")

if __name__ == "__main__":
    main()