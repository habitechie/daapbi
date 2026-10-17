import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="DAAPBI | Bóc Tách ROAS Ảo & Tính MER", layout="wide")
st.title("🎯 DAAPBI.COM — Bóc Tách ROAS Ảo & Tính MER (Marketing Efficiency Ratio)")

st.markdown(
    "Nhiều chủ shop thấy Meta báo ROAS 4.0x, TikTok báo 5.0x nhưng tài khoản ngân hàng vẫn thâm hụt. "
    "Công cụ này giúp bạn đối soát chi phí quảng cáo đa kênh với doanh thu thực tế để tính **MER thực tế** "
    "và phát hiện mức độ **nhận vơ chuyển đổi (Attribution Overlap)** giữa các kênh."
)

with st.sidebar:
    st.header("🚀 Hệ sinh thái DAAPBI.COM")
    st.markdown("- **Trang chủ:** [daapbi.com](https://daapbi.com)")
    st.markdown("- **Tải Template Looker Studio Real ROAS ($29):** [Gumroad](https://gumroad.com/pricing)")
    st.markdown("---")
    st.markdown("- [Tự động gom chi phí Ads đa kênh với Make.com (Hoa hồng 35%)](https://www.make.com/en/affiliate)")
    st.markdown("- [Xây dựng luồng dữ liệu quảng cáo với n8n Cloud (Hoa hồng 30%)](https://n8n.io/affiliates/)")
    st.markdown("- [Khóa học Phân tích Dữ liệu Tiếp thị tại DataCamp](https://www.datacamp.com/affiliates)")

st.subheader("1. Nhập Số Liệu Doanh Thu & Chi Phí Quảng Cáo")
col_a, col_b = st.columns(2)
with col_a:
    actual_revenue = st.number_input("Tổng Doanh thu Thực tế từ Sàn/Tài khoản (VND)", min_value=0, value=120000000, step=5000000)
    cogs_margin_pct = st.slider("Biên lợi nhuận gộp trung bình của sản phẩm (%)", min_value=10, max_value=90, value=50)

with col_b:
    st.markdown("**Chi phí Quảng cáo đã chi tiêu (VND):**")
    meta_spend = st.number_input("Meta Ads Spend", value=18000000, step=1000000)
    tiktok_spend = st.number_input("TikTok Ads Spend", value=12000000, step=1000000)
    google_spend = st.number_input("Google Ads Spend", value=6000000, step=1000000)

st.markdown("**Doanh thu các nền tảng tự báo cáo (Reported Revenue):**")
col_c, col_d, col_e = st.columns(3)
meta_rep_rev = col_c.number_input("Meta báo mang về", value=65000000, step=5000000)
tiktok_rep_rev = col_d.number_input("TikTok báo mang về", value=48000000, step=5000000)
google_rep_rev = col_e.number_input("Google báo mang về", value=28000000, step=5000000)

total_spend = meta_spend + tiktok_spend + google_spend
total_reported_rev = meta_rep_rev + tiktok_rep_rev + google_rep_rev

if total_spend > 0 and actual_revenue > 0:
    mer = round(actual_revenue / total_spend, 2)
    reported_roas_avg = round(total_reported_rev / total_spend, 2)
    inflation_pct = round(((total_reported_rev - actual_revenue) / actual_revenue) * 100, 1)
    breakeven_mer = round(100 / cogs_margin_pct, 2)

    st.subheader("2. Kết Quả Kiểm Toán Hiệu Quả Marketing")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tổng Chi Phí Ads", f"{total_spend:,.0f} đ")
    m2.metric("Chỉ số MER Thực Tế", f"{mer}x", delta=f"{round(mer - breakeven_mer, 2)} so với Hòa vốn")
    m3.metric("ROAS Báo Cáo Ảo", f"{reported_roas_avg}x", delta=f"+{inflation_pct}% nhận vơ", delta_color="inverse")
    m4.metric("Điểm MER Hòa Vốn", f"{breakeven_mer}x")

    if mer < breakeven_mer:
        st.error(
            f"🚨 **CẢNH BÁO:** MER thực tế ({mer}x) đang THẤP HƠN điểm hòa vốn ({breakeven_mer}x)! "
            f"Dù các nền tảng báo cáo ROAS trung bình lên tới {reported_roas_avg}x, bạn thực chất đang bị LỖ "
            f"sau khi trừ giá vốn hàng bán và chi phí sàn."
        )
    else:
        st.success(
            f"✅ **AN TOÀN:** Kênh quảng cáo đang sinh lời thực tế! "
            f"MER đạt {mer}x (vượt mức hòa vốn {breakeven_mer}x)."
        )