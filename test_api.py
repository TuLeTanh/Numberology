import requests
import time
import json
import subprocess
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# Start the FastAPI server
print("Starting FastAPI server...")
server_process = subprocess.Popen([r".\.venv\Scripts\python", "main.py"])

# Wait for server to be ready
print("Waiting for server to start...")
time.sleep(3)

test_cases = [
    {
        "name": "Barack Obama",
        "data": {
            "ho_ten": "Barack Hussein Obama",
            "ngay_sinh": 4,
            "thang_sinh": 8,
            "nam_sinh": 1961
        }
    },
    {
        "name": "Emma Watson",
        "data": {
            "ho_ten": "Emma Charlotte Duerre Watson",
            "ngay_sinh": 15,
            "thang_sinh": 4,
            "nam_sinh": 1990
        }
    },
    {
        "name": "Steve Jobs",
        "data": {
            "ho_ten": "Steven Paul Jobs",
            "ngay_sinh": 24,
            "thang_sinh": 2,
            "nam_sinh": 1955
        }
    },
    {
        "name": "Albert Einstein",
        "data": {
            "ho_ten": "Albert Einstein",
            "ngay_sinh": 14,
            "thang_sinh": 3,
            "nam_sinh": 1879
        }
    },
    {
        "name": "Elon Musk",
        "data": {
            "ho_ten": "Elon Reeve Musk",
            "ngay_sinh": 28,
            "thang_sinh": 6,
            "nam_sinh": 1971
        }
    }
]

url = "http://127.0.0.1:8000/lasso"
headers = {"Content-Type": "application/json"}

try:
    for case in test_cases:
        print(f"\n--- Testing: {case['name']} ---")
        response = requests.post(url, json=case['data'], headers=headers)
        if response.status_code == 200:
            result = response.json()
            # Only print the summary to not clutter the output too much, but show full for 2 cases
            if case['name'] in ["Albert Einstein", "Steve Jobs"]:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                ts = result.get('than_so_hoc', {})
                print(f"Đường Đời: {ts.get('duong_doi', {}).get('gia_tri')}")
                print(f"Sứ Mệnh: {ts.get('su_menh', {}).get('gia_tri')}")
                print(f"Linh Hồn: {ts.get('linh_hon', {}).get('gia_tri')}")
                print(f"Nhân Cách: {ts.get('nhan_cach', {}).get('gia_tri')}")
        else:
            print(f"Failed! Status code: {response.status_code}")
            print(response.text)

finally:
    print("\nShutting down server...")
    server_process.terminate()
    server_process.wait()
    print("Done.")

