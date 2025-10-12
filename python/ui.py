import tkinter as tk
import math
from calculator import Calculator
from character import HajimiCharacter
from AI import HajimiAI


class HajimiUI:
    def __init__(self, master):
        self.master = master
        self.calc = Calculator()
        self.hajimi = HajimiCharacter()
        self.ai = HajimiAI()

        # 哈基米主题色彩 - 更丰富的配色
        self.colors = {
            'primary': '#FF6B9D',      # 粉色主色调
            'primary_light': '#FFB3D1', # 浅粉色
            'primary_dark': '#E91E63',  # 深粉色
            'secondary': '#4ECDC4',    # 薄荷绿
            'secondary_light': '#81E6D9', # 浅薄荷绿
            'accent': '#45B7D1',       # 天蓝色
            'accent_light': '#74C0FC', # 浅天蓝
            'background': '#F8F9FA',   # 浅灰背景
            'background_dark': '#E9ECEF', # 深灰背景
            'text': '#2C3E50',         # 深蓝文字
            'text_light': '#6C757D',   # 浅灰文字
            'button_normal': '#FFFFFF', # 白色按钮
            'button_hover': '#E8F4FD',  # 悬停效果
            'display_bg': '#2C3E50',   # 深色显示区
            'display_text': '#FFFFFF',  # 白色显示文字
            'shadow': '#00000020',     # 阴影色
            'border': '#DEE2E6',       # 边框色
            'success': '#28A745',      # 成功色
            'warning': '#FFC107',      # 警告色
            'danger': '#DC3545'        # 危险色
        }
        
        # 设置主窗口样式
        self.master.configure(bg=self.colors['background'])
        
        # 创建界面布局
        self.create_title()
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
        
        # 副标题装饰
        subtitle_label = tk.Label(
            title_frame,
            text="🐱 曼波的计算助手 🐱",
            font=("微软雅黑", 10),
            bg=self.colors['background'],
            fg=self.colors['text_light']
        )
        subtitle_label.pack(pady=(2, 0))
    
    def create_display_area(self):
        """创建显示区域"""
        # 主显示区域容器
        main_display_frame = tk.Frame(self.master, bg=self.colors['background'])
        main_display_frame.pack(pady=15, padx=25, fill='x')
        
        # 左侧：计算显示区域 - 添加渐变效果
        display_frame = tk.Frame(
            main_display_frame, 
            bg=self.colors['display_bg'], 
            relief='solid', 
            bd=2,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        display_frame.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # 输入显示区域装饰
        input_container = tk.Frame(display_frame, bg=self.colors['display_bg'])
        input_container.pack(fill='x', padx=15, pady=(15, 5))
        
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
        self.input_label.pack(fill='x', pady=(2, 0))
        
        # 分隔线
        separator = tk.Frame(display_frame, height=1, bg=self.colors['border'])
        separator.pack(fill='x', padx=15, pady=5)
        
        # 计算结果区域
        calc_result_container = tk.Frame(display_frame, bg=self.colors['display_bg'])
        calc_result_container.pack(fill='x', padx=15, pady=(5, 5))
        
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
        self.calc_result_label.pack(fill='x', pady=(2, 0))
        
        # 哈基米评论区域
        comment_container = tk.Frame(display_frame, bg=self.colors['display_bg'])
        comment_container.pack(fill='x', padx=15, pady=(5, 15))
        
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
        self.result_label.pack(fill='x', pady=(2, 0))
        
        # 右侧：角色表情区域 - 美化设计
        character_frame = tk.Frame(
            main_display_frame, 
            bg=self.colors['display_bg'], 
            relief='solid', 
            bd=2,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        character_frame.pack(side='right', fill='y', ipadx=10)
        
        # 角色标题
        character_title = tk.Label(
            character_frame,
            text="曼波状态",
            font=("微软雅黑", 9),
            bg=self.colors['display_bg'],
            fg=self.colors['text_light']
        )
        character_title.pack(pady=(10, 5))
        
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
            text="曼波",
            font=("微软雅黑", 11, "bold"),
            bg=self.colors['display_bg'],
            fg=self.colors['primary']
        )
        self.character_status_label.pack(pady=(5, 15))
    
    
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
        """创建简洁实用的按钮布局"""
        # 主按钮网格容器
        main_grid = tk.Frame(self.button_container, bg=self.colors['background'])
        main_grid.pack(expand=True)
        
        # 传统计算器布局 - 4列布局
        buttons = [
            # 第一行：控制键和运算符
            ['AC', '⌫', 'Del', '÷'],
            # 第二行：数字和运算符
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            # 第五行：0和小数点
            ['0', '.', '(', ')'],
            # 第六行：三角函数和百分比
            ['sin(', 'cos(', '%', '='],
            # 第七行：其他科学函数
            ['tan(', 'sqrt(', 'ln(', 'lg('],
            # 第八行：常量和特殊功能
            ['pi', 'e', 'BMR', '静音']
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
        else:  # AC, ⌫, Del, 静音
            return 'control'
    
    
    def create_styled_button(self, parent, text, style, row, column):
        """创建样式化按钮"""
        styles = {
            'number': {
                'bg': self.colors['button_normal'], 
                'fg': self.colors['text'],
                'activebackground': self.colors['button_hover'],
                'activeforeground': self.colors['text']
            },
            'operator': {
                'bg': self.colors['secondary'], 
                'fg': '#FFFFFF',
                'activebackground': self.colors['secondary_light'],
                'activeforeground': '#FFFFFF'
            },
            'equals': {
                'bg': self.colors['success'], 
                'fg': '#FFFFFF',
                'activebackground': '#218838',
                'activeforeground': '#FFFFFF'
            },
            'bmr': {
                'bg': self.colors['warning'], 
                'fg': '#FFFFFF',
                'activebackground': '#E0A800',
                'activeforeground': '#FFFFFF'
            },
            'function': {
                'bg': self.colors['primary'], 
                'fg': '#FFFFFF',
                'activebackground': self.colors['primary_light'],
                'activeforeground': '#FFFFFF'
            },
            'control': {
                'bg': self.colors['text_light'], 
                'fg': '#FFFFFF',
                'activebackground': self.colors['text'],
                'activeforeground': '#FFFFFF'
            }
        }
        
        btn = tk.Button(
            parent,
            text=text,
            font=("微软雅黑", 12, "bold"),
            width=8, height=2,
            relief='solid',
            bd=1,
            command=lambda val=text: self.on_click(val),
            cursor='hand2',
            **styles[style]
        )
        btn.grid(row=row, column=column, padx=4, pady=4, sticky='nsew')
        
        # 添加悬停效果和按下效果
        btn.bind("<Enter>", lambda e, b=btn: self.button_hover_enter(b, styles[style]))
        btn.bind("<Leave>", lambda e, b=btn: self.button_hover_leave(b, styles[style]))
        btn.bind("<Button-1>", lambda e, b=btn: self.button_press_effect(b, styles[style]))
        
        return btn
    
    def button_hover_enter(self, button, style):
        """按钮悬停进入效果"""
        if 'activebackground' in style:
            button.config(bg=style['activebackground'])
            if 'activeforeground' in style:
                button.config(fg=style['activeforeground'])
    
    def button_hover_leave(self, button, style):
        """按钮悬停离开效果"""
        button.config(bg=style['bg'])
        button.config(fg=style['fg'])
    
    def button_press_effect(self, button, style):
        """按钮按下效果"""
        original_bg = button.cget('bg')
        original_fg = button.cget('fg')
        
        # 按下时的颜色（稍微深一点）
        press_bg = self.darken_color(original_bg)
        press_fg = original_fg
        
        button.config(bg=press_bg, fg=press_fg)
        
        # 100ms后恢复原色
        self.master.after(100, lambda: button.config(bg=original_bg, fg=original_fg))
    
    def darken_color(self, color):
        """将颜色变深"""
        color_map = {
            self.colors['button_normal']: self.colors['background_dark'],
            self.colors['secondary']: '#3AB4A8',
            self.colors['primary']: self.colors['primary_dark'],
            self.colors['text_light']: '#495057',
            self.colors['success']: '#1E7E34',
            self.colors['warning']: '#D39E00'
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
            if '.' in current.split('+')[-1].split('-')[-1].split('*')[-1].split('/')[-1]:
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
        ai_response = self.ai.comment(result, msg)
        
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
            'default': "东海帝王",
            'happy': "开心！",
            'satisfied': "满意！",
            'surprised': "惊讶！",
            'angry': "生气！",
            'furious': "暴怒！",
            'sad': "难过...",
            'tired': "困倦...",
            'expressionless': "无语..."
        }
        status = status_texts.get(self.hajimi.current_expression, "东海帝王")
        self.character_status_label.config(text=status)
    
    def toggle_mute(self):
        """切换静音状态"""
        self.hajimi.mute = not self.hajimi.mute
        status = "静音" if self.hajimi.mute else "有声"
        self.result_label.config(text=f"哈基米：{status}模式！")
        
        # 更新角色表情
        special_type = 'mute_on' if self.hajimi.mute else 'mute_off'
        self.hajimi.react_to_special(special_type)
        self.update_character_display()
    
    def update_character_display(self):
        """更新角色显示"""
        expression_img = self.hajimi.get_expression(self.hajimi.current_expression)
        self.character_label.config(image=expression_img)
        
        # 更新角色状态文字
        status_texts = {
            'default': "曼波",
            'happy': "开心！",
            'satisfied': "满意！",
            'surprised': "惊讶！",
            'angry': "生气！",
            'furious': "暴怒！",
            'sad': "难过...",
            'tired': "困倦...",
            'expressionless': "无语..."
        }
        status = status_texts.get(self.hajimi.current_expression, "东海帝王")
        self.character_status_label.config(text=status)

    def open_bmr_window(self):
        """打开BMR计算窗口"""
        win = tk.Toplevel(self.master)
        win.title("基础代谢率计算 🏃‍♀️")
        win.geometry("380x450")
        win.configure(bg=self.colors['background'])
        win.resizable(False, False)
        
        # 设置窗口图标和居中
        try:
            win.iconbitmap(default='icon.ico')
        except:
            pass
        
        # 窗口居中
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (380 // 2)
        y = (win.winfo_screenheight() // 2) - (450 // 2)
        win.geometry(f"380x450+{x}+{y}")
        
        # 标题区域
        title_frame = tk.Frame(win, bg=self.colors['background'])
        title_frame.pack(pady=25, padx=20, fill='x')
        
        title_label = tk.Label(
            title_frame, 
            text="BMR 基础代谢率计算",
            font=("微软雅黑", 18, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="💪 计算您的每日基础代谢需求",
            font=("微软雅黑", 10),
            bg=self.colors['background'],
            fg=self.colors['text_light']
        )
        subtitle_label.pack(pady=(5, 0))
        
        # 输入框架 - 添加装饰边框
        input_container = tk.Frame(win, bg=self.colors['background'])
        input_container.pack(pady=20, padx=25, fill='x')
        
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
            font=("微软雅黑", 12), 
            width=12,
            relief='solid',
            bd=1,
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
            font=("微软雅黑", 12), 
            width=12,
            relief='solid',
            bd=1,
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
            font=("微软雅黑", 12), 
            width=12,
            relief='solid',
            bd=1,
            justify='right'
        )
        weight_entry.pack(side='right')
        
        # 计算按钮区域
        button_frame = tk.Frame(win, bg=self.colors['background'])
        button_frame.pack(pady=20)
        
        calc_btn = tk.Button(
            button_frame, 
            text="计算 BMR",
            font=("微软雅黑", 14, "bold"),
            bg=self.colors['primary'],
            fg='#FFFFFF',
            command=lambda: self.calc_bmr_in_window(win, gender_var, age_entry, height_entry, weight_entry, result_label),
            width=18,
            height=2,
            relief='solid',
            bd=1,
            cursor='hand2'
        )
        calc_btn.pack()
        
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
            text="请输入信息后点击计算",
            font=("微软雅黑", 12),
            bg=self.colors['display_bg'],
            fg=self.colors['display_text'],
            wraplength=280,
            justify='center'
        )
        result_label.pack(pady=10)
        
        # 预设示例
        example_frame = tk.Frame(win, bg=self.colors['background'])
        example_frame.pack(pady=(10, 20))
        
        example_label = tk.Label(
            example_frame,
            text="💡 示例：男，25岁，175cm，70kg",
            font=("微软雅黑", 10),
            bg=self.colors['background'],
            fg=self.colors['text_light']
        )
        example_label.pack()
    
    def calc_bmr_in_window(self, win, gender_var, age_entry, height_entry, weight_entry, result_label):
        """在BMR窗口中执行计算"""
        try:
            gender = gender_var.get()
            age = float(age_entry.get())
            height = float(height_entry.get())
            weight = float(weight_entry.get())
            
            result, msg = self.calc.calculate_bmr(gender, age, height, weight)
            result_label.config(text=msg)
            
            # 根据BMR结果选择表情
            if result < 1300:
                self.hajimi.react_to_special('BMR_low')
            elif result < 1700:
                self.hajimi.react_to_special('BMR_normal')
            else:
                self.hajimi.react_to_special('BMR_high')
            
            # 更新主界面角色表情
            self.update_character_display()
        except ValueError:
            result_label.config(text="哈基米：请输入有效的数字！")
            self.hajimi.react_to_error("输入错误")
            self.update_character_display()