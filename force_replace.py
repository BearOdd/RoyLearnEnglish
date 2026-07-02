import re
import shutil

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_str = "function switchTab(tab) {"
end_str = "function finishDay(btn) {"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

new_switch_logic = """function switchTab(tab) {
    currentTab = tab;
    ['listen', 'speak', 'write'].forEach(t => {
        let btn = document.getElementById('tab-' + t);
        if(btn) btn.classList.remove('text-indigo-600', 'scale-110');
    });
    
    let activeBtn = document.getElementById('tab-' + tab);
    if(activeBtn) activeBtn.classList.add('text-indigo-600', 'scale-110');
    
    let content = document.getElementById('contentArea');
    content.scrollTop = 0;
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
                    <img src="https://api.dicebear.com/9.x/avataaars/svg?seed=${conf.seed}&backgroundColor=${conf.bgHex}" class="w-10 h-10 sm:w-12 sm:h-12 rounded-full shadow-sm bg-white border-2 border-slate-100 relative z-10 transition duration-300">
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
                <h2 class="text-3xl font-extrabold text-slate-800 drop-shadow-sm">角色配音</h2>
                <p class="text-sm text-rose-500 font-bold mt-1 tracking-wider uppercase">Dubbing Practice</p>
            </div>
            <div class="flex gap-2">
                <button onclick="playAllRecordings()" class="bg-emerald-500 text-white px-3 py-2 rounded-full font-bold shadow-md hover:bg-emerald-600 active:scale-95 transition text-sm flex items-center gap-2">
                    <i class="fas fa-play"></i> 播放全部录音
                </button>
            </div>
        </div><div class="flex flex-col gap-6 pb-20">`;
        
        currentDay.dialogues.forEach((d, index) => {
            let conf = getSpeakerConfig(d.speaker);
            let audioId = `Day${currentDay.day}_Speak_${index}`;
            let flexDir = conf.isLeft ? 'flex-row' : 'flex-row-reverse';
            
            html += `<div class="flex ${flexDir} items-end gap-2 sm:gap-3 w-full" style="animation: fadeIn 0.3s ease-out ${index * 0.1}s both;">
                <div class="relative group cursor-pointer flex-shrink-0 text-center" onclick="this.querySelector('img').classList.toggle('rotate-12');">
                    <img src="https://api.dicebear.com/9.x/avataaars/svg?seed=${conf.seed}&backgroundColor=${conf.bgHex}" class="w-10 h-10 sm:w-12 sm:h-12 rounded-full shadow-sm bg-white border-2 border-slate-100 relative z-10 transition duration-300">
                    <div class="text-[10px] text-slate-400 mt-1 font-bold whitespace-nowrap">${conf.name}</div>
                </div>
                
                <div class="max-w-[75%] p-3 sm:p-4 shadow-sm rounded-2xl ${conf.border} ${conf.bg} border relative group flex flex-col justify-center">
                    <div class="flex items-start justify-between gap-3">
                        <div class="text-[15px] sm:text-base font-bold ${conf.textColor} leading-snug font-sans">${d.en}</div>
                    </div>
                    
                    <div class="mt-3 flex gap-2 justify-${conf.isLeft ? 'start' : 'end'}" id="speak-actions-${audioId}">
                        <button onclick="playAudio('${d.en.replace(/'/g, "\\\\'")}', this.querySelector('i'), '${conf.voiceType}')" class="flex-none bg-white bg-opacity-60 text-indigo-600 font-bold py-1 px-3 rounded shadow-sm active:scale-95 transition text-[12px] flex items-center justify-center gap-1"><i class="fas fa-volume-up"></i> 示范</button>
                        <button id="record-btn-${audioId}" onclick="toggleRecording(this, '${audioId}')" class="flex-none bg-rose-500 text-white font-bold py-1 px-3 rounded shadow-sm active:scale-95 transition text-[12px] flex items-center justify-center gap-1"><i class="fas fa-microphone"></i> 录制配音</button>
                    </div>
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

function renderSavedAudioBtn(btn, url, audioId) {
    let parent = btn.parentElement;
    let oldOriginBtn = parent.firstElementChild.outerHTML; 
    
    parent.innerHTML = oldOriginBtn + `
        <div class="flex flex-1 gap-1">
            <button onclick="let a = new Audio('${url}'); a.play();" class="flex-1 bg-green-500 text-white font-bold rounded shadow-sm active:scale-95 flex items-center justify-center py-1 px-2"><i class="fas fa-play text-sm"></i><span class="text-[12px] ml-1">回放</span></button>
            <button onclick="toggleRecording(this.parentElement, '${audioId}')" class="flex-none bg-rose-50 text-rose-600 border border-rose-200 font-bold rounded shadow-sm active:scale-95 flex items-center justify-center py-1 px-2"><i class="fas fa-redo text-sm"></i><span class="text-[12px] ml-1">重录</span></button>
        </div>
    `;
}

let mediaRecorder = null;
let currentRecordAudioId = null;
let recordTimeout = null;
let audioChunks = [];

async function toggleRecording(btn, audioId) {
    if(mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        if(recordTimeout) clearTimeout(recordTimeout);
        return;
    }
    if(!navigator.mediaDevices) return alert("浏览器不支持录音，或未开启 HTTPS！");
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        currentRecordAudioId = audioId;
        audioChunks = [];
        
        mediaRecorder.start();
        
        btn.outerHTML = `<button id="stop-btn-${audioId}" onclick="toggleRecording(this, '${audioId}')" class="flex-1 bg-red-50 border border-red-200 text-red-600 font-bold py-1 px-3 rounded shadow-sm active:scale-95 transition text-[12px]"><i class="fas fa-stop-circle text-sm animate-pulse mr-1"></i>录音中</button>`;
        
        recordTimeout = setTimeout(() => {
            if(mediaRecorder && mediaRecorder.state === "recording") mediaRecorder.stop();
        }, 10000);
        
        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            saveAudioToDB(audioId, audioBlob); 
            let url = URL.createObjectURL(audioBlob);
            
            let stopBtn = document.getElementById(`stop-btn-${audioId}`);
            if(stopBtn) {
                renderSavedAudioBtn(stopBtn, url, audioId);
            }
            stream.getTracks().forEach(t => t.stop());
        };
    } catch(err) {
        alert("无法访问麦克风，请检查权限！");
    }
}

"""

new_content = content[:start_idx] + new_switch_logic + content[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Massive hard replace complete!")
