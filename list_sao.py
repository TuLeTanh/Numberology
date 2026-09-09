import os, sys
sys.stdout.reconfigure(encoding='utf-8')
files = os.listdir('sao_json')
print("All files:")
for f in sorted(files):
    print(f)
