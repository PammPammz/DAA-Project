from pathlib import Path

import pandas as pd

FILE_DATA = Path(__file__).resolve().parent.parent / "data" / "processed" / "data_bersih.csv"

# AKG Permenkes No. 28 Tahun 2019, usia 19-29 tahun (kkal)
AKG = {"pria": 2650, "perempuan": 2250}


def kapasitas(jenis_kelamin, per_makan=False):
    # per_makan dipakai di skenario 1: batas harian dibagi 3 kali makan
    batas = AKG[jenis_kelamin]
    return batas / 3 if per_makan else batas


def baca_data(path=FILE_DATA):
    return pd.read_csv(path)


def ambil_sampel(df, n, seed=42):
    # seed tetap supaya sampelnya sama tiap kali dijalankan
    return df.sample(n=n, random_state=seed).reset_index(drop=True)


def ke_list(df):
    return list(df["Nama barang"]), list(df["berat"]), list(df["profit"])
