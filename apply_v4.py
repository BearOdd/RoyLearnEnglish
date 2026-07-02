import re
import json
import shutil

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

with open('db_v4.json', 'r', encoding='utf-8') as f:
    db_new_str = f.read()

# Replace DB
content = re.sub(r'const DB = \[.*?\];', f'const DB = {db_new_str};', content, flags=re.DOTALL)

# Update getSpeakerConfig with better avatar configurations
speaker_config = """function getSpeakerConfig(role) {
    switch(role) {
        case 'dad': return { name: '爸爸(罗威)', bg: 'bg-blue-50', border: 'border-blue-200', seed: 'Felix&hair=shortHairShortFlat&clothing=blazerAndShirt&facialHair=beardMedium', voiceType: 'dad', isLeft: true, iconColor: 'text-blue-400', textColor: 'text-slate-800' };
        case 'mom': return { name: '妈妈(熊单)', bg: 'bg-pink-50', border: 'border-pink-200', seed: 'Jocelyn&hair=longHairStraight&clothing=collarAndSweater', voiceType: 'mom', isLeft: false, iconColor: 'text-pink-400', textColor: 'text-slate-800' };
        case 'son': return { name: '儿子(光头)', bg: 'bg-green-50', border: 'border-green-200', seed: 'Leo&hair=noHair&clothing=graphicShirt', voiceType: 'son', isLeft: false, iconColor: 'text-green-400', textColor: 'text-slate-800' };
        case 'daughter': return { name: '女儿(妞妞)', bg: 'bg-yellow-50', border: 'border-yellow-200', seed: 'Lily&hair=pigtails&accessories=prescription02', voiceType: 'daughter', isLeft: true, iconColor: 'text-yellow-400', textColor: 'text-slate-800' };
        default: return { name: 'Robot', bg: 'bg-indigo-50', border: 'border-indigo-200', seed: 'bot', voiceType: 'mom', isLeft: true, iconColor: 'text-indigo-400', textColor: 'text-slate-800' };
    }
}"""
content = re.sub(r'function getSpeakerConfig\(role\) \{.*?(?=function speakWithGender)', speaker_config + "\n\n", content, flags=re.DOTALL)


# Update switchTab('speak') to make it look IDENTICAL to 'listen', just replacing Translate with Record
pattern_speak = re.compile(r"else if\(tab === 'speak'\) \{.*?(?=else if\(tab === 'write'\))", re.DOTALL)

new_speak_logic = """else if(tab === 'speak') {
        let html = `<div class="flex justify-between items-end mb-6">
            <div>
                <h2 class="text-3xl font-extrabold text-slate-800 drop-shadow-sm">角色扮演</h2>
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
                <div class="flex ${flexDir} items-end gap-2 sm:gap-3 w-full">
                    <div class="relative group cursor-pointer flex-shrink-0 text-center opacity-80" onclick="this.querySelector('img').classList.toggle('rotate-12');">
                        <img src="https://api.dicebear.com/9.x/avataaars/svg?seed=${conf.seed}&backgroundColor=${conf.bg.replace('bg-','')}" class="w-10 h-10 sm:w-12 sm:h-12 rounded-full shadow-sm bg-white border-2 border-slate-200 relative z-10 transition duration-300">
                        <div class="text-[10px] text-slate-400 mt-1 font-bold whitespace-nowrap">${conf.name}</div>
                    </div>
                    
                    <div class="max-w-[75%] p-3 sm:p-4 shadow-sm rounded-2xl ${conf.border} bg-white border active:scale-[0.98] transition relative group flex flex-col justify-center">
                        <div class="flex items-start justify-between gap-3">
                            <div class="text-[15px] sm:text-base font-bold text-slate-800 leading-snug font-sans">${d.en}</div>
                        </div>
                        
                        <div class="mt-3 flex gap-2 justify-end" id="speak-actions-${audioId}">
                            <button onclick="playAudio('${d.en.replace(/'/g, "\\\\'")}', this.querySelector('i'), '${conf.voiceType}')" class="flex-1 bg-indigo-50 text-indigo-600 font-bold py-2 rounded-xl active:scale-95 transition text-sm flex items-center justify-center gap-1"><i class="fas fa-volume-up"></i> 原音</button>
                            <button id="record-btn-${audioId}" onclick="toggleRecording(this, '${audioId}')" class="flex-1 bg-rose-50 border border-rose-100 text-rose-600 font-bold py-2 rounded-xl active:scale-95 transition text-sm flex items-center justify-center gap-1"><i class="fas fa-microphone"></i> 录制</button>
                        </div>
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
    """

content = pattern_speak.sub(new_speak_logic, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

shutil.copy('index.html', 'RoyLearnEnglish_V2.html')

print("Applied strict textbook dialogues, Avatar props, and UI cleanup.")
