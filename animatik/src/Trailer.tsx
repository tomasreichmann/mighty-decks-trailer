import {AbsoluteFill, Sequence, useCurrentFrame} from 'remotion';
import cut from '../../storyboard/strih.json';
import {ScenePlate} from './ScenePlate';
import PictureA from './PictureA';
import PictureB from './PictureB';
import {Graphics} from './Graphics';
import {SoundDialogue, type Music} from './SoundDialogue';

export type Locale = 'cs' | 'en';
type Shot = (typeof cut.shots)[number];
type TrailerProps = {locale: Locale; beastMotion?: boolean; music?: Music};

function ShotImage({shot, locale, beastMotion}: TrailerProps & {shot: Shot}) {
  const localFrame = useCurrentFrame();
  const frame = shot.in + localFrame;
  return <>
    {(frame < 180 || (frame >= 660 && frame < 930)) ? <PictureA frame={frame} lang={locale} />
      : frame >= 930 ? <PictureB frame={frame} lang={locale} />
      : <ScenePlate shotId={shot.id} frame={frame} locale={locale} beastMotion={beastMotion ?? true} />}
    {frame < 1230 && <Graphics frame={frame} locale={locale} />}
  </>;
}

export const Trailer = ({locale, beastMotion, music = 'lift'}: TrailerProps) => (
  <AbsoluteFill style={{backgroundColor: '#121b23', overflow: 'hidden'}}>
    {cut.shots.map((shot) => (
      <Sequence key={shot.id} from={shot.in} durationInFrames={shot.out - shot.in} name={shot[locale].action}>
        <ShotImage shot={shot} locale={locale} beastMotion={beastMotion} />
      </Sequence>
    ))}
    <SoundDialogue locale={locale} music={music} />
  </AbsoluteFill>
);
