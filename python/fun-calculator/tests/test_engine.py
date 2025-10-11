# tests/test_engine.py
# 说明：我们以“包名”方式导入引擎，所以运行测试时要在项目根目录。
from app.core.engine import evaluate_expr as ev

def ok(expr: str, deg: bool = True) -> str:
    success, out = ev(expr, deg=deg)
    assert success, f"表达式失败: {expr}"
    return out

def test_basic_arithmetic():
    assert ok("1+2*3") == "7"
    assert ok("(1+2)*(3-4)/5") == "-0.6"

def test_percent():
    assert ok("50%") == "0.5"
    assert ok("200+10%") == "200.1"

def test_scientific_deg():
    assert ok("sqrt(9)") == "3"
    assert ok("pow2(3)") == "9"
    assert ok("pow(2,8)") == "256"
    assert ok("sin(30)")[:3] == "0.5"
    assert ok("cos(60)")[:3] == "0.5"

def test_scientific_rad():
    assert ok("sin(pi/6)", deg=False)[:3] == "0.5"
    assert ok("ln(e)")[:1] == "1"
    assert ok("lg(100)") == "2"

def test_invalid_inputs():
    assert ev("sqrt(-1)")[0] is False
    assert ev("import os")[0] is False
