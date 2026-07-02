import json
import random

with open('db_v5.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

for day in db:
    target_w = day['words'][0] if len(day['words']) > 0 else None
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

with open('db_v5_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
content = re.sub(r'const DB = \[.*?\];', f"const DB = {json.dumps(db, ensure_ascii=False)};", content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Quiz restored in DB and injected into HTML!")
