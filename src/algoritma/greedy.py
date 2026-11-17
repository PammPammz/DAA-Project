"""
Algoritma Greedy untuk 0/1 Knapsack dengan 3 strategi (materi 3. Algoritma Greedy):

1. Greedy by profit  : pilih objek dengan profit terbesar lebih dulu
2. Greedy by weight  : pilih objek dengan berat teringan lebih dulu
3. Greedy by density : pilih objek dengan profit/berat terbesar lebih dulu

Cara kerja: urutkan objek sesuai strategi, lalu masukkan satu per satu.
Objek yang tidak muat dilewati, dan pemeriksaan lanjut ke objek berikutnya.
Sekali dimasukkan, objek tidak dikeluarkan lagi.

Greedy TIDAK menjamin solusi optimal untuk 0/1 Knapsack.

Kompleksitas: O(n log n), didominasi oleh pengurutan.
"""

STRATEGI = ["profit", "weight", "density"]


def urutan(berat, profit, strategi):
    """Mengembalikan indeks objek yang sudah diurutkan sesuai strategi."""
    indeks = range(len(berat))
    if strategi == "profit":
        return sorted(indeks, key=lambda i: profit[i], reverse=True)
    if strategi == "weight":
        return sorted(indeks, key=lambda i: berat[i])
    if strategi == "density":
        return sorted(indeks, key=lambda i: profit[i] / berat[i], reverse=True)
    raise ValueError(f"Strategi tidak dikenal: {strategi}")


def greedy(berat, profit, kapasitas, strategi):
    """
    Masukan : berat, profit (list sepanjang n), kapasitas, dan strategi
              ("profit", "weight", atau "density").
    Keluaran: (x, total_profit, total_berat)
    """
    n = len(berat)
    x = [0] * n
    total_berat = 0
    total_profit = 0

    for i in urutan(berat, profit, strategi):
        if total_berat + berat[i] <= kapasitas:
            x[i] = 1
            total_berat += berat[i]
            total_profit += profit[i]

    return x, total_profit, total_berat
