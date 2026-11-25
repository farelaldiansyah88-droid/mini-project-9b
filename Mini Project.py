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
