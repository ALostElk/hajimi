#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import sys
import os

# 确保当前目录在Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from ui import HajimiUI
    
    if __name__ == "__main__":
        # 创建主窗口 - 优化尺寸和布局
        root = tk.Tk()
        root.title("哈基米计算器")
        root.geometry("650x750")  # 增加宽度以显示所有按钮
        root.resizable(True, True)
        
        # 设置窗口最小尺寸
        root.minsize(600, 700)
        
        # 设置窗口图标（如果有的话）
        try:
            root.iconbitmap(default='icon.ico')
        except:
            pass
        
        # 创建应用实例
        app = HajimiUI(root)
        
        # 启动主循环
        root.mainloop()
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖已安装")
    input("按回车键退出...")
except Exception as e:
    print(f"运行错误: {e}")
    import traceback
    traceback.print_exc()
    input("按回车键退出...")
