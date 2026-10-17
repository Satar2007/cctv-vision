# Pengujian dan Reproduksibilitas

## Perintah pengujian

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Workflow GitHub Actions berada di `.github/workflows/tests.yml`; hasil status CI **harus dilihat di halaman Actions setelah push**, dan tidak boleh diasumsikan sukses hanya dari hasil lokal.

## Lingkup tes otomatis

Enam pengujian di `tests/test_demo.py` memeriksa: dimensi frame, kesesuaian referensi dan hasil, perubahan posisi helm sintetis, deteksi subjek berdasarkan piksel, integritas berkas sumber, dan batasan informasi identitas di laporan.

**Hasil lokal saat menyiapkan paket dokumentasi:** 6 tes lulus pada lingkungan Linux; ini bukan pernyataan bahwa GitHub Actions sudah hijau.

## Interpretasi hasil

- Video masukan berdurasi 12 detik, resolusi 800×450, 12 FPS (144 frame).
- Evaluasi PSNR menggunakan frame sampel dan referensi sintetis. PSNR tidak menggantikan pengukuran ketepatan deteksi pada data dunia nyata.
- Deteksi warna pada karakter sintetis bukan pendeteksi orang universal.
- Tidak ada dataset CCTV riil, precision, recall, mAP atau evaluasi forensik dalam versi ini.

## Validasi manual sebelum rilis

1. Jalankan `BUKA_DEMO.bat` di Windows.
2. Buka `http://localhost:8502` dan pastikan video simulasi muncul.
3. Klik **JALANKAN ANALISIS OTOMATIS**.
4. Pastikan video perbandingan, metrik, crop dan linimasa tampil.
5. Unduh ZIP hasil dan pastikan berkas MP4/PNG/JSON dapat dibuka.
6. Pastikan label fiktif tetap terlihat dan tidak ada rekaman orang nyata di repository.
