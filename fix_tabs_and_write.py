import json
import re

with open('db_v5_fixed.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

letter_schedule = [
    ['Aa', 'Bb', 'Cc'],
    ['Dd', 'Ee', 'Ff'],
    ['Gg', 'Hh', 'Ii'],
    ['Jj', 'Kk', 'Ll'],
    ['Mm', 'Nn', 'Oo'],
    ['Pp', 'Qq', 'Rr'],
    ['Ss', 'Tt', 'Uu'],
    ['Vv', 'Ww', 'Xx'],
    ['Yy', 'Zz'],
    ['Aa', 'Zz']
]

for day in db:
    d = day['day']
    if d <= 10:
        day['letters'] = letter_schedule[(d - 1) % 10]
    else:
        # Just use the vocabulary words for the grid!
        day['letters'] = [w['en'] for w in day.get('words', [])[:3]]

with open('db_v5_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace DB
content = re.sub(r'const DB = \[.*?\];', f"const DB = {json.dumps(db, ensure_ascii=False)};", content, flags=re.DOTALL)

# Fix Tab IDs
content = content.replace(
    '<button onclick="switchTab(\'listen\')" class="tab-btn active',
    '<button id="tab-listen" onclick="switchTab(\'listen\')" class="tab-btn active'
)
content = content.replace(
    '<button onclick="switchTab(\'speak\')" class="tab-btn',
    '<button id="tab-speak" onclick="switchTab(\'speak\')" class="tab-btn'
)
content = content.replace(
    '<button onclick="switchTab(\'write\')" class="tab-btn',
    '<button id="tab-write" onclick="switchTab(\'write\')" class="tab-btn'
)

# Replace Write Tab Logic
write_logic_old = r"else if\(tab === 'write'\) \{.*?content\.innerHTML = html;\n    \}"

write_logic_new = """else if(tab === 'write') {
        let q = currentDay.quiz;
        
        let gridHtml = '';
        if(currentDay.letters && currentDay.letters.length > 0) {
            gridHtml = `<div class="mt-4 mb-2">
                <p class="text-amber-800 text-sm font-bold mb-2">✨ 标准四线三格示范：</p>
                <div class="flex flex-col gap-3">`;
            
            currentDay.letters.forEach(letter => {
                gridHtml += `
                <div class="relative h-[48px] w-full rounded bg-white shadow-inner overflow-hidden border border-amber-100 flex items-center justify-center">
                    <div class="absolute top-[12px] w-full border-t border-red-200"></div>
                    <div class="absolute top-[24px] w-full border-t border-dashed border-blue-200"></div>
                    <div class="absolute top-[36px] w-full border-t border-red-200"></div>
                    <div class="relative z-10 text-[32px] text-slate-700 tracking-[0.2em]" style="font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif; line-height: 48px; transform: translateY(-2px);">${letter}</div>
                </div>`;
            });
            
            gridHtml += `</div></div>`;
        }

        let html = `<h3 class="font-extrabold text-lg text-slate-800 mb-4 flex items-center gap-2"><i class="fas fa-pencil-alt text-emerald-500"></i> 线下书写任务</h3>
        <div class="bg-amber-50 p-5 rounded-2xl border border-amber-200 shadow-sm mb-6 relative overflow-hidden">
            <div class="absolute right-0 top-0 opacity-10 text-6xl transform translate-x-4 -translate-y-4"><i class="fas fa-book"></i></div>
            <p class="text-amber-800 font-bold mb-3">📝 请在英语四线三格本上完成：</p>
            <ul class="list-disc pl-5 text-amber-700 text-sm font-medium space-y-1 mb-2">
                ${currentDay.day <= 10 ? '<li>将今天的字母各规范抄写 5 遍</li>' : '<li>将今天的重点单词各规范抄写 3 遍</li>'}
                <li>将今天的对话句子各抄写 1 遍</li>
            </ul>
            ${gridHtml}
        </div>
        
        <h3 class="font-extrabold text-lg text-slate-800 mb-4 flex items-center gap-2 mt-8"><i class="fas fa-gamepad text-indigo-500"></i> 随堂通关测验</h3>
        <div id="quiz-container" class="bg-white p-5 sm:p-6 rounded-2xl shadow-sm border border-slate-200 text-center">
            <div class="text-lg font-bold text-slate-700 mb-6 leading-relaxed">${q ? q.question : '复习今天的单词'}</div>
            <div class="flex flex-col gap-3">`;
            
        if(q && q.options) {
            q.options.forEach((opt, i) => {
                let isCorrect = (i === q.answer);
                html += `<button onclick="checkQuiz(this, ${isCorrect})" class="quiz-opt w-full py-3 px-4 bg-slate-50 hover:bg-indigo-50 border-2 border-slate-200 hover:border-indigo-300 rounded-xl font-bold text-slate-700 text-lg transition active:scale-95">${opt}</button>`;
            });
        }
        
        html += `</div>
            <div id="quiz-result" class="mt-4 font-bold text-lg hidden"></div>
        </div>`;
        content.innerHTML = html;
    }"""

content = re.sub(write_logic_old, write_logic_new, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Write tab upgraded with letter grid and tab selection fixed!")
