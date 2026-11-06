# PRODUCT BACKLOG - NUTRISYNC (PHIÊN BẢN v1)

## DỰ ÁN: NutriSync - Food Vision Nutrition Parser (Giai đoạn 1)
* **Phiên bản:** v1.0.0-beta
* **Trạng thái:** Đang triển khai (In Progress - Sprint 1)
* **Thời gian dự kiến hoàn thành:** 4 – 5 tuần
* **Tài liệu liên quan:** [PRD_NutriSync_Phase1.md](PRD_NutriSync_Phase1.md)

---

## BẢNG TỔNG QUAN TIẾN ĐỘ THEO GIAI ĐOẠN (SPRINT MILESTONES)

| Giai đoạn (Milestone) | Trọng tâm công việc | Số lượng Task | Thời gian dự kiến | Trạng thái |
| :--- | :--- | :---: | :---: | :---: |
| **Giai đoạn 0 (Sprint 1)** | Dữ liệu Dinh dưỡng Tham chiếu & Bộ ảnh Benchmark | 3 Tasks | Tuần 1 | `[x] Hoàn thành (3/3)` |
| **Giai đoạn 1 (Sprint 2)** | AI Core, Pydantic Schema & Prompt Engineering | 4 Tasks | Tuần 2 | `[>] Sẵn sàng triển khai` |
| **Giai đoạn 2 (Sprint 3)** | Xây dựng Backend Pipeline (FastAPI) & Resolver | 5 Tasks | Tuần 3 | `[ ] Chưa bắt đầu` |
| **Giai đoạn 3 (Sprint 4)** | Xây dựng Frontend Mobile Web & Human-in-the-Loop | 4 Tasks | Tuần 4 | `[ ] Chưa bắt đầu` |
| **Giai đoạn 4 (Sprint 5)** | Chạy Thực nghiệm, Đo Sai số & Đóng gói Báo cáo | 3 Tasks | Tuần 5 | `[ ] Chưa bắt đầu` |

---

## CHI TIẾT CÁC TASKS THEO TỪNG GIAI ĐOẠN

---

### GIAI ĐOẠN 0: DỮ LIỆU THAM CHIẾU & BENCHMARK (DATA FOUNDATION) - `[x] Hoàn thành (3/3)`
> **Mục tiêu:** Tạo "thước đo chuẩn" (Ground Truth) để thẩm định độ chính xác của AI ngay từ đầu, tránh tình trạng phát triển xong nhưng không có căn cứ đánh giá.

#### - [x] `TASK-0.1`: Chuẩn hóa danh mục 30 món ăn Việt Nam & lập bảng FCT
* **Mô tả:** Lọc ra 30 món ăn phổ biến (15 món khô/đĩa, 12 món nước, 3 món cuốn/ăn nhẹ). Thu thập số liệu calo, protein, carb, fat tiêu chuẩn cho từng món theo tài liệu Viện Dinh Dưỡng hoặc công thức chuẩn hóa.
* **Đầu ra (Deliverable):** File `backend/app/data/nutrition_ref.json`.
* **Tiêu chí hoàn thành (DoD):**
  - Đủ 30 món ăn có cấu trúc JSON hợp lệ.
  - Mỗi món có đủ: calo cơ sở, tỷ lệ macro (P/C/F), hệ số khẩu phần (small: 0.8, standard: 1.0, large: 1.3), và danh sách topping phổ biến kèm calo cộng thêm.
* **Thời gian ước tính:** 2 ngày.
* **Phụ thuộc:** Không.

#### - [x] `TASK-0.2`: Thu thập bộ dữ liệu kiểm thử (Ground Truth Dataset)
* **Mô tả:** Thu thập tập 60 ảnh thực tế (khoảng 2 ảnh/món với các góc chụp khác nhau: 45 độ và 90 độ thẳng đứng). Cân đo khối lượng thực tế từng món ăn bằng cân tiểu ly điện tử.
* **Đầu ra (Deliverable):** 
  - Thư mục ảnh `evaluation/dataset/images/` (60 ảnh).
  - File nhãn `evaluation/dataset/ground_truth.json` chứa: `image_name`, `true_dish_id`, `true_calories`, `true_portion`.
* **Tiêu chí hoàn thành (DoD):** 100% ảnh có nhãn ground truth về calo thực tế được ghi nhận chính xác.
* **Thời gian ước tính:** 3 ngày.
* **Phụ thuộc:** `TASK-0.1`.

#### - [x] `TASK-0.3`: Viết script kiểm tra tính hợp lệ của dữ liệu tham chiếu
* **Mô tả:** Viết script unit test kiểm tra xem file `nutrition_ref.json` có bị thiếu trường dữ liệu, sai kiểu dữ liệu hoặc calo âm hay không.
* **Đầu ra (Deliverable):** `backend/tests/test_nutrition_data.py`.
* **Tiêu chí hoàn thành (DoD):** Chạy `pytest` kiểm tra 100% bản ghi hợp lệ.
* **Thời gian ước tính:** 0.5 ngày.
* **Phụ thuộc:** `TASK-0.1`.

---

### GIAI ĐOẠN 1: AI CORE & PROMPT ENGINEERING
> **Mục tiêu:** Đảm bảo VLM nhận diện đúng món ăn Việt Nam và 100% trả về đúng định dạng JSON có cấu trúc.

#### - [ ] `TASK-1.1`: Thiết kế Data Contract (Pydantic v2 Models)
* **Mô tả:** Xây dựng toàn bộ các schema dữ liệu đầu vào/đầu ra giữa Client, Backend và AI Core bằng Pydantic v2.
* **Đầu ra (Deliverable):** `backend/app/models/schemas.py`.
* **Tiêu chí hoàn thành (DoD):**
  - Chứa đầy đủ: `PortionSizeEnum`, `DishTypeEnum`, `DetectedComponent`, `VLMMealAnalysis`, `ScanResponse`, `ConfirmMealRequest`.
  - Có validation chặt chẽ cho confidence (từ 0.0 đến 1.0).
* **Thời gian ước tính:** 1 ngày.
* **Phụ thuộc:** `TASK-0.1`.

#### - [ ] `TASK-1.2`: Xây dựng System Prompt chuyên sâu ẩm thực Việt Nam
* **Mô tả:** Thiết kế prompt hướng dẫn mô hình nhận diện đặc trưng món Việt (phân biệt bún chả vs bún thịt nướng, nhận diện mỡ hành, tóp mỡ, nước béo, phân loại `soup_dish` vs `dry_dish`).
* **Đầu ra (Deliverable):** `backend/app/core/prompts.py`.
* **Tiêu chí hoàn thành (DoD):** Prompt súc tích, tối ưu token, có ví dụ Few-shot định dạng JSON mẫu.
* **Thời gian ước tính:** 1 ngày.
* **Phụ thuộc:** `TASK-1.1`.

#### - [ ] `TASK-1.3`: Xây dựng VLM Engine với Strategy Pattern & Fallback
* **Mô tả:** Tạo interface `BaseVLMProvider`. Viết implementation cho mô hình chính `GeminiFlashProvider` (dùng SDK `google-genai` mới với Structured Output) và `OpenAIProvider` (`gpt-4o-mini` hoặc model kế nhiệm) để fallback.
* **Đầu ra (Deliverable):** `backend/app/services/vlm_engine.py`.
* **Tiêu chí hoàn thành (DoD):**
  - Khi Gemini gặp lỗi mạng hoặc timeout > 3.5s, hệ thống tự động kích hoạt OpenAI fallback trong cùng 1 request mà không làm crash app.
* **Thời gian ước tính:** 2 ngày.
* **Phụ thuộc:** `TASK-1.1`, `TASK-1.2`.

#### - [ ] `TASK-1.4`: Script kiểm thử độc lập AI Core (Offline Batch Test)
* **Mô tả:** Viết script chạy thử AI Core trên 10 bức ảnh đầu tiên từ dataset để đo thời gian phản hồi và tỷ lệ parse schema thành công.
* **Đầu ra (Deliverable):** `evaluation/scripts/test_vlm_standalone.py`.
* **Tiêu chí hoàn thành (DoD):** Tỷ lệ parse Pydantic schema thành công đạt 100% trên 10 ảnh mẫu.
* **Thời gian ước tính:** 0.5 ngày.
* **Phụ thuộc:** `TASK-1.3`.

---

### GIAI ĐOẠN 2: XÂY DỰNG BACKEND PIPELINE (FASTAPI)
> **Mục tiêu:** Hoàn thiện pipeline từ tiếp nhận ảnh, nén, gọi AI Core, tính toán dải calo cho đến lưu trữ CSDL.

#### - [ ] `TASK-2.1`: Module Tiền xử lý & Nén ảnh phía Server (Image Service)
* **Mô tả:** Nhận file upload từ request, kiểm tra định dạng MIME, resize cạnh dài tối đa 1024px và nén chuyển đổi sang định dạng WebP (chất lượng 80%, dung lượng $\le 300\text{KB}$).
* **Đầu ra (Deliverable):** `backend/app/services/image_service.py`.
* **Tiêu chí hoàn thành (DoD):**
  - Chuyển đổi mọi định dạng ảnh hợp lệ (JPEG, PNG, HEIC) sang WebP.
  - Dung lượng file sau nén luôn $\le 300\text{KB}$.
* **Thời gian ước tính:** 1 ngày.
* **Phụ thuộc:** Không.

#### - [ ] `TASK-2.2`: Module Suy luận Dinh dưỡng 2 tầng (Deterministic Resolver)
* **Mô tả:** Nhận object `VLMMealAnalysis` từ AI Core, tra cứu `dish_id` trong `nutrition_ref.json`, áp dụng hệ số khẩu phần và cộng dồn calo topping; tính dải calo (món khô $\pm 12\%$, món nước $\pm 20\%$).
* **Đầu ra (Deliverable):** `backend/app/services/nutrition_service.py`.
* **Tiêu chí hoàn thành (DoD):**
  - Tính đúng công thức toán học, không bịa số.
  - Trả về đúng dải `min_kcal`, `nominal_kcal`, `max_kcal` và tổng macro (P/C/F).
* **Thời gian ước tính:** 1.5 ngày.
* **Phụ thuộc:** `TASK-0.1`, `TASK-1.1`.

#### - [ ] `TASK-2.3`: Xây dựng Endpoints API Quét món & Xác nhận
* **Mô tả:** Tạo router FastAPI tiếp nhận request:
  - `POST /api/v1/meals/scan`: Nhận file ảnh $\rightarrow$ Nén $\rightarrow$ AI Core $\rightarrow$ Resolver $\rightarrow$ Trả kết quả dự kiến.
  - `POST /api/v1/meals/confirm`: Nhận dữ liệu người dùng đã chỉnh sửa $\rightarrow$ Lưu vào database.
* **Đầu ra (Deliverable):** `backend/app/api/endpoints/meals.py`.
* **Tiêu chí hoàn thành (DoD):** Endpoints phản hồi mã HTTP chuẩn (200, 201, 400, 422, 500), có xử lý lỗi thân thiện.
* **Thời gian ước tính:** 1.5 ngày.
* **Phụ thuộc:** `TASK-2.1`, `TASK-2.2`, `TASK-1.3`.

#### - [ ] `TASK-2.4`: Thiết lập CSDL Người dùng & Nhật ký bữa ăn (Persistence Layer)
* **Mô tả:** Thiết lập SQLite (cho dev/test) hoặc PostgreSQL (cho production) bằng SQLAlchemy v2. Tạo bảng `meal_logs` và `daily_summaries`.
* **Đầu ra (Deliverable):** `backend/app/core/database.py`, `backend/app/models/db_models.py`.
* **Tiêu chí hoàn thành (DoD):** Thực hiện được các thao tác CRUD cơ bản: lưu bữa ăn mới, lấy danh sách bữa ăn trong ngày, tính tổng calo ngày.
* **Thời gian ước tính:** 1.5 ngày.
* **Phụ thuộc:** `TASK-2.3`.

#### - [ ] `TASK-2.5`: Unit Tests & Integration Tests toàn bộ Backend
* **Mô tả:** Viết test tự động cho toàn bộ luồng Backend bằng `pytest` và `httpx.AsyncClient`.
* **Đầu ra (Deliverable):** `backend/tests/test_api_flow.py`.
* **Tiêu chí hoàn thành (DoD):** Code coverage đạt $\ge 80\%$ cho các services và endpoints.
* **Thời gian ước tính:** 1 ngày.
* **Phụ thuộc:** `TASK-2.3`, `TASK-2.4`.

---

### GIAI ĐOẠN 3: FRONTEND MOBILE WEB & HUMAN-IN-THE-LOOP
> **Mục tiêu:** Xây dựng giao diện web tối ưu cho màn hình di động, thao tác chụp ảnh và xác nhận món ăn trong vòng 5 giây.

#### - [ ] `TASK-3.1`: Khởi tạo dự án Frontend & Cấu hình Mobile-First UI
* **Mô tả:** Khởi tạo Web App (Next.js / React + Tailwind CSS), cấu hình layout tối ưu cho màn hình điện thoại (viewport, touch friendly, mobile navbar).
* **Đầu ra (Deliverable):** Toàn bộ thư mục `frontend/`.
* **Tiêu chí hoàn thành (DoD):** Ứng dụng chạy mượt mà trên trình duyệt di động (Chrome/Safari trên iOS và Android).
* **Thời gian ước tính:** 1 ngày.
* **Phụ thuộc:** Không.

#### - [ ] `TASK-3.2`: Module Chụp ảnh từ Camera & Nén Client-side
* **Mô tả:** Tích hợp Media Capture API để mở camera điện thoại trực tiếp. Sử dụng Canvas/WebWorker để nén ảnh sơ bộ trước khi gửi lên Backend.
* **Đầu ra (Deliverable):** `frontend/src/components/CameraCapture.tsx`, `frontend/src/services/imageCompression.ts`.
* **Tiêu chí hoàn thành (DoD):**
  - Chụp ảnh và hiển thị preview tức thì.
  - Nén ảnh client-side xuống $\le 500\text{KB}$ trong thời gian $< 500\text{ms}$.
* **Thời gian ước tính:** 1.5 ngày.
* **Phụ thuộc:** `TASK-3.1`.

#### - [ ] `TASK-3.3`: Giao diện Xác nhận Khẩu phần (Human-in-the-Loop UI)
* **Mô tả:** Màn hình hiển thị kết quả phân tích:
  - Tên món ăn (kèm nút sửa nhanh nếu AI nhận diện nhầm).
  - Selector chọn khẩu phần trực quan: `[ Nhỏ ]` | `[ Vừa ]` | `[ Lớn ]`.
  - Toggle list chọn nhanh topping: `[✓ Thêm trứng]`, `[ ] Nước béo]`.
  - Hiển thị dải calo tự động nhảy số theo lựa chọn của người dùng.
* **Đầu ra (Deliverable):** `frontend/src/components/MealReviewCard.tsx`.
* **Tiêu chí hoàn thành (DoD):** Người dùng có thể hoàn thành việc chọn khẩu phần và bấm "Lưu" trong vòng 3 thao tác chạm.
* **Thời gian ước tính:** 2 ngày.
* **Phụ thuộc:** `TASK-3.1`, `TASK-2.3`.

#### - [ ] `TASK-3.4`: Trang Nhật ký Bữa ăn & Tổng kết Dinh dưỡng Ngày
* **Mô tả:** Màn hình Dashboard hiển thị danh sách các bữa ăn đã quét trong ngày, thanh tiến trình calo nạp vào so với mục tiêu, biểu đồ tỷ lệ Macro (Protein/Carb/Fat).
* **Đầu ra (Deliverable):** `frontend/src/components/DailyLogDashboard.tsx`.
* **Tiêu chí hoàn thành (DoD):** Cập nhật dữ liệu thời gian thực ngay sau khi người dùng lưu bữa ăn thành công.
* **Thời gian ước tính:** 1.5 ngày.
* **Phụ thuộc:** `TASK-3.3`, `TASK-2.4`.

---

### GIAI ĐOẠN 4: ĐÁNH GIÁ THỰC NGHIỆM & BÁO CÁO KHOA HỌC
> **Mục tiêu:** Thu thập số liệu đo lường định lượng thực tế để viết báo cáo đề tài có căn cứ khoa học vững chắc.

#### - [ ] `TASK-4.1`: Xây dựng Framework Benchmark tự động
* **Mô tả:** Viết script Python tự động nạp 60 ảnh từ `evaluation/dataset/`, gửi qua pipeline, ghi nhận kết quả và so sánh với `ground_truth.json`.
* **Đầu ra (Deliverable):** `evaluation/scripts/run_benchmark.py`.
* **Tiêu chí hoàn thành (DoD):** Tự động xuất ra file kết quả `evaluation/results_benchmark.json` chứa thông tin từng mẫu chạy.
* **Thời gian ước tính:** 1.5 ngày.
* **Phụ thuộc:** `TASK-0.2`, `TASK-2.3`.

#### - [ ] `TASK-4.2`: Tính toán & Trực quan hóa các chỉ số đo lường (Metrics)
* **Mô tả:** Viết script tính toán:
  - Top-1 Accuracy (Tỷ lệ nhận diện đúng tên món).
  - Phân rã độ trễ (Latency $P_{50}$, $P_{95}$).
  - Sai số calo trung bình (MAE) và sai số phần trăm trung bình (MAPE) phân tách theo 2 nhóm: Món khô vs Món nước.
  - Vẽ biểu đồ phân bố sai số calo bằng `matplotlib` / `seaborn`.
* **Đầu ra (Deliverable):** `evaluation/scripts/generate_report_charts.py`, thư mục chứa biểu đồ `evaluation/charts/`.
* **Tiêu chí hoàn thành (DoD):** Có đầy đủ các bảng số liệu và biểu đồ để đưa trực tiếp vào báo cáo/slide thuyết trình.
* **Thời gian ước tính:** 1 ngày.
* **Phụ thuộc:** `TASK-4.1`.

#### - [ ] `TASK-4.3`: Hoàn thiện Báo cáo Nghiên cứu & Hướng dẫn Sử dụng
* **Mô tả:** Tổng hợp toàn bộ số liệu thực nghiệm vào báo cáo đề tài, phân tích trung thực các trường hợp thất bại (failure cases) do calo tàng hình/món ngập nước, hoàn thiện README hướng dẫn cài đặt.
* **Đầu ra (Deliverable):** `docs/EXPERIMENTAL_RESULTS.md`, cập nhật `README.md`.
* **Tiêu chí hoàn thành (DoD):** Tài liệu hoàn chỉnh, sẵn sàng bảo vệ đề tài trước hội đồng thẩm định.
* **Thời gian ước tính:** 2 ngày.
* **Phụ thuộc:** `TASK-4.2`.

---

## MA TRẬN PHÂN CHIA TRÁCH NHIỆM & ƯU TIÊN (PRIORITY MATRIX)

```text
[MỨC ĐỘ ƯU TIÊN CAO NHẤT - LÀM TRƯỚC]:
├── TASK-0.1: Bảng CSDL Dinh dưỡng chuẩn (nutrition_ref.json)
├── TASK-1.1: Pydantic Data Contract (schemas.py)
├── TASK-1.3: VLM Engine (Gemini Flash + Fallback)
└── TASK-2.2: Deterministic Nutrition Resolver (nutrition_service.py)

[MỨC ĐỘ ƯU TIÊN TRUNG BÌNH - HOÀN THIỆN SẢN PHẨM]:
├── TASK-2.1: Module nén WebP server-side
├── TASK-2.3: Endpoints FastAPI (/scan & /confirm)
├── TASK-3.2: Module Camera & nén client-side
└── TASK-3.3: Giao diện xác nhận Human-in-the-loop

[MỨC ĐỘ ĐO LƯỜNG & CHỨNG MINH KHOA HỌC]:
├── TASK-0.2: Tập ảnh Ground Truth cân đo thực tế
├── TASK-4.1: Script chạy benchmark tự động
└── TASK-4.2: Tính toán chỉ số MAE/MAPE và vẽ biểu đồ báo cáo
```

