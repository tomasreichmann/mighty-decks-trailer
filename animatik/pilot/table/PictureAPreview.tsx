import {AbsoluteFill, Composition, Sequence, registerRoot, useCurrentFrame} from 'remotion';
import PictureA from '../../src/PictureA';
import {Graphics} from '../../src/Graphics';
import {Dialogue} from '../../src/SoundDialogue';
import cues from '../../src/dialogue.json';

const decisionCues = [[8,66], [74,109], [117,144]];
function Decision() {
  const frame = useCurrentFrame() + 750;
  return <AbsoluteFill style={{background:'#121b23'}}>
    <PictureA frame={frame} lang="cs"/>
    <Graphics frame={frame >= 882 && frame < 918 ? 900 : frame} locale="cs"/>
    {decisionCues.map(([start,end],i)=><Sequence key={start} from={start} durationInFrames={end-start}>
      <Dialogue cue={cues.cs[6+i]}/>
    </Sequence>)}
  </AbsoluteFill>;
}
registerRoot(()=> <Composition id="PictureA" component={Decision} width={1920} height={1080} durationInFrames={180} fps={30}/>);
