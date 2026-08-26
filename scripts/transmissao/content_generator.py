"""Transforma UMA notícia real (já coletada via RSS) em roteiro narrado
pra Rádio Fala Brasil — mesma regra do brasil-digital-bot: zero invenção.
"""
import json
import os

import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

PERIOD_LABELS = {
    "manha": "edição do meio-dia",
    "noite": "edição da noite",
}


def generate_content(article: dict, period: str) -> dict:
    """Adapta UMA notícia real em roteiro de boletim de rádio (~5-8 min).

    Regra inegociável: o modelo só pode usar o que está no texto da fonte.
    Nada de estatística, citação ou fato extra inventado ("achômetro"
    proibido) — igual à regra do content_generator.py do brasil-digital-bot.
    """
    label = PERIOD_LABELS.get(period, "edição")
    prompt = f"""Você é o âncora da "Transmissão Ao Vivo" da Rádio Fala Brasil, um programa estilo rádio comunitária pra brasileiros vivendo nos Estados Unidos (Massachusetts). Esta é a {label} do dia, narrada pela voz do Ronny.

O programa cobre só três tipos de assunto: política mundial em geral, descobertas de saúde, e principalmente tecnologia/IA. Tom de rádio comunitária: informativo, próximo, sem sensacionalismo — não é um programa policial nem de fofoca.

REGRA INEGOCIÁVEL: baseie-se EXCLUSIVAMENTE nas informações fornecidas abaixo, extraídas de uma matéria jornalística real. É PROIBIDO inventar números, datas, nomes, citações, causas ou consequências que não estejam no texto. Se um detalhe não estiver claro na fonte, seja mais genérico em vez de inventar — isso é jornalismo verificado, não especulação ("zero achômetro"). Pode mencionar a data de hoje normalmente, sem receio.

Fonte: {article['source']}
Link original: {article['link']}
Título original: {article['title']}
Resumo/trecho da matéria: {article['summary']}
Publicado: {article.get('published') or 'recentemente'}

Tarefa: escreva o roteiro de um boletim de notícias falado, em português brasileiro natural, tom de rádio (caloroso mas informativo, sem sensacionalismo, sem opinião pessoal), com saudação de abertura mencionando a Rádio Fala Brasil e a comunidade brasileira nos EUA, o conteúdo da notícia, e um encerramento curto. Total de 700 a 1000 palavras (~5-8 minutos falados).

Divida o roteiro em blocos curtos e naturais (2 a 4 blocos) pra facilitar a narração por partes.

Responda APENAS com JSON válido, sem markdown, seguindo exatamente este formato:
{{
  "headline": "manchete curta da notícia (máx 90 caracteres)",
  "summary": "resumo de 1-2 frases pra mostrar no site ao lado do player de áudio",
  "source_name": "{article['source']}",
  "source_url": "{article['link']}",
  "script_blocks": [
    "texto completo do bloco 1 (abertura + início da notícia), só o texto narrado, sem indicação de cena ou colchetes",
    "texto completo do bloco 2...",
    "... mais blocos se necessário, o último bloco deve fechar com uma despedida curta da Rádio Fala Brasil"
  ]
}}"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    content = json.loads(text.strip())

    content["period"] = period
    return content
