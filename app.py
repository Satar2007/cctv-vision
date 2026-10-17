"""Streamlit CCTV Vision SIMAPRES educational fictional scenario, single-button demo."""
from pathlib import Path
import io, json, zipfile
import cv2
import streamlit as st
from demo_engine import analyze_demo, generate_inputs, SCRIPT_EVENTS, SCENE_DETAILS

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT/'assets'
RESULTS = ROOT/'hasil_demo'

st.set_page_config(page_title='CCTV Vision | Simulasi Interaktif',page_icon='🎥',layout='wide',initial_sidebar_state='collapsed')
st.markdown('''<style>
.block-container {max-width:1120px; padding-top: 2.3rem;}
h1,h2,h3{letter-spacing:-.02em;}
.stButton>button[kind="primary"] {background:#0b9c82; border:0; min-height:3.2rem; font-size:1.07rem; font-weight:750;}
[data-testid="stMetricValue"] {font-size:1.8rem;}
</style>''',unsafe_allow_html=True)

st.caption('SIMAPRES WONOGIRI 2026  /  PROTOTIPE EDUKASI INFORMATIKA')
st.title('CCTV Vision — Demo Investigasi Simulasi')
st.markdown('**Satu tombol untuk menganalisis adegan parkiran fiktif**, memperbaiki keterlihatan video, memberi kotak deteksi, dan menampilkan ringkasan subjek S-01.')
st.warning('**SIMULASI FIKTIF.** Subjek S-01 adalah karakter digital, bukan orang nyata. Detail pakaian dan alur pengambilan helm berasal dari skenario buatan. Deteksi menggunakan pemrosesan piksel OpenCV khusus simulasi, **bukan identifikasi pelaku atau wajah sungguhan**.')

if not (ASSETS/'02_CCTV_BURAM_SIMULASI.mp4').is_file():
    with st.spinner('Menyiapkan video simulasi pertama kali...'):
        generate_inputs(ASSETS)

st.subheader('01  ·  Rekaman CCTV simulasi')
st.video(str(ASSETS/'02_CCTV_BURAM_SIMULASI.mp4'))
st.caption('Durasi 12 detik; adegan ilustrasi: subjek berjaket marun, motor terparkir, dan helm kuning.')

if st.button('▶  JALANKAN ANALISIS OTOMATIS',type='primary',use_container_width=True):
    try:
        with st.spinner('Menjalankan OpenCV: membaca video, meningkatkan keterlihatan, mendeteksi warna objek, menyusun galeri dan laporan...'):
            report=analyze_demo(ASSETS,RESULTS)
        st.session_state['simapres_demo_report']=report
        st.success('Analisis selesai! Hasil deteksi dan detail skenario muncul di bawah.')
    except Exception as exc:
        st.error(f'Gagal melakukan analisis: {exc}')

report=st.session_state.get('simapres_demo_report')
if not report:
    st.info('Klik **JALANKAN ANALISIS OTOMATIS** untuk memunculkan video hasil, foto objek, dan laporan subjek.')
    st.stop()

st.divider()
st.subheader('02  ·  Video setelah analisis berjalan')
st.video(str(RESULTS/'04_PERBANDINGAN.mp4'))
st.caption('Kiri: video simulasi buram. Kanan: peningkatan citra dan kotak deteksi person/helm dari segmentasi warna pada frame video.')

stats=report['hasil_deteksi_piksel'];quality=report['pengukuran_referensi_sintetis']
a,b,c,d=st.columns(4)
a.metric('Frame diproses',stats['frame_total'])
b.metric('Frame memuat orang',stats['frame_terdeteksi_orang'])
c.metric('Frame memuat helm',stats['frame_terdeteksi_helm'])
d.metric('Perpindahan helm', 'Teramati' if stats['perubahan_posisi_helm_teramati'] else 'Belum teramati')

st.subheader('03  ·  Foto dan detail subjek simulasi S-01')
left,right=st.columns([1,1.2],gap='large')
with left:
    st.image(str(RESULTS/'06_OBJEK_DIPERTAJAM.png'),caption='Subjek S-01 · crop hasil peningkatan',use_container_width=True)
    st.image(str(RESULTS/'09_KEPALA_SIMULASI_OLAHAN.png'),caption='Area kepala/wajah ILUSTRASI · bukan restorasi identitas',use_container_width=True)
with right:
    st.markdown('#### Ringkasan visual dan skenario')
    st.markdown('**Kode objek:** S-01 · karakter digital')
    st.markdown('**Pakaian:** jaket merah marun, celana gelap')
    st.markdown('**Bagian kepala:** rambut gelap; wajah berupa ilustrasi, bukan citra orang sebenarnya')
    st.markdown('**Kendaraan di lokasi:** satu sepeda motor ilustratif')
    st.markdown('**Barang dalam skenario:** helm kuning')
    st.markdown('**Peristiwa:** dalam naskah simulasi, karakter mengambil helm dari area parkir dan membawanya menjauh')
    st.markdown('**Identitas dan kesalahan hukum:** tidak ditentukan; seluruh kejadian fiktif')
    st.caption('Ciri pakaian dan cerita berasal dari rancangan simulasi. Perangkat lunak menguji keberadaan area merah (jaket) dan kuning (helm) berdasarkan piksel.')

st.markdown('#### Bukti visual sebelum–sesudah (adegan simulasi)')
col1,col2,col3=st.columns(3)
col1.image(str(RESULTS/'05_OBJEK_ASLI.png'),caption='Objek dari video buram',use_container_width=True)
col2.image(str(RESULTS/'06_OBJEK_DIPERTAJAM.png'),caption='Hasil peningkatan OpenCV',use_container_width=True)
col3.image(str(RESULTS/'07_OBJEK_REFERENSI.png'),caption='Referensi sintetis yang diketahui',use_container_width=True)

st.subheader('04  ·  Linimasa skenario')
for event in SCRIPT_EVENTS:
    st.markdown(f"**{event['mulai']:04.1f}–{event['akhir']:04.1f} detik**  ·  {event['kejadian']}")
st.caption('Linimasa ini adalah anotasi skenario yang diketahui terlebih dahulu, **bukan inferensi kriminalitas oleh AI**.')

st.subheader('05  ·  Validasi pengolahan citra')
q1,q2,q3=st.columns(3)
q1.metric('PSNR video buram',f"{quality['rata_rata_psnr_video_buram_db']:.2f} dB")
q2.metric('PSNR video olahan',f"{quality['rata_rata_psnr_video_olahan_db']:.2f} dB")
q3.metric('Peningkatan PSNR',f"{quality['rata_rata_psnr_video_olahan_db']-quality['rata_rata_psnr_video_buram_db']:.2f} dB")
st.caption('Metrik ini dibandingkan dengan video referensi buatan, pada 12 frame sampel (1 fps) hasil decode MP4. Tidak membuktikan keberhasilan rekonstruksi wajah maupun akurasi deteksi pada CCTV nyata.')

st.subheader('06  ·  Unduh hasil analisis')
items=[RESULTS/'03_VIDEO_HASIL_ANALISIS.mp4',RESULTS/'04_PERBANDINGAN.mp4',RESULTS/'laporan_simulasi.json']
items+=list(RESULTS.glob('*.png'))
def create_zip():
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as z:
        for item in items:
            if item.exists():z.write(item,arcname=item.name)
    return buf.getvalue()
st.download_button('⬇ UNDUH HASIL ANALISIS (ZIP)',data=create_zip(),file_name='CCTV_Vision_SIMAPRES_Hasil_Demo.zip',mime='application/zip',use_container_width=True)
with st.expander('Lihat laporan JSON dan batasan analisis'):
    st.json(report)
    st.caption('Untuk KTI: ini proof-of-concept pada objek ilustratif dengan segmentasi warna, bukan uji YOLO pada orang sungguhan. Pengujian CCTV nyata dan izin akses masih diperlukan sebelum implementasi lapangan.')
