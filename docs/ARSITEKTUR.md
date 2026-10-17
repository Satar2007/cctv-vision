# Arsitektur Prototipe CCTV Vision Wonogiri

## Ruang lingkup

Proyek ini adalah demonstrasi **lokal, sintetis, dan edukatif**. Input yang disediakan berisi adegan buatan, bukan rekaman CCTV peristiwa asli. Antarmuka menggunakan Streamlit (`app.py`); mesin pemrosesan terdapat di `demo_engine.py`.

## Jalur data

1. `assets/01_REFERENSI_SIMULASI.mp4` merupakan referensi sintetis untuk evaluasi PSNR.
2. `assets/02_CCTV_BURAM_SIMULASI.mp4` merupakan video yang didegradasi secara terkontrol.
3. Tombol *Jalankan Analisis Otomatis* memanggil `analyze_demo(assets, hasil_demo)`.
4. Setiap frame diproses menggunakan koreksi gamma, CLAHE, bilateral filtering, dan penajaman.
5. `detect_by_color` melakukan segmentasi HSV pada warna yang telah ditentukan untuk pakaian dan helm fiktif. Area subjek diterjemahkan menjadi kotak pembatas untuk ilustrasi.
6. Video hasil, perbandingan, crop dan laporan JSON ditulis ke folder `hasil_demo/`, yang dikecualikan oleh `.gitignore`.
7. Nilai PSNR dibandingkan terhadap referensi sintetis pada sampel frame tertentu, **bukan** terhadap ground truth CCTV nyata.

## Batasan interpretasi

- Deskripsi pakaian dan urutan peristiwa berasal dari skenario pra-rancang, **bukan klasifikasi semantik otomatis**.
- Kotak deteksi mengindikasikan area piksel dengan warna spesifik, **bukan hasil model YOLO**.
- Peningkatan kualitas gambar tidak menambahkan informasi identitas yang belum terekam.
- Jangan menjadikan keluaran sebagai bukti identitas atau tindak pidana.
- Pemrosesan tetap berlangsung pada komputer lokal; tidak ada API eksternal pada alur pemrosesan inti.

## Modul dan data

| Berkas | Tanggung jawab |
|---|---|
| `app.py` | Dashboard, pemicu analisis, visualisasi, ekspor |
| `demo_engine.py` | Sintesis, peningkatan citra, segmentasi, metrik, laporan |
| `assets/*.mp4` | Dataset simulasi yang disertakan |
| `tests/test_demo.py` | Unit test integritas dan fungsi simulasi |
| `.github/workflows/tests.yml` | Pengujian otomatis di GitHub Actions |

## Rencana riset selanjutnya

Integrasi detektor generik dan evaluasi pada data berizin harus menjadi eksperimen terpisah, dengan metrik precision, recall dan mAP serta analisis risiko privasi. Belum menjadi bagian dari demonstrasi yang diklaim selesai.
