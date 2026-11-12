#!/usr/bin/env python3
# ferramentas/gerar_paginas.py
# Gera as páginas HTML de cada música, os QR codes e a folha de impressão.
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
        "link": None, "link_txt": None,
        # Versão enviada pelo professor (cantiga tradicional, domínio público)
        "letra": [
            ["Peneirou fubá,", "O fubá caiu.", "Tornei a peneirar,", "O fubá subiu."],
            ["Lá vêm as famílias,", "Todas animadas,", "Com a peneira na mão.", "Não deixe cair o fubá no chão!"],
            ["Peneirou fubá,", "O fubá caiu.", "Tornei a peneirar,", "O fubá subiu."],
        ],
    },
]

NOTAS = ["♪", "♫", "♩", "♬", "♪", "♫", "♩", "♬", "♪", "♫", "♬", "♪"]


def notas_html():
    # 12 notas flutuantes espalhadas pela tela, animadas via CSS
    partes = []
    for i, n in enumerate(NOTAS):
        partes.append(f'<span class="nota n{i+1}" aria-hidden="true">{n}</span>')
    return "\n    ".join(partes)


def bloco_letra(m):
    if m["letra"]:
        estrofes = []
        for est in m["letra"]:
            linhas = "<br>\n          ".join(html.escape(l) for l in est)
            estrofes.append(f"        <p>\n          {linhas}\n        </p>")
        corpo = "\n".join(estrofes)
        return f"""      <section class="letra" id="letra" aria-label="Letra da música">
{corpo}
      </section>"""
    # Música com direitos autorais: a letra não é reproduzida aqui.
    return f"""      <section class="letra letra-externa" id="letra" aria-label="Letra da música">
        <!--
          ============================================================
          LETRA DESTA MÚSICA
          A letra é protegida por direitos autorais e por isso não foi
          incluída automaticamente. Se a escola tiver autorização para
          publicá-la, apague o bloco <div class="aviso-letra"> abaixo e
          cole a letra no lugar, usando <p> para cada estrofe e <br>
          entre os versos, como no exemplo:

          <p>
            Primeiro verso<br>
            Segundo verso<br>
            Terceiro verso
          </p>
          ============================================================
        -->
        <div class="aviso-letra">
          <div class="aviso-icone">{m["emoji"]}</div>
          <p>A letra desta música é protegida por direitos autorais.<br>
          Toque no botão para abrir a letra oficial e cantar junto!</p>
          <a class="botao" href="{m["link"]}" target="_blank" rel="noopener">
            {m["link_txt"]} ↗
          </a>
        </div>
      </section>"""


def pagina_musica(m):
    url = f"{DOMINIO}{m['slug']}/"
    titulo = html.escape(m["titulo"])
    artista = html.escape(m["artista"])
    estilo = html.escape(m["estilo"])
    link_rodape = ""
    if m["link"]:
        link_rodape = f"""        <a class="link-externo" href="{m["link"]}" target="_blank" rel="noopener">{m["link_txt"]} ↗</a>\n"""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{titulo} — {artista} | Músicas SEEDUC</title>
  <meta name="description" content="{estilo}: {titulo}, de {artista}. Projeto Músicas com Letras — SEEDUC São Caetano do Sul.">
  <meta property="og:title" content="{titulo} — {artista}">
  <meta property="og:description" content="{estilo} · Músicas com Letras · SEEDUC São Caetano do Sul">
  <meta property="og:image" content="{DOMINIO}assets/logo-seeduc.png">
  <meta name="theme-color" content="{m['cor']}">
  <link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/estilo.css">
  <style>
    :root {{ --cor: {m['cor']}; --cor2: {m['cor2']}; }}
  </style>
</head>
<body>
  <div class="fundo" aria-hidden="true">
    {notas_html()}
  </div>

  <main class="cartao">
    <header class="topo">
      <a href="../" class="logo-link" title="Voltar para a lista de músicas">
        <img src="../assets/logo-seeduc.png" alt="SEEDUC — Secretaria de Educação de São Caetano do Sul" class="logo">
      </a>
      <span class="selo">Música {m['n']} de {len(MUSICAS)}</span>
    </header>

    <div class="cabecalho">
      <span class="estilo">{m['emoji']} {estilo}</span>
      <h1>{titulo}</h1>
      <p class="artista">{artista}</p>
    </div>

    <div class="ferramentas" role="toolbar" aria-label="Opções de leitura">
      <button type="button" onclick="mudarFonte(-1)" title="Diminuir letra">A−</button>
      <button type="button" onclick="mudarFonte(1)" title="Aumentar letra">A+</button>
      <button type="button" onclick="window.print()" title="Imprimir">🖨️ Imprimir</button>
      <button type="button" onclick="compartilhar()" title="Compartilhar">📤 Compartilhar</button>
    </div>

{bloco_letra(m)}

    <footer class="rodape">
      <div class="qr">
        <img src="qrcode.png" alt="QR Code desta página" width="120" height="120">
        <small>Aponte a câmera para abrir esta página</small>
      </div>
      <div class="rodape-texto">
{link_rodape}        <a class="link-externo" href="../">🎵 Todas as músicas</a>
        <p>Projeto <strong>Músicas com Letras</strong><br>SEEDUC — Secretaria de Educação de São Caetano do Sul</p>
      </div>
    </footer>
  </main>

  <script>
    // Controle do tamanho da letra (guardado no navegador)
    var tamanho = Number(localStorage.getItem('tamanhoLetra') || 0);
    function aplicarFonte() {{
      document.documentElement.style.setProperty('--escala', (1 + tamanho * 0.15).toFixed(2));
      localStorage.setItem('tamanhoLetra', tamanho);
    }}
    function mudarFonte(delta) {{
      tamanho = Math.max(-2, Math.min(4, tamanho + delta));
      aplicarFonte();
    }}
    aplicarFonte();

    // Compartilhar (usa o menu nativo do celular quando disponível)
    function compartilhar() {{
      var dados = {{ title: document.title, text: '{titulo} — {artista}', url: '{url}' }};
      if (navigator.share) {{
        navigator.share(dados).catch(function () {{}});
      }} else if (navigator.clipboard) {{
        navigator.clipboard.writeText(dados.url).then(function () {{
          alert('Link copiado: ' + dados.url);
        }});
      }} else {{
        prompt('Copie o link desta página:', dados.url);
      }}
    }}
  </script>
</body>
</html>
"""


def pagina_indice():
    itens = []
    for m in MUSICAS:
        itens.append(f"""      <a class="item" href="{m['slug']}/" style="--cor: {m['cor']}; --cor2: {m['cor2']};">
        <span class="num">{m['n']}</span>
        <span class="emoji">{m['emoji']}</span>
        <span class="info">
          <strong>{html.escape(m['titulo'])}</strong>
          <span>{html.escape(m['artista'])}</span>
          <em>{html.escape(m['estilo'])}</em>
        </span>
        <span class="seta">›</span>
      </a>""")
    lista = "\n".join(itens)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Músicas com Letras | SEEDUC São Caetano do Sul</title>
  <meta name="description" content="Repertório do projeto Músicas com Letras da SEEDUC São Caetano do Sul: samba, forró, sertanejo, rock, pop, MPB e brincadeira cantada.">
  <meta name="theme-color" content="#2563eb">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/estilo.css">
  <style>
    :root {{ --cor: #2563eb; --cor2: #ec4899; }}
  </style>
</head>
<body>
  <div class="fundo" aria-hidden="true">
    {notas_html()}
  </div>

  <main class="cartao">
    <header class="topo">
      <img src="assets/logo-seeduc.png" alt="SEEDUC — Secretaria de Educação de São Caetano do Sul" class="logo">
      <span class="selo">{len(MUSICAS)} músicas</span>
    </header>

    <div class="cabecalho">
      <span class="estilo">🎵 Repertório</span>
      <h1>Músicas com Letras</h1>
      <p class="artista">Escolha uma música para abrir a letra</p>
    </div>

    <nav class="lista" aria-label="Lista de músicas">
{lista}
    </nav>

    <footer class="rodape rodape-simples">
      <div class="rodape-texto">
        <a class="link-externo" href="qrcodes/">📱 Folha de QR codes para imprimir</a>
        <p>Projeto <strong>Músicas com Letras</strong><br>SEEDUC — Secretaria de Educação de São Caetano do Sul</p>
      </div>
    </footer>
  </main>
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
    corpo = "\n".join(cartoes)
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
