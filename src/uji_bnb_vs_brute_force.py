"""Cek apakah hasil B&B selalu sama dengan Brute Force di sampel acak dari data asli."""

import sys

from algoritma import branch_and_bound_detail, brute_force
from data_utils import ambil_sampel, baca_data, kapasitas, ke_list

DAFTAR_N = [8, 12, 16]
DAFTAR_SEED = range(1, 11)


def main():
    df = baca_data()
    total_uji = 0
    total_sama = 0

    for n in DAFTAR_N:
        for jk in ["pria", "perempuan"]:
            K = kapasitas(jk, per_makan=True)
            sama = 0
            total_simpul = 0
            for seed in DAFTAR_SEED:
                _, w, p = ke_list(ambil_sampel(df, n, seed))
                _, profit_bf, _ = brute_force(w, p, K)
                hasil = branch_and_bound_detail(w, p, K)

                if abs(hasil["total_profit"] - profit_bf) < 1e-9 and hasil["total_berat"] <= K:
                    sama += 1
                else:
                    print(f"  BEDA: n={n} seed={seed} {jk}: B&B={hasil['total_profit']} BF={profit_bf}")
                total_simpul += hasil["simpul_dibangkitkan"]

            total_uji += len(DAFTAR_SEED)
            total_sama += sama
            print(f"n={n:<2} {jk:<9} K={K:6.1f}  sama: {sama}/{len(DAFTAR_SEED)}  "
                  f"rata-rata simpul B&B: {total_simpul / len(DAFTAR_SEED):6.1f} dari {2 ** (n + 1) - 1}")

    print(f"\nTotal: {total_sama}/{total_uji} sampel, B&B sama dengan Brute Force.")
    sys.exit(0 if total_sama == total_uji else 1)


if __name__ == "__main__":
    main()
