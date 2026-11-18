from .branch_and_bound import branch_and_bound, branch_and_bound_detail
from .brute_force import brute_force
from .greedy import STRATEGI, greedy

# semua fungsi di sini dipanggil dengan bentuk yang sama: fungsi(berat, profit, kapasitas)
ALGORITMA = {
    "Brute Force": brute_force,
    "Greedy by profit": lambda w, p, K: greedy(w, p, K, "profit"),
    "Greedy by weight": lambda w, p, K: greedy(w, p, K, "weight"),
    "Greedy by density": lambda w, p, K: greedy(w, p, K, "density"),
    "Branch and Bound": branch_and_bound,
}
