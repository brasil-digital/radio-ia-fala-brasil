"""Orquestrador da Transmissão Ao Vivo — gera as edições da manhã e da
noite numa única execução diária (roda cedo, bem antes das duas janelas
"ao vivo" do site: 12h-13h e 19h-20h horário do Leste dos EUA).

Uso: python main.py
Requer: ELEVENLABS_API_KEY, ANTHROPIC_API_KEY no ambiente; ffmpeg/ffprobe no PATH.
"""
import datetime
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))

import audio_assembler
import content_generator
import history
import narration
import news_fetcher

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "public", "transmissao")
PERIODS = ["manha", "noite"]


def generate_edition(period: str, candidates: list[dict], used_links: set[str], newly_used: list[str]) -> None:
    article = news_fetcher.pick_unused(candidates, used_links | set(newly_used))
    if article is None:
        print(f"⚠️  Nenhuma notícia nova disponível pra edição '{period}' — pulando.")
        return

    print(f"\n===== Edição '{period}': {article['title']} ({article['source']}) =====")
    content = content_generator.generate_content(article, period)
    newly_used.append(article["link"])

    blocks = content["script_blocks"]
    print(f"{len(blocks)} blocos de roteiro.")

    with tempfile.TemporaryDirectory() as tmp:
        block_files = []
        for i, block_text in enumerate(blocks):
            block_path = os.path.join(tmp, f"bloco-{i:02d}.mp3")
            print(f"Narrando bloco {i + 1}/{len(blocks)}...")
            narration.narrate_block(block_text, block_path)
            block_files.append(block_path)

        os.makedirs(PUBLIC_DIR, exist_ok=True)
        output_mp3 = os.path.join(PUBLIC_DIR, f"{period}.mp3")
        duration = audio_assembler.assemble(block_files, output_mp3)

    metadata = {
        "headline": content["headline"],
        "summary": content["summary"],
        "source_name": content["source_name"],
        "source_url": content["source_url"],
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "duration_seconds": round(duration),
        "period": period,
    }
    output_json = os.path.join(PUBLIC_DIR, f"{period}.json")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"✅ Edição '{period}' pronta: {output_mp3} ({round(duration)}s)")


def main() -> None:
    used_links = history.load_used_links()
    candidates = news_fetcher.fetch_candidates()
    print(f"{len(candidates)} notícias candidatas encontradas.")

    newly_used: list[str] = []
    for period in PERIODS:
        generate_edition(period, candidates, used_links, newly_used)

    if newly_used:
        history.save_used_links(newly_used)
        print(f"\nHistórico atualizado com {len(newly_used)} novo(s) link(s).")


if __name__ == "__main__":
    main()
