import {AbsoluteFill, Easing, Img, interpolate, staticFile} from 'remotion';
import type {CSSProperties} from 'react';
import manifest from '../../storyboard/vrstvy/manifest.json';

const hangar = manifest.shots.find((shot) => shot.id === 'hangar')!;
const fill = {position: 'absolute', inset: 0, width: 1920, height: 1080} as const;
const ease = Easing.inOut(Easing.cubic);

function travel(frame: number, from: number, to: number) {
  return interpolate(frame, [from, to], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease,
  });
}

type HangarProps = {frame: number; beastMotion?: boolean};

function BeastCel({src, style, padded}: {src: string; style: CSSProperties; padded: boolean}) {
  if (!padded) return <Img src={src} style={style}/>;
  // The 448-square reference was placed at (32, 32) in the 512-square
  // generated cel. Keep that exact scale and show the tail outside the square.
  const margin = 32 / 448 * 100;
  return <div style={style}><Img src={src} style={{
    position:'absolute', left:`-${margin}%`, top:`-${margin}%`, maxWidth:'none',
    width:`${100 + 2 * margin}%`, height:`${100 + 2 * margin}%`,
  }}/></div>;
}

function Approach({frame, beastMotion}: HangarProps) {
  const beats = [424, 427, 431, 437, 443, 449, 454, 459];
  const pose = (values: number[]) => interpolate(frame, beats, values, {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const center = pose([-190,-25,182,318,415,488,613,804]);
  const size = pose([292,320,369,426,481,593,804,1150]);
  const sole = pose([837,839,843,849,858,876,960,1103]);
  const lean = pose([5,3,1,-.5,0,-2,-2,0]);
  const shadowLead = travel(frame, 421, 427);
  const shadowCenter = frame < 427 ? -295 + 257*shadowLead : center - 13;
  const shadowWidth = frame < 427 ? 389 + 97*shadowLead : size*1.52;
  const illumination = .62 + .58*travel(frame,429,457);
  const brace = travel(frame, 438, 458);
  const animated = Boolean(beastMotion && frame >= 431);
  const shape = staticFile(animated
    ? `picture-b/beast-${String(frame - 431).padStart(3, '0')}.webp`
    : 'hangar/approach.png');

  return <AbsoluteFill style={{overflow: 'hidden'}}>
    <Img src={staticFile('storyboard/vrstvy/hangar/00-pozadi.png')} style={fill}/>
    {frame >= 421 && <BeastCel src={shape} padded={animated} style={{
      position:'absolute', left:shadowCenter-shadowWidth/2, top:sole-size*.028,
      width:shadowWidth, height:size*.085, transformOrigin:'center',
      transform:'skewX(-54deg) scaleY(-1)', filter:'brightness(0) blur(8px)',
      opacity: .55,
    }}/>}
    {frame >= 424 && <>
      <svg viewBox="0 0 1920 1080" style={fill} aria-hidden="true">
        <defs><radialGradient id="stalker-floor-shadow"><stop stopColor="#11171a" stopOpacity=".74"/>
          <stop offset="1" stopColor="#11171a" stopOpacity="0"/></radialGradient></defs>
        <ellipse cx={center} cy={sole-11} rx={size*.54} ry={size*.052} fill="url(#stalker-floor-shadow)"/>
      </svg>
      <BeastCel src={shape} padded={animated} style={{
        position:'absolute', left:center-size/2, top:sole-size, width:size, height:size,
        transformOrigin:'50% 94%', transform:`rotate(${lean}deg)`,
        filter:`brightness(${illumination})`,
      }}/>
    </>}
    {frame >= 438 && <Img src={staticFile('hangar/ready-rifle.png')} style={{
      ...fill, transformOrigin: '21% 100%',
      transform:`translate(${-52*(1-brace)}px,${652-623*brace}px) rotate(${-8*(1-brace)}deg)`,
    }}/>}
  </AbsoluteFill>;
}

function Guard({frame}: {frame: number}) {
  const pressure = travel(frame, 505, 533) * (1 - travel(frame, 538, 557));
  const torn = travel(frame, 533, 543);
  const edge = -135 + torn * 600;
  const propDetail = frame >= 460 && frame < 480;
  const impactDetail = frame >= 534;
  const recovery = 1 - travel(frame, 534, 547);
  let camera = 'none';
  if (propDetail) {
    const recoil = 1 - travel(frame,460,468);
    camera = `translate(${-495-20*recoil}px,${-430-13*recoil}px) scale(${1.79+.025*recoil})`;
  }
  if (impactDetail) camera = `translate(-${12 * recovery}px,${-848 + 12 * recovery}px) scale(1.95)`;

  // A short contraction on contact, followed by a slower release. Leave the
  // torn sleeve in the clear part of the ellipse and the card above the effect.
  const wound = interpolate(frame, [533, 534, 537, 545, 558, 580], [0, .7, 1, .67, .38, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return <AbsoluteFill style={{overflow: 'hidden'}}>
    <div style={{...fill, transformOrigin: '0 0', transform: camera}}>
      {hangar.layers.map((layer) => {
        const transform = `translate(${layer.dx * pressure}px,${layer.dy * pressure}px)`;
        return <Img key={layer.file}
          src={staticFile('storyboard/vrstvy/' + layer.file)} style={{...fill, transform}}/>;
      })}
      {torn < 1 && <Img src={staticFile('hangar/sleeve.png')} style={{
        position: 'absolute', left: 0, top: 642, width: 375, height: 304,
        transform: `translate(${pressure}px,${pressure}px)`,
        clipPath: `polygon(${edge + 72}px 0,100% 0,100% 100%,${edge - 42}px 100%)`,
      }}/>}
    </div>
    {wound > 0 && <AbsoluteFill style={{
      opacity: wound,
      background: 'radial-gradient(ellipse 72% 83% at 42% 59%, transparent 42%, rgba(87,13,35,.14) 61%, rgba(118,13,39,.59) 81%, rgba(58,4,23,.92) 100%)',
    }}/>}
  </AbsoluteFill>;
}

function Escape({frame}: {frame: number}) {
  // The three bodies, crate handles and kit stay rigidly registered. The
  // shutter draws down BEHIND the crew after it has passed the lintel.
  const stepFrame = Math.max(0, Math.min(51, frame - 608));
  const approach = stepFrame / 51;
  const slide = travel(frame, 634, 653);
  const shutterBottom = 232 + 400 * slide;
  const crewScale = .93 + approach * .093;
  const sway = Math.sin(stepFrame / 25 * 2 * Math.PI) * 2;
  return <AbsoluteFill style={{overflow: 'hidden'}}>
    <Img src={staticFile('storyboard/vrstvy/hangar/00-pozadi.png')} style={fill}/>
    <Img src={staticFile('hangar/shutter.png')} style={{
      position: 'absolute', left: 0, top: shutterBottom - 654, width: 1128, height: 654,
      filter: 'drop-shadow(0px 11px 8px rgba(11, 16, 24, .45))',
    }}/>
    <Img src={staticFile('storyboard/vrstvy/rescue/01-prah.png')} style={{
      ...fill,
      // Use only the threshold uprights and ceiling; the original foreground
      // floor contains silhouettes belonging to the later rescue composition.
      clipPath: 'polygon(0 0,100% 0,100% 100%,61% 100%,56% 81%,50% 79%,0 77%)',
    }}/>
    <div style={{
      ...fill, transformOrigin: '0 0',
      transform: `translate(${55 + 70 * approach}px,${161 - 36 * approach - sway}px) scale(${crewScale})`,
    }}>
      <Img src={staticFile(`picture-b/step-${String(stepFrame).padStart(2,'0')}.webp`)} style={{
        position:'absolute', left:35, top:155, width:675, height:568,
      }}/>
    </div>
  </AbsoluteFill>;
}

export function HangarPlate({frame, beastMotion}: HangarProps) {
  if (frame < 460) return <Approach frame={frame} beastMotion={beastMotion}/>;
  return frame < 608 ? <Guard frame={frame}/> : <Escape frame={frame}/>;
}
