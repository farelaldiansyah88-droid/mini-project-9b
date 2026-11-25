# Sistem Rekapitulasi dan Klasifikasi Tingkat Daur Ulang Sampah Kabupaten/Kota Tahun 2025 Berbasis Python

Mini Project Praktikum Pemrograman Komputer — **Laboratorium Sistem Informasi dan Keputusan (LSIK)**, Departemen Teknik Industri, Fakultas Teknik, Universitas Andalas (2026).

---

##  Deskripsi Proyek

Program berbasis antarmuka baris perintah (*Command Line Interface* / CLI) yang dirancang menggunakan bahasa pemrograman **Python** untuk membaca, memvalidasi, merekapitulasi, dan mengklasifikasikan data pengelolaan sampah dari **291 kabupaten/kota di 37 provinsi** di Indonesia pada tahun 2025. 

Program ini membantu mengotomatisasi pemeriksaan data sekunder berskala nasional agar terhindar dari kesalahan perhitungan manual serta mampu mendeteksi anomali pencatatan data daerah secara cepat.

---

##  Fitur Utama

1. **Pembersihan & Validasi Kewajaran Data (`cek_kewajaran_data`)**
   * Membaca file CSV dengan deteksi pemisah kolom otomatis (`,` atau `;`) dan *encoding* `utf-8-sig`.
   * Mengonversi format angka/persentase secara otomatis (`bersihkan_angka`).
   * Mendeteksi jumlah baris yang memiliki data utama kosong (`None`, `NaN`, `-`, dll.) serta mengidentifikasi anomali nilai persentase daur ulang (kurang dari $0\%$ atau melebihi $100\%$, seperti anomali pencatatan pada Kab. Purworejo sebesar $291,62\%$).
2. **Rekapitulasi Tonase Sampah (`rekapitulasi_per_provinsi`)**
   * Menghitung total jumlah timbulan sampah tahunan, total sampah yang didaur ulang, dan total bahan baku hasil pengolahan pada masing-masing provinsi serta akumulasi tingkat nasional.
3. **Klasifikasi Capaian Daur Ulang (`klasifikasi_kategori` & `tentukan_kategori`)**
   * Mengelompokkan kabupaten/kota ke dalam empat kelompok berdasarkan `persen_recycling_rate` dan menampilkan daftar daerah terurut dari persentase tertinggi ke terendah:
     * **Rendah:** $< 10\%$
     * **Sedang:** $10\% - 30\%$
     * **Tinggi:** $> 30\%$ (hingga $100\%$)
     * **Tidak Wajar:** Kosong, $< 0\%$, atau $> 100\%$
4. **Penyaringan Data per Provinsi (`filter_per_provinsi`)**
   * Menampilkan daftar seluruh kabupaten/kota beserta capaian pengelolaan sampahnya berdasarkan kata kunci nama provinsi yang dimasukkan pengguna.
5. **Komparasi Antar Daerah (`bandingkan_dua_daerah` & `cari_satu_daerah`)**
   * Membandingkan metrik timbulan sampah, jumlah daur ulang, bahan baku, persentase, dan kategori capaian antara dua kabupaten/kota secara berdampingan.

---

##  Sumber Dataset

Dataset yang digunakan adalah data sekunder dari portal **Satu Data Kementerian Lingkungan Hidup (KemenLH) / Badan Pengendalian Lingkungan Hidup Republik Indonesia**:
* **Nama File:** `Tingkat daur ulang (2025).csv`
* **Tautan Sumber:** [Satu Data KemenLH - Tingkat Daur Ulang](https://satudata.kemenlh.go.id/dataset/tingkat-daur-ulang)
* **Cakupan Data:** Tahun 2025 (Periode 1), terdiri dari 291 baris data kabupaten/kota.

### Struktur Kolom Dataset
| No | Nama Kolom | Keterangan | Diproses Program |
| :--- | :--- | :--- | :---: |
| 1 | `Kode wilayah` | Kode administrasi kabupaten/kota | Tidak |
| 2 | `tahun` | Tahun pencatatan data (`2025`) | Tidak |
| 3 | `periode` | Periode pencatatan (`1`) | Tidak |
| 4 | `nama provinsi` | Nama provinsi | Ya |
| 5 | `nama kabkota` | Nama kabupaten/kota | Ya |
| 6 | `jml_timbulan_tahunan` | Jumlah timbulan sampah tahunan (ton) | Ya |
| 7 | `jml_daur_ulang` | Jumlah sampah yang didaur ulang (ton) | Ya |
| 8 | `jml_bahan_baku` | Jumlah bahan baku hasil pengolahan (ton) | Ya |
| 9 | `persen_recycling_rate` | Persentase tingkat daur ulang ($\%$) | Ya |
