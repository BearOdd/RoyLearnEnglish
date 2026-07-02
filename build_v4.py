import json
import random

with open('db_dump.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

def get_unit_dialogue(day_num):
    unit = (day_num - 1) // 10 + 1
    
    if unit == 1: # Greetings & Stationery
        d = [
            {'speaker': 'dad', 'en': 'Good morning, Guangtou! Time to go to school.', 'zh': '早上好，光头！该去上学了。'},
            {'speaker': 'son', 'en': 'Good morning, Dad! Where is my pencil?', 'zh': '早上好，爸爸！我的铅笔在哪儿？'},
            {'speaker': 'mom', 'en': 'Here it is. And do you have your ruler?', 'zh': '在这里。你带尺子了吗？'},
            {'speaker': 'son', 'en': 'Yes, I have a ruler. Goodbye, Mom!', 'zh': '带了，我有一把尺子。妈妈再见！'},
            {'speaker': 'daughter', 'en': 'Bye, brother!', 'zh': '哥哥再见！'}
        ]
    elif unit == 2: # Colors
        d = [
            {'speaker': 'daughter', 'en': 'Look at my new drawing!', 'zh': '看我的新画！'},
            {'speaker': 'son', 'en': 'Wow, it is very nice. I see green and blue.', 'zh': '哇，真好看。我看到了绿色和蓝色。'},
            {'speaker': 'mom', 'en': 'Show me red, Niuniu.', 'zh': '妞妞，给我指一下红色。'},
            {'speaker': 'daughter', 'en': 'OK, here it is!', 'zh': '好的，在这里！'},
            {'speaker': 'dad', 'en': 'Great job, kids.', 'zh': '孩子们做得很棒。'}
        ]
    elif unit == 3: # Body Parts
        d = [
            {'speaker': 'mom', 'en': 'Wash your face, Guangtou. Your face is dirty.', 'zh': '洗洗你的脸，光头。你的脸有点脏。'},
            {'speaker': 'son', 'en': 'OK, Mom. Look at me! This is my clean face.', 'zh': '好的，妈妈。看着我！这是我干净的脸。'},
            {'speaker': 'dad', 'en': 'Now clap your hands and stamp your foot.', 'zh': '现在拍拍手，跺跺脚。'},
            {'speaker': 'daughter', 'en': 'Hahaha! I can stamp my foot too!', 'zh': '哈哈哈！我也能跺脚！'}
        ]
    elif unit == 4: # Animals
        d = [
            {'speaker': 'son', 'en': 'Look! What is that?', 'zh': '看！那是什么？'},
            {'speaker': 'dad', 'en': 'It is a funny dog.', 'zh': '那是一只搞笑的狗。'},
            {'speaker': 'daughter', 'en': 'I like dogs. What is this?', 'zh': '我喜欢狗。这是什么？'},
            {'speaker': 'mom', 'en': 'It is a duck. Act like a duck, Guangtou!', 'zh': '这是一只鸭子。光头，学一下鸭子！'},
            {'speaker': 'son', 'en': 'Quack, quack! Hahaha!', 'zh': '嘎嘎！哈哈哈！'}
        ]
    elif unit == 5: # Food
        d = [
            {'speaker': 'son', 'en': 'Mom, I am hungry.', 'zh': '妈妈，我饿了。'},
            {'speaker': 'mom', 'en': 'Have some bread, Guangtou. Dinner is coming.', 'zh': '吃点面包吧，光头。晚饭马上就好。'},
            {'speaker': 'daughter', 'en': 'I would like some juice, please.', 'zh': '请给我来点果汁。'},
            {'speaker': 'dad', 'en': 'Here you are. Can I have some water?', 'zh': '给你。我能喝点水吗？'},
            {'speaker': 'daughter', 'en': "Sure. Let's eat!", 'zh': '当然。我们开动吧！'}
        ]
    else: # Numbers & Birthday
        d = [
            {'speaker': 'dad', 'en': 'Happy birthday, Guangtou! How old are you?', 'zh': '生日快乐，光头！你几岁了？'},
            {'speaker': 'son', 'en': 'Thank you, Dad! I am ten.', 'zh': '谢谢爸爸！我十岁了。'},
            {'speaker': 'mom', 'en': 'Look at the cake! How many candles?', 'zh': '看这个蛋糕！有几根蜡烛？'},
            {'speaker': 'daughter', 'en': "Let's count! One, two, three... ten!", 'zh': '我们来数一数！一，二，三……十！'}
        ]
    return d

for day in db:
    target_w = random.choice(day['words']) if day['words'] else None
    if target_w:
        day['quiz'] = {
            'question': f"根据中文提示，选择正确的单词：<br><br><b>{target_w['zh']}</b>",
            'options': [target_w['en']],
            'answer': 0
        }
        all_words = ['apple', 'ruler', 'pencil', 'eraser', 'red', 'green', 'blue', 'face', 'foot', 'school', 'bear', 'dog', 'duck', 'monkey', 'bread', 'juice', 'water', 'plate', 'one', 'two', 'three', 'four', 'five', 'six']
        while len(day['quiz']['options']) < 3:
            fake = random.choice(all_words)
            if fake not in day['quiz']['options']: 
                day['quiz']['options'].append(fake)
        random.shuffle(day['quiz']['options'])
        day['quiz']['answer'] = day['quiz']['options'].index(target_w['en'])
    else:
        day['quiz'] = {
            'question': "根据中文提示，选择正确的单词：<br><br><b>早上好</b>",
            'options': ["Good morning", "Good night", "Goodbye"],
            'answer': 0
        }
    day['dialogues'] = get_unit_dialogue(day['day'])

with open('db_v4.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False)
