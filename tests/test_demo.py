import sys, unittest, tempfile
from pathlib import Path
import cv2
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import demo_engine as e

class DemoTests(unittest.TestCase):
 def test_scene_size(self):
  f=e.scene(6.5); self.assertEqual(f.shape,(450,800,3))
 def test_visible_subject_detected_from_processed_pixels(self):
  f=e.enhance(e.degrade(e.scene(4.5),54)); found=e.detect_by_color(f)
  self.assertIn('person',found);self.assertIn('helmet',found)
 def test_helmet_location_changes(self):
  a=e.detect_by_color(e.enhance(e.degrade(e.scene(1.),12)))['helmet']
  b=e.detect_by_color(e.enhance(e.degrade(e.scene(10.),120)))['helmet']
  center=lambda v: (v[0]+v[2])/2
  self.assertGreater(abs(center(a)-center(b)),80)
 def test_same_width_height_reference_processed(self):
  f=e.scene(2.); g=e.degrade(f,24);h=e.enhance(g)
  self.assertEqual(f.shape,g.shape);self.assertEqual(g.shape,h.shape)
 def test_no_replaced_source_file(self):
  a=Path(__file__).resolve().parents[1]/'assets'
  original=e.sha256(a/'02_CCTV_BURAM_SIMULASI.mp4')
  with tempfile.TemporaryDirectory() as td:
   r=e.analyze_demo(a,td)
   self.assertEqual(e.sha256(a/'02_CCTV_BURAM_SIMULASI.mp4'),original)
   self.assertEqual(r['sha256_video_masukan'],original)
   self.assertEqual(r['hasil_deteksi_piksel']['frame_total'],144)
   self.assertGreater(r['hasil_deteksi_piksel']['frame_terdeteksi_orang'],100)
   self.assertGreater(r['hasil_deteksi_piksel']['frame_terdeteksi_helm'],100)
   self.assertGreater(r['pengukuran_referensi_sintetis']['rata_rata_psnr_video_olahan_db'],r['pengukuran_referensi_sintetis']['rata_rata_psnr_video_buram_db'])
   self.assertTrue(Path(td,'09_KEPALA_SIMULASI_OLAHAN.png').exists())
   cap=cv2.VideoCapture(str(Path(td,'04_PERBANDINGAN.mp4')))
   ok,frame=cap.read();cap.release()
   self.assertTrue(ok);self.assertEqual(frame.shape[:2],(450,1600))
 def test_no_identity_or_real_person_in_model_report(self):
  self.assertIn('fiktif',e.SCENE_DETAILS['kode_subjek'].lower())
  self.assertIn('Tidak tersedia',e.SCENE_DETAILS['identitas'])

if __name__=='__main__':unittest.main()
