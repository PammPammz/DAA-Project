"""
Membuat grafik dari hasil eksperimen (folder hasil/). Grafik disimpan sebagai PNG
sehingga bisa langsung dimasukkan ke makalah dan slide.

Biasanya dijalankan otomatis di akhir eksperimen.py. Bisa juga dijalankan sendiri
untuk membuat ulang grafik tanpa mengulang eksperimen:
    python src/grafik.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # simpan ke file tanpa membuka jendela
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter

FOLDER_HASIL = Path(__file__).resolve().parent.parent / "hasil"

# Warna dan bentuk marker tetap per algoritma, sama di semua grafik.
# Bentuk marker yang berbeda membantu pembaca buta warna dan cetak hitam-putih.
GAYA = {
    "Brute Force":       {"warna": "#2a78d6", "marker": "o"},
    "Greedy by profit":  {"warna": "#eb6834", "marker": "s"},
    "Greedy by weight":  {"warna": "#1baf7a", "marker": "^"},
    "Greedy by density": {"warna": "#eda100", "marker": "D"},
    "Branch and Bound":  {"warna": "#e87ba4", "marker": "v"},
}
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
TINTA_REDUP = "#898781"
GRID = "#e1e0d9"
SUMBU = "#c3c2b7"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 9.5,
    "axes.edgecolor": SUMBU,
    "axes.labelcolor": TINTA_2,
    "axes.titlecolor": TINTA,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "xtick.color": TINTA_REDUP,
    "ytick.color": TINTA_REDUP,
    "xtick.labelcolor": TINTA_2,
    "ytick.labelcolor": TINTA_2,
    "legend.frameon": False,
    "legend.fontsize": 8.5,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "figure.facecolor": "white",
})


def angka_id(nilai):
    """Format angka gaya Indonesia: koma untuk desimal, titik untuk ribuan."""
    if nilai >= 1:
        return f"{nilai:,.0f}".replace(",", ".")
    teks = f"{nilai:.4f}".rstrip("0").rstrip(".")
    return teks.replace(".", ",")


def rapikan_sumbu(ax, log_y=False):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    if log_y:
        ax.set_yscale("log")
        ax.yaxis.set_major_locator(LogLocator(base=10))
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: angka_id(v)))


def garis(ax, x, y, algoritma, label=None):
    gaya = GAYA[algoritma]
    ax.plot(x, y, color=gaya["warna"], linewidth=2, marker=gaya["marker"], markersize=6.5,
            markeredgecolor="white", markeredgewidth=1.2, solid_capstyle="round",
            solid_joinstyle="round", label=label or algoritma, zorder=3)


def atur_sumbu_n(ax, daftar_n, log_x=False):
    """Label sumbu x = nilai n yang diuji. Skenario 2 memakai skala log agar 100 dan 200 tidak berdempetan."""
    if log_x:
        ax.set_xscale("log")
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_xticks(daftar_n)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: angka_id(v)))
    ax.set_xlabel("Jumlah makanan (n)" + (", skala log" if log_x else ""))


def grafik_waktu(per_n, nomor, judul, nama_file):
    data = per_n[per_n["skenario"] == nomor]
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    for algoritma in GAYA:
        baris = data[data["algoritma"] == algoritma]
        if not baris.empty:
            garis(ax, baris["n"], baris["rata_waktu_ms"], algoritma)
    rapikan_sumbu(ax, log_y=True)
    atur_sumbu_n(ax, sorted(data["n"].unique()))

    # Di skenario 1 ketiga strategi Greedy waktunya hampir sama sehingga garisnya
    # berimpit (garis by profit tertutup). Keterangan diletakkan di bawah garisnya.
    if nomor == 1:
        greedy = data[data["algoritma"].str.startswith("Greedy")]
        ax.set_ylim(greedy["rata_waktu_ms"].min() / 2.5, None)
        n_akhir = greedy["n"].max()
        y_akhir = greedy[greedy["n"] == n_akhir]["rata_waktu_ms"].min()
        ax.annotate("ketiga strategi Greedy hampir berimpit", (n_akhir, y_akhir), xytext=(-6, -15),
                    textcoords="offset points", ha="right", fontsize=8, color=TINTA_2)
    ax.set_ylabel("Rata-rata waktu eksekusi (ms, skala log)")
    ax.set_title(judul)

    # Label langsung hanya pada titik terakhir Brute Force (nilai terpenting)
    bf = data[data["algoritma"] == "Brute Force"]
    if not bf.empty:
        akhir = bf.iloc[-1]
        detik = akhir["rata_waktu_ms"] / 1000
        teks = f"{detik:.1f} detik".replace(".", ",") if detik >= 1 else f"{angka_id(akhir['rata_waktu_ms'])} ms"
        ax.annotate(teks, (akhir["n"], akhir["rata_waktu_ms"]), xytext=(-8, 8),
                    textcoords="offset points", ha="right", fontsize=8.5, color=TINTA)

    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1))
    fig.savefig(FOLDER_HASIL / nama_file)
    plt.close(fig)


def grafik_kualitas(per_n):
    fig, daftar_ax = plt.subplots(1, 2, figsize=(7.4, 4.0), sharey=True)
    judul = {1: "Skenario 1 (n kecil, kapasitas per makan)",
             2: "Skenario 2 (n besar, kapasitas harian)"}
    for ax, nomor in zip(daftar_ax, [1, 2]):
        data = per_n[per_n["skenario"] == nomor]
        ax.axhline(100, color=TINTA_REDUP, linewidth=1, zorder=2,
                   label="Optimal (Brute Force = Branch and Bound)")
        for algoritma in ["Greedy by profit", "Greedy by weight", "Greedy by density"]:
            baris = data[data["algoritma"] == algoritma]
            garis(ax, baris["n"], baris["rata_persen_optimal"], algoritma)
        rapikan_sumbu(ax)
        ax.set_ylim(0, 108)
        atur_sumbu_n(ax, sorted(data["n"].unique()))
        ax.set_title(judul[nomor], fontsize=9)
    daftar_ax[0].set_ylabel("Rata-rata protein (% dari optimal)")
    # Legenda di bawah kedua panel supaya panel mendapat lebar penuh
    pegangan, label = daftar_ax[1].get_legend_handles_labels()
    fig.legend(pegangan, label, loc="lower center", ncol=2, bbox_to_anchor=(0.5, 0.0))
    fig.suptitle("Kualitas solusi Greedy dibanding solusi optimal", x=0.01, ha="left",
                 fontsize=11, fontweight="bold", color=TINTA)
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    fig.savefig(FOLDER_HASIL / "grafik_kualitas.png")
    plt.close(fig)


def grafik_simpul(per_n):
    data = per_n[(per_n["skenario"] == 1) & (per_n["algoritma"] == "Branch and Bound")]
    n = data["n"]
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    garis(ax, n, 2 ** (n + 1) - 1, "Brute Force",
          label="Pohon ruang status penuh (2^(n+1) − 1 simpul)")
    garis(ax, n, data["rata_simpul_bnb"], "Branch and Bound",
          label="Branch and Bound (rata-rata simpul dibangkitkan)")
    rapikan_sumbu(ax, log_y=True)
    ax.set_ylim(10, None)
    atur_sumbu_n(ax, sorted(n))
    ax.set_ylabel("Jumlah simpul (skala log)")
    ax.set_title("Branch and Bound hanya memeriksa sebagian kecil pohon ruang status")
    ax.legend(loc="upper left")
    fig.savefig(FOLDER_HASIL / "grafik_simpul_bnb.png")
    plt.close(fig)


def main():
    per_n = pd.read_csv(FOLDER_HASIL / "ringkasan_per_n.csv")
    grafik_waktu(per_n, 1, "Waktu eksekusi, skenario 1 (n kecil)", "grafik_waktu_skenario1.png")
    grafik_waktu(per_n, 2, "Waktu eksekusi, skenario 2 (n besar)", "grafik_waktu_skenario2.png")
    grafik_kualitas(per_n)
    grafik_simpul(per_n)
    print("Grafik tersimpan: grafik_waktu_skenario1.png, grafik_waktu_skenario2.png, "
          "grafik_kualitas.png, grafik_simpul_bnb.png")


if __name__ == "__main__":
    main()
