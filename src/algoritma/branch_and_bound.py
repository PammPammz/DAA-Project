import heapq
from itertools import count


def branch_and_bound_detail(berat, profit, kapasitas):
    """
    B&B best-first untuk 0/1 knapsack. Simpul dengan bound terbesar diekspansi duluan,
    bound dihitung pakai fractional knapsack (greedy by density).
    """
    n = len(berat)
    urutan = sorted(range(n), key=lambda i: profit[i] / berat[i], reverse=True)

    def hitung_bound(level, total_profit, total_berat):
        # sisa kapasitas diisi objek density terbesar, objek terakhir boleh diambil sebagian
        sisa = kapasitas - total_berat
        bound = total_profit
        for j in range(level, n):
            i = urutan[j]
            if berat[i] <= sisa:
                sisa -= berat[i]
                bound += profit[i]
            else:
                bound += profit[i] * sisa / berat[i]
                break
        return bound

    profit_terbaik, berat_terbaik, diambil_terbaik = 0, 0, ()
    dibangkitkan, diekspansi = 1, 0

    # heapq itu min-heap, jadi bound disimpan negatif biar yang terbesar keluar duluan.
    # isi simpul: (-bound, nomor, level, total_profit, total_berat, objek_yang_diambil)
    nomor = count()
    simpul_hidup = [(-hitung_bound(0, 0, 0), next(nomor), 0, 0, 0, ())]

    while simpul_hidup:
        neg_bound, _, level, total_profit, total_berat, diambil = heapq.heappop(simpul_hidup)

        # bound terbesar pun tidak bisa ngalahin solusi terbaik -> sisa simpul dibunuh semua
        if -neg_bound <= profit_terbaik:
            break
        if level == n:
            continue

        diekspansi += 1
        i = urutan[level]

        # anak kiri: objek i diambil
        dibangkitkan += 1
        if total_berat + berat[i] <= kapasitas:
            p, w, a = total_profit + profit[i], total_berat + berat[i], diambil + (i,)
            if p > profit_terbaik:
                profit_terbaik, berat_terbaik, diambil_terbaik = p, w, a
            bound = hitung_bound(level + 1, p, w)
            if bound > profit_terbaik:
                heapq.heappush(simpul_hidup, (-bound, next(nomor), level + 1, p, w, a))

        # anak kanan: objek i tidak diambil
        dibangkitkan += 1
        bound = hitung_bound(level + 1, total_profit, total_berat)
        if bound > profit_terbaik:
            heapq.heappush(simpul_hidup, (-bound, next(nomor), level + 1,
                                          total_profit, total_berat, diambil))

    x = [0] * n
    for i in diambil_terbaik:
        x[i] = 1

    return {
        "x": x,
        "total_profit": profit_terbaik,
        "total_berat": berat_terbaik,
        "simpul_dibangkitkan": dibangkitkan,
        "simpul_diekspansi": diekspansi,
    }


def branch_and_bound(berat, profit, kapasitas):
    hasil = branch_and_bound_detail(berat, profit, kapasitas)
    return hasil["x"], hasil["total_profit"], hasil["total_berat"]
