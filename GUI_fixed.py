#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import threading
import time
import random
import json
import sys

class TicketHelperGUI:
    def __init__(self):
        # 设置错误处理
        try:
            self.window = tk.Tk()
            self.setup_window()
        except Exception as e:
            print(f"GUI初始化错误: {e}")
            self.fallback_mode()

    def setup_window(self):
        self.window.title("抢票助手 V5.0")
        self.window.geometry("1200x900")
        self.window.config(bg="#e3f2fd")  # 蓝色背景

        # 尝试禁止调整窗口大小（可能在某些系统上不兼容）
        try:
            self.window.resizable(False, False)
        except:
            pass  # 如果不支持就跳过

        # 设置主题样式
        try:
            self.style = ttk.Style()
            self.style.configure("TButton", font=("Arial", 14), padding=10, relief="flat", background="#3498db", foreground="white", width=20)
            self.style.map("TButton", background=[('active', '#2980b9')])
            self.style.configure("TCheckbutton", font=("Arial", 12), foreground="#333", background="#e3f2fd")
            self.style.configure("TLabel", font=("Arial", 12), foreground="#333", background="#e3f2fd")
        except Exception as e:
            print(f"样式设置警告: {e}")

        # 创建菜单栏
        self.create_menus()
        # 创建UI组件
        self.create_widgets()

    def create_menus(self):
        try:
            menu_bar = tk.Menu(self.window)

            # 文件菜单
            file_menu = tk.Menu(menu_bar, tearoff=0)
            file_menu.add_command(label="保存配置", command=self.save_config)
            file_menu.add_command(label="加载配置", command=self.load_config)
            file_menu.add_separator()
            file_menu.add_command(label="退出", command=self.window.quit)
            menu_bar.add_cascade(label="文件", menu=file_menu)

            # 帮助菜单
            help_menu = tk.Menu(menu_bar, tearoff=0)
            help_menu.add_command(label="关于", command=self.show_about)
            menu_bar.add_cascade(label="帮助", menu=help_menu)

            self.window.config(menu=menu_bar)
        except Exception as e:
            print(f"菜单创建警告: {e}")

    def create_widgets(self):
        # 创建主框架
        main_frame = tk.Frame(self.window, bg="#e3f2fd")
        main_frame.place(relwidth=1, relheight=1)

        # 创建标题
        title_label = tk.Label(main_frame, text="抢票助手", font=("Arial", 30, 'bold'),
                           foreground="#2c3e50", background="#e3f2fd")
        title_label.grid(row=0, column=0, columnspan=4, pady=30)

        # -------------------------- 登录区 --------------------------
        login_frame = tk.LabelFrame(main_frame, text="登录信息", font=("Arial", 14),
                                bg="#ffffff", fg="#333", padx=10, pady=10)
        login_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        url_label = tk.Label(login_frame, text="票务页面 URL",
                          background="#ffffff", font=("Arial", 12))
        url_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.url_entry = tk.Entry(login_frame, font=("Arial", 12), width=40)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5)

        time_label = tk.Label(login_frame, text="抢票时间 (HH:MM:SS)",
                          background="#ffffff", font=("Arial", 12))
        time_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.time_entry = tk.Entry(login_frame, font=("Arial", 12), width=40)
        self.time_entry.grid(row=1, column=1, padx=10, pady=5)

        # -------------------------- 场次管理区 --------------------------
        session_frame = tk.LabelFrame(main_frame, text="场次管理", font=("Arial", 14),
                                  bg="#ffffff", fg="#333", padx=10, pady=10)
        session_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        session_label = tk.Label(session_frame, text="选择场次",
                             background="#ffffff", font=("Arial", 12))
        session_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.session_listbox = tk.Listbox(session_frame, font=("Arial", 12),
                                       selectmode=tk.MULTIPLE, height=6)
        # 模拟一些场次
        for i in range(1, 21):
            self.session_listbox.insert(tk.END, f"场次 {i}")
        self.session_listbox.grid(row=1, column=0, padx=10, pady=5)

        # -------------------------- 代理设置区 --------------------------
        proxy_frame = tk.LabelFrame(main_frame, text="代理设置", font=("Arial", 14),
                                bg="#ffffff", fg="#333", padx=10, pady=10)
        proxy_frame.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

        self.proxy_check_var = tk.BooleanVar()
        proxy_check = tk.Checkbutton(proxy_frame, text="启用代理 IP",
                                  variable=self.proxy_check_var,
                                  background="#ffffff", font=("Arial", 12))
        proxy_check.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        proxy_ip_label = tk.Label(proxy_frame, text="代理 IP (可选)",
                               background="#ffffff", font=("Arial", 12))
        proxy_ip_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.proxy_ip_entry = tk.Entry(proxy_frame, font=("Arial", 12), width=40)
        self.proxy_ip_entry.grid(row=1, column=1, padx=10, pady=5)

        proxy_port_label = tk.Label(proxy_frame, text="代理端口",
                               background="#ffffff", font=("Arial", 12))
        proxy_port_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.proxy_port_entry = tk.Entry(proxy_frame, font=("Arial", 12), width=40)
        self.proxy_port_entry.grid(row=2, column=1, padx=10, pady=5)

        # -------------------------- 任务控制区 --------------------------
        task_control_frame = tk.LabelFrame(main_frame, text="任务控制", font=("Arial", 14),
                                       bg="#ffffff", fg="#333", padx=10, pady=10)
        task_control_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        self.auto_buy_check_var = tk.BooleanVar()
        auto_buy_check = tk.Checkbutton(task_control_frame, text="启用自动抢票",
                                      variable=self.auto_buy_check_var,
                                      background="#ffffff", font=("Arial", 12))
        auto_buy_check.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        start_button = tk.Button(task_control_frame, text="开始抢票",
                              command=self.start_ticket_task,
                              font=("Arial", 14), bg="#27ae60", fg="white",
                              padx=20, pady=10)
        start_button.grid(row=1, column=0, padx=10, pady=10)

        stop_button = tk.Button(task_control_frame, text="停止任务",
                             command=self.stop_ticket_task,
                             font=("Arial", 14), bg="#e74c3c", fg="white",
                             padx=20, pady=10)
        stop_button.grid(row=1, column=1, padx=10, pady=10)

        retry_button = tk.Button(task_control_frame, text="重试任务",
                              command=self.retry_ticket_task,
                              font=("Arial", 14), bg="#f39c12", fg="white",
                              padx=20, pady=10)
        retry_button.grid(row=1, column=2, padx=10, pady=10)

        # -------------------------- 状态栏 --------------------------
        status_frame = tk.Frame(main_frame, bg="#e3f2fd")
        status_frame.grid(row=3, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

        status_label = tk.Label(status_frame, text="当前状态: 未开始",
                            font=("Arial", 12), background="#e3f2fd",
                            foreground="#2c3e50")
        status_label.grid(row=0, column=0, padx=10)

        # 简单的进度条（使用Canvas代替ttk.Progressbar）
        progress_canvas = tk.Canvas(status_frame, width=200, height=20, bg="#ecf0f1")
        progress_canvas.grid(row=0, column=1, padx=10)
        self.progress_rect = progress_canvas.create_rectangle(0, 0, 0, 20, fill="#3498db", outline="")

        progress_label = tk.Label(status_frame, text="进度: 0%",
                              font=("Arial", 12), background="#e3f2fd",
                              foreground="#2c3e50")
        progress_label.grid(row=0, column=2, padx=10)
        self.progress_label = progress_label

        # -------------------------- 日志区域 --------------------------
        log_frame = tk.LabelFrame(main_frame, text="日志输出", font=("Arial", 14),
                                bg="#ffffff", fg="#333", padx=10, pady=10)
        log_frame.grid(row=4, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

        self.log_text = tk.Text(log_frame, height=10, width=90, font=("Arial", 12),
                             wrap=tk.WORD, bg="#f8f9fa", state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, padx=10, pady=5)

        # 添加一些测试日志
        self.log("GUI界面初始化完成！")
        self.log("欢迎使用抢票助手 V5.0")

    def start_ticket_task(self):
        self.log("任务开始！")
        self.update_progress(0)

        # 任务逻辑模拟
        self.task_thread = threading.Thread(target=self.simulate_ticket_task)
        self.task_thread.start()

    def stop_ticket_task(self):
        self.log("任务已停止！")
        self.update_progress(0)
        if hasattr(self, 'task_thread') and self.task_thread.is_alive():
            # 注意：在Python中不能强制终止线程，这里只是演示
            pass

    def retry_ticket_task(self):
        self.log("正在重试任务...")
        self.start_ticket_task()

    def simulate_ticket_task(self):
        # 模拟任务执行，更新进度条
        for i in range(1, 101):
            time.sleep(0.05)  # 减少延迟，让演示更快
            self.update_progress(i)
            if i == 100:
                self.log("任务完成！")

    def update_progress(self, value):
        try:
            # 更新进度条
            self.progress_label.config(text=f"进度: {value}%")
            # 更新Canvas进度条
            progress_width = int(200 * value / 100)
            self.window.after(0, lambda: self._update_canvas_progress(progress_width))
        except Exception as e:
            print(f"进度更新错误: {e}")

    def _update_canvas_progress(self, width):
        try:
            # 找到Canvas对象并更新
            for widget in self.window.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Frame):
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, tk.Canvas):
                                    grandchild.coords(self.progress_rect, 0, 0, width, 20)
                                    return
        except:
            pass

    def log(self, message):
        try:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, f"{message}\n")
            self.log_text.config(state=tk.DISABLED)
            self.log_text.yview(tk.END)
            print(f"[LOG] {message}")  # 同时输出到控制台
        except Exception as e:
            print(f"日志写入错误: {e}")
            print(f"[LOG] {message}")  # 备用输出

    def save_config(self):
        try:
            config_data = {
                "url": self.url_entry.get(),
                "time": self.time_entry.get(),
                "proxy_ip": self.proxy_ip_entry.get(),
                "proxy_port": self.proxy_port_entry.get(),
                "auto_buy": self.auto_buy_check_var.get(),
                "sessions": list(self.session_listbox.curselection())
            }
            with open("config.json", "w") as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            self.log("配置已保存到 config.json")
        except Exception as e:
            self.log(f"保存配置失败: {e}")

    def load_config(self):
        try:
            with open("config.json", "r") as f:
                config_data = json.load(f)

            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, config_data.get("url", ""))

            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, config_data.get("time", ""))

            self.proxy_ip_entry.delete(0, tk.END)
            self.proxy_ip_entry.insert(0, config_data.get("proxy_ip", ""))

            self.proxy_port_entry.delete(0, tk.END)
            self.proxy_port_entry.insert(0, config_data.get("proxy_port", ""))

            self.auto_buy_check_var.set(config_data.get("auto_buy", False))

            # 清除并重新选择场次
            self.session_listbox.selection_clear(0, tk.END)
            for idx in config_data.get("sessions", []):
                try:
                    self.session_listbox.selection_set(idx)
                except:
                    pass

            self.log("配置已加载成功")
        except FileNotFoundError:
            self.log("配置文件未找到，使用默认设置")
        except Exception as e:
            self.log(f"加载配置失败: {e}")

    def show_about(self):
        about_text = """抢票助手 V5.0

功能特性：
• 图形化界面操作
• 多平台票务支持
• 自动抢票功能
• 代理IP支持
• 配置保存/加载

开发者：damaihelper团队
版本：V5.0

注意：本工具仅供学习和个人合法使用"""
        messagebox.showinfo("关于抢票助手", about_text)

    def fallback_mode(self):
        """当GUI无法启动时的备用模式"""
        print("=" * 50)
        print("GUI界面启动失败，进入命令行模式")
        print("=" * 50)
        print("请按以下步骤操作：")
        print("1. 使用命令行模式：python ticket_script.py")
        print("2. 或修复GUI问题：")
        print("   - 检查系统是否支持GUI")
        print("   - 更新Python和相关库")
        print("   - 检查是否为远程SSH连接")
        print("=" * 50)

    def run(self):
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            print("\n用户中断程序")
        except Exception as e:
            print(f"GUI运行错误: {e}")

# 创建并启动界面
if __name__ == "__main__":
    print("正在启动抢票助手GUI...")
    try:
        app = TicketHelperGUI()
        app.run()
    except Exception as e:
        print(f"启动失败: {e}")
        print("尝试使用命令行模式: python ticket_script.py")