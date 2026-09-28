// Tira do pacote do app o que ele já busca do site no ar (edições diárias da
// Transmissão Ao Vivo) — rode depois do `cap sync`.
import { rmSync, readdirSync } from 'node:fs'
import { join } from 'node:path'

const dir = 'android/app/src/main/assets/public/transmissao'
for (const f of readdirSync(dir)) {
  if (f.endsWith('.mp3')) rmSync(join(dir, f))
}
console.log('app-slim: MP3 da transmissão removidos do pacote Android')
