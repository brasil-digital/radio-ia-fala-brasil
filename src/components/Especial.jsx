import { useState, useEffect } from 'react'
import { live } from '../lib/native'

// Reportagem especial em destaque no topo (ex.: notícia de uma cidade). O
// conteúdo vem de public/especial/especial.json — trocar o especial é só
// trocar os arquivos dessa pasta, sem mexer no código. Some sozinho depois
// da data "ate" (fim do dia, horário de Brasília).
async function fetchEspecial() {
  try {
    const res = await fetch(live('/especial/especial.json'), { cache: 'no-store' })
    if (!res.ok) return null
    return await res.json()
  } catch {
    return null
  }
}

function expirado(ate) {
  if (!ate) return false
  const fim = new Date(`${ate}T23:59:59-03:00`)
  return !Number.isNaN(fim.getTime()) && Date.now() > fim.getTime()
}

export default function Especial() {
  const [dados, setDados] = useState(null)

  useEffect(() => {
    let cancelled = false
    fetchEspecial().then((d) => {
      if (!cancelled) setDados(d)
    })
    return () => { cancelled = true }
  }, [])

  if (!dados || expirado(dados.ate)) return null

  const fotos = dados.fotos || []
  const versao = encodeURIComponent(dados.versao || '')

  return (
    <div className="mt-8 bg-radio-card border-2 border-radio-yellow/70 rounded-2xl p-5 text-left max-w-xl mx-auto shadow-lg shadow-radio-yellow/10">
      <div className="inline-flex items-center gap-2 mb-3 bg-radio-yellow text-radio-dark rounded-full px-3 py-1">
        <span className="text-xs font-bold tracking-widest">⭐ ESPECIAL</span>
        {dados.local && <span className="text-xs font-semibold">· {dados.local}</span>}
      </div>

      {fotos.length > 0 && (
        <div className="flex gap-2 overflow-x-auto snap-x snap-mandatory rounded-xl mb-4 pb-1">
          {fotos.map((foto) => (
            <img
              key={foto.arquivo}
              src={live(`/especial/${foto.arquivo}?v=${versao}`)}
              alt={foto.legenda || dados.titulo}
              loading="lazy"
              className={`${fotos.length > 1 ? 'w-[80%]' : 'w-full'} shrink-0 snap-center rounded-xl object-cover aspect-[4/5]`}
            />
          ))}
        </div>
      )}

      <h4 className="font-display font-bold text-white text-xl leading-tight mb-2">{dados.titulo}</h4>
      <p className="text-gray-300 text-sm mb-4">{dados.resumo}</p>
      <audio controls preload="none" className="w-full" src={live(`/especial/${dados.audio}?v=${versao}`)} />
      {dados.credito && <p className="text-gray-500 text-xs mt-2">{dados.credito}</p>}
    </div>
  )
}
