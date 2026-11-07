"""Build registered RGBA performance patches from H3's two keyed islands."""
import json

import cv2
import numpy as np
from PIL import Image, ImageSequence

from prepare import ARM, HEAD, HERE, SIZE, actor_crop, clean_alpha, region

def card_mask():
    data=json.loads((HERE.parent/"table/registration.json").read_text(encoding="utf8"))
    return np.maximum.reduce([region(card["outline"]) for card in data["cards"].values()])

def source_planes():
    src=np.array(actor_crop())
    orig=src[:,:,3].astype(np.float32)/255
    shape=np.maximum(region(HEAD),region(ARM))
    motion=np.minimum(shape,clean_alpha())
    motion[card_mask()>0]=0
    # Solve the ordinary straight-alpha "over" equation in the feathered
    # outline so that the two layers recompose to the artist's exact first pose.
    active=motion.astype(np.float32)/255
    remain=np.divide(orig-active,1-active,out=np.zeros_like(orig),where=active<1)
    # A soft original alpha over a fully opaque source pixel would leave an
    # opaque copy of its colour behind. Clear that thin contour too, so that
    # a lifted finger reveals clean wood, rather than its old black outline.
    dilation=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(19,19))
    clear=(cv2.dilate((motion>64).astype(np.uint8),dilation)>0)&(shape>0)
    remain[clear]=0
    residual=src.copy()
    residual[:,:,3]=np.uint8(np.rint(np.clip(remain,0,1)*255))
    residual[residual[:,:,3]==0]=0
    Image.fromarray(residual).save(HERE/"residual.png")
    src[:,:,3]=motion
    src[motion==0]=0
    return src

def read_clip():
    # Work with the direct RGB decoder output: MP4 chroma subsampling visibly
    # stair-steps the border of the lips and the fingertips in a green key.
    with Image.open(HERE/"h3-actor-lossless.webp") as sequence:
        frames=[np.array(im.convert("RGB")) for im in ImageSequence.Iterator(sequence)]
    if len(frames)!=68:
        raise ValueError(f"Expected 68 lossless performance frames, decoded {len(frames)}")
    return frames

def unkey(frame):
    rgb=frame.astype(np.float32)
    green=np.median(rgb[:15,::4],axis=(0,1))
    excess=rgb[:,:,1]-np.maximum(rgb[:,:,0],rgb[:,:,2])
    key_excess=green[1]-max(green[0],green[2])
    # The drawing uses warm skin and brown/black ink. Only the green plane
    # has this positive green excess. Remove it at the antialiased boundary.
    a=np.clip((key_excess-excess-8)/(key_excess-12),0,1)
    # Recover subpixel coverage from full-rate luma as well as chroma.
    safe=(a>.98).astype(np.uint8)
    solid=cv2.erode(safe,np.ones((3,3),np.uint8))
    dist,labels=cv2.distanceTransformWithLabels(1-solid,cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL)
    anchors=np.zeros((int(labels.max())+1,3),np.float32)
    anchors[labels[solid>0]]=rgb[solid>0]
    edge=(dist>0)&(dist<4.5)
    estimated=anchors[labels[edge]]
    diff=estimated-green
    coverage=np.sum((rgb[edge]-green)*diff,axis=1)/np.maximum(np.sum(diff*diff,axis=1),1)
    a[edge]=np.clip(.80*coverage+.20*a[edge],0,1)
    a[a<.05]=0
    premul=np.clip(rgb-green[None,None,:]*(1-a[:,:,None]),0,255)*np.float32(a[:,:,None]>0)
    premul[:,:,1]=np.minimum(premul[:,:,1],np.maximum(premul[:,:,0],premul[:,:,2]))
    # On hair and outline the chroma is more blurred than the line. Replace
    # its hue while retaining the model's luma, including the black contour.
    bad=edge & (excess>4) & (a>.05)
    ref=anchors[labels[bad]]*.80+rgb[bad]*.20
    ref[:,1]=np.minimum(ref[:,1],.9*np.maximum(ref[:,0],ref[:,2]))
    weights=np.array([.213,.715,.072])
    lum=np.maximum(0,(rgb[bad]@weights)-(1-a[bad])*(green@weights))
    premul[bad]=ref*(lum/np.maximum(ref@weights,1))[:,None]
    return np.dstack([premul,a*255]).astype(np.float32)

def smooth(x):
    t=np.clip(x,0,1)
    return t*t*(3-2*t)

def read_sam2():
    with np.load(HERE/"sam2-mattes.npz") as masks:
        return {name:np.unpackbits(stack,axis=2) for name,stack in masks.items()}

def tracked_repaint(mattes, sample, gridx, gridy, field):
    """Follow the SAM2 cheek and wrist; include swept silhouettes to reveal wood."""
    profiles=[]
    for part, feather in (("face",14),("hand",12)):
        # The former location must also be replaced when the chin drops or
        # the fingertips lift. Otherwise the still source silhouette remains.
        original=mattes["art-"+part][0]
        tracked=mattes["tracked-"+part][sample]
        original=cv2.resize(original,SIZE,interpolation=cv2.INTER_NEAREST)
        tracked=cv2.resize(tracked,SIZE,interpolation=cv2.INTER_NEAREST)
        if part=="face":
            # The video predictor can label the entire fringe as "head" on a
            # blink. Lock that identification to the reference SAM skin mask,
            # carried into this pose, with room for the newly opened mouth.
            predicted=warp(original,gridx+field[:,:,0],gridy+field[:,:,1])
            interior=cv2.dilate(predicted,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)))
            outer=cv2.dilate(predicted,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(29,29)))
            envelope=np.where((gridx>605)&(gridy>263),outer,interior)
            tracked=predicted | (tracked & envelope)
        core=np.maximum(original,tracked)
        # Join small internal holes in printed ink, without crossing the gap
        # from jaw to wrist. The chroma matte gives each island its true edge.
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13))
        core=cv2.morphologyEx(core,cv2.MORPH_CLOSE,kernel)
        inside=cv2.distanceTransform(core,cv2.DIST_L2,5)
        outside=cv2.distanceTransform(1-core,cv2.DIST_L2,5)
        weight=smooth((inside-outside+feather+6)/(2*feather))
        # Keep the original cel anchored only where it joins static artwork.
        if part=="face":
            neck_line=np.interp(gridx,[418,454,499,535],[415,422,429,421])
            weight*=np.maximum(smooth((neck_line-gridy)/24),smooth((gridx-498)/40))
        else:
            weight*=smooth((gridx-333)/65)
        profiles.append(weight)
    return np.maximum(*profiles).astype(np.float32)

def warp(image,mx,my):
    return cv2.remap(image,mx.astype('float32'),my.astype('float32'),cv2.INTER_LINEAR,
                     borderMode=cv2.BORDER_CONSTANT)

def cloth_contact(gridx, gridy):
    # The sleeve opening is a curved ink line in the source, not a vertical
    # rectangle. Pin that line and the jacket above the bare forearm, then let
    # the SAM-tracked skin articulate a few pixels inside that contact.
    cuff_x=np.interp(gridy,[610,620,627,638,655,677,697,726],
                     [390,381,371,361,351,341,337,334])
    cuff=smooth((gridx-cuff_x-5)/26)
    arm_top=np.interp(gridx,[375,395,435,484,535,560,596,628],
                      [622,625,631,635,637,636,628,620])
    jacket=smooth((gridy-arm_top-3)/18)
    beyond_jacket=smooth((gridx-591)/42)
    return np.where(gridy<530,1,cuff*np.maximum(jacket,beyond_jacket)).astype(np.float32)

def premultiply(rgba):
    px=rgba.astype(np.float32)
    px[:,:,:3]*=px[:,:,3,None]/255
    return px

def straight(premul):
    a=premul[:,:,3,None]
    rgb=np.divide(premul[:,:,:3]*255,a,out=np.zeros_like(premul[:,:,:3]),where=a>.5)
    return np.concatenate([np.uint8(np.rint(np.clip(rgb,0,255))),np.uint8(np.rint(np.clip(a,0,255)))],axis=2)

def generate():
    src=source_planes()
    frames=read_clip()
    motion=premultiply(src)
    gridy,gridx=np.indices(src.shape[:2],dtype=np.float32)
    is_head=gridy<530
    # Keep the lower neck pinned to the source hood, and keep the cut across
    # the sleeve still. H3's disconnected islands may otherwise float.
    seam=np.interp(gridx,[240,297,337,380,418,454,499,535],[338,352,364,386,415,422,429,421])
    head_free=np.maximum(smooth((seam-gridy-5)/48),smooth((gridx-530)/70))
    arm_free=smooth((gridx-335)/94)
    freedom=np.where(is_head,head_free,arm_free).astype(np.float32)
    cloth=cloth_contact(gridx,gridy)
    freedom*=cloth
    mattes=read_sam2()
    src_gray=cv2.cvtColor(frames[0],cv2.COLOR_RGB2GRAY)
    dis=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    dis.setFinestScale(0)
    folder=HERE/"frames"
    folder.mkdir(exist_ok=True)
    # Local frame-to-frame timing of the first sentence. These landmarks are
    # recording times (s) before conversion to native 24 fps.
    timing=json.loads((HERE/"timing.json").read_text(encoding="utf8"))
    output_anchors=timing["acceptedSeconds"]
    input_anchors=timing["generatedSeconds"]
    sampled=[]
    for i in range(53):
        t=np.interp(i/24,output_anchors,input_anchors)
        sample=int(np.clip(round(t*24),0,len(frames)-1))
        sampled.append(sample)
        target=frames[sample]
        gray=cv2.cvtColor(target,cv2.COLOR_RGB2GRAY)
        field=cv2.resize(dis.calc(gray,src_gray,None),SIZE,interpolation=cv2.INTER_LINEAR)*2
        repaint=tracked_repaint(mattes,sample,gridx,gridy,field)*cloth
        # Use inverse flow for the original ink. The native patch is already
        # in output space. Moving fingers must be sampled at their actual
        # position even where new wood becomes visible between them.
        reach=freedom*(.50+.50*repaint)
        dx=gridx+field[:,:,0]*reach
        dy=gridy+field[:,:,1]*reach
        artwork=warp(motion,dx,dy)
        native=cv2.resize(unkey(target),SIZE,interpolation=cv2.INTER_CUBIC)
        # Restore fine ink on cheek/arm interiors from the moving original.
        # Leave the changing lip opening, eyelids and finger contours to H3.
        fine=artwork[:,:,:3]-cv2.GaussianBlur(artwork[:,:,:3],(0,0),1.25)
        ink=.48*smooth((640-gridx)/100)
        opaque=((artwork[:,:,3]>249)&(native[:,:,3]>249)).astype(np.uint8)
        interior=cv2.erode(opaque,np.ones((7,7),np.uint8))
        native[:,:,:3]+=fine*(ink*interior)[:,:,None]
        soft=repaint[:,:,None]*smooth(i/4)
        out=straight(artwork*(1-soft)+native*soft)
        # The actor never owns card pixels or elements away from these islands.
        out[(((gridy>486)&(gridy<535))|(gridx>790)|(gridy>761))]=0
        Image.fromarray(out).save(folder/f"actor-{i:03d}.png",compress_level=4)
    print("Native frame indices:",sampled)

if __name__=="__main__":
    generate()
