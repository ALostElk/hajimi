import os
import random
import pygame
from PIL import Image, ImageTk

class HajimiCharacter:
    def __init__(self):
        try:
            pygame.mixer.init()
            # 设置同时播放的音频通道数
            pygame.mixer.set_num_channels(8)
        except Exception as e:
            print(f"音频系统初始化失败: {e}")
        
        self.base_path = os.path.join(os.path.dirname(__file__), "../shucai")
        self.expression_path = os.path.join(self.base_path, "东海帝王王表情包")
        
        # 加载音频文件列表，并验证文件
        self.sound_files = self.load_valid_sound_files()
        self.mute = False
        self.volume = 0.5  # 默认音量50%
        
        # 音效缓存
        self.sound_cache = {}
        self.preload_common_sounds()
        
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

    def preload_common_sounds(self):
        """预加载常用音效到内存"""
        print("正在预加载音效...")
        try:
            # 预加载数字音效
            number_sounds = {
                '0': '哈.wav',
                '1': '曼波（干脆.低.wav',
                '2': '曼波（可爱.低.wav',
                '3': '曼波↑.低.wav',
                '4': '曼波（干脆.中.wav',
                '5': '曼波（可爱.中.wav',
                '6': '曼波↑.中.wav',
                '7': '曼波（干脆.高.wav',
                '8': '曼波（可爱.高.wav',
                '9': '曼波↑.高.wav'
            }
            
            for num, filename in number_sounds.items():
                self._load_sound_to_cache(filename)
            
            # 预加载运算符音效（+、-、×、÷、.）
            operator_sounds = [
                '曼波.wav',          # + 号专属
                '曼波（干脆.wav',    # - 号专属
                '曼波（可爱.wav',    # × 号专属
                '曼波↑.wav'          # ÷ 号专属
                # 哈.wav 已经在数字0中预加载
            ]
            for filename in operator_sounds:
                self._load_sound_to_cache(filename)
            
            # 预加载成功/失败音效
            result_sounds = [
                '曼波欧耶.wav', '曼波wow.wav', '帝皇私人笑声.wav',
                '曼波duang.wav', '曼波啊米诺斯.wav', '曼波我嘞个豆.wav'
            ]
            for filename in result_sounds:
                self._load_sound_to_cache(filename)
            
            print(f"音效预加载完成！共加载 {len(self.sound_cache)} 个音效")
        except Exception as e:
            print(f"预加载音效失败: {e}")
    
    def _load_sound_to_cache(self, filename):
        """加载单个音效到缓存"""
        try:
            path = os.path.join(self.base_path, filename)
            if os.path.exists(path):
                self.sound_cache[filename] = pygame.mixer.Sound(path)
        except Exception as e:
            print(f"加载音效 {filename} 失败: {e}")

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
        """播放音效，优先使用缓存，带错误处理和音量控制"""
        if self.mute or self.volume == 0: 
            return
        try:
            # 优先使用缓存的音效
            if filename in self.sound_cache:
                sound = self.sound_cache[filename]
                sound.set_volume(self.volume)
                sound.play()
            else:
                # 缓存中没有，使用旧方法
                path = os.path.join(self.base_path, filename)
                if os.path.exists(path):
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.set_volume(self.volume)
                    pygame.mixer.music.play()
        except pygame.error as e:
            print(f"音频加载失败: {filename} - {e}")
        except Exception as e:
            print(f"播放音效时出错: {filename} - {e}")

    def play_random(self):
        """随机播放音效"""
        if self.mute or self.volume == 0: 
            return
        if not self.sound_files:
            return
        try:
            file = random.choice(self.sound_files)
            self.play_sound(file)
        except Exception as e:
            print(f"随机播放音效失败: {e}")
    
    def play_number_sound(self, number):
        """播放数字按键对应的音效"""
        if self.mute or self.volume == 0:
            return
        
        # 数字按键音效映射
        number_sounds = {
            '0': '哈.wav',
            '1': '曼波（干脆.低.wav',
            '2': '曼波（可爱.低.wav',
            '3': '曼波↑.低.wav',
            '4': '曼波（干脆.中.wav',
            '5': '曼波（可爱.中.wav',
            '6': '曼波↑.中.wav',
            '7': '曼波（干脆.高.wav',
            '8': '曼波（可爱.高.wav',
            '9': '曼波↑.高.wav'
        }
        
        sound_file = number_sounds.get(number)
        if sound_file:
            self.play_sound(sound_file)
    
    def play_operator_sound(self, operator=None):
        """播放运算符对应的音效
        
        Args:
            operator: 运算符字符，如果为None则随机播放
        """
        if self.mute or self.volume == 0:
            return
        
        # 固定运算符音效映射
        operator_sounds = {
            '+': '曼波.wav',
            '-': '曼波（干脆.wav',
            '×': '曼波（可爱.wav',
            '÷': '曼波↑.wav',
            '.': '哈.wav'
        }
        
        if operator in operator_sounds:
            # 如果是指定的运算符，播放对应的固定音效
            sound_file = operator_sounds[operator]
            self.play_sound(sound_file)
        else:
            # 其他功能按键随机播放四种音效之一
            random_sounds = ['曼波.wav', '曼波（干脆.wav', '曼波（可爱.wav', '曼波↑.wav']
            sound_file = random.choice(random_sounds)
            self.play_sound(sound_file)
    
    def play_success_sound(self):
        """播放计算成功的音效（随机）"""
        if self.mute or self.volume == 0:
            return
        
        # 成功音效
        success_sounds = ['曼波欧耶.wav', '曼波wow.wav', '帝皇私人笑声.wav']
        sound_file = random.choice(success_sounds)
        self.play_sound(sound_file)
    
    def play_error_sound(self):
        """播放计算错误的音效（随机）"""
        if self.mute or self.volume == 0:
            return
        
        # 错误音效
        error_sounds = ['曼波duang.wav', '曼波啊米诺斯.wav', '曼波我嘞个豆.wav']
        sound_file = random.choice(error_sounds)
        self.play_sound(sound_file)

    def react(self, result):
        """根据计算结果选择表情和音效"""
        # 根据结果选择表情（不受静音影响）
        if result is None:
            self.set_expression('expressionless')
            # 错误音效在calculate方法中处理
        elif result == 520:
            # 彩蛋：520
            self.set_expression('happy')
            if not self.mute:
                self.play_sound("曼波欧耶.wav")
        elif result == 2333:
            # 彩蛋：2333
            self.set_expression('satisfied')
            if not self.mute:
                self.play_sound("曼波欧耶.wav")
        elif result == 114514:
            # 彩蛋：114514
            self.set_expression('furious')
            if not self.mute:
                self.play_sound("曼波啊米诺斯.wav")
        elif result == 0:
            self.set_expression('happy')
            # 普通成功音效
            self.play_success_sound()
        elif isinstance(result, (int, float)) and result < 0:
            self.set_expression('sad')
            # 普通成功音效
            self.play_success_sound()
        elif isinstance(result, (int, float)) and abs(result) > 1e6:
            self.set_expression('surprised')
            # 普通成功音效
            self.play_success_sound()
        else:
            self.set_expression('satisfied')
            # 普通成功音效
            self.play_success_sound()

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
            'mute_off': 'happy',
            'ai_on': 'happy',
            'ai_off': 'expressionless'
        }
        expression = reactions.get(special_type, 'default')
        self.set_expression(expression)
