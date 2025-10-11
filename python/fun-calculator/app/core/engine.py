# app/core/engine.py
from decimal import Decimal, getcontext, InvalidOperation, DivisionByZero
import math, re

getcontext().prec = 28
_Q8 = Decimal("0.00000001")

# 仅允许这些字符（防注入）
_ALLOWED = re.compile(r"^[0-9+\-*/().,%\sA-Za-z]+$")
# 把 12% → (12/100)
_PERCENT = re.compile(r"(?P<num>\d+(\.\d+)?)%")
# 只有当数字前面不是字母时才替换为 Decimal("…")（避免 pow2 的“2”被替换）
_NUMBER = re.compile(r"(?<![A-Za-z])\d+(\.\d+)?")

def _normalize(expr: str) -> str:
    # 把常见全角/特殊符号统一
    return (
        (expr or "")
        .replace("√(", "sqrt(")
        .replace("×", "*").replace("÷", "/")
        .replace("（", "(").replace("）", ")")
        .replace("，", ",").replace("％", "%")
        .replace("\u3000", " ")
    )

def _format_decimal(x: Decimal) -> str:
    # 先量化到 8 位小数，防止无限小数；再用固定小数格式，不使用科学计数法
    q = x.quantize(_Q8)
    s = format(q, "f")            # 固定小数格式，比如 10 -> "10", 1.23000000 -> "1.23000000"
    if "." in s:
        s = s.rstrip("0").rstrip(".")  # 只在有小数点时，去掉小数点后的 0 和可能多余的小数点
    if s == "-0":                 # 处理 -0
        s = "0"
    return s


def evaluate_expr(expr: str, deg: bool = True) -> tuple[bool, str]:
    """
    支持：
      - 四则与括号
      - 百分号：n% -> (n/100)
      - 函数：sqrt(x), inv(x), pow2(x), pow(a,b)
      - 三角：sin/cos/tan（deg=True 角度；False 弧度）
      - 对数：ln(x), lg(x)
      - 常量：pi, e
    """
    try:
        expr = _normalize(expr).strip()
        if not expr:
            return True, ""

        if not _ALLOWED.match(expr):
            return False, ""

        expr = _PERCENT.sub(lambda m: f'({m.group("num")}/100)', expr)

        def _num_repl(m: re.Match): return f'Decimal("{m.group(0)}")'
        dec_expr = _NUMBER.sub(_num_repl, expr)

        def _to_dec(x: float) -> Decimal: return Decimal(str(x))

        # 基本函数
        def sqrt(x: Decimal) -> Decimal:
            if x < 0: raise InvalidOperation
            return x.sqrt()
        def inv(x: Decimal) -> Decimal:
            if x == 0: raise DivisionByZero
            return Decimal(1) / x
        def pow2(x: Decimal) -> Decimal: return x * x
        def pow(a: Decimal, b: Decimal) -> Decimal:
            return _to_dec(float(a) ** float(b))

        # 三角与对数
        def _rad(x: Decimal) -> float:
            return math.radians(float(x)) if deg else float(x)
        def sin(x: Decimal) -> Decimal: return _to_dec(math.sin(_rad(x)))
        def cos(x: Decimal) -> Decimal: return _to_dec(math.cos(_rad(x)))
        def tan(x: Decimal) -> Decimal: return _to_dec(math.tan(_rad(x)))
        def ln(x: Decimal) -> Decimal:
            if x <= 0: raise InvalidOperation
            return _to_dec(math.log(float(x)))
        def lg(x: Decimal) -> Decimal:
            if x <= 0: raise InvalidOperation
            return _to_dec(math.log10(float(x)))

        pi = Decimal(str(math.pi))
        e = Decimal(str(math.e))

        result = eval(
            dec_expr,
            {"__builtins__": {}},
            {
                "Decimal": Decimal,
                "sqrt": sqrt, "inv": inv, "pow2": pow2, "pow": pow,
                "sin": sin, "cos": cos, "tan": tan,
                "ln": ln, "lg": lg,
                "pi": pi, "e": e,
            },
        )
        return True, _format_decimal(result)
    except (InvalidOperation, DivisionByZero, SyntaxError, ZeroDivisionError, Exception):
        return False, ""
