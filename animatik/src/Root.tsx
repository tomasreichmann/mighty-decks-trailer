import {Composition} from 'remotion';
import cut from '../../storyboard/strih.json';
import {Trailer} from './Trailer';

const {width, height, fps, durationInFrames} = cut;
const size = {width, height, fps, durationInFrames};

export const RemotionRoot = () => (
  <>
    <Composition id="Fangs-CS" component={Trailer} defaultProps={{locale: 'cs' as const}} {...size} />
    <Composition id="Fangs-EN" component={Trailer} defaultProps={{locale: 'en' as const}} {...size} />
  </>
);
