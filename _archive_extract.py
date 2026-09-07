import re
import os
import json
import time
from google import genai
from google.genai import types

# Tự động lấy API key từ biến môi trường
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Vui lòng thiết lập biến môi trường GEMINI_API_KEY trước khi chạy.")
    print(r"Ví dụ: $env:GEMINI_API_KEY='your_api_key'")
    exit(1)

client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTION = """
Vai trò: Bạn là trợ lý trích xuất tri thức từ văn bản Tử Vi Đẩu Số sang dữ liệu có cấu trúc để dùng trong 1 rule engine.

Input: đoạn văn bản chứa mô tả của NHIỀU sao liên tiếp, trích từ sách "Tự Điển Tử Vi Đẩu Số" (ý nghĩa 12 cung) và "Vương Đình Chi Đàm Đẩu Số" (cách cục, nếu có). Mỗi sao được đánh dấu ranh giới rõ bằng số thứ tự và tên sao trong sách gốc.

Nhiệm vụ — LẶP LẠI CHO TỪNG SAO CÓ TRONG INPUT, không được gộp/lẫn nội dung giữa các sao với nhau:
1. Xác định sao đang được mô tả.
2. Trích xuất chính xác điều kiện/công thức an sao (nếu văn bản có nêu).
3. Trích xuất ý nghĩa của sao tại các cung (Mệnh, Phụ Mẫu, Phúc Đức, Điền Trạch, Quan Lộc, Nô Bộc, Thiên Di, Tật Ách, Tài Bạch, Tử Tức, Phu Thê, Huynh Đệ, Hạn). Cung nào văn bản không đề cập thì bỏ qua, không ghi "THIẾU DỮ LIỆU" tràn lan cho đủ 12 cung — chỉ liệt kê cung nào thực sự có trong văn bản.
4. Trích xuất các "cách cục" (tổ hợp sao đặc biệt) và ý nghĩa, nếu văn bản có.
5. Không bịa thêm nội dung không có trong văn bản gốc, không tự suy diễn khi thiếu dữ liệu, không mượn nội dung của sao khác trong cùng batch để bù vào.

Ràng buộc TỐI QUAN TRỌNG:
- Số phần tử trong mảng output phải khớp ĐÚNG số sao có trong input — không được gộp 2 sao thành 1, không được bỏ sót sao nào.
- CHỈ tạo object cho các sao được đánh số/đề mục chính ở đầu dòng trong input (dạng 'N. TÊN SAO:'). TUYỆT ĐỐI KHÔNG tạo object riêng cho bất kỳ tên sao nào chỉ được nhắc đến/liệt kê thêm trong nội dung diễn giải của một sao khác (vd liệt kê tổ hợp sao đi cùng trong 1 cung).
- Nếu 1 sao trong batch không đủ dữ liệu để trích xuất trọn vẹn, vẫn trả về object cho sao đó với các trường rỗng/thiếu, kèm ghi chú trong "ghi_chu_thieu_du_lieu" — không vì 1 sao thiếu data mà bỏ luôn cả object đó ra khỏi mảng (sẽ làm lệch thứ tự đối chiếu về sau).
"""

response_schema = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "sao": {"type": "STRING"},
            "loai": {"type": "STRING"},
            "cong_thuc_an_sao": {
                "type": "OBJECT",
                "properties": {
                    "input": {"type": "ARRAY", "items": {"type": "STRING"}},
                    "logic": {"type": "STRING"}
                }
            },
            "y_nghia_theo_cung": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "cung": {"type": "STRING"},
                        "dien_giai": {"type": "STRING"}
                    }
                }
            },
            "cach_cuc": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "ten_cach": {"type": "STRING"},
                        "dieu_kien": {"type": "STRING"},
                        "y_nghia": {"type": "STRING"}
                    }
                }
            },
            "ghi_chu_thieu_du_lieu": {
                "type": "ARRAY",
                "items": {"type": "STRING"}
            }
        },
        "required": ["sao", "y_nghia_theo_cung"]
    }
}

def extract_stars_from_text(file_path):
    print(f"Đọc file {file_path}...")
    with open(file_path, encoding='utf-8') as f:
        text = f.read()
    
    start = text.find('4. TỰ ĐIỂN - TỬ VI ĐẨU SỐ')
    if start == -1:
        start = text.find('TỰ ĐIỂN')
    text = text[start:] if start != -1 else text

    vi_chars = "A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ"
    regex = r'\n(\d{1,3}(?:\s*VÀ\s*\d{1,3})?)\.\s+(["' + vi_chars + r'\s]+):?'
    matches = list(re.finditer(regex, text))
    
    entries = []
    for i in range(len(matches)):
        m = matches[i]
        num_str = m.group(1).strip()
        name_str = m.group(2).strip()
        start_pos = m.end()
        end_pos = matches[i+1].start() if i + 1 < len(matches) else len(text)
        
        content = text[start_pos:end_pos].strip()
        
        if len(name_str) > 1 and not name_str.islower():
            if 'VÀ' in num_str.upper():
                nums = re.split(r'\s*VÀ\s*', num_str.upper())
                names = re.split(r'\s*VÀ\s*', name_str.upper())
                if len(nums) == 2 and len(names) >= 2:
                    entries.append({"num": nums[0], "name": names[0].strip(), "content": content})
                    entries.append({"num": nums[1], "name": names[1].strip(), "content": content})
                else:
                    entries.append({"num": num_str, "name": name_str, "content": content})
            else:
                entries.append({"num": num_str, "name": name_str, "content": content})
            
    # Lọc các entry lỗi OCR
    entries = [e for e in entries if len(e['content']) >= 20]
    return entries

def process_batch(batch, batch_index, output_dir="sao_json"):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Đang xử lý Batch {batch_index} (chứa {len(batch)} sao)...")
    
    prompt = f"Batch này có ĐÚNG {len(batch)} sao sau đây, liệt kê theo thứ tự:\n"
    for idx, item in enumerate(batch, 1):
        prompt += f"{idx}. {item['name']}\n"
        
    prompt += f"\nBạn PHẢI trả về mảng JSON có ĐÚNG và CHỈ đúng {len(batch)} phần tử, mỗi phần tử ứng với 1 tên trong danh sách trên theo đúng thứ tự. Không thêm, không bớt, không đổi thứ tự.\n\n"
    prompt += "[VĂN BẢN ĐẦU VÀO CỦA CÁC SAO]:\n\n"
    
    for item in batch:
        prompt += f"--- SAO SỐ {item['num']}: {item['name']} ---\n{item['content']}\n\n"
    
    max_retries = 3
    first_attempt_429 = False
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    response_mime_type="application/json",
                    response_schema=response_schema,
                    temperature=0.0
                ),
            )
            
            results = json.loads(response.text)
            
            if not isinstance(results, list):
                print(f"[!] Lỗi Batch {batch_index}: Output không phải là mảng JSON. Đã log lại để chạy tay.")
                return "FAIL", False
                
            if len(results) != len(batch):
                print(f"[!] Lỗi Batch {batch_index}: Số lượng output ({len(results)}) khác số lượng input ({len(batch)}). Đã log lại để chạy tay.")
                with open(os.path.join(output_dir, f"_batch_{batch_index}_error_output.json"), 'w', encoding='utf-8') as err_f:
                    json.dump(results, err_f, ensure_ascii=False, indent=2)
                return "FAIL", False
                
            # Ghi các file JSON rời rạc cho từng sao
            for res in results:
                safe_name = res.get('sao', 'unknown').lower().replace(' ', '_').replace('/', '_')
                filename = os.path.join(output_dir, f"{safe_name}.json")
                with open(filename, 'w', encoding='utf-8') as out_f:
                    json.dump(res, out_f, ensure_ascii=False, indent=2)
                    
            print(f"-> Batch {batch_index}: input {len(batch)}, output {len(results)} — khớp! Đã lưu {len(results)} file.")
            return "SUCCESS", False
            
        except Exception as e:
            err_msg = str(e)
            is_429 = "429" in err_msg or "quota" in err_msg.lower() or "503" in err_msg
            print(f"Lỗi khi xử lý Batch {batch_index} (lần thử {attempt + 1}/{max_retries}): {err_msg}")
            
            if is_429:
                # Nếu lần thử ĐẦU TIÊN của batch bị 429, báo cờ hiệu để main() đếm
                if attempt == 0:
                    first_attempt_429 = True
                
                # Tìm retryDelay
                wait_time = 15 * (attempt + 1)
                delay_match = re.search(r"'retryDelay':\s*'(\d+)s'", err_msg)
                if delay_match:
                    wait_time = int(delay_match.group(1)) + 2 # +2s buffer
                    
                print(f"-> Chờ {wait_time}s rồi thử lại...")
                time.sleep(wait_time)
                
                # Nếu đã thử hết số lần mà vẫn tèo
                if attempt == max_retries - 1:
                    return "FAIL", first_attempt_429
            else:
                return "FAIL", first_attempt_429
    
    print(f"Batch {batch_index} thất bại sau {max_retries} lần thử.")
    return "FAIL", first_attempt_429
    
def chunk_entries(entries, batch_size=5):
    """Chia nhỏ entries thành các batch"""
    for i in range(0, len(entries), batch_size):
        yield entries[i:i + batch_size]

def main():
    # Đọc OCR file từ trong thư mục data/
    ocr_file = os.path.join('data', '1283-tu-dien-tu-vi-dau-so-va-than-so-hoc-thuviensach.vn_ocr.txt')
    all_stars = extract_stars_from_text(ocr_file)
    print(f"Tìm thấy {len(all_stars)} mục sao hợp lệ trong văn bản gốc.")
    
    output_dir = "sao_json"
    os.makedirs(output_dir, exist_ok=True)
    
    # Lọc bỏ những sao đã có file JSON
    pending_stars = []
    for star in all_stars:
        safe_name = star['name'].lower().replace(' ', '_').replace('/', '_')
        if not os.path.exists(os.path.join(output_dir, f"{safe_name}.json")):
            pending_stars.append(star)
            
    print(f"Số sao còn thiếu cần bóc tách: {len(pending_stars)}")
    if len(pending_stars) == 0:
        print("Tất cả các sao đã được bóc tách xong!")
        return

    BATCH_SIZE = 10 # Tăng lên 10 để giảm tổng số request
    batches = list(chunk_entries(pending_stars, BATCH_SIZE))
    
    print(f"Sẽ chạy tổng cộng {len(batches)} batches.")
    
    consecutive_first_try_429 = 0
    
    for idx, batch in enumerate(batches, 1):
        status, failed_on_first = process_batch(batch, idx, output_dir="sao_json")
        
        if failed_on_first and status == "FAIL":
            consecutive_first_try_429 += 1
        elif status == "SUCCESS":
            consecutive_first_try_429 = 0
            
        if consecutive_first_try_429 >= 2:
            print("\n[!!!] Quota ngày đã hết (hoặc bị rate-limit quá gắt liên tục), dừng lại, chạy lại sau!")
            break
            
        if status == "FAIL":
            print(f"Batch {idx} thất bại. Xin lưu ý log file và chạy tay hoặc fix lại sau.")
            
        time.sleep(5) # Tránh rate limit
        
if __name__ == "__main__":
    main()
