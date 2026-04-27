import streamlit as st
import pandas as pd

st.title("Dashboard Jurusan PTN")

# load data
df = pd.read_csv("dataset_ptn_371_385.csv")

# search
search = st.text_input("Cari Jurusan")

# filter kategori
kategori = st.selectbox(
    "Filter Kategori",
    ["Semua"] + sorted(df["kategori"].dropna().unique())
)

# filter data
filtered = df.copy()

if search:
    filtered = filtered[
        filtered["nama_prodi"].str.contains(search, case=False, na=False)
    ]

if kategori != "Semua":
    filtered = filtered[filtered["kategori"] == kategori]

st.write(f"Total data: {len(filtered)}")
st.dataframe(filtered)
