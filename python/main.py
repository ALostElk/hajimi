import tkinter as tk
from ui import HajimiUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("哈基米计算器")
    root.geometry("600x1000")
    root.resizable(True, True)
    app = HajimiUI(root)
    root.mainloop()
