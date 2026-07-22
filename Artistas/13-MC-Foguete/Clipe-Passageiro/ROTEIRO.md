# Passageiro do Mundo — Clipe Realístico com RONNY de protagonista 🌍✈️

**Música:** Passageiro do Mundo (MC Foguete) — 3:57 (MP3 íntegro, Downloads).
**Conceito:** Ronny viaja o mundo — cada país da letra vira uma cena com ele.
**Pedidos do Ronny (16/jul):** incluir cenas com ele na CHINA, DUBAI e MARROCOS.
**Foto-ref:** `..\Clipe-Green-Card\Fotos-Ref\ronny-aeroporto-malas.jpg` (escolhida por ele).
**Chat Gemini:** https://gemini.google.com/app/842974e6fd07bbc3 (MESMO chat = rosto consistente)

## MÉTODO NOVO p/ animar (confirmado 20/jul, usado p/ cenas 06 e 07 — o chat antigo
842974e6fd07bbc3 ficou permanentemente quebrado: "image generation offline in this
session", nem trocar p/ modelo Pro resolve)
1. Imagem de referência: usar a já gerada no chat antigo (Imagens-Cena\cenaNN-*.png)
   ou baixar do chat antigo se só existir lá (clicar imagem → editor → ⬇ topo 1424,20)
2. Copiar PNG p/ clipboard: PowerShell -STA `[System.Drawing.Image]::FromFile(...)` +
   `[System.Windows.Forms.Clipboard]::SetImage($img)`
3. Ir em gemini.google.com/app (chat NOVO, em branco — NÃO usar o chat antigo quebrado)
4. Clicar no campo "Ask Gemini", Ctrl+V (anexa a imagem — confirmar thumbnail apareceu),
   digitar prompt "Animate this exact image into an 8 second video: ..." e clicar no
   botão enviar (Enter sozinho às vezes só quebra linha, não envia)
5. Se recusar ("I can't generate that video" / "I can't make that type of video"):
   a) tentar "Please try again." no mesmo chat (às vezes preciso reenviar a imagem
      de novo junto, o chat "esquece" a imagem entre mensagens)
   b) ou simplificar o prompt (tirar "crowd"/multidão, "camera orbit" — parecem
      disparar recusa; usar "gentle slow camera push-in" no lugar)
   c) **PREVENTIVO (aprendido na cena 08/Índia)**: em cenas com multidão/mercado, já
      pedir na IMAGEM que vendedores/pedestres de fundo fiquem de costas, desfocados
      ou não reconhecíveis ("no other people's faces visible — turned away from
      camera, heavily blurred, or silhouetted") — rostos de terceiros reconhecíveis
      no fundo parecem disparar bloqueio de política ao tentar animar depois. Vale
      pra Nova York, China e Rio (cenas com multidão pela frente).
6. Download: menu "..." abaixo do vídeo → "Download video" (NÃO usar o ícone de
   compartilhar/share, esse cria link público) → cai em Downloads com nome do prompt
7. **SEMPRE conferir o conteúdo do vídeo baixado antes de copiar p/ Clipes-Veo**
   (`ffmpeg -y -i arquivo.mp4 -update 1 -vframes 1 out.jpg`) — Gemini já entregou
   vídeo de conteúdo completamente errado (estoque sem relação) nesse projeto.
   **Conferir MAIS de um frame (início, meio, fim)** — bug visto na cena 11 (Rio):
   vídeo "colava" os primeiros ~2s da cena ANTERIOR do mesmo chat antes de virar a
   cena certa; um único frame no início não pega isso. Se acontecer: baixar a
   imagem limpa (Library → clicar na imagem → ícone download) e reanimar do zero
   em chat NOVO (não insistir no mesmo chat/mensagem).

## Pipeline por cena (igual Green Card)
1. Imagem: "Scene N, same man (exact same face): photorealistic image in WIDE 16:9
   LANDSCAPE format — ..." (SEMPRE pedir 16:9 landscape, senão sai retrato)
2. Baixar imagem: clicar na imagem → abre editor → ícone download topo (1424,20) → Escape
3. Animar: "Now animate this exact image into an 8 second video: ..."
4. Veo demora 2-6 min; baixar vídeo: hover no player → ícone download (995,246)
5. Salvar: Imagens-Cena\cenaNN-*.png e Clipes-Veo\cenaNN.mp4 (Veo sai 1280x720 10s)

## SHOT LIST / STATUS (atualizado 20/jul — ver nota abaixo)

**NOTA 20/jul:** os arquivos `cena06.mp4` e `cena07.mp4` da pasta Clipes-Veo estavam
CORROMPIDOS/TROCADOS (vídeos de estoque sem relação — ginasta e ceramista), apesar do
status abaixo dizer "done". Movidos para `Clipes-Veo\_arquivos-errados-backup\`.
Cena 06 (Dubai) foi regerada e verificada nesta data (frame conferido = Ronny + Burj
Khalifa, correto). Cena 07 (Tóquio) segue realmente pendente — nunca foi gerada
(chat antigo trava em "image generation offline"; usar MÉTODO NOVO abaixo, chat
separado + colar imagem de referência via clipboard). SEMPRE conferir um frame de
cada vídeo baixado (`ffmpeg -y -i arquivo.mp4 -update 1 -vframes 1 out.jpg`) antes
de dar como concluído — Gemini já entregou vídeo de conteúdo errado nesse projeto.
| # | Cena | Letra (~ts) | Status |
|---|---|---|---|
| 01 | Aeroporto embarque, passaporte BR | intro/decolagem 0:02 | ✅ img+vídeo |
| 02 | Janela do avião, mar de nuvens douradas | "do asfalto até nuvem" 0:20 | ✅ img+vídeo |
| 03 | Paris — Trocadéro, Torre Eiffel, braços abertos | "Paris me chamando" 0:31 | ✅ img+vídeo |
| 04 | Roma — Coliseu, andando maravilhado | "Roma me contando história" 0:33 | ✅ img+vídeo |
| 05 | MARROCOS — souk de especiarias e lanternas | "Marrocos pintando o céu" 0:36 | ✅ img+vídeo |
| 06 | DUBAI — mirante com Burj Khalifa blue hour | refrão/"deserto" 0:39 | ✅ img+vídeo (regerado e CONFERIDO 20/jul) |
| 07 | Tóquio — Shibuya neon à noite | "Tóquio de neon" 1:23 | ✅ img+vídeo (regerado e CONFERIDO 20/jul, via MÉTODO NOVO) |
| 08 | Índia — mercado colorido/especiarias | "Índia colorida" 1:29 | ✅ img+vídeo (CONFERIDO 20/jul). 1ª imagem/vídeo travaram em bug (download sempre trazia Dubai) + depois recusa de política (rostos de vendedores no fundo). Resolvido regerando a imagem pedindo vendedores de costas/desfocados/não reconhecíveis — animou de primeira. Imagens-Cena\cena08-india-v2-semrostos.jpg (frame extraído do vídeo final, usar como referência de rosto para próximas cenas); v1 com rostos ficou em cena08-india-v1-comrostos.png (não usar como referência p/ animar, arriscou bloqueio). |
| 09 | Nova York — Times Square | "Nova York correndo" 1:34 | ✅ img+vídeo (CONFERIDO 20/jul) — imagem já saiu de primeira sem rostos de fundo reconhecíveis (pedindo isso desde o prompt inicial da imagem) e a animação passou sem recusa nenhuma. Confirma a lição da cena 08: pedir pedestres de costas/desfocados na imagem evita bloqueio de política ao animar. |
| 10 | CHINA — Muralha da China | "China antiga guardando muralha" 2:40 | ✅ img+vídeo (CONFERIDO 20/jul) — saiu de primeira, sem recusa, seguindo o mesmo método (turistas de fundo pequenos/distantes pedidos desde a imagem). |
| 11 | Rio de Janeiro — calçadão/Pão de Açúcar sorrindo | "Rio sorrindo, batucando" 2:45 | ✅ img+vídeo (CONFERIDO 20/jul, frames em 0s/4s/9s todos corretos) — precisou de 3 tentativas: 1ª e 2ª saíram com bug novo (vídeo começa com a cena ANTERIOR do chat — Muralha da China — e só depois de ~2s vira a cena certa, um "glue" de dois renders); 3ª tentativa em chat novo do zero (baixando a imagem limpa da Library antes) saiu perfeita. |
| 12 | Final — mirante pôr do sol, passaporte na mão, olha p/ câmera | "próximo destino te chamando" 3:46 | ✅ img+vídeo (CONFERIDO 20/jul, frames em 0s/4s/9s todos corretos) — saiu de primeira. |

Paisagens sem Ronny (texto→vídeo direto, se sobrar cota): estrada drone golden hour
p/ refrões; savana África ("África com ritmo" 1:37).

## STATUS: MONTAGEM COMPLETA ✅ (20/jul/2026)
Todas as 12 cenas prontas + clipe montado e finalizado. 4 arquivos em Downloads:
- `MC Foguete - Passageiro do Mundo - CLIPE OFICIAL.mp4` (1920x1080, 237.7s, com legenda estilo karaokê)
- `MC Foguete - Passageiro do Mundo - SHORT.mp4` (1080x1920, 45s, refrão final + fechamento)
- `MC Foguete - Passageiro do Mundo - STORY.mp4` (1080x1920, 30s, refrão final)
- `MC Foguete - Thumbnail - Passageiro do Mundo.jpg` (1280x720, padrão do canal)

## Como foi feita a montagem (método, p/ reusar em próximas músicas)
Scripts em `Ferramentas\lyric-video\` (sufixo `_passageiro`):
1. **plan_passageiro.py** — calcula a linha do tempo: cada cena começa no timestamp
   do ROTEIRO (shot list) e dura até o timestamp da próxima cena (ou fim da música).
   Cada clipe Veo tem só 10s — se a cena precisa durar menos, corta (`TRIM`); se
   precisa durar mais, ou estica com zoom Ken Burns no último frame (gaps curtos,
   <3s) ou preenche com um "medley" de recortes de 4.5s de OUTRAS cenas já prontas,
   ciclando pela lista sem repetir a mesma logo em seguida (gaps grandes — imita o
   recurso de clipe de repetir imagens do refrão, evita ficar 60s parado numa cena só).
2. **render_chunks_passageiro.py** — renderiza cada pedaço da linha do tempo em um
   arquivo .mp4 separado (mesmo codec/resolução/fps em todos, pra concatenar com
   `-c copy` sem re-encode) + zoompan pros trechos de "hold".
3. Concat via `ffmpeg -f concat` + mux com o MP3 completo (`-shortest`).
4. **make_ass_passageiro.py** — gera legenda .ass estilo karaokê (`\k` por palavra,
   cores branco/amarelo) a partir do letra_passageiro.json, já aplicando o fix de
   transcrição conhecido ("Pé-pé-pé-pé-pé-sia..." → "Pérsia me ensinando mito e
   filosofia"). Queimar com `-vf subtitles=arquivo.ass`.
5. Upscale pra 1920x1080 no render final.
6. **Para SHORT/STORY (vertical)**: usar `make_ass_clip.py START DUR saida.ass` pra
   gerar uma legenda com PlayResX=1080 (não 1280) e timestamps DESLOCADOS pro
   começo do recorte (senão a legenda mostra a letra errada E fica cortada nas
   bordas ao recortar pra 9:16 — dois bugs reais encontrados nesta sessão).
   Crop vertical: `scale=-2:1920,crop=1080:1920:(iw-1080)/2:0` ANTES de aplicar
   as legendas (nunca depois, senão o texto pensado pro frame largo é cortado).
7. **Thumbnail**: `Ferramentas\lyric-video\thumb-passageiro.html` (cópia do padrão
   thumb-sonho.html com título trocado) renderizado via Chrome headless
   (`chrome.exe --headless=new --screenshot=... --window-size=2400,1350`, com
   PATH ABSOLUTO Windows — path estilo `/c/...` deu "Access denied"), depois
   `ffmpeg -vf scale=1280:720`.
