import tkinter as tk
from ui import HajimiUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("哈基米计算器")
    root.geometry("400x600")
    root.resizable(False, False)
    app = HajimiUI(root)
    root.mainloop()
