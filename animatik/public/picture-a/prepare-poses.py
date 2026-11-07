from pathlib import Path
import cv2
import numpy as np

# Deform the existing two registered cutouts separately. Both hands stay
# anchored to the lip while the boots slip, then the reaching arm takes weight.
root = Path(__file__).resolve().parents[3]
source = root / 'storyboard/vrstvy/ramp-jump'
out = Path(__file__).resolve().parent
left, top, width, height = 380, 240, 680, 685
ys, xs = np.mgrid[top:top+height, left:left+width].astype(np.float32)
def layer(name):
    src = cv2.imread(str(source/name), cv2.IMREAD_UNCHANGED)
    crop = src[top:top+height, left:left+width].astype(np.float32) / 255
    if crop.shape[2] == 3:
        return crop
    crop[:,:,:3] *= crop[:,:,3:]
    return crop

bg = layer('00-pozadi.png')[:,:,:3]
man = layer('02-visici-paserak.png')
crew = layer('01-posadka.png')
def gaussian(x, y, sx, sy):
    return np.exp(-.5*(((xs-x)/sx)**2 + ((ys-y)/sy)**2))
def warp(src, dx, dy):
    return cv2.remap(src, xs-left-dx, ys-top-dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
def over(base, fg):
    return base * (1-fg[:,:,3:]) + fg[:,:,:3]
def ease(t):
    t = max(0, min(1,t))
    return t*t*(3-2*t)
def pose(f):
    slip = ease(f/9)
    heave = ease((f-18)/23)
    reach = ease((f-5)/12)
    # Keep the grip on the serrated edge fixed. The loose boots take the
    # broadest arc, with the hip and shoulders following only a little.
    boots = gaussian(863,790,184,174)
    back_boot = gaussian(935,747,50,107)
    torso = gaussian(812,538,89,102)
    dx = (1-slip)*(38*boots + 18*back_boot) - heave*(36*boots + 11*torso)
    dy = (1-slip)*(-65*boots - 18*back_boot) + slip*(14*boots+5*torso) - heave*(49*boots+15*torso)
    suspended = warp(man, dx, dy)
    hand = gaussian(555,480,67,77)
    # Reach down across the wounded hand, then start to draw it up.
    rescuer = warp(crew, hand*(19*reach-6*heave), hand*(61*reach-13*heave))
    final = over(over(bg, suspended), rescuer)
    # Match the registered paint exactly outside the moving region.
    ref = cv2.imread(str(root/'reference/planches/ramp-jump.png'))[top:top+height,left:left+width].astype(np.float32)/255
    blend = np.minimum.reduce([np.clip((xs-left)/25,0,1),np.clip((left+width-xs)/25,0,1),np.clip((ys-top)/25,0,1),np.clip((top+height-ys)/25,0,1)])
    final = (ref*(1-blend[:,:,None]) + final*blend[:,:,None])
    cv2.imwrite(str(out/f'catch-{f:02}.webp'),np.uint8(np.clip(final*255+.5,0,255)),[cv2.IMWRITE_WEBP_QUALITY,98])
for frame in range(0,48,2):
    pose(frame)
