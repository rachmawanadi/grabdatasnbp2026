import requests
from bs4 import BeautifulSoup

url = "https://sidatagrun-public-1076756628210.asia-southeast2.run.app/ptn_sb.php?ptn=332"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

data = []

table = soup.find("table")
rows = table.find_all("tr")

for r in rows:
    cols = r.find_all("td")
    
    if len(cols) >= 6:
        kode_prodi = cols[1].text.strip()
        nama_prodi = cols[2].text.strip()
        jenjang = cols[3].text.strip()
        daya_tampung = cols[4].text.strip()
        peminat = cols[5].text.strip()

        nama_lower = nama_prodi.lower()

        # 🔥 FILTER: teknik & sipil
        if "teknik" in nama_lower or "sipil" in nama_lower:
            data.append({
                "ptn_id": 332,
                "kode_prodi": kode_prodi,
                "nama_prodi": nama_prodi,
                "jenjang": jenjang,
                "daya_tampung_2026": daya_tampung,
                "peminat_2025": peminat
            })

# tampilkan hasil
for d in data:
    print(d)

print("\nTotal ditemukan:", len(data))
