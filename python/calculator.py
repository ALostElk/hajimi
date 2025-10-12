import math
from engine import evaluate_expr

class Calculator:
    def __init__(self):
        self.angle_mode = True  # True=度数模式, False=弧度模式
        
    def evaluate(self, expr: str):
        """
        使用engine.py的安全表达式求值
        返回: (结果, 状态消息)
        """
        try:
            # 调用engine进行计算
            success, result_str = evaluate_expr(expr, deg=self.angle_mode)
            
            if success:
                # 计算成功
                if result_str == "":
                    # 空表达式
                    return 0, "ok"
                
                try:
                    # 将字符串结果转换为数值
                    if '.' in result_str:
                        result = float(result_str)
                    else:
                        result = int(result_str)
                    return result, "ok"
                except ValueError:
                    # 结果格式错误，直接返回字符串
                    return result_str, "ok"
            else:
                # 计算失败 - 可能是语法错误、除零等
                return None, "计算错误"
                
        except Exception as e:
            return None, f"异常: {str(e)}"
    
    def set_angle_mode(self, mode: str):
        """
        设置角度模式
        mode: 'deg' 或 'rad'
        """
        self.angle_mode = (mode == 'deg')
    
    def calculate_bmr(self, gender, age, height, weight):
        """
        计算基础代谢率 (BMR)
        gender: 'M' 男性, 'F' 女性
        age: 年龄
        height: 身高(cm)
        weight: 体重(kg)
        """
        try:
            age = float(age)
            height = float(height)
            weight = float(weight)
            
            if gender.upper() == 'M':
                # Harris-Benedict公式(男性)
                bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
            else:
                # Harris-Benedict公式(女性)
                bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)
            
            # 生成友好的消息
            if bmr < 1300:
                msg = f"哈基米：要多注意饮食哦～ BMR={bmr:.1f} kcal/天"
            elif bmr < 1700:
                msg = f"哈基米：刚刚好，健康平衡！BMR={bmr:.1f} kcal/天"
            else:
                msg = f"哈基米：曼波！BMR={bmr:.1f}，身体在躺平时都这么努力！"
            
            return bmr, msg
            
        except ValueError:
            return None, "哈基米：请输入有效的数字！"
        except Exception as e:
            return None, f"哈基米：计算出错了：{str(e)}"
