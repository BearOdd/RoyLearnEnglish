import json

with open('db_dump.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

def generate_60_unique_dialogues():
    all_days = []
    
    for day in range(1, 61):
        unit = (day - 1) // 10 + 1
        d = []
        if unit == 1:
            scenarios = [
                [('dad', "Time to go to school, Guangtou!", '该去上学了，光头！'), ('son', "Where is my pencil?", '我的铅笔在哪儿？'), ('mom', "It is on the desk.", '在桌子上。')],
                [('mom', "Do you have your ruler?", '你带尺子了吗？'), ('son', "Yes, I have my ruler.", '带了，我带了尺子。'), ('daughter', "I want a ruler too!", '我也想要一把尺子！')],
                [('son', "Hello, Mom! I am home.", '你好，妈妈！我回来了。'), ('mom', "Hello, Guangtou. Wash your hands.", '你好，光头。洗洗手。'), ('daughter', "Play with me, brother!", '哥哥，跟我玩！')],
                [('dad', "Show me your bag.", '让我看看你的书包。'), ('son', "Look, my bag is big.", '看，我的书包很大。'), ('mom', "Very good.", '非常好。')],
                [('daughter', "What is your name?", '你叫什么名字？'), ('son', "My name is Guangtou.", '我的名字叫光头。'), ('dad', "Stop playing, kids.", '别玩了，孩子们。')],
            ]
        elif unit == 2:
            scenarios = [
                [('mom', "Look at this flower.", '看这朵花。'), ('son', "Wow, it is red!", '哇，它是红色的！'), ('daughter', "I like red.", '我喜欢红色。')],
                [('son', "My pencil is blue.", '我的铅笔是蓝色的。'), ('daughter', "My ruler is green.", '我的尺子是绿色的。'), ('dad', "They are beautiful.", '它们很漂亮。')],
                [('dad', "What color is the sky?", '天空是什么颜色的？'), ('son', "The sky is blue.", '天空是蓝色的。'), ('mom', "Correct!", '正确！')],
                [('daughter', "Look at my green bag.", '看我的绿色书包。'), ('son', "It is nice.", '很好看。')],
                [('mom', "The grass is green.", '草是绿色的。'), ('dad', "The sun is red.", '太阳是红色的。'), ('son', "I love nature.", '我爱大自然。')],
            ]
        elif unit == 3:
            scenarios = [
                [('mom', "Wash your face, Guangtou.", '洗洗你的脸，光头。'), ('son', "My face is clean now.", '我的脸现在很干净了。'), ('daughter', "Look at my face!", '看我的脸！')],
                [('dad', "Stamp your foot.", '跺跺你的脚。'), ('son', "Like this, Dad?", '像这样吗，爸爸？'), ('mom', "Be gentle!", '轻一点！')],
                [('daughter', "Touch your nose.", '摸摸你的鼻子。'), ('son', "Haha, I touched my nose.", '哈哈，我摸了我的鼻子。'), ('dad', "Good game.", '好游戏。')],
                [('mom', "Open your mouth.", '张开你的嘴巴。'), ('son', "Ahhh.", '啊——'), ('dad', "Your teeth are clean.", '你的牙齿很干净。')],
                [('son', "Clap your hands!", '拍拍你的手！'), ('daughter', "Clap, clap, clap!", '拍拍拍！'), ('mom', "You are so happy.", '你们真开心。')],
            ]
        elif unit == 4:
            scenarios = [
                [('son', "Look at the dog.", '看那只狗。'), ('daughter', "The dog is running.", '狗在跑。'), ('dad', "It is very fast.", '它非常快。')],
                [('mom', "There is a duck.", '那有一只鸭子。'), ('son', "Quack, quack!", '嘎嘎！'), ('daughter', "Hahaha!", '哈哈哈！')],
                [('dad', "Look at the big bear.", '看那只大熊。'), ('son', "Wow, it is so big!", '哇，它好大！'), ('mom', "Don't go near.", '不要靠近。')],
                [('daughter', "Act like a monkey.", '学猴子。'), ('son', "Ooh ooh aah aah!", '（猴子叫）'), ('dad', "Funny monkey!", '搞笑的猴子！')],
                [('mom', "The cat is sleeping.", '猫在睡觉。'), ('son', "Shh... Be quiet.", '嘘……安静点。')],
            ]
        elif unit == 5:
            scenarios = [
                [('son', "I am hungry, Mom.", '我饿了，妈妈。'), ('mom', "Have some bread.", '吃点面包吧。'), ('dad', "I want some too.", '我也想要一点。')],
                [('daughter', "Can I have some juice?", '我能喝点果汁吗？'), ('mom', "Here you are.", '给你。'), ('daughter', "Thank you.", '谢谢。')],
                [('dad', "Drink some water, Guangtou.", '喝点水，光头。'), ('son', "OK, Dad.", '好的，爸爸。'), ('mom', "Water is good for you.", '水对你有好处。')],
                [('mom', "Pass me a plate.", '递给我一个盘子。'), ('son', "Here is the plate.", '盘子在这里。'), ('dad', "Dinner is ready!", '晚饭做好了！')],
                [('son', "I like milk.", '我喜欢牛奶。'), ('daughter', "I like juice.", '我喜欢果汁。'), ('dad', "We all like drinking.", '我们都喜欢喝饮料。')],
            ]
        else:
            scenarios = [
                [('dad', "How old are you, Guangtou?", '你几岁了，光头？'), ('son', "I am ten.", '我十岁了。'), ('mom', "Happy birthday!", '生日快乐！')],
                [('mom', "Let's count the candles.", '我们来数数蜡烛。'), ('daughter', "One, two, three...", '一，二，三……'), ('son', "Ten!", '十！')],
                [('son', "I have five pencils.", '我有五支铅笔。'), ('daughter', "I have six rulers.", '我有六把尺子。'), ('dad', "You have so many.", '你们有这么多。')],
                [('mom', "How many plates?", '需要几个盘子？'), ('dad', "Four plates, please.", '请拿四个盘子。'), ('son', "I will get them.", '我去拿。')],
                [('daughter', "Let's count to ten.", '我们数到十。'), ('son', "One, two, three, four, five...", '一，二，三，四，五……'), ('dad', "Six, seven, eight, nine, ten!", '六，七，八，九，十！')],
            ]
        
        scenario = scenarios[day % 5]
        for role, en, zh in scenario:
            d.append({'speaker': role, 'en': en, 'zh': zh})
        all_days.append(d)
    return all_days

all_dialogues = generate_60_unique_dialogues()

for i, day in enumerate(db):
    day['dialogues'] = all_dialogues[i]

with open('db_v5.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False)
