# app/config/prefs.py
import os, configparser

CFG_PATH = os.path.join(os.path.dirname(__file__), "settings.ini")

def _ensure_exists():
    if not os.path.exists(CFG_PATH):
        cfg = configparser.ConfigParser()
        cfg["ui"] = {
            "angle": "DEG",
            "mute": "off",
            "volume": "35",
            "mode": "basic",   # basic / expanded
        }
        with open(CFG_PATH, "w", encoding="utf-8") as f:
            cfg.write(f)

def _read():
    _ensure_exists()
    cfg = configparser.ConfigParser()
    cfg.read(CFG_PATH, encoding="utf-8")
    return cfg

def _write(cfg):
    with open(CFG_PATH, "w", encoding="utf-8") as f:
        cfg.write(f)

def load_angle_is_deg() -> bool:
    cfg = _read()
    return cfg.get("ui", "angle", fallback="DEG").upper() == "DEG"

def save_angle(is_deg: bool) -> None:
    cfg = _read()
    if "ui" not in cfg: cfg["ui"] = {}
    cfg["ui"]["angle"] = "DEG" if is_deg else "RAD"
    _write(cfg)

def load_mute() -> bool:
    cfg = _read()
    return cfg.get("ui", "mute", fallback="off").lower() == "on"

def save_mute(mute: bool) -> None:
    cfg = _read()
    if "ui" not in cfg: cfg["ui"] = {}
    cfg["ui"]["mute"] = "on" if mute else "off"
    _write(cfg)

def load_volume() -> int:
    cfg = _read()
    try:
        v = int(cfg.get("ui", "volume", fallback="35"))
    except Exception:
        v = 35
    return max(0, min(100, v))

def save_volume(vol: int) -> None:
    cfg = _read()
    if "ui" not in cfg: cfg["ui"] = {}
    cfg["ui"]["volume"] = str(max(0, min(100, int(vol))))
    _write(cfg)

# ------- 模式: basic / expanded -------
def load_mode() -> str:
    cfg = _read()
    mode = cfg.get("ui", "mode", fallback="basic").lower()
    return "expanded" if mode == "expanded" else "basic"

def save_mode(mode: str) -> None:
    cfg = _read()
    if "ui" not in cfg: cfg["ui"] = {}
    cfg["ui"]["mode"] = "expanded" if mode == "expanded" else "basic"
    _write(cfg)
