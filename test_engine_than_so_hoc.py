import pytest
from engine_than_so_hoc import calculate_life_path, calculate_destiny, calculate_soul_urge, calculate_personality

def test_engine_than_so_hoc_cases():
    test_cases = [
        {
            "name": "Barack Hussein Obama",
            "day": 4, "month": 8, "year": 1961,
            # Life Path B: 4 + 8 + 1961 = 1973 -> 1+9+7+3 = 20 -> 2
            "expected": {"lifePath": 2, "destiny": 1, "soul": 9, "personality": 1}
        },
        {
            "name": "Emma Charlotte Duerre Watson",
            "day": 15, "month": 4, "year": 1990,
            # Life Path B: 15 + 4 + 1990 = 2009 -> 2+0+0+9 = 11 (Master)
            "expected": {"lifePath": 11, "destiny": 9, "soul": 11, "personality": 7}
        },
        {
            "name": "Nguyễn Văn An",
            "day": 21, "month": 5, "year": 2015,
            # NGUYEN VAN AN
            # Vowels: U(3)+E(5)+A(1)+A(1) = 10 -> 1
            # Consonants: N(5)+G(7)+Y(7)+N(5) + V(4)+N(5) + N(5) = 38 -> 11 (Master Number)
            # Destiny: 38 + 10 = 48 -> 12 -> 3
            # Life Path B: 21 + 5 + 2015 = 2041 -> 2+0+4+1 = 7
            "expected": {"lifePath": 7, "destiny": 3, "soul": 1, "personality": 11}
        },
        {
            "name": "Trần Tuấn Dũng",
            "day": 1, "month": 1, "year": 2000,
            # TRAN TUAN DUNG
            # Vowels: A(1) + U(3) + A(1) + U(3) = 8
            # Consonants: T(2)+R(9)+N(5) + T(2)+N(5) + D(4)+N(5)+G(7) = 39 -> 12 -> 3
            # Destiny: 47 -> 11 (Master Number)
            # Life Path B: 1 + 1 + 2000 = 2002 -> 2+0+0+2 = 4
            "expected": {"lifePath": 4, "destiny": 11, "soul": 8, "personality": 3}
        },
        {
            "name": "Lê Lộc",
            "day": 2, "month": 2, "year": 2002,
            # LE LOC
            # Vowels: E(5) + O(6) = 11 (Master Number)
            # Consonants: L(3) + L(3) + C(3) = 9
            # Destiny: 11 + 9 = 20 -> 2
            # Life Path B: 2 + 2 + 2002 = 2006 -> 2+0+0+6 = 8
            "expected": {"lifePath": 8, "destiny": 2, "soul": 11, "personality": 9}
        },
        {
            "name": "Trần Đức Anh",
            "day": 12, "month": 3, "year": 1990,
            # TRAN DUC ANH
            # Vowels: A(1) + U(3) + A(1) = 5 (Soul)
            # Consonants: T(2)+R(9)+N(5) + D(4)+C(3) + N(5)+H(8) = 36 -> 9 (Personality)
            # Destiny: 5 + 9 = 14 -> 5
            # Life Path B: 12 + 3 + 1990 = 2005 -> 2+0+0+5 = 7
            "expected": {"lifePath": 7, "destiny": 5, "soul": 5, "personality": 9}
        }
    ]

    for tc in test_cases:
        lp = calculate_life_path(tc["day"], tc["month"], tc["year"])
        des = calculate_destiny(tc["name"])
        soul = calculate_soul_urge(tc["name"])
        per = calculate_personality(tc["name"])

        assert lp == tc["expected"]["lifePath"], f'Failed LP for {tc["name"]}: {lp} != {tc["expected"]["lifePath"]}'
        assert des == tc["expected"]["destiny"], f'Failed Destiny for {tc["name"]}: {des} != {tc["expected"]["destiny"]}'
        assert soul == tc["expected"]["soul"], f'Failed Soul for {tc["name"]}: {soul} != {tc["expected"]["soul"]}'
        assert per == tc["expected"]["personality"], f'Failed Personality for {tc["name"]}: {per} != {tc["expected"]["personality"]}'
