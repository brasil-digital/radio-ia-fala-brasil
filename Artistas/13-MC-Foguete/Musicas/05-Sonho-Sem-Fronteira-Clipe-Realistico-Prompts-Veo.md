# Sonho Sem Fronteira — Clipe Realístico (Shot List + Prompts Veo)

**Objetivo:** clipe com cara de FILMADO, não de IA. Música: 4:35 (275s).
**Método:** 14 cenas de 8s no Veo → câmera lenta 0.5x no FFmpeg (vira ~16s cada)
→ montagem sincronizada com a letra (timestamps via faster-whisper) → color grade
de filme. Câmera lenta é proposital: esconde artefatos de IA e dá tom emocional.

---

## REGRAS DE REALISMO (aplicar em TODA cena)

Todo prompt termina com este bloco fixo:

```
Shot on 35mm film, handheld documentary style, shallow depth of field,
natural lighting, visible skin texture, subtle film grain, muted realistic
colors, slight camera shake, photorealistic, no text, no captions
```

**Evitar (denuncia IA):** close de mãos fazendo gestos complexos, placas/letreiros
legíveis, multidões grandes em movimento rápido, rostos muito próximos da câmera
por mais de 3s.

**PROTAGONISTA FIXO** — usar esta descrição IDÊNTICA em toda cena em que ele aparece
(é o que garante que pareça a mesma pessoa no clipe inteiro):

```
a Brazilian man in his early 30s, short dark curly hair, trimmed beard,
tired but determined brown eyes, wearing a worn gray hoodie
```

---

## SHOT LIST (sincronizada com a letra)

### CENA 1 — Abertura: o quarto vazio (intro falada, ~0:00-0:25)
*"Essa aqui eu escrevo com o peito apertado"*
```
Cinematic 8 second shot: a Brazilian man in his early 30s, short dark curly
hair, trimmed beard, tired but determined brown eyes, wearing a worn gray
hoodie, sits on the edge of a bare mattress in a small empty bedroom in
Brazil at dawn, packed duffel bag at his feet, he stares at an old family
photo in his hands, dust floating in a beam of pale morning light from the
window. Shot on 35mm film, handheld documentary style, shallow depth of
field, natural lighting, visible skin texture, subtle film grain, muted
realistic colors, slight camera shake, photorealistic, no text, no captions
```

### CENA 2 — A mãe na porta (~0:25-0:45)
*"Deixou a casa, deixou a mãe chorando na porta"*
```
Cinematic 8 second shot: an elderly Brazilian woman with gray hair stands
in the doorway of a simple house in a Brazilian small town at dawn, holding
back tears, she embraces a Brazilian man in his early 30s, short dark curly
hair, trimmed beard, wearing a worn gray hoodie, he carries a duffel bag,
he walks away down the dirt street and she watches, hand over her mouth.
Shot on 35mm film, handheld documentary style, shallow depth of field,
natural lighting, visible skin texture, subtle film grain, muted realistic
colors, slight camera shake, photorealistic, no text, no captions
```

### CENA 3 — O consulado / o "não" (~0:45-1:00)
*"Foi no consulado sonhando com visto na mão / Ouviu um não"*
```
Cinematic 8 second shot: a Brazilian man in his early 30s, short dark curly
hair, trimmed beard, wearing a button-up shirt, walks out of a formal
government building in a Brazilian city, defeated, he loosens his collar
and sits down on the concrete steps, holding a folder of documents, people
blurred passing by, overcast gray daylight. Shot on 35mm film, handheld
documentary style, shallow depth of field, natural lighting, visible skin
texture, subtle film grain, muted realistic colors, slight camera shake,
photorealistic, no text, no captions
```

### CENA 4 — REFRÃO 1: coração dividido (~1:00-1:30)
*"Sonho sem fronteira, coração dividido"*
```
Cinematic 8 second shot: aerial drone shot slowly rising over a lone
Brazilian man walking with a duffel bag along an empty dusty road at dusk,
vast landscape splitting the frame between warm orange sunset sky and cold
blue approaching night, he is a tiny determined figure in the immensity.
Shot on 35mm film, shallow depth of field, natural lighting, subtle film
grain, muted realistic colors, photorealistic, no text, no captions
```

### CENA 5 — Deserto: sol (~1:30-1:45)
*"Travessia no deserto, sol rachando a pele"*
```
Cinematic 8 second shot: a small group of exhausted travelers walking in
single file through a vast desert under harsh midday sun, heat waves
distorting the horizon, a Brazilian man in his early 30s, short dark curly
hair, trimmed beard, wearing a worn gray hoodie tied around his waist,
squints against the blinding light, cracked dry earth underfoot, extreme
wide shot then medium shot of his sunburned face. Shot on 35mm film,
handheld documentary style, shallow depth of field, natural lighting,
visible skin texture, subtle film grain, muted realistic colors, slight
camera shake, photorealistic, no text, no captions
```

### CENA 6 — Deserto: noite fria (~1:45-2:00)
*"Depois vem o frio da noite, quase congela"*
```
Cinematic 8 second shot: night in the desert, a Brazilian man in his early
30s, short dark curly hair, trimmed beard, wrapped in a thin blanket lying
on bare ground among sleeping travelers, breath visible in the cold air,
he stares up at an immense starry sky, moonlight, he shivers and pulls the
blanket tighter. Shot on 35mm film, handheld documentary style, shallow
depth of field, natural moonlight, visible skin texture, subtle film grain,
muted cold blue colors, slight camera shake, photorealistic, no text,
no captions
```

### CENA 7 — O rio / a fronteira (~2:00-2:15)
*"Rio que quase leva junto, fronteira que separa a vida"*
```
Cinematic 8 second shot: a Brazilian man in his early 30s, short dark curly
hair, trimmed beard, wades chest-deep through a wide muddy river at dawn,
holding a plastic bag with belongings above his head, strong current
pulling at him, his face straining with effort and fear, gray-blue cold
morning light, water splashing. Shot on 35mm film, handheld documentary
style, shallow depth of field, natural lighting, visible skin texture,
subtle film grain, muted realistic colors, slight camera shake,
photorealistic, no text, no captions
```

### CENA 8 — REFRÃO 2 (~2:15-2:45)
**REUSAR Cena 4 do promo EUA** (chegada no aeroporto/cidade — se já gerada)
ou gerar variação:
```
Cinematic 8 second shot: a Brazilian man in his early 30s, short dark curly
hair, trimmed beard, wearing a worn gray hoodie, stands still on a busy
American city sidewalk in winter, dwarfed by tall buildings, strangers
rushing past him in both directions in motion blur, he looks up slowly at
the skyline, snowflakes starting to fall on his face, mix of fear and awe.
Shot on 35mm film, handheld documentary style, shallow depth of field,
natural lighting, visible skin texture, subtle film grain, muted cold
colors, slight camera shake, photorealistic, no text, no captions
```

### CENA 9 — Videochamada com a mãe (~2:45-3:05)
*"Ligou pra mãe chorando, disse que tava tudo bem"*
**REUSAR Cena 3 do promo EUA** (já gerada ✅) — encaixa perfeitamente.

### CENA 10 — Trabalho no inverno (~3:05-3:20)
*"Trabalha de inverno com a mão rachando de frio"*
```
Cinematic 8 second shot: close-medium shot of a Brazilian man in his early
30s, short dark curly hair, trimmed beard, shoveling snow off a driveway
in a Massachusetts suburb before sunrise, orange streetlight glow, thick
jacket and wool cap, chapped red hands gripping the shovel, exhausted
breath clouds, he pauses and looks at the gray sky, then keeps going.
Shot on 35mm film, handheld documentary style, shallow depth of field,
natural lighting, visible skin texture, subtle film grain, muted realistic
colors, slight camera shake, photorealistic, no text, no captions
```

### CENA 11 — Trabalho no verão / construção (~3:20-3:35)
**REUSAR Cena 1 do promo EUA** (construção ao amanhecer — se já gerada)
ou gerar com o protagonista fixo no lugar do operário genérico.

### CENA 12 — Mandando dinheiro / o sacrifício (~3:35-3:55)
*"Manda dinheiro pra casa antes de pensar no próprio bem-estar"*
```
Cinematic 8 second shot: a Brazilian man in his early 30s, short dark curly
hair, trimmed beard, sits at a tiny kitchen table in a small American
apartment at night, counting worn dollar bills into two piles, he pushes
the bigger pile into an envelope with a handwritten address, keeps only a
few bills for himself, instant noodles cooking behind him, warm dim lamp
light, quiet dignity. Shot on 35mm film, handheld documentary style,
shallow depth of field, natural lighting, visible skin texture, subtle
film grain, muted realistic colors, slight camera shake, photorealistic,
no text, no captions
```

### CENA 13 — REFRÃO FINAL: a virada (~3:55-4:15)
*"Cansado, mas nunca derrotado"*
```
Cinematic 8 second shot: a Brazilian man in his early 30s, short dark curly
hair, trimmed beard, wearing work clothes, stands on a rooftop or high
scaffolding at golden hour overlooking an American city, he closes his
eyes, breathes deep, a small Brazilian flag patch visible on his backpack,
wind in his hair, the exhaustion in his face slowly turning into a proud
quiet smile, warm golden light. Shot on 35mm film, handheld documentary
style, shallow depth of field, natural lighting, visible skin texture,
subtle film grain, warm golden colors, slight camera shake, photorealistic,
no text, no captions
```

### CENA 14 — Encerramento: a esperança (~4:15-4:35)
*"Um dia essa saudade toda vai virar motivo de sorrir"*
```
Cinematic 8 second shot: a Brazilian man in his early 30s, short dark curly
hair, trimmed beard, laughing genuinely during a video call at night, phone
propped against a window, city lights bokeh behind, on the screen glow his
family celebrates, he wipes a happy tear, slow push-in, then he looks out
the window at the city with hope, fade-friendly composition. Shot on 35mm
film, handheld documentary style, shallow depth of field, natural lighting,
visible skin texture, subtle film grain, warm colors, slight camera shake,
photorealistic, no text, no captions
```

---

## MONTAGEM (FFmpeg — Claude faz)

1. Salvar clipes como `Clipes-Veo\cena01.mp4` ... `cena14.mp4` (16:9, 8s)
2. Timestamps reais da letra: `faster-whisper` no MP3 (script `Ferramentas\lyric-video\transcrever.py`)
3. Cada cena: slow motion 0.5x (`setpts=2.0*PTS` + `minterpolate` p/ suavizar) → ~16s
4. Concat com crossfade 0.5s entre cenas, cortes casando com as viradas do beat
5. Color grade filme: `curves` (leve S-curve) + `noise=alls=6:allf=t` (grain) + vinheta suave
6. Áudio: MP3 da música com `loudnorm=I=-14:TP=-1`
7. Saídas: 16:9 1080p (YouTube) + Short 9:16 do refrão final (cena 13, ~45s antes do fim)

## CUSTO/GERAÇÃO

- 11 cenas novas a gerar (3 reusadas do promo EUA) no Veo via Gemini
- Gerar 2 variações por cena quando possível e escolher a melhor
- Conferir consistência do protagonista entre cenas ANTES de baixar tudo

## STATUS (atualizado 14/jul/2026 — geradas via Claude + Gemini/Veo)

| Cena | Arquivo | Obs |
|---|---|---|
| 1 | ✅ cena01.mp4 | quarto vazio + foto da família — perfeita |
| 2 | ✅ cena02.mp4 | abraço da mãe (regenerada sem borda de filme) |
| 3 | ✅ cena03.mp4 | consulado, escada — perfeita |
| 4 | ✅ cena04.mp4 | drone estrada ao entardecer — linda |
| 5 | ✅ cena05.mp4 | deserto SOL (versão SOLO — grupo foi bloqueado pelo filtro) |
| 6 | ✅ cena06.mp4 | deserto noite/Via Láctea — CORTAR primeiros ~2s (borda de filme) |
| 7 | ✅ cena07.mp4 | rio — dramática |
| 8 | ✅ cena08.mp4 | cidade inverno, gerada nova |
| 9 | reuso | Cena 3 do promo EUA (videochamada) OU usar trecho da cena14 |
| 10 | ✅ cena10.mp4 | pá de neve Massachusetts |
| 11 | reuso | Cena 1 do promo EUA (construção) |
| 12 | ✅ cena12.mp4 | contando dólares na cozinha |
| 13 | ✅ cena13.mp4 | telhado golden hour + BANDEIRA DO BRASIL na mochila — a melhor |
| 14 | ✅ cena14.mp4 | videochamada final com família na tela — emocionante |

## LIÇÕES APRENDIDAS (para próximos clipes)

- **NÃO usar "Shot on 35mm film"** — o Veo desenha borda de rolo de filme literal.
  Usar: "Cinematic 8 second shot, full frame with no borders" + "no frame overlay".
- **Grupo de viajantes no deserto = bloqueado** (erros 1155/1097, remete a travessia
  ilegal). Versão com protagonista SOZINHO passa numa boa.
- Protagonista idêntico em todas as cenas: repetir descrição física palavra por palavra.
- Gemini web: depois de resposta terminar, 1º clique no botão de enviar às vezes só
  foca — conferir e clicar de novo. Se UI travar ("Something went wrong"), recarregar
  a página resolve (o prompt precisa ser redigitado).
- Verificar cada download por hash MD5 (botões de download de vídeos antigos confundem).
