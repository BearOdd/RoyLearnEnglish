import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

speaker_config = """function getSpeakerConfig(role) {
    switch(role) {
        case 'dad': return { name: '爸爸(罗威)', bg: 'bg-blue-50', bgHex: 'dbeafe', border: 'border-blue-200', seed: 'Felix&top=shortHairShortFlat&facialHair=beardMedium&clothing=blazerAndShirt', voiceType: 'dad', isLeft: true, iconColor: 'text-blue-400', textColor: 'text-slate-800' };
        case 'mom': return { name: '妈妈(熊单)', bg: 'bg-pink-50', bgHex: 'fce7f3', border: 'border-pink-200', seed: 'Jocelyn&top=longHairStraight&accessories=prescription02&clothing=collarAndSweater', voiceType: 'mom', isLeft: false, iconColor: 'text-pink-400', textColor: 'text-slate-800' };
        case 'son': return { name: '儿子(光头)', bg: 'bg-green-50', bgHex: 'dcfce3', border: 'border-green-200', seed: 'Leo&top=noHair&clothing=graphicShirt', voiceType: 'son', isLeft: false, iconColor: 'text-green-400', textColor: 'text-slate-800' };
        case 'daughter': return { name: '女儿(妞妞)', bg: 'bg-yellow-50', bgHex: 'fef08a', border: 'border-yellow-200', seed: 'Lily&top=longHairBun&clothing=overall', voiceType: 'daughter', isLeft: true, iconColor: 'text-yellow-400', textColor: 'text-slate-800' };
        default: return { name: 'Robot', bg: 'bg-indigo-50', bgHex: 'e0e7ff', border: 'border-indigo-200', seed: 'Robot', voiceType: 'mom', isLeft: true, iconColor: 'text-indigo-400', textColor: 'text-slate-800' };
    }
}"""

content = re.sub(r'function getSpeakerConfig\(role\) \{.*?(?=function speakWithGender)', speaker_config + "\n\n", content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Avatar config updated!")
