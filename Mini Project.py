import csv
import os

NAMA_FILE = "Tingkat daur ulang (2025).csv"

def bersihkan_angka(nilai_str):#Untuk merubah tipe data angka string menjadi float

    if nilai_str is None:
        return None
    teks = str(nilai_str).strip().replace("%", "")
    if teks == "" or teks.lower() in ["nan", "null", "none", "-"]:
        return None
    
    if "," in teks and "." in teks:
        teks = teks.replace(".", "").replace(",", ".")
    elif "," in teks:
        teks = teks.replace(",", ".")
    try:
        return float(teks)
    except ValueError:
        return None
        
def baca_data_csv(nama_file):
    
    if not os.path.exists(nama_file):
        print(f"\n[ERROR] File '{nama_file}' tidak ditemukan!")
        print("Pastikan file CSV berada di folder yang sama dengan program Python ini.")
        return [], 0

    data_bersih = []
    jumlah_data_kosong = 0

    with open(nama_file, mode="r", encoding="utf-8-sig") as file:
        
        sampel = file.read(2048)
        file.seek(0)
        delimiter = ";" if sampel.count(";") > sampel.count(",") else ","

        reader = csv.DictReader(file, delimiter=delimiter)

        for baris_ke, row in enumerate(reader, start=2):
            
            row_clean = {k.strip().lower(): (v.strip() if v else "") for k, v in row.items() if k}

            provinsi = row_clean.get("nama_provinsi", "")
            kabkota = row_clean.get("nama_kabkota", "")
            timbulan = bersihkan_angka(row_clean.get("jml_timbulan_tahun"))
            daur_ulang = bersihkan_angka(row_clean.get("jml_daur_ulang"))
            bahan_baku = bersihkan_angka(row_clean.get("jml_bahan_baku"))
            persen = bersihkan_angka(row_clean.get("persen_recycling_rate"))
