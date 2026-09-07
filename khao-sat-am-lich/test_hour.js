// File: test_hour.js

/**
 * Tính Giờ Chi cố định dựa trên giờ đồng hồ thực tế.
 * 23h-1h=Tý, 1h-3h=Sửu, 3h-5h=Dần, 5h-7h=Mão, 7h-9h=Thìn, 9h-11h=Tỵ, 
 * 11h-13h=Ngọ, 13h-15h=Mùi, 15h-17h=Thân, 17h-19h=Dậu, 19h-21h=Tuất, 21h-23h=Hợi.
 * 
 * @param {number} hour Giờ từ 0 đến 23
 * @param {number} minute Phút từ 0 đến 59
 * @returns {string} Tên Chi của giờ
 */
function getHourChi(hour, minute = 0) {
    if (hour < 0 || hour > 23 || minute < 0 || minute > 59) {
        throw new Error("Giờ không hợp lệ");
    }

    if (hour === 23 || hour === 0) return "Tý";
    if (hour === 1 || hour === 2) return "Sửu";
    if (hour === 3 || hour === 4) return "Dần";
    if (hour === 5 || hour === 6) return "Mão";
    if (hour === 7 || hour === 8) return "Thìn";
    if (hour === 9 || hour === 10) return "Tỵ";
    if (hour === 11 || hour === 12) return "Ngọ";
    if (hour === 13 || hour === 14) return "Mùi";
    if (hour === 15 || hour === 16) return "Thân";
    if (hour === 17 || hour === 18) return "Dậu";
    if (hour === 19 || hour === 20) return "Tuất";
    if (hour === 21 || hour === 22) return "Hợi";
    
    return "Không xác định";
}

// Bảng tra để test
const testCases = [
    // Biên giờ Tý
    { h: 23, m: 0, expected: "Tý", desc: "Đầu giờ Tý" },
    { h: 23, m: 59, expected: "Tý", desc: "Trong giờ Tý" },
    { h: 0, m: 0, expected: "Tý", desc: "Nửa đêm giờ Tý" },
    { h: 0, m: 59, expected: "Tý", desc: "Cuối giờ Tý" },

    // Các khung giờ khác
    { h: 1, m: 0, expected: "Sửu", desc: "Đầu giờ Sửu" },
    { h: 3, m: 30, expected: "Dần", desc: "Giữa giờ Dần" },
    { h: 6, m: 59, expected: "Mão", desc: "Cuối giờ Mão" },
    { h: 8, m: 15, expected: "Thìn", desc: "Trong giờ Thìn" },
    { h: 10, m: 10, expected: "Tỵ", desc: "Trong giờ Tỵ" },
    { h: 12, m: 0, expected: "Ngọ", desc: "Giữa trưa giờ Ngọ" },
    { h: 14, m: 45, expected: "Mùi", desc: "Trong giờ Mùi" },
    { h: 16, m: 0, expected: "Thân", desc: "Trong giờ Thân" },
    { h: 18, m: 30, expected: "Dậu", desc: "Trong giờ Dậu" },
    { h: 20, m: 0, expected: "Tuất", desc: "Đầu giờ Tuất" },
    { h: 22, m: 59, expected: "Hợi", desc: "Cuối giờ Hợi" }
];

function runTest() {
    console.log("=== TEST HÀM TÍNH GIỜ CHI ĐỘC LẬP ===");
    let allPassed = true;
    for (const t of testCases) {
        const timeStr = `${t.h.toString().padStart(2, '0')}:${t.m.toString().padStart(2, '0')}`;
        const result = getHourChi(t.h, t.m);
        const pass = result === t.expected;
        if (!pass) allPassed = false;
        
        console.log(`[${timeStr}] ${t.desc} -> Trả về: ${result} | Kì vọng: ${t.expected} -> ${pass ? "KHỚP" : "LỖI"}`);
    }

    console.log(`\nTổng kết: ${allPassed ? "PASS 100%" : "CÓ LỖI"}`);

    // NHẮC NHỞ VỀ SỬ DỤNG THƯ VIỆN LUNAR_DATE_VI:
    /*
     * CHÚ Ý QUAN TRỌNG KHI TÍCH HỢP VÀO AN SAO ENGINE:
     * - Thư viện npm 'lunar-date-vi' CHỈ ĐƯỢC PHÉP DÙNG để chuyển đổi Ngày/Tháng/Năm Dương <-> Âm.
     * - KHÔNG ĐƯỢC DÙNG thư viện lunar-date-vi để tính Giờ Âm Lịch (hàm getHourName()) do đã
     *   xác nhận lỗi hardcode trả về giờ Tý cho mọi thời điểm.
     * - Khi cần an cung theo giờ, BẮT BUỘC dùng hàm getHourChi() tự viết tay ở trên.
     */
}

runTest();
