"""Histórico de links já usados — evita repetir a mesma notícia entre dias.

Mais confiável que comparar títulos (que podem variar em cada fonte):
guardamos o link original da matéria usada em cada edição já gerada.
"""
import json
import os

HISTORY_PATH = os.path.join(os.path.dirname(__file__), "data", "posted_links_transmissao.json")
MAX_HISTORY = 200


def load_used_links() -> set[str]:
    if not os.path.exists(HISTORY_PATH):
        return set()
    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_used_links(links: list[str]) -> None:
    """Persiste vários links de uma vez (usado no fim de main.py, depois
    que as edições da manhã E da noite já foram escolhidas — evita gravar
    o histórico pela metade se o processo cair no meio da execução)."""
    existing = list(load_used_links())
    existing.extend(links)
    existing = existing[-MAX_HISTORY:]
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
