import re
import shutil

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Bug 2: Audio Skipping First Sentence
content = content.replace(
    "if ('speechSynthesis' in window && window.speechSynthesis.getVoices().length > 0) {",
    "if ('speechSynthesis' in window) {"
)

# And another bug: "utterance.onerror = () => playYoudaoFallback(text, isLeft, onComplete);"
# Wait, if utterance.onerror fires, does it mean speechSynthesis is completely broken?
# Yes, but on Safari, sometimes the first utterance fires an error if the user gesture is missing.
# Let's add a small retry or just let Youdao fallback handle it.
# Actually, Youdao fallback is failing. Let's make Youdao fallback more robust by logging the exact error.

content = content.replace(
    'currentAudio.play().catch(e => {',
    'currentAudio.play().catch(e => {\n        console.error("Youdao fallback failed: ", e);'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

shutil.copy('index.html', 'RoyLearnEnglish_V2.html')

print("First sentence skip bug fixed!")
