import math
import re
import json
import os
from datetime import datetime


class Calculator:
    """哈基米计算器核心计算类"""
    
    def __init__(self):
        self.angle_mode = True  # True=度数模式, False=弧度模式
        
        # 支持的数学函数
        self.functions = {
            'sin': self._sin,
            'cos': self._cos,
            'tan': self._tan,
            'sqrt': math.sqrt,
            'ln': math.log,
            'lg': math.log10,
        }
        
        # 支持的常量
        self.constants = {
            'pi': math.pi,
            'e': math.e
        }
    
    def evaluate(self, expr: str):
        """
        计算数学表达式
        返回: (结果, 状态消息)
        """
        try:
            if not expr or expr.strip() == "":
                return None, "空表达式"
            
            # 预处理表达式
            processed_expr = self._preprocess_expression(expr)
            
            # 验证表达式
            if not self._validate_expression(processed_expr):
                return None, "表达式格式错误"
            
            # 计算表达式
            result = self._evaluate_expression(processed_expr)
            
            # 检查结果有效性
            if math.isnan(result):
                return None, "结果为NaN"
            elif math.isinf(result):
                return None, "结果为无穷大"
            
            return result, "ok"
            
        except ZeroDivisionError:
            return None, "除数不能为零"
        except ValueError as e:
            return None, f"数值错误: {str(e)}"
        except Exception as e:
            return None, f"计算错误: {str(e)}"
    
    def _preprocess_expression(self, expr: str) -> str:
        """预处理表达式"""
        # 移除所有空格
        expr = expr.replace(' ', '')
        
        # 替换UI中的特殊符号为Python运算符
        expr = expr.replace('×', '*')
        expr = expr.replace('÷', '/')
        
        # 处理百分号：将数字%转换为数字/100
        expr = re.sub(r'(\d+\.?\d*)%', r'(\1/100)', expr)
        
        # 替换常量
        for const_name, const_value in self.constants.items():
            expr = expr.replace(const_name, str(const_value))
        
        return expr
    
    def _validate_expression(self, expr: str) -> bool:
        """验证表达式的基本格式"""
        try:
            # 检查括号是否匹配
            if expr.count('(') != expr.count(')'):
                return False
            
            # 检查是否有连续的运算符
            if re.search(r'[+\-*/]{2,}', expr):
                # 允许负号，如 5+-3
                if not re.search(r'[+\-*/][\-]', expr):
                    return False
            
            # 检查是否以运算符结尾（除了括号）
            if expr and expr[-1] in ['+', '-', '*', '/', '.']:
                return False
            
            return True
        except:
            return False
    
    def _evaluate_expression(self, expr: str) -> float:
        """计算表达式的值"""
        # 处理数学函数
        expr = self._replace_functions(expr)
        
        # 使用Python的eval进行计算（已经过预处理，相对安全）
        # 创建安全的命名空间
        safe_dict = {
            '__builtins__': {},
            'abs': abs,
            'min': min,
            'max': max,
            'pow': pow,
        }
        
        result = eval(expr, safe_dict)
        
        return float(result)
    
    def _replace_functions(self, expr: str) -> str:
        """替换数学函数调用"""
        # 处理每个支持的函数
        for func_name, func in self.functions.items():
            # 查找函数调用模式: func_name(...)
            pattern = rf'{func_name}\(((?:[^()]|\((?:[^()]|\([^()]*\))*\))*)\)'
            
            while re.search(pattern, expr):
                def replace_func(match):
                    arg_expr = match.group(1)
                    # 递归计算参数
                    arg_value = self._evaluate_expression(arg_expr)
                    # 调用函数
                    result = func(arg_value)
                    return str(result)
                
                expr = re.sub(pattern, replace_func, expr, count=1)
        
        return expr
    
    def _sin(self, x: float) -> float:
        """正弦函数（支持角度/弧度模式）"""
        if self.angle_mode:
            x = math.radians(x)
        return math.sin(x)
    
    def _cos(self, x: float) -> float:
        """余弦函数（支持角度/弧度模式）"""
        if self.angle_mode:
            x = math.radians(x)
        return math.cos(x)
    
    def _tan(self, x: float) -> float:
        """正切函数（支持角度/弧度模式）"""
        if self.angle_mode:
            x = math.radians(x)
        return math.tan(x)
    
    def set_angle_mode(self, mode: str):
        """
        设置角度模式
        mode: 'deg' 度数模式 或 'rad' 弧度模式
        """
        self.angle_mode = (mode.lower() == 'deg')
    
    def calculate_bmi(self, height: float, weight: float):
        """
        计算身体质量指数 (BMI - Body Mass Index)
        
        参数:
            height: 身高（厘米）
            weight: 体重（公斤）
        
        返回:
            (bmi值, 描述信息)
        """
        try:
            # BMI = 体重(kg) / 身高(m)²
            height_m = height / 100  # 转换为米
            bmi = weight / (height_m ** 2)
            bmi_rounded = round(bmi, 1)
            
            # BMI分类
            if bmi < 18.5:
                category = "偏瘦"
                advice = "哈基米：要注意营养均衡，适当增重哦～"
            elif bmi < 24:
                category = "正常"
                advice = "哈基米：体重很健康，继续保持！💪"
            elif bmi < 28:
                category = "偏胖"
                advice = "哈基米：可以适当控制饮食，多运动！🏃‍♀️"
            else:
                category = "肥胖"
                advice = "哈基米：建议咨询医生，制定健康计划！🏥"
            
            msg = f"BMI = {bmi_rounded}\n分类: {category}\n\n{advice}"
            return bmi, msg
            
        except Exception as e:
            return None, f"哈基米：BMI计算出错了：{str(e)}"

    def calculate_bmr(self, gender: str, age: float, height: float, weight: float):
        """
        计算基础代谢率 (BMR - Basal Metabolic Rate)
        使用 Harris-Benedict 公式
        
        参数:
            gender: 性别 ('M' 男性, 'F' 女性)
            age: 年龄（岁）
            height: 身高（厘米）
            weight: 体重（公斤）
        
        返回:
            (bmr值, 描述信息)
        """
        try:
            age = float(age)
            height = float(height)
            weight = float(weight)
            
            # 验证输入范围 - 更宽松的检查
            if age <= 0 or age > 120:
                return None, "哈基米：年龄数据不合理哦！\n💡 提示：年龄应在1-120岁之间"
            if height <= 0 or height > 250:
                return None, "哈基米：身高数据不合理哦！\n💡 提示：身高应在1-250cm之间"
            if weight <= 0 or weight > 300:
                return None, "哈基米：体重数据不合理哦！\n💡 提示：体重应在1-300kg之间"
            
            # 使用 Harris-Benedict 修正公式计算 BMR
            if gender.upper() == 'M':
                # 男性公式
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            elif gender.upper() == 'F':
                # 女性公式
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            else:
                return None, "哈基米：请选择正确的性别！"
            
            # 计算BMI
            bmi, bmi_msg = self.calculate_bmi(height, weight)
            
            # 生成友好的反馈消息
            bmr_rounded = round(bmr, 1)
            
            # BMR评估
            if bmr < 1200:
                bmr_advice = "哈基米：基础代谢偏低，要多注意营养哦～"
                level = "low"
            elif bmr < 1500:
                bmr_advice = "哈基米：代谢水平正常，保持健康生活方式！"
                level = "normal"
            elif bmr < 1800:
                bmr_advice = "哈基米：代谢不错，继续保持！💪"
                level = "good"
            else:
                bmr_advice = "哈基米：曼波！代谢率很高，身体躺平时都这么努力！🔥"
                level = "high"
            
            # 使用AI生成个性化健康报告
            try:
                # 尝试导入AI模块
                from AI import HajimiAI
                ai = HajimiAI()
                ai_report = ai.generate_health_report(bmr, bmi, age, gender, height, weight)
                return bmr, ai_report
            except ImportError:
                # 如果AI模块不可用，使用基础报告
                if bmi is not None:
                    msg = f"📊 健康数据报告\n\n"
                    msg += f"🔥 BMR = {bmr_rounded} kcal/天\n{bmr_advice}\n\n"
                    msg += f"⚖️ {bmi_msg}"
                else:
                    msg = f"BMR = {bmr_rounded} kcal/天\n\n{bmr_advice}"
                return bmr, msg
            except Exception as e:
                # AI生成失败时的备用方案
                print(f"AI健康报告生成失败: {e}")
                if bmi is not None:
                    msg = f"📊 健康数据报告\n\n"
                    msg += f"🔥 BMR = {bmr_rounded} kcal/天\n{bmr_advice}\n\n"
                    msg += f"⚖️ {bmi_msg}"
                else:
                    msg = f"BMR = {bmr_rounded} kcal/天\n\n{bmr_advice}"
                return bmr, msg
            
        except ValueError:
            return None, "哈基米：请输入有效的数字！"
        except Exception as e:
            return None, f"哈基米：计算出错了：{str(e)}"


# 测试代码
if __name__ == "__main__":
    calc = Calculator()
    
    # 测试基本运算
    test_cases = [
        "2+3",
        "10-5",
        "4×5",
        "20÷4",
        "2+3×4",
        "(2+3)×4",
        "sin(30)",
        "cos(60)",
        "tan(45)",
        "sqrt(16)",
        "ln(e)",
        "lg(100)",
        "pi",
        "50%",
        "sin(30)+cos(60)",
        "sqrt(16)+sqrt(9)",
        "(1+2)×(3+4)",
    ]
    
    print("=" * 50)
    print("哈基米计算器测试")
    print("=" * 50)
    
    for expr in test_cases:
        result, msg = calc.evaluate(expr)
        if result is not None:
            print(f"✓ {expr:20s} = {result}")
        else:
            print(f"✗ {expr:20s} : {msg}")
    
    print("\n" + "=" * 50)
    print("BMI 测试")
    print("=" * 50)
    
    # 测试BMI计算
    bmi, bmi_msg = calc.calculate_bmi(175, 70)
    print(f"\n身高175cm，体重70kg:")
    print(bmi_msg)
    
    bmi, bmi_msg = calc.calculate_bmi(165, 55)
    print(f"\n身高165cm，体重55kg:")
    print(bmi_msg)
    
    print("\n" + "=" * 50)
    print("AI健康报告测试")
    print("=" * 50)
    
    # 测试AI健康报告生成
    bmr, msg = calc.calculate_bmr('M', 25, 175, 70)
    print(f"\n男性，25岁，175cm，70kg:")
    print(msg)
    print("\n" + "-" * 30)
    
    bmr, msg = calc.calculate_bmr('F', 23, 165, 55)
    print(f"\n女性，23岁，165cm，55kg:")
    print(msg)
