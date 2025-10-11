# app/ui/main_window.py
import os, random
from typing import List

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton,
    QHBoxLayout, QLabel, QSlider, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QUrl, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QFont, QKeySequence, QShortcut

# 音频模块：环境缺失时自动降级为静音
try:
    from PyQt6.QtMultimedia import QSoundEffect
except Exception:
    QSoundEffect = None

from app.core.engine import evaluate_expr
from app.config.prefs import (
    load_angle_is_deg, save_angle,
    load_mute, save_mute,
    load_volume, save_volume,
    load_mode, save_mode,
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("趣味计算器 - 原型 (macOS)")
        self.resize(420, 650)

        # 偏好
        self.is_deg = load_angle_is_deg()
        self.is_mute = load_mute()
        self.volume = load_volume()           # 0~100
        self.mode = load_mode()               # "basic" / "expanded"

        # 状态
        self.error_state = False
        self._handling_text_edit = False

        # UI
        self._build_ui()
        self._bind_shortcuts()

        # 同步按钮/滑块文案
        self.mode_btn.setText("DEG" if self.is_deg else "RAD")
        self._update_mute_ui()
        self._update_volume_label()
        self._update_calc_mode_ui(apply=True)   # 按偏好应用当前模式

        # 文本编辑钩子
        self.display.textEdited.connect(self._on_text_edited)

        # 音效
        self._init_sounds()
        self._apply_volume()

        # 首次提示当前模式（淡入淡出）
        self._show_hint("当前模式：扩展（科学功能已开启）" if self.mode == "expanded" else "当前模式：简洁（仅四则运算）",
                        stay_ms=1400)

    # ---------- 音效 ----------
    def _assets_path(self, name: str) -> str:
        return os.path.join(os.path.dirname(__file__), "assets", name)

    def _load_sound(self, path: str):
        if QSoundEffect is None or not os.path.exists(path):
            return None
        try:
            s = QSoundEffect(self)
            s.setSource(QUrl.fromLocalFile(path))
            return s
        except Exception:
            return None

    def _init_sounds(self):
        click_files = [
            "Background.wav",
            "Foreground.wav",
            "Hardware Fail.wav",
            "Hardware Insert.wav",
            "Hardware Remove.wav",
        ]
        self.snd_clicks: List[QSoundEffect] = []
        for fn in click_files:
            s = self._load_sound(self._assets_path(fn))
            if s is not None:
                self.snd_clicks.append(s)

        self.equal_sound_name = "User Account Control.wav"
        self.snd_equal = self._load_sound(self._assets_path(self.equal_sound_name))

    def _apply_volume(self):
        vol = max(0, min(100, int(self.volume))) / 100.0
        for s in getattr(self, "snd_clicks", []):
            if s is not None:
                s.setVolume(vol)
        if getattr(self, "snd_equal", None) is not None:
            self.snd_equal.setVolume(vol)

    def _play_click_random(self):
        if self.is_mute or not self.snd_clicks:
            return
        random.choice(self.snd_clicks).play()

    def _play_equal(self):
        if self.is_mute:
            return
        if self.snd_equal is not None:
            self.snd_equal.play()
        elif self.snd_clicks:
            random.choice(self.snd_clicks).play()

    # ---------- UI ----------
    def _build_ui(self):
        root = QVBoxLayout(self); root.setSpacing(10); root.setContentsMargins(14, 12, 14, 12)

        # 顶部：行1 角度制 + 静音 + 模式切换
        top1 = QHBoxLayout()
        lbl = QLabel("角度单位："); lbl.setFont(QFont("PingFang SC", 12))
        self.mode_btn = QPushButton("DEG")
        self.mode_btn.setCheckable(True); self.mode_btn.setMinimumHeight(30)
        self.mode_btn.setFont(QFont("PingFang SC", 12))
        self.mode_btn.clicked.connect(self.toggle_angle)

        self.mute_btn = QPushButton()
        self.mute_btn.setCheckable(True); self.mute_btn.setMinimumHeight(30)
        self.mute_btn.setFont(QFont("PingFang SC", 12))
        self.mute_btn.clicked.connect(self.toggle_mute)

        # 模式切换键
        self.calc_mode_btn = QPushButton()
        self.calc_mode_btn.setMinimumHeight(30)
        self.calc_mode_btn.setFont(QFont("PingFang SC", 12))
        self.calc_mode_btn.clicked.connect(self.toggle_calc_mode)

        top1.addWidget(lbl); top1.addWidget(self.mode_btn)
        top1.addSpacing(12); top1.addWidget(QLabel("音效：")); top1.addWidget(self.mute_btn)
        top1.addSpacing(12); top1.addWidget(QLabel("模式：")); top1.addWidget(self.calc_mode_btn)
        top1.addStretch(1)
        root.addLayout(top1)

        # 顶部：行2 音量滑块
        top2 = QHBoxLayout()
        vol_lbl = QLabel("音量："); vol_lbl.setFont(QFont("PingFang SC", 12))
        self.vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.vol_slider.setRange(0, 100)
        self.vol_slider.setValue(self.volume)
        self.vol_slider.setSingleStep(1)
        self.vol_slider.setMinimumWidth(200)
        self.vol_slider.valueChanged.connect(self._on_volume_changed)
        self.vol_value_lbl = QLabel(); self.vol_value_lbl.setFont(QFont("PingFang SC", 12))
        top2.addWidget(vol_lbl); top2.addWidget(self.vol_slider, 1); top2.addWidget(self.vol_value_lbl)
        root.addLayout(top2)

        # 显示区
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setPlaceholderText("输入表达式，如 8/2 或 5*7；扩展模式可用 sqrt(9)、sin(30) 等")
        self.display.setFont(QFont("PingFang SC", 18))
        root.addWidget(self.display)
        self.display.returnPressed.connect(lambda: self.on_button("="))

        # ★ 模式提示标签（淡入淡出）
        self.hint_label = QLabel("")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.hint_label.setFont(QFont("PingFang SC", 11))
        self.hint_label.setStyleSheet("color: #888;")
        self._hint_opacity = QGraphicsOpacityEffect(self.hint_label)
        self.hint_label.setGraphicsEffect(self._hint_opacity)
        self._hint_opacity.setOpacity(0.0)  # 初始透明
        root.addWidget(self.hint_label)

        # 科学功能区（可隐藏）
        self.sci_layout = QGridLayout(); self.sci_layout.setSpacing(6); root.addLayout(self.sci_layout)
        sci_buttons = [
            ("√", 0, 0), ("1/x", 0, 1), ("x²", 0, 2), ("x^y", 0, 3),
            ("sin", 1, 0), ("cos", 1, 1), ("tan", 1, 2), ("%", 1, 3),
            ("ln", 2, 0), ("lg", 2, 1), ("π", 2, 2), ("e", 2, 3),
        ]
        self._sci_btns: list[QPushButton] = []
        for text, r, c in sci_buttons:
            btn = QPushButton(text); btn.setMinimumHeight(40); btn.setFont(QFont("PingFang SC", 13))
            self.sci_layout.addWidget(btn, r, c)
            btn.clicked.connect(lambda _, t=text: self.on_sci_button(t))
            self._sci_btns.append(btn)

        # 基础区（部分键在简洁模式隐藏）
        grid = QGridLayout(); grid.setSpacing(6); root.addLayout(grid)
        rows = [
            [("7",0), ("8",1), ("9",2), ("/",3)],
            [("4",0), ("5",1), ("6",2), ("*",3)],
            [("1",0), ("2",1), ("3",2), ("-",3)],
            [("0",0), (".",1), ("(",2), (")",3)],
            [("AC",0), ("⌫",1), ("=",2), ("+",3)],
        ]
        self._grid_buttons: dict[str, QPushButton] = {}
        for r, row in enumerate(rows):
            for text, c in row:
                btn = QPushButton(text); btn.setMinimumHeight(48); btn.setFont(QFont("PingFang SC", 14))
                grid.addWidget(btn, r, c)
                btn.clicked.connect(lambda _, t=text: self.on_button(t))
                self._grid_buttons[text] = btn

        # 简洁模式下需要隐藏的按键（可按需增减）
        self._basic_hidden_keys = {"(", ")"}  # 例如可加入 "%", "." 等
        self._apply_basic_visibility()        # 初始按偏好应用一次

    def _bind_shortcuts(self):
        QShortcut(QKeySequence("Meta+R"), self, activated=self.toggle_angle)
        QShortcut(QKeySequence("Escape"), self, activated=lambda: self.on_button("AC"))
        QShortcut(QKeySequence("Return"), self, activated=lambda: self.on_button("="))
        QShortcut(QKeySequence("Enter"), self, activated=lambda: self.on_button("="))

    # ---------- 模式切换（简洁/扩展） ----------
    def _update_calc_mode_ui(self, apply=False):
        if self.mode == "expanded":
            self.calc_mode_btn.setText("扩展")
            self.calc_mode_btn.setToolTip("点击切换到：简洁")
        else:
            self.calc_mode_btn.setText("简洁")
            self.calc_mode_btn.setToolTip("点击切换到：扩展")
        if apply:
            self._apply_basic_visibility()

    def _apply_basic_visibility(self):
        # 科学区：仅扩展模式显示
        sci_visible = (self.mode == "expanded")
        for b in self._sci_btns:
            b.setVisible(sci_visible)
        # 基础区里部分键：简洁模式隐藏
        for k, b in self._grid_buttons.items():
            if k in self._basic_hidden_keys:
                b.setVisible(self.mode == "expanded")

    def toggle_calc_mode(self):
        self.mode = "expanded" if self.mode == "basic" else "basic"
        save_mode(self.mode)
        self._update_calc_mode_ui(apply=True)
        # 弹出提示
        self._show_hint("已切换到：扩展模式（科学功能可用）" if self.mode == "expanded"
                        else "已切换到：简洁模式（仅四则运算）")

    # ---------- 角度/静音/音量 ----------
    def toggle_angle(self):
        self.is_deg = not self.is_deg
        self.mode_btn.setText("DEG" if self.is_deg else "RAD")
        save_angle(self.is_deg)
        self.display.setFocus()
        self._play_click_random()
        self._show_hint("角度单位：DEG（角度）" if self.is_deg else "角度单位：RAD（弧度）", stay_ms=900)

    def _update_mute_ui(self):
        self.mute_btn.setChecked(self.is_mute)
        self.mute_btn.setText("🔇" if self.is_mute else "🔊")
        self.mute_btn.setToolTip("静音" if self.is_mute else "开启音效")

    def toggle_mute(self):
        self.is_mute = not self.is_mute
        self._update_mute_ui()
        save_mute(self.is_mute)
        self._show_hint("已静音" if self.is_mute else "音效已开启", stay_ms=900)

    def _update_volume_label(self):
        self.vol_value_lbl.setText(f"{self.volume}%")

    def _on_volume_changed(self, v: int):
        self.volume = int(v)
        self._update_volume_label()
        self._apply_volume()
        save_volume(self.volume)

    # ---------- 提示标签动画 ----------
    def _show_hint(self, text: str, stay_ms: int = 1200):
        """显示提示文本，200ms 淡入，停留 stay_ms，400ms 淡出。"""
        self.hint_label.setText(text)
        # 如果上一次淡出还在进行，先停止
        try:
            self._fade_in_anim.stop(); self._fade_out_anim.stop()
        except Exception:
            pass

        # 淡入
        self._fade_in_anim = QPropertyAnimation(self._hint_opacity, b"opacity", self)
        self._fade_in_anim.setDuration(200)
        self._fade_in_anim.setStartValue(float(self._hint_opacity.opacity()))
        self._fade_in_anim.setEndValue(1.0)
        self._fade_in_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._fade_in_anim.start()

        # 停留后淡出
        def start_fade_out():
            self._fade_out_anim = QPropertyAnimation(self._hint_opacity, b"opacity", self)
            self._fade_out_anim.setDuration(400)
            self._fade_out_anim.setStartValue(1.0)
            self._fade_out_anim.setEndValue(0.0)
            self._fade_out_anim.setEasingCurve(QEasingCurve.Type.InCubic)
            self._fade_out_anim.start()

        QTimer.singleShot(stay_ms, start_fade_out)

    # ---------- 错误态 & 文本编辑 ----------
    def _prepare_for_input(self):
        if self.error_state or self.display.text() == "输入错误":
            self.error_state = False
            self.display.clear()

    def _on_text_edited(self, new_text: str):
        if self._handling_text_edit: return
        if self.error_state:
            self._handling_text_edit = True
            prefix = "输入错误"
            keep = new_text[len(prefix):] if new_text.startswith(prefix) else new_text
            self.display.setText(keep)
            self.display.setCursorPosition(len(keep))
            self.error_state = False
            self._handling_text_edit = False

    # ---------- 主按钮逻辑 ----------
    def on_button(self, t: str):
        if t == "AC":
            self._play_click_random()
            self.error_state = False
            self.display.clear()
            return
        if t == "⌫":
            self._play_click_random()
            self._prepare_for_input()
            self.display.backspace()
            return
        if t == "(":
            if self.mode != "expanded":
                return
            self._play_click_random()
            self._insert_pair_parentheses()
            return
        if t == "=":
            self._play_equal()
            ok, result = evaluate_expr(self.display.text(), deg=self.is_deg)
            if ok:
                self.display.setText(result); self.error_state = False
            else:
                self.display.setText("输入错误"); self.error_state = True
            self.display.setCursorPosition(len(self.display.text()))
            return

        self._prepare_for_input()
        self._play_click_random()
        if self.mode == "basic" and t in {"%",}:
            return
        self.display.insert(t)
        self.display.setFocus()

    # ---------- 科学键智能插入 ----------
    def _insert_func_call(self, name: str, args: int = 1):
        if self.mode != "expanded":
            return
        self._prepare_for_input()
        self._play_click_random()

        s = self.display.text()
        sel_start = self.display.selectionStart()
        sel_text = self.display.selectedText()
        has_sel = sel_start != -1 and len(sel_text) > 0

        if name == "pow" and args == 2:
            if has_sel:
                start, end = sel_start, sel_start + len(sel_text)
                new = s[:start] + f"pow({sel_text}, )" + s[end:]
                cursor_pos = start + len(f"pow({sel_text}, ")
            else:
                p = self.display.cursorPosition()
                new = s[:p] + "pow(, )" + s[p:]
                cursor_pos = p + len("pow(")
            self.display.setText(new); self.display.setCursorPosition(cursor_pos); return

        if has_sel:
            start, end = sel_start, sel_start + len(sel_text)
            new = s[:start] + f"{name}({sel_text})" + s[end:]
            cursor_pos = start + len(f"{name}({sel_text})")
        else:
            p = self.display.cursorPosition()
            new = s[:p] + f"{name}()" + s[p:]
            cursor_pos = p + len(name) + 1
        self.display.setText(new); self.display.setCursorPosition(cursor_pos)

    def _insert_pair_parentheses(self):
        s = self.display.text()
        sel_start = self.display.selectionStart()
        sel_text = self.display.selectedText()
        has_sel = sel_start != -1 and len(sel_text) > 0
        if has_sel:
            start, end = sel_start, sel_start + len(sel_text)
            new = s[:start] + f"({sel_text})" + s[end:]
            cursor_pos = start + len(f"({sel_text})")
        else:
            p = self.display.cursorPosition()
            new = s[:p] + "()" + s[p:]
            cursor_pos = p + 1
        self.display.setText(new); self.display.setCursorPosition(cursor_pos)

    def on_sci_button(self, t: str):
        if self.mode != "expanded":
            return
        if t == "√":
            self._insert_func_call("sqrt", 1)
        elif t == "1/x":
            self._insert_func_call("inv", 1)
        elif t == "x²":
            self._insert_func_call("pow2", 1)
        elif t == "x^y":
            self._insert_func_call("pow", 2)
        elif t in ("sin", "cos", "tan", "ln", "lg"):
            self._insert_func_call(t, 1)
        elif t == "π":
            self._prepare_for_input(); self._play_click_random(); self.display.insert("pi")
        elif t == "e":
            self._prepare_for_input(); self._play_click_random(); self.display.insert("e")
        elif t == "%":
            self._prepare_for_input(); self._play_click_random(); self.display.insert("%")
        self.display.setFocus()

    # 关闭时做一次保存（保险）
    def closeEvent(self, event):
        try:
            save_angle(self.is_deg)
            save_mute(self.is_mute)
            save_volume(self.volume)
            save_mode(self.mode)
        finally:
            super().closeEvent(event)
