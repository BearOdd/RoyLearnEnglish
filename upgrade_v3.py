import re
import json
import shutil

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

with open('db_new.json', 'r', encoding='utf-8') as f:
    db_new_str = f.read()

# 1. Replace DB
content = re.sub(r'const DB = \[.*?\];', f'const DB = {db_new_str};', content, flags=re.DOTALL)

# 2. Update Nav Bar (Remove Read)
content = content.replace(
    '<button onclick="switchTab(\'read\')" id="tab-read" class="flex flex-col items-center p-2 text-slate-400 hover:text-indigo-600 transition"><i class="fas fa-book-open text-xl mb-1"></i><span class="text-xs font-bold">读</span></button>',
    ''
)

# 3. Inject new Voice System and Speaker Config
voice_system = """
let voiceCache = { dad: null, mom: null, son: null, daughter: null, inited: false };

function initVoices() {
    if(voiceCache.inited) return;
    let voices = window.speechSynthesis.getVoices().filter(v => v.lang.startsWith('en'));
    if(voices.length === 0) return;
    
    let males = voices.filter(v => v.name.toLowerCase().match(/male|boy|daniel|david|mark|arthur/));
    let females = voices.filter(v => v.name.toLowerCase().match(/female|girl|samantha|victoria|karen|moira/));
    
    voiceCache.dad = males[0] || voices[0];
    voiceCache.mom = females[0] || voices[voices.length - 1];
    voiceCache.son = males[1] || males[0] || voices[0];
    voiceCache.daughter = females[1] || females[0] || voices[voices.length - 1];
    
    voiceCache.inited = true;
}
if ('speechSynthesis' in window) {
    window.speechSynthesis.onvoiceschanged = initVoices;
}

function getSpeakerConfig(role) {
    switch(role) {
        case 'dad': return { name: '爸爸(罗威)', bg: 'bg-blue-50', border: 'border-blue-200', seed: 'Felix', voiceType: 'dad', isLeft: true, iconColor: 'text-blue-400', textColor: 'text-slate-800' };
        case 'mom': return { name: '妈妈(熊单)', bg: 'bg-pink-50', border: 'border-pink-200', seed: 'Jocelyn', voiceType: 'mom', isLeft: false, iconColor: 'text-pink-400', textColor: 'text-slate-800' };
        case 'son': return { name: '儿子(光头)', bg: 'bg-green-50', border: 'border-green-200', seed: 'Leo', voiceType: 'son', isLeft: false, iconColor: 'text-green-400', textColor: 'text-slate-800' };
        case 'daughter': return { name: '女儿(妞妞)', bg: 'bg-yellow-50', border: 'border-yellow-200', seed: 'Lily', voiceType: 'daughter', isLeft: true, iconColor: 'text-yellow-400', textColor: 'text-slate-800' };
        default: return { name: 'Robot', bg: 'bg-indigo-50', border: 'border-indigo-200', seed: 'bot', voiceType: 'mom', isLeft: true, iconColor: 'text-indigo-400', textColor: 'text-slate-800' };
    }
}

function speakWithGender(text, voiceType, onComplete) {
    initVoices();
    if ('speechSynthesis' in window) {
        let utterance = new SpeechSynthesisUtterance(text);
        utterance.voice = voiceCache[voiceType];
        utterance.rate = 0.85;
        
        // Use pitch to distinguish kids if they share the same voice engine
        if (voiceType === 'son' && voiceCache.son === voiceCache.dad) utterance.pitch = 1.4;
        else if (voiceType === 'daughter' && voiceCache.daughter === voiceCache.mom) utterance.pitch = 1.4;
        else if (voiceType === 'dad') utterance.pitch = 0.8;
        else if (voiceType === 'mom') utterance.pitch = 1.1;
        
        utterance.onend = onComplete;
        utterance.onerror = () => playYoudaoFallback(text, (voiceType==='mom'||voiceType==='daughter'), onComplete);
        window.speechSynthesis.speak(utterance);
    } else {
        playYoudaoFallback(text, (voiceType==='mom'||voiceType==='daughter'), onComplete);
    }
}

function playYoudaoFallback(text, isFemale, onComplete) {
    let type = isFemale ? 1 : 2;
    currentAudio = new Audio(`https://dict.youdao.com/dictvoice?type=${type}&audio=` + encodeURIComponent(text));
    currentAudio.onended = onComplete;
    currentAudio.play().catch(e => {
        console.error("Youdao fallback failed: ", e);
        onComplete();
    });
}
"""

# Replace old voice logic
content = re.sub(r'let voiceCache = \{.*?(?=function playAllDialogues\(\) \{)', voice_system, content, flags=re.DOTALL)

# Update `playNext` in `playAllDialogues`
content = content.replace('let isLeft = (index % 2 === 0);', "let isLeft = false; let voiceType = dialogues[index].speaker || 'mom';")
content = content.replace('speakWithGender(text, isLeft, onComplete);', 'speakWithGender(text, voiceType, onComplete);')

# Update `playAudio`
content = content.replace('function playAudio(text, btnElement, isLeft = true) {', 'function playAudio(text, btnElement, voiceType = "mom") {')

# 4. Refactor switchTab
# Extract the whole switchTab body to replace it
pattern_switchTab = re.compile(r"function switchTab\(tab\) \{.*?document\.getElementById\('tab-' \+ tab\)\.classList\.add\('text-indigo-600', 'scale-110'\);\n\}", re.DOTALL)

new_switchTab = """function switchTab(tab) {
    ['listen', 'speak', 'write'].forEach(t => {
        let btn = document.getElementById('tab-' + t);
        if(btn) btn.classList.remove('text-indigo-600', 'scale-110');
    });
    
    let content = document.getElementById('contentArea');
    content.innerHTML = '';
    
    if(tab === 'listen') {
        let html = `<div class="flex justify-between items-end mb-6">
            <div>
                <h2 class="text-3xl font-extrabold text-slate-800 drop-shadow-sm">Day ${currentDay.day}</h2>
                <p class="text-sm text-indigo-500 font-bold mt-1 tracking-wider uppercase">Family Dialogue</p>
            </div>
            <button id="playAllBtn" onclick="playAllDialogues()" class="bg-indigo-600 text-white px-4 py-2 rounded-full font-bold shadow-md hover:bg-indigo-700 active:scale-95 transition text-sm flex items-center gap-2">
                <i class="fas fa-play"></i> 播放全部
            </button>
        </div><div class="flex flex-col gap-6 pb-20">`;
        
        currentDay.dialogues.forEach((d, index) => {
            let conf = getSpeakerConfig(d.speaker);
            let flexDir = conf.isLeft ? 'flex-row' : 'flex-row-reverse';
            
            html += `<div class="flex ${flexDir} items-end gap-2 sm:gap-3 w-full" style="animation: fadeIn 0.3s ease-out ${index * 0.1}s both;">
                <div class="relative group cursor-pointer flex-shrink-0 text-center" onclick="this.querySelector('img').classList.toggle('rotate-12');">
                    <img src="https://api.dicebear.com/9.x/avataaars/svg?seed=${conf.seed}&backgroundColor=${conf.bg.replace('bg-','')}" class="w-10 h-10 sm:w-12 sm:h-12 rounded-full shadow-sm bg-white border-2 border-white relative z-10 transition duration-300">
                    <div class="text-[10px] text-slate-400 mt-1 font-bold whitespace-nowrap">${conf.name}</div>
                </div>
                
                <div class="max-w-[75%] p-3 sm:p-4 shadow-sm rounded-2xl ${conf.border} ${conf.bg} border active:scale-[0.98] transition cursor-pointer relative group flex flex-col justify-center" onclick="playAudio('${d.en.replace(/'/g, "\\\\'")}', this.querySelector('i.fa-volume-up'), '${conf.voiceType}')">
                    <div class="flex items-start justify-between gap-3">
                        <div class="text-[15px] sm:text-base font-bold ${conf.textColor} leading-snug font-sans">${d.en}</div>
                        <i id="dialogue-btn-${index}" class="fas fa-volume-up ${conf.iconColor} opacity-50 group-hover:opacity-100 transition text-sm mt-1 flex-shrink-0"></i>
                    </div>
                    
                    ${d.zh ? `<div class="translation-block hidden mt-2 pt-2 border-t border-slate-200 border-opacity-50">
                        <div class="text-[12px] sm:text-sm text-slate-500">${d.zh}</div>
                    </div>` : ''}
                    
                    ${d.zh ? `<div class="mt-2 text-right">
                        <span class="inline-block text-[10px] text-slate-400 bg-white bg-opacity-50 rounded px-2 py-0.5 opacity-80 hover:opacity-100 transition" onclick="event.stopPropagation(); this.parentElement.previousElementSibling.classList.toggle('hidden')"><i class="fas fa-language"></i> 译</span>
                    </div>` : ''}
                </div>
            </div>`;
        });
        html += '</div>';
        content.innerHTML = html;
    }
    else if(tab === 'speak') {
        let html = `<div class="flex justify-between items-end mb-6">
            <div>
                <h2 class="text-2xl font-extrabold text-slate-800 drop-shadow-sm">角色扮演</h2>
                <p class="text-sm text-rose-500 font-bold mt-1 tracking-wider uppercase">Dubbing Practice</p>
            </div>
            <button onclick="playAllDialogues()" class="bg-rose-500 text-white px-4 py-2 rounded-full font-bold shadow-md hover:bg-rose-600 active:scale-95 transition text-sm flex items-center gap-2">
                <i class="fas fa-play"></i> 示范朗读
            </button>
        </div><div class="flex flex-col gap-6 pb-20">`;
        
        currentDay.dialogues.forEach((d, index) => {
            let conf = getSpeakerConfig(d.speaker);
            let audioId = `Day${currentDay.day}_Speak_${index}`;
            let flexDir = conf.isLeft ? 'flex-row' : 'flex-row-reverse';
            
            html += `<div class="flex flex-col w-full" style="animation: fadeIn 0.3s ease-out ${index * 0.1}s both;">
                <div class="flex ${flexDir} items-end gap-2 sm:gap-3 w-full mb-2">
                    <div class="relative group flex-shrink-0 text-center">
                        <img src="https://api.dicebear.com/9.x/avataaars/svg?seed=${conf.seed}&backgroundColor=${conf.bg.replace('bg-','')}" class="w-10 h-10 sm:w-12 sm:h-12 rounded-full shadow-sm bg-white border-2 border-white relative z-10 transition duration-300 opacity-80 grayscale">
                    </div>
                    <div class="max-w-[75%] p-3 shadow-sm rounded-2xl ${conf.border} bg-white border relative">
                        <div class="text-[15px] sm:text-base font-bold text-slate-800 leading-snug font-sans">${d.en}</div>
                        <div class="text-[12px] sm:text-sm text-slate-400 mt-1">${d.zh}</div>
                    </div>
                </div>
                
                <div class="flex ${conf.isLeft ? 'justify-start pl-14' : 'justify-end pr-14'} gap-2" id="speak-actions-${audioId}">
                    <button onclick="playAudio('${d.en.replace(/'/g, "\\\\'")}', this.querySelector('i'), '${conf.voiceType}')" class="bg-indigo-50 text-indigo-600 font-bold py-2 px-4 rounded-xl active:scale-95 transition text-sm"><i class="fas fa-volume-up mr-1"></i>原音</button>
                    <button id="record-btn-${audioId}" onclick="toggleRecording(this, '${audioId}')" class="bg-rose-50 border border-rose-100 text-rose-600 font-bold py-2 px-4 rounded-xl active:scale-95 transition text-sm"><i class="fas fa-microphone mr-1"></i>录制 (配音)</button>
                </div>
            </div>`;
            
            loadAudioFromDB(audioId).then(blob => {
                if(blob) {
                    let btn = document.getElementById(`record-btn-${audioId}`);
                    if(btn) {
                        let url = URL.createObjectURL(blob);
                        renderSavedAudioBtn(btn, url, audioId);
                    }
                }
            });
        });
        html += '</div>';
        content.innerHTML = html;
    }
    else if(tab === 'write') {
        let q = currentDay.quiz;
        let html = `<h3 class="font-extrabold text-lg text-slate-800 mb-4 flex items-center gap-2"><i class="fas fa-pencil-alt text-emerald-500"></i> 线下书写任务</h3>
        <div class="bg-amber-50 p-5 rounded-2xl border border-amber-200 shadow-sm mb-6 relative overflow-hidden">
            <div class="absolute right-0 top-0 opacity-10 text-6xl transform translate-x-4 -translate-y-4"><i class="fas fa-book"></i></div>
            <p class="text-amber-800 font-bold mb-3">📝 请在英语四线三格本上完成：</p>
            <ul class="list-disc pl-5 text-amber-700 text-sm font-medium space-y-1">
                <li>将今天的重点单词各抄写 3 遍</li>
                <li>将今天的对话句子各抄写 1 遍</li>
            </ul>
        </div>
        
        <h3 class="font-extrabold text-lg text-slate-800 mb-4 flex items-center gap-2 mt-8"><i class="fas fa-gamepad text-indigo-500"></i> 随堂通关测验</h3>
        <div id="quiz-container" class="bg-white p-5 sm:p-6 rounded-2xl shadow-sm border border-slate-200 text-center">
            <div class="text-lg font-bold text-slate-700 mb-6 leading-relaxed">${q.question}</div>
            <div class="flex flex-col gap-3">`;
            
        q.options.forEach((opt, i) => {
            let isCorrect = (i === q.answer);
            html += `<button onclick="checkQuiz(this, ${isCorrect})" class="quiz-opt w-full py-3 px-4 bg-slate-50 hover:bg-indigo-50 border-2 border-slate-200 hover:border-indigo-300 rounded-xl font-bold text-slate-700 text-lg transition active:scale-95">${opt}</button>`;
        });
        
        html += `</div>
            <div id="quiz-result" class="mt-4 font-bold text-lg hidden"></div>
        </div>`;
        content.innerHTML = html;
    }
    
    let activeBtn = document.getElementById('tab-' + tab);
    if(activeBtn) activeBtn.classList.add('text-indigo-600', 'scale-110');
}

function checkQuiz(btn, isCorrect) {
    let container = document.getElementById('quiz-container');
    let opts = document.querySelectorAll('.quiz-opt');
    let res = document.getElementById('quiz-result');
    
    if(isCorrect) {
        opts.forEach(o => o.disabled = true);
        btn.classList.remove('bg-slate-50', 'border-slate-200', 'hover:bg-indigo-50', 'hover:border-indigo-300');
        btn.classList.add('bg-emerald-100', 'border-emerald-400', 'text-emerald-700');
        res.innerHTML = '🎉 回答正确！太棒啦！';
        res.className = 'mt-4 font-bold text-lg text-emerald-600 animate-bounce';
        res.classList.remove('hidden');
        confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
        let a = new Audio('data:audio/mp3;base64,//OkwAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAAQAABdwA==');
        a.play().catch(e=>{});
    } else {
        btn.classList.add('animate-shake', 'bg-red-50', 'border-red-300', 'text-red-600');
        setTimeout(() => btn.classList.remove('animate-shake'), 500);
        res.innerHTML = '❌ 不对哦，再试一次！';
        res.className = 'mt-4 font-bold text-lg text-red-500';
        res.classList.remove('hidden');
    }
}
"""

content = pattern_switchTab.sub(new_switchTab, content)

# Add animate-shake to styles
style_insert = """.animate-shake { animation: shake 0.5s; }
@keyframes shake { 0%, 100% {transform: translateX(0);} 25% {transform: translateX(-5px);} 75% {transform: translateX(5px);} }"""
content = content.replace('</style>', style_insert + '\n    </style>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("V3 Upgrade Complete!")
