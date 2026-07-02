import re
import shutil

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Nav Tab Deletion
content = re.sub(r'<button onclick="switchTab\(\'read\'\)".*?</button>', '', content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

shutil.copy('index.html', 'RoyLearnEnglish_V2.html')
print("Read tab removed!")
