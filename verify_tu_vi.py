import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

cuc_map = {
    "Thủy Nhị Cục": 2,
    "Mộc Tam Cục": 3,
    "Kim Tứ Cục": 4,
    "Thổ Ngũ Cục": 5,
    "Hỏa Lục Cục": 6
}

chi_list = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

def get_tu_vi_pos(cuc_val, day):
    for x in range(cuc_val):
        if (day + x) % cuc_val == 0:
            X = x
            break
    Q = (day + X) // cuc_val
    pos = 2 + (Q - 1) # base is Dần (index 2)
    if X % 2 == 0:
        pos += X
    else:
        pos -= X
    pos = pos % 12
    return chi_list[pos]

with open('bang_tu_vi.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('verify_output.md', 'w', encoding='utf-8') as out:
    out.write("| Cục | Ngày Sinh Âm Lịch | Vị trí trong file JSON | Vị trí theo công thức chuẩn Trung Châu | Khớp/Lệch |\n")
    out.write("|---|---|---|---|---|\n")

    mismatch = 0
    for cuc_name, branches in data.items():
        cuc_val = cuc_map[cuc_name]
        for branch, days in branches.items():
            for day in days:
                expected = get_tu_vi_pos(cuc_val, day)
                status = "✅ Khớp" if expected == branch else "❌ Lệch"
                if expected != branch:
                    mismatch += 1
                out.write(f"| {cuc_name} | {day} | {branch} | {expected} | {status} |\n")

    out.write(f"\nTotal mismatch: {mismatch}\n")

