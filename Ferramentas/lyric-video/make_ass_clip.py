# -*- coding: utf-8 -*-
import json
import sys

SRC = r"C:\Users\Owner\Radio-IA-Fala-Brasil\Artistas\13-MC-Foguete\Clipe-Passageiro\letra_passageiro.json"

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
    t = max(0.0, t)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"

def build_karaoke_text(words, shift):
    parts = []
    for w in words:
        dur_cs = max(1, round((w["e"] - w["s"]) * 100))
        parts.append(f"{{\\k{dur_cs}}}{w['w']}")
    return "".join(parts)

HEADER = """[Script Info]
Title: Passageiro do Mundo - MC Foguete (clip)
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Lyric,Montserrat,52,&H00FFFFFF,&H0000D7FF,&H00202020,&H80000000,1,0,0,0,100,100,0,0,1,3,1,2,50,50,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def main():
    clip_start = float(sys.argv[1])
    clip_dur = float(sys.argv[2])
    out_path = sys.argv[3]
    clip_end = clip_start + clip_dur

    with open(SRC, encoding="utf-8") as f:
        data = json.load(f)

    events = []
    for line in data:
        if line["end"] <= clip_start or line["start"] >= clip_end:
            continue
        text = line["text"]
        words = line["words"]
        if text in FIX_TEXT:
            text = FIX_TEXT[text]
        if line["start"] in FIX_WORDS:
            words = FIX_WORDS[line["start"]]

        karaoke = build_karaoke_text(words, clip_start)
        start = fmt_time(line["start"] - clip_start)
        end = fmt_time(min(line["end"], clip_end) - clip_start)
        events.append(f"Dialogue: 0,{start},{end},Lyric,,0,0,0,,{karaoke}")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(HEADER)
        f.write("\n".join(events) + "\n")

    print(f"Wrote {len(events)} lines to {out_path} (shifted by -{clip_start}s)")

if __name__ == "__main__":
    main()
