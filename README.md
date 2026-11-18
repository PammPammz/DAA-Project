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
- **Skenario 2** (n = 100, 250, 500, 750, dan seluruh 1107 makanan; Greedy vs Branch and Bound): batas harian (pria 2650 kkal, perempuan 2250 kkal)

## Dataset
Indonesian Food and Drink Nutrition Dataset (Kaggle, oleh anasfikrihanif), bersumber dari Tabel Komposisi Pangan Indonesia, Kementerian Kesehatan RI.

Preprocessing (`src/preprocessing.py`): 1346 baris → 1107 baris. Kolom yang dipakai: `name` → Nama barang, `calories` → berat, `proteins` → profit.

| Langkah | Dibuang | Alasan |
| --- | --- | --- |
| Kalori = 0 | 1 | greedy by density membagi profit dengan berat |
| Protein = 0 | 21 | tidak pernah menambah nilai solusi |
| Tidak konsisten secara gizi | 5 | 4 × protein > kalori (protein 1 g = 4 kkal) |
| Bentuk tidak siap santap | 144 | nama mengandung mentah, kering, tepung, bubuk, atau serbuk; nilai gizi per 100 g bentuk ini tidak mewakili porsi yang dimakan |
| Satwa dilindungi atau satwa liar | 6 | kura-kura, penyu, hiu, buaya, rusa, menjangan |
| Tidak lazim dikonsumsi sehari-hari | 13 | keong, ulat sagu, kuda, sarang burung, bungkil, tempe bongkrek |
| Non-halal | 19 | mayoritas calon pengguna beragama Islam |
| Nama dobel | 30 | makanan sama dengan nama berbeda, misalnya "Kakap" dan "Ikan kakap segar" |

Daftar lengkap baris yang dibuang beserta alasannya ada di `data/processed/data_dibuang.csv`. Setiap kriteria bisa dimatikan di `KRITERIA_PENGECUALIAN` dalam `preprocessing.py`.

## Struktur folder
```
data/
  raw/nutrition.csv            data asli Kaggle
  processed/data_bersih.csv    hasil preprocessing
  processed/data_dibuang.csv   baris yang dibuang beserta alasannya
src/
  algoritma/                   brute_force.py, greedy.py, branch_and_bound.py
  data_utils.py                baca data, ambil sampel, kapasitas
  preprocessing.py             membersihkan data
  uji_contoh_slide.py          menguji algoritma dengan contoh di slide kuliah
  uji_bnb_vs_brute_force.py    memastikan B&B selalu sama dengan Brute Force (optimal)
  eksperimen.py                menjalankan semua algoritma untuk skenario 1 dan 2
  grafik.py                    membuat grafik dari hasil eksperimen
hasil/
  skenario1_mentah.csv         satu baris per percobaan (skenario 1)
  skenario2_mentah.csv         satu baris per percobaan (skenario 2)
  ringkasan_per_n.csv          rata-rata per skenario, n, dan algoritma
  ringkasan_per_algoritma.csv  rata-rata per skenario dan algoritma
  grafik_*.png                 grafik waktu, kualitas solusi, dan simpul B&B
docs/                          makalah dan slide presentasi
```

## Cara menjalankan
```
pip install -r requirements.txt
python src/preprocessing.py
python src/uji_contoh_slide.py
python src/uji_bnb_vs_brute_force.py
python src/eksperimen.py
```

Eksperimen: setiap kombinasi n × jenis kelamin dijalankan dengan 10 seed (sampel acak berbeda). Waktu Greedy dan B&B adalah median dari 5 kali pengulangan; Brute Force dijalankan sekali. Pembanding optimal di skenario 1 adalah Brute Force, di skenario 2 adalah Branch and Bound. Pada n = 1107 (seluruh data), setiap seed berisi makanan yang sama, jadi pengulangannya hanya mengulang pengukuran waktu.

## Batasan
- Model hanya memaksimalkan protein dengan batas kalori. Tidak ada batas atas protein, keseimbangan gizi lain, maupun variasi menu, sehingga total protein solusi optimal jauh melebihi kebutuhan harian. Hasilnya adalah pembanding kinerja algoritma, bukan rekomendasi diet.
- Setiap makanan dihitung tepat satu porsi 100 g (0/1), bukan porsi yang bisa diatur.
- Penyaringan data memakai kata kunci pada nama makanan, sehingga masih mungkin ada makanan yang kurang lazim yang lolos.

## Status
- [x] Preprocessing data
- [x] Brute Force
- [x] Greedy (by profit, by weight, by density)
- [x] Branch and Bound (best-first, bound dari fractional knapsack)
- [x] Eksperimen
- [ ] Artikel dan slide

## Anggota
- (nama – NIM)
- (nama – NIM)
- (nama – NIM)


## Jurnal tujuan
(diisi setelah jurnal dipilih)
