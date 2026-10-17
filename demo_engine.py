"""CCTV Simapres: demonstration with fictional illustrated characters.

All scene annotations come from the synthetic screenplay and MUST NOT be
mistaken for an AI prediction of identity, criminality or real-world events.
Actual pixel processing: degradation, CLAHE/gamma enhancement, HSV segmentation,
contour detection, tracking through sampling, ROI export, PSNR versus known
synthetic source. No face generation or identity recognition.
"""
from __future__ import annotations
import cv2
import numpy as np
from pathlib import Path
import json, hashlib, shutil

W, H, FPS, DUR = 800, 450, 12, 12
YELLOW=(32,212,248)  # BGR yellow helmet
RED=(59,65,199)      # BGR red jacket
INK=(45,54,61)
SCENE_DETAILS={
    'kode_subjek': 'S-01 (tokoh fiktif)',
    'pakaian_atas': 'Jaket merah marun',
    'pakaian_bawah': 'Celana gelap',
    'rambut_kepala': 'Rambut gelap; wajah berupa ilustrasi',
    'barang_dalam_skenario': 'Helm kuning',
    'lokasi': 'Parkiran ilustratif (bukan lokasi kejadian nyata)',
    'identitas': 'Tidak tersedia; tokoh digital, bukan orang sungguhan',
}
SCRIPT_EVENTS=[
    {'mulai':0.0,'akhir':4.5,'kejadian':'S-01 berjalan memasuki area parkir'},
    {'mulai':4.5,'akhir':6.0,'kejadian':'S-01 mendekati sepeda motor'},
    {'mulai':6.0,'akhir':7.2,'kejadian':'Dalam skenario, S-01 mengambil helm kuning dari motor'},
    {'mulai':7.2,'akhir':12.0,'kejadian':'S-01 bergerak menjauh sambil membawa helm'},
]

def write_text(img, text, x, y, scale=.5, color=(244,244,244), thickness=1):
    cv2.putText(img,str(text),(int(x),int(y)),cv2.FONT_HERSHEY_SIMPLEX,scale,color,thickness,cv2.LINE_AA)

def subject_x(t):
    if t < 5.0: return int(120 + 59*t)
    if t < 7.0: return 415
    return max(110,int(415-60*(t-7)))

def circle(img, center, radius, color, thick=-1):
    cv2.circle(img,(int(center[0]),int(center[1])),int(radius),color,thick,cv2.LINE_AA)

def scene(t):
    img=np.zeros((H,W,3),np.uint8)
    img[:]=(86,102,107)
    # wall and forecourt
    cv2.rectangle(img,(0,0),(W,270),(122,139,149),-1)
    cv2.rectangle(img,(0,270),(W,H),(106,111,114),-1)
    # calm neutral background, no red/yellow clutter
    cv2.rectangle(img,(44,90),(142,266),(80,100,110),-1)
    cv2.rectangle(img,(51,99),(135,254),(153,165,172),-1)
    cv2.rectangle(img,(660,94),(745,258),(74,91,102),-1)
    cv2.rectangle(img,(666,100),(739,251),(151,167,174),-1)
    cv2.line(img,(0,270),(W,270),(61,76,81),5)
    for x in range(-60,850,110): cv2.line(img,(x,280),(x-55,H),(130,135,133),1,cv2.LINE_AA)
    for y in (330,390): cv2.line(img,(0,y),(W,y),(126,130,131),1,cv2.LINE_AA)
    cv2.line(img,(85,332),(85,430),(230,230,228),4)
    cv2.line(img,(730,332),(730,430),(230,230,228),4)
    # motorcycle: dark blue body; static
    cv2.ellipse(img,(531,399),(126,15),0,0,360,(84,92,94),-1)
    for cx in (454,622):
        circle(img,(cx,370),43,(22,32,42));circle(img,(cx,370),31,(165,174,181),4)
        circle(img,(cx,370),12,(76,86,92))
    cv2.line(img,(454,370),(511,284),(38,49,60),12)
    cv2.line(img,(511,284),(622,370),(38,49,60),12)
    cv2.line(img,(454,370),(570,347),(41,51,61),11)
    pts=np.array([[493,306],[511,270],[568,280],[610,324],[567,342],[497,334]],np.int32)
    cv2.fillPoly(img,[pts],(103,72,49));cv2.polylines(img,[pts],True,(57,51,48),4)
    cv2.ellipse(img,(537,265),(75,14),0,0,360,(33,41,46),-1)
    cv2.line(img,(622,367),(641,278),(37,43,50),7)
    cv2.line(img,(637,278),(674,278),(36,43,51),6)
    write_text(img,'PARKIR MOTOR',340,250,.45,(240,240,241),1)
    # person, red upper garment, dark pants; fictional vector-illustration
    x=subject_x(t)
    dx=int(np.sin(t*5)*7) if (t<5 or t>7) else 0
    cv2.ellipse(img,(x,413),(52,10),0,0,360,(77,83,87),-1)
    cv2.line(img,(x-17,307),(x-22+dx,404),(34,38,45),23)
    cv2.line(img,(x+17,307),(x+23-dx,404),(39,43,51),23)
    cv2.line(img,(x-22+dx,400),(x-34+dx,408),(36,40,48),8)
    cv2.line(img,(x+23-dx,400),(x+35-dx,408),(36,40,48),8)
    cv2.rectangle(img,(x-41,204),(x+41,314),RED,-1)
    cv2.ellipse(img,(x,205),(44,15),0,180,360,RED,-1)
    cv2.line(img,(x-37,213),(x-55-dx,278),(53,62,188),18,cv2.LINE_AA)
    cv2.line(img,(x+37,213),(x+55+dx,278),(53,62,188),18,cv2.LINE_AA)
    cv2.line(img,(x-10,206),(x+12,308),(64,72,90),4)
    # neck / illustrative face, with short black hair
    cv2.rectangle(img,(x-12,183),(x+12,211),(112,158,206),-1)
    cv2.ellipse(img,(x,153),(38,48),0,0,360,(139,177,210),-1)
    cv2.ellipse(img,(x,123),(38,20),0,180,360,(34,43,50),-1)
    cv2.ellipse(img,(x-35,151),(9,25),0,250,110,(34,43,50),-1)
    circle(img,(x-13,152),4,(35,43,50));circle(img,(x+13,152),4,(35,43,50))
    cv2.line(img,(x,157),(x-3,170),(86,127,163),2)
    cv2.ellipse(img,(x,180),(11,4),0,0,180,(78,99,125),2)
    # helmet transferred after 6 seconds; this is scene truth, NOT model inference
    if t<6:
        hx,hy=548,249
    elif t<7:
        a=t-6
        hx=int(548*(1-a)+(x+55)*a);hy=int(249*(1-a)+268*a)
    else:
        hx,hy=x+56+dx,269
    cv2.ellipse(img,(hx,hy),(26,23),0,190,520,YELLOW,-1)
    cv2.ellipse(img,(hx+5,hy+4),(14,8),0,350,180,(42,59,64),-1)
    cv2.ellipse(img,(hx,hy),(26,23),0,180,350,(8,148,197),2)
    # overlay
    cv2.rectangle(img,(0,0),(W,60),(25,35,39),-1)
    write_text(img,'CCTV VISION | SIMULASI - BUKAN REKAMAN ASLI',18,24,.64,(249,252,252),2)
    write_text(img,'Skenario fiktif: pengambilan helm di area parkir',19,47,.44,(199,221,227))
    cv2.rectangle(img,(0,H-29),(W,H),(31,40,46),-1)
    write_text(img,'DEMO PENGOLAHAN CITRA - KARAKTER DIGITAL',18,H-9,.45,(232,239,243))
    write_text(img,f'00:{int(t):02d}.{int((t%1)*10):01d}',W-104,H-9,.53,(242,242,242))
    return img

def degrade(frame,seed):
    h,w=frame.shape[:2]
    small=cv2.resize(frame,(int(w*.64),int(h*.64)),interpolation=cv2.INTER_AREA)
    small=cv2.GaussianBlur(small,(5,5),.8)
    z=cv2.resize(small,(w,h),interpolation=cv2.INTER_LINEAR).astype(np.float32)*.63+5
    rng=np.random.default_rng(1000+seed)
    z=np.clip(z+rng.normal(0,5.7,(h,w,1)),0,255).astype(np.uint8)
    ok,j=cv2.imencode('.jpg',z,[cv2.IMWRITE_JPEG_QUALITY,47])
    if not ok: raise RuntimeError('JPEG simulasi gagal')
    return cv2.imdecode(j,cv2.IMREAD_COLOR)

def enhance(frame):
    lut=np.clip((np.arange(256,dtype=np.float32)/255.)**.75*255.,0,255).astype(np.uint8)
    a=cv2.LUT(frame,lut)
    lab=cv2.cvtColor(a,cv2.COLOR_BGR2LAB)
    l,aa,bb=cv2.split(lab)
    l=cv2.createCLAHE(clipLimit=1.65,tileGridSize=(8,8)).apply(l)
    a=cv2.cvtColor(cv2.merge((l,aa,bb)),cv2.COLOR_LAB2BGR)
    a=cv2.bilateralFilter(a,5,22,22)
    blur=cv2.GaussianBlur(a,(0,0),.8)
    return cv2.addWeighted(a,1.1,blur,-.1,0)

def detect_by_color(frame):
    """Actual HSV detection on visual pixels; tailored to synthetic demo colors."""
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # Red/maroon jacket
    red=(cv2.inRange(hsv,np.array([0,60,60]),np.array([13,255,255])) |
         cv2.inRange(hsv,np.array([169,60,60]),np.array([179,255,255])))
    yellow=cv2.inRange(hsv,np.array([16,85,65]),np.array([42,255,255]))
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    results={}
    for key,mask,min_a in [('person',red,420),('helmet',yellow,65)]:
        # Limit red to main scenery, exclude header and floor
        mask[:78]=0
        mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
        mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
        contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        possibilities=[]
        for c in contours:
            x,y,w,h=cv2.boundingRect(c);area=cv2.contourArea(c)
            if area>=min_a and w>8 and h>7:possibilities.append((area,(x,y,x+w,y+h)))
        if possibilities: results[key]=max(possibilities,key=lambda x:x[0])[1]
    return results

def full_person_box(box,shape):
    h,w=shape[:2]; x1,y1,x2,y2=box
    pad=int(max(20,(x2-x1)*.14))
    return (max(0,x1-pad),max(0,y1-102),min(w,x2+pad),min(h,y2+116))

def crop(img,box):
    x1,y1,x2,y2=[int(z) for z in box]
    return img[max(0,y1):max(1,y2),max(0,x1):max(1,x2)].copy()

def draw_box(img,box,label,color):
    x1,y1,x2,y2=[int(i) for i in box]
    cv2.rectangle(img,(x1,y1),(x2,y2),color,2,cv2.LINE_AA)
    tx=max(0,x1);ty=max(70,y1-8)
    cv2.rectangle(img,(tx-1,ty-17),(min(img.shape[1]-1,tx+max(106,11*len(label))),ty+3),color,-1)
    write_text(img,label,tx+3,ty-3,.48,(10,20,25),2)


def video_writer(path,size=(W,H),fps=FPS):
    writer=cv2.VideoWriter(str(path),cv2.VideoWriter_fourcc(*'mp4v'),float(fps),size)
    if not writer.isOpened(): raise RuntimeError(f'Gagal membuat video MP4: {path}')
    return writer

def generate_inputs(outdir):
    outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    ref=outdir/'01_REFERENSI_SIMULASI.mp4';bad=outdir/'02_CCTV_BURAM_SIMULASI.mp4'
    if ref.exists() and bad.exists():return ref,bad
    a=video_writer(ref);b=video_writer(bad)
    try:
        for i in range(FPS*DUR):
            frame=scene(i/FPS)
            a.write(frame);b.write(degrade(frame,i))
    finally:a.release();b.release()
    return ref,bad

def psnr(a,b):
    mse=float(np.mean((a.astype(np.float32)-b.astype(np.float32))**2))
    return float(10*np.log10(255.**2/max(mse,1e-9)))

def sha256(path):
    s=hashlib.sha256()
    with open(path,'rb') as f:
        while True:
            b=f.read(1024*1024)
            if not b:break
            s.update(b)
    return s.hexdigest()

def analyze_demo(assets,outdir):
    assets=Path(assets);outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    ref=assets/'01_REFERENSI_SIMULASI.mp4';low=assets/'02_CCTV_BURAM_SIMULASI.mp4'
    if not ref.is_file() or not low.is_file():raise FileNotFoundError('Berkas video simulasi tidak lengkap')
    orig_sha=sha256(low)
    cap=cv2.VideoCapture(str(low));cref=cv2.VideoCapture(str(ref))
    final=outdir/'03_VIDEO_HASIL_ANALISIS.mp4'
    compare=outdir/'04_PERBANDINGAN.mp4'
    a=video_writer(final);b=video_writer(compare,(W*2,H))
    detected=[];metrics=[];best=None;firstperson=None;frames=0
    try:
        while True:
            ok,fr=cap.read();ok2,rf=cref.read()
            if not ok:break
            if not ok2:raise RuntimeError('Video referensi tidak sinkron')
            t=frames/FPS;processed=enhance(fr)
            found=detect_by_color(processed)
            annotated=processed.copy()
            if 'person' in found:
                person_box=full_person_box(found['person'],processed.shape)
                draw_box(annotated,person_box,'S-01 / ORANG',(71,225,106))
                detected.append({'detik':round(t,2),'kategori':'orang','kotak':list(person_box)})
                if firstperson is None:firstperson=t
                if 4.1<=t<=7.1:
                    # higher preference for samples where subject and helmet both visible
                    score=2 if 'helmet' in found else 1
                    if best is None or score>best['score']:
                        best={'t':t,'score':score,'box':person_box,'source':fr.copy(),'processed':processed.copy(),'reference':rf.copy(),'found':found.copy()}
            if 'helmet' in found:
                draw_box(annotated,found['helmet'],'HELM',(66,229,246))
                detected.append({'detik':round(t,2),'kategori':'helm','kotak':list(found['helmet'])})
            write_text(annotated,'DETEKSI WARNA / KHUSUS SIMULASI',17,80,.55,(244,249,249),2)
            a.write(annotated); b.write(np.concatenate((fr,annotated),axis=1))
            if frames % FPS == 0:
                metrics.append({'t':round(t,2),'buram_psnr':round(psnr(rf,fr),2),'olahan_psnr':round(psnr(rf,processed),2)})
            frames+=1
        if frames!=DUR*FPS:raise RuntimeError(f'Jumlah frame bukan {DUR*FPS}: {frames}')
    finally:
        cap.release();cref.release();a.release();b.release()
    if best is None: raise RuntimeError('Segmentasi merah belum mendeteksi karakter di rentang utama')
    box=best['box']
    # selection based on actually detected bounding boxes; head box is top-of-body illustration
    x1,y1,x2,y2=box
    head=(max(0,x1+4),max(0,y1+5),min(W,x2-4),min(H,y1+120))
    original=crop(best['source'],box);result=crop(best['processed'],box);reference=crop(best['reference'],box)
    ref_head=crop(best['reference'],head);head_low=crop(best['source'],head);head_proc=crop(best['processed'],head)
    figs={
        '05_OBJEK_ASLI.png': original,
        '06_OBJEK_DIPERTAJAM.png': result,
        '07_OBJEK_REFERENSI.png': reference,
        '08_KEPALA_SIMULASI_ASLI.png':head_low,
        '09_KEPALA_SIMULASI_OLAHAN.png':head_proc,
        '10_KEPALA_REFERENSI.png':ref_head,
    }
    for name,im in figs.items():
        if im.size==0: raise RuntimeError(f'Crop kosong {name}')
        cv2.imwrite(str(outdir/name),im)
    # natural side-by-side, resize if necessary (same boxes by construction)
    cv2.imwrite(str(outdir/'11_PERBANDINGAN_OBJEK.png'),np.hstack([original,result,reference]))
    avg_before=round(float(np.mean([m['buram_psnr'] for m in metrics])),2)
    avg_after=round(float(np.mean([m['olahan_psnr'] for m in metrics])),2)
    helmet_samples=[d for d in detected if d['kategori']=='helm']
    helmet_positions=[(.5*(d['kotak'][0]+d['kotak'][2]),d['detik']) for d in helmet_samples]
    moved=bool(helmet_positions and max(x for x,t in helmet_positions)-min(x for x,t in helmet_positions)>80)
    report={
        'jenis':'DEMO FIKTIF BERBASIS ILUSTRASI',
        'metode':'OpenCV HSV color segmentation, gamma, CLAHE, bilateral filtering; bukan YOLO atau pengenalan wajah',
        'kode_subjek':'S-01',
        'detail_subjek_berdasarkan_skenario':SCENE_DETAILS,
        'peristiwa_fiktif_dari_skenario':SCRIPT_EVENTS,
        'hasil_deteksi_piksel':{
            'frame_total':frames,'frame_terdeteksi_orang':len(set(d['detik'] for d in detected if d['kategori']=='orang')),
            'frame_terdeteksi_helm':len(set(d['detik'] for d in detected if d['kategori']=='helm')),
            'perubahan_posisi_helm_teramati':moved,
            'frame_pilihan_detik':round(best['t'],2),'orang_pertama_terdeteksi_detik':round(float(firstperson or 0),2),
            'catatan':'Deteksi didasarkan piksel merah/kuning yang sengaja digunakan dalam simulasi, bukan bukti pelaku',
        },
        'pengukuran_referensi_sintetis':{
            'rata_rata_psnr_video_buram_db':avg_before,'rata_rata_psnr_video_olahan_db':avg_after,
            'catatan':'Dihitung pada frame hasil decode MP4 terhadap referensi simulasi. Tidak berlaku untuk rekaman kejadian nyata.',
        },
        'sha256_video_masukan':orig_sha,
        'peringatan':'Bukan bukti pencurian nyata. Tidak dapat menentukan identitas, wajah sebenarnya, atau kesalahan orang.',
    }
    (outdir/'laporan_simulasi.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':
    base=Path(__file__).resolve().parent
    a,b=generate_inputs(base/'assets')
    r=analyze_demo(base/'assets',base/'assets'/'contoh_hasil')
    print('Generated',a,b,'PSNR',r['pengukuran_referensi_sintetis'],'detections',r['hasil_deteksi_piksel'])
