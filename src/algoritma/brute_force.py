"""
Algoritma Brute Force (exhaustive search) untuk 0/1 Knapsack.

Ide: coba SEMUA himpunan bagian (subset) dari n objek. Ada 2^n subset.
Untuk tiap subset, hitung total berat dan total profit. Subset yang
total beratnya <= kapasitas dan total profitnya terbesar adalah solusi optimal.

Kompleksitas: O(n * 2^n)
    - 2^n subset yang diperiksa
    - tiap subset butuh O(n) untuk menjumlahkan berat dan profit
"""


def brute_force(berat, profit, kapasitas):
    """
    Masukan : berat, profit (list sepanjang n) dan kapasitas.
    Keluaran: (x, total_profit, total_berat)
              x = vektor solusi 0/1, misalnya [0, 1, 1, 0]
    """
    n = len(berat)
    x_terbaik = [0] * n
    profit_terbaik = 0
    berat_terbaik = 0

    # Setiap bilangan 0 .. 2^n - 1 mewakili satu subset.
    # Bit ke-i bernilai 1 artinya objek ke-i dipilih.
    # Contoh n = 4: subset 6 = 0110 (biner) -> objek ke-2 dan ke-3 dipilih.
    for subset in range(2 ** n):
        total_berat = 0
        total_profit = 0
        for i in range(n):
            if (subset >> i) & 1:
                total_berat += berat[i]
                total_profit += profit[i]

        # Simpan jika muat di knapsack dan profitnya lebih besar
        if total_berat <= kapasitas and total_profit > profit_terbaik:
            profit_terbaik = total_profit
            berat_terbaik = total_berat
            x_terbaik = [(subset >> i) & 1 for i in range(n)]

    return x_terbaik, profit_terbaik, berat_terbaik
