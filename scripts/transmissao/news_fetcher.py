"""Busca notícias reais e recentes em fontes jornalísticas verificadas via
RSS — nenhum fato é inventado aqui, só coletado.

Escopo editorial (estilo rádio comunitária, definido pelo usuário em
26/ago/2026): política mundial em geral, descobertas de saúde, e
PRINCIPALMENTE tecnologia/IA — por isso a maioria dos feeds abaixo é de
tech/IA. Nada de política/economia doméstica do dia a dia, nem
crime/polícia local (o feed geral do G1 foi removido por causa disso —
trazia bastante notícia policial).

Regra do canal (igual ao brasil-digital-bot): o roteiro final
(content_generator.py) é obrigado a se basear SOMENTE no texto retornado
por essas fontes, nunca a inventar.
"""
import datetime
import html
import re

import feedparser

# (nome da fonte, URL do feed RSS) — todas testadas em 26/ago/2026
# (feedparser + status 200/302, entries > 0).
# Descartadas por não existir/retornar vazio: cnnbrasil.com.br (mundo/saude/
# category, todas 404), agenciabrasil.ebc.com.br (política/geral/saude/
# internacional, todas 404), rss.uol.com.br (internacional/saude/ciencia,
# todas 404).
FEEDS = [
    # Política mundial / notícias internacionais em geral
    ("BBC Brasil", "http://feeds.bbci.co.uk/portuguese/rss.xml"),
    ("G1 Mundo", "https://g1.globo.com/rss/g1/mundo/"),
    # Descobertas de saúde / ciência
    ("G1 Ciência e Saúde", "https://g1.globo.com/rss/g1/ciencia-e-saude/"),
    # Tecnologia e IA — foco principal do programa, por isso a maioria
    # dos feeds é daqui (mesmas fontes já validadas no brasil-digital-bot)
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("MIT Technology Review", "https://www.technologyreview.com/feed/"),
    ("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
    ("Ars Technica AI", "https://arstechnica.com/ai/feed/"),
    ("Wired AI", "https://www.wired.com/feed/tag/ai/latest/rss"),
    ("Canaltech IA", "https://canaltech.com.br/rss/inteligencia-artificial/"),
    ("Olhar Digital IA", "https://olhardigital.com.br/editorias/inteligencia-artificial/feed/"),
    ("InfoMoney IA", "https://www.infomoney.com.br/tudo-sobre/inteligencia-artificial/feed/"),
]

# Mistura de notícia geral (envelhece rápido) com tech/IA (o brasil-digital-bot
# usa 30h pros mesmos feeds de tech) — meio-termo de 24h cobre os dois bem.
MAX_AGE_HOURS = 24
LIMIT_PER_FEED = 15

# Filtro de segurança: descarta ruído óbvio (loteria, cupom/promoção,
# horóscopo, guia de compra) que não é notícia.
NOISE_PATTERNS = re.compile(
    r"loteria|quina|lotof[aá]cil|mega-?sena|resultado da|cupom|% ?off|"
    r"promo[cç][aã]o|achados|onde comprar|melhor pre[cç]o|hor[oó]scopo",
    re.IGNORECASE,
)

# Fora do escopo editorial (rádio comunitária: política mundial, saúde,
# tech/IA) — os feeds de "Mundo"/BBC também trazem crime/polícia/tragédia
# local, que não é o tom pedido. Feeds de tech/IA/saúde não costumam bater
# aqui, então o filtro é seguro pra todas as fontes.
OFF_TOPIC_PATTERNS = re.compile(
    r"pol[ií]cia|policial|pres[oa] (em|por|ap[oó]s)|prende|prend[eu]|"
    r"assassinat|homic[ií]dio|estupr|sequestr|guilhotina|esfaque|tiroteio|"
    r"balead[oa]|linchad|desaparecid|desabou",
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
            if NOISE_PATTERNS.search(title) or OFF_TOPIC_PATTERNS.search(title):
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
