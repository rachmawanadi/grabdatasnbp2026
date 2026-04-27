import streamlit as st
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard PTN",
    layout="wide"
)

# =========================
# LOAD DATA (WAJIB CACHE)
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("dataset_ptn_371-385.csv")

df = load_data()

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.title("🎛️ Filter")

search = st.sidebar.text_input("Cari Jurusan")

kategori = st.sidebar.selectbox(
    "Kategori",
    ["Semua"] + sorted(df["kategori"].dropna().unique())
)

ptn = st.sidebar.selectbox(
    "Pilih PTN",
    ["Semua"] + sorted(df["nama_ptn"].dropna().unique())
)

# =========================
# FILTER DATA
# =========================
filtered = df.copy()

if search:
    filtered = filtered[
        filtered["nama_prodi"].str.contains(search, case=False, na=False)
    ]

if kategori != "Semua":
    filtered = filtered[filtered["kategori"] == kategori]

if ptn != "Semua":
    filtered = filtered[filtered["nama_ptn"] == ptn]

# =========================
# HEADER
# =========================
st.title("🎓 Dashboard Jurusan PTN Indonesia")

# =========================
# KPI / METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Data", len(filtered))
col2.metric("Jumlah PTN", filtered["nama_ptn"].nunique())
col3.metric("Rata-rata Rasio", round(filtered["rasio"].mean(), 1))

# =========================
# GRAFIK
# =========================
st.subheader("📊 Top 10 Jurusan Paling Ketat")

top10 = filtered.sort_values(by="rasio", ascending=False).head(10)

st.bar_chart(top10.set_index("nama_prodi")["rasio"])

# =========================
# TABEL DATA
# =========================
st.subheader("📋 Data Jurusan")

st.dataframe(
    filtered.sort_values(by="rasio", ascending=False),
    use_container_width=True
)

# =========================
# DOWNLOAD BUTTON
# =========================
st.download_button(
    label="📥 Download Data",
    data=filtered.to_csv(index=False),
    file_name="hasil_filter.csv",
    mime="text/csv"
)
