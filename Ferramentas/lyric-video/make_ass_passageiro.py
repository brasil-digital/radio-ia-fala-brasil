# -*- coding: utf-8 -*-
import json

SRC = r"C:\Users\Owner\Radio-IA-Fala-Brasil\Artistas\13-MC-Foguete\Clipe-Passageiro\letra_passageiro.json"
OUT = r"C:\Users\Owner\AppData\Local\Temp\claude\C--Users-Owner\76d66d91-2272-4e59-b55e-241596b8466d\scratchpad\montagem\legendas.ass"

# Known transcription fix documented in ROTEIRO.md
FIX_TEXT = {
    "Pé-pé-pé-pé-pé-sia me ensinando mito, filosofima": "Pérsia me ensinando mito e filosofia",
}
FIX_WORDS = {
    153.56: [
        {"w": " Pérsia", "s": 153.56, "e": 154.3},
        {"w": " me", "s": 154.3, "e": 154.6},
        {"w": " ensinando", "s": 154.6, "e": 155.3},
        {"w": " mito", "s": 155.3, "e": 155.8},
        {"w": " e", "s": 155.8, "e": 155.95},
        {"w": " filosofia", "s": 155.95, "e": 156.62},
    ]
}

def fmt_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"

def build_karaoke_text(words):
    parts = []
    for w in words:
        dur_cs = max(1, round((w["e"] - w["s"]) * 100))
        parts.append(f"{{\\k{dur_cs}}}{w['w']}")
    return "".join(parts)

HEADER = """[Script Info]
Title: Passageiro do Mundo - MC Foguete
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Lyric,Montserrat,54,&H00FFFFFF,&H0000D7FF,&H00202020,&H80000000,1,0,0,0,100,100,0,0,1,3,1,2,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def main():
    with open(SRC, encoding="utf-8") as f:
        data = json.load(f)

    events = []
    for line in data:
        text = line["text"]
        words = line["words"]
        if text in FIX_TEXT:
            text = FIX_TEXT[text]
        if line["start"] in FIX_WORDS:
            words = FIX_WORDS[line["start"]]

        karaoke = build_karaoke_text(words)
        start = fmt_time(line["start"])
        end = fmt_time(line["end"])
        events.append(f"Dialogue: 0,{start},{end},Lyric,,0,0,0,,{karaoke}")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(HEADER)
        f.write("\n".join(events) + "\n")

    print(f"Wrote {len(events)} lines to {OUT}")

if __name__ == "__main__":
    main()
