import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def audit_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Count 'æ' and 'ò'
    # Wait, 'ò' is a standard Vietnamese character (o huyền).
    # But let's check if the user meant 'ò' as a standalone weird character from VNI that didn't get mapped properly.
    count_ae = text.count('æ')
    count_o_grave = text.count('ò') # Note: 'ò' could be from standard mapping or unmapped VNI?
    # Actually, my VNI map has 'oø': 'ò'. So 'ò' is expected if it was 'oø'.
    # But maybe the word 'vò' (vị) was literal 'v' + 'ò'.
    
    print(f"Total 'æ': {count_ae}")
    print(f"Total 'ò': {count_o_grave}")
    
    print("\n--- 10 Contexts for 'æ' ---")
    ae_contexts = []
    lines = text.split('\n')
    for line in lines:
        if 'æ' in line:
            ae_contexts.append(line.strip())
            if len(ae_contexts) >= 10: break
    for c in ae_contexts:
        print(c)
        
    print("\n--- 10 Contexts for 'vò' (to see if 'vò' is used as 'vị') ---")
    vo_contexts = []
    for line in lines:
        if 'vò ' in line or ' vò ' in line or 'vò.' in line or 'vò,' in line:
            vo_contexts.append(line.strip())
            if len(vo_contexts) >= 10: break
    for c in vo_contexts:
        print(c)

    # 5. Regex for all non-Vietnamese and non-punctuation characters
    # Standard Vietnamese characters + numbers + common punctuation + newlines
    # Also include uppercase
    pattern = re.compile(r'[^a-zA-Z0-9\s.,;:\'"!?()\[\]{}\-–—_+=/\\|<>@#$%^&*\~`'
                         r'áàảãạăắằẳẵặâấầẩẫậ'
                         r'éèẻẽẹêếềểễệ'
                         r'íìỉĩị'
                         r'óòỏõọôốồổỗộơớờởỡợ'
                         r'úùủũụưứừửữự'
                         r'ýỳỷỹỵđ'
                         r'ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ'
                         r'ÉÈẺẼẸÊẾỀỂỄỆ'
                         r'ÍÌỈĨỊ'
                         r'ÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ'
                         r'ÚÙỦŨỤƯỨỪỬỮỰ'
                         r'ÝỲỶỸỴĐ]')
    
    weird_chars = {}
    for match in pattern.finditer(text):
        char = match.group()
        weird_chars[char] = weird_chars.get(char, 0) + 1
        
    print("\n--- Weird Characters Found ---")
    for k, v in sorted(weird_chars.items(), key=lambda x: x[1], reverse=True):
        print(f"Char: '{k}' (Hex: {hex(ord(k))}) - Count: {v}")
        
    print("\n--- Contexts for weird characters ---")
    for k in ['ë', 'î', 'ü', 'ø', 'Ï', 'û', 'ï', 'Æ', 'ó']:
        contexts = []
        for line in lines:
            if k in line:
                contexts.append(line.strip())
                if len(contexts) >= 3: break
        if contexts:
            print(f"Contexts for '{k}':")
            for c in contexts:
                print(f"  {c}")

if __name__ == "__main__":
    audit_file(r"D:\All Code\New folder\Numerology_Project\data\toan_thu_unicode.txt")
