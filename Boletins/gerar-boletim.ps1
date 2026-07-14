# ============================================================
#  Gerador de Boletins — Rádio Fala Brasil (Boston/MA)
#  Voz: "Voz do Ronny" (ElevenLabs, clone da voz do Ronny)
#  Clima: Open-Meteo (gratuito, sem chave)
#
#  Uso:
#    .\gerar-boletim.ps1                  # período automático (hora de Boston)
#    .\gerar-boletim.ps1 -Periodo manha   # manha | tarde | noite
#    .\gerar-boletim.ps1 -SomenteTexto    # só mostra o roteiro, sem gerar áudio
#
#  Requisitos:
#    - Variável de ambiente ELEVENLABS_API_KEY
#    - ffmpeg no PATH
#    - Opcional: trilha-fundo.mp3 nesta pasta (fundo musical)
#    - Opcional: eventos.txt nesta pasta (1 evento por linha)
# ============================================================

param(
  [ValidateSet('manha', 'tarde', 'noite')]
  [string]$Periodo,
  [switch]$SomenteTexto
)

$ErrorActionPreference = 'Stop'
$PastaBase   = $PSScriptRoot
$PastaSaida  = Join-Path $PastaBase 'Saida'
$TrilhaFundo = Join-Path $PastaBase 'trilha-fundo.mp3'
$ArqEventos  = Join-Path $PastaBase 'eventos.txt'

$VoiceId  = 'EY32nkT8HLbeyhhUFVlv'   # Voz do Ronny
$ModeloTts = 'eleven_multilingual_v2'

New-Item -ItemType Directory -Force -Path $PastaSaida | Out-Null

# ---------- Hora de Boston e período ----------
$tzBoston   = [TimeZoneInfo]::FindSystemTimeZoneById('Eastern Standard Time')
$agoraBoston = [TimeZoneInfo]::ConvertTime((Get-Date), $tzBoston)

if (-not $Periodo) {
  $Periodo = if ($agoraBoston.Hour -lt 12) { 'manha' } elseif ($agoraBoston.Hour -lt 18) { 'tarde' } else { 'noite' }
}

$ptBR = [cultureinfo]'pt-BR'
$dataFalada = $agoraBoston.ToString("dddd, d 'de' MMMM", $ptBR)

# ---------- Clima de Boston (Open-Meteo) ----------
$urlClima = 'https://api.open-meteo.com/v1/forecast?latitude=42.3601&longitude=-71.0589' +
  '&current=temperature_2m,apparent_temperature,weather_code' +
  '&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max' +
  '&temperature_unit=fahrenheit&timezone=America%2FNew_York&forecast_days=1'

$clima = Invoke-RestMethod -Uri $urlClima -TimeoutSec 20

function FahrToCelsius([double]$f) { [math]::Round(($f - 32) * 5 / 9) }

$tempF    = [math]::Round($clima.current.temperature_2m)
$tempC    = FahrToCelsius $clima.current.temperature_2m
$maxF     = [math]::Round($clima.daily.temperature_2m_max[0])
$maxC     = FahrToCelsius $clima.daily.temperature_2m_max[0]
$minF     = [math]::Round($clima.daily.temperature_2m_min[0])
$minC     = FahrToCelsius $clima.daily.temperature_2m_min[0]
$chuvaPct = [int]$clima.daily.precipitation_probability_max[0]
$codigo   = [int]$clima.current.weather_code

$condicoes = @{
  0 = 'céu limpo'; 1 = 'poucas nuvens'; 2 = 'parcialmente nublado'; 3 = 'tempo nublado'
  45 = 'neblina'; 48 = 'neblina'; 51 = 'garoa'; 53 = 'garoa'; 55 = 'garoa'
  61 = 'chuva fraca'; 63 = 'chuva'; 65 = 'chuva forte'; 66 = 'chuva congelante'; 67 = 'chuva congelante'
  71 = 'neve fraca'; 73 = 'neve'; 75 = 'neve forte'; 77 = 'neve'
  80 = 'pancadas de chuva'; 81 = 'pancadas de chuva'; 82 = 'pancadas fortes de chuva'
  85 = 'pancadas de neve'; 86 = 'pancadas de neve'; 95 = 'tempestade'; 96 = 'tempestade com granizo'; 99 = 'tempestade com granizo'
}
$condicao = if ($condicoes.ContainsKey($codigo)) { $condicoes[$codigo] } else { 'tempo instável' }

# ---------- Dica baseada no clima ----------
$dica = if ($codigo -ge 71 -and $codigo -le 86) {
  'Vai nevar, então dirija com calma e cuidado nas estradas!'
} elseif (($codigo -ge 61 -and $codigo -le 67) -or ($codigo -ge 80 -and $codigo -le 99) -or $chuvaPct -ge 60) {
  'Não esquece o guarda-chuva, hein?'
} elseif ($tempF -le 40) {
  'Tá frio, então casaco reforçado antes de sair de casa!'
} elseif ($tempF -ge 85) {
  'Calor forte hoje: bebe bastante água e procura uma sombra!'
} else {
  'Aproveita o dia!'
}

# ---------- Eventos (opcional, manual) ----------
$eventosTxt = ''
if (Test-Path $ArqEventos) {
  $eventos = Get-Content $ArqEventos -Encoding UTF8 | Where-Object { $_.Trim() } | Select-Object -First 2
  if ($eventos) {
    $eventosTxt = 'Agenda da comunidade: ' + ($eventos -join ' E mais: ') + '.'
  }
}

# ---------- Montagem do roteiro (frases variadas) ----------
$saudacoes = @{
  manha = @(
    'Bom dia, Boston! Aqui é o Ronny, na Rádio Fala Brasil!',
    'Bom dia, Boston! Ronny na área pra começar o seu dia com você!',
    'Acorda, Boston! Aqui é o Ronny, e a Rádio Fala Brasil já tá no ar!'
  )
  tarde = @(
    'Boa tarde, Boston! Aqui é o Ronny, na Rádio Fala Brasil!',
    'Boa tarde, Boston! Ronny com você no meio do seu dia!',
    'Boa tarde, comunidade! Aqui é o Ronny, na rádio dos brasileiros na América!'
  )
  noite = @(
    'Boa noite, Boston! Aqui é o Ronny, na Rádio Fala Brasil!',
    'Boa noite, Boston! Ronny com você pra fechar o dia em grande estilo!',
    'Boa noite, comunidade brasileira! Aqui é o Ronny, na Rádio Fala Brasil!'
  )
}

$despedidas = @(
  'Agora, mais música na Rádio Fala Brasil: a sua voz nos Estados Unidos! Um abraço do Ronny!',
  'Fica com a gente, que vem muita música boa por aí. Rádio Fala Brasil: a sua voz nos Estados Unidos!',
  'Esse foi o seu boletim. Rádio Fala Brasil: a sua voz nos Estados Unidos! Valeu, Boston!'
)

$climaFrase = switch ($Periodo) {
  'manha' { "Hoje é $dataFalada. Agora faz $tempF graus Fahrenheit, uns $tempC Celsius, com $condicao. A máxima de hoje chega a $maxF Fahrenheit, $maxC Celsius, e a mínima cai pra $minF, que dá $minC Celsius. $dica" }
  'tarde' { "Nesta $dataFalada, estamos com $tempF graus Fahrenheit neste momento, uns $tempC Celsius, e $condicao. Mais tarde a mínima vai a $minF Fahrenheit, $minC Celsius. $dica" }
  'noite' { "Agora à noite faz $tempF graus Fahrenheit, uns $tempC Celsius, com $condicao. Durante a madrugada a mínima chega a $minF Fahrenheit, $minC Celsius. $dica" }
}

$saudacao  = $saudacoes[$Periodo] | Get-Random
$despedida = $despedidas | Get-Random

$roteiro = (@($saudacao, $climaFrase, $eventosTxt, $despedida) | Where-Object { $_ }) -join ' '

Write-Host "`n===== ROTEIRO ($Periodo — $($agoraBoston.ToString('dd/MM/yyyy HH:mm')) hora de Boston) =====" -ForegroundColor Green
Write-Host $roteiro
Write-Host "=====`n" -ForegroundColor Green

if ($SomenteTexto) { exit 0 }

# ---------- Narração (ElevenLabs) ----------
$apiKey = $env:ELEVENLABS_API_KEY
if (-not $apiKey) { throw 'Variável de ambiente ELEVENLABS_API_KEY não definida. Rode: setx ELEVENLABS_API_KEY "sk_..." e abra um novo terminal.' }

$stamp    = $agoraBoston.ToString('yyyy-MM-dd')
$narracao = Join-Path $PastaSaida "narracao-tmp.mp3"
$saida    = Join-Path $PastaSaida "Boletim-$Periodo-$stamp.mp3"

$body = @{
  text     = $roteiro
  model_id = $ModeloTts
  voice_settings = @{ stability = 0.5; similarity_boost = 0.8; style = 0.25 }
} | ConvertTo-Json -Depth 4

Write-Host 'Gerando narração com a Voz do Ronny...' -ForegroundColor Cyan
Invoke-WebRequest -Method POST `
  -Uri "https://api.elevenlabs.io/v1/text-to-speech/$VoiceId`?output_format=mp3_44100_128" `
  -Headers @{ 'xi-api-key' = $apiKey } `
  -ContentType 'application/json; charset=utf-8' `
  -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) `
  -OutFile $narracao | Out-Null

# ---------- Mixagem e normalização (padrão da rádio: -14 LUFS) ----------
if (Test-Path $TrilhaFundo) {
  Write-Host 'Mixando com trilha de fundo...' -ForegroundColor Cyan
  ffmpeg -y -hide_banner -loglevel error -i $narracao -stream_loop -1 -i $TrilhaFundo `
    -filter_complex '[1:a]volume=0.30[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=3,loudnorm=I=-14:TP=-1:LRA=11' `
    -c:a libmp3lame -b:a 192k $saida
} else {
  Write-Host 'Sem trilha-fundo.mp3 — gerando só com a narração.' -ForegroundColor Yellow
  ffmpeg -y -hide_banner -loglevel error -i $narracao -af 'loudnorm=I=-14:TP=-1:LRA=11' -c:a libmp3lame -b:a 192k $saida
}

Remove-Item $narracao -Force -ErrorAction SilentlyContinue
$dur = [math]::Round([double](ffprobe -v error -show_entries format=duration -of csv=p=0 $saida))
Write-Host "`n✅ Boletim pronto: $saida ($dur segundos)" -ForegroundColor Green
Write-Host '   Agora é só subir no painel da BR Logic: https://app.brlogic.com/r/f1f2681da7/radio/'
