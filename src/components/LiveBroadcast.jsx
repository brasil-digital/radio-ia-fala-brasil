import { useState, useEffect } from 'react'

// Janelas fixas de "ao vivo", em horário do Leste dos EUA (America/New_York)
// — a Rádio Fala Brasil e o público (imigrantes brasileiros em Massachusetts)
// vivem nos EUA, não no Brasil.
const WINDOWS = {
  manha: { startHour: 12, endHour: 13, label: 'meio-dia' },
  noite: { startHour: 19, endHour: 20, label: '19h' },
}

// Pra testar os 3 estados sem esperar o relógio bater meio-dia/19h:
// http://localhost:5173/?debugTime=2026-08-26T13:30 (só funciona em dev).
// Sobrescreve completamente o horário/data "de agora" usados abaixo — não é
// uma conversão de fuso, é uma simulação direta do horário-parede no Leste
// dos EUA, então a data também precisa ser informada.
function getDebugOverride() {
  if (!import.meta.env.DEV) return null
  const params = new URLSearchParams(window.location.search)
  const raw = params.get('debugTime')
  if (!raw) return null
  const match = raw.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})$/)
  if (!match) return null
  const [, year, month, day, hour, minute] = match.map(Number)
  return { year, month, day, hour, minute }
}

// Horário/data "de agora" no Leste dos EUA, resolvido corretamente com
// horário de verão pelo próprio navegador (tabela IANA embutida no Intl) —
// nunca fazemos conta manual de offset UTC-4/UTC-5.
function getNowET() {
  const override = getDebugOverride()
  if (override) return override

  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/New_York',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).formatToParts(new Date())

  const get = (type) => parseInt(parts.find((p) => p.type === type)?.value, 10)
  return { year: get('year'), month: get('month'), day: get('day'), hour: get('hour'), minute: get('minute') }
}

function currentPeriod(nowET) {
  for (const [period, w] of Object.entries(WINDOWS)) {
    if (nowET.hour >= w.startHour && nowET.hour < w.endHour) return period
  }
  return null
}

function nextAirtimeLabel(nowET) {
  const minutesNow = nowET.hour * 60 + nowET.minute
  const upcoming = Object.values(WINDOWS)
    .map((w) => ({ ...w, startMinutes: w.startHour * 60 }))
    .sort((a, b) => a.startMinutes - b.startMinutes)
  const next = upcoming.find((w) => w.startMinutes > minutesNow)
  return next ? `hoje às ${next.label}` : `amanhã às ${upcoming[0].label}`
}

function isFromToday(generatedAtUtc, nowET) {
  if (!generatedAtUtc) return false
  const genDate = new Date(generatedAtUtc)
  if (Number.isNaN(genDate.getTime())) return false
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/New_York',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).formatToParts(genDate)
  const get = (type) => parseInt(parts.find((p) => p.type === type)?.value, 10)
  return get('year') === nowET.year && get('month') === nowET.month && get('day') === nowET.day
}

async function fetchMeta(period) {
  try {
    const res = await fetch(`/transmissao/${period}.json`, { cache: 'no-store' })
    if (!res.ok) return null
    return await res.json()
  } catch {
    return null
  }
}

export default function LiveBroadcast() {
  const [meta, setMeta] = useState({ manha: null, noite: null })
  const [nowET, setNowET] = useState(getNowET)

  useEffect(() => {
    let cancelled = false
    Promise.all([fetchMeta('manha'), fetchMeta('noite')]).then(([manha, noite]) => {
      if (!cancelled) setMeta({ manha, noite })
    })
    return () => { cancelled = true }
  }, [])

  useEffect(() => {
    const id = setInterval(() => setNowET(getNowET()), 30000)
    return () => clearInterval(id)
  }, [])

  if (!meta.manha && !meta.noite) return null

  const period = currentPeriod(nowET)
  const activeMeta = period ? meta[period] : null
  const isLive = Boolean(activeMeta && isFromToday(activeMeta.generated_at_utc, nowET))

  if (isLive) {
    return (
      <div className="mt-8 bg-radio-card border border-radio-red/50 rounded-2xl p-5 text-left max-w-xl mx-auto">
        <div className="relative rounded-xl overflow-hidden mb-4">
          <img
            src="/transmissao/ronny.jpg"
            alt="Ronny, âncora da Transmissão Ao Vivo, no estúdio da Rádio Fala Brasil"
            className="w-full h-auto block"
          />
          <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/85 to-transparent px-3 pt-6 pb-2 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-radio-red animate-pulse2" />
            <span className="text-xs font-bold tracking-widest text-white">AO VIVO AGORA</span>
          </div>
        </div>
        <div className="inline-flex items-center gap-2 mb-3">
          <span className="w-2.5 h-2.5 rounded-full bg-radio-red animate-pulse2" />
          <span className="text-sm font-bold tracking-widest text-radio-red">TRANSMISSÃO AO VIVO</span>
        </div>
        <h4 className="font-display font-bold text-white text-lg leading-tight mb-1">{activeMeta.headline}</h4>
        <p className="text-gray-400 text-sm mb-4">{activeMeta.summary}</p>
        <audio controls className="w-full" src={`/transmissao/${period}.mp3`} />
        <p className="text-gray-500 text-xs mt-2">
          Fonte: {activeMeta.source_name}
          {activeMeta.source_url && (
            <>
              {' — '}
              <a href={activeMeta.source_url} target="_blank" rel="noopener noreferrer" className="hover:text-radio-yellow underline">
                matéria original
              </a>
            </>
          )}
        </p>
      </div>
    )
  }

  // Última edição disponível (a mais recente entre manhã/noite), pra mostrar
  // como "última edição" fora do ar — nunca com o badge de ao vivo.
  const last = [meta.manha, meta.noite]
    .filter(Boolean)
    .sort((a, b) => new Date(b.generated_at_utc) - new Date(a.generated_at_utc))[0]

  return (
    <div className="mt-8 bg-radio-card border border-radio-border rounded-2xl p-5 text-left max-w-xl mx-auto">
      <div className="relative rounded-xl overflow-hidden mb-4">
        <img
          src="/transmissao/ronny.jpg"
          alt="Ronny, âncora da Transmissão Ao Vivo, no estúdio da Rádio Fala Brasil"
          className="w-full h-auto block grayscale opacity-70"
        />
        <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/85 to-transparent px-3 pt-6 pb-2 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-gray-400" />
          <span className="text-xs font-bold tracking-widest text-gray-200">FORA DO AR</span>
        </div>
      </div>
      <div className="inline-flex items-center gap-2 mb-3">
        <span className="w-2.5 h-2.5 rounded-full bg-gray-600" />
        <span className="text-sm font-semibold tracking-widest text-gray-400">TRANSMISSÃO AO VIVO — FORA DO AR</span>
      </div>
      <p className="text-gray-300 text-sm mb-3">Próxima transmissão {nextAirtimeLabel(nowET)} (horário do Leste dos EUA).</p>
      {last && (
        <>
          <p className="text-gray-500 text-xs uppercase tracking-wide mb-1">Última edição</p>
          <h4 className="font-display font-bold text-white text-base leading-tight mb-1">{last.headline}</h4>
          {last.duration_seconds > 0 && (
            <audio controls className="w-full" src={`/transmissao/${last.period}.mp3`} />
          )}
        </>
      )}
    </div>
  )
}
