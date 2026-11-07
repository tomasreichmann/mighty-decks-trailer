import {AbsoluteFill, Easing, Img, interpolate, staticFile} from 'remotion';
import type {CSSProperties} from 'react';
import {Graphics} from './Graphics';
import {ScenePlate} from './ScenePlate';

type Props = {frame: number; lang: 'cs' | 'en'};
const fill = {position:'absolute', inset:0, width:1920, height:1080} as const;
const windshield = 'polygon(0 328px,173px 0,1309px 0,983px 568px,117px 579px,0 382px)';
const ease = {extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic)} as const;

function Layer({path,style}: {path:string;style?:CSSProperties}) {
  return <Img src={staticFile(path)} style={{...fill,...style}}/>;
}
function Thrust({frame,lang}:Props) {
  const full = lang === 'en' ? 991 : 984;
  const turn = interpolate(frame,[full,full+36],[0,1],ease);
  const press = interpolate(frame,[978,988],[0,1],ease);
  const ignite = interpolate(frame,[983,984,full+4,full+12,full+28],[0,.14,.84,.55,0],ease);
  const windowLayers = 'storyboard/vrstvy/thrust/';
  return <AbsoluteFill style={{overflow:'hidden'}}>
    <Layer path={windowLayers+'00-pozadi.png'}/>
    <div style={{...fill,clipPath:windshield}}>
      <Layer path="storyboard/vrstvy/opening/00-pozadi.png" style={{
        opacity:turn*.66,transform:'translate(-530px,-310px) scale(1.55)',transformOrigin:'0 0',
      }}/>
      <Layer path={windowLayers+'01-troska.png'} style={{
        transform:`translate(${turn*1370}px,${turn*-440}px) rotate(${turn*-7}deg)`,transformOrigin:'450px 197px',
      }}/>
      <div style={{...fill,opacity:ignite,background:'radial-gradient(ellipse 46% 24% at -3% 48%,#fffae9 0%,#ffba61 31%,#f6852d66 63%,transparent 100%)',mixBlendMode:'screen'}}/>
    </div>
    <Layer path={windowLayers+'02-paka.png'} style={{transform:`translate(${press*2}px,${press*2}px)`}}/>
  </AbsoluteFill>;
}
function Loot({frame,lang}:Props) {
  if (frame<1092) {
    // A closer overhead angle on the closed catches. The bandaged hand stays
    // attached to the same upper hinge that appears on the open reverse.
    return <AbsoluteFill style={{overflow:'hidden'}}>
      <div style={{...fill,transformOrigin:'960px 590px',transform:'scale(1.14)'}}>
        <Layer path="picture-b/closed-case.webp"/>
        <Layer path="storyboard/vrstvy/loot/01-obvaz.png" style={{transform:'scaleY(1.19)',transformOrigin:'0 0'}}/>
      </div>
    </AbsoluteFill>;
  }
  if(frame<1130) {
    // Reframe the left well at the latch cut. The right well comes into view
    // only on the following wider angle, with the other product face.
    return <AbsoluteFill style={{overflow:'hidden',background:'#282018'}}>
      <Layer path="storyboard/vrstvy/loot/00-pozadi.png" style={{transform:'translate(800px,-203px) scale(1.34)',transformOrigin:'0 0'}}/>
      <Layer path="storyboard/vrstvy/loot/01-obvaz.png" style={{transform:'translate(800px,-203px) scale(1.34)',transformOrigin:'0 0'}}/>
      <div style={{position:'absolute',inset:'0 30% 0 0',background:'linear-gradient(90deg,#282018 0%,#282018 60%,transparent 100%)'}}/>
      <Img src={staticFile('reference/karty/ruka/'+lang+'/base_light_weapon.png')} style={{position:'absolute',width:440,top:168,left:233,filter:'drop-shadow(0 7px 10px #120f0f)'}}/>
    </AbsoluteFill>;
  }
  const reach = interpolate(frame,[1152,1170],[0,1],ease);
  return <AbsoluteFill>
    <ScenePlate frame={frame} locale={lang} shotId="06-korist"/>
    <Img src={staticFile('picture-b/buckle-00-pozadi.webp')} style={{
      position:'absolute',left:1180,top:145,width:315,height:373,
    }}/>
    <Img src={staticFile('picture-b/buckle-02-mlade.webp')} style={{
      position:'absolute',left:1197,top:166,width:264,height:329,transformOrigin:'77% 19%',
      transform:`translate(${32-34*reach}px,${-34+37*reach}px) rotate(${-4*(1-reach)}deg)`,
    }}/>
  </AbsoluteFill>;
}
export default function PictureB({frame, lang}:Props) {
  if(frame<1080) return <Thrust frame={frame} lang={lang}/>;
  if(frame<1230) return <Loot frame={frame} lang={lang}/>;
  return <Graphics frame={frame} locale={lang}/>;
}

