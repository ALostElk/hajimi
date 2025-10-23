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
        self.api_key = "set your API key"
        
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
3. 可以包含"曼波"、"欧耶"、"我嘞个豆"、"哈基米"、"阿米诺斯"等口头禅
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
    
    def generate_bmr_report(self, gender, age, height, weight, bmr, bmi):
        """生成哈基米风格的BMR健康报告"""
        if not self.ai_enabled:
            return self._generate_fallback_bmr_report(gender, age, height, weight, bmr, bmi)
        
        try:
            gender_text = "男生" if gender == "M" else "女生"
            
            prompt = f"""
你是"东海帝皇"哈基米（曼波），一个超级可爱、调皮活泼的健康助手！你的口头禅是"曼波"、"欧耶"、"我嘞个豆"、"哈基米"等。

现在要为用户生成一份健康报告，用户信息：
- 性别：{gender_text}
- 年龄：{age}岁
- 身高：{height}cm
- 体重：{weight}kg
- BMR（基础代谢率）：{bmr}大卡/天
- BMI（身体质量指数）：{bmi}

请用哈基米超级可爱调皮的语气，生成一份详细的健康报告，要求：

1. **开场白**（30字左右）
   - 用可爱的方式打招呼
   - 必须包含"曼波"或其他口头禅
   - 要活泼有趣

2. **数据解读**（100字左右）
   - 用通俗易懂的方式解释BMR和BMI
   - 加入可爱的比喻
   - 语气要俏皮

3. **健康评估**（80字左右）
   - 评价当前身体状况
   - 用鼓励和关心的语气
   - 可以用"曼波觉得..."这样的表达

4. **个性化建议**（200字左右）
   包含：
   - 🍽️ 每日热量摄入建议（给出具体数值范围）
   - 🥗 饮食小贴士（3-4条简短建议）
   - 💪 运动建议（类型、频率、强度）
   - 😴 生活习惯建议
   - 每条建议前加emoji，语气要可爱

5. **特别提醒**（50字左右）
   - 重要的注意事项
   - 用关心但不说教的语气
   - 可以说"曼波提醒你哦～"

6. **结束语**（30字左右）
   - 鼓励的话语
   - 必须包含口头禅
   - 充满正能量

要求：
- 全文使用第二人称"你"
- 语气要非常可爱、调皮、活泼
- 大量使用emoji表情
- 每段开头可以用"曼波～"、"哈基米～"、"欧耶～"等
- 专业建议要准确，但表达要可爱
- 总字数控制在600-700字
- 使用纯文本格式，不要使用任何Markdown符号（如#、*、-、**等）
- 用空行分隔段落，用emoji和数字来标识要点
- 每个部分用可爱的表达方式标识，如"【曼波～ 数据解读】"

请直接输出报告内容，不要添加其他说明：
"""
            
            response = Generation.call(
                model="qwen-plus",
                prompt=prompt,
                temperature=0.7,
                result_format='message'
            )
            
            report = response['output']['choices'][0]['message']['content'].strip()
            return report
            
        except Exception as e:
            print(f"AI生成BMR报告失败: {e}")
            return self._generate_fallback_bmr_report(gender, age, height, weight, bmr, bmi)
    
    def _generate_fallback_bmr_report(self, gender, age, height, weight, bmr, bmi):
        """生成备用的BMR报告（AI失败时使用）"""
        gender_text = "小哥哥" if gender == "M" else "小姐姐"
        
        # BMI评估
        if bmi < 18.5:
            bmi_status = "偏瘦"
            bmi_emoji = "🌱"
            bmi_advice = "需要适当增重"
        elif 18.5 <= bmi < 24:
            bmi_status = "健康"
            bmi_emoji = "💚"
            bmi_advice = "保持现状"
        elif 24 <= bmi < 28:
            bmi_status = "偏胖"
            bmi_emoji = "⚠️"
            bmi_advice = "建议适当减重"
        else:
            bmi_status = "肥胖"
            bmi_emoji = "🚨"
            bmi_advice = "需要减重"
        
        # 计算每日推荐热量
        if gender == "M":
            daily_cal = int(bmr * 1.5)
        else:
            daily_cal = int(bmr * 1.4)
        
        report = f"""
🎀 曼波～ {gender_text}你好呀！哈基米来了！

欧耶！你的健康数据分析完成啦！让哈基米来告诉你结果吧～

━━━━━━━━━━━━━━━━━━━━━━

【📊 曼波～ 数据解读】

你的BMR是 {bmr}大卡/天，这是什么意思呢？

就是说，即使你整天躺着不动（像哈基米一样懒懒的～），你的身体也需要消耗{bmr}大卡来维持心跳、呼吸、体温等基本生命活动！这就是你身体的"最低能耗"哦！

你的BMI是 {bmi}，身体状况是：{bmi_emoji} {bmi_status}

━━━━━━━━━━━━━━━━━━━━━━

【💪 哈基米～ 健康评估】

哈基米觉得：你的身体状况{bmi_status}哦！{bmi_advice}～

以你{age}岁的年龄，这个代谢率{'挺不错的' if bmr > 1400 else '还可以'}！继续加油！曼波～

━━━━━━━━━━━━━━━━━━━━━━

【🎯 欧耶～ 个性化建议】

🍽️ 饮食建议：
   每日推荐热量：{daily_cal-200} 到 {daily_cal+200} 大卡
   🥗 多吃蔬菜水果，营养均衡最重要！
   🍖 适量蛋白质（鸡蛋、肉类、豆类）
   💧 每天喝8杯水，约2000ml哦～
   🍰 少吃高糖高油的零食（虽然很好吃，曼波也爱吃～）

💪 运动建议：
   类型：{'力量训练+有氧运动' if gender == 'M' else '有氧运动为主'}
   频率：每周3到5次，每次30到60分钟
   强度：微微出汗、心跳加快为宜
   🏃 推荐：快走、慢跑、游泳、骑车都很棒！

😴 生活习惯：
   每天睡7到9小时，规律作息
   避免熬夜，11点前睡觉最好
   保持心情愉快，像哈基米一样开心～欧耶！

━━━━━━━━━━━━━━━━━━━━━━

【⚠️ 曼波提醒你哦～】

🔸 如果要减重，不要节食！会影响代谢的！
🔸 如果要增肌，记得补充蛋白质～
🔸 有任何不适，记得看医生哦！
🔸 健康的速度是每周变化0.5到1kg

━━━━━━━━━━━━━━━━━━━━━━

【🌟 加油鸭！】

哈基米相信你一定可以的！保持健康的身体，享受美好的生活！

曼波～ 我嘞个豆！你最棒啦！💖✨

━━━━━━━━━━━━━━━━━━━━━━

报告生成时间 | {age}岁 | 身高{height}cm | 体重{weight}kg
"""
        return report
    
    def chat_with_hajimi(self, user_message, context=""):
        """与哈基米进行对话（曼波主题）"""
        if not self.ai_enabled:
            return self._generate_fallback_chat(user_message)
        
        try:
            # 构建上下文部分（避免f-string中使用反斜杠）
            context_part = ""
            if context:
                context_part = f"【之前的对话】：\n{context}\n\n"
            
            prompt = f"""
你是"东海帝皇"哈基米（曼波），一个超级可爱、调皮活泼的计算器助手！

【角色设定】
- 性格：可爱、调皮、活泼、善良、爱帮助人
- 口头禅：曼波、欧耶、我嘞个豆、哈基米、阿米诺斯（生气时）
- 特点：说话经常带"～"，喜欢用emoji，偶尔会撒娇
- 专长：数学计算、健康建议、陪伴聊天

【对话规则】
1. 不要总是以"哈基米："开头，可以直接说话
2. 语气要超级可爱，像真实的朋友聊天
3. 回答要有帮助，但不要太正经
4. 每段话必须包含至少1-2个口头禅
5. 大量使用emoji表情
6. 如果是数学问题，要给出准确答案
7. 如果不是计算问题，也要友好回应，可以引导到计算器功能
8. 长度控制在100字以内（除非是复杂解释）
9. 如果有上下文，要记住之前的对话内容，能够回答"刚才说的是什么"这类问题
10. 对于涉及前面提到的内容，要自然地提及，表现出记忆力

{context_part}【当前用户问】：{user_message}

请用哈基米的方式回复用户，记得参考之前的对话内容，直接输出回复内容：
"""
            
            response = Generation.call(
                model="qwen-plus",
                prompt=prompt,
                temperature=0.8,
                result_format='message'
            )
            
            reply = response['output']['choices'][0]['message']['content'].strip()
            
            # 如果回复太短，添加一个可爱的结尾
            if len(reply) < 20:
                endings = ["曼波～", "欧耶！", "我嘞个豆！", "哈基米～"]
                reply += " " + random.choice(endings)
            
            return reply
            
        except Exception as e:
            print(f"AI对话生成失败: {e}")
            return self._generate_fallback_chat(user_message)
    
    def _generate_fallback_chat(self, user_message):
        """生成备用对话回复（AI失败时使用）"""
        message_lower = user_message.lower()
        
        # 数学计算相关
        if any(word in message_lower for word in ['算', '计算', '等于', '多少', '+', '-', '×', '÷', '*', '/']):
            return "曼波～ 我是计算助手！你可以直接在计算器上输入算式，我会帮你算哦！试试看吧～欧耶！✨"
        
        # 问候
        if any(word in message_lower for word in ['你好', 'hello', 'hi', '嗨']):
            return "哈基米～ 你好呀！我是东海帝皇曼波！有什么可以帮你的吗？曼波～ 💖"
        
        # 健康相关
        if any(word in message_lower for word in ['bmr', '健康', '体重', '减肥', '运动']):
            return "欧耶！想了解健康数据吗？点击「BMR」按钮，我可以帮你计算基础代谢率，还会生成超详细的健康报告哦！曼波～ 💪"
        
        # 三角函数
        if any(word in message_lower for word in ['sin', 'cos', 'tan', '三角']):
            return "曼波～ 三角函数是我的强项！点击sin、cos、tan按钮，输入角度就行啦！比如sin(30)～ 我嘞个豆！📐"
        
        # 功能询问
        if any(word in message_lower for word in ['功能', '能做', '会什么', '怎么用']):
            return "哈基米～ 我可厉害啦！可以：\n💙 基础计算（加减乘除）\n💚 科学计算（sin、sqrt、ln）\n💛 健康计算（BMR、BMI）\n💜 还有音效播放器、幸运数字、历史记录！\n曼波～ 快来试试吧！✨"
        
        # 夸奖
        if any(word in message_lower for word in ['可爱', '棒', '厉害', '聪明', '喜欢']):
            return "哈基米～ 谢谢你！你也超可爱的！我嘞个豆！让我们一起加油吧～欧耶！💖✨"
        
        # 默认回复
        responses = [
            "曼波～ 有什么我可以帮你的吗？我是计算小助手哦！欧耶！✨",
            "哈基米～ 我在呢！需要算什么吗？还是想聊聊天？我嘞个豆！💙",
            "欧耶～ 虽然我不太懂你说的，但我会努力帮你的！曼波～ 要不要试试计算器功能？✨",
            "曼波曼波～ 我是计算助手哈基米！如果有数学问题尽管问我，其他问题我也会尽力回答哦！💖"
        ]
        return random.choice(responses)