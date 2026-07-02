import re
import shutil

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject IndexedDB logic at the top of the JS block
db_logic = """const audioDB = new Promise((resolve, reject) => {
    let req = indexedDB.open("RoyEnglishDB", 1);
    req.onupgradeneeded = e => {
        let db = e.target.result;
        if(!db.objectStoreNames.contains("audioStore")) {
            db.createObjectStore("audioStore");
        }
    };
    req.onsuccess = e => resolve(e.target.result);
    req.onerror = e => reject(e);
});

async function saveAudioToDB(id, blob) {
    try {
        let db = await audioDB;
        db.transaction("audioStore", "readwrite").objectStore("audioStore").put(blob, id);
    } catch(e) { console.error("DB Save Error:", e); }
}

async function loadAudioFromDB(id) {
    try {
        let db = await audioDB;
        return new Promise(resolve => {
            let req = db.transaction("audioStore").objectStore("audioStore").get(id);
            req.onsuccess = e => resolve(e.target.result);
            req.onerror = () => resolve(null);
        });
    } catch(e) { return null; }
}

let"""

if "audioDB" not in content:
    content = content.replace("let currentDay = null;", db_logic + " currentDay = null;")

# 2. Update switchTab('speak')
pattern_speak = re.compile(r"tab === 'speak'\) \{.*?(?=else if\(tab === 'read'\))", re.DOTALL)

new_speak_logic = """tab === 'speak') {
        let html = '<h3 class="font-extrabold text-lg text-slate-800 mb-4 flex items-center gap-2"><i class="fas fa-bullhorn text-pink-500"></i> 大声说出来</h3><div class="flex flex-col gap-4">';
        let itemsToSpeak = currentDay.words.slice(0, 3);
        if(itemsToSpeak.length === 0 && currentDay.dialogues.length > 0) itemsToSpeak = [{en: currentDay.dialogues[0].en, zh: currentDay.dialogues[0].zh}];
        
        itemsToSpeak.forEach((w, i) => {
            let audioId = `Day${currentDay.day}_Speak_${i}`;
            html += `<div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 text-center relative overflow-hidden">
                <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-pink-400 to-rose-400"></div>
                <div class="text-2xl sm:text-3xl font-extrabold text-slate-800 mb-1 mt-2">${w.en}</div>
                <div class="text-slate-500 mb-6 text-sm font-medium">${w.zh}</div>
                <div class="flex justify-center gap-3" id="speak-actions-${audioId}">
                    <button onclick="playAudio('${w.en.replace(/'/g, "\\\\'")}', this.querySelector('i'))" class="flex-1 bg-indigo-50 text-indigo-600 font-bold py-3 rounded-xl active:scale-95 transition"><i class="fas fa-volume-up mb-1 block text-xl"></i>听原音</button>
                    <button id="record-btn-${audioId}" onclick="toggleRecording(this, '${audioId}')" class="flex-1 bg-rose-50 border border-rose-100 text-rose-600 font-bold py-3 rounded-xl active:scale-95 transition"><i class="fas fa-microphone mb-1 block text-xl"></i>录音 (限10秒)</button>
                </div>
            </div>`;
            
            // Check cache asynchronously
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

# 3. Update toggleRecording and add renderSavedAudioBtn
pattern_record = re.compile(r"let mediaRecorder;.*?async function toggleRecording.*?catch\(err\) \{.*?\}", re.DOTALL)

new_record_logic = """let mediaRecorder = null;
let currentRecordAudioId = null;
let recordTimeout = null;
let audioChunks = [];

function renderSavedAudioBtn(btn, url, audioId) {
    let parent = btn.parentElement;
    let oldOriginBtn = parent.firstElementChild.outerHTML; // Keep the '听原音' button
    
    parent.innerHTML = oldOriginBtn + `
        <div class="flex-1 flex gap-1 sm:gap-2">
            <button onclick="let a = new Audio('${url}'); a.play();" class="flex-1 bg-green-50 text-green-600 font-bold rounded-xl active:scale-95 flex flex-col items-center justify-center py-2"><i class="fas fa-play text-lg"></i><span class="text-[10px] mt-1">回放</span></button>
            <a href="${url}" download="${audioId}.webm" class="flex-1 bg-sky-50 text-sky-600 font-bold rounded-xl active:scale-95 flex flex-col items-center justify-center py-2"><i class="fas fa-download text-lg"></i><span class="text-[10px] mt-1">保存</span></a>
            <button onclick="toggleRecording(this.parentElement, '${audioId}')" class="flex-1 bg-rose-50 text-rose-600 font-bold rounded-xl active:scale-95 flex flex-col items-center justify-center py-2"><i class="fas fa-redo text-lg"></i><span class="text-[10px] mt-1">重录</span></button>
        </div>
    `;
}

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
        
        // Transform the clicked element into a stop button
        btn.outerHTML = `<button id="stop-btn-${audioId}" onclick="toggleRecording(this, '${audioId}')" class="flex-1 bg-red-50 border border-red-200 text-red-600 font-bold py-3 rounded-xl active:scale-95 transition"><i class="fas fa-stop-circle text-xl animate-pulse mb-1 block"></i>录音中...点击停止</button>`;
        
        // Auto stop after 10 seconds
        recordTimeout = setTimeout(() => {
            if(mediaRecorder && mediaRecorder.state === "recording") mediaRecorder.stop();
        }, 10000);
        
        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            saveAudioToDB(audioId, audioBlob); // Save to IndexedDB
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
}"""

content = pattern_record.sub(new_record_logic, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

shutil.copy('index.html', 'RoyLearnEnglish_V2.html')
print("IndexedDB cache and 10s limit added to recording!")
