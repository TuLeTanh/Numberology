import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('bang_tu_vi.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for cuc_name, branches in data.items():
    all_days = set()
    for branch, days in branches.items():
        all_days.update(days)
    missing = set(range(1, 31)) - all_days
    if missing:
        print(f"{cuc_name} missing: {missing}")
