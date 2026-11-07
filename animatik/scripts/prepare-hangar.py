"""Make the intact sleeve and moving shutter from the supplied hangar drawing."""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parent
DEST = PROJECT / "public" / "hangar"


def incoming_beast():
    """Use the reference's unoccluded, open-jaw pose for the incoming leap."""
    source=Image.open(ROOT/"reference/exiles/alpha_mallowtail.png").convert("RGB")
    rgb=np.array(source)
    # Trace at 768 px for legibility. The left/right feet are on the photo
    # borders. Trace between each foot to keep the floor out of the leap.
    contour=[
        (0,622),(7,595),(24,574),(43,541),(55,505),(74,474),(81,440),
        (99,395),(124,366),(129,340),(114,303),(119,264),(126,246),
        (143,227),(128,202),(117,176),(116,166),(158,189),(177,192),
        (198,160),(227,143),(255,122),(291,108),(317,85),(339,53),(353,29),
        (359,69),(385,51),(385,72),(403,62),(416,77),(422,82),(450,103),
        (471,119),(500,146),(521,170),(510,133),(520,99),(541,74),
        (566,58),(596,50),(631,57),(665,74),(691,101),(705,128),
        (717,165),(720,192),(709,212),(685,222),(667,207),(656,187),
        (658,158),(667,134),(657,114),(635,101),(610,97),(585,96),
        (563,111),(548,132),(549,151),(559,172),(571,186),
        (606,196),(630,211),(658,245),(676,282),(689,310),(714,335),
        (728,369),(735,403),(749,421),(757,454),(759,501),(758,553),
        (766,590),(767,620),(689,628),(687,613),(696,588),(709,575),
        (709,522),(703,474),(682,440),(648,411),(619,380),(605,367),
        (575,342),(557,345),(551,356),(570,376),(595,394),(603,423),
        (605,452),(619,482),(615,511),(607,535),(607,574),(614,613),
        (632,657),(639,693),(638,721),(628,738),(613,716),(603,738),
        (593,736),(587,714),(564,710),(551,717),(534,716),(511,729),
        (484,754),(476,747),(478,716),(485,682),(469,674),(448,687),
        (431,704),(428,691),(438,652),(467,623),(485,583),(496,544),
        (505,499),(499,469),(508,419),(508,400),(494,417),(477,450),
        (459,478),(447,516),(439,551),(427,578),(353,585),(347,570),
        (355,548),(367,534),(375,507),(391,486),(421,429),(425,400),
        (424,382),(403,386),(388,403),(381,438),(365,483),(349,514),
        (331,553),(320,578),(304,593),(241,598),(234,585),(254,562),
        (281,551),(293,540),(307,515),(326,481),(333,448),(335,423),
        (325,413),(311,424),(294,447),(273,456),(250,449),(230,465),
        (212,484),(205,520),(206,567),(198,590),(187,613),(179,603),
        (175,576),(164,579),(151,624),(136,625),(137,592),(135,570),
        (125,567),(124,546),(134,522),(151,491),(185,444),(208,399),
        (207,378),(196,363),(188,389),(180,433),(153,467),(123,499),
        (109,534),(115,568),(120,600),(111,625),(99,626),(93,606),
        (82,616),(73,627),(61,623),(56,613),(45,625),(32,629),(26,618),
        (15,626)
    ]
    rough=np.zeros(rgb.shape[:2],np.uint8)
    cv2.fillPoly(rough,[np.rint(np.array(contour)*4/3).astype(np.int32)],255)
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(19,19))
    mask=np.where(rough,cv2.GC_PR_FGD,cv2.GC_PR_BGD).astype(np.uint8)
    mask[cv2.erode(rough,kernel)>0]=cv2.GC_FGD
    mask[cv2.dilate(rough,kernel)==0]=cv2.GC_BGD
    cv2.setRNGSeed(434)
    cv2.grabCut(rgb,mask,None,np.zeros((1,65)),np.zeros((1,65)),4,cv2.GC_INIT_WITH_MASK)
    matte=cv2.GaussianBlur(np.uint8(mask%2)*255,(3,3),.65)
    # Translate the photographic reference to a backlit blue-black ink drawing,
    # only the most illuminated fur carries warm ochre from the hangar lights.
    gray=np.array(source.convert("L"))
    luma=cv2.bilateralFilter(gray,7,24,7)
    palette=np.array([[17,23,29],[36,34,36],[75,61,48],[109,83,63],
                      [161,120,82],[201,157,110],[235,201,154],[247,222,179]])
    stops=[0,35,62,90,120,150,185,230]
    ink=np.stack([np.interp(luma,stops,palette[:,c]) for c in range(3)],axis=2)
    contours=cv2.Canny(luma,39,81)
    ink*=1-.25*(contours.astype(float)/255)[:,:,None]
    p=Image.fromarray(np.uint8(ink)).convert("RGBA")
    p.putalpha(Image.fromarray(matte))
    p.save(DEST/"approach.png",optimize=True)


def ready_weapon():
    """Rebuild the stock before the bite; teeth are baked into the grip layer."""
    plate=Image.open(ROOT/"reference/planches/hangar.png").convert("RGBA")
    original=Image.open(ROOT/"storyboard/vrstvy/hangar/02-karabina.png")
    grip=np.array(plate)
    # Sample the exposed uninterrupted walnut at the left end. Warp its grain
    # across the stock where fangs, mouth, and flecks of fur cover the drawing.
    top=[(495,524),(526,531),(576,545),(649,558),(713,565),(793,574)]
    bottom=[(793,671),(754,662),(700,650),(620,637),(569,638),(495,652)]
    poly=np.zeros(grip.shape[:2],np.uint8)
    cv2.fillPoly(poly,[np.array(top+bottom,np.int32)],255)
    y,x=np.mgrid[:1080,:1920]
    u=np.interp(x,[498,790],[500,568])
    ymin=np.interp(x,*zip(*top)); ymax=np.interp(x,*zip(*bottom[::-1]))
    frac=np.clip((y-ymin)/np.maximum(ymax-ymin,1),0,1)
    v=550+75*frac
    wood=cv2.remap(grip[:,:,:3],u.astype(np.float32),v.astype(np.float32),cv2.INTER_CUBIC)
    relief=1-.30*np.exp(-(y-ymin).clip(0)/5)-.63*np.exp(-(ymax-y).clip(0)/6)
    wood=np.uint8(wood*relief[:,:,None])
    grip[:,:,:3]=np.where(poly[:,:,None]>0,wood,grip[:,:,:3])
    # The muzzle, both hands and the sight keep their original 3D drawing.
    # The hard outside contour prevents matting fragments of fur/wall riding up.
    outline=[(0,962),(56,883),(120,808),(197,747),(219,710),(252,647),
        (272,617),(283,586),(302,551),(313,528),(335,521),(353,507),
        (381,497),(397,486),(414,463),(429,466),(444,478),(465,480),(485,485),
        (502,499),(516,524),*top[1:],(810,567),(848,568),(880,539),
        (910,538),(918,518),(941,517),(957,530),(992,534),(1046,538),
        (1071,540),(1079,523),(1097,522),(1110,532),(1125,520),(1140,524),
        (1152,544),(1173,544),(1188,554),(1204,555),(1215,568),
        (1290,577),(1308,587),(1320,608),(1328,631),(1349,637),
        (1352,679),(1339,695),(1328,701),(1320,712),(1222,698),
        (1215,731),(1207,754),(1221,805),(1265,884),(1306,976),(1345,1080),
        (983,1080),(1019,943),(1037,855),(1045,748),(1010,716),
        (1006,694),(976,691),(986,710),(989,741),(980,755),(962,754),
        (950,744),(950,727),(956,698),(930,693),(930,723),(918,752),
        (847,739),(850,674),(791,672),*bottom[1:],(484,674),(460,694),
        (429,704),(379,719),(362,742),(360,769),(342,834),(323,902),
        (307,983),(282,1080),(0,1080)]
    trim=np.zeros(grip.shape[:2],np.uint8)
    cv2.fillPoly(trim,[np.array(outline,np.int32)],255)
    # Hollow trigger loop.
    cv2.fillPoly(trim,[np.array([(965,702),(978,707),(983,722),(981,738),(972,745),(964,741)],np.int32)],0)
    grip[:,:,3]=np.minimum(np.maximum(poly,np.array(original.getchannel("A"))),cv2.GaussianBlur(trim,(3,3),.7))
    dest=Image.fromarray(grip)
    dest.alpha_composite(Image.open(DEST/"sleeve.png"),(0,642))
    dest.paste((0,0,0,0),mask=dest.getchannel("A").point(lambda alpha: 255 if alpha==0 else 0))
    dest.save(DEST/"ready-rifle.png",optimize=True)


def intact_sleeve(plate):
    # The intact material is a registered patch of the same illustrated jacket.
    # Leave the three claw tips, glove, outer silhouette and rolled cuff intact.
    # The polygon follows the inked contour of the artist's compound forearm.
    left, top = 0, 642
    width, height = 375, 304
    outline = [
        (0,828),(46,796),(92,775),(125,758),(153,746),(165,744),(170,747),
        (171,740),(192,732),(222,714),(249,695),(268,684),(285,679),
        (302,679),(323,684),(341,697),(353,716),(361,736),(360,754),
        (355,777),(348,813),(340,840),(326,864),(312,877),
        (306,879),(299,865),(287,850),(266,836),(240,831),(213,832),
        (179,838),(137,852),(89,877),(49,904),(0,942),
    ]
    outline = [(x-left, y-top) for x,y in outline]
    mask = Image.new("L", (width, height))
    ImageDraw.Draw(mask).polygon(outline, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.15))
    yy, xx = np.mgrid[:height, :width]
    # Unroll the still-intact opposite sleeve between cuff and elbow. Sampling
    # stays inside its tapered silhouette, including at the narrow wrist.
    along = ((xx-301) * -.81 + (yy+top-705) * .59) / 330
    across = ((xx-301) * .59 + (yy+top-705) * .81) / (88 + 64 * np.clip(along,0,1))
    along = np.abs(1 - np.abs((along % 2) - 1))
    u = 1120 + 9*along + np.sin(across) * (47+50*along)
    v = 842 + 120*along
    cloth = cv2.remap(np.asarray(plate), u.astype("float32"), v.astype("float32"), cv2.INTER_CUBIC)
    # Warm sidelight and the shadow under the rolled cuff wrap around the arm.
    gain = .88 + .13 * (xx / width) - .11 * ((yy - 110) / height)
    grain = np.asarray(plate.convert("L"))[885:919,142:192].astype(float)
    grain -= cv2.GaussianBlur(grain,(0,0),1.5)
    relief = np.tile(grain,(height//grain.shape[0]+1,width//grain.shape[1]+1))[:height,:width]
    fabric = Image.fromarray(np.uint8(np.clip(cloth * gain[:, :, None] + relief[:,:,None]*.55, 0, 255))).convert("RGBA")
    fabric.putalpha(mask)
    fabric.save(DEST / "sleeve.png")


def roller_shutter():
    # Unskew an existing industrial steel door. All plate texture, dents and
    # warning paint are sampled from the same illustrated hangar.
    wall = np.asarray(Image.open(ROOT / "storyboard/vrstvy/hangar/00-pozadi.png").convert("RGB"))
    source = np.float32([[1444,342],[1908,102],[1908,655],[1444,679]])
    target = np.float32([[0,0],[1127,0],[1127,653],[0,653]])
    warped = cv2.warpPerspective(wall, cv2.getPerspectiveTransform(source, target), (1128,654))
    plate = Image.fromarray(np.uint8(np.clip(warped.astype(float) * [.78,.80,.84],0,255)))
    metal = ImageDraw.Draw(plate, "RGBA")
    for y in range(53, 586, 54):
        metal.line((0,y,1128,y),fill=(19,22,27,192),width=4)
        metal.line((0,y+4,1128,y+4),fill=(208,167,116,92),width=2)
    metal.rectangle((0,646,1128,653), fill=(19,22,27,255))
    metal.line((0,643,1128,643),fill=(236,190,109,198),width=3)
    plate.save(DEST / "shutter.png", optimize=True)


def crew():
    # The registered ramp layer includes reflections from its original wet
    # floor. On the hangar floor those fragments read as a bright rectangular
    # fringe, so trim the cutout against the actual soles, handles and hair.
    source = Image.open(ROOT / "storyboard/vrstvy/ramp/02-posadka.png").convert("RGBA")
    box = (35,155,710,665)
    rgba = np.array(source.crop(box))
    outline = [
        (59,648),(62,621),(69,602),(73,581),(80,560),(75,549),(86,528),
        (106,511),(119,488),(129,464),(123,446),(126,429),(112,414),(119,391),
        (133,365),(145,341),(132,343),(116,337),(109,320),(113,301),
        (125,279),(137,265),(153,263),(166,248),(178,232),(193,222),
        (216,215),(239,217),(252,219),(253,205),(258,193),(270,185),
        (285,179),(305,183),(317,189),(327,203),(323,215),(317,219),
        (319,228),(315,240),(311,248),(318,261),(325,287),(330,330),
        (336,328),(334,311),(342,289),(353,272),(373,263),(383,257),
        (370,252),(362,241),(366,225),(380,212),(394,200),(411,196),
        (428,195),(438,203),(444,218),(440,232),(445,244),(438,251),
        (450,261),(465,262),(472,266),(470,277),(465,282),(472,298),
        (475,317),(477,337),(485,336),(489,310),(499,289),(511,274),
        (529,262),(551,255),(561,246),(563,236),(575,225),(593,217),
        (612,218),(624,226),(633,240),(628,250),(624,259),(626,269),
        (638,279),(647,293),(650,310),(652,330),(654,346),(645,365),
        (640,382),(641,396),(657,415),(676,441),(685,460),(679,483),
        (679,504),(666,525),(665,544),(651,555),(649,567),(657,579),
        (673,584),(676,598),(666,603),(620,602),(598,598),(598,582),
        (604,560),(602,540),(610,519),(618,498),(625,480),(609,470),
        (595,451),(579,446),(563,460),(557,488),(545,516),(535,534),
        (530,557),(506,561),(506,569),(520,574),(523,588),(513,596),
        (479,605),(455,603),(452,590),(457,565),(459,556),(354,556),
        (350,568),(347,583),(353,599),(349,619),(337,623),(311,621),
        (305,618),(302,605),(309,581),(316,558),(299,551),(298,528),
        (284,536),(273,552),(257,558),(255,581),(265,592),(281,597),
        (284,613),(278,622),(251,626),(217,623),(187,618),(188,596),
        (196,577),(202,556),(211,543),(209,531),(226,497),(241,478),
        (228,468),(210,455),(201,444),(190,463),(182,487),(172,516),
        (150,540),(144,560),(129,567),(117,583),(113,608),(116,626),
        (121,642),(116,651),(87,651),
    ]
    holes = [
        [(278,344),(285,353),(291,381),(302,399),(298,409),(281,393),(270,375),(267,361)],
        [(470,361),(482,352),(481,373),(484,397),(479,421),(473,438),(464,431),(462,413)],
    ]
    polygon = Image.new("L",source.size)
    d = ImageDraw.Draw(polygon)
    d.polygon(outline,fill=255)
    for hole in holes:
        d.polygon(hole,fill=0)
    rough = np.uint8(polygon.crop(box))
    kernel = np.ones((5,5),np.uint8)
    mask = np.where(rough,cv2.GC_PR_FGD,cv2.GC_PR_BGD).astype("uint8")
    mask[cv2.erode(rough,kernel,iterations=2)>0] = cv2.GC_FGD
    mask[cv2.dilate(rough,kernel,iterations=3)==0] = cv2.GC_BGD
    mask[rgba[:,:,3]<36] = cv2.GC_BGD
    cv2.setRNGSeed(621)
    cv2.grabCut(rgba[:,:,:3].copy(),mask,None,np.zeros((1,65)),np.zeros((1,65)),3,cv2.GC_INIT_WITH_MASK)
    silhouette = np.uint8((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD))*255
    # Keep only the group connected by the crate to both bearers.
    _, labels, stats, _ = cv2.connectedComponentsWithStats(silhouette)
    silhouette = np.uint8(labels==1+np.argmax(stats[1:,4]))*255
    # Repainted floor fragments between individual boot treads can have the
    # same colour as the ink. Trace those five contact contours explicitly.
    soles = Image.new("L", (box[2]-box[0],box[3]-box[1]))
    trace = ImageDraw.Draw(soles)
    trace.rectangle((0,0,soles.width,399),fill=255)
    for boot in [
        [(46,398),(103,398),(95,408),(88,412),(81,430),(78,449),(77,466),(82,475),(83,485),(72,490),(31,490),(27,485),(30,470),(34,455),(35,437),(42,427),(44,415)],
        [(181,398),(226,398),(218,408),(211,421),(211,433),(218,438),(230,444),(241,446),(247,454),(247,464),(237,468),(216,470),(159,466),(155,461),(156,447),(159,432),(167,422),(170,410)],
        [(289,398),(328,398),(320,414),(317,427),(313,441),(314,454),(311,460),(294,463),(271,466),(268,459),(272,445),(274,432),(279,420)],
        [(431,398),(476,398),(470,413),(470,424),(477,430),(484,435),(485,443),(476,447),(464,449),(440,452),(422,447),(423,437),(426,424),(427,411)],
        [(576,398),(618,398),(613,412),(615,419),(620,426),(629,429),(635,435),(636,448),(625,450),(604,449),(573,441),(567,438),(568,427),(570,413)],
    ]:
        trace.polygon(boot,fill=255)
    silhouette = np.minimum(silhouette,np.asarray(soles))
    # Two gaps amid overlapping legs, sling and the crate reveal today's floor.
    for gap in [[(257,324),(267,313),(267,351),(265,378),(250,377),(255,361)],
                [(606,186),(618,174),(624,211),(606,224),(601,224)],
                [(268,261),(247,236),(255,256),(267,274)]]:
        cv2.fillPoly(silhouette,[np.int32(gap)],0)
    alpha = cv2.GaussianBlur(silhouette,(3,3),.60)
    rgba[:,:,3] = np.minimum(rgba[:,:,3],alpha)
    rgba[rgba[:,:,3]==0]=0
    Image.fromarray(rgba).save(DEST / "crew.png")
    # Each boot meets the polished floor at its own depth. Mirror only the
    # last piece of shin below that sole, with slight horizontal breakup
    # matching the inked water. The card, jacket and faces stay out of it.
    reflection = np.zeros((140,675,4),dtype=np.uint8)
    for x0,x1,sole in [(22,99,490),(155,251,470),(265,326,464),(420,488,451),(563,641,448)]:
        height = 43
        for row in range(height):
            shift = round(1.5 * np.sin(row*.80) + .044*row)
            pixels = rgba[sole-2-row*2, x0:x1].astype(float)
            pixels[:,:3] = pixels[:,:3] * [.61,.66,.76]
            pixels[:,3] *= .44 * (1-row/height)**1.5 * (.78 + .22*np.sin(row*.83))
            reflection[sole-430+row,x0+shift:x1+shift] = np.uint8(pixels)
    Image.fromarray(reflection).filter(ImageFilter.GaussianBlur(.85)).save(DEST / "reflections.png")


if __name__ == "__main__":
    DEST.mkdir(parents=True, exist_ok=True)
    intact_sleeve(Image.open(ROOT / "reference/planches/hangar.png").convert("RGB"))
    incoming_beast()
    ready_weapon()
    roller_shutter()
    crew()
