"""
Preprocessing dataset untuk Final Project DAA (0/1 Knapsack).

Sumber data : Indonesian Food and Drink Nutrition Dataset (Kaggle, anasfikrihanif),
              berasal dari Tabel Komposisi Pangan Indonesia, Kemenkes RI.
              Semua nilai gizi dihitung per 100 gram.

Pemetaan ke knapsack:
    name     -> Nama barang
    calories -> berat   (kalori per 100 g, yang dibatasi oleh kapasitas)
    proteins -> profit  (protein per 100 g, yang dimaksimalkan)

Setiap makanan dianggap satu porsi 100 g yang dipilih (1) atau tidak (0). Karena
itu hanya makanan yang wajar dimakan sebagai porsi 100 g yang dipertahankan.

Hasil:
    data/processed/data_bersih.csv   data yang dipakai algoritma
    data/processed/data_dibuang.csv  daftar baris yang dibuang beserta alasannya

Cara menjalankan (dari folder utama repo):
    python src/preprocessing.py
"""

import re
from pathlib import Path

import pandas as pd

# Lokasi file dihitung dari letak script ini, jadi bisa dijalankan dari folder mana pun
FOLDER_DATA = Path(__file__).resolve().parent.parent / "data"
FILE_MENTAH = FOLDER_DATA / "raw" / "nutrition.csv"
FILE_BERSIH = FOLDER_DATA / "processed" / "data_bersih.csv"
FILE_DIBUANG = FOLDER_DATA / "processed" / "data_dibuang.csv"

# Protein menyumbang 4 kkal per gram. Kalau 4 x protein melebihi total kalori
# (diberi toleransi 10%), datanya tidak konsisten. Ubah ke False kalau
# kelompok memutuskan semua baris tetap dipakai.
BUANG_DATA_TIDAK_KONSISTEN = True

# Kriteria pengecualian berdasarkan nama makanan (pola regex, huruf besar/kecil diabaikan).
# Setiap kriteria bisa dimatikan dengan mengubah True menjadi False.
KRITERIA_PENGECUALIAN = {
    # Nilai gizi per 100 g bentuk ini tidak mewakili porsi yang dimakan. Contoh: 100 g
    # beras mentah sekitar 360 kkal, sedangkan yang dimakan adalah nasi; 100 g teri
    # kering atau susu bubuk jauh lebih pekat daripada porsi makan sebenarnya.
    "Bentuk tidak siap santap (mentah, kering, tepung, bubuk)": (
        True, r"\bmentah\b|\bkering\b|\btepung\b|\bbubuk\b|\bserbuk\b"),
    # Satwa dilindungi atau satwa liar yang tidak diperjualbelikan sebagai bahan makanan umum
    "Satwa dilindungi atau satwa liar": (
        True, r"kura-kura|penyu|\bhiu\b|buaya|\brusa\b|menjangan"),
    # Pangan yang tidak umum dikonsumsi sehari-hari oleh masyarakat luas, termasuk bungkil
    # (ampas perasan minyak, umumnya untuk pakan) dan tempe bongkrek (produksinya dilarang)
    "Tidak lazim dikonsumsi sehari-hari": (
        True, r"\bkeong\b|\bulat\b|\bkuda\b|sarang|^bungkil|bongkrek"),
    # Pangan non-halal; mayoritas calon pengguna (mahasiswa di Indonesia) beragama Islam.
    # "Kacang babi" adalah sejenis kacang-kacangan, jadi tidak ikut dibuang.
    "Non-halal": (
        True, r"(?<!kacang )\bbabi\b|anjing|darah|dideh|katak|kodok|\bular\b"),
}

# Kata yang diabaikan saat mencari nama dobel, misalnya "Kakap" dan
# "Ikan kakap segar" dianggap makanan yang sama
KATA_PENGISI = {"ikan", "daging", "segar", "masakan"}


def kunci_nama(nama):
    """Menormalkan nama: huruf kecil, tanpa tanda baca, tanpa kata pengisi, urutan kata diabaikan."""
    kata = re.sub(r"[^a-z0-9 ]", " ", nama.lower()).split()
    return " ".join(sorted(set(kata) - KATA_PENGISI))


def main():
    df = pd.read_csv(FILE_MENTAH)
    print(f"Data mentah                 : {len(df)} baris, kolom {list(df.columns)}")
    dibuang = []

    def buang(mask, alasan):
        nonlocal df
        baris = df[mask]
        dibuang.append(baris.assign(alasan=alasan))
        df = df[~mask]
        print(f"  - {alasan:<55}: -{len(baris)} baris")

    # 1. Ambil 3 kolom yang dipakai, lalu ganti namanya sesuai format knapsack
    df = df[["name", "calories", "proteins"]].rename(
        columns={"name": "Nama barang", "calories": "berat", "proteins": "profit"}
    )
    df["Nama barang"] = df["Nama barang"].str.strip()

    # 2. Baris kosong atau nama yang persis sama
    buang(df.isna().any(axis=1) | df.duplicated(subset="Nama barang"), "Kosong atau nama persis sama")

    # 3. Kalori = 0, karena greedy by density menghitung profit/berat
    buang(df["berat"] <= 0, "Kalori = 0")

    # 4. Protein = 0, karena tidak pernah menambah nilai solusi
    buang(df["profit"] <= 0, "Protein = 0")

    # 5. Data yang tidak konsisten secara gizi
    if BUANG_DATA_TIDAK_KONSISTEN:
        buang(df["profit"] * 4 > df["berat"] * 1.1, "Tidak konsisten (4 x protein > kalori)")

    # 6. Kriteria pengecualian berdasarkan nama makanan
    for alasan, (aktif, pola) in KRITERIA_PENGECUALIAN.items():
        if aktif:
            buang(df["Nama barang"].str.contains(pola, case=False, regex=True), alasan)

    # 7. Makanan yang sama dengan nama berbeda (setelah dinormalisasi); baris pertama dipertahankan
    buang(df["Nama barang"].map(kunci_nama).duplicated(), "Nama dobel (makanan sama, nama berbeda)")

    df = df.reset_index(drop=True)
    FILE_BERSIH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(FILE_BERSIH, index=False)
    pd.concat(dibuang).to_csv(FILE_DIBUANG, index=False)
    print(f"Data bersih                 : {len(df)} baris -> data/processed/{FILE_BERSIH.name}")
    print(f"Daftar baris yang dibuang   : data/processed/{FILE_DIBUANG.name}")


if __name__ == "__main__":
    main()
