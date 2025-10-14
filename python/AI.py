import random
import json
import re

# 尝试导入dashscope，如果失败则禁用AI功能
try:
    import dashscope
    from dashscope import Generation
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False
    print("警告: dashscope模块未安装，AI功能将被禁用")

class HajimiAI:
    def __init__(self):
        # 设置通义千问API密钥
        self.api_key = "sk-cbf4265d902f4721ab7d08d7fedad32f"
        
        # 检查dashscope是否可用
        if DASHSCOPE_AVAILABLE:
            dashscope.api_key = self.api_key
        else:
            print("AI功能已禁用：缺少dashscope依赖")
        
        # 表情相关的反馈语句（作为备用）
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
        
        # 是否启用AI生成（只有在dashscope可用时才启用）
        self.ai_enabled = DASHSCOPE_AVAILABLE

    def safe_load_json(self, text):
        """安全解析 JSON，尝试提取首个大括号内 JSON"""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re.S)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass
            raise

    def generate_dynamic_comment(self, result, msg, expression_type="default"):
        """使用通义千问生成动态的哈基米评论"""
        if not self.ai_enabled:
            return self.comment(result, msg)
        
        try:
            # 构建提示词
            prompt = self._build_comment_prompt(result, msg, expression_type)
            
            # 调用通义千问API
            response = Generation.call(
                model="qwen-plus",
                prompt=prompt,
                temperature=0.7,
                result_format='message'
            )
            
            # 提取生成的评论
            ai_comment = response['output']['choices'][0]['message']['content'].strip()
            
            # 确保评论以"哈基米："开头
            if not ai_comment.startswith("哈基米："):
                ai_comment = f"哈基米：{ai_comment}"
            
            return ai_comment
            
        except Exception as e:
            # 如果AI生成失败，回退到原有逻辑
            print(f"AI生成失败，使用备用逻辑: {e}")
            return self.comment(result, msg)

    def _build_comment_prompt(self, result, msg, expression_type):
        """构建评论生成的提示词"""
        # 根据表情类型确定语气
        mood_map = {
            'happy': "开心活泼",
            'satisfied': "满意得意",
            'surprised': "惊讶好奇",
            'angry': "生气不满",
            'furious': "暴怒愤怒",
            'sad': "难过沮丧",
            'tired': "困倦疲惫",
            'expressionless': "无语无奈",
            'default': "正常"
        }
        
        mood = mood_map.get(expression_type, "正常")
        
        # 构建上下文信息
        context = ""
        if result is not None:
            context = f"计算结果: {result}"
        else:
            context = f"错误信息: {msg}"
        
        prompt = f"""
你是一个名为"哈基米"的可爱计算器助手，性格活泼可爱，喜欢说"曼波"、"欧耶"、"嘞个豆"等口头禅。

当前情况：
- 表情状态: {mood}
- {context}

请生成一句符合哈基米性格的评论，要求：
1. 以"哈基米："开头
2. 语气要符合{mood}的状态
3. 可以包含"曼波"、"欧耶"、"我嘞个豆"、"哈基米"等口头禅
4. 长度控制在20字以内
5. 要生动有趣，符合可爱助手的形象

请直接输出评论内容，不要添加其他说明：
"""
        return prompt

    def generate_expression_feedback(self, expression_type, context=""):
        """为特定表情生成动态反馈"""
        if not self.ai_enabled:
            return self.get_expression_feedback(expression_type)
        
        try:
            prompt = f"""
你是哈基米，一个可爱的计算器助手。当前表情状态是：{expression_type}

上下文：{context}

请生成一句符合这个表情的哈基米式评论，要求：
1. 以"哈基米："开头
2. 体现{expression_type}的情绪
3. 可以包含"曼波"、"欧耶"、"嘞个豆"等口头禅
4. 长度控制在15字以内

请直接输出评论：
"""
            
            response = Generation.call(
                model="qwen-plus",
                prompt=prompt,
                temperature=0.8,
                result_format='message'
            )
            
            ai_feedback = response['output']['choices'][0]['message']['content'].strip()
            
            if not ai_feedback.startswith("哈基米："):
                ai_feedback = f"哈基米：{ai_feedback}"
            
            return ai_feedback
            
        except Exception as e:
            print(f"AI生成表情反馈失败: {e}")
            return self.get_expression_feedback(expression_type)

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

    def toggle_ai(self):
        """切换AI生成开关"""
        self.ai_enabled = not self.ai_enabled
        status = "启用" if self.ai_enabled else "禁用"
        return f"哈基米：AI生成已{status}！"

    def set_ai_enabled(self, enabled):
        """设置AI生成开关"""
        self.ai_enabled = enabled
        status = "启用" if enabled else "禁用"
        return f"哈基米：AI生成已{status}！"

    def get_ai_status(self):
        """获取AI生成状态"""
        return f"哈基米：AI生成{'已启用' if self.ai_enabled else '已禁用'}！"

    def generate_special_comment(self, special_type, context=""):
        """为特殊事件生成动态评论"""
        if not self.ai_enabled:
            return self.get_expression_feedback('default')
        
        try:
            prompt = f"""
你是哈基米，一个可爱的计算器助手。当前发生了特殊事件：{special_type}

上下文：{context}

请生成一句符合这个特殊事件的哈基米式评论，要求：
1. 以"哈基米："开头
2. 体现对{special_type}事件的反应
3. 可以包含"曼波"、"欧耶"、"嘞个豆"等口头禅
4. 长度控制在20字以内
5. 要生动有趣，符合可爱助手的形象

请直接输出评论：
"""
            
            response = Generation.call(
                model="qwen-plus",
                prompt=prompt,
                temperature=0.8,
                result_format='message'
            )
            
            ai_comment = response['output']['choices'][0]['message']['content'].strip()
            
            if not ai_comment.startswith("哈基米："):
                ai_comment = f"哈基米：{ai_comment}"
            
            return ai_comment
            
        except Exception as e:
            print(f"AI生成特殊评论失败: {e}")
            return self.get_expression_feedback('default')
