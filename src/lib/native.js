import { Capacitor } from '@capacitor/core'

// No app (Android/iOS) as páginas vêm empacotadas dentro do APK/IPA — o que
// muda todo dia (edições da Transmissão Ao Vivo) precisa vir do site no ar,
// senão o app ficaria preso na edição do dia em que foi gerado.
export const isNative = Capacitor.isNativePlatform()
export const SITE = 'https://www.radiofalabrasil.com'

export const live = (path) => (isNative ? SITE + path : path)
