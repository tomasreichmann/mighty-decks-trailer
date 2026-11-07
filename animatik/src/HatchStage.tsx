import type {CSSProperties} from "react";
import {AbsoluteFill, Easing, Img, interpolate, staticFile} from "remotion";

const sheet: CSSProperties = {position:"absolute", left:0, top:0, width:1920, height:1080};
const hatch = (file: string) => staticFile("storyboard/vrstvy/hatch/" + file + ".png");
const room = hatch("00-pozadi");
const ease = {extrapolateLeft:"clamp", extrapolateRight:"clamp", easing:Easing.inOut(Easing.cubic)} as const;
const progress = (f: number, a: number, b: number) => interpolate(f, [a,b], [0,1], ease);
const opening = "M0 0H1028V867L1004 890L0 930Z";
// The bottom of the leaf surrounds the real latch boss, which projects below the sill.
const door = "M0 0H1025V867L1004 888L774 897L749 921L696 940Q671 1048 551 1058Q421 1070 383 957L0 946Z";
const windowHole = "M536 27C688 26 810 146 810 294C810 440 690 552 538 552C389 552 264 439 264 297C264 150 384 29 536 27Z";
const leafClip = `path(evenodd, "${door} ${windowHole}")`;

function Coordinates({frame}: {frame:number}) {
  const draw = progress(frame,330,344);
  if (!draw || frame >= 377) return null;
  return <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{...sheet, opacity:1-progress(frame,362,377)}}>
    <g fill="none" strokeLinecap="round" strokeLinejoin="round" style={{filter:"drop-shadow(0 0 4px #dc912d)"}}>
      <path d="M324 804L346 808L360 817L369 833 M370 781L378 796L386 808L391 825"
        stroke="#ffe4a0" strokeWidth="3.4" pathLength="1" strokeDasharray="1" strokeDashoffset={1-draw} />
      {[[324,804],[346,808],[360,817],[369,833],[370,781],[386,808],[391,825]].map(([x,y],i) =>
        <circle key={x} cx={x} cy={y} r={i===0||i===4?4.1:2.8} fill="#fff2ba" opacity={Math.min(1,draw*3)} />)}
    </g>
  </svg>;
}

function OpenBay({offset, frame}: {offset:number; frame:number}) {
  const shadowTravel = interpolate(frame, [395, 405, 419], [-475, -75, 510], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  return <AbsoluteFill>
    {/* Stationary cabin floor from the right of the same drawing, underneath the latch. */}
    <div style={{position:"absolute",left:0,top:886,width:1029,height:194,overflow:"hidden",
      maskImage:"linear-gradient(to right,black 85%,transparent)"}}>
      <Img src={room} style={{...sheet,left:-890,top:-886}} />
    </div>
    <div style={{...sheet, clipPath:`path("${opening}")`}}>
    <Img src={staticFile("storyboard/vrstvy/hangar/00-pozadi.png")} style={{...sheet,left:-495,top:-2,width:1925,height:1083}} />
    {frame >= 395 && <div style={{...sheet, clipPath:"polygon(0 66%,54% 59%,54% 84%,0 87%)"}}>
      <Img src={staticFile("storyboard/vrstvy/hangar/01-selma.png")} style={{
        ...sheet, transformOrigin:"0 0", transform:`matrix(.50,-.035,.17,.16,${shadowTravel},740)`,
        filter:"brightness(0) blur(10px)", opacity:.53,
      }} />
    </div>}
    <svg width={1920} height={1080} style={sheet} aria-hidden>
      <defs>
        <radialGradient id="hatch-footprint"><stop stopColor="#251a17" stopOpacity=".65"/><stop offset="1" stopColor="#251a17" stopOpacity="0"/></radialGradient>
        <linearGradient id="hatch-jamb"><stop stopColor="#111921" stopOpacity="0"/><stop offset="1" stopColor="#111921" stopOpacity=".83"/></linearGradient>
      </defs>
      <g fill="url(#hatch-footprint)">
        <ellipse cx="745" cy="676" rx="267" ry="26" opacity=".48" transform="rotate(-5 745 676)" />
        {[[476,707,34],[620,681,36],[715,682,23],[866,666,29],[1010,664,35]].map(([x,y,rx]) =>
          <ellipse key={x} cx={x} cy={y} rx={rx} ry="7.5" />)}
      </g>
      <path d="M983 0H1029V870L1005 891L0 931V919L992 877Z" fill="url(#hatch-jamb)" />
      <path d="M1020 0V861L998 884L0 925" stroke="#28282b" strokeWidth="8" fill="none" />
      <path d="M1014 0V861L996 879L0 919" stroke="#bc9b75" strokeWidth="3" opacity=".8" fill="none" />
    </svg>
    <Img src={staticFile("production/hatch/crew.png")} style={{position:"absolute",left:420,top:209,width:658,height:514}} />
    </div>
    <div style={{...sheet, transform:`translateX(${offset}px)`}}>
      {/* The glass belongs to the moving leaf. The people and ship stay in the bay. */}
      <div style={{...sheet, clipPath:`path("${windowHole}")`,background:"linear-gradient(126deg, #a0bbc833 15%, #dce1cc17 36%, #b7cfdf35 39%, #c2d5da0a 54%, #21324739 80%)"}} />
      <Img src={room} style={{...sheet,clipPath:leafClip}} />
      <svg width={1920} height={1080} style={sheet} aria-hidden>
        <path d={windowHole} fill="none" stroke="#322e2e" strokeWidth="3" />
        <path d={door} fill="none" stroke="#15191c" strokeWidth="7" />
        <path d="M1018 0V865L997 882" fill="none" stroke="#82725f" strokeWidth="3" />
      </svg>
    </div>
  </AbsoluteFill>;
}

/** Absolute frames. The cuts isolate the coordinates and the latch before the door travels. */
export function HatchStage({frame}: {frame:number}) {
  const wristInsert = frame >= 330 && frame < 376;
  const returnToBay = frame >= 376;
  const offset = -518 * progress(frame,376,403);
  const angle = -18 * progress(frame,357,368);
  return <AbsoluteFill style={{overflow:"hidden"}}>
    <div style={{...sheet,transformOrigin:"0 0",transform:wristInsert ? "translate(-42px,-777px) scale(1.76)" : undefined}}>
      <Img src={room} style={sheet} />
      {returnToBay ? <OpenBay offset={offset} frame={frame} /> :
        <Img src={hatch("01-paserak")} style={{...sheet,left:-3*progress(frame,185,250)}} />}
      {frame < 330 ? <Img src={hatch("02-paka")} style={sheet}/> :
        <div style={{...sheet,transformOrigin:"531px 902px", transform:`translateX(${offset}px) rotate(${angle}deg)`}}>
          <Img src={staticFile("production/hatch/lever.png")} style={{position:"absolute",left:0,top:456,width:740,height:624}} />
          <Coordinates frame={frame} />
        </div>}
    </div>
  </AbsoluteFill>;
}
