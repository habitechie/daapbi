# HƯỚNG DẪN KIẾN TRÚC CI/CD ĐA DỰ ÁN & CHUYỂN ĐỔI HẠ TẦNG $0 CHO DAAPBI.COM

Tài liệu kỹ thuật dành cho Kỹ sư dữ liệu (Data Engineer) quản trị hệ sinh thái `daapbi.com`.

---

## 1. CẤU TRÚC KHO MÃ NGUỒN ĐA DỰ ÁN (MONOREPO)

Thay vì tạo nhiều kho mã nguồn (repository) rời rạc khó đồng bộ, toàn bộ hệ sinh thái `daapbi.com` được tổ chức theo cấu trúc **Monorepo** tinh gọn:

```text
daapbi_monorepo/
├── .github/
│   └── workflows/
│       ├── deploy_landing.yml       # Tự động đẩy trang chủ daapbi.com lên Cloudflare Pages
│       ├── test_micro_saas.yml      # Tự động kiểm thử cú pháp và chất lượng mã nguồn Python
│       └── daily_auto_update.yml    # Chạy cron hàng ngày (8:00 sáng) ghi nhận nhật ký hệ thống
├── projects/
│   ├── landing_daapbi/              # Trang chủ tĩnh (HTML/Tailwind) cho daapbi.com ($0 hosting)
│   │   └── index.html
│   ├── micro_saas_inventory/        # Web app dự báo tồn kho & cháy hàng (Streamlit Python)
│   │   ├── app.py
│   │   └── requirements.txt
│   └── micro_saas_reconciliation/   # Công cụ đối soát đơn hàng đa sàn (Mở rộng trong tương lai)
├── docs/
│   ├── ARCHITECTURE_AND_MIGRATION_GUIDE.md
│   └── DAILY_LOG.md
└── README.md
```

### Cách thức hoạt động của luồng CI/CD:
1. **Bộ lọc đường dẫn (Path Filtering):** Khi bạn chỉnh sửa mã nguồn trong thư mục `projects/landing_daapbi/`, chỉ có luồng `deploy_landing.yml` được kích hoạt. Ngược lại, khi sửa code Python trong `projects/micro_saas_...`, chỉ có luồng kiểm thử `test_micro_saas.yml` chạy. Điều này giúp tiết kiệm tài nguyên và thời gian build tối đa.
2. **Triển khai ứng dụng Streamlit tự động:** [Streamlit Community Cloud](https://streamlit.io/cloud) được kết nối trực tiếp với nhánh `main` của repo này. Khi bạn cập nhật file `projects/micro_saas_inventory/app.py`, Streamlit sẽ tự động phát hiện và khởi động lại ứng dụng trên tên miền con `app.daapbi.com` chỉ sau vài giây.
3. **Cơ chế cập nhật tự động hàng ngày:** Luồng `daily_auto_update.yml` được cấu hình lịch trình định kỳ (Cron: `0 1 * * *` tương ứng 8:00 sáng giờ Việt Nam) để tự động chạy các bài kiểm tra sức khỏe hệ thống và ghi nhận nhật ký vận hành.

---

## 2. GIẢI PHÁP $0 THAY THẾ BỀN VỮNG CHO EASYWP (NAMECHEAP)

Gói dùng thử EasyWP chỉ miễn phí 1 tháng đầu (sau đó tính phí $2.91 – $8.88/tháng). Với mục tiêu bắt đầu bằng **chi phí 0 đồng bền vững**, bạn nên chuyển đổi trang web sang nền tảng **Cloudflare Pages** theo 3 bước sau:

### So sánh Giải pháp:
| Tiêu chí | Namecheap EasyWP (Trial 1 tháng) | Cloudflare Pages + Streamlit ($0 Vĩnh viễn) |
| :--- | :--- | :--- |
| **Chi phí hàng tháng** | Tốn phí sau 30 ngày ($35 – $100/năm) | **$0 / tháng vĩnh viễn** |
| **Băng thông & Lưu lượng** | Bị giới hạn dung lượng hosting | **Không giới hạn băng thông** |
| **Bảo mật & Chứng chỉ SSL** | Cần gia hạn chứng chỉ định kỳ | **Tự động cấp SSL miễn phí 100%** |
| **Tốc độ tải trang** | Chạy máy chủ đơn lẻ (dễ nghẽn) | **Mạng lưới phân phối toàn cầu (Edge CDN)** |
| **Rủi ro mã độc** | Dễ bị tấn công vào lỗ hổng WordPress | **Trang tĩnh (Static), miễn nhiễm tấn công CMS** |

### Các bước chuyển đổi cấu hình tên miền:
1. **Bước 1 — Đưa mã nguồn lên GitHub:** Đẩy toàn bộ thư mục `daapbi_monorepo` lên một kho lưu trữ riêng trên GitHub của bạn.
2. **Bước 2 — Kết nối với Cloudflare Pages:**
   - Đăng nhập vào trang quản trị [Cloudflare](https://dash.cloudflare.com/), chọn mục **Workers & Pages** -> **Create application** -> **Pages** -> **Connect to Git**.
   - Chọn repository `daapbi_monorepo`, thiết lập thư mục build (`Build output directory`) là: `projects/landing_daapbi`.
   - Nhấn **Save and Deploy**. Cloudflare sẽ tạo cho bạn một đường link miễn phí dạng `daapbi.pages.dev`.
3. **Bước 3 — Trỏ tên miền `daapbi.com` từ Namecheap về Cloudflare Pages:**
   - Trong trang quản trị dự án Cloudflare Pages, vào tab **Custom Domains** -> Nhập `daapbi.com`.
   - Vào tài khoản Namecheap (nơi bạn mua tên miền), chuyển phần Nameservers từ *Namecheap BasicDNS* sang *Custom DNS* và điền 2 địa chỉ Nameserver do Cloudflare cung cấp.
   - Hủy kích hoạt gói EasyWP trial trên Namecheap để không bị tự động trừ tiền thẻ tín dụng sau 30 ngày.

---

## 3. LÀM RÕ VẤN ĐỀ NGHIÊN CỨU THỊ TRƯỜNG: VÌ SAO CHỌN "CHÁY HÀNG & TỒN KHO CHẾT"?

### Nhìn nhận khách quan về 2 liên kết nghiên cứu trước đó:
Trong 2 bài viết từ [Holistics eCommerce Analytics](https://www.holistics.io/blog/ecommerce-analytics-tools/) và [Luca AI](https://ask-luca.com/blogs/best-predictive-analytics-tools-for-ecommerce), các nền tảng này là các hệ thống BI doanh nghiệp toàn diện (Enterprise/Mid-market BI) trị giá từ **$800/tháng** trở lên, bao gồm hàng chục tính năng phức tạp như Customer Churn, Multi-touch Attribution, Cohort Analysis và Lifetime Value. Trong các bài viết đó, vấn đề tồn kho chỉ được nhắc đến dưới dạng khái niệm tổng quát:
- *"Demand Forecasting: Predict trends to avoid running out of stock—or sitting on unsold inventory"* (Dự báo nhu cầu: để tránh hết hàng hoặc đọng hàng tồn chưa bán được).
- *"Inventory Management: Monitor stock levels, turnover rates, and dead stock"* (Quản trị kho: theo dõi mức tồn, tốc độ vòng quay và tồn kho chết).

### Chiến lược Micro-SaaS: "Xẻ nhỏ phần mềm lớn" (The Unbundling Strategy)
Một lập trình viên độc lập (Solo Founder / Data Engineer) **không thể và không nên** cố gắng xây dựng một bản sao hoàn chỉnh của Holistics hay Power BI với 50 tính năng. Thay vào đó, chiến lược thành công nhất trong thế giới Micro-SaaS là **Unbundling**:
1. **Quy mô thiệt hại thực tế của thị trường:** Theo nghiên cứu thường niên của tổ chức nghiên cứu bán lẻ toàn cầu [IHL Group - 2026 Inventory Distortion Study](https://www.ihlservices.com/product/inventory-distortion-study-2026/), sự méo mó trong quản trị kho hàng (bao gồm **Out-of-stocks: Cháy hàng** và **Overstocks: Thừa ứ đọng vốn**) gây thiệt hại tới **1,7 nghìn tỷ USD mỗi năm**, tương đương **6,2% - 6,5% tổng doanh thu bán lẻ toàn cầu** ([IHL Group Research](https://www.ihlservices.com/news/ihl-research-findings/)).
2. **Khoảng trống thị trường cho SME:** Các phần mềm lớn (ERP, NetSuite, SAP, Holistics) quá đắt đỏ và phức tạp đối với chủ shop vừa và nhỏ bán hàng trên Shopee/TikTok/Lazada. Chủ shop chỉ cần một công cụ giải quyết đúng 1 việc trong 30 giây:
   - *Tính giúp tôi khi nào cần đặt hàng lại để không bị đứt hàng mùa sale (Reorder Point).*
   - *Chỉ ra giúp tôi những mã hàng nào đang nằm im trong kho trên 90 ngày làm nghẽn dòng tiền.*
3. **Giá trị chuyển đổi của `daapbi.com`:** Bằng cách cung cấp công cụ tính toán Reorder Point & Deadstock hoàn toàn miễn phí trên `app.daapbi.com`, chúng ta giải quyết trực diện "nỗi đau nhức nhối nhất", từ đó tạo phễu thu hút khách hàng mua bộ mẫu Dashboard chuyên sâu ($25) hoặc thuê dịch vụ tư vấn kỹ thuật dữ liệu của bạn.
