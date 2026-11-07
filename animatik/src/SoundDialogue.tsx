import type {CSSProperties} from 'react';
import {Html5Audio, Img, Sequence, staticFile} from 'remotion';
import dialogue from './dialogue.json';

type Locale = 'cs' | 'en';
type Cue = (typeof dialogue.cs)[number];

// The artist's sheet is a registered 2 x 2 portrait atlas. Player/Exile share a
// voice, yet use different portraits so each change of viewpoint reads at once.
const portraits: Record<string, readonly [number, number]> = {
  Hráčka: [0, 0], Player: [0, 0],
  Vypravěč: [1, 0], Storyteller: [1, 0],
  Vyhnankyně: [0, 1], Exile: [0, 1],
  Pašerák: [1, 1], Smuggler: [1, 1],
};

const lettering: CSSProperties = {
  fontFamily: '"Segoe UI", Arial, sans-serif',
  fontWeight: 700,
  paintOrder: 'stroke fill',
  WebkitTextStroke: '8px #121b23',
  textShadow: '0 2px 2px #121b23',
};

export function Dialogue({cue}: {cue: Cue}) {
  const [col, row] = portraits[cue.speaker];
  const invitation = cue.startFrame >= 1350;
  const size = invitation ? 144 : 216;
  // During the overhead choice, keep the captions to the left of all three
  // physical faces. The wide table and CTA have a full line clear at the foot.
  let width = 635;
  if (cue.startFrame < 180) width = 730;
  if ((cue.startFrame >= 750 && cue.startFrame < 816) || cue.startFrame >= 1350) width = 1590;
  if (cue.startFrame >= 816 && cue.startFrame < 930) width = 418;
  return <>
    <div style={{
      position: 'absolute', left: 40, bottom: 24, width: size, height: size,
      border: '4px solid #efd9bb', boxSizing: 'content-box',
      boxShadow: '0 0 0 2px #121b23', backgroundColor: '#121b23', overflow: 'hidden',
    }}>
      <Img src={staticFile('reference/planches/portraits.png')} style={{
        position: 'absolute', width: size * 2, height: size * 2, left: -size * col, top: -size * row,
        maxWidth: 'none',
      }}/>
    </div>
    <div style={{...lettering, position: 'absolute', left: invitation ? 218 : 286, bottom: invitation ? 28 : 43, width}}>
      <div style={{color: '#efd9bb', fontSize: 35, lineHeight: '42px', marginBottom: 5,
        textTransform: 'uppercase'}}>{cue.speaker}</div>
      <div style={{color: '#fff', fontSize: invitation ? 60 : 68, lineHeight: '70px'}}>{cue.text}</div>
    </div>
  </>;
}

export type Music = 'lift' | 'constancy' | 'getaway';

export function SoundDialogue({locale, music}: {locale: Locale; music: Music}) {
  return <>
    <Html5Audio name="Music" src={staticFile(`audio/music/${music}-${locale}.wav`)}/>
    <Html5Audio name="Room" src={staticFile('audio/room.wav')}/>
    <Html5Audio name="Pulse" src={staticFile('audio/pulse.wav')}/>
    <Html5Audio name="Foley" src={staticFile(`audio/final-foley-${locale}.wav`)}/>
    {dialogue[locale].map((cue) => (
      <Sequence key={cue.file} name={cue.speaker + ' · ' + cue.text}
        from={cue.startFrame} durationInFrames={cue.endFrame - cue.startFrame}>
        <Html5Audio name={cue.speaker} src={staticFile('audio/' + cue.file)}/>
        <Dialogue cue={cue}/>
      </Sequence>
    ))}
  </>;
}

