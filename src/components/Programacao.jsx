import { useState, useEffect } from 'react'

// Grade do painel BR Logic, que roda no horário de Brasília (UTC-3 fixo,
// sem horário de verão). Mostramos no fuso de quem está ouvindo — a maior
// parte do público está nos EUA.
const GRADE = [
  { hora: 0, nome: 'Madrugada Romântica', desc: 'Baladas internacionais dos anos 70, 80 e 90' },
  { hora: 3, nome: 'Vozes do Coração', desc: 'MPB romântica e grandes cantoras' },
  { hora: 6, nome: 'Dance 2000', desc: 'Os hits dance que marcaram época' },
  { hora: 9, nome: 'Rock & Pop 90', desc: 'Clássicos da MTV dos anos 90' },
  { hora: 13, nome: 'Dance 2000', desc: 'Energia pra tarde toda' },
  { hora: 20, nome: 'Boteco Sertanejo', desc: 'O melhor do sertanejo pra fechar o dia' },
  { hora: 22, nome: 'Dance 2000', desc: 'Pista cheia até a madrugada' },
]

const BRASILIA_UTC_OFFSET = 3

function inicioLocal(hora) {
  const agora = new Date()
  // hoje, na data de Brasília, às `hora`:00 de Brasília
  const brasil = new Date(agora.getTime() - BRASILIA_UTC_OFFSET * 3600e3)
  return new Date(Date.UTC(brasil.getUTCFullYear(), brasil.getUTCMonth(), brasil.getUTCDate(), hora + BRASILIA_UTC_OFFSET))
}

function horaBrasiliaAgora() {
  const d = new Date(Date.now() - BRASILIA_UTC_OFFSET * 3600e3)
  return d.getUTCHours() + d.getUTCMinutes() / 60
}

const fmt = (d) => d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })

export default function Programacao() {
  const [agora, setAgora] = useState(horaBrasiliaAgora)

  useEffect(() => {
    const id = setInterval(() => setAgora(horaBrasiliaAgora()), 60000)
    return () => clearInterval(id)
  }, [])

  const atual = [...GRADE].reverse().find((p) => p.hora <= agora) || GRADE[GRADE.length - 1]
  let fuso = ''
  try {
    fuso = Intl.DateTimeFormat().resolvedOptions().timeZone.split('/').pop().replace(/_/g, ' ')
  } catch { /* fuso desconhecido */ }

  return (
    <section className="max-w-3xl mx-auto px-4 py-16">
      <div className="text-center mb-8">
        <h3 className="font-display font-bold text-3xl md:text-4xl tracking-wide mb-2">
          <span className="text-white">PROGRAMA</span><span className="brasil-text">ÇÃO</span>
        </h3>
        <p className="text-gray-400 text-sm">Horários no seu fuso{fuso ? ` (${fuso})` : ''}</p>
      </div>
      <ul className="space-y-2">
        {GRADE.map((p, i) => {
          const noAr = p === atual
          return (
            <li
              key={i}
              className={`flex items-center gap-4 rounded-xl px-4 py-3 border ${
                noAr ? 'bg-radio-greenDeep/30 border-radio-green' : 'bg-radio-card border-radio-border'
              }`}
            >
              <span className={`font-display font-bold text-lg w-16 shrink-0 ${noAr ? 'text-radio-greenBright' : 'text-radio-yellow'}`}>
                {fmt(inicioLocal(p.hora))}
              </span>
              <div className="flex-1 text-left">
                <p className="text-white font-semibold leading-tight">{p.nome}</p>
                <p className="text-gray-400 text-xs">{p.desc}</p>
              </div>
              {noAr && (
                <span className="flex items-center gap-1.5 text-xs font-bold tracking-widest text-radio-greenBright">
                  <span className="w-2 h-2 rounded-full bg-radio-greenBright onair-dot" /> NO AR
                </span>
              )}
            </li>
          )
        })}
      </ul>
    </section>
  )
}
