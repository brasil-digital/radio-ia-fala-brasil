# ============================================================
#  Gerador de Spots/Vinhetas — Rádio Fala Brasil
#  Voz: "Voz do Ronny" (ElevenLabs)
#  Gera áudio fixo (sem clima/data) a partir de qualquer texto.
#
#  Uso:
#    .\gerar-spot.ps1 -Texto "..." -Arquivo "Spot-Nome.mp3"
#
#  Saída em: Radio-IA-Fala-Brasil\Vinhetas\
#  Lembrete: manter spots < 20s (crossfade da BR Logic corta vinhetas longas)
# ============================================================

param(
  [Parameter(Mandatory)][string]$Texto,
  [Parameter(Mandatory)][string]$Arquivo
)

$ErrorActionPreference = 'Stop'
$PastaSaida = 'C:\Users\Owner\Radio-IA-Fala-Brasil\Vinhetas'
$VoiceId    = 'EY32nkT8HLbeyhhUFVlv'   # Voz do Ronny
$ModeloTts  = 'eleven_multilingual_v2'

$apiKey = $env:ELEVENLABS_API_KEY
if (-not $apiKey) { throw 'Variável ELEVENLABS_API_KEY não definida.' }
if ($Arquivo -notmatch '\.mp3$') { $Arquivo += '.mp3' }

$tmp   = Join-Path $PastaSaida 'spot-tmp.mp3'
$saida = Join-Path $PastaSaida $Arquivo

$body = @{
  text     = $Texto
  model_id = $ModeloTts
  voice_settings = @{ stability = 0.5; similarity_boost = 0.8; style = 0.35 }
} | ConvertTo-Json -Depth 4

Write-Host "Gerando spot com a Voz do Ronny..." -ForegroundColor Cyan
Invoke-WebRequest -Method POST `
  -Uri "https://api.elevenlabs.io/v1/text-to-speech/$VoiceId`?output_format=mp3_44100_128" `
  -Headers @{ 'xi-api-key' = $apiKey } `
  -ContentType 'application/json; charset=utf-8' `
  -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) `
  -OutFile $tmp | Out-Null

ffmpeg -y -hide_banner -loglevel error -i $tmp -af 'loudnorm=I=-14:TP=-1:LRA=11' -c:a libmp3lame -b:a 192k $saida
Remove-Item $tmp -Force -ErrorAction SilentlyContinue

$dur = [math]::Round([double](ffprobe -v error -show_entries format=duration -of csv=p=0 $saida), 1)
$alerta = if ($dur -gt 20) { ' ⚠️ ACIMA DE 20s — pode ser cortado pelo crossfade da BR Logic!' } else { '' }
Write-Host "✅ Spot pronto: $saida ($dur segundos)$alerta" -ForegroundColor Green
