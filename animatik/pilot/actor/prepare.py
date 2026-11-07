"""Prepare H3's isolated chroma input from the storyboard actor RGBA layer."""
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SIZE = (896, 832)
KEY = (12, 226, 62)

# Coarse artist-space outline. Alpha from the source extends beyond the hair
# into the shelves and below the wrist onto two cards. Those are stationary.
OUTLINE = [
    (0,635),(36,581),(72,559),(62,541),(65,527),(85,483),(109,470),(107,414),
    (148,386),(187,355),(209,338),(238,337),(290,348),(315,349),(290,338),
    (273,319),(254,294),(247,266),(242,252),(261,231),(265,208),(276,194),
    (309,180),(326,156),(348,141),(381,114),(417,97),(437,89),(462,93),
    (488,88),(508,107),(536,106),(552,104),(570,122),(599,128),(603,140),
    (624,149),(633,160),(648,169),(665,194),(677,211),(687,248),(680,271),
    (665,291),(648,299),(660,317),(656,326),(646,335),(647,348),(640,357),
    (641,371),(634,389),(633,409),(624,420),(611,423),(575,419),(542,407),
    (535,414),(552,432),(574,450),(595,473),(595,493),(607,531),(621,565),
    (624,587),(611,605),(624,619),(644,615),(658,615),(683,629),(719,640),
    (731,659),(744,689),(749,707),(742,716),(720,724),(694,722),(664,712),
    (647,706),(601,708),(565,717),(521,709),(490,710),(423,722),(355,728),
    (335,741),(295,742),(270,740),(245,747),(207,743),(173,731),(147,732),
    (70,738),(0,743),
]

# Lower head boundary follows the hood seam and the actor's jaw; the far
# shoulder and jacket never enter the generated image. Select only a short
# sleeve-to-hand chain around the wrist for the optional finger gesture.
HEAD = [(200,0),(735,0),(735,440),(580,440),(535,421),(499,429),
        (454,422),(418,415),(380,386),(337,364),(298,352),(245,338),(200,322)]
ARM = [(305,591),(349,571),(394,573),(423,607),(489,621),(576,615),(630,602),
       (772,596),(773,742),(664,741),(610,720),(545,721),(391,740),(330,748),(295,729)]

def region(points):
    out = np.zeros((SIZE[1],SIZE[0]),np.uint8)
    cv2.fillPoly(out,[np.array(points,np.int32)],255)
    return out

def actor_crop():
    return Image.open(ROOT / "storyboard/vrstvy/table/02-hracka.png").convert("RGBA").crop((0,0,*SIZE))

def clean_alpha():
    rgba = np.asarray(actor_crop())
    outline = np.zeros(rgba.shape[:2], np.uint8)
    cv2.fillPoly(outline, [np.array(OUTLINE, np.int32)], 255)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17,17))
    mark = np.full(outline.shape, cv2.GC_BGD, np.uint8)
    mark[cv2.dilate(outline,kernel)>0] = cv2.GC_PR_BGD
    mark[outline>0] = cv2.GC_PR_FGD
    mark[cv2.erode(outline,kernel)>0] = cv2.GC_FGD
    mark[rgba[:,:,3]<24] = cv2.GC_BGD
    cv2.setRNGSeed(305)
    cv2.grabCut(rgba[:,:,:3].copy(),mark,None,np.zeros((1,65)),np.zeros((1,65)),4,cv2.GC_INIT_WITH_MASK)
    return np.minimum(cv2.GaussianBlur(np.uint8(mark%2)*255,(3,3),0.7),rgba[:,:,3])

def prepare():
    im = actor_crop()
    parts = np.maximum(region(HEAD),region(ARM))
    im.putalpha(Image.fromarray(np.minimum(clean_alpha(),parts)))
    key = Image.new("RGB", SIZE, KEY)
    key.paste(im, mask=im.getchannel("A"))
    key.resize((448,416), Image.Resampling.LANCZOS).save(HERE/"md-actor-green.png")
    graph = json.loads((HERE.parent/"graphs/h3-quiet.json").read_text(encoding="utf8"))
    graph["5"]["inputs"].update(width=448, height=416, prompt=(
        "Five-second 2D hand-inked animation, an isolated female dialogue cel against an absolutely flat solid chroma green screen. "
        "Two separated pieces of animation artwork, a right-facing woman's inked head floating at the top and an isolated forearm and hand at the bottom. "
        "Keep the blank green space between the two pieces. Only animate these two supplied pieces in place. Fixed scale, locked camera. "
        "Mouth and eyes move naturally in profile. "
        "She speaks Czech with a quiet, warm, confident voice, looking to the right, taking a small breath as her gaze drops. "
        "Her wrist stays planted and her fingertips flex just a little, as she decides. Keep shoulders and torso absent. Hair shifts only slightly. Her mouth articulates clearly. "
        "No other people, props, ground, cast shadows, table, card, lettering, cuts, subtitles or environment. "
        "Remain on the flat green matte for the entire clip. "
        "Native Czech speech, exactly: “Úspěch potřebuju na záchranu lodi. Hraju částečný. Beru zranění.” "
        "First short natural breath, first line at 0.27 seconds. Very intimate, level, quietly convinced. Low, warm and dry. "
        "Measured first phrase, tiny breath before her decision. No music. No other speech."
    ))
    graph["16"]["inputs"]["image"]="md-actor-green.png"
    graph["14"]["inputs"]["filename_prefix"]="video/mighty_decks/actor-c"
    graph["17"]["inputs"]["filename_prefix"]="audio/mighty_decks/actor-c"
    graph["18"]={"class_type":"ImageFromBatch","inputs":{"image":["11",0],"batch_index":0,"length":68}}
    graph["19"]={"class_type":"SaveAnimatedWEBP","inputs":{"images":["18",0],"filename_prefix":"video/mighty_decks/actor-c-lossless","fps":24.0,"lossless":True,"quality":90,"method":"fastest"}}
    (HERE/"h3-actor.json").write_text(json.dumps(graph,indent=2,ensure_ascii=False)+"\n",encoding="utf8")

if __name__=="__main__":
    prepare()
