import random

class HajimiAI:
    def comment(self, result, msg):
        if msg != "ok":
            return f"哈基米：阿米诺斯！你脑子呢？（{msg}）"
        if result is None:
            return "哈基米：曼波？算不出来！"
        if result == 0:
            return "哈基米：曼波！"
        if result < 0:
            return "哈基米：波曼！"
        if abs(result) > 1e6:
            return "哈基米：哈基米！哈！"
        return f"哈基米：结果是 {round(result, 8)}"

    def random_phrase(self):
        return random.choice(["哈基米～", "欧耶！", "哇哦～", "嘞个豆！"])
