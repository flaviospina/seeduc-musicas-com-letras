# Músicas com Letras — SEEDUC São Caetano do Sul

Páginas HTML estáticas (uma por música) com logo da SEEDUC, fundo animado com
notas musicais, controle de tamanho de letra, botão de impressão, botão de
compartilhar e QR code de acesso. Publicação em `https://cecapescs.com.br/musica/`.

## Estrutura

```
musica/
├── index.html                      ← lista das 9 músicas
├── assets/
│   ├── estilo.css                  ← estilo compartilhado por todas as páginas
│   ├── logo-seeduc.png             ← LOGO (ver "Logo oficial" abaixo)
│   └── favicon.svg
├── qrcodes/
│   ├── index.html                  ← folha com os 9 QR codes para imprimir/recortar
│   └── <musica>.png                ← um PNG de QR code por música
├── canta-canta-minha-gente/        ← 1. Samba — Martinho da Vila
├── eu-so-quero-um-xodo/            ← 2. Forró — Dominguinhos
├── estrada-da-vida/                ← 3. Caipira / Sertanejo raiz — Milionário & José Rico
├── e-preciso-saber-viver/          ← 4. Rock nacional — Titãs
├── stand-by-me/                    ← 5. Rock internacional — Ben E. King
├── o-sol/                          ← 6. Pop — Vitor Kley
├── tempos-modernos/                ← 7. MPB — Lulu Santos
├── evidencias/                     ← 8. Sertanejo — Chitãozinho & Xororó
└── peneirei-fuba/                  ← 9. Brincadeira cantada — cantiga popular
    ├── index.html
    └── qrcode.png
```

Cada pasta de música contém `index.html` (a página) e `qrcode.png` (QR code que
aponta para `https://cecapescs.com.br/musica/<pasta>/`).

## Como publicar (cPanel, sem terminal)

1. Compacte a pasta `musica` em um arquivo `musica.zip`.
2. No cPanel → **Gerenciador de Arquivos**, entre em `public_html` (raiz do
   domínio `cecapescs.com.br`).
3. Envie o `musica.zip` e use **Extrair**. Deve ficar `public_html/musica/index.html`.
4. Teste em `https://cecapescs.com.br/musica/` e em uma música, por exemplo
   `https://cecapescs.com.br/musica/peneirei-fuba/`.
5. Abra `https://cecapescs.com.br/musica/qrcodes/` e clique em **Imprimir folha**
   para gerar os cartões com QR code.

Os QR codes só funcionam depois da publicação, pois apontam para o domínio.

## Logo oficial

O arquivo `musica/assets/logo-seeduc.png` é um **logo provisório** gerado
automaticamente. Substitua pelo logo oficial da SEEDUC mantendo o mesmo nome
de arquivo (`logo-seeduc.png`, de preferência com fundo transparente e largura
mínima de 600 px). Todas as páginas e a folha de QR codes usam esse único arquivo.

## Letras das músicas

- **Peneirei Fubá** (cantiga popular, domínio público): letra completa na página,
  na versão enviada.
- **Demais músicas** (protegidas por direitos autorais): a letra **não** foi
  incluída. A página mostra um botão "Ver letra completa no Letras.mus.br"
  (e "Ver letra e tradução" no caso de Stand by Me) que abre a letra oficial.
  Se a escola tiver autorização para publicar a letra, abra o `index.html` da
  música no editor do cPanel: dentro de `<section class="letra ...">` há um
  comentário explicando onde colar a letra (um `<p>` por estrofe, `<br>` entre
  os versos). Ao colar, apague o bloco `<div class="aviso-letra">`.

## Alterar cores, textos ou músicas

- Cores e visual: `musica/assets/estilo.css`. Cada página define `--cor` e
  `--cor2` (as duas cores do gradiente) no `<style>` do `<head>`.
- Para trocar título, artista ou link de uma música, edite o `index.html` da
  pasta correspondente.
- Para regenerar tudo de uma vez (inclusive QR codes), em um computador com
  Python: `pip install segno pillow` e `python3 ferramentas/gerar_paginas.py`.
  O script não sobrescreve `logo-seeduc.png` se o arquivo já existir.
