"""
cohere_client.py — Phase 3: Wrapper gọi Cohere Chat API

Dùng Cohere SDK v7 (ClientV2).
Model: command-r-plus-08-2024 (alias command-r-plus)
- command-r-plus: 128k context, chất lượng cao nhất, 3$/1M input token
- command-r:      128k context, nhanh hơn, 0.15$/1M input token

Đã xác nhận tên model từ SDK v7.0.8:
    cohere.ClientV2.chat(model="command-r-plus", ...)
"""
import os
import cohere

# Bộ đếm cuộc gọi trong phiên — in-memory, reset khi restart server
_call_count = 0


def goi_cohere(
    system_prompt: str,
    user_message: str,
    api_key: str | None = None,
    max_tokens: int = 300,
    model: str = "command-r-plus-08-2024",
) -> str:
    """
    Gọi Cohere Chat API, trả về text response.

    Parameters
    ----------
    system_prompt : Hướng dẫn ràng buộc hành vi model
    user_message  : Nội dung câu hỏi / yêu cầu diễn giải
    api_key       : Nếu None, đọc từ COHERE_API_KEY env var
    max_tokens    : Giới hạn token trong response
    model         : Tên model Cohere (mặc định: command-r-plus)

    Returns
    -------
    str  — text response, hoặc thông báo lỗi nếu gọi API thất bại
    """
    global _call_count

    key = api_key if api_key is not None else os.environ.get("COHERE_API_KEY", "")
    if not key:
        return "[LỖI] COHERE_API_KEY chưa được cấu hình. Kiểm tra file .env."

    try:
        client = cohere.ClientV2(api_key=key)
        response = client.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=max_tokens,
        )
        _call_count += 1
        text = response.message.content[0].text
        print(f"[Cohere] Lần gọi #{_call_count} trong phiên này | model={model} | tokens_out≈{len(text.split())}")
        return text

    except cohere.errors.UnauthorizedError:
        return "[LỖI 401] COHERE_API_KEY không hợp lệ hoặc đã hết hạn."
    except cohere.errors.TooManyRequestsError:
        return "[LỖI 429] Đã vượt giới hạn rate limit. Thử lại sau ít phút."
    except Exception as e:
        return f"[LỖI] Không thể kết nối Cohere: {type(e).__name__}: {e}"


def get_call_count() -> int:
    """Trả về số lần đã gọi Cohere trong phiên server hiện tại."""
    return _call_count
