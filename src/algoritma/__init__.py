"""
Kumpulan algoritma 0/1 Knapsack.

Semua algoritma punya bentuk yang sama:
    x, total_profit, total_berat = fungsi(berat, profit, kapasitas)

Daftar ALGORITMA di bawah dipakai oleh file eksperimen. Untuk menambah
algoritma baru, cukup tambahkan satu baris di daftar ini.
"""

from .brute_force import brute_force
from .greedy import STRATEGI, greedy

ALGORITMA = {
    "Brute Force": brute_force,
    "Greedy by profit": lambda berat, profit, kapasitas: greedy(berat, profit, kapasitas, "profit"),
    "Greedy by weight": lambda berat, profit, kapasitas: greedy(berat, profit, kapasitas, "weight"),
    "Greedy by density": lambda berat, profit, kapasitas: greedy(berat, profit, kapasitas, "density"),
    # "Branch and Bound": branch_and_bound,   <- ditambahkan setelah B&B selesai
}
