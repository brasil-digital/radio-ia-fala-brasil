import { Capacitor } from '@capacitor/core'

// No app (Android/iOS) as páginas vêm empacotadas dentro do APK/IPA — o que
// muda todo dia (edições da Transmissão Ao Vivo) precisa vir do site no ar,
// senão o app ficaria preso na edição do dia em que foi gerado.
export const isNative = Capacitor.isNativePlatform()
export const SITE = 'https://www.radiofalabrasil.com'
export const LOJA = 'https://loja.falabrasil.digital'

export const live = (path) => (isNative ? SITE + path : path)

// No app não existe "nova aba": link com target="_blank" simplesmente não faz
// nada no WebView. Navegando a própria página pra URL externa, o Capacitor
// entrega o link pro sistema — abre o app do YouTube, o navegador ou o e-mail.
export function abrirLinksExternosForaDoApp() {
  if (!isNative) return
  document.addEventListener(
    'click',
    (e) => {
      const a = e.target.closest?.('a[href]')
      if (!a) return
      const href = a.getAttribute('href')
      if (!/^(https?:|mailto:|tel:)/i.test(href)) return
      e.preventDefault()
      window.location.href = href
    },
    true,
  )
}
