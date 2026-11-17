# DAA-Project
Final Project DAA: Perbandingan Brute Force, Greedy, dan Branch and Bound pada 0/1 Knapsack untuk pemilihan makanan berprotein tinggi dengan batas kalori

## Masalah
Memilih makanan dengan total protein sebanyak mungkin tanpa melebihi batas kalori. Setiap makanan dihitung satu porsi 100 gram, dipilih (1) atau tidak (0).

| Istilah knapsack | Di proyek ini |
| --- | --- |
| Objek | Makanan |
| Berat (w) | Kalori per 100 g |
| Profit (p) | Protein (g) per 100 g |
| Kapasitas (K) | Batas kalori dari Angka Kecukupan Gizi (Permenkes No. 28 Tahun 2019), usia 19–29 tahun |

Dua skenario kapasitas:
- **Skenario 1** (n = 10–20, ketiga algoritma): batas sekali makan, AKG ÷ 3 (pria ≈ 883 kkal, perempuan 750 kkal)
- **Skenario 2** (n = 100–1319, Greedy vs Branch and Bound): batas harian (pria 2650 kkal, perempuan 2250 kkal)

## Dataset
Indonesian Food and Drink Nutrition Dataset (Kaggle, oleh anasfikrihanif), bersumber dari Tabel Komposisi Pangan Indonesia, Kementerian Kesehatan RI.

Preprocessing (`src/preprocessing.py`): 1346 baris → 1319 baris
- kolom yang dipakai: `name` → Nama barang, `calories` → berat, `proteins` → profit
- dibuang: kalori 0 (1 baris), protein 0 (21 baris), data tidak konsisten secara gizi, yaitu 4 × protein > kalori (5 baris)

## Struktur folder
```
data/
  raw/nutrition.csv            data asli Kaggle
  processed/data_bersih.csv    hasil preprocessing
src/
  algoritma/                   brute_force.py, greedy.py, branch_and_bound.py
  data_utils.py                baca data, ambil sampel, kapasitas
  preprocessing.py             membersihkan data
  uji_contoh_slide.py          menguji algoritma dengan contoh di slide kuliah
  uji_bnb_vs_brute_force.py    memastikan B&B selalu sama dengan Brute Force (optimal)
hasil/                         tabel dan grafik eksperimen
docs/                          makalah dan slide presentasi
```

## Cara menjalankan
```
pip install -r requirements.txt
python src/preprocessing.py
python src/uji_contoh_slide.py
python src/uji_bnb_vs_brute_force.py
```

## Status
- [x] Preprocessing data
- [x] Brute Force
- [x] Greedy (by profit, by weight, by density)
- [x] Branch and Bound (best-first, bound dari fractional knapsack)
- [ ] Eksperimen
- [ ] Makalah dan slide

## Anggota
- (nama – NIM)
- (nama – NIM)
- (nama – NIM)

## Jurnal tujuan
(diisi setelah jurnal dipilih)
