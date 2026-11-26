import csv
import os

NAMA_FILE = "Tingkat daur ulang (2025).cv"


def bersihkan_angka(nilai_str):
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


def hitung_statistik_nasional(data):
    nilai_valid = [
        d["persen_recycling_rate"]
        for d in data
        if d["persen_recycling_rate"] is not None and 0 <= d["persen_recycling_rate"] <= 100
    ]
    n = len(nilai_valid)
    if n < 2:
        return 0.0, 0.0, n

    rata_rata = sum(nilai_valid) / n
    variansi = sum((x - rata_rata) ** 2 for x in nilai_valid) / (n - 1)
    std_dev = variansi ** 0.5
    return rata_rata, std_dev, n


def hitung_dan_interpretasi_z(nilai_rate, rata_rata, std_dev):
    if nilai_rate is None or nilai_rate < 0 or nilai_rate > 100 or std_dev == 0:
        return None, "Data tidak wajar / tidak dapat dihitung"

    z = (nilai_rate - rata_rata) / std_dev

    if abs(z) < 0.05:
        posisi = "Setara dengan rata-rata nasional"
    elif z > 0:
        posisi = f"{abs(z):.2f} SD di ATAS rata-rata nasional"
    else:
        posisi = f"{abs(z):.2f} SD di BAWAH rata-rata nasional"

    if abs(z) > 3:
        status = "Pencilan ekstrem (Outlier > 3 SD)"
    elif abs(z) > 2:
        status = "Tidak biasa / sangat jauh dari rata-rata (> 2 SD)"
    else:
        status = "Sebaran normal (dalam rentang ±2 SD)"

    return z, f"{posisi} | {status}"


def cek_kewajaran_data(data, jumlah_kosong):
    print("\n" + "=" * 75)
    print(" " * 15 + "HASIL PENGECEKAN KELENGKAPAN & KEWAJARAN DATA")
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


def rekapitulasi_per_provinsi(data):
    rekap = {}
    total_nasional_timbulan = 0.0
    total_nasional_daur_ulang = 0.0
    total_nasional_bahan_baku = 0.0

    for item in data:
        prov = item["nama_provinsi"] if item["nama_provinsi"] else "Tidak Diketahui"
        if prov not in rekap:
            rekap[prov] = {
                "jumlah_daerah": 0,
                "timbulan": 0.0,
                "daur_ulang": 0.0,
                "bahan_baku": 0.0,
            }

        rekap[prov]["jumlah_daerah"] += 1
        rekap[prov]["timbulan"] += item["jml_timbulan_tahun"]
        rekap[prov]["daur_ulang"] += item["jml_daur_ulang"]
        rekap[prov]["bahan_baku"] += item["jml_bahan_baku"]

        total_nasional_timbulan += item["jml_timbulan_tahun"]
        total_nasional_daur_ulang += item["jml_daur_ulang"]
        total_nasional_bahan_baku += item["jml_bahan_baku"]

    print("\n" + "=" * 100)
    print(" " * 13 + "REKAPITULASI TOTAL TONASE SAMPAH DAN DAUR ULANG PER PROVINSI (TAHUN 2025)")
    print("=" * 100)
    print(f"{'No':<4} | {'Provinsi':<26} | {'Jml':>3} | {'Timbulan (Ton)':>17} | {'Daur Ulang (Ton)':>17} | {'Bahan Baku (Ton)':>17} |")
    print("-" * 100)

    for idx, prov in enumerate(sorted(rekap.keys()), start=1):
        r = rekap[prov]
        print(
            f"{idx:<4} | {prov:<26} | {r['jumlah_daerah']:>3} | "
            f"{r['timbulan']:>17,.2f} | {r['daur_ulang']:>17,.2f} | {r['bahan_baku']:>17,.2f} |"
        )

    print("-" * 100)
    print(
        f"{'TOTAL NASIONAL':<33} | {len(data):>3} | "
        f"{total_nasional_timbulan:>17,.2f} | {total_nasional_daur_ulang:>17,.2f} | {total_nasional_bahan_baku:>17,.2f} |"
    )
    print("=" * 100)


def tentukan_kategori(persen):
    if persen is None or persen < 0 or persen > 100:
        return "Tidak Wajar"
    elif persen < 10:
        return "Rendah"
    elif persen <= 30:
        return "Sedang"
    else:
        return "Tinggi"


def klasifikasi_kategori(data):
    kelompok = {
        "Rendah": [],
        "Sedang": [],
        "Tinggi": [],
        "Tidak Wajar": [],
    }

    for item in data:
        kategori = tentukan_kategori(item["persen_recycling_rate"])
        kelompok[kategori].append(item)

    print("\n" + "=" * 82)
    print("KLASIFIKASI TINGKAT DAUR ULANG KABUPATEN/KOTA")
    print("=" * 82)
    print(f"1. Kategori Rendah (< 10%)      : {len(kelompok['Rendah'])} daerah")
    print(f"2. Kategori Sedang (10% - 30%)  : {len(kelompok['Sedang'])} daerah")
    print(f"3. Kategori Tinggi (> 30%)      : {len(kelompok['Tinggi'])} daerah")
    if kelompok["Tidak Wajar"]:
        print(f"4. Data Tidak Wajar (<0%/>100%) : {len(kelompok['Tidak Wajar'])} daerah")
    print("-" * 82)

    pilihan = input("Tampilkan daftar daerah untuk kategori (Rendah/Sedang/Tinggi/Enter untuk kembali): ").strip().capitalize()
    if pilihan in kelompok and kelompok[pilihan]:
        print("\n" + "=" * 25 + f" DAFTAR DAERAH KATEGORI {pilihan.upper()} " + "=" * 26)
        print(f"{'No':<4} | {'Kabupaten/Kota':<33} | {'Provinsi':<27} | {'Rate (%)':>9}")
        print("-" * 82)
        daftar_urut = sorted(kelompok[pilihan], key=lambda x: x["persen_recycling_rate"], reverse=True)
        for idx, d in enumerate(daftar_urut, start=1):
            print(f"{idx:<4} | {d['nama_kabkota']:<33} | {d['nama_provinsi']:<27} | {d['persen_recycling_rate']:>8.2f}%")
        print("-" * 82)
    elif pilihan != "":
        print("Kategori tidak dikenali atau data kosong.")
