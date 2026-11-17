"""
Preprocessing dataset untuk Final Project DAA (0/1 Knapsack).

Sumber data : Indonesian Food and Drink Nutrition Dataset (Kaggle, anasfikrihanif),
              berasal dari Tabel Komposisi Pangan Indonesia, Kemenkes RI.
              Semua nilai gizi dihitung per 100 gram.

Pemetaan ke knapsack:
    name     -> Nama barang
    calories -> berat   (kalori per 100 g, yang dibatasi oleh kapasitas)
    proteins -> profit  (protein per 100 g, yang dimaksimalkan)

Cara menjalankan (dari folder utama repo):
    python src/preprocessing.py
"""

from pathlib import Path

import pandas as pd

# Lokasi file dihitung dari letak script ini, jadi bisa dijalankan dari folder mana pun
FOLDER_DATA = Path(__file__).resolve().parent.parent / "data"
FILE_MENTAH = FOLDER_DATA / "raw" / "nutrition.csv"
FILE_BERSIH = FOLDER_DATA / "processed" / "data_bersih.csv"

# Protein menyumbang 4 kkal per gram. Kalau 4 x protein melebihi total kalori
# (diberi toleransi 10%), datanya tidak konsisten. Ubah ke False kalau
# kelompok memutuskan semua baris tetap dipakai.
BUANG_DATA_TIDAK_KONSISTEN = True


def main():
    df = pd.read_csv(FILE_MENTAH)
    print(f"Data mentah            : {len(df)} baris, kolom {list(df.columns)}")

    # 1. Ambil 3 kolom yang dipakai, lalu ganti namanya sesuai format knapsack
    df = df[["name", "calories", "proteins"]].rename(
        columns={"name": "Nama barang", "calories": "berat", "proteins": "profit"}
    )

    # 2. Rapikan nama dan buang baris kosong atau dobel
    df["Nama barang"] = df["Nama barang"].str.strip()
    sebelum = len(df)
    df = df.dropna().drop_duplicates(subset="Nama barang")
    print(f"Buang kosong/dobel     : -{sebelum - len(df)} baris")

    # 3. Buang berat (kalori) = 0, karena greedy by density menghitung profit/berat
    sebelum = len(df)
    df = df[df["berat"] > 0]
    print(f"Buang kalori = 0       : -{sebelum - len(df)} baris")

    # 4. Buang profit (protein) = 0, karena tidak pernah menambah nilai solusi
    sebelum = len(df)
    df = df[df["profit"] > 0]
    print(f"Buang protein = 0      : -{sebelum - len(df)} baris")

    # 5. Buang data yang tidak konsisten secara gizi
    if BUANG_DATA_TIDAK_KONSISTEN:
        janggal = df[df["profit"] * 4 > df["berat"] * 1.1]
        df = df.drop(janggal.index)
        print(f"Buang tidak konsisten  : -{len(janggal)} baris -> {list(janggal['Nama barang'])}")

    df = df.reset_index(drop=True)
    FILE_BERSIH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(FILE_BERSIH, index=False)
    print(f"Data bersih            : {len(df)} baris, disimpan ke data/processed/{FILE_BERSIH.name}")


if __name__ == "__main__":
    main()
