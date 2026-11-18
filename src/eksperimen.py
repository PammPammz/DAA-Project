"""
Eksperimen perbandingan Brute Force, Greedy (3 strategi), dan Branch and Bound.

Skenario 1 (n kecil, semua algoritma):
    n = 10, 12, ..., 20 makanan, kapasitas sekali makan (AKG / 3).
    Solusi optimal = hasil Brute Force.
Skenario 2 (n besar, tanpa Brute Force karena 2^n terlalu besar):
    n = 100, 250, 500, 750, dan seluruh data makanan, kapasitas harian (AKG).
    Solusi optimal = hasil Branch and Bound (sudah terbukti selalu sama dengan
    Brute Force, lihat uji_bnb_vs_brute_force.py).

Setiap kombinasi n x jenis kelamin dijalankan dengan 10 seed (sampel acak berbeda).

Hasil disimpan di folder hasil/:
    skenario1_mentah.csv, skenario2_mentah.csv  -> satu baris per percobaan
    ringkasan_per_n.csv                         -> rata-rata per skenario, n, algoritma
    ringkasan_per_algoritma.csv                 -> rata-rata per skenario, algoritma
    grafik_*.png                                -> dibuat oleh grafik.py

Cara menjalankan (dari folder utama repo):
    python src/eksperimen.py
"""

import statistics
import time
from pathlib import Path

import pandas as pd

from algoritma import branch_and_bound_detail, brute_force, greedy
from data_utils import ambil_sampel, baca_data, kapasitas, ke_list

FOLDER_HASIL = Path(__file__).resolve().parent.parent / "hasil"

DAFTAR_SEED = range(1, 11)
JENIS_KELAMIN = ["pria", "perempuan"]

SKENARIO = {
    1: {"daftar_n": [10, 12, 14, 16, 18, 20], "per_makan": True, "pakai_brute_force": True},
    # None = seluruh data bersih. Pada ukuran ini setiap seed berisi makanan yang sama
    # (hanya urutannya berbeda), jadi pengulangannya hanya mengulang pengukuran waktu.
    2: {"daftar_n": [100, 250, 500, 750, None], "per_makan": False, "pakai_brute_force": False},
}

# Algoritma cepat diulang beberapa kali dan diambil median waktunya supaya
# pengukuran waktu stabil. Brute Force cukup sekali karena sudah lama.
ULANG_CEPAT = 5


def ukur_waktu(fungsi, ulang):
    """Menjalankan fungsi sebanyak `ulang` kali; mengembalikan hasil dan median waktu (ms)."""
    daftar_waktu = []
    hasil = None
    for _ in range(ulang):
        mulai = time.perf_counter()
        hasil = fungsi()
        daftar_waktu.append((time.perf_counter() - mulai) * 1000)
    return hasil, statistics.median(daftar_waktu)


def jalankan_semua(w, p, K, pakai_brute_force):
    """Menjalankan semua algoritma pada satu sampel. Mengembalikan list hasil per algoritma."""
    hasil = []

    if pakai_brute_force:
        (x, total_p, total_w), waktu = ukur_waktu(lambda: brute_force(w, p, K), ulang=1)
        hasil.append({"algoritma": "Brute Force", "x": x, "total_protein": total_p,
                      "total_kalori": total_w, "waktu_ms": waktu, "simpul_bnb": None})

    for strategi in ["profit", "weight", "density"]:
        (x, total_p, total_w), waktu = ukur_waktu(lambda: greedy(w, p, K, strategi), ULANG_CEPAT)
        hasil.append({"algoritma": f"Greedy by {strategi}", "x": x, "total_protein": total_p,
                      "total_kalori": total_w, "waktu_ms": waktu, "simpul_bnb": None})

    detail, waktu = ukur_waktu(lambda: branch_and_bound_detail(w, p, K), ULANG_CEPAT)
    hasil.append({"algoritma": "Branch and Bound", "x": detail["x"],
                  "total_protein": detail["total_profit"], "total_kalori": detail["total_berat"],
                  "waktu_ms": waktu, "simpul_bnb": detail["simpul_dibangkitkan"]})
    return hasil


def jalankan_skenario(nomor, df):
    konfigurasi = SKENARIO[nomor]
    pembanding = "Brute Force" if konfigurasi["pakai_brute_force"] else "Branch and Bound"
    baris = []

    for n in konfigurasi["daftar_n"]:
        n = len(df) if n is None else n
        for jk in JENIS_KELAMIN:
            K = kapasitas(jk, per_makan=konfigurasi["per_makan"])
            for seed in DAFTAR_SEED:
                _, w, p = ke_list(ambil_sampel(df, n, seed))
                hasil = jalankan_semua(w, p, K, konfigurasi["pakai_brute_force"])
                optimal = next(h["total_protein"] for h in hasil if h["algoritma"] == pembanding)

                for h in hasil:
                    if h["total_kalori"] > K + 1e-9:
                        raise RuntimeError(f"{h['algoritma']} melebihi kapasitas (n={n}, seed={seed})")
                    baris.append({
                        "skenario": nomor,
                        "n": n,
                        "jenis_kelamin": jk,
                        "kapasitas": round(K, 2),
                        "seed": seed,
                        "algoritma": h["algoritma"],
                        "total_protein": round(h["total_protein"], 2),
                        "total_kalori": round(h["total_kalori"], 2),
                        "jumlah_dipilih": sum(h["x"]),
                        "persen_optimal": round(h["total_protein"] / optimal * 100, 2),
                        "waktu_ms": round(h["waktu_ms"], 4),
                        "simpul_bnb": h["simpul_bnb"],
                    })
            print(f"  Skenario {nomor}: n={n:<5} {jk:<9} selesai")

    return pd.DataFrame(baris)


def buat_ringkasan(semua):
    semua = semua.assign(optimal=semua["persen_optimal"] >= 99.995)
    kelompok = ["skenario", "n", "algoritma"]
    per_n = semua.groupby(kelompok, sort=False).agg(
        percobaan=("seed", "size"),
        rata_protein=("total_protein", "mean"),
        rata_persen_optimal=("persen_optimal", "mean"),
        min_persen_optimal=("persen_optimal", "min"),
        jumlah_optimal=("optimal", "sum"),
        rata_waktu_ms=("waktu_ms", "mean"),
        rata_simpul_bnb=("simpul_bnb", "mean"),
    ).reset_index()

    per_algoritma = semua.groupby(["skenario", "algoritma"], sort=False).agg(
        percobaan=("seed", "size"),
        rata_persen_optimal=("persen_optimal", "mean"),
        min_persen_optimal=("persen_optimal", "min"),
        jumlah_optimal=("optimal", "sum"),
        rata_waktu_ms=("waktu_ms", "mean"),
    ).reset_index()

    return per_n.round(4), per_algoritma.round(4)


def main():
    FOLDER_HASIL.mkdir(exist_ok=True)
    df = baca_data()

    semua = []
    for nomor in SKENARIO:
        print(f"Menjalankan skenario {nomor} ...")
        hasil = jalankan_skenario(nomor, df)
        hasil.to_csv(FOLDER_HASIL / f"skenario{nomor}_mentah.csv", index=False)
        semua.append(hasil)
    semua = pd.concat(semua, ignore_index=True)

    per_n, per_algoritma = buat_ringkasan(semua)
    per_n.to_csv(FOLDER_HASIL / "ringkasan_per_n.csv", index=False)
    per_algoritma.to_csv(FOLDER_HASIL / "ringkasan_per_algoritma.csv", index=False)

    print("\nRingkasan per algoritma:")
    print(per_algoritma.to_string(index=False))

    # Grafik dibuat dari CSV di atas
    import grafik
    grafik.main()
    print(f"\nSemua hasil tersimpan di folder hasil/")


if __name__ == "__main__":
    main()
