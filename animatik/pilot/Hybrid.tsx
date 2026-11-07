import {AbsoluteFill, Composition, Img, Sequence, registerRoot, staticFile, useCurrentFrame} from 'remotion';
import {Graphics} from '../src/Graphics';
import {ScenePlate} from '../src/ScenePlate';
import {Dialogue} from '../src/SoundDialogue';
import {TableStage} from '../src/TableStage';
import cues from '../src/dialogue.json';

type Performance = {
  windows: number[][];
};

function PlayerAtTable({frame}: {frame: number}) {
  const sample = Math.floor(frame * 24 / 30);
  const path = 'storyboard/pilot/actor/';
  const placement = {position: 'absolute', left: 0, top: 0, width: 896, height: 832} as const;
  return <TableStage locale="cs"
    actress={<Img src={staticFile(path + 'residual.png')} style={placement} />}
    foreground={<Img src={staticFile(path + 'actor-' + String(sample).padStart(3, '0') + '.png')} style={placement} />}
  />;
}

// Pilot frame 0 is frame 750 in the full trailer. Filmed eye contact gives
// way to the approved hand and crate on their original edit points.
function Hybrid({windows}: Performance) {
  const frame = useCurrentFrame();
  const absolute = 750 + frame;
  const lines = cues.cs.slice(6, 9);
  const onInjury = frame >= 132 && frame < 168;
  // The pilot cuts to the torn forearm during “zranění”, then holds this
  // registered pose for reading. The next wide shot rejoins the master at 918.
  const storyFrame = onInjury ? 900 + Math.min(frame - 132, 17) : absolute;
  return <AbsoluteFill style={{background: '#121b23'}}>
    {frame < 66 && <PlayerAtTable frame={frame} />}
    {frame >= 66 && frame < 120 && <ScenePlate shotId="04b-volba" frame={absolute} locale="cs" />}
    {frame >= 120 && frame < 132 && <ScenePlate shotId="04c-unik" frame={absolute} locale="cs" />}
    {onInjury && <ScenePlate shotId="05a-zraneni" frame={storyFrame} locale="cs" />}
    {frame >= 168 && <ScenePlate shotId="04e-prah" frame={absolute} locale="cs" />}
    <Graphics frame={storyFrame} locale="cs" />
    {windows.map(([start, end], i) => <Sequence key={i} from={start} durationInFrames={end - start}>
      <Dialogue cue={lines[i]} />
    </Sequence>)}
  </AbsoluteFill>;
}

const Pilot = () => <Composition id="Hybrid" component={Hybrid} width={1920} height={1080}
  fps={30} durationInFrames={180}
  defaultProps={{windows: [[8, 66], [74, 109], [117, 144]]}} />;

registerRoot(Pilot);
