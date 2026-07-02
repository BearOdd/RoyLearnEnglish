import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the SECOND declaration
content = content.replace('let mediaRecorder = null;\nlet currentRecordAudioId = null;\nlet recordTimeout = null;\nlet audioChunks = [];\n\nasync function toggleRecording', 'async function toggleRecording')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
