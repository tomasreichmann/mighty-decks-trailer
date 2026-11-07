"""Audition Czech pickups against the voices of the selected synthetic performances."""
import json
from pathlib import Path
import soundfile as sf
import torch
from fish_speech.models.text2semantic.inference import init_model, load_codec_model, encode_audio, decode_to_audio, generate_long

root = Path(__file__).resolve().parents[1]
output = root / "pilot" / "sound-pickups"
output.mkdir(exist_ok=True)
fish = Path("C:/AI/Tools/Fish-Speech/checkpoints/s2-pro")
lines = json.loads((root / "src/dialogue.json").read_text(encoding="utf8"))["cs"]
model, decoder = init_model(fish, "cuda", torch.bfloat16, compile=False)
model.config.max_seq_len = 4096
with torch.device("cuda"):
    model.setup_caches(max_batch_size=1, max_seq_len=4096, dtype=torch.bfloat16)
codec = load_codec_model(fish / "codec.pth", "cuda", torch.bfloat16)
for index, reference, ref_text in [
    (1, "performance/cs-02.wav", lines[1]["text"]),
    (10, "performance/cs-07.wav", lines[6]["text"]),
    (11, "performance/cs-07.wav", lines[6]["text"]),
]:
    codes = encode_audio(root / "public/audio" / reference, codec, "cuda").cpu()
    torch.manual_seed(816 + index)
    with torch.inference_mode():
        responses = generate_long(model=model, device="cuda", decode_one_token=decoder,
                text=lines[index-1]["text"], max_new_tokens=240, top_p=.7, top_k=30,
                temperature=.7, compile=False, iterative_prompt=False,
                prompt_text=[ref_text], prompt_tokens=[codes])
        seq = torch.cat([r.codes for r in responses if r.action == "sample"], dim=1)
        waveform = decode_to_audio(seq.to("cuda"), codec).float().cpu().numpy()
    sf.write(output / f"cs-{index:02d}.wav", waveform, codec.sample_rate)
    print(f"Pickup {index} recorded", flush=True)
