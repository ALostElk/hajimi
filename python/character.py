import os
import random
import pygame

class HajimiCharacter:
    def __init__(self):
        pygame.mixer.init()
        self.base_path = os.path.join(os.path.dirname(__file__), "../shucai")
        self.sound_files = [f for f in os.listdir(self.base_path) if f.endswith(('.wav', '.mp3'))]
        self.mute = False

    def play_sound(self, filename):
        if self.mute: return
        path = os.path.join(self.base_path, filename)
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()

    def play_random(self):
        if self.mute: return
        file = random.choice(self.sound_files)
        self.play_sound(file)

    def react(self, result):
        if self.mute: return
        if result is None:
            self.play_sound("曼波啊米诺斯.mp3")
        elif result == 0:
            self.play_sound("曼波.mp3")
        elif result < 0:
            self.play_sound("曼波傻笑.mp3")
        elif abs(result) > 1e6:
            self.play_sound("曼波哈基米.mp3")
        else:
            self.play_random()
