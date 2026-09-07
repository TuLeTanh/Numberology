def reduce_number(num):
    master_numbers = {11, 22, 33}
    current = num
    while current > 9 and current not in master_numbers:
        current = sum(int(digit) for digit in str(current))
    return current

def calculate_life_path(day, month, year):
    date_str = f"{day}{month}{year}"
    total = sum(int(digit) for digit in date_str)
    return reduce_number(total)

def get_letter_value(char):
    pythagorean_table = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    }
    return pythagorean_table.get(char.upper(), 0)

def is_vowel(char):
    return char.upper() in {'A', 'E', 'I', 'O', 'U'}

def calculate_destiny(full_name):
    clean_name = ''.join(c.upper() for c in full_name if c.isalpha())
    total = sum(get_letter_value(c) for c in clean_name)
    return reduce_number(total)

def calculate_soul_urge(full_name):
    clean_name = ''.join(c.upper() for c in full_name if c.isalpha())
    total = sum(get_letter_value(c) for c in clean_name if is_vowel(c))
    return reduce_number(total)

def calculate_personality(full_name):
    clean_name = ''.join(c.upper() for c in full_name if c.isalpha())
    total = sum(get_letter_value(c) for c in clean_name if not is_vowel(c))
    return reduce_number(total)

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    test_cases = [
        {
            "name": "Barack Hussein Obama",
            "day": 4, "month": 8, "year": 1961,
            "expected": {"lifePath": 11, "destiny": 1, "soul": 9, "personality": 1}
        },
        {
            "name": "Emma Charlotte Duerre Watson",
            "day": 15, "month": 4, "year": 1990,
            "expected": {"lifePath": 11, "destiny": 9, "soul": 11, "personality": 7}
        },
        {
            "name": "Steven Paul Jobs",
            "day": 24, "month": 2, "year": 1955,
            "expected": {"lifePath": 1, "destiny": 1, "soul": 2, "personality": 8}
        },
        {
            # Note: Quy tắc đã chốt (quyết định có chủ đích của chủ dự án): 
            # giữ Master Number 11/22/33 ngay khi xuất hiện ở BẤT KỲ bước cộng nào trong quá trình rút gọn, 
            # kể cả ở lần cộng tổng thô đầu tiên — không yêu cầu phải xuất hiện đúng ở bước cộng cuối cùng 
            # (khác quy ước 33/6 của một số trường phái như Hans Decoz).
            "name": "Albert Einstein",
            "day": 14, "month": 3, "year": 1879,
            "expected": {"lifePath": 33, "destiny": 9, "soul": 7, "personality": 11}
        },
        {
            "name": "Elon Reeve Musk",
            "day": 28, "month": 6, "year": 1971,
            "expected": {"lifePath": 7, "destiny": 3, "soul": 11, "personality": 1}
        }
    ]

    print("CHẠY UNIT TEST THẦN SỐ HỌC ENGINE (PYTHON):\n")
    all_passed = True
    
    for idx, tc in enumerate(test_cases, 1):
        lp = calculate_life_path(tc["day"], tc["month"], tc["year"])
        des = calculate_destiny(tc["name"])
        soul = calculate_soul_urge(tc["name"])
        per = calculate_personality(tc["name"])
        
        pass_lp = (lp == tc["expected"]["lifePath"])
        pass_des = (des == tc["expected"]["destiny"])
        pass_soul = (soul == tc["expected"]["soul"])
        pass_per = (per == tc["expected"]["personality"])
        
        passed = pass_lp and pass_des and pass_soul and pass_per
        if not passed:
            all_passed = False
            
        exp_lp = tc["expected"]["lifePath"]
        exp_des = tc["expected"]["destiny"]
        exp_soul = tc["expected"]["soul"]
        exp_per = tc["expected"]["personality"]
        
        print(f'Case {idx}: {tc["name"]} ({tc["day"]}/{tc["month"]}/{tc["year"]})')
        print(f"  - Đường Đời:  {lp} {'✅' if pass_lp else f'❌ (Expected: {exp_lp})'}")
        print(f"  - Sứ Mệnh:    {des} {'✅' if pass_des else f'❌ (Expected: {exp_des})'}")
        print(f"  - Linh Hồn:   {soul} {'✅' if pass_soul else f'❌ (Expected: {exp_soul})'}")
        print(f"  - Nhân Cách:  {per} {'✅' if pass_per else f'❌ (Expected: {exp_per})'}")
        print("-" * 50)

    if all_passed:
        print("🎉 TẤT CẢ 5/5 TEST CASES ĐỀU PASS 100%!")
    else:
        print("⚠️ CÓ TEST CASE BỊ FAIL, KIỂM TRA LẠI LOGIC.")
