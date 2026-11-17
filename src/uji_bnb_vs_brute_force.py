"""
Menguji bahwa Branch and Bound selalu menemukan solusi optimal, dengan
membandingkannya dengan Brute Force pada banyak sampel acak dari data asli.

Untuk setiap sampel diperiksa:
    1. total protein B&B sama dengan Brute Force (optimal)
    2. total kalori B&B tidak melebihi kapasitas

Cara menjalankan (dari folder utama repo):
    python src/uji_bnb_vs_brute_force.py
"""

import sys

from algoritma import branch_and_bound_detail, brute_force
from data_utils import ambil_sampel, baca_data, kapasitas, ke_list

DAFTAR_N = [8, 12, 16]
DAFTAR_SEED = range(1, 11)


def main():
    df = baca_data()
    jumlah_uji = 0
    jumlah_sama = 0

    for n in DAFTAR_N:
        for jenis_kelamin in ["pria", "perempuan"]:
            K = kapasitas(jenis_kelamin, per_makan=True)
            sama = 0
            total_simpul = 0
            for seed in DAFTAR_SEED:
                _, w, p = ke_list(ambil_sampel(df, n, seed))
                _, profit_bf, _ = brute_force(w, p, K)
                hasil = branch_and_bound_detail(w, p, K)

                cocok = abs(hasil["total_profit"] - profit_bf) < 1e-9
                muat = hasil["total_berat"] <= K
                if cocok and muat:
                    sama += 1
                else:
                    print(f"  BEDA: n={n} seed={seed} {jenis_kelamin}: "
                          f"B&B={hasil['total_profit']} Brute Force={profit_bf}")
                total_simpul += hasil["simpul_dibangkitkan"]

            jumlah_uji += len(DAFTAR_SEED)
            jumlah_sama += sama
            rata_simpul = total_simpul / len(DAFTAR_SEED)
            simpul_pohon_penuh = 2 ** (n + 1) - 1
            print(f"n={n:<2} {jenis_kelamin:<9} K={K:6.1f}  sama dengan Brute Force: "
                  f"{sama}/{len(DAFTAR_SEED)}  rata-rata simpul B&B: {rata_simpul:6.1f} "
                  f"dari {simpul_pohon_penuh} simpul pohon penuh")

    print(f"\nTotal: {jumlah_sama}/{jumlah_uji} sampel, B&B sama dengan Brute Force.")
    sys.exit(0 if jumlah_sama == jumlah_uji else 1)


if __name__ == "__main__":
    main()
