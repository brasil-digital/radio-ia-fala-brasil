import { LOJA } from '../lib/native'

// Vitrine da Fala Brasil Store (Shopify) dentro da rádio.
const ITENS = ['Camisetas', 'Moletons', 'Bonés', 'Canecas', 'Capinhas', 'Adesivos']

export default function Loja() {
  return (
    <section className="max-w-4xl mx-auto px-4 pb-16">
      <div className="bg-gradient-to-br from-radio-greenDeep/60 via-radio-card to-radio-card border border-radio-yellow/40 rounded-2xl p-6 md:p-8 text-center">
        <p className="text-radio-yellow text-xs font-bold tracking-[0.3em] mb-2">🛒 FALA BRASIL STORE</p>
        <h3 className="font-display font-bold text-2xl md:text-3xl text-white tracking-wide mb-3">
          LEVE O BRASIL COM <span className="brasil-text">VOCÊ</span>
        </h3>
        <p className="text-gray-300 mb-5">
          Saudade, Uai Sô, Oxente, Tô Bizado… as gírias e o orgulho brasileiro em produtos feitos nos EUA.
        </p>
        <div className="flex flex-wrap justify-center gap-2 mb-6">
          {ITENS.map((item) => (
            <span key={item} className="text-xs text-gray-200 bg-radio-dark/70 border border-radio-border rounded-full px-3 py-1">
              {item}
            </span>
          ))}
        </div>
        <a
          href={LOJA}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 bg-radio-yellow hover:brightness-110 text-radio-dark font-bold px-8 py-3.5 rounded-full text-lg transition"
        >
          Visitar a loja
          <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5-5 5M6 12h12" />
          </svg>
        </a>
        <p className="text-gray-500 text-xs mt-3">loja.falabrasil.digital · entrega em todos os EUA</p>
      </div>
    </section>
  )
}
