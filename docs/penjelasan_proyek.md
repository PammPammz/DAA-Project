# Penjelasan Proyek

Catatan ini kami tulis supaya semua anggota paham isi proyek dari awal sampai akhir, dan supaya waktu menulis artikel tinggal ambil bahan dari sini. Angka waktu di bagian hasil berasal dari laptop yang dipakai menjalankan eksperimen; kalau dijalankan di laptop lain, angka waktunya akan sedikit berbeda, tapi angka protein dan persentasenya akan sama persis karena sampelnya dikunci pakai seed.

## Masalah yang diangkat

Kami ingin memilih makanan yang total proteinnya paling besar tanpa melewati batas kalori. Setiap makanan dihitung satu porsi 100 gram, dan cuma ada dua pilihan: diambil atau tidak. Bentuk seperti ini persis 0/1 knapsack yang ada di materi Brute Force dan Greedy, hanya saja "barang" diganti makanan dan "tas" diganti batas kalori.

| Istilah knapsack | Di proyek ini |
| --- | --- |
| objek | makanan |
| berat (w) | kalori per 100 g |
| profit (p) | protein per 100 g |
| kapasitas (K) | batas kalori |

Model matematisnya:

$$\text{maksimasi } F = \sum_{i=1}^{n} p_i x_i \quad \text{dengan} \quad \sum_{i=1}^{n} w_i x_i \le K,\; x_i \in \{0, 1\}$$

Batas kalori diambil dari Angka Kecukupan Gizi (Permenkes No. 28 Tahun 2019) untuk usia 19–29 tahun: 2650 kkal untuk pria dan 2250 kkal untuk perempuan. Kami pakai dua versi kapasitas. Batas harian penuh dipakai untuk data besar, sedangkan untuk data kecil kami pakai batas sekali makan, yaitu AKG dibagi 3 (sekitar 883 kkal untuk pria dan 750 kkal untuk perempuan). Alasannya praktis: Brute Force cuma sanggup sampai sekitar 20 makanan, sedangkan rata-rata kalori di data kami 185 kkal per makanan. Sepuluh makanan totalnya sekitar 1850 kkal, jadi dengan kapasitas 2650 kkal semuanya muat dan perbandingannya tidak ada artinya.

## Data

Datasetnya "Indonesian Food and Drink Nutrition Dataset" dari Kaggle (anasfikrihanif). Isinya 1346 makanan dan minuman yang diambil dari Tabel Komposisi Pangan Indonesia (TKPI) Kemenkes, dengan nilai gizi per 100 gram. Dari 7 kolom yang ada, kami cuma pakai tiga: `name` jadi Nama barang, `calories` jadi berat, `proteins` jadi profit.

Data mentahnya tidak bisa langsung dipakai. Versi pertama kami cuma membuang data yang rusak, dan hasilnya B&B memilih menu harian berisi kura-kura, katak, darah sapi, dan udang kering mentah dengan total 588 g protein. Secara algoritma itu benar (memang itu jawaban optimalnya), tapi jelas bukan menu yang masuk akal. Jadi `preprocessing.py` sekarang membuang 239 baris dengan rincian berikut.

| Yang dibuang | Jumlah | Alasan |
| --- | --- | --- |
| kalori = 0 | 1 | greedy by density membagi protein dengan kalori |
| protein = 0 | 21 | tidak pernah menambah nilai solusi |
| tidak konsisten | 5 | 4 × protein > kalori, padahal 1 g protein = 4 kkal |
| bentuk tidak siap santap | 144 | nama mengandung mentah, kering, tepung, bubuk, atau serbuk |
| satwa dilindungi/liar | 6 | kura-kura, penyu, hiu, buaya, rusa, menjangan |
| tidak lazim dikonsumsi | 13 | keong, ulat sagu, kuda, sarang burung, bungkil, tempe bongkrek |
| non-halal | 19 | mayoritas calon pengguna beragama Islam |
| nama dobel | 30 | makanan sama dengan nama berbeda, misalnya "Kakap" dan "Ikan kakap segar" |

Aturan "bentuk tidak siap santap" paling banyak membuang data dan paling perlu dijelaskan di artikel. Di dataset ini, beras giling mentah tercatat 357 kkal per 100 g sedangkan nasi cuma 180 kkal, padahal yang dimakan orang adalah nasi; teri kering tawar (68,7 g protein per 100 g) dan susu bubuk juga jauh lebih pekat daripada porsi yang biasa dimakan. Karena model kami menganggap setiap makanan satu porsi 100 g, bentuk-bentuk seperti itu bikin hasilnya tidak realistis. Daftar lengkap baris yang dibuang beserta alasannya ada di `data/processed/data_dibuang.csv`, dan setiap aturan bisa dimatikan lewat `KRITERIA_PENGECUALIAN` di `preprocessing.py`. Hasil akhirnya 1107 makanan.

## Tiga algoritma yang dibandingkan

### Brute Force

Setiap makanan punya dua kemungkinan, jadi n makanan menghasilkan 2ⁿ kombinasi, dan Brute Force mengecek semuanya. Di kode, satu kombinasi diwakili satu bilangan biner: untuk 3 makanan, angka 5 (biner `101`) artinya makanan ke-1 dan ke-3 diambil. Loop dari 0 sampai 2ⁿ − 1, jumlahkan kalori dan proteinnya, lalu simpan kombinasi yang muat dan proteinnya paling besar. Ada 2ⁿ kombinasi dan masing-masing butuh n langkah, jadi kompleksitasnya O(n · 2ⁿ).

Waktu menguji kode dengan contoh di slide, kami menemukan satu kesalahan. Di slide Greedy Contoh 5 (kapasitas 100), jawaban optimal tertulis 53 dari objek 2 dan 3. Brute Force menemukan 55 dari objek 2, 3, dan 6, dengan berat 50 + 45 + 5 = 100, pas di kapasitas. Kami cek ulang dengan cara lain dan hasilnya tetap 55. Koreksi ini kami catat di `uji_contoh_slide.py`.

### Greedy

Urutkan makanan berdasarkan satu kriteria, lalu ambil satu per satu selama masih muat. Kalau ada yang tidak muat, lewati saja dan cek makanan berikutnya. Ada tiga strategi seperti di slide: by profit (protein terbesar dulu), by weight (kalori terkecil dulu), dan by density (protein per kalori terbesar dulu). Bagian paling berat adalah pengurutannya, jadi kompleksitasnya O(n log n). Greedy cepat sekali, tapi tidak menjamin optimal. Contoh 5 tadi buktinya: by density cuma dapat 51, padahal optimalnya 55.

### Branch and Bound

B&B memakai pohon yang sama dengan Brute Force (di level ke-i diputuskan makanan ke-i diambil atau tidak), bedanya ada pemangkasan. Setiap simpul diberi nilai bound, yaitu perkiraan optimis protein yang masih mungkin didapat dari cabang itu. Bound dihitung dengan fractional knapsack: sisa kapasitas diisi makanan dengan density terbesar, dan makanan terakhir boleh diambil sebagian. Karena versi "boleh diambil sebagian" tidak mungkin kalah dari versi utuh, bound tidak pernah meremehkan. Aturannya sederhana: kalau bound sebuah cabang tidak lebih besar dari solusi terbaik yang sudah ketemu, cabang itu dibuang.

Simpul yang diekspansi duluan adalah yang bound-nya paling besar. Di slide (contoh TSP) justru yang cost-nya paling kecil, karena TSP masalah minimasi sedangkan knapsack maksimasi. Simpul hidup disimpan di priority queue (`heapq`), dan bound-nya disimpan negatif karena `heapq` mengeluarkan nilai terkecil lebih dulu.

Di Contoh 5, urutan density-nya objek 5, 2, 1, 3, 6, 4 dan bound akarnya 61. B&B langsung turun mengambil objek 5 dan 2 (protein 45), lalu pindah ke cabang tanpa objek 5 yang bound-nya 55, mengambil objek 2 dan 3 (53), lalu menambah objek 6 (55). Setelah itu semua simpul hidup bound-nya ≤ 55, jadi pencarian berhenti. Totalnya cuma 8 simpul diekspansi dan 17 simpul dibangkitkan dari 127 simpul pohon penuh. Kasus terburuk B&B tetap O(2ⁿ); bound hanya membuatnya jauh lebih cepat dalam praktik.

Untuk memastikan B&B benar, `uji_bnb_vs_brute_force.py` membandingkan hasilnya dengan Brute Force di 60 sampel acak (n = 8, 12, 16), dan semuanya sama.

## Isi kode

```
data/raw/nutrition.csv           data asli dari Kaggle
data/processed/data_bersih.csv   hasil preprocessing (1107 baris)
data/processed/data_dibuang.csv  baris yang dibuang + alasannya
src/algoritma/                   brute_force.py, greedy.py, branch_and_bound.py
src/data_utils.py                baca data, ambil sampel, hitung kapasitas
src/preprocessing.py             bersihkan data
src/uji_contoh_slide.py          uji pakai contoh soal di slide
src/uji_bnb_vs_brute_force.py    uji B&B vs Brute Force
src/eksperimen.py                jalankan eksperimen, simpan CSV
src/grafik.py                    bikin grafik dari CSV
hasil/                           CSV dan grafik hasil eksperimen
```

Semua algoritma dipanggil dengan bentuk yang sama, `fungsi(berat, profit, kapasitas)`, dan mengembalikan `(x, total_profit, total_berat)` dengan x berupa vektor 0/1 seperti notasi di slide. Daftarnya ada di `src/algoritma/__init__.py`. Urutan menjalankannya:

```
pip install -r requirements.txt
python src/preprocessing.py
python src/uji_contoh_slide.py
python src/uji_bnb_vs_brute_force.py
python src/eksperimen.py
```

## Desain eksperimen

| | Skenario 1 | Skenario 2 |
| --- | --- | --- |
| algoritma | Brute Force, Greedy (3 strategi), B&B | Greedy (3 strategi), B&B |
| jumlah makanan (n) | 10, 12, 14, 16, 18, 20 | 100, 250, 500, 750, 1107 |
| kapasitas | sekali makan (883 / 750 kkal) | harian (2650 / 2250 kkal) |
| pembanding optimal | Brute Force | B&B |

Setiap kombinasi n dan jenis kelamin dijalankan dengan 10 seed, sehingga skenario 1 punya 120 percobaan per algoritma dan skenario 2 punya 100. Di skenario 2 Brute Force tidak ikut karena 2¹⁰⁰ kombinasi jelas mustahil dihitung; pembandingnya B&B, yang sudah terbukti selalu sama dengan Brute Force. Yang dicatat tiap percobaan: total protein, total kalori, jumlah makanan yang dipilih, waktu eksekusi, persentase protein terhadap optimal, dan jumlah simpul B&B. Waktu Greedy dan B&B adalah median dari 5 kali pengulangan karena keduanya terlalu cepat untuk diukur sekali; Brute Force cukup sekali.

Satu catatan: di n = 1107 sampelnya selalu berisi seluruh data, jadi 10 seed di sana cuma mengulang pengukuran waktu.

## Hasil

Lingkungan pengujian: (isi spesifikasi laptop: prosesor, RAM, versi Python).

Kualitas solusi, dihitung sebagai rata-rata protein dibanding solusi optimal:

| Algoritma | Skenario 1 | Optimal di skenario 1 | Skenario 2 | Terendah di skenario 2 |
| --- | --- | --- | --- | --- |
| Brute Force | 100% | 120/120 | (tidak dijalankan) | (tidak dijalankan) |
| Greedy by profit | 93,3% | 45/120 | 69,9% | 54,7% |
| Greedy by weight | 58,6% | 0/120 | 35,5% | 25,4% |
| Greedy by density | 95,7% | 64/120 | 99,8% | 97,9% |
| Branch and Bound | 100% | 120/120 | 100% | 100% |

Waktu Brute Force naik sekitar 4,4–4,6 kali setiap n bertambah 2, dari 0,49 ms di n = 10 menjadi 879 ms di n = 20. Pola ini cocok dengan O(n · 2ⁿ): menambah 2 makanan berarti jumlah kombinasi jadi 4 kali lipat, ditambah sedikit karena n-nya ikut bertambah. Di n = 20, B&B hanya butuh 0,023 ms (sekitar 37.900 kali lebih cepat) dan rata-rata hanya membangkitkan 77 simpul dari 2.097.151 simpul pohon penuh.

Di skenario 2, B&B tetap optimal dengan rata-rata waktu di bawah 1 ms untuk setiap n (0,12 ms di n = 100, 0,83 ms di n = 750); percobaan paling lama pun cuma 1,4 ms. Ada satu hal yang menarik: waktu di n = 750 lebih lama daripada di n = 1107 (0,66 ms), karena di n = 750 B&B membangkitkan rata-rata 2504 simpul sedangkan di n = 1107 cuma 1642. Artinya waktu B&B tidak cuma bergantung pada jumlah data, tapi juga pada seberapa cepat bound bisa memangkas cabang untuk data tertentu. Greedy sekitar 4–14 kali lebih cepat dari B&B, tapi selisihnya di bawah 1 ms.

Untuk Greedy, strategi terbaik bergantung pada kondisinya. Di n kecil dengan batas per makan, by profit sedikit lebih baik di n = 10 dan 12 (98,2% dan 97,1%), lalu disusul by density mulai n = 14. Di batas harian, by profit turun ke sekitar 70%, sedangkan by density tidak pernah di bawah 97,9% di satu percobaan pun. Dugaan kami, by profit memilih makanan yang proteinnya besar tapi kalorinya juga besar, sehingga kapasitas cepat habis; rata-rata cuma 6,9 makanan yang terpilih di skenario 2, padahal B&B memilih 22. By weight kebalikannya: ia mengambil rata-rata 74,7 makanan berkalori rendah, yang ternyata kebanyakan juga rendah protein (sayur dan buah), sehingga hasilnya paling jelek di kedua skenario.

Grafik untuk artikel ada di folder `hasil/`: `grafik_waktu_skenario1.png`, `grafik_waktu_skenario2.png`, `grafik_kualitas.png`, dan `grafik_simpul_bnb.png`.

## Batasan

Model ini cuma memaksimalkan protein dengan batas kalori. Tidak ada batas atas protein, keseimbangan gizi lain, atau aturan variasi menu, sehingga menu harian optimal untuk pria berisi 28 porsi dengan total 545,6 g protein, jauh di atas kebutuhan sekitar 65 g. Hasil proyek ini adalah pembanding kinerja algoritma, bukan rekomendasi diet, dan hal itu perlu ditulis jelas di artikel.

Porsi setiap makanan juga dikunci 100 g, padahal di dunia nyata porsi bisa diatur. Penyaringan data pun memakai kata kunci pada nama makanan, jadi masih mungkin ada makanan kurang lazim yang lolos. Terakhir, waktu diukur di Python pada satu laptop, sehingga angka absolutnya bergantung pada mesin; yang lebih penting dibaca adalah perbandingan dan polanya.

## Dari proyek ke artikel

| Bagian artikel | Bahan dari proyek |
| --- | --- |
| Pendahuluan | masalah memilih makanan tinggi protein dengan batas kalori; kenapa perlu algoritma yang tepat; tujuan membandingkan 3 algoritma |
| Tinjauan Pustaka | 0/1 knapsack, Brute Force, Greedy (3 strategi), Branch and Bound, fractional knapsack sebagai bound; penelitian sejenis |
| Metode: data | sumber dataset, tabel preprocessing di atas |
| Metode: model | tabel pemetaan knapsack dan rumus maksimasi |
| Metode: algoritma | penjelasan tiap algoritma, kompleksitas, contoh Contoh 5 (termasuk jalannya B&B) |
| Metode: eksperimen | tabel desain eksperimen, cara mengukur waktu, lingkungan pengujian |
| Hasil dan Pembahasan | tabel kualitas solusi, keempat grafik, temuan di bagian Hasil |
| Kesimpulan | B&B selalu optimal dan tetap cepat sampai 1107 makanan; Greedy by density paling mendekati optimal; Brute Force hanya layak untuk n kecil |

Batasan bisa masuk di akhir Pembahasan atau sebagai subbab sendiri, tergantung template jurnal yang dipilih.

## Pertanyaan yang mungkin muncul

**Kenapa tidak pakai Dynamic Programming?** DP memang cara standar untuk 0/1 knapsack, dengan kompleksitas O(n · K). Waktu kami menyusun proyek, DP belum diajarkan, jadi kami memakai algoritma yang sudah ada di materi. Kalori di data juga ada yang desimal, sehingga DP butuh pembulatan dulu (misalnya dikali 10), sedangkan B&B bisa langsung dipakai dan hasilnya sudah dicek sama dengan Brute Force. DP bisa jadi saran untuk penelitian berikutnya.

**Kenapa kapasitas skenario 1 dibagi 3?** Supaya perbandingan dengan Brute Force bermakna. Dengan batas harian penuh, 10 makanan (sekitar 1850 kkal) semuanya muat, jadi setiap algoritma otomatis "optimal" dan tidak ada yang bisa dibandingkan. Batas sekali makan juga masuk akal dipakai sehari-hari.

**Kenapa memakai seed?** Supaya sampel acaknya selalu sama. Semua algoritma diuji dengan makanan yang sama, dan orang lain bisa mengulang eksperimen dengan hasil yang sama.

**Greedy by density kan optimal untuk fractional knapsack, kenapa di sini tidak selalu optimal?** Di fractional knapsack makanan terakhir boleh diambil sebagian, sedangkan di 0/1 tidak. Sisa kapasitas yang tidak terisi itulah yang membuat by density kadang kalah dari solusi optimal. Kapasitas harian cukup besar untuk sekitar 20 makanan, jadi sisa yang terbuang relatif kecil dibanding totalnya; kemungkinan itu sebabnya by density hampir selalu mendekati 100% di skenario 2.
