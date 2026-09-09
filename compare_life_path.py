def reduce_number(num):
    master_numbers = {11, 22, 33}
    current = num
    while current > 9 and current not in master_numbers:
        current = sum(int(digit) for digit in str(current))
    return current

def calc_a(day, month, year):
    date_str = f"{day}{month}{year}"
    total = sum(int(digit) for digit in date_str)
    return reduce_number(total)

def calc_b(day, month, year):
    total = day + month + year
    return reduce_number(total)

import datetime
start_date = datetime.date(1950, 1, 1)
end_date = datetime.date(2010, 12, 31)

diffs = []
total_days = (end_date - start_date).days + 1

for i in range(total_days):
    d = start_date + datetime.timedelta(days=i)
    a = calc_a(d.day, d.month, d.year)
    b = calc_b(d.day, d.month, d.year)
    if a != b:
        diffs.append((d, a, b))

print(f"Total checked: {total_days}")
print(f"Total differences: {len(diffs)}")
for diff in diffs[:20]:
    print(f"Date: {diff[0].strftime('%d/%m/%Y')} -> Method A: {diff[1]}, Method B: {diff[2]}")
