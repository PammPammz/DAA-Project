"""
Algoritma Branch and Bound (B&B) untuk 0/1 Knapsack.

Ide: sama seperti Brute Force, ruang solusi berbentuk pohon. Di level ke-i
diputuskan objek ke-i diambil (x = 1) atau tidak (x = 0). Bedanya, B&B
TIDAK menelusuri seluruh pohon. Setiap simpul diberi nilai batas (bound),
yaitu taksiran profit TERBESAR yang masih mungkin dicapai dari simpul itu.
Kalau bound sebuah simpul tidak lebih besar dari solusi terbaik yang sudah
ditemukan, simpul itu "dibunuh" beserta seluruh cabangnya.

Hubungan dengan slide (8. Algoritma Branch and Bound):
    - Slide membahas persoalan minimasi (TSP), sehingga simpul yang diekspansi
      adalah yang cost-nya paling KECIL (least cost search).
    - Knapsack adalah persoalan maksimasi, sehingga simpul yang diekspansi
      adalah yang bound-nya paling BESAR.
    - "Simpul hidup" disimpan di antrian prioritas, "simpul-E" adalah simpul
      yang sedang diekspansi.

Fungsi bound memakai fractional knapsack dengan greedy by density
(materi 3, Teorema 3.2): sisa kapasitas diisi objek dengan profit/berat
terbesar, dan objek terakhir boleh diambil SEBAGIAN. Karena boleh mengambil
sebagian, hasilnya tidak pernah lebih kecil dari solusi 0/1 terbaik di
cabang itu. Jadi aman dipakai sebagai batas atas.

Kompleksitas: kasus terburuk tetap eksponensial, O(2^n), sama seperti
Brute Force. Dalam praktiknya jauh lebih sedikit simpul yang diperiksa
karena banyak cabang dibunuh.
"""

import heapq
from itertools import count


def branch_and_bound_detail(berat, profit, kapasitas):
    """
    Sama seperti branch_and_bound(), tetapi juga mengembalikan jumlah simpul
    yang dibangkitkan dan diekspansi (dipakai di eksperimen).
    """
    n = len(berat)

    # Urutkan objek berdasarkan density (profit/berat) dari besar ke kecil.
    # Pohon ruang status mengikuti urutan ini, dan fungsi bound juga
    # membutuhkan urutan ini.
    urutan = sorted(range(n), key=lambda i: profit[i] / berat[i], reverse=True)

    def hitung_bound(level, total_profit, total_berat):
        """Batas atas profit dari simpul yang sudah memutuskan `level` objek pertama."""
        sisa = kapasitas - total_berat
        bound = total_profit
        for j in range(level, n):
            i = urutan[j]
            if berat[i] <= sisa:
                sisa -= berat[i]
                bound += profit[i]
            else:
                bound += profit[i] * sisa / berat[i]   # ambil sebagian
                break
        return bound

    profit_terbaik = 0
    berat_terbaik = 0
    diambil_terbaik = ()
    simpul_dibangkitkan = 1   # simpul akar
    simpul_diekspansi = 0

    # Antrian prioritas berisi simpul hidup. heapq di Python mengeluarkan nilai
    # terkecil lebih dulu, jadi bound disimpan negatif agar bound terbesar keluar dulu.
    # Isi simpul: (-bound, nomor_urut, level, total_profit, total_berat, objek_diambil)
    nomor = count()
    simpul_hidup = [(-hitung_bound(0, 0, 0), next(nomor), 0, 0, 0, ())]

    while simpul_hidup:
        neg_bound, _, level, total_profit, total_berat, diambil = heapq.heappop(simpul_hidup)

        # Simpul-E punya bound terbesar di antara semua simpul hidup. Kalau
        # bound-nya pun tidak bisa mengalahkan solusi terbaik, semua simpul
        # hidup lain juga tidak bisa, jadi semuanya dibunuh dan pencarian selesai.
        if -neg_bound <= profit_terbaik:
            break
        if level == n:
            continue

        simpul_diekspansi += 1
        i = urutan[level]

        # Anak 1: objek i diambil (x = 1), hanya jika masih muat
        simpul_dibangkitkan += 1
        if total_berat + berat[i] <= kapasitas:
            profit_baru = total_profit + profit[i]
            berat_baru = total_berat + berat[i]
            diambil_baru = diambil + (i,)
            if profit_baru > profit_terbaik:
                profit_terbaik = profit_baru
                berat_terbaik = berat_baru
                diambil_terbaik = diambil_baru
            bound = hitung_bound(level + 1, profit_baru, berat_baru)
            if bound > profit_terbaik:
                heapq.heappush(simpul_hidup, (-bound, next(nomor), level + 1,
                                              profit_baru, berat_baru, diambil_baru))

        # Anak 2: objek i tidak diambil (x = 0)
        simpul_dibangkitkan += 1
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
        "simpul_dibangkitkan": simpul_dibangkitkan,
        "simpul_diekspansi": simpul_diekspansi,
    }


def branch_and_bound(berat, profit, kapasitas):
    """
    Masukan : berat, profit (list sepanjang n) dan kapasitas.
    Keluaran: (x, total_profit, total_berat), sama seperti algoritma lain.
    """
    hasil = branch_and_bound_detail(berat, profit, kapasitas)
    return hasil["x"], hasil["total_profit"], hasil["total_berat"]
