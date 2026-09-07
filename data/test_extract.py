import re

text = open('1283-tu-dien-tu-vi-dau-so-va-than-so-hoc-thuviensach.vn_ocr.txt', encoding='utf-8').read()
start = text.find('4. TỰ ĐIỂN - TỬ VI')
if start == -1:
    start = text.find('TỰ ĐIỂN')
text = text[start:] if start != -1 else text

# Match numbers followed by dot, then capitalized words
vi_chars = "A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ"
regex = r'\n(\d{1,3})\.\s+([' + vi_chars + r'\s]+):?'

matches = list(re.finditer(regex, text))

entries = []
for i in range(len(matches)):
    m = matches[i]
    num = m.group(1)
    name = m.group(2).strip()
    start_pos = m.end()
    end_pos = matches[i+1].start() if i + 1 < len(matches) else len(text)
    
    content = text[start_pos:end_pos].strip()
    if len(name) > 1 and not name.islower():
        entries.append((num, name, content))

print(f"Found {len(entries)} stars")
for e in entries[:10]:
    print(f"{e[0]}. {e[1]}")
    
# Check if 113 was found
for e in entries:
    if e[0] == '113':
        print(f"\nLast star: {e[0]}. {e[1]}")
