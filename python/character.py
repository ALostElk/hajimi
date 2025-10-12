import os
import random
import pygame
from PIL import Image, ImageTk

class HajimiCharacter:
    def __init__(self):
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"音频系统初始化失败: {e}")
        
        self.base_path = os.path.join(os.path.dirname(__file__), "../shucai")
        self.expression_path = os.path.join(self.base_path, "东海帝王王表情包")
        
        # 加载音频文件列表，并验证文件
        self.sound_files = self.load_valid_sound_files()
        self.mute = False
        
        # 表情映射
        self.expressions = {
            'default': 'moren.png',           # 默认表情
            'happy': 'kaixinye.png',          # 开心
            'satisfied': 'zan.png',           # 满意/点赞
            'surprised': 'jingkong.png',      # 惊恐/惊讶
            'angry': 'shengqi.png',           # 生气
            'furious': 'shengqibaoxiong.png', # 暴怒
            'sad': 'kubizi.png',              # 哭泣
            'tired': 'kun.png',               # 困倦
            'expressionless': 'wubiaoqing.png' # 无表情
        }
        
        # 当前表情
        self.current_expression = 'default'
        
        # 表情图片缓存
        self.expression_images = {}
        self.load_expressions()
    
    def load_valid_sound_files(self):
        """加载有效的音频文件"""
        valid_files = []
        try:
            all_files = [f for f in os.listdir(self.base_path) if f.endswith(('.wav', '.mp3'))]
            
            # 测试每个音频文件
            for filename in all_files:
                path = os.path.join(self.base_path, filename)
                try:
                    # 尝试加载文件以验证其有效性
                    pygame.mixer.music.load(path)
                    valid_files.append(filename)
                except pygame.error:
                    print(f"跳过损坏的音频文件: {filename}")
                except Exception:
                    print(f"跳过无法加载的文件: {filename}")
            
            # 如果没有有效的音频文件，添加一个空列表避免错误
            if not valid_files:
                print("警告: 没有找到有效的音频文件，音效将被禁用")
                self.mute = True
                
        except Exception as e:
            print(f"加载音频文件列表失败: {e}")
            valid_files = []
            self.mute = True
        
        return valid_files

    def load_expressions(self):
        """加载表情图片"""
        try:
            for key, filename in self.expressions.items():
                path = os.path.join(self.expression_path, filename)
                if os.path.exists(path):
                    # 加载并调整图片大小
                    img = Image.open(path)
                    img = img.resize((120, 120), Image.Resampling.LANCZOS)
                    self.expression_images[key] = ImageTk.PhotoImage(img)
                else:
                    print(f"表情文件未找到: {path}")
        except Exception as e:
            print(f"加载表情图片失败: {e}")

    def get_expression(self, key):
        """获取表情图片"""
        return self.expression_images.get(key, self.expression_images.get('default'))

    def set_expression(self, key):
        """设置当前表情"""
        if key in self.expressions:
            self.current_expression = key
            return True
        return False

    def play_sound(self, filename):
        """播放音效，带错误处理"""
        if self.mute: 
            return
        try:
            path = os.path.join(self.base_path, filename)
            if os.path.exists(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
        except pygame.error as e:
            # 音频加载失败，静默处理
            print(f"音频加载失败: {filename} - {e}")
        except Exception as e:
            print(f"播放音效时出错: {filename} - {e}")

    def play_random(self):
        """随机播放音效"""
        if self.mute: 
            return
        if not self.sound_files:
            return
        try:
            file = random.choice(self.sound_files)
            self.play_sound(file)
        except Exception as e:
            print(f"随机播放音效失败: {e}")

    def react(self, result):
        """根据计算结果选择表情和音效"""
        # 根据结果选择表情（不受静音影响）
        if result is None:
            self.set_expression('expressionless')
            if not self.mute:
                self.play_sound("曼波啊米诺斯.mp3")
        elif result == 0:
            self.set_expression('happy')
            if not self.mute:
                self.play_sound("曼波.mp3")
        elif isinstance(result, (int, float)) and result < 0:
            self.set_expression('sad')
            if not self.mute:
                self.play_sound("曼波傻笑.mp3")
        elif isinstance(result, (int, float)) and abs(result) > 1e6:
            self.set_expression('surprised')
            if not self.mute:
                self.play_sound("曼波哈基米.mp3")
        elif result == 520:
            self.set_expression('happy')
            if not self.mute:
                self.play_sound("曼波哈基米.mp3")
        elif result == 2333:
            self.set_expression('satisfied')
            if not self.mute:
                self.play_sound("曼波欧耶.mp3")
        elif result == 114514:
            self.set_expression('furious')
            if not self.mute:
                self.play_sound("曼波啊米诺斯.mp3")
        else:
            self.set_expression('satisfied')
            if not self.mute:
                self.play_random()

    def react_to_error(self, error_msg):
        """对错误消息的反应"""
        if "除以零" in error_msg:
            self.set_expression('angry')
        elif "输入错误" in error_msg:
            self.set_expression('expressionless')
        else:
            self.set_expression('sad')

    def react_to_special(self, special_type):
        """对特殊情况的反应"""
        reactions = {
            'BMR_low': 'tired',
            'BMR_normal': 'satisfied', 
            'BMR_high': 'happy',
            'mute_on': 'expressionless',
            'mute_off': 'happy'
        }
        expression = reactions.get(special_type, 'default')
        self.set_expression(expression)
