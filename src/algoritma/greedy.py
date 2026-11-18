STRATEGI = ["profit", "weight", "density"]


def urutan(berat, profit, strategi):
    indeks = range(len(berat))
    if strategi == "profit":
        return sorted(indeks, key=lambda i: profit[i], reverse=True)
    if strategi == "weight":
        return sorted(indeks, key=lambda i: berat[i])
    if strategi == "density":
        return sorted(indeks, key=lambda i: profit[i] / berat[i], reverse=True)
    raise ValueError(f"strategi tidak dikenal: {strategi}")


def greedy(berat, profit, kapasitas, strategi):
    """Ambil objek satu per satu sesuai urutan strategi selama masih muat."""
    x = [0] * len(berat)
    total_berat = 0
    total_profit = 0

    for i in urutan(berat, profit, strategi):
        # objek yang tidak muat dilewati, lanjut cek objek berikutnya
        if total_berat + berat[i] <= kapasitas:
            x[i] = 1
            total_berat += berat[i]
            total_profit += profit[i]

    return x, total_profit, total_berat
