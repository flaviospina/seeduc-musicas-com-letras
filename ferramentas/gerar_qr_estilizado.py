#!/usr/bin/env python3
# ferramentas/gerar_qr_estilizado.py
# Gera o QR code estilizado (pontos e curvas, gradiente colorido, logo no centro)
# em SVG, e uma arte 1920x1080 para telão (HTML). A rasterização em PNG e a
# verificação de leitura são feitas por ferramentas/renderizar_qr.js.
import base64
from pathlib import Path
import segno

RAIZ = Path(__file__).resolve().parent.parent
URL = "https://cecapescs.com.br/seeduc/musica/"
SAIDA = RAIZ / "musica" / "qrcodes"
LOGO = RAIZ / "musica" / "assets" / "logo-seeduc.png"

qr = segno.make(URL, error="h")
matriz = [list(linha) for linha in qr.matrix]
N = len(matriz)
BORDA = 2
M = 10                      # tamanho de um módulo em unidades SVG
TAM = (N + 2 * BORDA) * M   # lado total

def escuro(r, c):
    return 0 <= r < N and 0 <= c < N and matriz[r][c] == 1

def eh_finder(r, c):
    return (r < 7 and c < 7) or (r < 7 and c >= N - 7) or (r >= N - 7 and c < 7)

# Zona do logo (centro): módulos cobertos não são desenhados (correção H aguenta ~30%)
LOGO_MODS = round(N * 0.26)
if LOGO_MODS % 2 != N % 2:
    LOGO_MODS += 1
ini_logo = (N - LOGO_MODS) // 2
fim_logo = ini_logo + LOGO_MODS

def no_logo(r, c):
    return ini_logo <= r < fim_logo and ini_logo <= c < fim_logo

def pos(i):
    return (i + BORDA) * M

partes = []
raio = M * 0.50          # raio dos pontos (0.5 = pontos encostados: leitura confiável)
lig = M * 1.00           # espessura das ligações entre pontos vizinhos (formam as curvas)

# ligações horizontais e verticais entre pontos vizinhos (formam as "curvas")
for r in range(N):
    for c in range(N):
        if not escuro(r, c) or eh_finder(r, c) or no_logo(r, c):
            continue
        x, y = pos(c) + M / 2, pos(r) + M / 2
        if escuro(r, c + 1) and not eh_finder(r, c + 1) and not no_logo(r, c + 1):
            partes.append(f'<rect x="{x:.1f}" y="{y - lig / 2:.1f}" width="{M}" height="{lig:.1f}" rx="{lig / 2:.1f}"/>')
        if escuro(r + 1, c) and not eh_finder(r + 1, c) and not no_logo(r + 1, c):
            partes.append(f'<rect x="{x - lig / 2:.1f}" y="{y:.1f}" width="{lig:.1f}" height="{M}" rx="{lig / 2:.1f}"/>')
# pontos
for r in range(N):
    for c in range(N):
        if escuro(r, c) and not eh_finder(r, c) and not no_logo(r, c):
            partes.append(f'<circle cx="{pos(c) + M / 2:.1f}" cy="{pos(r) + M / 2:.1f}" r="{raio:.1f}"/>')

# padrões de localização (os três cantos): anel arredondado + miolo arredondado
# Raios testados com jsQR e OpenCV: 1.5 / 0.8 / 0.8 módulos leem em todos os tamanhos.
def finder(r0, c0):
    x, y = pos(c0), pos(r0)
    return (f'<rect x="{x}" y="{y}" width="{7 * M}" height="{7 * M}" rx="{1.5 * M}"/>'
            f'<rect x="{x + M}" y="{y + M}" width="{5 * M}" height="{5 * M}" rx="{0.8 * M}" fill="#fff"/>'
            f'<rect x="{x + 2 * M}" y="{y + 2 * M}" width="{3 * M}" height="{3 * M}" rx="{0.8 * M}"/>')
finders = finder(0, 0) + finder(0, N - 7) + finder(N - 7, 0)

logo_b64 = base64.b64encode(LOGO.read_bytes()).decode()
lx = pos(ini_logo); ls = LOGO_MODS * M
caixa = (f'<rect x="{lx}" y="{lx}" width="{ls}" height="{ls}" rx="{ls * 0.18:.1f}" fill="#fff" stroke="url(#g)" stroke-width="{M * 0.45:.1f}"/>'
         f'<image href="data:image/png;base64,{logo_b64}" x="{lx + ls * 0.09:.1f}" y="{lx + ls * 0.09:.1f}" width="{ls * 0.82:.1f}" height="{ls * 0.82:.1f}" preserveAspectRatio="xMidYMid meet"/>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TAM} {TAM}" width="{TAM}" height="{TAM}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#1d4ed8"/>
      <stop offset="0.5" stop-color="#7c3aed"/>
      <stop offset="1" stop-color="#db2777"/>
    </linearGradient>
  </defs>
  <rect width="{TAM}" height="{TAM}" rx="{M * 3}" fill="#ffffff"/>
  <g fill="url(#g)">
    {finders}
    {"".join(partes)}
  </g>
  {caixa}
</svg>
'''
(SAIDA / "geral-estilizado.svg").write_text(svg, encoding="utf-8")
print("SVG:", SAIDA / "geral-estilizado.svg", f"({N}x{N} módulos, logo cobre {LOGO_MODS}x{LOGO_MODS})")

# Arte para telão 1920x1080
svg_b64 = base64.b64encode(svg.encode("utf-8")).decode()
telao = f'''<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><title>QR Telão</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;900&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; box-sizing:border-box; }}
  body {{ width:1920px; height:1080px; overflow:hidden; font-family:'Nunito',sans-serif; color:#fff; position:relative;
    background: radial-gradient(circle at 12% 15%, rgba(255,255,255,.28) 0, transparent 40%),
                radial-gradient(circle at 88% 85%, rgba(255,255,255,.22) 0, transparent 40%),
                linear-gradient(135deg,#1d4ed8 0%,#7c3aed 50%,#db2777 100%); }}
  .nota {{ position:absolute; color:rgba(255,255,255,.28); font-size:120px; text-shadow:0 10px 30px rgba(0,0,0,.15); }}
  .cartao {{ position:absolute; left:120px; top:120px; width:840px; height:840px; background:#fff; border-radius:60px;
    box-shadow:0 40px 100px rgba(15,23,42,.35); padding:50px; }}
  .cartao img {{ width:100%; height:100%; display:block; }}
  .texto {{ position:absolute; left:1060px; top:0; height:1080px; width:760px; display:flex; flex-direction:column; justify-content:center; gap:28px; }}
  .logo {{ background:#fff; border-radius:28px; padding:18px 26px; width:fit-content; }}
  .logo img {{ height:150px; display:block; }}
  h1 {{ font-size:92px; font-weight:900; line-height:1; letter-spacing:-1px; text-shadow:0 8px 30px rgba(0,0,0,.25); }}
  h2 {{ font-size:40px; font-weight:700; opacity:.95; }}
  .chamada {{ margin-top:12px; background:rgba(255,255,255,.18); border:3px solid rgba(255,255,255,.55); border-radius:999px; padding:18px 34px; font-size:34px; font-weight:800; width:fit-content; backdrop-filter:blur(6px); }}
  .url {{ font-size:30px; font-weight:700; opacity:.9; letter-spacing:.5px; }}
</style></head><body>
  <span class="nota" style="left:1000px;top:40px;font-size:150px;transform:rotate(-15deg)">♪</span>
  <span class="nota" style="left:1760px;top:120px;transform:rotate(12deg)">♫</span>
  <span class="nota" style="left:1020px;top:880px;font-size:140px;transform:rotate(8deg)">♬</span>
  <span class="nota" style="left:1780px;top:860px;font-size:110px;transform:rotate(-10deg)">♩</span>
  <span class="nota" style="left:30px;top:960px;font-size:90px;transform:rotate(-20deg)">♪</span>
  <span class="nota" style="left:30px;top:20px;font-size:90px;transform:rotate(15deg)">♫</span>
  <div class="cartao"><img src="data:image/svg+xml;base64,{svg_b64}" alt="QR code"></div>
  <div class="texto">
    <div class="logo"><img src="data:image/png;base64,{logo_b64}" alt="SEEDUC"></div>
    <h1>Músicas<br>com Letras</h1>
    <h2>Cante junto com a gente!</h2>
    <div class="chamada">📱 Aponte a câmera para o QR code</div>
    <div class="url">cecapescs.com.br/seeduc/musica</div>
  </div>
</body></html>
'''
(SAIDA / "telao.html").write_text(telao, encoding="utf-8")
print("Telão:", SAIDA / "telao.html")
