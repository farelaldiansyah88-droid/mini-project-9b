# Sistem Rekapitulasi dan Klasifikasi Tingkat Daur Ulang Sampah Kabupaten/Kota Tahun 2025 Berbasis Python

Mini Project Praktikum Pemrograman Komputer (`TIN61104`) — **Laboratorium Sistem Informasi dan Keputusan (LSIK)**, Departemen Teknik Industri, Fakultas Teknik, Universitas Andalas (2026).

---

##  Deskripsi Proyek

Program berbasis antarmuka teks pada terminal (*Command Line Interface* / CLI) yang dirancang menggunakan bahasa pemrograman **Python** untuk membaca, memvalidasi, merekapitulasi, mengklasifikasikan, serta menganalisis posisi kinerja pengelolaan sampah dari **291 kabupaten/kota di 37 provinsi** di Indonesia pada tahun 2025.

Program ini mengotomatisasi pengolahan data sekunder berskala nasional agar terhindar dari kesalahan perhitungan manual, mendeteksi anomali maupun duplikasi pencatatan data daerah secara otomatis, serta mengevaluasi capaian daur ulang tiap daerah secara objektif terhadap rata-rata nasional menggunakan standar skor Z (*Z-Score*).

---

##  Fitur Utama (Menu 1–6)

1. **Cek Kelengkapan & Kewajaran Data (`cek_kewajaran_data`)**
   * Membaca berkas CSV dengan deteksi pemisah kolom otomatis (`,` atau `;`) dan *encoding* `utf-8-sig`.
   * Membersihkan serta mengonversi teks angka/persentase ke tipe numerik (`bersihkan_angka`), serta mendeteksi dan melewati baris duplikat pada versi 2.1.
   * Melaporkan total baris terbaca, jumlah baris dengan data utama kosong (`None`, `NaN`, `-`, dll.), serta daftar daerah dengan nilai persentase tidak wajar ($< 0\%$ atau $> 100\%$, seperti anomali pencatatan pada Kab. Purworejo sebesar $291,62\%$).
2. **Rekapitulasi Total Sampah & Daur Ulang per Provinsi (`rekapitulasi_per_provinsi`)**
   * Menjumlahkan total timbulan sampah tahunan, jumlah sampah didaur ulang, dan jumlah bahan baku hasil pengolahan pada masing-masing dari 37 provinsi serta akumulasi tingkat nasional (mengecualikan data berkategori *Tidak Wajar* pada versi 2.1).
3. **Klasifikasi Kategori Tingkat Daur Ulang (`klasifikasi_kategori` & `tentukan_kategori`)**
   * Mengelompokkan kabupaten/kota ke dalam empat kategori berdasarkan `persen_recycling_rate` dan menampilkan rincian daftar daerah terurut dari persentase tertinggi ke terendah sesuai kategori yang dipilih pengguna:
     * **Rendah:** $< 10\%$ ($166$ daerah)
     * **Sedang:** $10\% - 30\%$ ($96$ daerah)
     * **Tinggi:** $> 30\%$ hingga $100\%$ ($28$ daerah)
     * **Tidak Wajar:** Kosong, $< 0\%$, atau $> 100\%$ ($1$ daerah)
4. **Filter Daftar Kabupaten/Kota berdasarkan Provinsi (`filter_per_provinsi`)**
   * Menyaring dan menampilkan tabel seluruh kabupaten/kota beserta nilai timbulan sampah dan tingkat daur ulangnya berdasarkan kata kunci nama provinsi yang dimasukkan pengguna.
5. **Bandingkan Data Dua Kabupaten/Kota (`bandingkan_dua_daerah` & `cari_satu_daerah`)**
   * Membandingkan secara berdampingan metrik timbulan sampah, sampah didaur ulang, bahan baku dihasilkan, persentase daur ulang, kategori capaian, serta **Skor Z terhadap rata-rata nasional** antara dua kabupaten/kota pilihan pengguna.
6. **Analisis Z-Score & Interpretasi Posisi Daerah (`analisis_z_score_daerah`, `hitung_statistik_nasional`, & `hitung_dan_interpretasi_z`)**
   * Menghitung rata-rata nasional ($\bar{x} = 11,33\%$) dan simpangan baku sampel nasional ($s = 13,47\%$) dari populasi sampel valid ($n = 290$ daerah).
   * Menampilkan 5 langkah perhitungan skor Z untuk suatu kabupaten/kota beserta pembacaan posisi (setara, di atas, atau di bawah rata-rata nasional) dan status sebaran (normal dalam rentang $\pm 2\text{ SD}$, tidak biasa $> 2\text{ SD}$, atau pencilan ekstrem $> 3\text{ SD}$).

---

##  Arsitektur Modular (12 Fungsi)

Program dirancang secara modular dengan memisahkan fungsi pemrosesan/perhitungan dari fungsi antarmuka laporan:

| No | Nama Fungsi | Deskripsi Singkat |
| :---: | :--- | :--- |
| 1 | `bersihkan_angka(nilai_str)` | Menghapus simbol `%`, mengenali teks kosong (`nan`, `null`, `-`), dan mengonversi format koma/titik desimal ke `float`. |
| 2 | `baca_data_csv(nama_file)` | Memeriksa keberadaan berkas, mendeteksi *delimiter*, melewati baris duplikat (v2.1), dan menyusun `list of dict`. |
| 3 | `hitung_statistik_nasional(data)` | Menghitung rata-rata ($\bar{x}$), simpangan baku sampel ($s$), dan jumlah sampel valid ($n$) dari nilai $0\% - 100\%$. |
| 4 | `hitung_dan_interpretasi_z(...)` | Menghitung nilai $Z = \frac{x - \bar{x}}{s}$ dan mengembalikan tafsir posisi serta status pencilan. |
| 5 | `cek_kewajaran_data(data, jumlah_kosong)` | Menampilkan ringkasan baris terbaca, data kosong, dan tabel daerah di luar rentang $0\% - 100\%$ (Menu 1). |
| 6 | `rekapitulasi_per_provinsi(data)` | Merekapitulasi total tonase timbulan, daur ulang, dan bahan baku per provinsi serta total nasional (Menu 2). |
| 7 | `tentukan_kategori(persen)` | Menentukan label kategori (`Tidak Wajar`, `Rendah`, `Sedang`, atau `Tinggi`). |
| 8 | `klasifikasi_kategori(data)` | Mengelompokkan daerah berdasarkan kategori dan menampilkan daftar terurut menurun (Menu 3). |
| 9 | `filter_per_provinsi(data)` | Menyaring dan menampilkan tabel kabupaten/kota sesuai kata kunci provinsi (Menu 4). |
| 10 | `cari_satu_daerah(data, kata_kunci)` | Mencari kecocokan nama kabupaten/kota secara persis maupun sebagian (*partial match*). |
| 11 | `bandingkan_dua_daerah(data)` | Menyandingkan metrik dan skor Z dua kabupaten/kota dalam satu tabel komparasi (Menu 5). |
| 12 | `analisis_z_score_daerah(data)` | Menampilkan parameter nasional dan tahapan perhitungan skor Z untuk satu daerah (Menu 6). |

---

##  Dataset dan Sumber

Dataset yang digunakan adalah data sekunder dari portal **Satu Data Kementerian Lingkungan Hidup (KemenLH) / Badan Pengendalian Lingkungan Hidup Republik Indonesia**:
* **Nama File:** `Tingkat daur ulang (2025).csv`
* **Tautan Sumber:** [Satu Data KemenLH - Tingkat Daur Ulang](https://satudata.kemenlh.go.id/dataset/tingkat-daur-ulang)
* **Cakupan Data:** Tahun 2025 (Periode 1), mencakup **291 kabupaten/kota** pada **37 provinsi** di Indonesia (*encoding* UTF-8 with BOM).

### Struktur Kolom Dataset
| No | Nama Kolom | Keterangan | Contoh Nilai | Diproses Program |
| :---: | :--- | :--- | :--- | :---: |
| 1 | `Kode wilayah` | Kode wilayah administrasi kabupaten/kota | `11.01` | Tidak |
| 2 | `tahun` | Tahun pencatatan data | `2025` | Tidak |
| 3 | `periode` | Periode pencatatan | `1` | Tidak |
| 4 | `nama_provinsi` | Nama provinsi | `Aceh` | Ya |
| 5 | `nama_kabkota` | Nama kabupaten/kota | `Kab. Aceh Selatan` | Ya |
| 6 | `jml_timbulan_tahun` | Jumlah timbulan sampah tahunan (ton) | `35331,124` | Ya |
| 7 | `jml_daur_ulang` | Jumlah sampah yang didaur ulang (ton) | `0` | Ya |
| 8 | `jml_bahan_baku` | Jumlah bahan baku hasil pengolahan sampah (ton) | `18,615` | Ya |
| 9 | `persen_recycling_rate` | Persentase tingkat daur ulang ($\%$) | `0,05` | Ya |

> **Catatan Formula:** Nilai `persen_recycling_rate` pada dataset dihitung berdasarkan gabungan sampah didaur ulang dan bahan baku hasil pengolahan:
> $$\text{Recycling Rate} = \frac{\text{jml\_daur\_ulang} + \text{jml\_bahan\_baku}}{\text{jml\_timbulan\_tahun}} \times 100\%$$

---
