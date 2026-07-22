# -*- coding: utf-8 -*-
import json
from faster_whisper import WhisperModel

mp3 = r"C:\Users\Owner\Downloads\Passageiro do Mundo.mp3"
out = r"C:\Users\Owner\AppData\Local\Temp\claude\C--Users-Owner\b71b767b-d6a2-4a86-a123-c1efe21722b8\scratchpad\letra_passageiro.json"

model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
segments, info = model.transcribe(mp3, language="pt", word_timestamps=True,
                                  beam_size=5, condition_on_previous_text=False)

data = []
for seg in segments:
    words = [{"w": w.word, "s": round(w.start, 2), "e": round(w.end, 2)} for w in (seg.words or [])]
    data.append({"start": round(seg.start, 2), "end": round(seg.end, 2),
                 "text": seg.text.strip(), "words": words})
    print(f"[{seg.start:7.2f} - {seg.end:7.2f}] {seg.text.strip()}", flush=True)

with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("OK ->", out)
