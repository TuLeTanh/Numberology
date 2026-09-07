const { SolarDate, LunarDate } = require("./lunar-date/dist/index.cjs");

function runTest() {
    console.log("=== BẮT ĐẦU TEST BỔ SUNG ===");

    // 2. Mở rộng round-trip test lên tối thiểu 8 ngày biên khác nhau
    console.log("\n--- TEST CASE C: ROUND-TRIP NGÀY BIÊN (2023-2026) ---");
    let boundaryDates = [];
    
    // Quét toàn bộ ngày để tự động tìm ngày biên (ngày ngay trước mùng 1)
    let d = new Date(2023, 0, 1);
    const endDate = new Date(2026, 11, 31);
    while (d <= endDate) {
        const nextDay = new Date(d);
        nextDay.setDate(nextDay.getDate() + 1);
        
        const solarNext = new SolarDate(nextDay);
        const lunarNext = solarNext.toLunarDate();
        
        if (lunarNext.day === 1) {
            // Hôm nay là ngày cuối tháng âm lịch
            const solarToday = new SolarDate(new Date(d));
            const lunarToday = solarToday.toLunarDate();
            boundaryDates.push({ solar: solarToday, lunar: lunarToday });
            if (boundaryDates.length >= 8) break; // Lấy 8 ngày biên đầu tiên
        }
        
        d.setDate(d.getDate() + 1);
    }

    let allBoundaryPass = true;
    for (const b of boundaryDates) {
        const solarRevert = b.lunar.toSolarDate();
        const pass = b.solar.day === solarRevert.day && 
                     b.solar.month === solarRevert.month && 
                     b.solar.year === solarRevert.year;
        
        const typeStr = b.lunar.day === 30 ? "Tháng đủ (30)" : "Tháng thiếu (29)";
        const leapStr = b.lunar.leap_month ? "[NHUẬN]" : "";
        console.log(`Âm: ${b.lunar.day}/${b.lunar.month}/${b.lunar.year} ${leapStr} ${typeStr} -> Dương gốc: ${b.solar.day}/${b.solar.month}/${b.solar.year} | Ngược lại: ${solarRevert.day}/${solarRevert.month}/${solarRevert.year} -> ${pass ? "KHỚP" : "LỆCH"}`);
        if (!pass) allBoundaryPass = false;
    }

    // 3. Test phần chuyển đổi Giờ sinh sang giờ Chi
    console.log("\n--- TEST CASE D: CHUYỂN ĐỔI GIỜ SINH SANG CHI (TÝ, NGỌ) ---");
    const testDate = new SolarDate(new Date(2023, 1, 1)).toLunarDate();
    console.log(`Lấy thông tin giờ của ngày: ${testDate.day}/${testDate.month}/${testDate.year}`);
    
    // Gọi thử hàm getHourName
    try {
        const hourName = testDate.getHourName();
        console.log(`- Kết quả getHourName() không truyền tham số: "${hourName}"`);
        
        // Thử xem hàm có nhận tham số không
        const hourNameNgo = testDate.getHourName(12); // thử truyền 12h (Ngọ)
        console.log(`- Kết quả getHourName(12) [Thử truyền giờ Ngọ]: "${hourNameNgo}"`);
        
        if (hourNameNgo.includes("Ngọ") || hourNameNgo.includes("ngọ")) {
            console.log("-> CÓ hỗ trợ giờ Ngọ.");
        } else {
            console.log("-> LỖI: Thư viện trả về cùng 1 kết quả, không hỗ trợ nhập giờ để lấy Can Chi tương ứng.");
        }
    } catch (e) {
        console.log("Lỗi khi chạy getHourName:", e.message);
    }
}

runTest();
