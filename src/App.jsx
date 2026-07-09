import { useState, useRef, useEffect } from 'react'
import { MediaSession } from '@jofr/capacitor-media-session'
import { artists } from './data/artists'

// ⚠️ Substitua pela URL real do seu stream BR Logic
const STREAM_URL = 'https://servidor29-1.brlogic.com:7018/live'

const setMediaSessionState = (playbackState) => {
  MediaSession.setPlaybackState({ playbackState }).catch(() => {})
}

// Equalizador: 28 barras no degradê da bandeira (verde → amarelo → azul)
const EQ_STOPS = [
  [0, 224, 96],   // verde
  [255, 223, 0],  // amarelo
  [59, 130, 246], // azul
]
const eqColor = (t) => {
  const seg = t < 0.5 ? 0 : 1
  const f = (t - seg * 0.5) / 0.5
  const [a, b] = [EQ_STOPS[seg], EQ_STOPS[seg + 1]]
  const mix = a.map((c, i) => Math.round(c + (b[i] - c) * f))
  return { color: `rgb(${mix.join(',')})`, dark: `rgb(${mix.map((c) => Math.round(c * 0.35)).join(',')})` }
}
const EQ_BARS = Array.from({ length: 28 }, (_, i) => {
  const t = i / 27
  return {
    ...eqColor(t),
    height: Math.round(16 + 36 * Math.abs(Math.sin(i * 1.7 + 0.6))),
    delay: +((i * 0.077) % 0.9).toFixed(2),
    duration: +(0.85 + ((i * 37) % 55) / 100).toFixed(2),
  }
})

export default function App() {
  const [playing, setPlaying] = useState(false)
  const [volume, setVolume] = useState(0.8)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(false)
  const audioRef = useRef(null)
  const playingRef = useRef(false)

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = volume
    }
  }, [volume])

  const startPlay = () => {
    const audio = audioRef.current
    if (!audio || playingRef.current) return
    setLoading(true)
    setError(false)
    audio.src = STREAM_URL
    audio.load()
    audio.play()
      .then(() => {
        playingRef.current = true
        setPlaying(true)
        setLoading(false)
        MediaSession.setMetadata({
          title: 'Rádio Fala Brasil — Ao Vivo',
          artist: 'Música Brasileira 24 horas por dia',
          album: 'radiofalabrasil.com',
          artwork: [{ src: '/logo.jpg', sizes: '512x512', type: 'image/jpeg' }],
        }).catch(() => {})
        setMediaSessionState('playing')
      })
      .catch(() => {
        setError(true)
        setLoading(false)
        playingRef.current = false
        setPlaying(false)
        setMediaSessionState('none')
      })
  }

  const stopPlay = () => {
    const audio = audioRef.current
    if (!audio) return
    audio.pause()
    audio.src = ''
    playingRef.current = false
    setPlaying(false)
    setError(false)
    setMediaSessionState('paused')
  }

  const togglePlay = () => {
    if (playingRef.current) stopPlay()
    else startPlay()
  }

  useEffect(() => {
    // Controles da tela de bloqueio / notificação de mídia (Android + web)
    MediaSession.setActionHandler({ action: 'play' }, () => startPlay()).catch(() => {})
    MediaSession.setActionHandler({ action: 'pause' }, () => stopPlay()).catch(() => {})
    MediaSession.setActionHandler({ action: 'stop' }, () => stopPlay()).catch(() => {})
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const handleVolumeChange = (e) => {
    const val = parseFloat(e.target.value)
    setVolume(val)
    if (audioRef.current) audioRef.current.volume = val
  }

  return (
    <div className="min-h-screen bg-radio-dark text-white">
      <audio ref={audioRef} preload="none" />

      {/* Faixa da bandeira */}
      <div className="brasil-stripe" />

      {/* Header */}
      <header className="border-b border-radio-border sticky top-0 z-50 bg-radio-dark/95 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img
              src="/logo.jpg"
              alt="Mascote Rádio IA Fala Brasil"
              className="w-10 h-10 rounded-full object-cover shadow-lg shadow-radio-green/40 border border-radio-green/50"
            />
            <div>
              <h1 className="font-display font-bold text-white text-lg leading-tight tracking-wide">
                RÁDIO <span className="brasil-text">FALA BRASIL</span>
              </h1>
              <p className="text-xs text-radio-green">A Primeira Rádio 100% IA do Brasil</p>
            </div>
          </div>
          <a
            href="https://www.youtube.com/@ritmos-do-brasil"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 bg-red-700 hover:bg-red-600 text-white text-sm font-semibold px-3 py-1.5 rounded-full transition-colors"
          >
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
            </svg>
            Ritmos do Brasil
          </a>
        </div>
      </header>

      {/* Hero Player */}
      <section className="bg-gradient-to-b from-radio-greenDeep/30 via-radio-dark to-radio-dark py-16 px-4">
        <div className="max-w-2xl mx-auto text-center">

          {/* On Air badge */}
          <div className="inline-flex items-center gap-2 bg-radio-card border border-radio-border rounded-full px-4 py-1.5 mb-8">
            <span className={`w-2.5 h-2.5 rounded-full ${playing ? 'bg-radio-greenBright onair-dot' : 'bg-gray-600'}`} />
            <span className={`text-sm font-semibold tracking-widest ${playing ? 'text-radio-greenBright' : 'text-gray-300'}`}>
              {playing ? 'AO VIVO' : 'OFF AIR'}
            </span>
          </div>

          {/* Mascote / Logo oficial */}
          <div className="mb-4">
            <h2 className="sr-only">Rádio IA Fala Brasil — A Voz Inteligente do Brasil</h2>
            <img
              src="/logo.jpg"
              alt="Rádio IA Fala Brasil — mascote arara com fones de ouvido"
              className="w-64 md:w-96 mx-auto rounded-3xl shadow-2xl shadow-radio-green/30"
            />
          </div>
          <p className="text-radio-yellow font-semibold text-lg mb-10 tracking-wide">
            🎵 Música Brasileira 24 horas por dia
          </p>

          {/* Equalizer */}
          <div className={`flex items-end justify-center gap-1.5 h-14 mb-8 ${!playing ? 'opacity-30' : ''}`}>
            {EQ_BARS.map((bar, i) => (
              <div
                key={i}
                className={`eq-bar ${!playing ? 'paused' : ''}`}
                style={{
                  height: `${bar.height}px`,
                  background: `linear-gradient(to top, ${bar.dark}, ${bar.color})`,
                  boxShadow: `0 0 10px ${bar.color}, 0 0 22px ${bar.color}55`,
                  animationDelay: `${bar.delay}s`,
                  animationDuration: `${bar.duration}s`,
                }}
              />
            ))}
          </div>

          {/* Player controls */}
          <div className="flex flex-col items-center gap-6">
            <button
              onClick={togglePlay}
              disabled={loading}
              className="play-btn-glow w-24 h-24 rounded-full bg-gradient-to-br from-radio-green to-radio-greenDeep hover:from-radio-greenBright hover:to-radio-green active:scale-95 transition-all flex items-center justify-center disabled:opacity-70"
            >
              {loading ? (
                <svg className="w-8 h-8 animate-spin text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
                </svg>
              ) : playing ? (
                <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
                </svg>
              ) : (
                <svg className="w-10 h-10 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7L8 5z"/>
                </svg>
              )}
            </button>

            {error && (
              <p className="text-red-400 text-sm">
                Erro ao conectar ao stream. Verifique a URL do BR Logic.
              </p>
            )}

            {/* Volume */}
            <div className="flex items-center gap-3 w-64">
              <svg className="w-5 h-5 text-gray-400 shrink-0" fill="currentColor" viewBox="0 0 24 24">
                <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/>
              </svg>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={volume}
                onChange={handleVolumeChange}
                className="w-full accent-radio-yellow cursor-pointer"
              />
              <svg className="w-5 h-5 text-gray-400 shrink-0" fill="currentColor" viewBox="0 0 24 24">
                <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
              </svg>
            </div>
          </div>

          <p className="mt-8 text-gray-300 text-base md:text-lg">
            Uma parceria oficial{' '}
            <a
              href="https://www.falabrasil.digital/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-radio-yellow font-bold hover:underline hover:brightness-110 transition"
            >
              Fala Brasil
            </a>
            {' '}— o aplicativo de mensagens 100% brasileiro
          </p>
        </div>
      </section>

      {/* Artists Section */}
      <section className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h3 className="font-display font-bold text-3xl md:text-4xl tracking-wide mb-2">
            <span className="text-white">NOSSOS </span><span className="brasil-text">ARTISTAS</span>
          </h3>
          <p className="text-gray-400">12 artistas virtuais criados com IA — todos estilos do Brasil</p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          {artists.map((artist) => (
            <ArtistCard key={artist.id} artist={artist} />
          ))}
        </div>
      </section>

      {/* YouTube Section */}
      <section className="bg-radio-card border-y border-radio-border py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="font-display font-bold text-3xl text-white tracking-wide mb-3">
            ASSISTA NO YOUTUBE
          </h3>
          <p className="text-gray-400 mb-8">
            Todos os clipes e lyric videos no canal <span className="text-radio-yellow font-semibold">Ritmos do Brasil</span>
          </p>
          <a
            href="https://www.youtube.com/@ritmos-do-brasil"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-3 bg-red-600 hover:bg-red-500 text-white font-bold px-8 py-4 rounded-full text-lg transition-colors"
          >
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
            </svg>
            Acessar Canal Ritmos do Brasil
          </a>
        </div>
      </section>

      {/* About */}
      <section className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h3 className="font-display font-bold text-3xl tracking-wide mb-6">
          <span className="text-white">SOBRE A </span><span className="brasil-text">RÁDIO</span>
        </h3>
        <p className="text-gray-300 text-lg leading-relaxed mb-4">
          A <strong className="text-white">Rádio Fala Brasil</strong> é a primeira rádio brasileira com elenco
          100% criado por Inteligência Artificial. São 12 artistas virtuais, cada um com identidade,
          biografia e estilo musical próprios — representando os mais variados ritmos do Brasil.
        </p>
        <p className="text-gray-400 leading-relaxed">
          Do sertanejo ao axé, do reggae ao R&B, do rock ao pagodão —
          <span className="text-radio-yellow font-semibold"> o Brasil inteiro em uma só rádio.</span>
        </p>

        <div className="grid grid-cols-3 gap-6 mt-12">
          <div className="bg-radio-card border border-radio-green/40 rounded-xl p-6">
            <div className="font-display text-4xl font-bold text-radio-greenBright mb-1">12</div>
            <div className="text-gray-400 text-sm">Artistas Virtuais</div>
          </div>
          <div className="bg-radio-card border border-radio-yellow/40 rounded-xl p-6">
            <div className="font-display text-4xl font-bold text-radio-yellow mb-1">600</div>
            <div className="text-gray-400 text-sm">Músicas em Produção</div>
          </div>
          <div className="bg-radio-card border border-blue-500/40 rounded-xl p-6">
            <div className="font-display text-4xl font-bold text-blue-400 mb-1">24h</div>
            <div className="text-gray-400 text-sm">No Ar</div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-radio-border py-8 px-4">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="font-display font-bold tracking-wider">
            <span className="text-gray-400">RÁDIO </span><span className="brasil-text">FALA BRASIL</span>
          </div>
          <div className="text-center">
            <p className="text-gray-600 text-sm">
              © 2026 Rádio Fala Brasil · Powered by{' '}
              <span className="text-radio-green">Ritmos do Brasil</span> ·{' '}
              Música 100% criada por IA
            </p>
            <p className="text-gray-500 text-sm mt-2">
              Dúvidas ou parcerias:{' '}
              <a
                href="mailto:suporte@falabrasil.digital"
                className="text-radio-yellow hover:text-radio-greenBright transition-colors font-semibold"
              >
                suporte@falabrasil.digital
              </a>
            </p>
          </div>
          <a
            href="https://www.youtube.com/@ritmos-do-brasil"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-500 hover:text-radio-yellow transition-colors"
          >
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
            </svg>
          </a>
        </div>
      </footer>

      {/* Faixa da bandeira */}
      <div className="brasil-stripe" />
    </div>
  )
}

function ArtistCard({ artist }) {
  return (
    <a
      href={artist.youtube}
      target="_blank"
      rel="noopener noreferrer"
      className="group bg-radio-card border border-radio-border rounded-xl p-4 text-center hover:border-radio-yellow hover:shadow-lg hover:shadow-radio-green/20 transition-all hover:-translate-y-1"
    >
      <div
        className="w-16 h-16 rounded-full mx-auto mb-3 flex items-center justify-center text-3xl border-2 border-radio-green/50 group-hover:border-radio-yellow transition-colors overflow-hidden"
        style={{ backgroundColor: artist.color + '33' }}
      >
        {artist.avatar ? (
          <img
            src={artist.avatar}
            alt={artist.name}
            className="w-full h-full object-cover rounded-full"
            onError={(e) => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'block' }}
          />
        ) : null}
        <span className={artist.avatar ? 'hidden' : ''}>{artist.emoji}</span>
      </div>
      <h4 className="font-semibold text-white text-sm leading-tight mb-1 group-hover:text-radio-yellow transition-colors">
        {artist.name}
      </h4>
      <p className="text-xs text-radio-green">{artist.style}</p>
      <p className="text-xs text-gray-500 mt-0.5">{artist.origin}</p>
    </a>
  )
}
