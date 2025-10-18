import tkinter as tk
import math
import os
import pygame
from calculator import Calculator
from character import HajimiCharacter
from AI import HajimiAI


class HajimiUI:
    def __init__(self, master):
        self.master = master
        try:
            self.calc = Calculator()
            print("Calculator初始化成功")
        except Exception as e:
            print(f"Calculator初始化失败: {e}")
            import traceback
            traceback.print_exc()
        
        self.hajimi = HajimiCharacter()
        self.ai = HajimiAI()
        
        # 计算历史记录 (最多保存10条)
        self.calc_history = []
        self.max_history = 10

        # 哈基米主题色彩 - 双色调圆润配色
        self.colors = {
            # 主色调：柔和粉色系
            'primary': '#FF8FA3',      # 主粉色
            'primary_light': '#FFB3C6', # 浅粉色
            'primary_dark': '#E85A7A',  # 深粉色
            
            # 辅助色：柔和薄荷绿系
            'secondary': '#6BCF7F',    # 主薄荷绿
            'secondary_light': '#8DD8A3', # 浅薄荷绿
            'secondary_dark': '#4ECDC4',  # 深薄荷绿
            
            # 强调色
            'accent': '#6BB6FF',       # 天蓝色强调色
            'accent_light': '#8CC8FF', # 浅天蓝色
            
            # 基础色
            'background': '#FFF0F5',   # 浅粉色背景
            'background_dark': '#FFE5EC', # 浅粉色背景
            'text': '#3A3A3A',         # 深色文字
            'text_light': '#8A8A8A',   # 浅灰文字
            'button_normal': '#FFFFFF', # 白色按钮
            'button_hover': '#F0F8FF',  # 悬停效果
            'display_bg': '#2D3748',   # 深色显示区
            'display_text': '#F7FAFC',  # 白色显示文字
            'border': '#E2E8F0',       # 边框色
            'success': '#6BCF7F',      # 成功色（使用薄荷绿）
            'warning': '#FF8FA3',      # 警告色（使用粉色）
            'danger': '#E85A7A',       # 危险色（使用深粉色）
        }
        
        # 设置主窗口样式
        self.master.configure(bg=self.colors['background'])
        
        # 创建界面布局
        self.create_title()
        self.create_sound_control()  # 声音控制移到上方
        self.create_display_area()
        self.create_button_areas()
        
        # 绑定键盘事件
        self.bind_keyboard_events()
    
    def create_title(self):
        """创建标题区域 - 趣味版"""
        # 标题容器框架
        title_frame = tk.Frame(
            self.master, 
            bg=self.colors['primary_light'],
            relief='raised',
            bd=3
        )
        title_frame.pack(pady=(10, 5), padx=20, fill='x')
        
        # 顶部emoji装饰行
        emoji_top = tk.Label(
            title_frame,
            text="✨ 🐱 ✨", 
            font=("微软雅黑", 16),
            bg=self.colors['primary_light'],
            fg=self.colors['primary_dark']
        )
        emoji_top.pack(pady=(8, 0))
        
        # 主标题
        title_label = tk.Label(
            title_frame, 
            text="哈基米趣味计算器", 
            font=("微软雅黑", 24, "bold"),
            bg=self.colors['primary_light'],
            fg='#FFFFFF'
        )
        title_label.pack(pady=(2, 0))
        
        # 副标题
        subtitle_label = tk.Label(
            title_frame, 
            text="让数学变得更有趣 ～(˘▾˘～)", 
            font=("微软雅黑", 11),
            bg=self.colors['primary_light'],
            fg=self.colors['primary_dark']
        )
        subtitle_label.pack(pady=(0, 8))
    
    def create_cat_ears(self):
        """创建可爱的猫猫装饰（耳朵+脸）"""
        # 猫猫装饰容器
        cat_frame = tk.Frame(self.master, bg=self.colors['background'], height=120)
        cat_frame.pack(pady=(10, 0), fill='x')
        
        # 创建Canvas来绘制猫猫
        canvas = tk.Canvas(
            cat_frame, 
            width=520, 
            height=120, 
            bg=self.colors['background'],
            highlightthickness=0
        )
        canvas.pack()
        
        # === 绘制猫耳朵 ===
        # 左耳朵（更尖锐的三角形）
        left_ear_x = 150
        left_ear_y = 15
        canvas.create_polygon(
            left_ear_x, left_ear_y + 35,      # 底部左
            left_ear_x + 50, left_ear_y + 35, # 底部右
            left_ear_x + 25, left_ear_y,      # 顶部尖
            fill='#FF8FA3', 
            outline='#C55A78',
            width=3,
            smooth=False
        )
        # 左耳朵内部粉色
        canvas.create_polygon(
            left_ear_x + 12, left_ear_y + 30,
            left_ear_x + 38, left_ear_y + 30,
            left_ear_x + 25, left_ear_y + 12,
            fill='#FFB3C6',
            outline=''
        )
        
        # 右耳朵（更尖锐的三角形）
        right_ear_x = 320
        canvas.create_polygon(
            right_ear_x, left_ear_y + 35,
            right_ear_x + 50, left_ear_y + 35,
            right_ear_x + 25, left_ear_y,
            fill='#FF8FA3',
            outline='#C55A78',
            width=3,
            smooth=False
        )
        # 右耳朵内部粉色
        canvas.create_polygon(
            right_ear_x + 12, left_ear_y + 30,
            right_ear_x + 38, left_ear_y + 30,
            right_ear_x + 25, left_ear_y + 12,
            fill='#FFB3C6',
            outline=''
        )
        
        # === 绘制猫脸 ===
        face_center_x = 260
        face_y = 65
        
        # 左眼睛
        canvas.create_oval(
            face_center_x - 30, face_y,
            face_center_x - 18, face_y + 12,
            fill='#5C3D5C',
            outline=''
        )
        
        # 右眼睛
        canvas.create_oval(
            face_center_x + 18, face_y,
            face_center_x + 30, face_y + 12,
            fill='#5C3D5C',
            outline=''
        )
        
        # 鼻子（小三角形）
        canvas.create_polygon(
            face_center_x - 3, face_y + 20,
            face_center_x + 3, face_y + 20,
            face_center_x, face_y + 25,
            fill='#8B4789',
            outline=''
        )
        
        # ω 嘴巴（使用贝塞尔曲线模拟）
        # 左半边嘴巴
        canvas.create_arc(
            face_center_x - 20, face_y + 22,
            face_center_x - 2, face_y + 35,
            start=180, extent=90,
            outline='#8B4789',
            width=2,
            style='arc'
        )
        # 右半边嘴巴
        canvas.create_arc(
            face_center_x + 2, face_y + 22,
            face_center_x + 20, face_y + 35,
            start=270, extent=90,
            outline='#8B4789',
            width=2,
            style='arc'
        )
        # 中间连接
        canvas.create_line(
            face_center_x - 2, face_y + 28,
            face_center_x + 2, face_y + 28,
            fill='#8B4789',
            width=2
        )
        
        # 左边胡须
        for i in range(3):
            y_offset = face_y + 15 + i * 6
            canvas.create_line(
                face_center_x - 35, y_offset,
                face_center_x - 50, y_offset - 3 + i * 2,
                fill='#C55A78',
                width=2
            )
        
        # 右边胡须
        for i in range(3):
            y_offset = face_y + 15 + i * 6
            canvas.create_line(
                face_center_x + 35, y_offset,
                face_center_x + 50, y_offset - 3 + i * 2,
                fill='#C55A78',
                width=2
            )
        
        # 腮红（可选）
        canvas.create_oval(
            face_center_x - 45, face_y + 18,
            face_center_x - 32, face_y + 28,
            fill='#FFD1DC',
            outline=''
        )
        canvas.create_oval(
            face_center_x + 32, face_y + 18,
            face_center_x + 45, face_y + 28,
            fill='#FFD1DC',
            outline=''
        )
        
    def create_display_area(self):
        """创建圆润美观的显示区域"""
        # 主显示区域容器 - 增加内边距
        main_display_frame = tk.Frame(self.master, bg=self.colors['background'])
        main_display_frame.pack(pady=20, padx=30, fill='x')
        
        # 左侧：计算显示区域 - 趣味粉色边框
        display_frame = tk.Frame(
            main_display_frame, 
            bg='#2D3748',  # 深色背景
            relief='groove', 
            bd=4,
            highlightbackground=self.colors['primary'],
            highlightthickness=3
        )
        display_frame.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # 输入显示区域装饰
        input_container = tk.Frame(display_frame, bg=self.colors['display_bg'])
        input_container.pack(fill='x', padx=15, pady=10)
        
        # 输入标签
        input_title = tk.Label(
            input_container,
            text="输入:",
            font=("微软雅黑", 9),
            bg=self.colors['display_bg'],
            fg=self.colors['text_light']
        )
        input_title.pack(anchor='w')
        
        # 输入显示
        self.input_label = tk.Label(
            input_container,
            text="",
            font=("Consolas", 20, "bold"),
            bg=self.colors['display_bg'],
            fg='#E9ECEF',
            anchor='e',
            height=1
        )
        self.input_label.pack(fill='x', pady=2)
        
        # 分隔线
        separator = tk.Frame(display_frame, height=1, bg=self.colors['border'])
        separator.pack(fill='x', padx=15, pady=5)
        
        # 计算结果区域
        calc_result_container = tk.Frame(display_frame, bg=self.colors['display_bg'])
        calc_result_container.pack(fill='x', padx=15, pady=5)
        
        # 计算结果标签
        calc_result_title = tk.Label(
            calc_result_container,
            text="计算结果:",
            font=("微软雅黑", 9),
            bg=self.colors['display_bg'],
            fg=self.colors['text_light']
        )
        calc_result_title.pack(anchor='w')
        
        # 结果行容器
        result_row = tk.Frame(calc_result_container, bg=self.colors['display_bg'])
        result_row.pack(fill='x', pady=2)
        
        # 计算结果显示
        self.calc_result_label = tk.Label(
            result_row,
            text="",
            font=("Consolas", 18, "bold"),
            bg=self.colors['display_bg'],
            fg='#FFD700',  # 金色更醒目
            anchor='e',
            height=1
        )
        self.calc_result_label.pack(side='left', fill='x', expand=True, padx=10)
        
        # 哈基米评论区域
        comment_container = tk.Frame(display_frame, bg=self.colors['display_bg'])
        comment_container.pack(fill='x', padx=15, pady=10)
        
        # 哈基米评论标签
        comment_title = tk.Label(
            comment_container,
            text="哈基米说:",
            font=("微软雅黑", 9),
            bg=self.colors['display_bg'],
            fg=self.colors['text_light']
        )
        comment_title.pack(anchor='w')
        
        # 哈基米评论显示
        self.result_label = tk.Label(
            comment_container,
            text="哈基米：准备好了！",
            font=("微软雅黑", 12, "bold"),
            bg=self.colors['display_bg'],
            fg=self.colors['primary'],
            anchor='e',
            height=1
        )
        self.result_label.pack(fill='x', pady=2)
        
        # 右侧：角色表情区域 - 趣味粉色边框
        character_frame = tk.Frame(
            main_display_frame, 
            bg='#FFE5EC',  # 浅粉色背景
            relief='groove', 
            bd=4,
            highlightbackground=self.colors['primary'],
            highlightthickness=3
        )
        character_frame.pack(side='right', fill='y', ipadx=10, ipady=10)
        
        # 角色标题 - 更可爱的样式
        character_title = tk.Label(
            character_frame,
            text="😺 哈基米表情 😺",
            font=("微软雅黑", 10, "bold"),
            bg='#FFE5EC',
            fg=self.colors['primary_dark']
        )
        character_title.pack(pady=8)
        
        # 角色表情标签
        self.character_label = tk.Label(
            character_frame,
            image=self.hajimi.get_expression('default'),
            bg='#FFE5EC'
        )
        self.character_label.pack(pady=5)
        
        # 角色状态标签 - 更醒目
        self.character_status_label = tk.Label(
            character_frame,
            text="哈基米",
            font=("微软雅黑", 12, "bold"),
            bg='#FFE5EC',
            fg=self.colors['primary']
        )
        self.character_status_label.pack(pady=8)
    
    def create_cat_slider(self, parent):
        """创建可爱的猫猫滑动条"""
        # 当前音量值
        self.current_volume = 50
        
        # 滑动条画布
        self.slider_canvas = tk.Canvas(
            parent,
            width=120,
            height=30,
            bg='#FFF0F5',
            highlightthickness=0
        )
        self.slider_canvas.pack()
        
        # 绘制滑动轨道
        self.slider_track = self.slider_canvas.create_rectangle(
            10, 12, 110, 18,
            fill='#FFD1DC',
            outline='#FFB3C6',
            width=2
        )
        
        # 绘制进度条
        self.slider_progress = self.slider_canvas.create_rectangle(
            10, 12, 60, 18,
            fill='#FF8FA3',
            outline=''
        )
        
        # 创建猫猫滑块（使用emoji）
        self.slider_cat = self.slider_canvas.create_text(
            60, 15,
            text='😺',
            font=('Arial', 16),
            anchor='center'
        )
        
        # 绑定鼠标事件
        self.slider_canvas.bind('<Button-1>', self.on_slider_click)
        self.slider_canvas.bind('<B1-Motion>', self.on_slider_drag)
        
        # 存储滑块位置范围
        self.slider_min_x = 10
        self.slider_max_x = 110
    
    def on_slider_click(self, event):
        """点击滑动条"""
        self.update_slider_position(event.x)
    
    def on_slider_drag(self, event):
        """拖动滑动条"""
        self.update_slider_position(event.x)
    
    def update_slider_position(self, x):
        """更新滑块位置"""
        # 限制在有效范围内
        x = max(self.slider_min_x, min(x, self.slider_max_x))
        
        # 更新猫猫滑块位置
        self.slider_canvas.coords(self.slider_cat, x, 15)
        
        # 更新进度条
        self.slider_canvas.coords(self.slider_progress, 10, 12, x, 18)
        
        # 计算音量值 (0-100)
        volume_range = self.slider_max_x - self.slider_min_x
        volume = int((x - self.slider_min_x) / volume_range * 100)
        
        # 音量以10为步进
        volume = (volume // 10) * 10
        
        if volume != self.current_volume:
            self.current_volume = volume
            self.on_volume_change(volume)
    
    def create_sound_control(self):
        """创建趣味声音控制面板"""
        # 声音控制容器 - 可爱粉色边框
        sound_frame = tk.Frame(
            self.master, 
            bg='#FFF0F5',
            relief='raised',
            bd=2
        )
        sound_frame.pack(pady=10, padx=20, fill='x')
        
        # 音量控制区域 - 重新布局为两行
        
        # 第一行：音量标签和滑块
        top_row = tk.Frame(sound_frame, bg='#FFF0F5')
        top_row.pack(fill='x', padx=10, pady=(5, 2))
        
        # 音量标签
        self.volume_label = tk.Label(
            top_row,
            text="🔊 音量: 50%",
            font=("微软雅黑", 10, "bold"),
            bg='#FFF0F5',
            fg=self.colors['primary_dark']
        )
        self.volume_label.pack(side='left', padx=(0, 8))
        
        # 创建自定义的猫猫滑动条
        slider_container = tk.Frame(top_row, bg='#FFF0F5')
        slider_container.pack(side='left')
        
        self.create_cat_slider(slider_container)
        
        # 静音按钮放在滑块右边
        self.mute_button = tk.Button(
            top_row,
            text="🔇 静音",
            font=("微软雅黑", 10, "bold"),
            bg='#FFB3C6',
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=8,
            height=1,
            command=self.toggle_mute,
            cursor='hand2'
        )
        self.mute_button.pack(side='left', padx=10)
        
        # 第二行：功能按钮
        bottom_row = tk.Frame(sound_frame, bg='#FFF0F5')
        bottom_row.pack(fill='x', padx=10, pady=(2, 5))
        
        # 左侧标签
        func_label = tk.Label(
            bottom_row,
            text="📱 功能:",
            font=("微软雅黑", 10, "bold"),
            bg='#FFF0F5',
            fg=self.colors['primary_dark']
        )
        func_label.pack(side='left', padx=(0, 8))
        
        # 功能按钮容器
        btn_container = tk.Frame(bottom_row, bg='#FFF0F5')
        btn_container.pack(side='left')
        
        # 音效播放器按钮
        self.sound_player_button = tk.Button(
            btn_container,
            text="🎵 音效",
            font=("微软雅黑", 10, "bold"),
            bg='#FF99CC',
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=8,
            height=1,
            command=self.open_sound_player,
            cursor='hand2'
        )
        self.sound_player_button.pack(side='left', padx=3)
        
        # 幸运数字按钮
        self.lucky_button = tk.Button(
            btn_container,
            text="🎲 幸运",
            font=("微软雅黑", 10, "bold"),
            bg='#FFB366',
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=8,
            height=1,
            command=self.generate_lucky_number,
            cursor='hand2'
        )
        self.lucky_button.pack(side='left', padx=3)
        
        # 历史记录按钮
        self.history_button = tk.Button(
            btn_container,
            text="📊 历史",
            font=("微软雅黑", 10, "bold"),
            bg='#9B59B6',
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=8,
            height=1,
            command=self.open_history_window,
            cursor='hand2'
        )
        self.history_button.pack(side='left', padx=3)
        
        # 对话助手按钮
        self.chat_button = tk.Button(
            btn_container,
            text="💬 对话",
            font=("微软雅黑", 10, "bold"),
            bg='#3498DB',
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=8,
            height=1,
            command=self.open_chat_window,
            cursor='hand2'
        )
        self.chat_button.pack(side='left', padx=3)
        
        # 背景音乐按钮
        self.music_button = tk.Button(
            btn_container,
            text="🎵 背景音乐",
            font=("微软雅黑", 10, "bold"),
            bg='#E91E63',
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=10,
            height=1,
            command=self.open_background_music,
            cursor='hand2'
        )
        self.music_button.pack(side='left', padx=3)
    
    def create_button_areas(self):
        """创建按钮区域"""
        # 主按钮容器
        self.button_container = tk.Frame(
            self.master, 
            bg=self.colors['background']
        )
        self.button_container.pack(pady=10, padx=30, fill='both', expand=True)
        
        # 创建统一的按钮布局
        self.create_all_buttons()
    
    def bind_keyboard_events(self):
        """绑定键盘事件"""
        # 绑定到主窗口
        self.master.focus_set()
        self.master.bind('<Key>', self.on_key_press)
        
        # 设置焦点
        self.master.focus()
    
    def on_key_press(self, event):
        """处理键盘按键"""
        key = event.char
        key_code = event.keycode
        
        # 数字键
        if key.isdigit():
            self.on_click(key)
        # 运算符
        elif key in ['+', '-', '*', '/', '=']:
            if key == '=':
                self.on_click('=')
            elif key == '*':
                self.on_click('×')
            elif key == '/':
                self.on_click('÷')
            else:
                self.on_click(key)
        # 小数点
        elif key == '.':
            self.on_click('.')
        # 回车键计算
        elif key_code == 13:  # Enter
            self.on_click('=')
        # 退格键
        elif key_code == 8:  # Backspace
            self.on_click('⌫')
        # Escape键清空
        elif key_code == 27:  # Escape
            self.on_click('AC')
        # 括号
        elif key in ['(', ')']:
            self.on_click(key)
        # Delete键
        elif key_code == 46:  # Delete
            self.on_click('Del')
    
    def create_all_buttons(self):
        """创建统一圆润的按钮布局"""
        # 主按钮网格容器 - 增加圆润内边距
        main_grid = tk.Frame(self.button_container, bg=self.colors['background'])
        main_grid.pack(expand=True, padx=15, pady=15)
        
        # 配置网格权重，让按钮均匀分布
        for i in range(4):
            main_grid.columnconfigure(i, weight=1)
        for i in range(8):
            main_grid.rowconfigure(i, weight=1)
        
        # 优化后的按钮布局 - 更合理的分组
        buttons = [
            ['sin(', 'cos(', 'tan(', 'sqrt('],
            ['ln(', 'lg(', 'pi', 'e'],
            ['AC', '⌫', 'Del', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '(', ')'],
            ['BMR', 'AI开关', '%', '=']
        ]

        for r, row in enumerate(buttons):
            for c, text in enumerate(row):
                style = self.get_button_style(text)
                btn = self.create_styled_button(
                    main_grid, text, style, row=r, column=c
                )
    
    def get_button_style(self, text):
        """根据按钮文本确定样式"""
        if text.isdigit() or text == '.' or text == '0':
            return 'number'
        elif text in ['÷', '×', '-', '+', '(', ')', '%']:
            return 'operator'
        elif text == '=':
            return 'equals'
        elif text == 'BMR':
            return 'bmr'
        elif text in ['sin(', 'cos(', 'tan(', 'sqrt(', 'ln(', 'lg(', 'pi', 'e']:
            return 'function'
        elif text == 'AI开关':
            return 'ai_control'
        else:  # AC, ⌫, Del, 静音
            return 'control'
    
    
    def create_styled_button(self, parent, text, style, row, column):
        """创建统一圆润样式化按钮 - macOS 兼容的自定义按钮"""
        # 可爱的猫猫粉色主题配色
        if style == 'number':
            bg_color = '#FFE5EC'  # 非常浅的粉色
            fg_color = '#8B4789'  # 深紫粉色文字
            hover_color = '#FFD1DC'
        elif style == 'operator':
            bg_color = '#FFB3C6'  # 浅粉色
            fg_color = '#FFFFFF'
            hover_color = '#FF99B3'
        elif style == 'equals':
            bg_color = '#FF6B9D'  # 鲜艳粉色
            fg_color = '#FFFFFF'
            hover_color = '#FF5287'
        elif style == 'function':
            bg_color = '#E8A5D4'  # 粉紫色
            fg_color = '#FFFFFF'
            hover_color = '#D98BC4'
        elif style == 'bmr':
            bg_color = '#B4E7CE'  # 薄荷绿
            fg_color = '#FFFFFF'
            hover_color = '#9FDDBE'
        elif style == 'control':
            bg_color = '#C9ADA7'  # 灰粉色
            fg_color = '#FFFFFF'
            hover_color = '#B39B96'
        elif style == 'ai_control':
            bg_color = '#FF85A2'  # 亮粉色
            fg_color = '#FFFFFF'
            hover_color = '#FF6B8A'
        else:
            bg_color = '#FFE5EC'  # 默认浅粉色
            fg_color = '#8B4789'
            hover_color = '#FFD1DC'
        
        # 创建 Frame 作为按钮容器（macOS 兼容方法）
        btn_frame = tk.Frame(
            parent,
            bg=bg_color,
            relief='raised',
            bd=2,
            highlightthickness=0
        )
        btn_frame.grid(row=row, column=column, padx=4, pady=4, sticky='nsew')
        
        # 创建 Label 作为按钮文字
        btn_label = tk.Label(
            btn_frame,
            text=text,
            font=("微软雅黑", 12, "bold"),
            bg=bg_color,
            fg=fg_color,
            cursor='hand2',
            padx=20,
            pady=15
        )
        btn_label.pack(fill='both', expand=True)
        
        # 悬停效果
        def on_enter(event):
            btn_frame.config(bg=hover_color)
            btn_label.config(bg=hover_color)
        
        def on_leave(event):
            btn_frame.config(bg=bg_color)
            btn_label.config(bg=bg_color)
        
        def on_press(event):
            btn_frame.config(relief='sunken')
            # 立即触发点击事件，避免卡顿
            self.on_click(text)
        
        def on_release(event):
            btn_frame.config(relief='raised')
        
        # 绑定事件
        btn_frame.bind("<Enter>", on_enter)
        btn_frame.bind("<Leave>", on_leave)
        btn_frame.bind("<ButtonPress-1>", on_press)
        btn_frame.bind("<ButtonRelease-1>", on_release)
        
        btn_label.bind("<Enter>", on_enter)
        btn_label.bind("<Leave>", on_leave)
        btn_label.bind("<ButtonPress-1>", on_press)
        btn_label.bind("<ButtonRelease-1>", on_release)
        
        return btn_frame
    
    def configure_rounded_button(self, button, style):
        """配置按钮的圆角效果"""
        # 由于tkinter原生不支持圆角，我们通过其他方式模拟圆润效果
        # 设置按钮的字体和间距来营造圆润感
        button.config(
            font=("微软雅黑", 11, "bold"),
            padx=8,
            pady=4
        )
    
    def button_hover_enter(self, button, style):
        """按钮悬停进入效果 - 圆润过渡"""
        if 'activebackground' in style:
            button.config(bg=style['activebackground'])
            if 'activeforeground' in style:
                button.config(fg=style['activeforeground'])
    
    def button_hover_leave(self, button, style):
        """按钮悬停离开效果 - 圆润过渡"""
        button.config(bg=style['bg'])
        button.config(fg=style['fg'])
    
    def button_press_effect(self, button, style):
        """按钮按下效果 - 圆润反馈"""
        original_bg = button.cget('bg')
        original_fg = button.cget('fg')
        original_font = button.cget('font')
        
        # 按下时的颜色（稍微深一点）
        press_bg = self.darken_color(original_bg)
        press_fg = original_fg
        
        # 立即改变颜色和字体大小（模拟按下效果）
        button.config(bg=press_bg, fg=press_fg, font=("微软雅黑", 11, "bold"))
        
        # 120ms后恢复原色和字体
        self.master.after(120, lambda: [
            button.config(bg=original_bg, fg=original_fg, font=original_font)
        ])
    
    def animate_color_transition(self, widget, attribute, start_color, end_color, duration):
        """颜色过渡动画"""
        # 简化的颜色过渡
        widget.config(**{attribute: end_color})
    
    def darken_color(self, color):
        """将颜色变深 - 猫猫粉色主题深色效果"""
        color_map = {
            '#FFE5EC': '#FFD1DC',  # 浅粉色数字按键
            '#FFB3C6': '#FF99B3',  # 运算符
            '#FF6B9D': '#FF5287',  # 等号
            '#E8A5D4': '#D98BC4',  # 数学函数
            '#B4E7CE': '#9FDDBE',  # BMR按钮
            '#C9ADA7': '#B39B96',  # 控制按键
            '#FF85A2': '#FF6B8A',  # AI控制
            self.colors['button_normal']: self.colors['background_dark'],
            self.colors['secondary']: self.colors['secondary_dark'],
            self.colors['primary']: self.colors['primary_dark'],
            self.colors['text_light']: '#6B7280',
        }
        return color_map.get(color, color)
    

    def on_click(self, val):
        """按钮点击事件处理"""
        # 添加按钮按下动画效果
        self.button_press_animation(val)
        
        if val == "AC":
            self.clear_display()
            self.hajimi.play_operator_sound()
            return
        
        if val == "⌫":
            self.backspace()
            return
        
        if val == "Del":
            self.delete_all()
            return
        
        if val == "=":
            self.calculate()
            return
        
        if val == "BMR":
            self.open_bmr_window()
            return

        if val == "静音":
            self.toggle_mute()
            return

        if val == "AI开关":
            self.toggle_ai()
            return

        # 添加输入到显示区域
        self.add_input(val)
        
        # 根据按键类型播放对应音效
        if val.isdigit():
            # 数字按键：播放对应的固定音效
            self.hajimi.play_number_sound(val)
        elif val in ['+', '-', '×', '÷', '.']:
            # 加减乘除和小数点：播放固定音效
            self.hajimi.play_operator_sound(val)
        elif val in ['*', '/']:
            # 键盘输入的乘除号，映射到对应符号
            operator_map = {'*': '×', '/': '÷'}
            self.hajimi.play_operator_sound(operator_map[val])
        elif val in ['(', ')', '%']:
            # 括号和百分号：随机播放
            self.hajimi.play_operator_sound()
        elif val in ['sin(', 'cos(', 'tan(', 'sqrt(', 'ln(', 'lg(', 'pi', 'e']:
            # 数学函数和常量：随机播放
            self.hajimi.play_operator_sound()

    def button_press_animation(self, val):
        """按钮按下动画效果"""
        # 这里可以添加按钮按下的视觉反馈
        pass
    
    def clear_display(self):
        """清空显示区域"""
        self.input_label.config(text="")
        self.calc_result_label.config(text="")
        self.result_label.config(text="哈基米：准备好了！")
    
    def backspace(self):
        """退格功能 - 删除最后一个字符"""
        current = self.input_label.cget('text')
        if current:
            new_text = current[:-1]
            self.input_label.config(text=new_text)
    
    def delete_all(self):
        """删除全部功能 - 清空输入"""
        self.input_label.config(text="")
        self.calc_result_label.config(text="")
        self.result_label.config(text="哈基米：准备好了！")
        # 重置角色表情
        self.hajimi.set_expression('default')
        self.update_character_display()
    
    def add_input(self, val):
        """添加输入到显示区域"""
        current = self.input_label.cget('text')
        
        # 输入验证和限制
        if not self.is_valid_input(current, val):
            return
        
        # 添加输入
        new_text = current + val
        self.input_label.config(text=new_text)
    
    def is_valid_input(self, current, new_val):
        """验证输入是否有效"""
        # 限制最大长度
        if len(current) >= 50:
            return False
        
        # 小数点验证
        if new_val == '.':
            # 检查是否已经有小数点
            # 需要处理所有运算符，包括×和÷
            last_operand = current
            for op in ['+', '-', '*', '/', '×', '÷']:
                if op in last_operand:
                    last_operand = last_operand.split(op)[-1]
            if '.' in last_operand:
                return False
        
        # 运算符验证
        if new_val in ['+', '-', '×', '÷', '*', '/']:
            # 不能连续输入运算符
            if current and current[-1] in ['+', '-', '×', '÷', '*', '/']:
                return False
            # 不能以运算符开始（除了负号）
            if not current and new_val != '-':
                return False
        
        # 括号验证
        if new_val == '(':
            # 检查括号数量限制
            if current.count('(') - current.count(')') >= 5:
                return False
        elif new_val == ')':
            # 检查是否有对应的左括号
            if current.count('(') <= current.count(')'):
                return False
        
        return True
    
    def calculate(self):
        """执行计算"""
        expr = self.input_label.cget('text').strip()
        
        # 检查输入是否为空
        if not expr:
            self.show_error("请输入表达式")
            return
        
        # 检查表达式是否完整
        if not self.is_complete_expression(expr):
            self.show_error("表达式不完整")
            return
        
        # 执行计算
        result, msg = self.calc.evaluate(expr)
        # 使用动态AI生成评论
        ai_response = self.ai.generate_dynamic_comment(result, msg, self.hajimi.current_expression)
        
        # 添加到历史记录
        if result is not None:
            self.add_to_history(expr, result)
        
        # 更新显示
        self.update_display(result, ai_response, msg)
        
        # 更新角色表情和音效（react在这里面已经调用）
        self.update_character_expression(result, msg)
        
        # 添加结果高亮动画
        self.result_highlight_animation()
        
        # 清空输入
        self.input_label.config(text="")
    
    def is_complete_expression(self, expr):
        """检查表达式是否完整"""
        # 检查括号是否匹配
        if expr.count('(') != expr.count(')'):
            return False
        
        # 检查是否以运算符结尾（除了右括号和百分号）
        if expr and len(expr) > 0:
            last_char = expr[-1]
            if last_char in ['+', '-', '×', '÷', '*', '/', '.']:
                return False
        
        # 检查是否有空括号
        if '()' in expr:
            return False
        
        return True
    
    def update_display(self, result, ai_response, msg):
        """更新显示区域"""
        # 更新计算结果显示
        if result is not None:
            formatted_result = self.format_result(result)
            self.calc_result_label.config(text=formatted_result)
        else:
            self.calc_result_label.config(text="")
        
        # 更新哈基米评论显示
        self.result_label.config(text=ai_response)
    
    def show_error(self, error_msg):
        """显示错误信息"""
        self.calc_result_label.config(text="")
        self.result_label.config(text=f"哈基米：{error_msg}")
        self.hajimi.react_to_error(error_msg)
        self.hajimi.play_error_sound()
        self.update_character_display()
    
    def format_result(self, result):
        """格式化结果显示"""
        try:
            if isinstance(result, (int, float)):
                # 处理无穷大和NaN
                if math.isnan(result):
                    return "NaN"
                elif math.isinf(result):
                    return "∞" if result > 0 else "-∞"
                
                # 处理整数
                if isinstance(result, int):
                    return str(result)
                
                # 处理浮点数
                if result == 0:
                    return "0"
                
                # 科学计数法阈值
                if abs(result) > 1e10 or (abs(result) < 1e-6 and result != 0):
                    return f"{result:.6e}"
                
                # 普通数值格式化
                formatted = f"{result:.10g}"
                
                # 移除不必要的小数点和尾随零
                if '.' in formatted:
                    formatted = formatted.rstrip('0').rstrip('.')
                
                return formatted
            else:
                return str(result)
        except Exception:
            return "错误"
    
    def result_highlight_animation(self):
        """结果高亮动画"""
        # 高亮计算结果显示
        original_calc_fg = self.calc_result_label.cget('fg')
        self.calc_result_label.config(fg=self.colors['accent'])
        
        # 高亮哈基米评论显示
        original_comment_fg = self.result_label.cget('fg')
        self.result_label.config(fg=self.colors['accent'])
        
        # 500ms后恢复原色
        self.master.after(500, lambda: [
            self.calc_result_label.config(fg=original_calc_fg),
            self.result_label.config(fg=original_comment_fg)
        ])
    
    def update_character_expression(self, result, msg):
        """更新角色表情和音效"""
        if result is None:
            # 计算失败：设置表情并播放错误音效
            self.hajimi.react_to_error(msg)
            self.hajimi.play_error_sound()
        else:
            # 计算成功：根据结果设置表情并播放音效
            self.hajimi.react(result)
        
        # 更新表情图片
        expression_img = self.hajimi.get_expression(self.hajimi.current_expression)
        self.character_label.config(image=expression_img)
        
        # 更新角色状态文字
        status_texts = {
            'default': "哈基米",
            'happy': "开心！",
            'satisfied': "满意！",
            'surprised': "惊讶！",
            'angry': "生气！",
            'furious': "暴怒！",
            'sad': "难过...",
            'tired': "困倦...",
            'expressionless': "无语..."
        }
        status = status_texts.get(self.hajimi.current_expression, "哈基米")
        self.character_status_label.config(text=status)
    
    def on_volume_change(self, value):
        """音量滑块变化事件"""
        volume = int(value)
        self.hajimi.volume = volume / 100.0  # 转换为0-1范围
        
        # 更新音量标签 - 带emoji
        if hasattr(self, 'volume_label'):
            emoji = "🔊" if volume > 50 else ("🔉" if volume > 0 else "🔇")
            self.volume_label.config(text=f"{emoji} 音量: {volume}%")
        
        # 更新音量指示器（安全检查）
        if hasattr(self, 'volume_indicator'):
            if volume == 0:
                self.volume_indicator.config(text="🔇", fg=self.colors['danger'])
            elif volume < 30:
                self.volume_indicator.config(text="🔉", fg=self.colors['warning'])
            elif volume < 70:
                self.volume_indicator.config(text="🔊", fg=self.colors['success'])
            else:
                self.volume_indicator.config(text="🔊", fg=self.colors['primary'])
        
        # 更新静音按钮状态（安全检查）
        if hasattr(self, 'mute_button'):
            if volume == 0:
                self.mute_button.config(text="🔇", bg=self.colors['danger'])
            else:
                self.mute_button.config(text="🔇", bg=self.colors['text_light'])
    
    def toggle_mute(self):
        """切换静音状态"""
        if self.hajimi.mute:
            # 取消静音，恢复之前的音量
            self.hajimi.mute = False
            volume = int(self.hajimi.volume * 100)
            # 更新猫猫滑块位置
            x = self.slider_min_x + (volume / 100.0) * (self.slider_max_x - self.slider_min_x)
            self.slider_canvas.coords(self.slider_cat, x, 15)
            self.slider_canvas.coords(self.slider_progress, 10, 12, x, 18)
            self.current_volume = volume
            self.mute_button.config(text="🔇", bg='#FFB3C6')
            status = "有声"
        else:
            # 静音
            self.hajimi.mute = True
            # 将猫猫滑块移到最左边
            self.slider_canvas.coords(self.slider_cat, self.slider_min_x, 15)
            self.slider_canvas.coords(self.slider_progress, 10, 12, self.slider_min_x, 18)
            self.current_volume = 0
            self.mute_button.config(text="🔊", bg=self.colors['success'])
            status = "静音"
        
        self.result_label.config(text=f"哈基米：{status}模式！")
        
        # 更新角色表情
        special_type = 'mute_on' if self.hajimi.mute else 'mute_off'
        self.hajimi.react_to_special(special_type)
        self.update_character_display()

    def toggle_ai(self):
        """切换AI生成状态"""
        ai_response = self.ai.toggle_ai()
        self.result_label.config(text=ai_response)
        
        # 更新角色表情
        if self.ai.ai_enabled:
            self.hajimi.react_to_special('ai_on')
        else:
            self.hajimi.react_to_special('ai_off')
        self.update_character_display()
    
    def update_character_display(self):
        """更新角色显示"""
        expression_img = self.hajimi.get_expression(self.hajimi.current_expression)
        self.character_label.config(image=expression_img)
        
        # 更新角色状态文字
        status_texts = {
            'default': "哈基米",
            'happy': "开心！",
            'satisfied': "满意！",
            'surprised': "惊讶！",
            'angry': "生气！",
            'furious': "暴怒！",
            'sad': "难过...",
            'tired': "困倦...",
            'expressionless': "无语..."
        }
        status = status_texts.get(self.hajimi.current_expression, "哈基米")
        self.character_status_label.config(text=status)
    
    def open_sound_player(self):
        """打开音效播放器窗口"""
        win = tk.Toplevel(self.master)
        win.title("🎵 哈基米音效播放器")
        win.geometry("500x600")
        win.configure(bg=self.colors['background'])
        win.resizable(False, False)
        
        # 标题
        title = tk.Label(
            win,
            text="🎵 东海帝皇曼波音效库 🎵",
            font=("微软雅黑", 16, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary_dark']
        )
        title.pack(pady=20)
        
        # 音效列表容器
        list_frame = tk.Frame(win, bg=self.colors['background'])
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 添加滚动条
        canvas = tk.Canvas(list_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 音效列表
        sound_files = [
            ("数字音效", [
                ("曼波（干脆.低", "曼波（干脆.低.wav"),
                ("曼波（可爱.低", "曼波（可爱.低.wav"),
                ("曼波↑.低", "曼波↑.低.wav"),
                ("曼波（干脆.中", "曼波（干脆.中.wav"),
                ("曼波（可爱.中", "曼波（可爱.中.wav"),
                ("曼波↑.中", "曼波↑.中.wav"),
                ("曼波（干脆.高", "曼波（干脆.高.wav"),
                ("曼波（可爱.高", "曼波（可爱.高.wav"),
                ("曼波↑.高", "曼波↑.高.wav"),
                ("哈", "哈.wav"),
            ]),
            ("运算符音效", [
                ("曼波", "曼波.wav"),
                ("曼波（干脆", "曼波（干脆.wav"),
                ("曼波（可爱", "曼波（可爱.wav"),
                ("曼波↑", "曼波↑.wav"),
            ]),
            ("特殊音效", [
                ("曼波欧耶", "曼波欧耶.wav"),
                ("曼波wow", "曼波wow.wav"),
                ("帝皇私人笑声", "帝皇私人笑声.wav"),
                ("曼波duang", "曼波duang.wav"),
                ("曼波啊米诺斯", "曼波啊米诺斯.wav"),
                ("曼波我嘞个豆", "曼波我嘞个豆.wav"),
            ])
        ]
        
        for category, sounds in sound_files:
            # 分类标题
            cat_label = tk.Label(
                scrollable_frame,
                text=f"━━━ {category} ━━━",
                font=("微软雅黑", 12, "bold"),
                bg=self.colors['background'],
                fg=self.colors['primary']
            )
            cat_label.pack(pady=(15, 10))
            
            # 音效按钮
            for sound_name, sound_file in sounds:
                sound_frame = tk.Frame(scrollable_frame, bg='#FFE5F0', relief='raised', bd=2)
                sound_frame.pack(fill='x', pady=5, padx=10)
                
                # 音效名称
                name_label = tk.Label(
                    sound_frame,
                    text=sound_name,
                    font=("微软雅黑", 11),
                    bg='#FFE5F0',
                    fg=self.colors['text'],
                    anchor='w'
                )
                name_label.pack(side='left', padx=15, pady=8)
                
                # 播放按钮
                play_btn = tk.Button(
                    sound_frame,
                    text="▶️ 播放",
                    font=("微软雅黑", 10, "bold"),
                    bg=self.colors['primary'],
                    fg='#FFFFFF',
                    relief='raised',
                    bd=2,
                    cursor='hand2',
                    command=lambda f=sound_file: self.hajimi.play_sound(f)
                )
                play_btn.pack(side='right', padx=10, pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 关闭按钮
        close_btn = tk.Button(
            win,
            text="关闭",
            font=("微软雅黑", 12, "bold"),
            bg=self.colors['danger'],
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=15,
            command=win.destroy,
            cursor='hand2'
        )
        close_btn.pack(pady=15)
    
    def generate_lucky_number(self):
        """生成幸运数字"""
        import random
        import datetime
        
        # 生成幸运数字
        lucky_num = random.randint(1, 999)
        
        # 根据数字特点给出不同的评论
        comments = []
        
        # 特殊数字判断
        if lucky_num == 520:
            comment = "哇！幸运数字 520！爱意满满的一天！💕"
            self.hajimi.play_sound("曼波欧耶.wav")
        elif lucky_num == 666:
            comment = "幸运数字 666！今天顺顺利利！🎉"
            self.hajimi.play_sound("曼波wow.wav")
        elif lucky_num == 888:
            comment = "幸运数字 888！发发发！💰"
            self.hajimi.play_sound("帝皇私人笑声.wav")
        elif lucky_num == 114:
            comment = "幸运数字 114！今天要做个好人！😇"
            self.hajimi.play_sound("曼波.wav")
        elif lucky_num % 100 == 0:
            comment = f"幸运数字 {lucky_num}！完美的整百数！🎯"
            self.hajimi.play_sound("曼波欧耶.wav")
        elif lucky_num % 10 == 0:
            comment = f"幸运数字 {lucky_num}！整十数很吉利！✨"
            self.hajimi.play_sound("曼波（可爱.wav")
        elif lucky_num < 100:
            comment = f"幸运数字 {lucky_num}！小数字有大运气！🌟"
            self.hajimi.play_sound("曼波（干脆.wav")
        elif lucky_num > 800:
            comment = f"幸运数字 {lucky_num}！大数字大吉大利！🎊"
            self.hajimi.play_sound("曼波↑.wav")
        else:
            # 一般数字的随机评论
            general_comments = [
                f"幸运数字 {lucky_num}！今天很适合学习哦！📚",
                f"幸运数字 {lucky_num}！心想事成！🌈",
                f"幸运数字 {lucky_num}！好运连连！🍀",
                f"幸运数字 {lucky_num}！加油加油！💪",
                f"幸运数字 {lucky_num}！开心每一天！😊",
            ]
            comment = random.choice(general_comments)
            self.hajimi.play_operator_sound()
        
        # 显示结果
        self.calc_result_label.config(text=str(lucky_num))
        self.result_label.config(text=f"哈基米：{comment}")
        
        # 更新表情
        if lucky_num in [520, 666, 888] or lucky_num % 100 == 0:
            self.hajimi.react_to_special('lucky_great')
        else:
            self.hajimi.react_to_special('lucky_good')
        self.update_character_display()
    
    def add_to_history(self, expression, result):
        """添加计算到历史记录"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        history_item = {
            'time': timestamp,
            'expression': expression,
            'result': str(result)
        }
        
        # 添加到历史记录
        self.calc_history.insert(0, history_item)
        
        # 限制历史记录数量
        if len(self.calc_history) > self.max_history:
            self.calc_history = self.calc_history[:self.max_history]
        
        # 更新历史记录显示（如果窗口存在）
        if hasattr(self, 'history_window') and self.history_window.winfo_exists():
            self.update_history_display()
    
    def open_history_window(self):
        """打开历史记录窗口"""
        # 如果窗口已存在，则聚焦到该窗口
        if hasattr(self, 'history_window') and self.history_window.winfo_exists():
            self.history_window.lift()
            self.history_window.focus()
            return
        
        self.history_window = tk.Toplevel(self.master)
        self.history_window.title("📊 计算历史记录")
        self.history_window.geometry("450x500")
        self.history_window.configure(bg=self.colors['background'])
        self.history_window.resizable(False, False)
        
        # 标题
        title = tk.Label(
            self.history_window,
            text="📊 最近计算记录",
            font=("微软雅黑", 16, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary_dark']
        )
        title.pack(pady=20)
        
        # 历史记录列表容器
        self.history_list_frame = tk.Frame(self.history_window, bg=self.colors['background'])
        self.history_list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 添加滚动条
        history_canvas = tk.Canvas(self.history_list_frame, bg=self.colors['background'], highlightthickness=0)
        history_scrollbar = tk.Scrollbar(self.history_list_frame, orient="vertical", command=history_canvas.yview)
        self.history_scrollable_frame = tk.Frame(history_canvas, bg=self.colors['background'])
        
        self.history_scrollable_frame.bind(
            "<Configure>",
            lambda e: history_canvas.configure(scrollregion=history_canvas.bbox("all"))
        )
        
        history_canvas.create_window((0, 0), window=self.history_scrollable_frame, anchor="nw")
        history_canvas.configure(yscrollcommand=history_scrollbar.set)
        
        history_canvas.pack(side="left", fill="both", expand=True)
        history_scrollbar.pack(side="right", fill="y")
        
        # 显示历史记录
        self.update_history_display()
        
        # 按钮区域
        btn_frame = tk.Frame(self.history_window, bg=self.colors['background'])
        btn_frame.pack(pady=15)
        
        # 清空历史按钮
        clear_btn = tk.Button(
            btn_frame,
            text="🗑️ 清空历史",
            font=("微软雅黑", 11, "bold"),
            bg=self.colors['danger'],
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=12,
            command=self.clear_history,
            cursor='hand2'
        )
        clear_btn.pack(side='left', padx=5)
        
        # 关闭按钮
        close_btn = tk.Button(
            btn_frame,
            text="关闭",
            font=("微软雅黑", 11, "bold"),
            bg=self.colors['text_light'],
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=12,
            command=self.history_window.destroy,
            cursor='hand2'
        )
        close_btn.pack(side='left', padx=5)
    
    def update_history_display(self):
        """更新历史记录显示"""
        # 清空当前显示
        for widget in self.history_scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.calc_history:
            # 没有历史记录
            empty_label = tk.Label(
                self.history_scrollable_frame,
                text="还没有计算记录哦~\n快去使用计算器吧！😊",
                font=("微软雅黑", 12),
                bg=self.colors['background'],
                fg=self.colors['text_light']
            )
            empty_label.pack(pady=50)
        else:
            # 显示历史记录
            for i, item in enumerate(self.calc_history):
                history_frame = tk.Frame(
                    self.history_scrollable_frame,
                    bg='#FFE5F0',
                    relief='raised',
                    bd=2
                )
                history_frame.pack(fill='x', pady=5, padx=10)
                
                # 时间标签
                time_label = tk.Label(
                    history_frame,
                    text=f"⏰ {item['time']}",
                    font=("微软雅黑", 9),
                    bg='#FFE5F0',
                    fg=self.colors['text_light']
                )
                time_label.pack(anchor='w', padx=10, pady=(5, 0))
                
                # 表达式
                expr_label = tk.Label(
                    history_frame,
                    text=item['expression'],
                    font=("Consolas", 11),
                    bg='#FFE5F0',
                    fg=self.colors['text']
                )
                expr_label.pack(anchor='w', padx=15)
                
                # 结果
                result_label = tk.Label(
                    history_frame,
                    text=f"= {item['result']}",
                    font=("Consolas", 13, "bold"),
                    bg='#FFE5F0',
                    fg=self.colors['primary_dark']
                )
                result_label.pack(anchor='w', padx=15, pady=(0, 5))
                
                # 点击加载按钮
                load_btn = tk.Button(
                    history_frame,
                    text="📝 加载",
                    font=("微软雅黑", 9),
                    bg=self.colors['secondary'],
                    fg='#FFFFFF',
                    relief='raised',
                    bd=1,
                    cursor='hand2',
                    command=lambda e=item['expression']: self.load_from_history(e)
                )
                load_btn.pack(anchor='e', padx=10, pady=5)
    
    def load_from_history(self, expression):
        """从历史记录加载表达式"""
        self.input_label.config(text=expression)
        self.hajimi.play_operator_sound()
        if hasattr(self, 'history_window') and self.history_window.winfo_exists():
            self.history_window.destroy()
    
    def clear_history(self):
        """清空历史记录"""
        self.calc_history = []
        self.update_history_display()
        self.hajimi.play_sound("曼波duang.wav")

    def open_bmr_window(self):
        """打开BMR计算窗口 - 重新设计的简化版本"""
        win = tk.Toplevel(self.master)
        win.title("🏥 哈基米健康数据计算器")
        win.geometry("600x1000")  # 增大窗口尺寸
        win.configure(bg=self.colors['background'])
        win.resizable(True, True)  # 允许调整大小
        
        # 设置窗口图标和居中
        try:
            win.iconbitmap(default='icon.ico')
        except:
            pass
        
        # 窗口居中
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (600 // 2)
        y = (win.winfo_screenheight() // 2) - (1000 // 2)
        win.geometry(f"600x1000+{x}+{y}")
        
        # 设置最小尺寸
        win.minsize(550, 900)
        
        # 标题区域
        title_frame = tk.Frame(win, bg=self.colors['background'])
        title_frame.pack(pady=20, padx=20, fill='x')
        
        title_label = tk.Label(
            title_frame, 
            text="🏥 健康数据计算器",
            font=("微软雅黑", 20, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="💪 计算BMR基础代谢率 + BMI身体质量指数",
            font=("微软雅黑", 11),
            bg=self.colors['background'],
            fg=self.colors['text_light']
        )
        subtitle_label.pack(pady=(5, 0))
        
        # 输入框架
        input_container = tk.Frame(win, bg=self.colors['background'])
        input_container.pack(pady=15, padx=25, fill='x')
        
        input_frame = tk.Frame(
            input_container, 
            bg=self.colors['background_dark'],
            relief='solid',
            bd=1,
            highlightbackground=self.colors['border']
        )
        input_frame.pack(fill='x', ipady=15, ipadx=15)
        
        # 性别选择
        gender_frame = tk.Frame(input_frame, bg=self.colors['background_dark'])
        gender_frame.pack(fill='x', pady=8)
        
        gender_label = tk.Label(
            gender_frame, 
            text="性别:", 
            font=("微软雅黑", 12, "bold"), 
            bg=self.colors['background_dark'], 
            fg=self.colors['text']
        )
        gender_label.pack(side='left')
        
        gender_var = tk.StringVar(value="M")
        gender_male = tk.Radiobutton(
            gender_frame, 
            text="男", 
            variable=gender_var, 
            value="M", 
            bg=self.colors['background_dark'], 
            fg=self.colors['text'],
            selectcolor=self.colors['primary'],
            font=("微软雅黑", 11)
        )
        gender_male.pack(side='left', padx=15)
        
        gender_female = tk.Radiobutton(
            gender_frame, 
            text="女", 
            variable=gender_var, 
            value="F", 
            bg=self.colors['background_dark'], 
            fg=self.colors['text'],
            selectcolor=self.colors['primary'],
            font=("微软雅黑", 11)
        )
        gender_female.pack(side='left', padx=15)
        
        # 年龄
        age_frame = tk.Frame(input_frame, bg=self.colors['background_dark'])
        age_frame.pack(fill='x', pady=8)
        
        age_label = tk.Label(
            age_frame, 
            text="年龄:", 
            font=("微软雅黑", 12, "bold"), 
            bg=self.colors['background_dark'], 
            fg=self.colors['text']
        )
        age_label.pack(side='left')
        
        age_entry = tk.Entry(
            age_frame, 
            font=("微软雅黑", 14), 
            width=15,
            relief='solid',
            bd=2,
            justify='right'
        )
        age_entry.pack(side='right')
        
        # 身高
        height_frame = tk.Frame(input_frame, bg=self.colors['background_dark'])
        height_frame.pack(fill='x', pady=8)
        
        height_label = tk.Label(
            height_frame, 
            text="身高(cm):", 
            font=("微软雅黑", 12, "bold"), 
            bg=self.colors['background_dark'], 
            fg=self.colors['text']
        )
        height_label.pack(side='left')
        
        height_entry = tk.Entry(
            height_frame, 
            font=("微软雅黑", 14), 
            width=15,
            relief='solid',
            bd=2,
            justify='right'
        )
        height_entry.pack(side='right')
        
        # 体重
        weight_frame = tk.Frame(input_frame, bg=self.colors['background_dark'])
        weight_frame.pack(fill='x', pady=8)
        
        weight_label = tk.Label(
            weight_frame, 
            text="体重(kg):", 
            font=("微软雅黑", 12, "bold"), 
            bg=self.colors['background_dark'], 
            fg=self.colors['text']
        )
        weight_label.pack(side='left')
        
        weight_entry = tk.Entry(
            weight_frame, 
            font=("微软雅黑", 14), 
            width=15,
            relief='solid',
            bd=2,
            justify='right'
        )
        weight_entry.pack(side='right')
        
        # 结果显示区域
        result_container = tk.Frame(win, bg=self.colors['background'])
        result_container.pack(pady=15, padx=25, fill='x')
        
        result_frame = tk.Frame(
            result_container,
            bg=self.colors['display_bg'], 
            relief='solid', 
            bd=2,
            highlightbackground=self.colors['border']
        )
        result_frame.pack(fill='x', ipady=15)
        
        result_label = tk.Label(
            result_frame,
            text="📝 请填写个人信息，哈基米将为您计算健康数据",
            font=("微软雅黑", 14),
            bg=self.colors['display_bg'],
            fg=self.colors['display_text'],
            wraplength=400,
            justify='center'
        )
        result_label.pack(pady=15)
        
        # 存储BMR计算数据和UI组件引用
        bmr_data = {}
        ui_refs = {}  # 存储UI组件引用
        
        # 简化的计算函数 - 直接在窗口内定义
        def calculate_bmr_simple():
            """简化的BMR计算函数"""
            try:
                print("=== BMR计算开始 ===")
                
                # 获取输入
                gender = gender_var.get()
                age_str = age_entry.get().strip()
                height_str = height_entry.get().strip()
                weight_str = weight_entry.get().strip()
                
                print(f"输入数据: 性别={gender}, 年龄={age_str}, 身高={height_str}, 体重={weight_str}")
                
                # 立即更新显示
                result_label.config(text="🔍 哈基米正在分析您的健康数据...")
                win.update()  # 强制更新界面
                
                # 验证输入
                if not all([age_str, height_str, weight_str]):
                    result_label.config(text="⚠️ 哈基米：请完整填写所有信息！\n💡 提示：年龄、身高、体重都要填写哦")
                    return
                
                # 转换数据
                try:
                    age = float(age_str)
                    height = float(height_str)
                    weight = float(weight_str)
                except ValueError:
                    result_label.config(text="❌ 哈基米：请输入有效的数字！\n💡 提示：只能输入数字，不要包含文字")
                    return
                
                print(f"转换后数据: 年龄={age}, 身高={height}, 体重={weight}")
                
                # 调用计算
                result, msg = self.calc.calculate_bmr(gender, age, height, weight)
                print(f"计算结果: result={result}, msg={msg}")
                
                # 显示结果
                result_label.config(text=msg)
                
                # 保存数据用于AI报告
                if result is not None:
                    # 从计算器获取BMI
                    bmi = weight / ((height/100) ** 2)
                    bmr_data['gender'] = gender
                    bmr_data['age'] = int(age)
                    bmr_data['height'] = int(height)
                    bmr_data['weight'] = float(weight)
                    bmr_data['bmr'] = int(result)
                    bmr_data['bmi'] = round(bmi, 1)
                    # 启用AI报告按钮
                    if 'ai_report_btn' in ui_refs:
                        ui_refs['ai_report_btn'].config(state='normal', bg='#FF69B4')
                        print("AI报告按钮已启用")
                
                # 更新角色表情
                if result is not None:
                    if result < 1300:
                        self.hajimi.react_to_special('BMR_low')
                    elif result < 1700:
                        self.hajimi.react_to_special('BMR_normal')
                    else:
                        self.hajimi.react_to_special('BMR_high')
                    self.update_character_display()
                
                print("=== BMR计算完成 ===")
                
            except Exception as e:
                print(f"BMR计算异常: {e}")
                result_label.config(text=f"😰 哈基米：计算出错了：{str(e)}\n💡 请检查输入的数据是否合理")
                import traceback
                traceback.print_exc()
        
        def generate_ai_report():
            """生成AI健康报告"""
            if not bmr_data:
                result_label.config(text="⚠️ 曼波～ 请先计算BMR数据哦！")
                return
            
            # 播放音效
            self.hajimi.play_sound("曼波欧耶.wav")
            
            # 显示加载状态
            result_label.config(text="🎨 哈基米正在生成你的专属健康报告...\n曼波～ 请稍等片刻～")
            win.update()
            
            # 生成AI报告
            try:
                report = self.ai.generate_bmr_report(
                    gender=bmr_data['gender'],
                    age=bmr_data['age'],
                    height=bmr_data['height'],
                    weight=bmr_data['weight'],
                    bmr=bmr_data['bmr'],
                    bmi=bmr_data['bmi']
                )
                
                # 显示报告窗口
                self.show_bmr_report(report, bmr_data)
                
            except Exception as e:
                print(f"生成AI报告失败: {e}")
                result_label.config(text=f"😰 哈基米：AI报告生成失败了\n💡 {str(e)}")
                import traceback
                traceback.print_exc()
        
        
        # 按钮区域
        button_frame = tk.Frame(win, bg=self.colors['background'])
        button_frame.pack(pady=15)
        
        # 计算按钮
        calc_btn = tk.Button(
            button_frame, 
            text="🏥 开始健康分析",
            font=("微软雅黑", 14, "bold"),
            bg=self.colors['primary'],
            fg='#FFFFFF',
            command=calculate_bmr_simple,
            width=18,
            height=2,
            relief='solid',
            bd=2,
            cursor='hand2'
        )
        calc_btn.pack(pady=5)
        
        # AI报告按钮
        ai_report_btn = tk.Button(
            button_frame,
            text="🎨 生成AI健康报告",
            font=("微软雅黑", 14, "bold"),
            bg='#CCCCCC',  # 初始灰色
            fg='#FFFFFF',
            command=generate_ai_report,
            width=18,
            height=2,
            relief='solid',
            bd=2,
            cursor='hand2',
            state='disabled'  # 初始禁用，计算后启用
        )
        ai_report_btn.pack(pady=5)
        
        # 存储按钮引用
        ui_refs['ai_report_btn'] = ai_report_btn
        
        # 返回按钮
        back_btn = tk.Button(
            button_frame,
            text="🔙 返回主界面",
            font=("微软雅黑", 12, "bold"),
            bg=self.colors['text_light'],
            fg='#FFFFFF',
            command=win.destroy,
            width=18,
            height=1,
            relief='solid',
            bd=2,
            cursor='hand2'
        )
        back_btn.pack(pady=5)
        
        
        # 示例提示
        example_frame = tk.Frame(win, bg=self.colors['background'])
        example_frame.pack(pady=(10, 20))
        
        example_label = tk.Label(
            example_frame,
            text="💡 示例数据：男，25岁，175cm，70kg\n📊 将得到：BMR≈1750kcal/天，BMI≈22.9(正常)",
            font=("微软雅黑", 10),
            bg=self.colors['background'],
            fg=self.colors['text_light'],
            justify='center'
        )
        example_label.pack()
    
    def show_bmr_report(self, report, bmr_data):
        """显示BMR健康报告窗口"""
        report_win = tk.Toplevel(self.master)
        report_win.title("🎨 哈基米专属健康报告")
        report_win.geometry("800x800")
        report_win.configure(bg=self.colors['background'])
        report_win.resizable(True, True)
        
        # 窗口居中
        report_win.update_idletasks()
        x = (report_win.winfo_screenwidth() // 2) - (800 // 2)
        y = (report_win.winfo_screenheight() // 2) - (800 // 2)
        report_win.geometry(f"800x800+{x}+{y}")
        
        # 标题
        title_frame = tk.Frame(report_win, bg=self.colors['primary'], height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🎀 哈基米的专属健康报告 🎀",
            font=("微软雅黑", 20, "bold"),
            bg=self.colors['primary'],
            fg='#FFFFFF'
        )
        title_label.pack(expand=True)
        
        # 报告内容区域（带滚动条）
        content_frame = tk.Frame(report_win, bg=self.colors['background'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 添加滚动条
        canvas = tk.Canvas(content_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 报告内容（使用Text widget显示Markdown格式）
        report_text = tk.Text(
            scrollable_frame,
            font=("微软雅黑", 11),
            bg='#FFFFFF',
            fg=self.colors['text'],
            wrap='word',
            padx=20,
            pady=20,
            relief='flat',
            bd=0
        )
        report_text.insert('1.0', report)
        report_text.config(state='disabled')  # 只读
        report_text.pack(fill='both', expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 底部按钮
        btn_frame = tk.Frame(report_win, bg=self.colors['background'])
        btn_frame.pack(fill='x', padx=20, pady=15)
        
        # 关闭按钮
        close_btn = tk.Button(
            btn_frame,
            text="关闭",
            font=("微软雅黑", 12, "bold"),
            bg=self.colors['text_light'],
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=15,
            command=report_win.destroy,
            cursor='hand2'
        )
        close_btn.pack(side='right', padx=5)
        
        # 播放庆祝音效
        self.hajimi.play_sound("帝皇私人笑声.wav")
    
    def open_chat_window(self):
        """打开与哈基米的对话窗口"""
        chat_win = tk.Toplevel(self.master)
        chat_win.title("💬 与哈基米对话")
        chat_win.geometry("600x700")
        chat_win.configure(bg=self.colors['background'])
        chat_win.resizable(True, True)
        
        # 窗口居中
        chat_win.update_idletasks()
        x = (chat_win.winfo_screenwidth() // 2) - (600 // 2)
        y = (chat_win.winfo_screenheight() // 2) - (700 // 2)
        chat_win.geometry(f"600x700+{x}+{y}")
        
        # 对话历史记录（保持记忆功能）
        conversation_history = []
        
        # 标题栏
        title_frame = tk.Frame(chat_win, bg=self.colors['primary'], height=70)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="💬 哈基米聊天室 - 曼波～ (带记忆功能)",
            font=("微软雅黑", 16, "bold"),
            bg=self.colors['primary'],
            fg='#FFFFFF'
        )
        title_label.pack(expand=True)
        
        # 对话记录区域
        chat_frame = tk.Frame(chat_win, bg='#FFFFFF')
        chat_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # 添加滚动条
        chat_scrollbar = tk.Scrollbar(chat_frame)
        chat_scrollbar.pack(side='right', fill='y')
        
        # 对话文本框
        chat_text = tk.Text(
            chat_frame,
            font=("微软雅黑", 11),
            bg='#FFFFFF',
            fg=self.colors['text'],
            wrap='word',
            padx=15,
            pady=15,
            yscrollcommand=chat_scrollbar.set,
            state='disabled'
        )
        chat_text.pack(side='left', fill='both', expand=True)
        chat_scrollbar.config(command=chat_text.yview)
        
        # 欢迎消息
        welcome_msg = "曼波～ 你好呀！我是哈基米！\n有什么想问我的吗？欧耶！💖\n\n💡 你可以问我：\n• 数学计算问题\n• 计算器功能\n• 健康建议\n• 或者随便聊聊天～\n\n🧠 提示：我现在有记忆功能啦！可以记住我们之前聊过的内容～"
        chat_text.config(state='normal')
        chat_text.insert('end', f"【哈基米】：{welcome_msg}\n\n", 'hajimi')
        chat_text.tag_config('hajimi', foreground=self.colors['primary'], font=("微软雅黑", 11, "bold"))
        chat_text.tag_config('user', foreground=self.colors['secondary_dark'], font=("微软雅黑", 11))
        chat_text.config(state='disabled')
        chat_text.see('end')
        
        # 输入区域
        input_frame = tk.Frame(chat_win, bg=self.colors['background'])
        input_frame.pack(fill='x', padx=15, pady=(15, 5))
        
        # 输入框
        input_entry = tk.Entry(
            input_frame,
            font=("微软雅黑", 12),
            bg='#FFFFFF',
            fg=self.colors['text'],
            relief='solid',
            bd=2
        )
        input_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        def send_message(event=None):
            """发送消息"""
            user_message = input_entry.get().strip()
            if not user_message:
                return
            
            # 显示用户消息
            chat_text.config(state='normal')
            chat_text.insert('end', f"【你】：{user_message}\n", 'user')
            chat_text.config(state='disabled')
            chat_text.see('end')
            
            # 清空输入框
            input_entry.delete(0, 'end')
            
            # 播放音效
            self.hajimi.play_operator_sound()
            
            # 显示"正在输入"
            chat_text.config(state='normal')
            chat_text.insert('end', "【哈基米】：正在思考...\n", 'hajimi')
            chat_text.config(state='disabled')
            chat_text.see('end')
            chat_win.update()
            
            # 构建对话上下文（最近5轮对话）
            context = ""
            if conversation_history:
                # 只取最近5轮对话，避免上下文过长
                recent_history = conversation_history[-5:]
                context_parts = []
                for i, (user_msg, ai_reply) in enumerate(recent_history, 1):
                    context_parts.append(f"第{i}轮 - 你问：{user_msg}\n哈基米答：{ai_reply}")
                context = "\n\n".join(context_parts)
            
            # 获取AI回复
            try:
                reply = self.ai.chat_with_hajimi(user_message, context=context)
                
                # 删除"正在思考"
                chat_text.config(state='normal')
                last_line_start = chat_text.index("end-2l linestart")
                chat_text.delete(last_line_start, 'end-1c')
                
                # 显示AI回复
                chat_text.insert('end', f"【哈基米】：{reply}\n\n", 'hajimi')
                chat_text.config(state='disabled')
                chat_text.see('end')
                
                # 将本轮对话加入历史记录
                conversation_history.append((user_message, reply))
                print(f"[对话记录] 用户：{user_message[:30]}... | 哈基米：{reply[:30]}...")
                print(f"[历史长度] 当前保存了 {len(conversation_history)} 轮对话")
                
                # 播放回复音效
                self.hajimi.play_sound("曼波（可爱.wav")
                
            except Exception as e:
                print(f"对话失败: {e}")
                chat_text.config(state='normal')
                last_line_start = chat_text.index("end-2l linestart")
                chat_text.delete(last_line_start, 'end-1c')
                error_reply = "曼波～ 出了点小问题，再试一次吧！💦"
                chat_text.insert('end', f"【哈基米】：{error_reply}\n\n", 'hajimi')
                chat_text.config(state='disabled')
                chat_text.see('end')
                # 即使出错也记录对话
                conversation_history.append((user_message, error_reply))
        
        # 数字键盘区域（初始隐藏）
        keyboard_frame = tk.Frame(chat_win, bg=self.colors['background'])
        keyboard_visible = [False]  # 使用列表来存储状态，方便在内部函数中修改
        
        def toggle_keyboard():
            """显示/隐藏数字键盘"""
            if keyboard_visible[0]:
                keyboard_frame.pack_forget()
                keyboard_visible[0] = False
                keyboard_btn.config(text="🔢 显示键盘")
            else:
                keyboard_frame.pack(fill='x', padx=15, pady=(0, 10))
                keyboard_visible[0] = True
                keyboard_btn.config(text="🔢 隐藏键盘")
        
        def insert_to_entry(text):
            """将文本插入到输入框的光标位置"""
            cursor_pos = input_entry.index(tk.INSERT)
            input_entry.insert(cursor_pos, text)
            input_entry.focus()
            # 播放对应音效
            if text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.hajimi.play_number_sound(text)
            elif text in ['+', '-', '×', '÷', '.']:
                self.hajimi.play_operator_sound(text)
            else:
                # 其他按钮（括号等）播放随机运算符音效
                self.hajimi.play_operator_sound()
        
        # 创建数字键盘布局（与主计算器完全一致）
        def create_chat_keyboard():
            """创建对话窗口的数字键盘 - 与主计算器设计完全一致"""
            keyboard_title = tk.Label(
                keyboard_frame,
                text="📱 完整计算器键盘",
                font=("微软雅黑", 11, "bold"),
                bg=self.colors['background'],
                fg=self.colors['primary']
            )
            keyboard_title.pack(pady=(5, 8))
            
            # 创建网格容器
            grid_frame = tk.Frame(keyboard_frame, bg=self.colors['background'])
            grid_frame.pack(padx=10, pady=(0, 10))
            
            # 配置网格权重
            for i in range(4):
                grid_frame.columnconfigure(i, weight=1)
            for i in range(8):
                grid_frame.rowconfigure(i, weight=1)
            
            # 完整的按钮布局 - 与主计算器相同
            buttons = [
                ['sin(', 'cos(', 'tan(', 'sqrt('],
                ['ln(', 'lg(', 'pi', 'e'],
                ['AC', '⌫', 'Del', '÷'],
                ['7', '8', '9', '×'],
                ['4', '5', '6', '-'],
                ['1', '2', '3', '+'],
                ['0', '.', '(', ')'],
                ['发送', '清空', '%', '=']
            ]
            
            def get_chat_button_style(text):
                """获取按钮样式 - 与主计算器一致"""
                if text.isdigit() or text == '.' or text == '0':
                    return 'number'
                elif text in ['÷', '×', '-', '+', '(', ')', '%']:
                    return 'operator'
                elif text == '=':
                    return 'equals'
                elif text in ['sin(', 'cos(', 'tan(', 'sqrt(', 'ln(', 'lg(', 'pi', 'e']:
                    return 'function'
                elif text in ['发送', '清空']:
                    return 'ai_control'
                else:  # AC, ⌫, Del
                    return 'control'
            
            def create_chat_styled_button(parent, text, style, row, column):
                """创建样式化按钮 - 与主计算器完全一致"""
                # 可爱的猫猫粉色主题配色（与主计算器相同）
                if style == 'number':
                    bg_color = '#FFE5EC'  # 非常浅的粉色
                    fg_color = '#8B4789'  # 深紫粉色文字
                    hover_color = '#FFD1DC'
                elif style == 'operator':
                    bg_color = '#FFB3C6'  # 浅粉色
                    fg_color = '#FFFFFF'
                    hover_color = '#FF99B3'
                elif style == 'equals':
                    bg_color = '#FF6B9D'  # 鲜艳粉色
                    fg_color = '#FFFFFF'
                    hover_color = '#FF5287'
                elif style == 'function':
                    bg_color = '#E8A5D4'  # 粉紫色
                    fg_color = '#FFFFFF'
                    hover_color = '#D98BC4'
                elif style == 'control':
                    bg_color = '#C9ADA7'  # 灰粉色
                    fg_color = '#FFFFFF'
                    hover_color = '#B39B96'
                elif style == 'ai_control':
                    bg_color = '#FF85A2'  # 亮粉色
                    fg_color = '#FFFFFF'
                    hover_color = '#FF6B8A'
                else:
                    bg_color = '#FFE5EC'
                    fg_color = '#8B4789'
                    hover_color = '#FFD1DC'
                
                # 创建 Frame 作为按钮容器（macOS 兼容方法）
                btn_frame = tk.Frame(
                    parent,
                    bg=bg_color,
                    relief='raised',
                    bd=2,
                    highlightthickness=0
                )
                btn_frame.grid(row=row, column=column, padx=3, pady=3, sticky='nsew')
                
                # 创建 Label 作为按钮文字
                btn_label = tk.Label(
                    btn_frame,
                    text=text,
                    font=("微软雅黑", 11, "bold"),
                    bg=bg_color,
                    fg=fg_color,
                    cursor='hand2',
                    padx=12,
                    pady=10
                )
                btn_label.pack(fill='both', expand=True)
                
                # 悬停效果
                def on_enter(event):
                    btn_frame.config(bg=hover_color)
                    btn_label.config(bg=hover_color)
                
                def on_leave(event):
                    btn_frame.config(bg=bg_color)
                    btn_label.config(bg=bg_color)
                
                def on_press(event):
                    btn_frame.config(relief='sunken')
                
                def on_release(event):
                    btn_frame.config(relief='raised')
                    # 处理点击事件
                    handle_chat_button_click(text)
                
                # 绑定事件
                btn_frame.bind("<Enter>", on_enter)
                btn_frame.bind("<Leave>", on_leave)
                btn_frame.bind("<ButtonPress-1>", on_press)
                btn_frame.bind("<ButtonRelease-1>", on_release)
                
                btn_label.bind("<Enter>", on_enter)
                btn_label.bind("<Leave>", on_leave)
                btn_label.bind("<ButtonPress-1>", on_press)
                btn_label.bind("<ButtonRelease-1>", on_release)
            
            def handle_chat_button_click(text):
                """处理键盘按钮点击"""
                if text == 'AC':
                    input_entry.delete(0, tk.END)
                elif text == '⌫':
                    cursor_pos = input_entry.index(tk.INSERT)
                    if cursor_pos > 0:
                        input_entry.delete(cursor_pos - 1)
                elif text == 'Del':
                    cursor_pos = input_entry.index(tk.INSERT)
                    input_entry.delete(cursor_pos)
                elif text == '发送' or text == '=':
                    send_message()
                elif text == '清空':
                    input_entry.delete(0, tk.END)
                else:
                    # 插入文本到光标位置
                    insert_to_entry(text)
            
            # 创建所有按钮
            for r, row in enumerate(buttons):
                for c, text in enumerate(row):
                    style = get_chat_button_style(text)
                    create_chat_styled_button(grid_frame, text, style, r, c)
        
        # 创建键盘（但不显示）
        create_chat_keyboard()
        
        # 键盘切换按钮
        keyboard_btn = tk.Button(
            input_frame,
            text="🔢 显示键盘",
            font=("微软雅黑", 11, "bold"),
            bg='#9B59B6',
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=10,
            command=toggle_keyboard,
            cursor='hand2'
        )
        keyboard_btn.pack(side='left', padx=5)
        
        # 发送按钮
        send_btn = tk.Button(
            input_frame,
            text="💬 发送",
            font=("微软雅黑", 12, "bold"),
            bg=self.colors['primary'],
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=10,
            command=send_message,
            cursor='hand2'
        )
        send_btn.pack(side='right')
        
        # 绑定Enter键发送
        input_entry.bind('<Return>', send_message)
        
        # 聚焦到输入框
        input_entry.focus()
        
        # 播放欢迎音效
        self.hajimi.play_sound("曼波欧耶.wav")
    
    def open_background_music(self):
        """打开背景音乐播放器"""
        music_win = tk.Toplevel(self.master)
        music_win.title("🎵 哈基米背景音乐")
        music_win.geometry("600x500")
        music_win.configure(bg=self.colors['background'])
        music_win.resizable(False, False)
        
        # 窗口居中
        music_win.update_idletasks()
        x = (music_win.winfo_screenwidth() // 2) - (600 // 2)
        y = (music_win.winfo_screenheight() // 2) - (500 // 2)
        music_win.geometry(f"600x500+{x}+{y}")
        
        # 标题区域
        title_frame = tk.Frame(music_win, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🎵 哈基米背景音乐播放器 🎵",
            font=("微软雅黑", 16, "bold"),
            bg=self.colors['primary'],
            fg='#FFFFFF'
        )
        title_label.pack(expand=True)
        
        # 主内容区域
        content_frame = tk.Frame(music_win, bg=self.colors['background'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 当前播放状态
        status_frame = tk.Frame(content_frame, bg='#FFE5EC', relief='solid', bd=2)
        status_frame.pack(fill='x', pady=10)
        
        status_title = tk.Label(
            status_frame,
            text="🎶 当前播放状态",
            font=("微软雅黑", 12, "bold"),
            bg='#FFE5EC',
            fg=self.colors['primary_dark']
        )
        status_title.pack(pady=8)
        
        # 状态显示
        self.bg_music_status_label = tk.Label(
            status_frame,
            text="🎵 暂无播放",
            font=("微软雅黑", 11),
            bg='#FFE5EC',
            fg=self.colors['text'],
            wraplength=500,
            justify='center'
        )
        self.bg_music_status_label.pack(pady=5)
        
        # 音乐文件列表
        music_files = [
            ("万恶之源", "万恶之源.WAV"),
            ("万恶之源2", "万恶之源2.WAV"),
            ("2.23AM", "2.23AM.WAV"),
            ("世上最小的哈基米", "世上最小的哈基米.WAV"),
            ("来去曼波", "来去曼波.WAV"),
            ("柠檬树上哈基果", "柠檬树上哈基果.WAV"),
            ("孤高曼波", "孤高曼波.WAV"),
            ("神曼波", "神曼波.WAV"),
            ("夜哈", "夜哈.WAV"),
            ("打火基", "打火基.WAV"),
            ("野哈飞舞", "野哈飞舞.WAV"),
            ("曼波、曼波、有时哈基米", "曼波、曼波、有时哈基米.WAV"),
            ("曼波你身", "曼波你身.WAV"),
            ("哈基山的基米美如水啊", "哈基山的基米美如水啊.WAV"),
            ("太空曼波", "太空曼波.WAV"),
            ("哈雪大冒险", "哈雪大冒险.WAV"),
            ("最后一哈", "最后一哈.WAV"),
            ("不再曼波", "不再曼波.WAV"),
            ("蓝莲哈", "蓝莲哈.WAV"),
            ("基米说", "基米说.WAV")
        ]
        
        # 歌曲选择区域
        song_frame = tk.Frame(content_frame, bg=self.colors['background'])
        song_frame.pack(fill='x', pady=10)
        
        song_title = tk.Label(
            song_frame,
            text="🎶 选择背景音乐:",
            font=("微软雅黑", 12, "bold"),
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        song_title.pack(anchor='w', pady=(0, 5))
        
        # 歌曲列表容器（带滚动条）
        list_container = tk.Frame(song_frame, bg=self.colors['background'])
        list_container.pack(fill='both', expand=True)
        
        # 创建滚动条
        list_canvas = tk.Canvas(list_container, bg=self.colors['background'], highlightthickness=0)
        list_scrollbar = tk.Scrollbar(list_container, orient="vertical", command=list_canvas.yview)
        scrollable_list = tk.Frame(list_canvas, bg=self.colors['background'])
        
        scrollable_list.bind(
            "<Configure>",
            lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
        )
        
        list_canvas.create_window((0, 0), window=scrollable_list, anchor="nw")
        list_canvas.configure(yscrollcommand=list_scrollbar.set)
        
        # 创建歌曲列表项
        for i, (song_name, song_file) in enumerate(music_files):
            song_item_frame = tk.Frame(scrollable_list, bg='#FFE5F0', relief='raised', bd=1)
            song_item_frame.pack(fill='x', pady=2, padx=5)
            
            # 歌曲信息
            song_info = tk.Label(
                song_item_frame,
                text=f"{i+1}. {song_name}",
                font=("微软雅黑", 10),
                bg='#FFE5F0',
                fg=self.colors['text'],
                anchor='w'
            )
            song_info.pack(side='left', padx=10, pady=5)
            
            # 播放按钮
            play_btn = tk.Button(
                song_item_frame,
                text="▶️ 播放",
                font=("微软雅黑", 8, "bold"),
                bg=self.colors['primary'],
                fg='#FFFFFF',
                relief='raised',
                bd=1,
                cursor='hand2',
                command=lambda f=song_file, n=song_name: self.play_background_music(f, n)
            )
            play_btn.pack(side='right', padx=10, pady=3)
        
        list_canvas.pack(side="left", fill="both", expand=True)
        list_scrollbar.pack(side="right", fill="y")
        
        # 控制按钮区域
        control_frame = tk.Frame(content_frame, bg=self.colors['background'])
        control_frame.pack(fill='x', pady=15)
        
        # 播放控制按钮
        control_buttons_frame = tk.Frame(control_frame, bg=self.colors['background'])
        control_buttons_frame.pack()
        
        # 暂停/继续按钮
        self.bg_music_pause_btn = tk.Button(
            control_buttons_frame,
            text="⏸️ 暂停",
            font=("微软雅黑", 11, "bold"),
            bg=self.colors['secondary'],
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=10,
            command=self.toggle_background_music,
            cursor='hand2'
        )
        self.bg_music_pause_btn.pack(side='left', padx=5)
        
        # 停止按钮
        self.bg_music_stop_btn = tk.Button(
            control_buttons_frame,
            text="⏹️ 停止",
            font=("微软雅黑", 11, "bold"),
            bg=self.colors['danger'],
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=10,
            command=self.stop_background_music,
            cursor='hand2'
        )
        self.bg_music_stop_btn.pack(side='left', padx=5)
        
        # 音量控制
        volume_frame = tk.Frame(control_frame, bg=self.colors['background'])
        volume_frame.pack(pady=10)
        
        volume_label = tk.Label(
            volume_frame,
            text="🔊 背景音乐音量:",
            font=("微软雅黑", 10, "bold"),
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        volume_label.pack()
        
        # 音量滑块
        self.bg_music_volume_scale = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient='horizontal',
            bg=self.colors['background'],
            fg=self.colors['text'],
            highlightthickness=0,
            length=300,
            command=self.set_background_music_volume
        )
        self.bg_music_volume_scale.set(30)  # 背景音乐默认音量30%
        self.bg_music_volume_scale.pack(pady=5)
        
        # 关闭按钮
        close_btn = tk.Button(
            control_frame,
            text="关闭",
            font=("微软雅黑", 11, "bold"),
            bg=self.colors['text_light'],
            fg='#FFFFFF',
            relief='raised',
            bd=2,
            width=15,
            command=music_win.destroy,
            cursor='hand2'
        )
        close_btn.pack(pady=10)
        
        # 初始化背景音乐状态
        self.current_bg_music = None
        self.is_bg_music_playing = False
        
        # 播放欢迎音效
        self.hajimi.play_sound("曼波欧耶.wav")
    
    def play_background_music(self, song_file, song_name):
        """播放背景音乐"""
        try:
            # 停止当前播放
            if self.current_bg_music:
                pygame.mixer.music.stop()
            
            # 设置新歌曲
            self.current_bg_music = song_file
            self.is_bg_music_playing = True
            
            # 播放音乐
            music_path = os.path.join(os.path.dirname(__file__), "../shucai/music", song_file)
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                # 背景音乐音量较低
                bg_volume = self.bg_music_volume_scale.get() / 100.0
                pygame.mixer.music.set_volume(bg_volume)
                pygame.mixer.music.play(-1)  # 循环播放
                
                # 更新状态显示
                self.bg_music_status_label.config(text=f"🎵 正在播放: {song_name}\n🔄 循环播放模式")
                
                # 播放成功音效
                self.hajimi.play_sound("曼波欧耶.wav")
            else:
                self.bg_music_status_label.config(text=f"❌ 文件未找到: {song_file}")
                
        except Exception as e:
            print(f"播放背景音乐失败: {e}")
            self.bg_music_status_label.config(text=f"❌ 播放失败: {str(e)}")
    
    def toggle_background_music(self):
        """切换背景音乐播放/暂停状态"""
        if not self.current_bg_music:
            return
            
        try:
            if self.is_bg_music_playing:
                # 当前正在播放，暂停
                pygame.mixer.music.pause()
                self.is_bg_music_playing = False
                self.bg_music_pause_btn.config(text="▶️ 继续")
                self.bg_music_status_label.config(text=self.bg_music_status_label.cget('text').replace("正在播放", "已暂停"))
            else:
                # 当前暂停，继续播放
                pygame.mixer.music.unpause()
                self.is_bg_music_playing = True
                self.bg_music_pause_btn.config(text="⏸️ 暂停")
                self.bg_music_status_label.config(text=self.bg_music_status_label.cget('text').replace("已暂停", "正在播放"))
        except Exception as e:
            print(f"切换背景音乐状态失败: {e}")
    
    def stop_background_music(self):
        """停止背景音乐播放"""
        try:
            pygame.mixer.music.stop()
            self.current_bg_music = None
            self.is_bg_music_playing = False
            self.bg_music_status_label.config(text="🎵 暂无播放")
            self.bg_music_pause_btn.config(text="⏸️ 暂停")
        except Exception as e:
            print(f"停止背景音乐失败: {e}")
    
    def set_background_music_volume(self, volume):
        """设置背景音乐音量"""
        try:
            volume_float = int(volume) / 100.0
            pygame.mixer.music.set_volume(volume_float)
        except Exception as e:
            print(f"设置背景音乐音量失败: {e}")
    
    
    