# PRODUCT REQUIREMENTS DOCUMENT (PRD)

## DỰ ÁN: NutriSync (Giai đoạn 1 - Food Vision Nutrition Parser)
* **Tên đề tài:** Nghiên cứu và xây dựng pipeline trích xuất thông tin dinh dưỡng món ăn Việt Nam từ hình ảnh sử dụng mô hình thị giác ngôn ngữ (Food Vision Nutrition Parser)
* **Trạng thái:** Bản thảo kỹ thuật (Draft)
* **Thời gian lập:** Tháng 11/2026
* **Tài liệu tham khảo:** `Project_Concept_NutriSync.pdf`

---

## 1. TỔNG QUAN & BỐI CẢNH (EXECUTIVE SUMMARY)

### 1.1. Bối cảnh bài toán
Kiểm soát năng lượng và thành phần dinh dưỡng (Calories & Macro) là nhu cầu cốt lõi của người tập luyện, giảm cân hoặc theo dõi bệnh lý. Tuy nhiên, các ứng dụng hiện hành (MyFitnessPal, Lose It) có tỷ lệ người dùng bỏ cuộc sau 1–2 tuần rất cao (> 90%) do thao tác ghi chép thủ công (cân đo từng gram, tìm kiếm thủ công tên nguyên liệu) tốn quá nhiều thời gian.

### 1.2. Thách thức ẩm thực Việt Nam
* **Cấu trúc phức hợp:** Món ăn Việt thường ở dạng trộn hoặc ngập nước dùng (bún, phở, hủ tiếu, cơm tấm sườn bì chả), khác biệt hoàn toàn với món ăn đĩa đơn lẻ phương Tây.
* **Calo tàng hình (Invisible Calories):** Dầu mỡ, nước mắm pha đường, nước màu, tóp mỡ ngấm sâu trong thực phẩm, không thể nhìn thấy đầy đủ qua camera 2D.
* **Thiếu chuẩn hóa:** Không có công thức chế biến mẫu số chung giữa các hàng quán vỉa hè.

### 1.3. Mục tiêu của Giai đoạn 1 (Core Scope)
Xây dựng một **Pipeline trích xuất dinh dưỡng bán tự động (Semi-automated Food Vision Nutrition Pipeline)** từ ảnh chụp điện thoại cho món ăn Việt Nam, kết hợp sức mạnh nhận diện của VLM (Vision-Language Model) với cơ chế xác nhận tinh giản của người dùng (Human-in-the-loop) và công thức dinh dưỡng chuẩn hóa.

---

## 2. PHÂN ĐỊNH PHẠM VI (SCOPE DEFINITION)

### 2.1. Trong phạm vi (In-Scope - Giai đoạn 1)
* **Frontend Mobile-First Web App:** Cho phép chụp hoặc tải ảnh món ăn từ camera điện thoại.
* **Quy trình tiền xử lý ảnh:** Tối ưu hóa kích thước, chuyển đổi định dạng WebP để giảm độ trễ upload.
* **Bộ suy luận VLM có cấu trúc (Structured VLM Engine):** Tích hợp Gemini-2.5-Flash / Gemini-3.8-Flash (chính) và cơ chế Fallback sang GPT-4o-mini (hoặc model kế nhiệm) khi lỗi; ép kiểu đầu ra thông qua JSON Schema / Pydantic.
* **Cơ chế phân giải dinh dưỡng 2 tầng (Two-stage Nutrition Resolver):** VLM nhận diện món và thành phần định tính $\rightarrow$ Hệ thống tra cứu bảng công thức chuẩn (Nutrition Reference DB) để suy ra dải calo (Range estimation: min - nominal - max).
* **Giao diện Human-in-the-loop tinh giản:** Cho phép người dùng điều chỉnh nhanh theo kích thước định tính (Nhỏ / Vừa / Lớn) và bật/tắt các topping thêm.
* **Cơ sở dữ liệu người dùng:** Lưu trữ lịch sử các bữa ăn trong ngày và thống kê tổng calo/macro (PostgreSQL / SQLite).
* **Bộ khung đánh giá thực nghiệm (Benchmark):** Đo lường độ trễ (latency), độ chính xác nhận diện món và sai số calo trên tập ảnh Ground Truth.

### 2.2. Ngoài phạm vi (Out-of-Scope - Dành cho Future Work)
* Thuật toán gợi ý món ăn theo vị trí định vị GPS (Hyper-local Recommender).
* Tích hợp đồng bộ thiết bị đeo thông minh (Wearable tracking qua Google Health Connect / Apple Health).
* Tự động dựng hình 3D (3D Mesh Reconstruction) để tính thể tích đĩa thức ăn.

---

## 3. CHÂN DUNG NGƯỜI DÙNG & HÀNH TRÌNH TRẢI NGHIỆM (USER JOURNEY)

### 3.1. Đối tượng sử dụng chính
* Người đang trong chế độ ăn kiêng, tập gym hoặc kiểm soát cân nặng tại Việt Nam, thường xuyên ăn ngoài hàng quán hoặc ăn cơm gia đình.
* Cần biết tương đối lượng calo nạp vào hằng ngày nhưng không có thời gian cân đo từng lạng thực phẩm.

### 3.2. Luồng trải nghiệm người dùng (Happy Path)
1. **Chụp ảnh:** Người dùng mở ứng dụng web trên điện thoại, bấm nút "Quét bữa ăn", chụp ảnh đĩa thức ăn.
2. **Xử lý nền & Hiển thị trạng thái:** Ứng dụng nén ảnh nhẹ, gửi lên server; màn hình hiển thị hiệu ứng quét (radar scanning) với thời gian phản hồi kỳ vọng 2.0 – 3.5s.
3. **Màn hình xác nhận (Human-in-the-loop):**
   * Hiển thị: Tên món (ví dụ: *Cơm tấm sườn*), kèm dải calo ước tính: *520 – 650 kcal*.
   * Người dùng chọn nhanh khẩu phần: `[ Nhỏ ]` | `[ Vừa ]` | `[ Lớn ]`.
   * Người dùng bật/tắt topping thấy trên bàn ăn: `[✓ Thêm trứng ốp la]`, `[ ] Thêm chả chưng]`.
4. **Lưu trữ:** Người dùng bấm "Xác nhận & Lưu", dữ liệu cộng dồn vào thanh tiến trình calo trong ngày.

---

## 4. YÊU CẦU CHỨC NĂNG (FUNCTIONAL REQUIREMENTS)

| Mã | Chức năng | Chi tiết kỹ thuật |
| :--- | :--- | :--- |
| **FR-01** | Tiếp nhận & Nén ảnh Client-side | • Hỗ trợ camera trực tiếp qua HTML5 Media Capture.<br>• Nén sơ bộ bằng Canvas/WebWorker trước khi gửi request `POST /api/v1/meals/scan`. |
| **FR-02** | Tiền xử lý ảnh Server-side | • Chuẩn hóa kích thước: Cạnh dài tối đa 1024px.<br>• Chuyển định dạng sang WebP, chất lượng 80%, dung lượng $\le 300\text{KB}$. |
| **FR-03** | Trích xuất VLM có cấu trúc | • Áp dụng Strategy Pattern gọi Gemini Flash làm mô hình chính.<br>• Fallback sang GPT-4o-mini khi gặp lỗi API/Timeout > 3.5s.<br>• Ép kiểu nghiêm ngặt bằng Pydantic v2 Schema. |
| **FR-04** | Suy luận Dinh dưỡng 2 tầng | • Nhận mã món (`dish_id`) từ VLM, tra cứu vào `nutrition_ref.json`.<br>• Tính toán dải calo (Min / Nominal / Max) theo phân loại (món khô $\pm 12\%$, món nước $\pm 20\%$). |
| **FR-05** | Tương tác Human-in-the-loop | • Cho phép sửa tên món qua autocomplete dropdown nếu AI nhận diện nhầm.<br>• Cho phép đổi hệ số khẩu phần (0.8x / 1.0x / 1.3x).<br>• Tự động tính lại calo trên UI mà không cần gọi lại AI. |
| **FR-06** | Lưu trữ nhật ký bữa ăn | • Lưu thông tin bữa ăn (timestamp, tên món, calo chốt, macro, link ảnh/thumbnail) vào PostgreSQL/SQLite. |
| **FR-07** | Thực nghiệm & Đánh giá | • Script chạy batch test trên tập ảnh Ground Truth.<br>• Đo đạc Top-1 Accuracy, MAE calo, MAPE (%) và phân rã độ trễ (latency breakdown). |

---

## 5. YÊU CẦU PHI CHỨC NĂNG (NON-FUNCTIONAL REQUIREMENTS)

1. **Hiệu năng & Độ trễ (Performance & Latency):**
   * Độ trễ toàn trình (Client chụp $\rightarrow$ Render kết quả xác nhận): Mục tiêu $P_{50} \le 2.5\text{s}$, $P_{95} \le 4.5\text{s}$.
2. **Độ tin cậy & Chống lỗi vỡ cấu trúc (Reliability & Schema Safety):**
   * Tỷ lệ lỗi gãy parse JSON từ VLM phải $< 1\%$. Mọi phản hồi không hợp lệ từ model chính phải được bắt lại và chuyển tiếp sang fallback provider hoặc thông báo lỗi thân thiện.
3. **Hiệu quả Chi phí (Cost Efficiency):**
   * Chi phí AI trung bình cho mỗi lượt quét ảnh: $\le 0.0008\text{ USD}$ (~20 VNĐ).
4. **Tính minh bạch về sai số (Uncertainty Transparency):**
   * Không bao giờ hiển thị một con số calo tuyệt đối cố định nếu độ tin cậy thấp. Luôn hiển thị kèm dải sai số và ghi chú cảnh báo (ví dụ: món nước, món ngập dầu).

---

## 6. THIẾT KẾ DATA CONTRACT (PYDANTIC SCHEMA)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "VLMMealAnalysis",
  "type": "object",
  "properties": {
    "dish_id": {
      "type": "string",
      "description": "Mã định danh món ăn chuẩn snake_case khớp với CSDL dinh dưỡng, ví dụ: com_tam_suon, pho_bo_tai"
    },
    "dish_name": {
      "type": "string",
      "description": "Tên tiếng Việt hoàn chỉnh của món ăn"
    },
    "dish_type": {
      "type": "string",
      "enum": ["dry_dish", "soup_dish", "drink", "snack"],
      "description": "Phân loại tính chất món ăn để áp dụng biên độ dung sai calo"
    },
    "detected_portion": {
      "type": "string",
      "enum": ["small", "standard", "large"],
      "description": "Kích thước ước lượng từ ảnh 2D"
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Độ tự tin nhận diện món"
    },
    "components": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "estimated_gram": {"type": ["integer", "null"]}
        },
        "required": ["name"]
      }
    },
    "modifiers_detected": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Danh sách các phụ gia/topping nhận diện được: them_trung, them_mo_hanh, nuoc_beo..."
    },
    "uncertainty_notes": {
      "type": ["string", "null"],
      "description": "Lưu ý nếu có thành phần chìm hoặc bị che khuất"
    }
  },
  "required": ["dish_id", "dish_name", "dish_type", "detected_portion", "confidence", "components"]
}
```

---

## 7. RỦI RO & PHƯƠNG ÁN GIẢM THIỂU (RISKS & MITIGATION)

| Rủi ro kỹ thuật / Thực tế | Mức độ | Phương án xử lý trong thiết kế |
| :--- | :---: | :--- |
| **VLM Hallucination về calo:** VLM tự bịa ra số calo phi thực tế cho món Việt. | Cao | **Tách biệt 2 tầng:** VLM chỉ làm nhiệm vụ nhận diện món/thành phần định tính. Calo được tính toán từ bảng chuẩn `nutrition_ref.json`. |
| **Món nước (phở, bún) chìm dưới đáy:** Không nhìn thấy lượng bún/thịt thực tế. | Cao | Phân loại `soup_dish`, mở rộng dải ước tính lên $\pm 20\%$, hiển thị cảnh báo để người dùng tự điều chỉnh kích thước tô nếu cần. |
| **Độ trễ mạng 4G/Wifi:** Upload ảnh độ phân giải cao mất nhiều giây. | Trung bình | Nén ảnh WebP $\le 300\text{KB}$ ngay trên trình duyệt trước khi gửi request. |
| **Thiếu dữ liệu Ground Truth:** Khó đánh giá khoa học cho báo cáo đề tài. | Cao | Xây dựng bộ test set tối thiểu 60 mẫu được cân đo thực tế ngay từ Giai đoạn 0, không dùng dataset có sẵn thiếu nhãn calo. |
| **Vòng đời API GPT-4o-mini (Shutdown 01/2027):** Mô hình fallback bị ngừng hoạt động. | Trung bình | Dùng Strategy Pattern và cấu hình tên model qua biến môi trường `.env`, sẵn sàng chuyển đổi sang model kế nhiệm. |

---

## 8. CÁC CỘT MỐC ĐÁNH GIÁ (ACCEPTANCE CRITERIA)

* [ ] Pipeline hoạt động thông suốt từ upload ảnh $\rightarrow$ VLM $\rightarrow$ Resolver $\rightarrow$ DB.
* [ ] Tỷ lệ nhận diện đúng tên món (Top-1 Accuracy) $\ge 80\%$ trên tập test món Việt phổ biến.
* [ ] Sai số calo trung bình (MAPE) đạt $\le 15\%$ đối với nhóm món khô và $\le 25\%$ đối với nhóm món nước.
* [ ] Thời gian xử lý trung bình toàn hệ thống $P_{50} \le 3.0\text{s}$.
* [ ] 100% request không bị sập do lỗi định dạng dữ liệu (nhờ Pydantic Validation & Fallback Strategy).

