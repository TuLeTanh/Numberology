import json
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

def fuzzy_search(text, query):
    q = re.sub(r'\s+', ' ', query).strip().lower()
    t = re.sub(r'\s+', ' ', text).strip().lower()
    
    if q in t:
        idx = t.find(q)
        return True, t[max(0, idx-20):idx+len(q)+20]
    
    words = q.split()
    if len(words) > 5:
        sub_q = " ".join(words[:5])
        if sub_q in t:
            idx = t.find(sub_q)
            return True, t[max(0, idx-20):idx+len(q)+20]
    return False, ""

with open("data/than_so_hoc_bang_tra.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("data/1283-tu-dien-tu-vi-dau-so-va-than-so-hoc-thuviensach.vn_ocr.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()
    
# Let's take some strings and see if they exist
def audit_all():
    matched = 0
    total = 0
    
    # check cach_tinh_so
    for key, text in data.get("cach_tinh_so", {}).items():
        total += 1
        found, match = fuzzy_search(raw_text, text)
        if found: matched += 1
        else: print(f"NOT FOUND: {text[:50]}...")
        
    for so, thong_tin in data.get("so_dinh_menh", {}).items():
        for field in ["hanh_tinh_lien_he", "tinh_tinh", "nhan_cach", "cong_viec_nang_khieu", "tien_bac"]:
            text = thong_tin.get(field, "")
            if text:
                total += 1
                found, match = fuzzy_search(raw_text, text)
                if found: matched += 1
                else: print(f"NOT FOUND (So {so} - {field}): {text[:50]}...")
        
        # tinh_duyen
        tinh_duyen = thong_tin.get("tinh_duyen", {}).get("mo_ta_chung", "")
        if tinh_duyen:
            total += 1
            found, match = fuzzy_search(raw_text, tinh_duyen)
            if found: matched += 1
            else: print(f"NOT FOUND (So {so} - tinh_duyen): {tinh_duyen[:50]}...")

    print(f"\nAudit complete: {matched}/{total} found ({matched/total*100:.2f}%)")

audit_all()
