import math

class Calculator:
    def evaluate(self, expr: str):
        try:
            expr = expr.replace("√", "math.sqrt")
            expr = expr.replace("sin", "math.sin")
            expr = expr.replace("cos", "math.cos")
            expr = expr.replace("tan", "math.tan")
            expr = expr.replace("ln", "math.log")
            expr = expr.replace("lg", "math.log10")
            expr = expr.replace("π", "math.pi")
            expr = expr.replace("e", "math.e")

            result = eval(expr, {"math": math})
            return result, "ok"
        except ZeroDivisionError:
            return None, "除以零错误"
        except Exception:
            return None, "输入错误"

    def calculate_bmr(self, gender, age, height, weight):
        if gender.upper() == 'M':
            bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
        else:
            bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

        if bmr < 1300:
            msg = f"哈基米：要多注意饮食哦～ BMR={bmr:.1f}"
        elif bmr < 1700:
            msg = f"哈基米：刚刚好，健康平衡！ BMR={bmr:.1f}"
        else:
            msg = f"哈基米：曼波！BMR={bmr:.1f}，身体在躺平时都这么努力！"
        return bmr, msg
