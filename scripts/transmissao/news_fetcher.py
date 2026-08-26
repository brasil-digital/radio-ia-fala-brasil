"""Busca notícias reais e recentes do Brasil em fontes jornalísticas
verificadas via RSS — nenhum fato é inventado aqui, só coletado.

Regra do canal (igual ao brasil-digital-bot): o roteiro final
(content_generator.py) é obrigado a se basear SOMENTE no texto retornado
por essas fontes, nunca a inventar.
"""
import datetime
import html
import re

import feedparser

# (nome da fonte, URL do feed RSS) — todas testadas em 26/ago/2026 e
# retornando itens válidos (feedparser + status 200/302, entries > 0).
# URLs alternativas testadas e descartadas: agenciabrasil.ebc.com.br/feed
# (301, 0 entries) e cnnbrasil.com.br/nacional/feed/ (404).
FEEDS = [
    ("G1", "https://g1.globo.com/rss/g1/"),
    ("Agência Brasil", "https://agenciabrasil.ebc.com.br/rss.xml"),
    ("CNN Brasil", "https://www.cnnbrasil.com.br/feed/"),
    ("UOL Notícias", "https://rss.uol.com.br/feed/noticias.xml"),
]

# Notícia geral envelhece mais rápido que tech (janela mais curta que o
# brasil-digital-bot, que usa 30h) — queremos algo do próprio dia.
MAX_AGE_HOURS = 18
LIMIT_PER_FEED = 15

# Filtro de segurança: descarta ruído óbvio (loteria, cupom/promoção,
# horóscopo, guia de compra) que não é notícia.
NOISE_PATTERNS = re.compile(
    r"loteria|quina|lotof[aá]cil|mega-?sena|resultado da|cupom|% ?off|"
    r"promo[cç][aã]o|achados|onde comprar|melhor pre[cç]o|hor[oó]scopo",
    re.IGNORECASE,
)


def _clean_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_candidates(max_age_hours: int = MAX_AGE_HOURS) -> list[dict]:
    """Retorna lista de notícias recentes reais, mais novas primeiro."""
    now = datetime.datetime.now(datetime.timezone.utc)
    candidates = []

    for source, url in FEEDS:
        try:
            parsed = feedparser.parse(url, agent="Mozilla/5.0 (compatible; RadioFalaBrasilBot/1.0)")
        except Exception as e:
            print(f"⚠️  Falha ao ler feed de {source}: {e}")
            continue

        if getattr(parsed, "bozo", 0) and not parsed.entries:
            print(f"⚠️  Feed de {source} inválido/vazio, pulando.")
            continue

        for entry in parsed.entries[:LIMIT_PER_FEED]:
            struct = entry.get("published_parsed") or entry.get("updated_parsed")
            pub_dt = None
            age_h = None
            if struct:
                pub_dt = datetime.datetime(*struct[:6], tzinfo=datetime.timezone.utc)
                age_h = (now - pub_dt).total_seconds() / 3600
                if age_h > max_age_hours or age_h < 0:
                    continue

            summary = _clean_html(entry.get("summary", "") or entry.get("description", ""))[:700]
            title = _clean_html(entry.get("title", ""))
            link = entry.get("link", "")

            if not title or not link:
                continue
            if NOISE_PATTERNS.search(title):
                continue

            candidates.append({
                "source": source,
                "title": title,
                "link": link,
                "summary": summary,
                "published": pub_dt.isoformat() if pub_dt else None,
                "age_hours": age_h if age_h is not None else 999,
            })

    candidates.sort(key=lambda c: c["age_hours"])
    return candidates


def pick_unused(candidates: list[dict], used_links: set[str]) -> dict | None:
    """Escolhe a notícia real mais recente que ainda não foi usada."""
    for c in candidates:
        if c["link"] not in used_links:
            return c
    return None
