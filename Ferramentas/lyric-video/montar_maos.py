# -*- coding: utf-8 -*-
# Clipe "Mãos de Trabalhador" - MC Foguete (imagens realísticas Gemini)
import json, os

BASE = r"C:\Users\Owner\AppData\Local\Temp\claude\C--Users-Owner\b71b767b-d6a2-4a86-a123-c1efe21722b8\scratchpad"
DUR_TOTAL = 219.84
FPS = 30

segs = json.load(open(os.path.join(BASE, "letra_maos.json"), encoding="utf-8"))

# remove o "Tchau, tchau." do fade final
segs = [s for s in segs if "tchau" not in s["text"].lower()]

sub_fix = [
    ("O esposa às vezes reclama", "A esposa às vezes reclama"),
    ("Ajuda os pais idoso,", "Ajuda os pais idosos,"),
    ("ninguém nunca esquista", "ninguém nunca esquece"),
    ("a casa e a própria pressa", "a casa e a própria peça"),
    ("mesmo o pequeno tempo", "mesmo com o pouco tempo"),
    ("Pra fazer beijos, filho dormindo", "Pra fazer; beija o filho dormindo"),
]
for s in segs:
    t = s["text"]
    for a, b in sub_fix:
        t = t.replace(a, b)
    s["text"] = t

blocos = [
    (0.00, "cena01"), (24.88, "cena02"), (31.62, "cena03"), (35.96, "cena04"),
    (45.00, "cena05"), (53.88, "cena11"), (67.48, "cena06"), (73.18, "cena07"),
    (79.14, "cena08"), (91.12, "cena05"), (99.94, "cena11"), (113.48, "cena10"),
    (126.50, "cena04"), (132.72, "cena09"), (138.38, "cena07"), (143.94, "cena03"),
    (150.78, "cena05"), (159.60, "cena11"), (173.36, "cena12"), (186.96, "cena10"),
    (196.00, "cena12"),
]

SHORT_INI, SHORT_FIM = 150.78, 196.00

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def duas_linhas(t, lim=46):
    if len(t) <= lim: return t
    meio = len(t) // 2
    esq = t.rfind(" ", 0, meio); dirt = t.find(" ", meio)
    corte = esq if (meio - esq) <= (dirt - meio if dirt != -1 else 999) else dirt
    if corte == -1: return t
    l1, l2 = t[:corte], t[corte+1:]
    if len(l2) > lim:
        m2 = len(l2) // 2
        e2 = l2.rfind(" ", 0, m2); d2 = l2.find(" ", m2)
        c2 = e2 if (m2 - e2) <= (d2 - m2 if d2 != -1 else 999) else d2
        if c2 != -1: l2 = l2[:c2] + r"\N" + l2[c2+1:]
    return l1 + r"\N" + l2

HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Letra,Arial,{FS},&H00FFFFFF,&H00FFFFFF,&H00101010,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,80,80,{MV},1
Style: Refrao,Arial,{FSR},&H004AD2FF,&H00FFFFFF,&H00101010,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,80,80,{MV},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def eh_refrao(t):
    tl = t.lower()
    return ("mãos de trabalhador" in tl or "mão de trabalhador" in tl
            or "marcada de cimento" in tl or "prova de valor" in tl
            or "não pediu esmola" in tl or "ergueu com o próprio suor" in tl
            or "brasil é feito assim" in tl or "silencioso, forte" in tl)

def gerar_ass(caminho, W, H, FS, FSR, MV, t_ini=0.0, t_fim=DUR_TOTAL, offset=0.0):
    linhas = [HEAD.format(W=W, H=H, FS=FS, FSR=FSR, MV=MV)]
    for i, s in enumerate(segs):
        if s["end"] <= t_ini or s["start"] >= t_fim: continue
        ini = max(s["start"], t_ini) - offset
        fim = s["end"] - offset
        prox = segs[i+1]["start"] - offset if i+1 < len(segs) else 1e9
        fim = min(fim + 0.8, prox - 0.05, t_fim - offset)
        estilo = "Refrao" if eh_refrao(s["text"]) else "Letra"
        linhas.append(f"Dialogue: 0,{ts(ini)},{ts(fim)},{estilo},,0,0,0,,{duas_linhas(s['text'])}\n")
    open(caminho, "w", encoding="utf-8-sig").writelines(linhas)

gerar_ass(os.path.join(BASE, "letra_maos.ass"), 1920, 1080, 58, 62, 70)
gerar_ass(os.path.join(BASE, "letra_maos_short.ass"), 1080, 1920, 60, 64, 420,
          t_ini=SHORT_INI, t_fim=SHORT_FIM, offset=SHORT_INI)

# ---------- filtro do clipe principal (Ken Burns) ----------
mov = ["z='1+0.12*on/{D}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2'",
       "z='1.12-0.12*on/{D}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2'",
       "z=1.10:x='(iw-iw/zoom)*on/{D}':y='(ih-ih/zoom)/2'",
       "z=1.10:x='(iw-iw/zoom)*(1-on/{D})':y='(ih-ih/zoom)/2'"]
parts, cadeia = [], []
for i, (ini, cena) in enumerate(blocos):
    fim = blocos[i+1][0] if i+1 < len(blocos) else DUR_TOTAL
    dur = fim - ini
    frames = round(dur * FPS)
    m = mov[i % 4].format(D=frames-1)
    parts.append(
        f"[{i}:v]scale=2880:1620,zoompan={m}:d={frames}:s=1920x1080:fps={FPS},"
        f"fade=t=in:st=0:d=0.4,fade=t=out:st={dur-0.4:.2f}:d=0.4,setsar=1[v{i}];")
    cadeia.append(f"[v{i}]")
parts.append("".join(cadeia) + f"concat=n={len(blocos)}:v=1:a=0[vcat];")
parts.append("[vcat]subtitles=letra_maos.ass,format=yuv420p[vf]")
open(os.path.join(BASE, "filtro_maos.txt"), "w", encoding="utf-8").write("\n".join(parts))

inputs = " ".join(f'-i "cenas/{c}.png"' for _, c in blocos)
open(os.path.join(BASE, "inputs_maos.txt"), "w", encoding="utf-8").write(inputs)

# ---------- filtro do SHORT (fundo desfocado + overlay) ----------
short_blocos = [(ini, c) for ini, c in blocos if SHORT_INI <= ini < SHORT_FIM]
sparts, scadeia = [], []
for i, (ini, cena) in enumerate(short_blocos):
    fim = short_blocos[i+1][0] if i+1 < len(short_blocos) else SHORT_FIM
    dur = fim - ini
    sparts.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5[bg{i}];")
    sparts.append(f"[{i}:v]scale=1080:-2[fg{i}];")
    fade_out = dur - 0.3
    sparts.append(f"[bg{i}][fg{i}]overlay=(W-w)/2:(H-h)/2,fade=t=in:st=0:d=0.3,fade=t=out:st={fade_out:.2f}:d=0.3,setsar=1,fps={FPS}[c{i}];")
    scadeia.append(f"[c{i}]")
sparts.append("".join(scadeia) + f"concat=n={len(short_blocos)}:v=1:a=0[vcat];")
sparts.append("[vcat]subtitles=letra_maos_short.ass,format=yuv420p[vf];")
sdur = SHORT_FIM - SHORT_INI
sparts.append(f"[{len(short_blocos)}:a]atrim=start={SHORT_INI}:end={SHORT_FIM},asetpts=PTS-STARTPTS,afade=t=out:st={sdur-1.4:.2f}:d=1.4[af]")
open(os.path.join(BASE, "filtro_maos_short.txt"), "w", encoding="utf-8").write("\n".join(sparts))

sinputs_list = []
for i, (ini, c) in enumerate(short_blocos):
    fim = short_blocos[i+1][0] if i+1 < len(short_blocos) else SHORT_FIM
    sinputs_list.append(f'-loop 1 -t {fim-ini:.2f} -i "cenas/{c}.png"')
sinputs = " ".join(sinputs_list)
open(os.path.join(BASE, "inputs_maos_short.txt"), "w", encoding="utf-8").write(sinputs)

print("Blocos clipe:", len(blocos), "| audio input index:", len(blocos))
for i, (ini, cena) in enumerate(blocos):
    fim = blocos[i+1][0] if i+1 < len(blocos) else DUR_TOTAL
    print(f"  {ini:7.2f} - {fim:7.2f}  {cena}")
print("Blocos short:", len(short_blocos), "| dur:", f"{sdur:.2f}s")
print("OK")
