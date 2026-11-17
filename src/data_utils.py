"""
Fungsi bantu yang dipakai semua algoritma: membaca data, mengambil sampel,
dan menentukan kapasitas knapsack.
"""

from pathlib import Path

import pandas as pd

# Lokasi data_bersih.csv dihitung dari letak file ini, jadi script bisa
# dijalankan dari folder mana pun.
FILE_DATA = Path(__file__).resolve().parent.parent / "data" / "processed" / "data_bersih.csv"

# Angka Kecukupan Gizi (Permenkes No. 28 Tahun 2019), usia 19-29 tahun, dalam kkal
AKG = {"pria": 2650, "perempuan": 2250}


def kapasitas(jenis_kelamin, per_makan=False):
    """
    Kapasitas knapsack = batas kalori.
    - per_makan=False : batas harian (skenario 2, n besar)
    - per_makan=True  : batas sekali makan = AKG / 3 (skenario 1, n kecil)
    """
    batas = AKG[jenis_kelamin]
    return batas / 3 if per_makan else batas


def baca_data(path=FILE_DATA):
    """Membaca data bersih dengan kolom: Nama barang, berat, profit."""
    return pd.read_csv(path)


def ambil_sampel(df, n, seed=42):
    """
    Mengambil n makanan secara acak. Seed dibuat tetap supaya sampel yang
    sama selalu terambil setiap kali dijalankan (hasil bisa diulang).
    """
    return df.sample(n=n, random_state=seed).reset_index(drop=True)


def ke_list(df):
    """Memecah DataFrame menjadi tiga list: nama, berat, profit."""
    return list(df["Nama barang"]), list(df["berat"]), list(df["profit"])
