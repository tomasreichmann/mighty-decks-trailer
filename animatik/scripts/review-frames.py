"""Contact sheets from the actual encoded cut; no browser or source plates."""
from pathlib import Path
import sys
import cv2
from PIL import Image, ImageDraw

path=Path(sys.argv[1])
groups={
    'door':[55,149,179,180,329,330,389,390,420,431,446,459,460,533,534,543,607,608,635,659],
    'choice':[660,675,676,749,750,758,788,815,816,839,840,848,869,870,881,882,917,918,929,930],
    'product':[943,944,983,984,990,991,1028,1044,1079,1080,1091,1092,1130,1170,1229,1230,1260,1284,1350,1425]
}
cap=cv2.VideoCapture(str(path))
for k,frames in groups.items():
    out=Image.new('RGB',(390*4,240*5))
    d=ImageDraw.Draw(out)
    for i,f in enumerate(frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES,f)
        ok,im=cap.read()
        if not ok: raise ValueError((path,f))
        pic=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)).resize((390,219),Image.Resampling.LANCZOS)
        x,y=i%4*390,i//4*240
        out.paste(pic,(x,y)); d.text((x+4,y+219),str(f),fill='white')
    out.save(path.with_name(path.stem+'-'+k+'.jpg'),quality=90)
cap.release()
