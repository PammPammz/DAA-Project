"""Cek Brute Force, Greedy, dan B&B pakai contoh soal di slide kuliah."""

import sys

from algoritma import branch_and_bound, brute_force, greedy

# jawaban ditulis sebagai (x, total_profit, total_berat)
CONTOH = [
    {
        "nama": "Slide Brute Force, n = 4, K = 16",
        "berat": [2, 5, 10, 5],
        "profit": [20, 30, 50, 10],
        "kapasitas": 16,
        "jawaban": {
            "optimal": ([0, 1, 1, 0], 80, 15),
        },
    },
    {
        "nama": "Slide Greedy Contoh 4, K = 16",
        "berat": [6, 5, 10, 5],
        "profit": [12, 15, 50, 10],
        "kapasitas": 16,
        "jawaban": {
            "profit": ([0, 1, 1, 0], 65, 15),
            "weight": ([1, 1, 0, 1], 37, 16),
            "density": ([0, 1, 1, 0], 65, 15),
            "optimal": ([0, 1, 1, 0], 65, 15),
        },
    },
    {
        "nama": "Slide Greedy Contoh 5, K = 100",
        "berat": [100, 50, 45, 20, 10, 5],
        "profit": [40, 35, 18, 4, 10, 2],
        "kapasitas": 100,
        "jawaban": {
            "profit": ([1, 0, 0, 0, 0, 0], 40, 100),
            "weight": ([0, 0, 1, 1, 1, 1], 34, 80),
            "density": ([0, 1, 0, 1, 1, 1], 51, 85),
            # di slide tertulis optimal 53 (objek 2 & 3), tapi objek 2, 3, 6
            # beratnya pas 100 dengan profit 55
            "optimal": ([0, 1, 1, 0, 0, 1], 55, 100),
        },
    },
]


def main():
    semua_ok = True
    for contoh in CONTOH:
        print(contoh["nama"])
        w, p, K = contoh["berat"], contoh["profit"], contoh["kapasitas"]
        for metode, harapan in contoh["jawaban"].items():
            if metode == "optimal":
                dijalankan = [("Brute Force", brute_force(w, p, K)),
                              ("Branch and Bound", branch_and_bound(w, p, K))]
            else:
                dijalankan = [(f"Greedy by {metode}", greedy(w, p, K, metode))]

            for label, hasil in dijalankan:
                ok = hasil == harapan
                semua_ok = semua_ok and ok
                x, total_profit, total_berat = hasil
                print(f"  [{'OK   ' if ok else 'GAGAL'}] {label:<18} X = {x}  profit = {total_profit}  berat = {total_berat}")
                if not ok:
                    print(f"          seharusnya: X = {harapan[0]}  profit = {harapan[1]}  berat = {harapan[2]}")
        print()

    print("Semua OK." if semua_ok else "Ada yang tidak sesuai.")
    sys.exit(0 if semua_ok else 1)


if __name__ == "__main__":
    main()
