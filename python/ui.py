import tkinter as tk
import math
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
            'background': '#FDFCFB',   # 温暖背景
            'background_dark': '#F5F3F0', # 深灰背景
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
        """创建标题区域"""
        # 标题容器框架，添加阴影效果
        title_frame = tk.Frame(self.master, bg=self.colors['background'])
        title_frame.pack(pady=(15, 10))
        
        # 主标题
        title_label = tk.Label(
            title_frame, 
            text="哈基米计算器", 
            font=("微软雅黑", 22, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        title_label.pack()
        
    def create_display_area(self):
        """创建圆润美观的显示区域"""
        # 主显示区域容器 - 增加内边距
        main_display_frame = tk.Frame(self.master, bg=self.colors['background'])
        main_display_frame.pack(pady=20, padx=30, fill='x')
        
        # 左侧：计算显示区域 - 更柔和的边框
        display_frame = tk.Frame(
            main_display_frame, 
            bg=self.colors['display_bg'], 
            relief='solid', 
            bd=1,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        display_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
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
            font=("Consolas", 18, "bold"),
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
        
        # 计算结果显示
        self.calc_result_label = tk.Label(
            calc_result_container,
            text="",
            font=("Consolas", 16, "bold"),
            bg=self.colors['display_bg'],
            fg='#E9ECEF',
            anchor='e',
            height=1
        )
        self.calc_result_label.pack(fill='x', pady=2)
        
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
        
        # 右侧：角色表情区域 - 更圆润的设计
        character_frame = tk.Frame(
            main_display_frame, 
            bg=self.colors['display_bg'], 
            relief='solid', 
            bd=1,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        character_frame.pack(side='right', fill='y', ipadx=15, ipady=10)
        
        # 角色标题
        character_title = tk.Label(
            character_frame,
            text="哈基米状态",
            font=("微软雅黑", 9),
            bg=self.colors['display_bg'],
            fg=self.colors['text_light']
        )
        character_title.pack(pady=10)
        
        # 角色表情标签
        self.character_label = tk.Label(
            character_frame,
            image=self.hajimi.get_expression('default'),
            bg=self.colors['display_bg']
        )
        self.character_label.pack(pady=5)
        
        # 角色状态标签
        self.character_status_label = tk.Label(
            character_frame,
            text="哈基米",
            font=("微软雅黑", 11, "bold"),
            bg=self.colors['display_bg'],
            fg=self.colors['primary']
        )
        self.character_status_label.pack(pady=10)
    
    def create_sound_control(self):
        """创建紧凑的声音控制面板"""
        # 声音控制容器 - 紧凑设计
        sound_frame = tk.Frame(self.master, bg=self.colors['background'])
        sound_frame.pack(pady=8, padx=20, fill='x')
        
        # 左侧：音量滑块和标签
        left_frame = tk.Frame(sound_frame, bg=self.colors['background'])
        left_frame.pack(side='left', fill='x', expand=True)
        
        # 音量标签和滑块在同一行
        volume_row = tk.Frame(left_frame, bg=self.colors['background'])
        volume_row.pack(fill='x')
        
        # 音量标签
        self.volume_label = tk.Label(
            volume_row,
            text="音量: 50%",
            font=("微软雅黑", 9),
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        self.volume_label.pack(side='left', padx=(0, 8))
        
        # 音量滑块 - 更紧凑
        self.volume_scale = tk.Scale(
            volume_row,
            from_=0,
            to=100,
            orient='horizontal',
            length=100,
            resolution=10,
            bg=self.colors['background'],
            fg=self.colors['text'],
            highlightthickness=0,
            troughcolor=self.colors['secondary_light'],
            activebackground=self.colors['secondary'],
            command=self.on_volume_change
        )
        self.volume_scale.set(50)  # 默认音量50%
        self.volume_scale.pack(side='left', padx=(0, 10))
        
        # 右侧：控制按钮
        right_frame = tk.Frame(sound_frame, bg=self.colors['background'])
        right_frame.pack(side='right')
        
        # 静音按钮 - 紧凑设计
        self.mute_button = tk.Button(
            right_frame,
            text="🔇",
            font=("微软雅黑", 10, "bold"),
            bg=self.colors['text_light'],
            fg='#FFFFFF',
            relief='flat',
            bd=0,
            width=3,
            height=1,
            command=self.toggle_mute,
            cursor='hand2'
        )
        self.mute_button.pack(side='left', padx=5)
        
        # 音量指示器 - 紧凑设计
        self.volume_indicator = tk.Label(
            right_frame,
            text="🔊",
            font=("微软雅黑", 12),
            bg=self.colors['background'],
            fg=self.colors['success']
        )
        self.volume_indicator.pack(side='left', padx=5)
    
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
        """创建统一圆润样式化按钮"""
        # 简化为两种主要样式：粉色系和薄荷绿系
        if style == 'number':
            btn_config = {
                'bg': self.colors['button_normal'], 
                'fg': self.colors['text'],
                'activebackground': self.colors['button_hover'],
                'activeforeground': self.colors['text']
            }
        elif style == 'operator':
            btn_config = {
                'bg': self.colors['secondary'], 
                'fg': '#FFFFFF',
                'activebackground': self.colors['secondary_light'],
                'activeforeground': '#FFFFFF'
            }
        elif style == 'equals':
            btn_config = {
                'bg': self.colors['primary'], 
                'fg': '#FFFFFF',
                'activebackground': self.colors['primary_light'],
                'activeforeground': '#FFFFFF'
            }
        elif style == 'function':
            btn_config = {
                'bg': self.colors['primary'], 
                'fg': '#FFFFFF',
                'activebackground': self.colors['primary_light'],
                'activeforeground': '#FFFFFF'
            }
        elif style == 'bmr':
            btn_config = {
                'bg': self.colors['secondary'], 
                'fg': '#FFFFFF',
                'activebackground': self.colors['secondary_light'],
                'activeforeground': '#FFFFFF'
            }
        elif style == 'control':
            btn_config = {
                'bg': self.colors['text_light'], 
                'fg': '#FFFFFF',
                'activebackground': self.colors['text'],
                'activeforeground': '#FFFFFF'
            }
        elif style == 'ai_control':
            btn_config = {
                'bg': self.colors['primary'], 
                'fg': '#FFFFFF',
                'activebackground': self.colors['primary_light'],
                'activeforeground': '#FFFFFF'
            }
        else:
            # 默认样式
            btn_config = {
                'bg': self.colors['button_normal'], 
                'fg': self.colors['text'],
                'activebackground': self.colors['button_hover'],
                'activeforeground': self.colors['text']
            }
        
        # 创建圆润按钮
        btn = tk.Button(
            parent,
            text=text,
            font=("微软雅黑", 12, "bold"),
            width=8, height=2,
            relief='flat',
            bd=0,
            padx=12,
            pady=8,
            command=lambda val=text: self.on_click(val),
            cursor='hand2',
            **btn_config
        )
        btn.grid(row=row, column=column, padx=4, pady=4, sticky='nsew')
        
        # 添加悬停效果和按下效果
        btn.bind("<Enter>", lambda e, b=btn: self.button_hover_enter(b, btn_config))
        btn.bind("<Leave>", lambda e, b=btn: self.button_hover_leave(b, btn_config))
        btn.bind("<Button-1>", lambda e, b=btn: self.button_press_effect(b, btn_config))
        
        return btn
    
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
        """将颜色变深 - 双色调深色效果"""
        color_map = {
            self.colors['button_normal']: self.colors['background_dark'],
            self.colors['secondary']: self.colors['secondary_dark'],  # 薄荷绿深色
            self.colors['primary']: self.colors['primary_dark'],      # 粉色深色
            self.colors['text_light']: '#6B7280',
        }
        return color_map.get(color, color)
    

    def on_click(self, val):
        """按钮点击事件处理"""
        # 添加按钮按下动画效果
        self.button_press_animation(val)
        
        if val == "AC":
            self.clear_display()
            self.hajimi.play_sound("Hardware Remove.wav")
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
        self.hajimi.play_random()

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
        
        # 更新显示
        self.update_display(result, ai_response, msg)
        
        # 更新角色表情和音效
        self.update_character_expression(result, msg)
        self.hajimi.react(result)
        
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
        """更新角色表情"""
        if result is None:
            self.hajimi.react_to_error(msg)
        else:
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
        
        # 更新音量标签
        if hasattr(self, 'volume_label'):
            self.volume_label.config(text=f"音量: {volume}%")
        
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
            self.volume_scale.set(int(self.hajimi.volume * 100))
            self.mute_button.config(text="🔇", bg=self.colors['text_light'])
            status = "有声"
        else:
            # 静音
            self.hajimi.mute = True
            self.volume_scale.set(0)
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

    def open_bmr_window(self):
        """打开BMR计算窗口 - 重新设计的简化版本"""
        win = tk.Toplevel(self.master)
        win.title("🏥 哈基米健康数据计算器")
        win.geometry("500x650")  # 增大窗口尺寸
        win.configure(bg=self.colors['background'])
        win.resizable(True, True)  # 允许调整大小
        
        # 设置窗口图标和居中
        try:
            win.iconbitmap(default='icon.ico')
        except:
            pass
        
        # 窗口居中
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (500 // 2)
        y = (win.winfo_screenheight() // 2) - (650 // 2)
        win.geometry(f"500x650+{x}+{y}")
        
        # 设置最小尺寸
        win.minsize(450, 600)
        
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
        
        
        # 按钮区域
        button_frame = tk.Frame(win, bg=self.colors['background'])
        button_frame.pack(pady=15)
        
        # 计算按钮
        calc_btn = tk.Button(
            button_frame, 
            text="🏥 开始健康分析",
            font=("微软雅黑", 16, "bold"),
            bg=self.colors['primary'],
            fg='#FFFFFF',
            command=calculate_bmr_simple,
            width=20,
            height=3,
            relief='solid',
            bd=2,
            cursor='hand2'
        )
        calc_btn.pack(pady=10)
        
        
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
    
    