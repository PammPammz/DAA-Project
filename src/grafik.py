"""Bikin grafik dari hasil/ringkasan_per_n.csv. Dipanggil otomatis di akhir eksperimen.py."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter, NullFormatter

FOLDER_HASIL = Path(__file__).resolve().parent.parent / "hasil"

# warna & marker dibuat tetap per algoritma, marker beda biar tetap kebaca kalau dicetak hitam putih
GAYA = {
    "Brute Force": ("#2a78d6", "o"),
    "Greedy by profit": ("#eb6834", "s"),
    "Greedy by weight": ("#1baf7a", "^"),
    "Greedy by density": ("#eda100", "D"),
    "Branch and Bound": ("#e87ba4", "v"),
}

plt.rcParams.update({
    "font.size": 9.5,
    "axes.titleweight": "bold",
    "legend.frameon": False,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})


def format_angka(v, _=None):
    # format Indonesia: 1.000 dan 0,01
    return f"{v:,.0f}".replace(",", ".") if v >= 1 else f"{v:g}".replace(".", ",")


def siapkan_sumbu(ax, daftar_n, log_y=False):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#e1e0d9")
    ax.set_axisbelow(True)
    if log_y:
        ax.set_yscale("log")
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.yaxis.set_major_formatter(FuncFormatter(format_angka))
    ax.set_xticks(daftar_n)
    ax.xaxis.set_major_formatter(FuncFormatter(format_angka))
    ax.set_xlabel("Jumlah makanan (n)")


def garis(ax, x, y, algoritma, label=None):
    warna, marker = GAYA[algoritma]
    ax.plot(x, y, color=warna, marker=marker, linewidth=2, markersize=6.5,
            markeredgecolor="white", label=label or algoritma, zorder=3)


def grafik_waktu(per_n, nomor, judul, nama_file):
    data = per_n[per_n["skenario"] == nomor]
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    for algoritma in GAYA:
        baris = data[data["algoritma"] == algoritma]
        if not baris.empty:
            garis(ax, baris["n"], baris["rata_waktu_ms"], algoritma)
    siapkan_sumbu(ax, sorted(data["n"].unique()), log_y=True)
    ax.set_ylabel("Rata-rata waktu (ms, skala log)")
    ax.set_title(judul)

    if nomor == 1:
        # garis greedy by profit ketutup garis greedy lain, jadi dikasih keterangan
        greedy = data[data["algoritma"].str.startswith("Greedy")]
        ax.set_ylim(greedy["rata_waktu_ms"].min() / 2.5, None)
        akhir = greedy[greedy["n"] == greedy["n"].max()]
        ax.annotate("ketiga strategi Greedy hampir berimpit",
                    (akhir["n"].iloc[0], akhir["rata_waktu_ms"].min()),
                    xytext=(-6, -15), textcoords="offset points", ha="right", fontsize=8)

        bf = data[data["algoritma"] == "Brute Force"].iloc[-1]
        ax.annotate(f"{format_angka(bf['rata_waktu_ms'])} ms", (bf["n"], bf["rata_waktu_ms"]),
                    xytext=(-8, 8), textcoords="offset points", ha="right", fontsize=8.5)

    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1))
    fig.savefig(FOLDER_HASIL / nama_file)
    plt.close(fig)


def grafik_kualitas(per_n):
    fig, daftar_ax = plt.subplots(1, 2, figsize=(7.4, 4.0), sharey=True)
    judul = {1: "Skenario 1 (n kecil, kapasitas per makan)",
             2: "Skenario 2 (n besar, kapasitas harian)"}
    for ax, nomor in zip(daftar_ax, [1, 2]):
        data = per_n[per_n["skenario"] == nomor]
        ax.axhline(100, color="gray", linewidth=1, label="Optimal (Brute Force = Branch and Bound)")
        for algoritma in ["Greedy by profit", "Greedy by weight", "Greedy by density"]:
            baris = data[data["algoritma"] == algoritma]
            garis(ax, baris["n"], baris["rata_persen_optimal"], algoritma)
        siapkan_sumbu(ax, sorted(data["n"].unique()))
        ax.set_ylim(0, 108)
        ax.set_title(judul[nomor], fontsize=9)
    daftar_ax[0].set_ylabel("Rata-rata protein (% dari optimal)")

    handles, labels = daftar_ax[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2)
    fig.suptitle("Kualitas solusi Greedy dibanding solusi optimal", fontweight="bold")
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    fig.savefig(FOLDER_HASIL / "grafik_kualitas.png")
    plt.close(fig)


def grafik_simpul(per_n):
    data = per_n[(per_n["skenario"] == 1) & (per_n["algoritma"] == "Branch and Bound")]
    n = data["n"]
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    garis(ax, n, 2 ** (n + 1) - 1, "Brute Force", label="Pohon ruang status penuh (2^(n+1) - 1 simpul)")
    garis(ax, n, data["rata_simpul_bnb"], "Branch and Bound", label="Branch and Bound (rata-rata simpul)")
    siapkan_sumbu(ax, sorted(n), log_y=True)
    ax.set_ylim(10, None)
    ax.set_ylabel("Jumlah simpul (skala log)")
    ax.set_title("Simpul yang diperiksa Branch and Bound vs pohon penuh")
    ax.legend(loc="upper left")
    fig.savefig(FOLDER_HASIL / "grafik_simpul_bnb.png")
    plt.close(fig)


def main():
    per_n = pd.read_csv(FOLDER_HASIL / "ringkasan_per_n.csv")
    grafik_waktu(per_n, 1, "Waktu eksekusi skenario 1 (n kecil)", "grafik_waktu_skenario1.png")
    grafik_waktu(per_n, 2, "Waktu eksekusi skenario 2 (n besar)", "grafik_waktu_skenario2.png")
    grafik_kualitas(per_n)
    grafik_simpul(per_n)
    print("Grafik tersimpan di folder hasil/")


if __name__ == "__main__":
    main()
