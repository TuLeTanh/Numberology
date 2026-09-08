import datetime as dt
import pytest
import sys
import os

# Add parent directory to path to import engine_tu_vi
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from engine_tu_vi import CHI_MAP
except ImportError:
    print("Cannot import CHI_MAP from engine_tu_vi.py")
    CHI_MAP = {
        0: "Tý", 1: "Sửu", 2: "Dần", 3: "Mão", 4: "Thìn", 5: "Tỵ",
        6: "Ngọ", 7: "Mùi", 8: "Thân", 9: "Dậu", 10: "Tuất", 11: "Hợi"
    }

# Test cases for Vietnamese Lunar Calendar
# Known dates:
# Date 1: 1985-03-21 (Solar) -> Lunar: 1985-02-01 (leap: True)
# Date 2: 2026-02-17 (Solar) -> Lunar: 2026-01-01 (leap: False)
# Date 3: 2007-02-17 (Solar) -> Lunar: 2007-01-01 (Vietnam Tet, China is 2007-02-18) -> Lunar VN must be 1/1, while Lunar CN would be 12/30 (of 2006)

test_cases = [
    {"solar": dt.date(2026, 2, 17), "lunar_expected": (2026, 1, 1, False)},
    {"solar": dt.date(1985, 3, 21), "lunar_expected": (1985, 2, 1, True)},
    {"solar": dt.date(2007, 2, 17), "lunar_expected": (2007, 1, 1, False)},
]

def test_lunar_vn():
    try:
        from lunar_vn import solar_to_lunar
        print("\n--- Testing lunar-vn ---")
        for tc in test_cases:
            res = solar_to_lunar(tc["solar"])
            print(f"Solar: {tc['solar']} -> lunar-vn: {res.year}-{res.month}-{res.day} (leap: {res.leap}) | Expected: {tc['lunar_expected'][0]}-{tc['lunar_expected'][1]}-{tc['lunar_expected'][2]}")
    except ImportError:
        print("\nlunar-vn not installed.")

def test_lunardate():
    try:
        from lunardate import LunarDate
        print("\n--- Testing lunardate (Chinese) ---")
        for tc in test_cases:
            res = LunarDate.from_solar_date(tc["solar"].year, tc["solar"].month, tc["solar"].day)
            print(f"Solar: {tc['solar']} -> lunardate: {res.year}-{res.month}-{res.day} (leap: {res.is_leap_month}) | Expected: {tc['lunar_expected'][0]}-{tc['lunar_expected'][1]}-{tc['lunar_expected'][2]}")
    except ImportError:
        print("\nlunardate not installed.")

from an_menh_cuc import get_gio_chi_index

def test_get_hour_chi():
    def get_hour_chi(gio: int, phut: int = 0) -> str:
        return CHI_MAP[get_gio_chi_index(gio, phut)]

    # 1. Tý
    assert get_hour_chi(23, 0) == CHI_MAP[0] # Tý
    assert get_hour_chi(23, 59) == CHI_MAP[0] # Tý
    assert get_hour_chi(0, 0) == CHI_MAP[0] # Tý
    assert get_hour_chi(0, 59) == CHI_MAP[0] # Tý

    # 2. Sửu
    assert get_hour_chi(1, 0) == CHI_MAP[1] # Sửu
    assert get_hour_chi(2, 59) == CHI_MAP[1] # Sửu

    # 3. Dần
    assert get_hour_chi(3, 0) == CHI_MAP[2] # Dần
    assert get_hour_chi(4, 59) == CHI_MAP[2] # Dần
    # 4. Mão
    assert get_hour_chi(5, 30) == CHI_MAP[3] # Mão
    # 5. Thìn
    assert get_hour_chi(7, 0) == CHI_MAP[4] # Thìn
    # 6. Tỵ
    assert get_hour_chi(10, 15) == CHI_MAP[5] # Tỵ
    # 7. Ngọ
    assert get_hour_chi(12, 0) == CHI_MAP[6] # Ngọ
    # 8. Mùi
    assert get_hour_chi(14, 45) == CHI_MAP[7] # Mùi
    # 9. Thân
    assert get_hour_chi(16, 0) == CHI_MAP[8] # Thân
    # 10. Dậu
    assert get_hour_chi(18, 30) == CHI_MAP[9] # Dậu
    # 11. Tuất
    assert get_hour_chi(20, 0) == CHI_MAP[10] # Tuất
    # 12. Hợi
    assert get_hour_chi(22, 59) == CHI_MAP[11] # Hợi
    
    import pytest
    with pytest.raises(ValueError):
        get_hour_chi(24, 0)
    with pytest.raises(ValueError):
        get_hour_chi(-1, 0)

if __name__ == "__main__":
    test_lunar_vn()
    test_lunardate()
    test_get_hour_chi()
    print("All tests passed.")
