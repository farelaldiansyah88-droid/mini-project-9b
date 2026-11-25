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

            if (
                not provinsi
                or not kabkota
                or timbulan is None
                or daur_ulang is None
                or bahan_baku is None
                or persen is None
            ):
                jumlah_data_kosong += 1

            data_bersih.append({
                "baris": baris_ke,
                "nama_provinsi": provinsi,
                "nama_kabkota": kabkota,
                "jml_timbulan_tahun": timbulan if timbulan is not None else 0.0,
                "jml_daur_ulang": daur_ulang if daur_ulang is not None else 0.0,
                "jml_bahan_baku": bahan_baku if bahan_baku is not None else 0.0,
                "persen_recycling_rate": persen,
            })

    return data_bersih, jumlah_data_kosong
    
def cek_kewajaran_data(data, jumlah_kosong):
    
    print("\n" + "=" * 75)
    print(" "*15+"HASIL PENGECEKAN KELENGKAPAN & KEWAJARAN DATA")
    print("=" * 75)
    print(f"Total baris data terbaca      : {len(data)} kabupaten/kota")
    print(f"Baris dengan data kosong/null : {jumlah_kosong} baris")

    data_tidak_wajar = []
    for item in data:
        persen = item["persen_recycling_rate"]
        if persen is None or persen < 0 or persen > 100:
            data_tidak_wajar.append(item)

    print(f"Data tidak wajar (<0% / >100%): {len(data_tidak_wajar)} daerah")
    print("-" * 75)

    if data_tidak_wajar:
        print(f"{'No':<4} | {'Kabupaten/Kota':<28} | {'Provinsi':<22} | {'Rate (%)':>10}")
        print("-" * 75)
        for idx, d in enumerate(data_tidak_wajar, start=1):
            nilai_str = f"{d['persen_recycling_rate']:.2f}%" if d["persen_recycling_rate"] is not None else "KOSONG"
            print(f"{idx:<4} | {d['nama_kabkota']:<28} | {d['nama_provinsi']:<22} | {nilai_str:>10}")
    else:
        print("Seluruh data berada dalam rentang wajar (0% - 100%).")
    print("=" * 75)
