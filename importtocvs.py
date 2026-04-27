import pandas as pd

df = pd.DataFrame(data)

# 🔧 konversi aman
df["daya_tampung_2026"] = pd.to_numeric(df["daya_tampung_2026"], errors="coerce")
df["peminat_2025"] = pd.to_numeric(df["peminat_2025"], errors="coerce")

# 🔥 hitung rasio
df["rasio"] = df["peminat_2025"] / df["daya_tampung_2026"]

# optional: urutkan
df = df.sort_values(by="rasio", ascending=False)

# simpan
df.to_csv("sipil_teknik_ptn_332.csv", index=False)

from google.colab import files
files.download("sipil_teknik_ptn_332.csv")
