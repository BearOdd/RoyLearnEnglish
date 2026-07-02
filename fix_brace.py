import re
import shutil

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the extra brace syntax error
content = content.replace('    }\n}\n}\n\nfunction checkSpelling', '    }\n}\n\nfunction checkSpelling')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

shutil.copy('index.html', 'RoyLearnEnglish_V2.html')

print("Syntax error fixed!")
