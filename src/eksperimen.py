"""
Eksperimen perbandingan algoritma. Hasil CSV dan grafik disimpan di folder hasil/.

Skenario 1: n = 10..20, kapasitas sekali makan (AKG/3), pembanding optimal = Brute Force
Skenario 2: n = 100..semua data, kapasitas harian (AKG), pembanding optimal = Branch and Bound
"""

import statistics
import time
from pathlib import Path

import pandas as pd

import grafik
from algoritma import branch_and_bound_detail, brute_force, greedy
from data_utils import ambil_sampel, baca_data, kapasitas, ke_list

FOLDER_HASIL = Path(__file__).resolve().parent.parent / "hasil"

DAFTAR_SEED = range(1, 11)
JENIS_KELAMIN = ["pria", "perempuan"]

SKENARIO = {
    1: {"daftar_n": [10, 12, 14, 16, 18, 20], "per_makan": True, "pakai_brute_force": True},
    # None = semua data. di ukuran ini tiap seed isinya sama (cuma beda urutan),
    # jadi pengulangannya cuma untuk ngukur waktu
    2: {"daftar_n": [100, 250, 500, 750, None], "per_makan": False, "pakai_brute_force": False},
}

# greedy & B&B terlalu cepat, jadi diulang 5x lalu diambil median waktunya
ULANG_CEPAT = 5


def ukur_waktu(fungsi, ulang):
    daftar_waktu = []
    for _ in range(ulang):
        mulai = time.perf_counter()
        hasil = fungsi()
        daftar_waktu.append((time.perf_counter() - mulai) * 1000)
    return hasil, statistics.median(daftar_waktu)


def jalankan_semua(w, p, K, pakai_brute_force):
    hasil = []

    def catat(nama, x, total_p, total_w, waktu, simpul=None):
        hasil.append({"algoritma": nama, "x": x, "total_protein": total_p,
                      "total_kalori": total_w, "waktu_ms": waktu, "simpul_bnb": simpul})

    if pakai_brute_force:
        (x, total_p, total_w), waktu = ukur_waktu(lambda: brute_force(w, p, K), ulang=1)
        catat("Brute Force", x, total_p, total_w, waktu)

    for strategi in ["profit", "weight", "density"]:
        (x, total_p, total_w), waktu = ukur_waktu(lambda: greedy(w, p, K, strategi), ULANG_CEPAT)
        catat(f"Greedy by {strategi}", x, total_p, total_w, waktu)

    d, waktu = ukur_waktu(lambda: branch_and_bound_detail(w, p, K), ULANG_CEPAT)
    catat("Branch and Bound", d["x"], d["total_profit"], d["total_berat"], waktu, d["simpul_dibangkitkan"])
    return hasil


def jalankan_skenario(nomor, df):
    cfg = SKENARIO[nomor]
    pembanding = "Brute Force" if cfg["pakai_brute_force"] else "Branch and Bound"
    baris = []

    for n in cfg["daftar_n"]:
        n = len(df) if n is None else n
        for jk in JENIS_KELAMIN:
            K = kapasitas(jk, per_makan=cfg["per_makan"])
            for seed in DAFTAR_SEED:
                _, w, p = ke_list(ambil_sampel(df, n, seed))
                hasil = jalankan_semua(w, p, K, cfg["pakai_brute_force"])
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
            print(f"  skenario {nomor}: n={n:<5} {jk:<9} selesai")

    return pd.DataFrame(baris)


def buat_ringkasan(semua):
    semua = semua.assign(optimal=semua["persen_optimal"] >= 99.995)
    per_n = semua.groupby(["skenario", "n", "algoritma"], sort=False).agg(
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
        print(f"Skenario {nomor} ...")
        hasil = jalankan_skenario(nomor, df)
        hasil.to_csv(FOLDER_HASIL / f"skenario{nomor}_mentah.csv", index=False)
        semua.append(hasil)
    semua = pd.concat(semua, ignore_index=True)

    per_n, per_algoritma = buat_ringkasan(semua)
    per_n.to_csv(FOLDER_HASIL / "ringkasan_per_n.csv", index=False)
    per_algoritma.to_csv(FOLDER_HASIL / "ringkasan_per_algoritma.csv", index=False)
    print("\n" + per_algoritma.to_string(index=False))

    grafik.main()
    print("Selesai, hasil ada di folder hasil/")


if __name__ == "__main__":
    main()
