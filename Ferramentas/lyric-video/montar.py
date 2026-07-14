# -*- coding: utf-8 -*-
# Gera letra.ass, letra_short.ass e filtro FFmpeg para o clipe
# "Segunda Casa, Primeiro Amor" - MC Foguete
import json, math, os

BASE = r"C:\Users\Owner\AppData\Local\Temp\claude\C--Users-Owner\92356ebf-ee78-4d8e-987b-49aa0af45618\scratchpad"
DUR_TOTAL = 303.84
FPS = 30

segs = json.load(open(os.path.join(BASE, "letra_timestamps.json"), encoding="utf-8"))

# --- correções de transcrição (needle -> texto completo novo) ---
full_fix = [
    ("two sets", "Essa aqui é pra Massachusetts inteiro"),
    ("Summerville", "Framingham, Medford, Somerville, Cape Cod"),
    ("nunca eu me atreve", "Que talvez nunca eu me atreva a voltar pra morar, só pra visitar de vez em quando"),
    ("bate, mas cedo", "Mas o coração ainda mora onde o sol bate mais cedo, no aconchego"),
    ("Que sustento", "É o que sustenta"),
    ("Tio Setsi", "Massachusetts me deu chão, me deu chance"),
    ("Massatio", "Massachusetts de verão sabe também abraçar"),
    ("Freeming", "Boston, Framingham, todo canto onde o brasileiro passou"),
    ("Tuxete", "Massachusetts me deu chão, me deu chance, me deu emprego"),
    ("Coguete", "Foguete decola"),
    ("me aposta", "Vai, minha gente, vai"),
]
sub_fix = [
    ("não aconchego", "no aconchego"),
    ("Viva entre dois mundos", "Vivo entre dois mundos"),
    ("virou lá que", "virou lar que"),
    ("É, foguete", "Ê, Foguete!"),
]
for s in segs:
    t = s["text"]
    for needle, new in full_fix:
        if needle.lower() in t.lower():
            t = new
            break
    for a, b in sub_fix:
        t = t.replace(a, b)
    s["text"] = t

# --- cenas por bloco de tempo (start, cena) ---
blocos = [
    (0.00, 1), (16.68, 2), (27.24, 4), (41.58, 3), (50.26, 5),
    (82.22, 2), (96.96, 3), (115.82, 5), (147.28, 3), (161.80, 1),
    (187.38, 4), (210.12, 2), (223.48, 5), (253.82, 3), (286.20, 6),
]

# --- ASS helpers ---
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
    if len(l2) > lim:  # três linhas se ainda longo
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
    return "primeiro amor" in tl or "segunda casa" in tl or "vivendo de saudade" in tl

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

gerar_ass(os.path.join(BASE, "letra.ass"), 1920, 1080, 58, 62, 70)
gerar_ass(os.path.join(BASE, "letra_short.ass"), 1080, 1920, 60, 64, 420,
          t_ini=50.26, t_fim=80.62, offset=50.26)

# --- filtro FFmpeg do vídeo principal ---
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
parts.append("[vcat]subtitles=letra.ass,format=yuv420p[vf]")
open(os.path.join(BASE, "filtro_clipe.txt"), "w", encoding="utf-8").write("\n".join(parts))

# lista de inputs na ordem dos blocos
inputs = " ".join(f'-i "cenas/cena{c}.png"' for _, c in blocos)
open(os.path.join(BASE, "inputs_clipe.txt"), "w", encoding="utf-8").write(inputs)

print("Blocos:", len(blocos))
for i, (ini, cena) in enumerate(blocos):
    fim = blocos[i+1][0] if i+1 < len(blocos) else DUR_TOTAL
    print(f"  {ini:7.2f} - {fim:7.2f}  cena{cena}")
print("OK: letra.ass, letra_short.ass, filtro_clipe.txt, inputs_clipe.txt")
