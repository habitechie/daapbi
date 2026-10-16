"""
DAAPBI.COM - Micro-SaaS Tool: SME Inventory Velocity & Deadstock Health Checker
Deploy: Streamlit Community Cloud (app.daapbi.com/inventory) | Cost: $0
"""

import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="DAAPBI | Quản trị Tồn kho & Dự báo Hết hàng", layout="wide")
st.title("📦 DAAPBI.COM — Phân tích Tốc độ Bán & Cảnh báo Cháy hàng / Đọng vốn")

st.markdown(
    "Công cụ hỗ trợ chủ shop E-commerce & SME bán lẻ phân tích file xuất kho/bán hàng để tự động "
    "tính số ngày tồn kho khả dụng, phân loại SKU ma trận ABC và phát hiện nguy cơ cháy hàng hoặc tồn kho chết."
)

with st.sidebar:
    st.header("🚀 Hệ sinh thái DAAPBI.COM")
    st.markdown("- **Trang chủ:** [daapbi.com](https://daapbi.com)")
    st.markdown("- **Tải Template Looker Studio Quản trị Tồn kho ($25):** [Gumroad](https://gumroad.com/pricing)")
    st.markdown("---")
    st.markdown("- [Tự động gửi cảnh báo tồn kho qua Telegram với Make.com (Hoa hồng 35%)](https://www.make.com/en/affiliate)")
    st.markdown("- [Tự động hóa luồng dữ liệu kho với n8n Cloud (Hoa hồng 30%)](https://n8n.io/affiliates/)")
    st.markdown("- [Khóa học Quản trị Dữ liệu & Chuỗi cung ứng trên DataCamp](https://www.datacamp.com/affiliates)")

uploaded_file = st.file_uploader("Tải lên file CSV dữ liệu bán hàng & tồn kho (hoặc trải nghiệm dữ liệu mẫu)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    sample_csv = io.StringIO(
        "sku,product_name,stock_qty,daily_sales_avg,lead_time_days,unit_cost\n"
        "SKU-A101,Nồi chiên không dầu 5L,12,3.5,7,450000\n"
        "SKU-A102,Máy xay sinh tố cầm tay,5,2.0,10,210000\n"
        "SKU-B201,Bình giữ nhiệt inox 800ml,85,1.2,5,85000\n"
        "SKU-C301,Hộp đựng thực phẩm thủy tinh,210,0.2,14,35000\n"
        "SKU-C302,Kẹp miệng túi snack đa năng,450,0.1,7,12000\n"
    )
    df = pd.read_csv(sample_csv)

required = {"sku", "product_name", "stock_qty", "daily_sales_avg", "lead_time_days", "unit_cost"}
if required.issubset(set(df.columns)):
    df["days_of_inventory"] = (df["stock_qty"] / df["daily_sales_avg"].replace(0, 0.001)).round(1)
    df["reorder_point"] = (df["daily_sales_avg"] * df["lead_time_days"] * 1.3).round(0)
    df["capital_tied_up"] = df["stock_qty"] * df["unit_cost"]

    def classify_status(row):
        if row["stock_qty"] <= row["reorder_point"]:
            return "🚨 Cảnh báo: Sắp cháy hàng (Cần đặt ngay)"
        elif row["days_of_inventory"] > 120:
            return "⚠️ Đọng vốn / Tồn kho chết (Cần xả hàng)"
        else:
            return "✅ Mức tồn kho an toàn"

    df["inventory_health"] = df.apply(classify_status, axis=1)

    c1, c2, c3 = st.columns(3)
    c1.metric("Tổng vốn đang đọng kho", f"{df['capital_tied_up'].sum():,.0f} VND")
    c2.metric("Số SKU sắp cháy hàng", len(df[df["inventory_health"].str.contains("Cảnh báo")]))
    c3.metric("Số SKU đọng vốn (>120 ngày)", len(df[df["inventory_health"].str.contains("Đọng vốn")]))

    st.dataframe(df[["sku", "product_name", "stock_qty", "days_of_inventory", "reorder_point", "inventory_health", "capital_tied_up"]], use_container_width=True)

    csv_out = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Xuất Báo cáo Tồn kho Đã phân tích (CSV)", csv_out, "daapbi_inventory_report.csv", "text/csv")
