import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Bug 1: Unescaped apostrophes breaking JS playAudio calls
content = content.replace("replace(/'/g, \"'\")", "replace(/'/g, \"\\\\'\")")
content = content.replace("replace(/'/g, \"\\'\")", "replace(/'/g, \"\\\\'\")")

# Fix Bug 2: Add Download button to MediaRecorder
pattern_record = re.compile(r"btn\.onclick = \(\) => \{.*?\};\n\s*};\n\s*\} catch\(err\)", re.DOTALL)

new_record_logic = """btn.onclick = () => {
                let audio = new Audio(recordedAudioUrl);
                btn.classList.add('opacity-70');
                audio.onended = () => btn.classList.remove('opacity-70');
                audio.play();
            };
            
            if (!btn.nextElementSibling || !btn.nextElementSibling.download) {
                let saveBtn = document.createElement('a');
                saveBtn.href = recordedAudioUrl;
                saveBtn.download = `Day${currentDay.day}_录音.webm`;
                saveBtn.className = 'flex-none w-16 bg-sky-50 border border-sky-100 text-sky-600 font-bold rounded-xl active:scale-95 transition flex flex-col items-center justify-center';
                saveBtn.innerHTML = '<i class="fas fa-download text-lg mb-1 block"></i>保存';
                btn.parentElement.appendChild(saveBtn);
            } else {
                btn.nextElementSibling.href = recordedAudioUrl;
            }
        };
    } catch(err)"""

content = pattern_record.sub(new_record_logic, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Apostrophe escapes fixed and Save Audio feature added!")
