import json
import random

with open('db_dump.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

def get_word_pool(words):
    pool = []
    for w in words:
        en = w['en'].lower()
        if len(en) < 15 and not ' ' in en:
            pool.append(w)
    return pool

for day in db:
    word_pool = get_word_pool(day['words'])
    
    # 1. Generate Family Dialogues
    new_dialogues = []
    
    # Let's try to inject the day's vocabulary into the dialogue if possible
    # We will pick 1 word from the word pool and make the dialogue revolve around it
    focus_w = random.choice(word_pool) if word_pool else None
    
    if day['day'] % 3 == 1:
        new_dialogues.append({'speaker': 'mom', 'en': 'Good morning, Guangtou! Time to wake up.', 'zh': '早上好，光头！该起床啦。'})
        new_dialogues.append({'speaker': 'son', 'en': 'Good morning, Mom. I am so sleepy.', 'zh': '早上好，妈妈。我好困。'})
        new_dialogues.append({'speaker': 'daughter', 'en': 'Hurry up, brother!', 'zh': '快点，哥哥！'})
        if focus_w:
            new_dialogues.append({'speaker': 'dad', 'en': f"Don't forget your {focus_w['en']}.", 'zh': f"别忘了你的{focus_w['zh']}。"})
        else:
            new_dialogues.append({'speaker': 'dad', 'en': "Let's go to school.", 'zh': '我们去上学吧。'})
            
    elif day['day'] % 3 == 2:
        new_dialogues.append({'speaker': 'dad', 'en': 'How was school today, Guangtou?', 'zh': '光头，今天学校怎么样？'})
        new_dialogues.append({'speaker': 'son', 'en': 'It was great, Dad! I learned a lot.', 'zh': '太棒了，爸爸！我学到了很多。'})
        if focus_w:
            new_dialogues.append({'speaker': 'daughter', 'en': f"Look, I have a new {focus_w['en']}.", 'zh': f"看，我有一个新{focus_w['zh']}。"})
        else:
            new_dialogues.append({'speaker': 'daughter', 'en': 'I want some juice, please!', 'zh': '我想喝点果汁！'})
        new_dialogues.append({'speaker': 'mom', 'en': 'Are you hungry? Dinner is ready.', 'zh': '你们饿了吗？晚饭准备好了。'})
        
    else:
        new_dialogues.append({'speaker': 'son', 'en': 'Niuniu, look at this!', 'zh': '妞妞，看这个！'})
        if focus_w:
            new_dialogues.append({'speaker': 'daughter', 'en': f"Wow! Is it a {focus_w['en']}?", 'zh': f"哇！这是一个{focus_w['zh']}吗？"})
            new_dialogues.append({'speaker': 'son', 'en': 'Yes, it is.', 'zh': '是的。'})
        else:
            new_dialogues.append({'speaker': 'daughter', 'en': 'Wow! What is it?', 'zh': '哇！这是什么？'})
        new_dialogues.append({'speaker': 'dad', 'en': 'Be careful, kids.', 'zh': '小心点，孩子们。'})
        new_dialogues.append({'speaker': 'mom', 'en': 'Come here and wash your hands.', 'zh': '过来洗洗手。'})
        
    day['dialogues'] = new_dialogues
    
    # 2. Generate Quiz
    if len(word_pool) > 0:
        target_w = random.choice(word_pool)
        question = f"请选择正确的单词填空：<br><br>The ____ is very nice.<br>(这个【{target_w['zh']}】非常好。)"
        options = [target_w['en']]
        
        all_words = ['apple', 'banana', 'cat', 'dog', 'ruler', 'pencil', 'red', 'green', 'water', 'juice', 'bear', 'foot', 'face', 'bag', 'book', 'duck']
        while len(options) < 3:
            fake = random.choice(all_words)
            if fake not in options and fake != target_w['en']: 
                options.append(fake)
        random.shuffle(options)
        correct_index = options.index(target_w['en'])
        
        day['quiz'] = {
            'question': question,
            'options': options,
            'answer': correct_index
        }
    else:
        day['quiz'] = {
            'question': "请选择正确的问候语：<br><br>____ morning!<br>(早上好！)",
            'options': ["Good", "Bad", "Bye"],
            'answer': 0
        }

with open('db_new.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False)
