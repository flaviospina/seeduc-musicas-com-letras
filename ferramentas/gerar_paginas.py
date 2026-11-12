#!/usr/bin/env python3
# ferramentas/gerar_paginas.py
# Gera as páginas HTML (índice e uma por música), os QR codes e a folha de impressão.
# As letras NÃO ficam aqui: estão em musica/assets/letras.js (único arquivo a editar).
# A lista abaixo serve só para nomes de pastas, cores e QR codes.
# Uso (opcional, só para regenerar): python3 ferramentas/gerar_paginas.py
# Requer: pip install segno pillow

import os, shutil, html
from pathlib import Path

import segno
from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "musica"
DOMINIO = "https://cecapescs.com.br/musica/"

MUSICAS = [
    {
        "n": 1, "slug": "canta-canta-minha-gente", "estilo": "Samba",
        "titulo": "Canta, Canta, Minha Gente", "artista": "Martinho da Vila",
        "cor": "#f59e0b", "cor2": "#ef4444", "emoji": "🥁",
        "link": "https://www.letras.mus.br/martinho-da-vila/287326/",
        "link_txt": "Ver letra completa no Letras.mus.br", "letra": None,
    },
    {
        "n": 2, "slug": "eu-so-quero-um-xodo", "estilo": "Forró",
        "titulo": "Eu Só Quero um Xodó", "artista": "Dominguinhos",
        "cor": "#f97316", "cor2": "#eab308", "emoji": "🪗",
        "link": "https://www.letras.mus.br/dominguinhos/357861/",
        "link_txt": "Ver letra completa no Letras.mus.br", "letra": None,
    },
    {
        "n": 3, "slug": "estrada-da-vida", "estilo": "Caipira / Sertanejo raiz",
        "titulo": "Estrada da Vida", "artista": "Milionário & José Rico",
        "cor": "#84cc16", "cor2": "#16a34a", "emoji": "🎸",
        "link": "https://www.letras.mus.br/milionario-e-jose-rico/47389/",
        "link_txt": "Ver letra completa no Letras.mus.br", "letra": None,
    },
    {
        "n": 4, "slug": "e-preciso-saber-viver", "estilo": "Rock nacional",
        "titulo": "É Preciso Saber Viver", "artista": "Titãs",
        "cor": "#8b5cf6", "cor2": "#ec4899", "emoji": "🎸",
        "link": "https://www.letras.mus.br/titas/48967/",
        "link_txt": "Ver letra completa no Letras.mus.br", "letra": None,
    },
    {
        "n": 5, "slug": "stand-by-me", "estilo": "Rock internacional",
        "titulo": "Stand by Me", "artista": "Ben E. King",
        "cor": "#3b82f6", "cor2": "#06b6d4", "emoji": "🎤",
        "link": "https://www.letras.mus.br/king-ben-e/21189/traducao.html",
        "link_txt": "Ver letra e tradução no Letras.mus.br", "letra": None,
    },
    {
        "n": 6, "slug": "o-sol", "estilo": "Pop",
        "titulo": "O Sol", "artista": "Vitor Kley",
        "cor": "#fbbf24", "cor2": "#f97316", "emoji": "☀️",
        "link": "https://www.letras.mus.br/vitor-kley/sol/",
        "link_txt": "Ver letra completa no Letras.mus.br", "letra": None,
    },
    {
        "n": 7, "slug": "tempos-modernos", "estilo": "MPB",
        "titulo": "Tempos Modernos", "artista": "Lulu Santos",
        "cor": "#14b8a6", "cor2": "#3b82f6", "emoji": "🎹",
        "link": "https://www.letras.mus.br/lulu-santos/47144/",
        "link_txt": "Ver letra completa no Letras.mus.br", "letra": None,
    },
    {
        "n": 8, "slug": "evidencias", "estilo": "Sertanejo",
        "titulo": "Evidências", "artista": "Chitãozinho & Xororó",
        "cor": "#ef4444", "cor2": "#be185d", "emoji": "🤠",
        "link": "https://www.letras.mus.br/chitaozinho-e-xororo/768469/",
        "link_txt": "Ver letra completa no Letras.mus.br", "letra": None,
    },
    {
        "n": 9, "slug": "peneirei-fuba", "estilo": "Brincadeira cantada",
        "titulo": "Peneirei Fubá", "artista": "Cantiga popular (domínio público)",
        "cor": "#22c55e", "cor2": "#facc15", "emoji": "🎶",
        "link": None, "link_txt": None, "letra": None,
    },
]

NOTAS = ["♪", "♫", "♩", "♬", "♪", "♫", "♩", "♬", "♪", "♫", "♬", "♪"]


def notas_html():
    # 12 notas flutuantes espalhadas pela tela, animadas via CSS
    partes = []
    for i, n in enumerate(NOTAS):
        partes.append(f'<span class="nota n{i+1}" aria-hidden="true">{n}</span>')
    return "\n    ".join(partes)



def cabeca_html(titulo_pagina, descricao, prefixo, cor, cor2):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{titulo_pagina}</title>
  <meta name="description" content="{descricao}">
  <meta property="og:title" content="{titulo_pagina}">
  <meta property="og:image" content="{DOMINIO}assets/logo-seeduc.png">
  <meta name="theme-color" content="{cor}">
  <link rel="icon" href="{prefixo}assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefixo}assets/estilo.css">
  <style>
    :root {{ --cor: {cor}; --cor2: {cor2}; }}
  </style>
</head>
"""


def pagina_musica(m):
    titulo = html.escape(m["titulo"])
    artista = html.escape(m["artista"])
    estilo = html.escape(m["estilo"])
    cabeca = cabeca_html(f"{titulo} — {artista} | Músicas SEEDUC",
                         f"{estilo}: {titulo}, de {artista}. Projeto Músicas com Letras — SEEDUC São Caetano do Sul.",
                         "../", m["cor"], m["cor2"])
    return f"""{cabeca}<body>
  <div class="fundo" aria-hidden="true">
    {notas_html()}
  </div>

  <main class="cartao">
    <header class="topo">
      <a href="../" class="logo-link" title="Voltar para a lista de músicas">
        <img src="../assets/logo-seeduc.png" alt="SEEDUC — Secretaria de Educação de São Caetano do Sul" class="logo">
      </a>
      <span class="selo" id="selo">Música {m['n']} de {len(MUSICAS)}</span>
    </header>

    <!-- O conteúdo (título, letra, QR) é montado por assets/app.js a partir de assets/letras.js -->
    <div id="conteudo" class="conteudo">
      <noscript><p>Ative o JavaScript para ver a letra, ou <a href="../">volte à lista</a>.</p></noscript>
    </div>
  </main>

  <script src="../assets/letras.js"></script>
  <script src="../assets/app.js"></script>
  <script>montarPagina('conteudo', '{m['slug']}');</script>
</body>
</html>
"""


def pagina_indice():
    cabeca = cabeca_html("Músicas com Letras | SEEDUC São Caetano do Sul",
                         "Repertório do projeto Músicas com Letras da SEEDUC São Caetano do Sul: samba, forró, sertanejo, rock, pop, MPB e brincadeira cantada.",
                         "", "#2563eb", "#ec4899")
    return f"""{cabeca}<body>
  <div class="fundo" aria-hidden="true">
    {notas_html()}
  </div>

  <main class="cartao">
    <header class="topo">
      <a href="#" class="logo-link" title="Lista de músicas">
        <img src="assets/logo-seeduc.png" alt="SEEDUC — Secretaria de Educação de São Caetano do Sul" class="logo">
      </a>
      <span class="selo" id="selo">{len(MUSICAS)} músicas</span>
    </header>

    <!-- Lista e letras montadas por assets/app.js a partir de assets/letras.js.
         Selecionar uma música muda o endereço para #nome-da-musica e mostra a letra. -->
    <div id="conteudo" class="conteudo">
      <noscript><p>Ative o JavaScript para ver as músicas.</p></noscript>
    </div>
  </main>

  <script src="assets/letras.js"></script>
  <script src="assets/app.js"></script>
  <script>montarIndice('conteudo');</script>
</body>
</html>
"""


def pagina_qrcodes():
    cartoes = []
    for m in MUSICAS:
        url = f"{DOMINIO}{m['slug']}/"
        cartoes.append(f"""      <article class="qr-cartao" style="--cor: {m['cor']}; --cor2: {m['cor2']};">
        <div class="qr-faixa"><img src="../assets/logo-seeduc.png" alt="SEEDUC" class="qr-logo"></div>
        <div class="qr-estilo">{m['emoji']} {html.escape(m['estilo'])}</div>
        <h2>{html.escape(m['titulo'])}</h2>
        <p class="qr-artista">{html.escape(m['artista'])}</p>
        <img src="{m['slug']}.png" alt="QR Code: {html.escape(m['titulo'])}" class="qr-img">
        <p class="qr-url">{url}</p>
      </article>""")
    geral = f"""      <article class="qr-cartao qr-geral" style="--cor: #2563eb; --cor2: #ec4899;">
        <div class="qr-faixa"><img src="../assets/logo-seeduc.png" alt="SEEDUC" class="qr-logo"></div>
        <div class="qr-estilo">🎵 QR code geral</div>
        <h2>Músicas com Letras</h2>
        <p class="qr-artista">Abre a lista completa — toque na música para ver a letra</p>
        <img src="geral.png" alt="QR Code: lista de músicas" class="qr-img">
        <p class="qr-url">{DOMINIO}</p>
      </article>"""
    corpo = geral + "\n" + "\n".join(cartoes)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>QR Codes — Músicas com Letras | SEEDUC</title>
  <link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/estilo.css">
  <style>
    :root {{ --cor: #2563eb; --cor2: #ec4899; }}
  </style>
</head>
<body class="pagina-qr">
  <div class="fundo" aria-hidden="true">
    {notas_html()}
  </div>

  <main class="cartao cartao-largo">
    <header class="topo">
      <a href="../" class="logo-link"><img src="../assets/logo-seeduc.png" alt="SEEDUC" class="logo"></a>
      <button type="button" class="botao-pequeno" onclick="window.print()">🖨️ Imprimir folha</button>
    </header>
    <div class="cabecalho">
      <span class="estilo">📱 QR Codes</span>
      <h1>Músicas com Letras</h1>
      <p class="artista">Recorte os cartões e cole na sala, no mural ou no caderno</p>
    </div>

    <section class="grade-qr">
{corpo}
    </section>
  </main>
</body>
</html>
"""


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2563eb"/><stop offset="1" stop-color="#ec4899"/></linearGradient></defs>
  <rect width="64" height="64" rx="14" fill="url(#g)"/>
  <text x="32" y="46" font-size="40" text-anchor="middle" fill="#fff" font-family="Arial, sans-serif">♪</text>
</svg>
"""


def gerar_logo_placeholder(caminho):
    """Gera um logo provisório. Substitua pelo arquivo oficial da SEEDUC mantendo o nome."""
    if caminho.exists():
        return  # não sobrescreve um logo oficial já colocado
    L, A = 720, 220
    img = Image.new("RGBA", (L, A), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    try:
        f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 92)
        f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 34)
    except OSError:
        f1 = f2 = ImageFont.load_default()
    d.rounded_rectangle((0, 0, 200, A), radius=40, fill=(37, 99, 235, 255))
    d.text((100, A // 2), "♪", font=f1, fill="white", anchor="mm")
    d.text((225, 78), "SEEDUC", font=f1, fill=(30, 41, 59, 255), anchor="lm")
    d.text((228, 160), "Secretaria de Educação · São Caetano do Sul", font=f2, fill=(71, 85, 105, 255), anchor="lm")
    img.save(caminho)


def gerar_qr(url, destino):
    qr = segno.make(url, error="h")  # correção alta: continua lendo mesmo com logo ou impressão ruim
    qr.save(str(destino), scale=12, border=2, dark="#1e293b", light="#ffffff")


def main():
    assets = SAIDA / "assets"
    qrs = SAIDA / "qrcodes"
    assets.mkdir(parents=True, exist_ok=True)
    qrs.mkdir(parents=True, exist_ok=True)

    (assets / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    gerar_logo_placeholder(assets / "logo-seeduc.png")

    (SAIDA / "index.html").write_text(pagina_indice(), encoding="utf-8")
    (qrs / "index.html").write_text(pagina_qrcodes(), encoding="utf-8")

    gerar_qr(DOMINIO, qrs / "geral.png")
    print(f"OK  QR  geral                      {DOMINIO}")

    for m in MUSICAS:
        pasta = SAIDA / m["slug"]
        pasta.mkdir(exist_ok=True)
        (pasta / "index.html").write_text(pagina_musica(m), encoding="utf-8")
        url = f"{DOMINIO}{m['slug']}/"
        gerar_qr(url, pasta / "qrcode.png")
        shutil.copy(pasta / "qrcode.png", qrs / f"{m['slug']}.png")
        print(f"OK  {m['n']:>2}  {m['slug']:<26} {url}")

    print(f"\nPáginas geradas em: {SAIDA}")


if __name__ == "__main__":
    main()
