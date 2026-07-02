import re
import json
import shutil

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

with open('db_v5.json', 'r', encoding='utf-8') as f:
    db_new_str = f.read()

# Replace DB
content = re.sub(r'const DB = \[.*?\];', f'const DB = {db_new_str};', content, flags=re.DOTALL)

# Update getSpeakerConfig with valid hex colors for Dicebear backgroundColor parameter
speaker_config = """function getSpeakerConfig(role) {
    switch(role) {
        case 'dad': return { name: '爸爸(罗威)', bg: 'bg-blue-50', bgHex: 'dbeafe', border: 'border-blue-200', seed: 'Dad6', voiceType: 'dad', isLeft: true, iconColor: 'text-blue-400', textColor: 'text-slate-800' };
        case 'mom': return { name: '妈妈(熊单)', bg: 'bg-pink-50', bgHex: 'fce7f3', border: 'border-pink-200', seed: 'Mom9', voiceType: 'mom', isLeft: false, iconColor: 'text-pink-400', textColor: 'text-slate-800' };
        case 'son': return { name: '儿子(光头)', bg: 'bg-green-50', bgHex: 'dcfce3', border: 'border-green-200', seed: 'Boy2', voiceType: 'son', isLeft: false, iconColor: 'text-green-400', textColor: 'text-slate-800' };
        case 'daughter': return { name: '女儿(妞妞)', bg: 'bg-yellow-50', bgHex: 'fef08a', border: 'border-yellow-200', seed: 'Girl3', voiceType: 'daughter', isLeft: true, iconColor: 'text-yellow-400', textColor: 'text-slate-800' };
        default: return { name: 'Robot', bg: 'bg-indigo-50', bgHex: 'e0e7ff', border: 'border-indigo-200', seed: 'Robot', voiceType: 'mom', isLeft: true, iconColor: 'text-indigo-400', textColor: 'text-slate-800' };
    }
}"""
content = re.sub(r'function getSpeakerConfig\(role\) \{.*?(?=function speakWithGender)', speaker_config + "\n\n", content, flags=re.DOTALL)

# In Listen tab, use bgHex for the Avatar API Call
content = content.replace(
    'src="https://api.dicebear.com/9.x/avataaars/svg?seed=${conf.seed}&backgroundColor=${conf.bg.replace(\'bg-\',\'\')}"',
    'src="https://api.dicebear.com/9.x/avataaars/svg?seed=${conf.seed}&backgroundColor=${conf.bgHex}"'
)

# Replace Speak Tab with Exact Same Layout as Listen Tab, Plus the playAllRecordings Logic
pattern_speak = re.compile(r"else if\(tab === 'speak'\) \{.*?(?=else if\(tab === 'write'\))", re.DOTALL)

new_speak_logic = """else if(tab === 'speak') {
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
                    <img src="https://api.dicebear.com/9.x/avataaars/svg?seed=${conf.seed}&backgroundColor=${conf.bgHex}" class="w-10 h-10 sm:w-12 sm:h-12 rounded-full shadow-sm bg-white border-2 border-white relative z-10 transition duration-300">
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
    """
content = pattern_speak.sub(new_speak_logic, content)

# Inject playAllRecordings function globally
play_all_recordings = """
async function playAllRecordings() {
    if(!currentDay || !currentDay.dialogues) return;
    let ids = currentDay.dialogues.map((d, i) => `Day${currentDay.day}_Speak_${i}`);
    let blobs = [];
    for(let id of ids) {
        let b = await loadAudioFromDB(id);
        blobs.push(b);
    }
    
    let i = 0;
    let playNextRecord = () => {
        while(i < blobs.length && !blobs[i]) i++;
        if(i >= blobs.length) {
            alert("所有可用录音播放完毕！");
            return;
        }
        let url = URL.createObjectURL(blobs[i]);
        let audio = new Audio(url);
        audio.onended = () => { i++; playNextRecord(); };
        audio.play().catch(err => { console.error(err); i++; playNextRecord(); });
    };
    playNextRecord();
}
"""

content = content.replace("function playAllDialogues() {", play_all_recordings + "\nfunction playAllDialogues() {")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("V5 Applied")
