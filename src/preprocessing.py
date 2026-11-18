"""
Membersihkan dataset Kaggle (Indonesian Food and Drink Nutrition Dataset, sumber TKPI Kemenkes)
jadi 3 kolom: Nama barang, berat (kalori per 100 g), profit (protein per 100 g).
"""

import re
from pathlib import Path

import pandas as pd

FOLDER_DATA = Path(__file__).resolve().parent.parent / "data"
FILE_MENTAH = FOLDER_DATA / "raw" / "nutrition.csv"
FILE_BERSIH = FOLDER_DATA / "processed" / "data_bersih.csv"
FILE_DIBUANG = FOLDER_DATA / "processed" / "data_dibuang.csv"

# protein 1 g = 4 kkal, jadi kalau 4 x protein > kalori (toleransi 10%) datanya janggal
BUANG_DATA_TIDAK_KONSISTEN = True

# makanan dibuang kalau namanya cocok dengan pola di bawah. set False untuk mematikan
KRITERIA_PENGECUALIAN = {
    # 100 g bahan mentah/kering/tepung/bubuk gizinya jauh lebih pekat dari porsi yang dimakan
    # (contoh: beras mentah ~360 kkal, padahal yang dimakan nasi)
    "Bentuk tidak siap santap (mentah, kering, tepung, bubuk)": (
        True, r"\bmentah\b|\bkering\b|\btepung\b|\bbubuk\b|\bserbuk\b"),
    "Satwa dilindungi atau satwa liar": (
        True, r"kura-kura|penyu|\bhiu\b|buaya|\brusa\b|menjangan"),
    # bungkil = ampas perasan minyak (biasanya pakan), tempe bongkrek produksinya dilarang
    "Tidak lazim dikonsumsi sehari-hari": (
        True, r"\bkeong\b|\bulat\b|\bkuda\b|sarang|^bungkil|bongkrek"),
    # "kacang babi" itu jenis kacang, jadi tidak ikut dibuang
    "Non-halal": (
        True, r"(?<!kacang )\bbabi\b|anjing|darah|dideh|katak|kodok|\bular\b"),
}

# kata yang diabaikan saat cek nama dobel ("Kakap" = "Ikan kakap segar")
KATA_PENGISI = {"ikan", "daging", "segar", "masakan"}


def kunci_nama(nama):
    kata = re.sub(r"[^a-z0-9 ]", " ", nama.lower()).split()
    return " ".join(sorted(set(kata) - KATA_PENGISI))


def main():
    df = pd.read_csv(FILE_MENTAH)
    print(f"Data mentah: {len(df)} baris")
    dibuang = []

    def buang(mask, alasan):
        nonlocal df
        dibuang.append(df[mask].assign(alasan=alasan))
        print(f"  - {alasan}: {mask.sum()} baris")
        df = df[~mask]

    df = df[["name", "calories", "proteins"]].rename(
        columns={"name": "Nama barang", "calories": "berat", "proteins": "profit"})
    df["Nama barang"] = df["Nama barang"].str.strip()

    buang(df.isna().any(axis=1) | df.duplicated(subset="Nama barang"), "Kosong atau nama persis sama")
    buang(df["berat"] <= 0, "Kalori = 0")  # bikin pembagian nol di greedy by density
    buang(df["profit"] <= 0, "Protein = 0")
    if BUANG_DATA_TIDAK_KONSISTEN:
        buang(df["profit"] * 4 > df["berat"] * 1.1, "Tidak konsisten (4 x protein > kalori)")

    for alasan, (aktif, pola) in KRITERIA_PENGECUALIAN.items():
        if aktif:
            buang(df["Nama barang"].str.contains(pola, case=False, regex=True), alasan)

    # yang dipertahankan baris pertama
    buang(df["Nama barang"].map(kunci_nama).duplicated(), "Nama dobel (makanan sama, nama berbeda)")

    df = df.reset_index(drop=True)
    FILE_BERSIH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(FILE_BERSIH, index=False)
    pd.concat(dibuang).to_csv(FILE_DIBUANG, index=False)
    print(f"Data bersih: {len(df)} baris -> data/processed/{FILE_BERSIH.name}")


if __name__ == "__main__":
    main()
