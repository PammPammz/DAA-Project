def brute_force(berat, profit, kapasitas):
    """Exhaustive search: cek semua 2^n himpunan bagian, ambil yang profitnya paling besar."""
    n = len(berat)
    x_terbaik, profit_terbaik, berat_terbaik = [0] * n, 0, 0

    # tiap bilangan 0..2^n-1 mewakili satu himpunan bagian,
    # bit ke-i = 1 berarti objek ke-i diambil
    for subset in range(2 ** n):
        total_berat = 0
        total_profit = 0
        for i in range(n):
            if (subset >> i) & 1:
                total_berat += berat[i]
                total_profit += profit[i]

        if total_berat <= kapasitas and total_profit > profit_terbaik:
            profit_terbaik = total_profit
            berat_terbaik = total_berat
            x_terbaik = [(subset >> i) & 1 for i in range(n)]

    return x_terbaik, profit_terbaik, berat_terbaik
