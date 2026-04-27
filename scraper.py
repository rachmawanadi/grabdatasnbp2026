import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

session = requests.Session()

# =========================
# 1. AMBIL MASTER PTN
# =========================
print("🔄 Ambil data PTN...")

mapping = []

for i in range(371, 387):  # 🔥 bisa diperluas
    url = f"https://sidatagrun-public-1076756628210.asia-southeast2.run.app/ptn_sb.php?ptn={i}"
    
    try:
        res = session.get(url, headers=headers, timeout=10)

        if "DAFTAR PRODI" not in res.text:
            continue

        soup = BeautifulSoup(res.text, "html.parser")

        tag = soup.find("a", class_="panel-title")

        if tag and tag.text.strip():
            nama_ptn = tag.text.strip()

            mapping.append({
                "ptn_id": i,
                "nama_ptn": nama_ptn
            })

            print(f"✔ PTN {i} - {nama_ptn}")

        time.sleep(1)

    except:
        continue

df_ptn = pd.DataFrame(mapping)

print("\nTotal PTN ditemukan:", len(df_ptn))


# =========================
# 2. AMBIL DATA PRODI SIPIL
# =========================
print("\n🔄 Ambil data Teknik Sipil...")

hasil = []

for ptn_id in df_ptn["ptn_id"]:
    url = f"https://sidatagrun-public-1076756628210.asia-southeast2.run.app/ptn_sb.php?ptn={ptn_id}"
    
    try:
        res = session.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        table = soup.find("table")
        if not table:
            continue

        rows = table.find_all("tr")

        for r in rows:
            cols = r.find_all("td")

            if len(cols) >= 6:
                kode_prodi = cols[1].text.strip()
                nama_prodi = cols[2].get_text(" ", strip=True)
                jenjang = cols[3].text.strip()
                daya = cols[4].text.strip()
                peminat = cols[5].text.strip()

                # 🔥 FILTER: hanya Teknik Sipil
                if nama_prodi.lower().strip() == "farmasi":
                    hasil.append({
                        "ptn_id": ptn_id,
                        "kode_prodi": kode_prodi,
                        "nama_prodi": nama_prodi,
                        "jenjang": jenjang,
                        "daya_tampung_2026": daya,
                        "peminat_2025": peminat
                    })

        print(f"✔ Prodi PTN {ptn_id}")

        time.sleep(1)

    except:
        continue

df_prodi = pd.DataFrame(hasil)

print("\nTotal data prodi:", len(df_prodi))


# =========================
# 3. CLEANING & RASIO
# =========================
df_prodi["daya_tampung_2026"] = pd.to_numeric(df_prodi["daya_tampung_2026"], errors="coerce")
df_prodi["peminat_2025"] = pd.to_numeric(df_prodi["peminat_2025"], errors="coerce")

df_prodi["rasio"] = (df_prodi["peminat_2025"] / df_prodi["daya_tampung_2026"]).round(1)

def kategori(r):
    if r > 20:
        return "Sangat Ketat"
    elif r > 10:
        return "Ketat"
    elif r > 5:
        return "Sedang"
    else:
        return "Longgar"

df_prodi["kategori"] = df_prodi["rasio"].apply(kategori)

# =========================
# 4. GABUNGKAN DATA
# =========================
df_final = df_prodi.merge(df_ptn, on="ptn_id", how="left")

df_final = df_final[[
    "ptn_id",
    "nama_ptn",
    "kode_prodi",
    "nama_prodi",
    "jenjang",
    "daya_tampung_2026",
    "peminat_2025",
    "rasio", 
    "kategori" 
]]

df_final = df_final.sort_values(by="rasio", ascending=False).reset_index(drop=True)


# =========================
# 5. SIMPAN HASIL
# =========================
df_final.to_csv("dataset_teknik_sipil_indonesia.csv", index=False)

print("\n✅ SELESAI!")
print(df_final.head())


# =========================
# 6. DOWNLOAD (COLAB)
# =========================
from google.colab import files
files.download("dataset_teknik_sipil_indonesia.csv")
