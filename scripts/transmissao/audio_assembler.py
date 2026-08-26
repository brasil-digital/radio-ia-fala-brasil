"""Concatena blocos narrados + vinhetas/trilha opcionais + normalização,
porta direta do pipeline ffmpeg de gerar-programa.ps1 pra Python/subprocess.

Vinheta de abertura/fechamento e trilha de fundo são OPCIONAIS (mesmo
padrão dos scripts PowerShell originais — nunca existiram como arquivos
reais no repo criativo, só como entrada aceita se presente). Coloque
`vinheta-abertura.mp3`, `vinheta-fechamento.mp3` e/ou `trilha-fundo.mp3`
em scripts/transmissao/assets/ se quiser usá-los; sem eles, sai só a
narração normalizada.
"""
import os
import subprocess
import tempfile

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
VINHETA_ABERTURA = os.path.join(ASSETS_DIR, "vinheta-abertura.mp3")
VINHETA_FECHAMENTO = os.path.join(ASSETS_DIR, "vinheta-fechamento.mp3")
TRILHA_FUNDO = os.path.join(ASSETS_DIR, "trilha-fundo.mp3")


def _run(args: list[str]) -> None:
    subprocess.run(args, check=True, capture_output=True)


def _make_silence(path: str, seconds: float = 0.8) -> None:
    _run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo",
        "-t", str(seconds), "-c:a", "libmp3lame", "-q:a", "4", path,
    ])


def assemble(block_files: list[str], output_path: str) -> float:
    """Concatena os blocos (+ vinhetas/pausas se existirem), mixa com
    trilha de fundo se existir, normaliza em -14 LUFS. Retorna a duração
    final em segundos."""
    with tempfile.TemporaryDirectory() as tmp:
        pausa = os.path.join(tmp, "pausa.mp3")
        _make_silence(pausa)

        sequence = []
        if os.path.exists(VINHETA_ABERTURA):
            sequence += [VINHETA_ABERTURA, pausa]
        for i, block in enumerate(block_files):
            sequence.append(block)
            if i < len(block_files) - 1:
                sequence.append(pausa)
        if os.path.exists(VINHETA_FECHAMENTO):
            sequence += [pausa, VINHETA_FECHAMENTO]

        # Reencoda na concatenação (em vez de -c copy) — juntar streams mp3
        # gerados separadamente sem reencodar causa timestamps inválidos e a
        # voz "embolar" na emenda entre blocos (mesmo motivo do .ps1 original).
        input_args = []
        for f in sequence:
            input_args += ["-i", f]
        filter_inputs = "".join(f"[{i}:a]" for i in range(len(sequence)))
        filter_complex = f"{filter_inputs}concat=n={len(sequence)}:v=0:a=1[outa]"

        narracao_completa = os.path.join(tmp, "narracao-completa.mp3")
        _run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            *input_args, "-filter_complex", filter_complex,
            "-map", "[outa]", "-c:a", "libmp3lame", "-b:a", "192k",
            narracao_completa,
        ])

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if os.path.exists(TRILHA_FUNDO):
            _run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", narracao_completa, "-stream_loop", "-1", "-i", TRILHA_FUNDO,
                "-filter_complex",
                "[1:a]volume=0.15[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=3,"
                "loudnorm=I=-14:TP=-1:LRA=11",
                "-c:a", "libmp3lame", "-b:a", "192k", output_path,
            ])
        else:
            _run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", narracao_completa, "-af", "loudnorm=I=-14:TP=-1:LRA=11",
                "-c:a", "libmp3lame", "-b:a", "192k", output_path,
            ])

    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", output_path],
        check=True, capture_output=True, text=True,
    )
    return float(result.stdout.strip())
