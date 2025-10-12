import random

class HajimiAI:
    def __init__(self):
        # 表情相关的反馈语句
        self.expressions_feedback = {
            'happy': ["哈基米：曼波！", "哈基米：开心！", "哈基米：欧耶！"],
            'satisfied': ["哈基米：满意！", "哈基米：不错！", "哈基米：嘞个豆！"],
            'surprised': ["哈基米：哈基米！哈！", "哈基米：哇哦～", "哈基米：惊呆！"],
            'angry': ["哈基米：生气！", "哈基米：哼！", "哈基米：不开心！"],
            'furious': ["哈基米：阿米诺斯！你脑子呢？", "哈基米：暴怒！", "哈基米：气死我了！"],
            'sad': ["哈基米：波曼！", "哈基米：难过...", "哈基米：不开心..."],
            'tired': ["哈基米：困倦...", "哈基米：累了...", "哈基米：想睡觉..."],
            'expressionless': ["哈基米：无语...", "哈基米：算不出来！", "哈基米：输入错误！"]
        }

    def comment(self, result, msg):
        # 处理错误情况
        if msg != "ok":
            if "除以零" in msg:
                return "哈基米：不能除以零啦！"
            elif "数值错误" in msg:
                return "哈基米：数字有问题哦～"
            elif "不完整" in msg:
                return "哈基米：表达式还没写完呢！"
            elif "不安全" in msg:
                return "哈基米：这个表达式不安全！"
            else:
                return "哈基米：阿米诺斯！输入有问题！"
        
        # 处理正常结果
        if result is None:
            return "哈基米：曼波？算不出来！"
        if result == 0:
            return "哈基米：曼波！结果是零！"
        if result < 0:
            return "哈基米：波曼！负数结果！"
        if abs(result) > 1e6:
            return "哈基米：哈基米！好大的数字！"
        
        # 正常结果
        return "哈基米：计算完成！"

    def get_expression_feedback(self, expression_type):
        """根据表情类型获取反馈语句"""
        feedbacks = self.expressions_feedback.get(expression_type, ["哈基米：曼波！"])
        return random.choice(feedbacks)

    def random_phrase(self):
        return random.choice(["哈基米～", "欧耶！", "哇哦～", "嘞个豆！", "曼波！", "开心！"])
