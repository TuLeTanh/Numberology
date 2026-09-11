// Địa chỉ backend API (có thể thay đổi linh hoạt)
const API_BASE = "http://localhost:8000";

// Biến toàn cục lưu kết quả /lasso đã tính để dùng cho /hoi (stateless client side)
let currentLassoData = null;

// Tọa độ 12 Cung trên bàn cờ 4x4 truyền thống của Tử Vi Đẩu Số
// Chiều thuận: Dần (4,1) -> Mão (3,1) -> Thìn (2,1) -> Tỵ (1,1) -> Ngọ (1,2) -> Mùi (1,3) -> Thân (1,4) -> Dậu (2,4) -> Tuất (3,4) -> Hợi (4,4) -> Tý (4,3) -> Sửu (4,2)
const PALACE_GRID_POSITIONS = {
  "Tỵ":   { row: 1, col: 1 },
  "Ngọ":  { row: 1, col: 2 },
  "Mùi":  { row: 1, col: 3 },
  "Thân": { row: 1, col: 4 },
  "Dậu":  { row: 2, col: 4 },
  "Tuất": { row: 3, col: 4 },
  "Hợi":  { row: 4, col: 4 },
  "Tý":   { row: 4, col: 3 },
  "Sửu":  { row: 4, col: 2 },
  "Dần":  { row: 4, col: 1 },
  "Mão":  { row: 3, col: 1 },
  "Thìn": { row: 2, col: 1 }
};

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("lasso-form");
  const btnSubmit = document.getElementById("btn-submit");
  const btnText = btnSubmit.querySelector(".btn-text");
  const btnLoader = btnSubmit.querySelector(".btn-loader");
  const apiError = document.getElementById("api-error");
  const resultContainer = document.getElementById("result-container");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearErrors();

    // 1. Thu thập dữ liệu
    const hoTen = document.getElementById("ho_ten").value.trim();
    const ngaySinh = document.getElementById("ngay_sinh").value.trim();
    const thangSinh = document.getElementById("thang_sinh").value.trim();
    const namSinh = document.getElementById("nam_sinh").value.trim();
    const gioSinh = document.getElementById("gio_sinh").value.trim();
    const phutSinh = document.getElementById("phut_sinh").value.trim();
    const gioiTinh = document.getElementById("gioi_tinh").value;

    // 2. Client-side Validation
    let isValid = true;

    if (!hoTen) {
      showFieldError("error-ho_ten", "Vui lòng nhập họ và tên khai sinh.");
      isValid = false;
    }

    const d = parseInt(ngaySinh, 10);
    if (isNaN(d) || d < 1 || d > 31) {
      showFieldError("error-ngay_sinh", "Ngày sinh phải từ 1 đến 31.");
      isValid = false;
    }

    const m = parseInt(thangSinh, 10);
    if (isNaN(m) || m < 1 || m > 12) {
      showFieldError("error-thang_sinh", "Tháng sinh phải từ 1 đến 12.");
      isValid = false;
    }

    const y = parseInt(namSinh, 10);
    if (isNaN(y) || y < 1900 || y > 2100) {
      showFieldError("error-nam_sinh", "Năm sinh phải từ 1900 đến 2100.");
      isValid = false;
    }

    const h = parseInt(gioSinh, 10);
    if (isNaN(h) || h < 0 || h > 23) {
      showFieldError("error-gio_sinh", "Giờ sinh phải từ 0 đến 23.");
      isValid = false;
    }

    const p = parseInt(phutSinh, 10);
    if (isNaN(p) || p < 0 || p > 59) {
      showFieldError("error-phut_sinh", "Phút sinh phải từ 0 đến 59.");
      isValid = false;
    }

    if (!isValid) return;

    const payload = {
      ho_ten: hoTen,
      ngay_sinh: d,
      thang_sinh: m,
      nam_sinh: y,
      gio_sinh: h,
      phut_sinh: p,
      gioi_tinh: gioiTinh
    };

    // 3. Gọi Backend API /lasso
    setLoading(true);
    apiError.style.display = "none";

    try {
      const response = await fetch(`${API_BASE}/lasso`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        let errDetail = "Không thể kết nối đến máy chủ.";
        try {
          const errData = await response.json();
          errDetail = errData.detail || JSON.stringify(errData);
        } catch (_) {}
        throw new Error(errDetail);
      }

      const data = await response.json();
      currentLassoData = data; // Lưu lại kết quả để dùng cho /hoi, tránh gọi lại /lasso

      // 4. Render kết quả
      renderTuViBoard(data);
      renderNumerology(data.than_so_hoc);

      resultContainer.style.display = "block";
      resultContainer.scrollIntoView({ behavior: "smooth" });

    } catch (err) {
      console.error("Lỗi khi lập lá số:", err);
      apiError.textContent = `Lỗi: ${err.message}`;
      apiError.style.display = "block";
    } finally {
      setLoading(false);
    }
  });

  function showFieldError(elementId, msg) {
    const el = document.getElementById(elementId);
    if (el) el.textContent = msg;
  }

  function clearErrors() {
    document.querySelectorAll(".field-error").forEach((el) => {
      el.textContent = "";
    });
    apiError.style.display = "none";
  }

  function setLoading(loading) {
    if (loading) {
      btnSubmit.disabled = true;
      btnText.style.display = "none";
      btnLoader.style.display = "inline";
    } else {
      btnSubmit.disabled = false;
      btnText.style.display = "inline";
      btnLoader.style.display = "none";
    }
  }

  // ── Render Bảng 12 Cung Tử Vi (Grid 4x4) ──
  function renderTuViBoard(data) {
    const board = document.getElementById("tuvi-board");
    board.innerHTML = "";

    const tuVi = data.tu_vi;
    const personal = data.thong_tin_ca_nhan;
    const bang12 = tuVi.bang_12_cung || {};

    // 1. Tạo ô Trung Cung (Thiên Bàn) ở vị trí row 2..3, col 2..3
    const centerCell = document.createElement("div");
    centerCell.className = "center-cell";

    const amLich = tuVi.am_lich || {};
    const leapStr = amLich.nhuan ? " (Nhuận)" : "";

    centerCell.innerHTML = `
      <div class="center-title">THIÊN BÀN</div>
      <div class="center-info-grid">
        <div class="center-item"><strong>Họ tên:</strong> <span>${personal.ho_ten}</span></div>
        <div class="center-item"><strong>Dương lịch:</strong> <span>${personal.ngay_thang_nam_sinh}</span></div>
        <div class="center-item"><strong>Âm lịch:</strong> <span>Ngày ${amLich.ngay} tháng ${amLich.thang}${leapStr} năm ${amLich.nam}</span></div>
        <div class="center-item"><strong>Giờ sinh:</strong> <span>Giờ ${tuVi.gio_chi}</span></div>
        <div class="center-item"><strong>Cục:</strong> <span>${tuVi.cuc}</span></div>
        <div class="center-item"><strong>Cung Mệnh:</strong> <span>${tuVi.cung_menh}</span></div>
        <div class="center-item"><strong>Cung Thân:</strong> <span>Thân cư ${tuVi.cung_than}</span></div>
      </div>
    `;
    board.appendChild(centerCell);

    console.log("=== RAW BANG_12_CUNG ===");
    console.log(JSON.stringify(bang12, null, 2));

    const appliedPositions = {};

    // 2. Tạo 12 ô Cung viền ngoài
    for (const [tenCung, info] of Object.entries(bang12)) {
      const diaChi = info.dia_chi;
      const can = info.can || "";
      const pos = PALACE_GRID_POSITIONS[diaChi];
      if (!pos) continue;

      appliedPositions[tenCung] = { dia_chi: diaChi, row: pos.row, col: pos.col };

      const isMenh = (tenCung === "Mệnh");
      const isThan = (tuVi.cung_than === diaChi);

      const cell = document.createElement("div");
      cell.className = `palace-cell${isMenh ? " is-menh" : ""}${isThan ? " is-than" : ""}`;
      cell.style.gridRow = pos.row;
      cell.style.gridColumn = pos.col;

      // Danh sách chính tinh có tag Tứ Hóa
      let chinhTinhHtml = "";
      if (info.chinh_tinh && info.chinh_tinh.length > 0) {
        chinhTinhHtml = info.chinh_tinh.map(item => {
          let tuHoaBadge = "";
          if (item.tu_hoa) {
            const hoaClass = item.tu_hoa.replace(/\s+/g, "");
            tuHoaBadge = `<span class="tu-hoa-tag tu-hoa-${hoaClass}">[${item.tu_hoa}]</span>`;
          }
          return `<div class="chinh-tinh-item"><span>${item.sao}</span>${tuHoaBadge}</div>`;
        }).join("");
      } else {
        chinhTinhHtml = `<div class="chinh-tinh-item" style="color: var(--text-dim); font-weight: normal; font-size: 0.85rem;">(Vô chính diệu)</div>`;
      }

      // Danh sách phụ tinh
      let phuTinhHtml = "";
      if (info.phu_tinh && info.phu_tinh.length > 0) {
        phuTinhHtml = info.phu_tinh.map(sao => {
          let extraClass = "";
          if (["Kình Dương", "Đà La", "Hỏa Tinh", "Linh Tinh", "Địa Không", "Địa Kiếp"].includes(sao)) {
            extraClass = " phu-tinh-sat";
          } else if (["Tuần Không", "Triệt Không"].includes(sao)) {
            extraClass = " phu-tinh-tuan-triet";
          }
          return `<span class="phu-tinh-item${extraClass}">${sao}</span>`;
        }).join(", ");
      }

      cell.innerHTML = `
        <div class="palace-header">
          <div class="palace-title-group">
            <span class="palace-name">${tenCung}</span>
            ${isMenh ? `<span class="badge-menh">MỆNH</span>` : ""}
            ${isThan ? `<span class="badge-than">THÂN</span>` : ""}
          </div>
          <div class="palace-canchi">${can} ${diaChi}</div>
        </div>
        <div class="palace-stars">
          <div class="chinh-tinh-list">
            ${chinhTinhHtml}
          </div>
          ${phuTinhHtml ? `<div class="phu-tinh-list">${phuTinhHtml}</div>` : ""}
        </div>
      `;

      // Thêm sự kiện click để xem diễn giải chi tiết (/dien-giai-cung)
      cell.addEventListener("click", () => {
        openPalaceModal(tenCung, can, diaChi);
      });

      board.appendChild(cell);
    }

    console.log("=== 12 PALACE GRID POSITIONS APPLIED ===");
    console.log(JSON.stringify(appliedPositions, null, 2));

    console.log("=== RAW RENDERED HTML OF TUVI-BOARD ===");
    console.log(board.innerHTML);
  }

  // ── Render 4 Chỉ số Thần Số Học ──
  function renderNumerology(thanSoHoc) {
    const grid = document.getElementById("numerology-grid");
    grid.innerHTML = "";

    if (!thanSoHoc) return;

    const cardsData = [
      { key: "duong_doi", title: "Số Đường Đời (Life Path)", data: thanSoHoc.duong_doi },
      { key: "su_menh", title: "Số Sứ Mệnh (Destiny)", data: thanSoHoc.su_menh },
      { key: "linh_hon", title: "Số Linh Hồn (Soul Urge)", data: thanSoHoc.linh_hon },
      { key: "nhan_cach", title: "Số Nhân Cách (Personality)", data: thanSoHoc.nhan_cach }
    ];

    cardsData.forEach(card => {
      const info = card.data || {};
      const cardEl = document.createElement("div");
      cardEl.className = "numerology-card";

      const dg = info.dien_giai || {};
      let bodyHtml = "";

      if (typeof dg === "string") {
        bodyHtml = `<p>${dg}</p>`;
      } else if (typeof dg === "object") {
        if (dg.y_nghia_tong_quat) {
          bodyHtml += `<p><strong>Ý nghĩa:</strong> ${dg.y_nghia_tong_quat}</p>`;
        }
        if (dg.diem_manh) {
          bodyHtml += `<p><strong>Điểm mạnh:</strong> ${dg.diem_manh}</p>`;
        }
        if (dg.diem_yeu) {
          bodyHtml += `<p><strong>Điểm yếu:</strong> ${dg.diem_yeu}</p>`;
        }
        if (dg.nang_khieu) {
          bodyHtml += `<p><strong>Năng khiếu:</strong> ${dg.nang_khieu}</p>`;
        }
        if (dg.dinh_huong_nghe_nghiep) {
          bodyHtml += `<p><strong>Nghề nghiệp phù hợp:</strong> ${dg.dinh_huong_nghe_nghiep}</p>`;
        }
        if (dg.khao_khat_ben_trong) {
          bodyHtml += `<p><strong>Khao khát:</strong> ${dg.khao_khat_ben_trong}</p>`;
        }
        if (dg.dong_luc_noi_tam) {
          bodyHtml += `<p><strong>Động lực nội tâm:</strong> ${dg.dong_luc_noi_tam}</p>`;
        }
        if (dg.an_tuong_ben_ngoai) {
          bodyHtml += `<p><strong>Ấn tượng bên ngoài:</strong> ${dg.an_tuong_ben_ngoai}</p>`;
        }
        if (dg.cach_nguoi_khac_nhin_nhan) {
          bodyHtml += `<p><strong>Góc nhìn xã hội:</strong> ${dg.cach_nguoi_khac_nhin_nhan}</p>`;
        }
      }

      cardEl.innerHTML = `
        <div class="card-header">
          <span class="card-title">${card.title}</span>
          <span class="card-number">${info.gia_tri !== undefined ? info.gia_tri : "-"}</span>
        </div>
        <div class="card-body">
          ${bodyHtml || "<p style='color: var(--text-dim);'>Chưa có mô tả diễn giải.</p>"}
        </div>
      `;

      grid.appendChild(cardEl);
    });
  }

  // ── Xử lý khung chat Hỏi Đáp (/hoi) ──
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const btnChatSend = document.getElementById("btn-chat-send");
  const btnChatText = btnChatSend.querySelector(".btn-chat-text");
  const btnChatLoader = btnChatSend.querySelector(".btn-chat-loader");
  const chatHistory = document.getElementById("chat-history");

  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const cauHoi = chatInput.value.trim();
    if (!cauHoi) return; // Validate: không gửi câu hỏi rỗng

    if (!currentLassoData) {
      appendChatMessage("bot", "Vui lòng lập lá số trước khi đặt câu hỏi!", "error-message");
      return;
    }

    // 1. Thêm câu hỏi của user vào khung chat
    appendChatMessage("user", cauHoi);
    chatInput.value = "";

    // 2. Tạo placeholder đang trả lời & disable nút gửi
    setChatLoading(true);
    const loadingMessageEl = appendChatMessage("bot", "Đang tra cứu dữ liệu & luận giải...", "loading-message");

    try {
      const tuVi = currentLassoData.tu_vi || {};
      const payloadHoi = {
        cau_hoi: cauHoi,
        muoi_hai_cung: tuVi.muoi_hai_cung || null,
        chinh_tinh: tuVi["14_chinh_tinh"] || tuVi.chinh_tinh || null,
        tu_hoa: tuVi.tu_hoa || null,
        than_so_hoc: currentLassoData.than_so_hoc || null
      };

      console.log("=== SENDING TO /hoi ===");
      console.log(JSON.stringify(payloadHoi, null, 2));

      const res = await fetch(`${API_BASE}/hoi`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payloadHoi)
      });

      if (!res.ok) {
        let errDetail = `Lỗi máy chủ (${res.status})`;
        try {
          const errJson = await res.json();
          errDetail = errJson.detail || JSON.stringify(errJson);
        } catch (_) {}
        throw new Error(errDetail);
      }

      const result = await res.json();
      console.log("=== RESPONSE FROM /hoi ===");
      console.log(JSON.stringify(result, null, 2));

      // Xóa loading placeholder và chèn câu trả lời thật
      loadingMessageEl.remove();
      appendChatMessage("bot", result.tra_loi || "Không nhận được phản hồi phù hợp.");

    } catch (err) {
      console.error("Lỗi khi gọi /hoi:", err);
      loadingMessageEl.remove();
      appendChatMessage("bot", `Lỗi: ${err.message}`, "error-message");
    } finally {
      setChatLoading(false);
      chatInput.focus();
    }
  });

  function setChatLoading(loading) {
    if (loading) {
      btnChatSend.disabled = true;
      btnChatText.style.display = "none";
      btnChatLoader.style.display = "inline";
    } else {
      btnChatSend.disabled = false;
      btnChatText.style.display = "inline";
      btnChatLoader.style.display = "none";
    }
  }

  function appendChatMessage(sender, text, extraClass = "") {
    const msgEl = document.createElement("div");
    msgEl.className = `chat-message ${sender}-message ${extraClass}`.trim();

    const senderTitle = sender === "user" ? "Bạn" : "Trợ lý Luận Giải";
    msgEl.innerHTML = `
      <div class="message-sender">${senderTitle}:</div>
      <div class="message-content">${escapeChatText(text)}</div>
    `;

    chatHistory.appendChild(msgEl);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return msgEl;
  }

  function escapeChatText(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;")
      .replace(/\n/g, "<br>");
  }

  // ── Xử lý Modal Diễn Giải Chi Tiết Cung (/dien-giai-cung) ──
  const palaceModal = document.getElementById("palace-modal");
  const modalPalaceTitle = document.getElementById("modal-palace-title");
  const modalBody = document.getElementById("modal-body");
  const btnModalClose = document.getElementById("btn-modal-close");

  async function openPalaceModal(tenCung, can, diaChi) {
    if (!currentLassoData) return;

    modalPalaceTitle.textContent = `Cung ${tenCung} (${can} ${diaChi})`;
    modalBody.innerHTML = `<div class="modal-loading">Đang tải diễn giải chi tiết cung ${tenCung}...</div>`;
    palaceModal.style.display = "flex";

    try {
      const tuVi = currentLassoData.tu_vi || {};
      const payload = {
        ten_cung: tenCung,
        muoi_hai_cung: tuVi.muoi_hai_cung || {},
        chinh_tinh: tuVi["14_chinh_tinh"] || tuVi.chinh_tinh || {},
        tu_hoa: tuVi.tu_hoa || {},
        phu_tinh: tuVi.phu_tinh || {},
        vong_thai_tue: tuVi.vong_thai_tue || {},
        tuan_triet: tuVi.tuan_triet || {},
        dao_hong_hi: tuVi.dao_hong_hi || {},
        quang_quy: tuVi.quang_quy || {},
        khoc_hu_co_qua: tuVi.khoc_hu_co_qua || {},
        hinh_rieu_y: tuVi.hinh_rieu_y || {}
      };

      console.log(`=== SENDING TO /dien-giai-cung (Cung ${tenCung}) ===`);
      console.log(JSON.stringify(payload, null, 2));

      const res = await fetch(`${API_BASE}/dien-giai-cung`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        let errDetail = `Lỗi máy chủ (${res.status})`;
        try {
          const errJson = await res.json();
          errDetail = errJson.detail || JSON.stringify(errJson);
        } catch (_) {}
        throw new Error(errDetail);
      }

      const resData = await res.json();
      console.log(`=== RESPONSE FROM /dien-giai-cung (Cung ${tenCung}) ===`);
      console.log(JSON.stringify(resData, null, 2));

      if (resData.sao_va_dien_giai && resData.sao_va_dien_giai.length > 0) {
        const cardsHtml = resData.sao_va_dien_giai.map(item => {
          let tuHoaBadge = "";
          if (item.tu_hoa && item.tu_hoa.length > 0) {
            tuHoaBadge = item.tu_hoa.map(th => {
              const c = th.replace(/\s+/g, "");
              return `<span class="tu-hoa-tag tu-hoa-${c}">[${th}]</span>`;
            }).join(" ");
          }
          const dgText = item.dien_giai || item.warning || "Chưa có dữ liệu diễn giải chi tiết cho sao này.";
          return `
            <div class="modal-sao-card">
              <div class="modal-sao-header">
                <span class="modal-sao-name">${escapeChatText(item.sao)}</span>
                ${tuHoaBadge}
              </div>
              <div class="modal-sao-dien-giai">${escapeChatText(dgText)}</div>
            </div>
          `;
        }).join("");
        modalBody.innerHTML = cardsHtml;
      } else {
        modalBody.innerHTML = `<p style="color: var(--text-muted); text-align: center; padding: 24px;">Cung này không có chính tinh hay phụ tinh nào đóng.</p>`;
      }

    } catch (err) {
      console.error(`Lỗi khi tra cứu cung ${tenCung}:`, err);
      modalBody.innerHTML = `<div class="modal-error">Lỗi khi tải diễn giải: ${escapeChatText(err.message)}</div>`;
    }
  }

  // ── Tính năng Xuất PDF (html2pdf.js) ──
  const btnExportPdfTuVi = document.getElementById("btn-export-pdf-tuvi");
  const btnExportPdfNumerology = document.getElementById("btn-export-pdf-numerology");

  function xuatPdfTuVi() {
    if (!currentLassoData || !currentLassoData.tu_vi) {
      alert("Vui lòng lập lá số trước khi xuất PDF.");
      return;
    }

    if (typeof html2pdf === "undefined") {
      alert("Thư viện xuất PDF chưa sẵn sàng. Vui lòng kiểm tra kết nối mạng.");
      return;
    }

    const personal = currentLassoData.thong_tin_ca_nhan || {};
    const tuVi = currentLassoData.tu_vi || {};
    const amLich = tuVi.am_lich || {};
    const bang12 = tuVi.bang_12_cung || {};

    const safeHoTen = (personal.ho_ten || "Nguoi_Dung").trim().replace(/\s+/g, "_");
    const fileName = `La_So_Tu_Vi_${safeHoTen}.pdf`;

    const palaceOrder = [
      "Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch",
      "Quan Lộc", "Nô Bộc", "Thiên Di", "Tật Ách",
      "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ"
    ];

    let rowsHtml = "";
    palaceOrder.forEach((tenCung, idx) => {
      const info = bang12[tenCung];
      if (!info) return;

      const isMenh = (tenCung === "Mệnh");
      const isThan = (tuVi.cung_than === info.dia_chi);
      let badges = "";
      if (isMenh) badges += ` <span style="background: #b8860b; color: #fff; padding: 2px 5px; font-size: 10px; border-radius: 3px;">MỆNH</span>`;
      if (isThan) badges += ` <span style="background: #4682b4; color: #fff; padding: 2px 5px; font-size: 10px; border-radius: 3px;">THÂN</span>`;

      // Chính tinh & Tứ Hóa
      let ctText = "(Vô chính diệu)";
      if (info.chinh_tinh && info.chinh_tinh.length > 0) {
        ctText = info.chinh_tinh.map(item => {
          let thStr = item.tu_hoa ? ` <b>[${item.tu_hoa}]</b>` : "";
          return `<span style="color: #8b0000; font-weight: bold;">${item.sao}</span>${thStr}`;
        }).join(", ");
      }

      // Phụ tinh & Tuần Triệt
      let ptText = "-";
      if (info.phu_tinh && info.phu_tinh.length > 0) {
        ptText = info.phu_tinh.map(sao => {
          if (["Kình Dương", "Đà La", "Hỏa Tinh", "Linh Tinh", "Địa Không", "Địa Kiếp"].includes(sao)) {
            return `<span style="color: #c0392b;">${sao}</span>`;
          } else if (["Tuần Không", "Triệt Không"].includes(sao)) {
            return `<span style="color: #2980b9; font-weight: bold;">[${sao}]</span>`;
          }
          return `<span>${sao}</span>`;
        }).join(", ");
      }

      const bgColor = idx % 2 === 0 ? "#ffffff" : "#fbf9f4";
      rowsHtml += `
        <tr style="background: ${bgColor}; page-break-inside: avoid;">
          <td style="border: 1px solid #dcd1be; padding: 6px 9px; font-weight: bold; color: #333;">
            ${tenCung} (${info.can || ""} ${info.dia_chi})${badges}
          </td>
          <td style="border: 1px solid #dcd1be; padding: 6px 9px;">
            ${ctText}
          </td>
          <td style="border: 1px solid #dcd1be; padding: 6px 9px; color: #444;">
            ${ptText}
          </td>
        </tr>
      `;
    });

    const printContainer = document.createElement("div");
    printContainer.id = "pdf-temp-container-tuvi";
    printContainer.style.cssText = "width: 780px; background: #ffffff; color: #222; padding: 18px 22px; font-family: 'Be Vietnam Pro', Arial, sans-serif; line-height: 1.35; box-sizing: border-box;";

    printContainer.innerHTML = `
      <div style="text-align: center; border-bottom: 2px solid #8b6508; padding-bottom: 10px; margin-bottom: 14px;">
        <h1 style="margin: 0 0 4px 0; color: #8b6508; font-size: 22px; text-transform: uppercase; letter-spacing: 1px;">Lá Số Tử Vi Đẩu Số</h1>
        <div style="font-size: 12px; color: #666;">Hồ Sơ Mệnh Bàn & Chi Tiết 12 Cung Số</div>
      </div>

      <div style="background: #fdfbf7; border: 1px solid #e5dbca; border-radius: 6px; padding: 10px 14px; margin-bottom: 14px; page-break-inside: avoid;">
        <div style="font-weight: bold; color: #8b6508; margin-bottom: 6px; font-size: 13px; text-transform: uppercase;">Thông Tin Đương Số (Thiên Bàn)</div>
        <table style="width: 100%; font-size: 12px; border-collapse: collapse;">
          <tr>
            <td style="padding: 2px 4px; width: 50%;"><strong>Họ và tên:</strong> ${personal.ho_ten || "-"}</td>
            <td style="padding: 2px 4px; width: 50%;"><strong>Giới tính:</strong> ${personal.gioi_tinh === "nu" ? "Nữ" : "Nam"}</td>
          </tr>
          <tr>
            <td style="padding: 2px 4px;"><strong>Dương lịch:</strong> ${personal.ngay_thang_nam_sinh || "-"}</td>
            <td style="padding: 2px 4px;"><strong>Âm lịch:</strong> Ngày ${amLich.ngay || "-"} tháng ${amLich.thang || "-"}${amLich.nhuan ? " (Nhuận)" : ""} năm ${amLich.nam || "-"}</td>
          </tr>
          <tr>
            <td style="padding: 2px 4px;"><strong>Giờ sinh:</strong> Giờ ${tuVi.gio_chi || "-"}</td>
            <td style="padding: 2px 4px;"><strong>Cục:</strong> ${tuVi.cuc || "-"}</td>
          </tr>
          <tr>
            <td style="padding: 2px 4px;"><strong>Cung Mệnh:</strong> ${tuVi.cung_menh || "-"}</td>
            <td style="padding: 2px 4px;"><strong>Cung Thân:</strong> Thân cư ${tuVi.cung_than || "-"}</td>
          </tr>
        </table>
      </div>

      <div style="font-weight: bold; color: #8b6508; margin: 12px 0 6px 0; font-size: 13px; text-transform: uppercase;">Chi Tiết Toàn Bộ 12 Cung Số</div>
      <table style="width: 100%; border-collapse: collapse; font-size: 11px; margin-bottom: 12px;">
        <thead>
          <tr style="background: #8b6508; color: #ffffff;">
            <th style="border: 1px solid #8b6508; padding: 6px 8px; width: 22%; text-align: left;">Cung Số & Vị Trí</th>
            <th style="border: 1px solid #8b6508; padding: 6px 8px; width: 38%; text-align: left;">Chính Tinh & Tứ Hóa</th>
            <th style="border: 1px solid #8b6508; padding: 6px 8px; width: 40%; text-align: left;">Phụ Tinh / Tuần Triệt</th>
          </tr>
        </thead>
        <tbody>
          ${rowsHtml}
        </tbody>
      </table>

      <div style="font-size: 10px; color: #888; text-align: right; margin-top: 10px; border-top: 1px solid #eee; padding-top: 4px;">
        Tạo tự động từ Hệ thống Tử Vi Đẩu Số &amp; Thần Số Học
      </div>
    `;

    const wrapper = document.createElement("div");
    wrapper.id = "pdf-wrapper-temp-tuvi";
    wrapper.style.cssText = "position: fixed; top: 0; left: 0; width: 780px; height: 0; overflow: hidden; z-index: -9999; pointer-events: none;";
    wrapper.appendChild(printContainer);
    document.body.appendChild(wrapper);

    const opt = {
      margin: 10,
      filename: fileName,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: {
        scale: 2,
        useCORS: true,
        scrollX: 0,
        scrollY: 0
      },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
      pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    };

    btnExportPdfTuVi.disabled = true;
    btnExportPdfTuVi.innerHTML = `<span class="btn-icon">⏳</span> Đang tạo PDF...`;

    const cleanup = () => {
      if (wrapper && wrapper.parentNode) {
        wrapper.parentNode.removeChild(wrapper);
      }
      btnExportPdfTuVi.disabled = false;
      btnExportPdfTuVi.innerHTML = `<span class="btn-icon">📄</span> Tải PDF Lá số Tử Vi`;
    };

    html2pdf().set(opt).from(printContainer).save()
      .then(cleanup)
      .catch(err => {
        cleanup();
        console.error("Lỗi xuất PDF Tử Vi:", err);
        alert("Không thể tạo file PDF. Chi tiết: " + err.message);
      });
  }

  function xuatPdfThanSoHoc() {
    if (!currentLassoData || !currentLassoData.than_so_hoc) {
      alert("Vui lòng lập lá số trước khi xuất PDF.");
      return;
    }

    if (typeof html2pdf === "undefined") {
      alert("Thư viện xuất PDF chưa sẵn sàng. Vui lòng kiểm tra kết nối mạng.");
      return;
    }

    const personal = currentLassoData.thong_tin_ca_nhan || {};
    const tsh = currentLassoData.than_so_hoc || {};

    const safeHoTen = (personal.ho_ten || "Nguoi_Dung").trim().replace(/\s+/g, "_");
    const fileName = `Ho_So_Than_So_Hoc_${safeHoTen}.pdf`;

    const printContainer = document.createElement("div");
    printContainer.id = "pdf-temp-container-tsh";
    printContainer.style.cssText = "width: 780px; margin: 0; background: #ffffff; color: #222; padding: 24px 28px; font-family: 'Be Vietnam Pro', Arial, sans-serif; line-height: 1.6; box-sizing: border-box;";

    const duongDoiVal = tsh.duong_doi && tsh.duong_doi.gia_tri !== undefined ? tsh.duong_doi.gia_tri : "-";
    const suMenhVal = tsh.su_menh && tsh.su_menh.gia_tri !== undefined ? tsh.su_menh.gia_tri : "-";
    const linhHonVal = tsh.linh_hon && tsh.linh_hon.gia_tri !== undefined ? tsh.linh_hon.gia_tri : "-";
    const nhanCachVal = tsh.nhan_cach && tsh.nhan_cach.gia_tri !== undefined ? tsh.nhan_cach.gia_tri : "-";

    printContainer.innerHTML = `
      <div style="text-align: center; border-bottom: 2px solid #8b6508; padding-bottom: 12px; margin-bottom: 20px;">
        <h1 style="margin: 0 0 6px 0; color: #8b6508; font-size: 24px; text-transform: uppercase; letter-spacing: 1px;">Hồ Sơ Thần Số Học</h1>
        <div style="font-size: 13px; color: #666;">Bảng Tổng Hợp Các Chỉ Số Định Danh Cốt Lõi</div>
      </div>

      <div style="background: #fdfbf7; border: 1px solid #e5dbca; border-radius: 8px; padding: 14px 18px; margin-bottom: 22px; page-break-inside: avoid;">
        <div style="font-weight: bold; color: #8b6508; margin-bottom: 8px; font-size: 14px; text-transform: uppercase;">Thông Tin Đương Số</div>
        <div style="font-size: 13.5px; margin-bottom: 5px;"><strong>Họ và tên khai sinh:</strong> ${personal.ho_ten || "-"}</div>
        <div style="font-size: 13.5px;"><strong>Ngày tháng năm sinh:</strong> ${personal.ngay_thang_nam_sinh || "-"}</div>
      </div>

      <div style="font-weight: bold; color: #8b6508; margin-bottom: 10px; font-size: 14px; text-transform: uppercase;">4 Chỉ Số Thần Số Học Cốt Lõi</div>
      <table style="width: 100%; border-collapse: collapse; font-size: 14px; margin-bottom: 22px; page-break-inside: avoid;">
        <thead>
          <tr style="background: #8b6508; color: #ffffff;">
            <th style="border: 1px solid #8b6508; padding: 10px 14px; width: 70%; text-align: left;">Tên Chỉ Số (Core Number)</th>
            <th style="border: 1px solid #8b6508; padding: 10px 14px; width: 30%; text-align: center;">Giá Trị Số</th>
          </tr>
        </thead>
        <tbody>
          <tr style="background: #ffffff;">
            <td style="border: 1px solid #e5dbca; padding: 12px 14px; font-weight: bold; color: #333;">
              Số Đường Đời (Life Path)
            </td>
            <td style="border: 1px solid #e5dbca; padding: 12px 14px; text-align: center; font-size: 20px; font-weight: bold; color: #8b6508;">
              ${duongDoiVal}
            </td>
          </tr>
          <tr style="background: #fbf9f4;">
            <td style="border: 1px solid #e5dbca; padding: 12px 14px; font-weight: bold; color: #333;">
              Số Sứ Mệnh (Destiny)
            </td>
            <td style="border: 1px solid #e5dbca; padding: 12px 14px; text-align: center; font-size: 20px; font-weight: bold; color: #8b6508;">
              ${suMenhVal}
            </td>
          </tr>
          <tr style="background: #ffffff;">
            <td style="border: 1px solid #e5dbca; padding: 12px 14px; font-weight: bold; color: #333;">
              Số Linh Hồn (Soul Urge)
            </td>
            <td style="border: 1px solid #e5dbca; padding: 12px 14px; text-align: center; font-size: 20px; font-weight: bold; color: #8b6508;">
              ${linhHonVal}
            </td>
          </tr>
          <tr style="background: #fbf9f4;">
            <td style="border: 1px solid #e5dbca; padding: 12px 14px; font-weight: bold; color: #333;">
              Số Nhân Cách (Personality)
            </td>
            <td style="border: 1px solid #e5dbca; padding: 12px 14px; text-align: center; font-size: 20px; font-weight: bold; color: #8b6508;">
              ${nhanCachVal}
            </td>
          </tr>
        </tbody>
      </table>

      <div style="font-size: 11px; color: #888; text-align: right; margin-top: 16px; border-top: 1px solid #eee; padding-top: 6px;">
        Tạo tự động từ Hệ thống Tử Vi Đẩu Số &amp; Thần Số Học
      </div>
    `;

    const wrapper = document.createElement("div");
    wrapper.id = "pdf-wrapper-temp-tsh";
    wrapper.style.cssText = "position: fixed; top: 0; left: 0; width: 780px; height: 0; overflow: hidden; z-index: -9999; pointer-events: none;";
    wrapper.appendChild(printContainer);
    document.body.appendChild(wrapper);

    const opt = {
      margin: 10,
      filename: fileName,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: {
        scale: 2,
        useCORS: true,
        scrollX: 0,
        scrollY: 0
      },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
      pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    };

    btnExportPdfNumerology.disabled = true;
    btnExportPdfNumerology.innerHTML = `<span class="btn-icon">⏳</span> Đang tạo PDF...`;

    const cleanup = () => {
      if (wrapper && wrapper.parentNode) {
        wrapper.parentNode.removeChild(wrapper);
      }
      btnExportPdfNumerology.disabled = false;
      btnExportPdfNumerology.innerHTML = `<span class="btn-icon">📄</span> Tải PDF Hồ sơ Thần Số Học`;
    };

    html2pdf().set(opt).from(printContainer).save()
      .then(cleanup)
      .catch(err => {
        cleanup();
        console.error("Lỗi xuất PDF Thần Số Học:", err);
        alert("Không thể tạo file PDF. Chi tiết: " + err.message);
      });
  }

  if (btnExportPdfTuVi) {
    btnExportPdfTuVi.addEventListener("click", xuatPdfTuVi);
  }
  if (btnExportPdfNumerology) {
    btnExportPdfNumerology.addEventListener("click", xuatPdfThanSoHoc);
  }

  function closePalaceModal() {
    palaceModal.style.display = "none";
  }

  btnModalClose.addEventListener("click", closePalaceModal);

  palaceModal.addEventListener("click", (e) => {
    if (e.target === palaceModal) {
      closePalaceModal();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && palaceModal.style.display === "flex") {
      closePalaceModal();
    }
  });
});
