import re
import shutil

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix Avatars (Remove invalid parameters that caused 400 Bad Request)
speaker_config = """function getSpeakerConfig(role) {
    switch(role) {
        case 'dad': return { name: '爸爸(罗威)', bg: 'bg-blue-50', bgHex: 'dbeafe', border: 'border-blue-200', seed: 'Felix', voiceType: 'dad', isLeft: true, iconColor: 'text-blue-400', textColor: 'text-slate-800' };
        case 'mom': return { name: '妈妈(熊单)', bg: 'bg-pink-50', bgHex: 'fce7f3', border: 'border-pink-200', seed: 'Jocelyn', voiceType: 'mom', isLeft: false, iconColor: 'text-pink-400', textColor: 'text-slate-800' };
        case 'son': return { name: '儿子(光头)', bg: 'bg-green-50', bgHex: 'dcfce3', border: 'border-green-200', seed: 'Leo', voiceType: 'son', isLeft: false, iconColor: 'text-green-400', textColor: 'text-slate-800' };
        case 'daughter': return { name: '女儿(妞妞)', bg: 'bg-yellow-50', bgHex: 'fef08a', border: 'border-yellow-200', seed: 'Lily', voiceType: 'daughter', isLeft: true, iconColor: 'text-yellow-400', textColor: 'text-slate-800' };
        default: return { name: 'Robot', bg: 'bg-indigo-50', bgHex: 'e0e7ff', border: 'border-indigo-200', seed: 'Robot', voiceType: 'mom', isLeft: true, iconColor: 'text-indigo-400', textColor: 'text-slate-800' };
    }
}"""
content = re.sub(r'function getSpeakerConfig\(role\) \{.*?(?=function speakWithGender)', speaker_config + "\n\n", content, flags=re.DOTALL)


# 2. Fix Voices (Catch all Windows/Edge/Chrome male/female voices + Extreme Pitch adjustments for kids)
voice_system = """let voiceCache = { dad: null, mom: null, son: null, daughter: null, inited: false };

function initVoices() {
    if(voiceCache.inited) return;
    let voices = window.speechSynthesis.getVoices().filter(v => v.lang.startsWith('en'));
    if(voices.length === 0) return;
    
    // Catch common Microsoft/Google/Apple voices
    let males = voices.filter(v => /guy|david|mark|george|arthur|brian|steffan|male|boy/i.test(v.name));
    let females = voices.filter(v => /aria|ana|jenny|zira|samantha|victoria|karen|moira|hazel|susan|female|girl/i.test(v.name));
    
    // Fallback to first available if none matched
    voiceCache.dad = males[0] || voices[0];
    voiceCache.mom = females[0] || voices[voices.length - 1];
    voiceCache.son = males[males.length > 1 ? 1 : 0] || voices[0];
    voiceCache.daughter = females[females.length > 1 ? 1 : 0] || voices[voices.length - 1];
    
    voiceCache.inited = true;
}

if ('speechSynthesis' in window) {
    window.speechSynthesis.onvoiceschanged = initVoices;
}

function speakWithGender(text, voiceType, onComplete) {
    initVoices();
    if ('speechSynthesis' in window) {
        let utterance = new SpeechSynthesisUtterance(text);
        utterance.voice = voiceCache[voiceType];
        utterance.rate = 0.85;
        
        // EXTREME Pitch modification to guarantee role identity
        if (voiceType === 'son') {
            utterance.pitch = 1.8; // High pitch for boy
            utterance.rate = 0.95; // Slightly faster
        } else if (voiceType === 'daughter') {
            utterance.pitch = 2.0; // Very high pitch for young girl
            utterance.rate = 0.95;
        } else if (voiceType === 'dad') {
            utterance.pitch = 0.5; // Deep voice for dad
        } else if (voiceType === 'mom') {
            utterance.pitch = 1.1; // Normal female
        }
        
        utterance.onend = onComplete;
        utterance.onerror = () => playYoudaoFallback(text, (voiceType==='mom'||voiceType==='daughter'), onComplete);
        window.speechSynthesis.speak(utterance);
    } else {
        playYoudaoFallback(text, (voiceType==='mom'||voiceType==='daughter'), onComplete);
    }
}"""
content = re.sub(r'let voiceCache = \{.*?(?=function playYoudaoFallback)', voice_system + "\n\n", content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Voices fixed and Avatar URLs sanitized!")
