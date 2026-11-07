"""Czech-only CPU audition conditioned on the same synthetic role recordings."""
from pathlib import Path
import json
import torch
import soundfile as sf
from pocket_tts import TTSModel
p=Path(__file__).resolve().parents[1]
d=json.loads((p/'src/dialogue.json').read_text(encoding='utf8'))['cs']
torch.set_num_threads(3)
torch.set_num_interop_threads(1)
m=TTSModel.load_model(config='hf://vvolhejn/pocket-tts-czech/czech.yaml@7c1fbd0acba765617749dd17f3dbddc2be791cc7',temp=.3)
for i,ref in [(10,7),(11,7),(1,2)]:
 torch.manual_seed(716+i)
 state=m.get_state_for_audio_prompt(str(p/'public/audio/performance'/f'cs-{ref:02d}.wav'))
 out=m.generate_audio(state,d[i-1]['text'])
 sf.write(p/'pilot/sound-pickups'/f'pocket-cs-{i:02d}.wav',out.detach().cpu().numpy().squeeze(),m.sample_rate)
 print(i, 'done',flush=True)
