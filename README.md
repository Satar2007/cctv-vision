# CCTV Vision Wonogiri — Prototipe Simulasi

Aplikasi demonstrasi **Streamlit + OpenCV** untuk karya tulis inovasi SIMAPRES Wonogiri 2026: *Rancangan Sistem Peningkatan Keterlihatan dan Deteksi Objek pada Rekaman CCTV Berkualitas Rendah di Kabupaten Wonogiri*.

> **DEMO FIKTIF, BUKAN PENYELIDIKAN NYATA.** Subjek `S-01`, sepeda motor, dan peristiwa helm seluruhnya dibuat secara sintetis. Informasi ciri pakaian dan linimasa berasal dari naskah simulasi, **bukan hasil prediksi identitas, pengenalan wajah, atau kesimpulan bersalah**. Deteksi orang dan helm di demo ini menggunakan **segmentasi warna HSV OpenCV** yang khusus diatur untuk objek ilustrasi. Tidak boleh diartikan sebagai kemampuan deteksi generik pada rekaman CCTV sungguhan.

## Fitur yang benar-benar bekerja

- **Satu tombol** untuk pemrosesan video simulasi 12 detik (144 frame, 800×450, 12 fps).
- Peningkatan pencahayaan/kontras menggunakan gamma, CLAHE, denoising dan penajaman terkendali.
- Segmentasi warna jaket dan helm pada video ilustrasi; kotak deteksi adalah hasil pemrosesan piksel, bukan anotasi yang digambar manual.
- Video sebelum–sesudah, galeri foto objek dan ilustrasi area kepala, linimasa **dari skenario**, ekspor video/gambar/JSON.
- Perhitungan PSNR relatif terhadap video referensi sintetis, bukan tolok ukur hasil pada CCTV nyata.
- SHA-256 video sumber untuk memastikan file input tidak berubah.

## Menjalankan pada Windows

**Paling cepat:** ekstrak ZIP, klik dua kali `BUKA_DEMO.bat`. Script akan menggunakan virtual environment Python yang sudah ada dari CCTV Vision terdahulu jika tersedia, atau membuat `.venv` menggunakan Python 3.11. Buka http://localhost:8502 jika browser belum terbuka.

Atau jalankan mandiri dengan PowerShell dari folder proyek:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8502
```

**Linux/macOS:**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8502
```

Jalankan pengujian otomatis:

```bash
python -m unittest discover -s tests -v
```

## Struktur repo

```
app.py                 antarmuka Streamlit
demo_engine.py         generator simulasi, OpenCV, hasil dan laporan
assets/                dua video masukan sintetis (boleh didistribusikan)
tests/                 pengujian otomatis
.github/workflows/     pemeriksaan sintaks dan pengujian CI
BUKA_DEMO.bat          jalankan aplikasi pada Windows
requirements.txt       dependensi utama
```

## Batasan penting

- **Tidak** mengidentifikasi seseorang, tidak menyimpulkan motif/tindak pidana, tidak mengenali wajah, dan tidak memulihkan detail yang tidak terekam.
- Contoh fokus kepala adalah **gambar ilustratif** dari model grafis. Bukan foto wajah pelaku.
- Linimasa pengambilan helm dibuat sebelum video dianalisis (ground truth skenario).
- PSNR yang meningkat pada satu simulasi **tidak** membuktikan akurasi pada rekaman nyata atau hasil deteksi YOLO.
- Jangan memasukkan CCTV atau data pribadi orang sungguhan ke GitHub; buat data uji dengan izin dan lakukan peninjauan privasi terlebih dahulu.

## Reproduksibilitas

Hasil tersimpan di `hasil_demo/` (diabaikan Git). Hapus folder itu sebelum pengujian ulang jika ingin membandingkan output. Video contoh diproses secara lokal, tanpa mengunggah ke server pihak ketiga.

## Rencana pengembangan

- Pengujian dengan relawan dan rekaman berizin.
- Pemisahan modul deteksi umum YOLO (belum divalidasi dalam demo ini) dari deteksi warna sintetis.
- Dataset beranotasi serta precision/recall/mAP, pengukuran SSIM, evaluasi artefak dan pengujian pengguna.
- Pengaturan manajemen akses bila nantinya dipakai di lingkungan operasional.

## Lisensi

MIT untuk kode sumber proyek. Video dan gambar sintetis disertakan untuk kebutuhan demonstrasi edukasi proyek ini.
