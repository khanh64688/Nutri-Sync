# NutriSync - Food Vision Nutrition Parser (Giai đoạn 1)

Dự án nghiên cứu và xây dựng pipeline trích xuất thông tin dinh dưỡng món ăn Việt Nam từ hình ảnh sử dụng mô hình thị giác ngôn ngữ (VLM).

---

## Cấu trúc thư mục dự án

```text
Nutri_Sync/
├── docs/                                # Tài liệu dự án & nghiên cứu
│   └── PRD_NutriSync_Phase1.md          # Tài liệu yêu cầu sản phẩm (PRD) chi tiết
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
Vui lòng tham khảo tài liệu yêu cầu sản phẩm đầy đủ tại: **[PRD_NutriSync_Phase1.md](docs/PRD_NutriSync_Phase1.md)**.

