# NutriSync - Food Vision Nutrition Parser (Giai đoạn 1)

Dự án nghiên cứu và xây dựng pipeline trích xuất thông tin dinh dưỡng món ăn Việt Nam từ hình ảnh sử dụng mô hình thị giác ngôn ngữ (VLM).

---

## Cấu trúc thư mục dự án

```text
Nutri_Sync/
├── docs/                                # Tài liệu dự án & nghiên cứu
│   ├── PRD_NutriSync_Phase1.md          # Tài liệu yêu cầu sản phẩm (PRD) chi tiết
│   └── BACKLOG_v1.md                    # Backlog và danh sách task triển khai chi tiết
│
├── backend/                             # Dịch vụ Backend (FastAPI)
│   ├── app/
│   │   ├── api/                         # Endpoints (Route nhận diện /api/v1/meals/scan)
│   │   ├── core/                        # Cấu hình hệ thống (Settings, Security)
│   │   ├── models/                      # Pydantic Schemas & Database Models
│   │   ├── services/                    # Logic tiền xử lý ảnh, VLM Engine, Nutrition Resolver
│   │   └── data/                        # CSDL Dinh dưỡng chuẩn hóa (nutrition_ref.json)
│   └── tests/                           # Unit tests & Integration tests
│
├── frontend/                            # Giao diện Web di động (Mobile-First Web App)
│   └── src/
│       ├── components/                  # Giao diện Camera, Slider, Confirmation UI
│       ├── services/                    # Xử lý nén ảnh client-side & gọi API
│       └── types/                       # TypeScript interfaces
│
└── evaluation/                          # Bộ đo lường & Đánh giá thực nghiệm
    ├── dataset/                         # Ảnh thử nghiệm + Ground Truth metadata
    └── scripts/                         # Script đo Latency, Accuracy, Sai số calo (MAE/MAPE)
```

## Tài liệu chi tiết
- **[Tài liệu Yêu cầu Sản phẩm (PRD)](docs/PRD_NutriSync_Phase1.md)**: Chi tiết bài toán, phạm vi, kiến trúc hệ thống và chỉ số nghiệm thu.
- **[Backlog Triển khai v1 (Backlog & Tasks)](docs/BACKLOG_v1.md)**: Danh sách công việc phân rã theo 5 giai đoạn, tiêu chí hoàn thành (DoD) và ma trận ưu tiên.

