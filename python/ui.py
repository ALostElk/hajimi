import tkinter as tk
from calculator import Calculator
from character import HajimiCharacter
from AI import HajimiAI


class HajimiUI:
    def __init__(self, master):
        self.master = master
        self.calc = Calculator()
        self.hajimi = HajimiCharacter()
        self.ai = HajimiAI()

        # 界面布局
        self.display = tk.Text(master, height=2, width=30, font=("微软雅黑", 20))
        self.display.pack(pady=10)

        self.result_label = tk.Label(master, text="哈基米：准备好了！", font=("微软雅黑", 14))
        self.result_label.pack(pady=5)

        # 按键布局
        self.create_buttons()

    def create_buttons(self):
        frame = tk.Frame(self.master)
        frame.pack()

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+'],
            ['sin', 'cos', 'tan', '√'],
            ['ln', 'lg', 'x²', 'x!'],
            ['AC', '⌫', 'BMR', '静音']
        ]

        for r, row in enumerate(buttons):
            for c, text in enumerate(row):
                btn = tk.Button(frame, text=text, width=6, height=2, font=("微软雅黑", 14),
                                command=lambda val=text: self.on_click(val))
                btn.grid(row=r, column=c, padx=3, pady=3)

    def on_click(self, val):
        if val == "AC":
            self.display.delete(1.0, tk.END)
            self.hajimi.play_sound("Hardware Remove.wav")
            return
        if val == "⌫":
            content = self.display.get(1.0, tk.END)[:-2]
            self.display.delete(1.0, tk.END)
            self.display.insert(tk.END, content)
            return
        if val == "=":
            expr = self.display.get(1.0, tk.END).strip()
            result, msg = self.calc.evaluate(expr)
            self.result_label.config(text=self.ai.comment(result, msg))
            self.hajimi.react(result)
            return
        if val == "BMR":
            self.open_bmr_window()
            return

        self.display.insert(tk.END, val)
        self.hajimi.play_random()

    def open_bmr_window(self):
        win = tk.Toplevel(self.master)
        win.title("基础代谢率计算")
        win.geometry("300x300")

        tk.Label(win, text="性别 (M/F):").pack()
        gender_entry = tk.Entry(win)
        gender_entry.pack()

        tk.Label(win, text="年龄:").pack()
        age_entry = tk.Entry(win)
        age_entry.pack()

        tk.Label(win, text="身高(cm):").pack()
        height_entry = tk.Entry(win)
        height_entry.pack()

        tk.Label(win, text="体重(kg):").pack()
        weight_entry = tk.Entry(win)
        weight_entry.pack()

        result_label = tk.Label(win, text="")
        result_label.pack()

        def calc_bmr():
            gender = gender_entry.get()
            age = float(age_entry.get())
            height = float(height_entry.get())
            weight = float(weight_entry.get())
            result, msg = self.calc.calculate_bmr(gender, age, height, weight)
            result_label.config(text=msg)
            self.hajimi.react(result)

        tk.Button(win, text="计算", command=calc_bmr).pack(pady=10)
