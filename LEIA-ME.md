# Músicas com Letras — SEEDUC São Caetano do Sul

Site estático com logo da SEEDUC, fundo animado com notas musicais, controle de
tamanho de letra, impressão, compartilhamento e QR codes. Publicação em
`https://cecapescs.com.br/seeduc/musica/`.

**Como funciona:** o **QR code geral** abre a página principal, que carrega a
lista de `assets/letras.js` e as letras dos arquivos de texto em `letras/`. Ao tocar em uma música, a letra aparece
na mesma página (endereço muda para `#nome-da-musica`), com botões de música
anterior/próxima e "Todas as músicas". Cada música também tem um endereço e um QR
code próprios (`musica/<pasta>/`), que mostram só aquela letra.

## Estrutura

```
musica/
├── index.html                      ← página principal: lista + letra da música escolhida
├── letras/                         ← ★ AS LETRAS: um .txt por música (texto puro)
│   ├── peneirei-fuba.txt           ← já preenchida
│   ├── canta-canta-minha-gente.txt ← cole a letra aqui (e assim por diante)
│   ├── stand-by-me.traducao.txt    ← tradução (opcional)
│   └── LEIA-ME.txt
├── .htaccess                       ← garante acentuação (UTF-8) nos .txt
├── assets/
│   ├── letras.js                   ← títulos, artistas, cores e links (sem letras)
│   ├── app.js                      ← monta a lista e a letra a partir de letras.js
│   ├── estilo.css                  ← estilo compartilhado por todas as páginas
│   ├── logo-seeduc.png             ← logo oficial da SEEDUC (otimizado)
│   └── favicon.svg
├── qrcodes/
│   ├── index.html                  ← folha com o QR geral + 9 QR codes para imprimir
│   ├── geral.png                   ← QR code GERAL simples (abre a lista de músicas)
│   ├── geral-com-logo.png          ← QR code GERAL com o logo da SEEDUC no centro (1600 px)
│   ├── geral-estilizado.svg/.png   ← QR GERAL estilizado (pontos, curvas, gradiente, logo) — vetor e 2000 px
│   ├── geral-estilizado-1200.png   ← o mesmo em 1200 px (WhatsApp, slides)
│   ├── telao.html / telao.png      ← arte 1920×1080 (PNG em 3840×2160) para o telão da apresentação
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

Cada pasta de música contém `index.html` (página individual, que lê a letra de
`letras/<pasta>.txt`) e `qrcode.png` (aponta para `https://cecapescs.com.br/seeduc/musica/<pasta>/`).

## Como publicar (cPanel, sem terminal)

1. Compacte a pasta `musica` em um arquivo `musica.zip`.
2. No cPanel → **Gerenciador de Arquivos**, entre em `public_html/seeduc`
   (crie a pasta `seeduc` se ainda não existir).
3. Envie o `musica.zip` e use **Extrair**. Deve ficar `public_html/seeduc/musica/index.html`.
4. Teste em `https://cecapescs.com.br/seeduc/musica/` e em uma música, por exemplo
   `https://cecapescs.com.br/seeduc/musica/peneirei-fuba/`.
5. Abra `https://cecapescs.com.br/seeduc/musica/qrcodes/` e clique em **Imprimir folha**
   para gerar os cartões: o **QR geral** (lista completa) e um por música.

Os QR codes só funcionam depois da publicação, pois apontam para o domínio.

## Logo oficial

`musica/assets/logo-seeduc.png` é o logo oficial da Secretaria de Educação
(baixado de cecapescs.com.br/logos/logo-seeduc.png), convertido de JPEG CMYK
para PNG com fundo transparente, 640 px de largura e sem perfil de cor (ficou
com cerca de 21 KB em vez de 1,2 MB). Para trocar o logo, substitua o arquivo
mantendo o mesmo nome. Todas as páginas e a folha de QR codes usam esse arquivo.

## Letras das músicas (como cadastrar)

Cada música tem um arquivo de texto em **`musica/letras/`** com o mesmo nome da
pasta da música (ex.: `musica/letras/evidencias.txt`). Não há código nenhum
nesses arquivos: é só o texto da letra.

1. No cPanel → Gerenciador de Arquivos → `public_html/seeduc/musica/letras/`.
2. Selecione o `.txt` da música e clique em **Editar** (codificação `utf-8`).
3. Cole a letra: um verso por linha, uma linha em branco entre as estrofes.
4. Salve. Recarregue a página da música: a letra aparece na página principal e
   na página individual. Nada mais precisa ser alterado.

- **Peneirei Fubá** (cantiga popular, domínio público) já está preenchida.
- Os demais `.txt` estão vazios. Enquanto estiverem vazios, a página mostra o
  botão "Ver letra completa no Letras.mus.br" com o link oficial e a lista marca
  "letra no site oficial". A decisão de publicar as letras protegidas, com base
  na finalidade educacional e sem fins comerciais, é da Secretaria.
- **Stand by Me**: cole o original em `stand-by-me.txt` e a tradução em
  `stand-by-me.traducao.txt`. Aparece o botão "Ver tradução".
- As páginas pedem o `.txt` sem cache, então a alteração aparece na hora.

## Alterar cores, textos ou músicas

- Cores e visual: `musica/assets/estilo.css`. Cada página define `--cor` e
  `--cor2` (as duas cores do gradiente) no `<style>` do `<head>`.
- Título, artista, estilo, emoji, cores e link de cada música: `musica/assets/letras.js`.
- Para regenerar tudo de uma vez (inclusive QR codes), em um computador com
  Python: `pip install segno pillow` e `python3 ferramentas/gerar_paginas.py`.
  O script não sobrescreve `logo-seeduc.png` se o arquivo já existir.
