# Músicas com Letras — SEEDUC São Caetano do Sul

Site estático com logo da SEEDUC, fundo animado com notas musicais, controle de
tamanho de letra, impressão, compartilhamento e QR codes. Publicação em
`https://cecapescs.com.br/musica/`.

**Como funciona:** o **QR code geral** abre a página principal, que carrega todas
as músicas do arquivo `assets/letras.js`. Ao tocar em uma música, a letra aparece
na mesma página (endereço muda para `#nome-da-musica`), com botões de música
anterior/próxima e "Todas as músicas". Cada música também tem um endereço e um QR
code próprios (`musica/<pasta>/`), que mostram só aquela letra.

## Estrutura

```
musica/
├── index.html                      ← página principal: lista + letra da música escolhida
├── assets/
│   ├── letras.js                   ← ★ ÚNICO ARQUIVO A EDITAR: títulos, links e LETRAS
│   ├── app.js                      ← monta a lista e a letra a partir de letras.js
│   ├── estilo.css                  ← estilo compartilhado por todas as páginas
│   ├── logo-seeduc.png             ← LOGO (ver "Logo oficial" abaixo)
│   └── favicon.svg
├── qrcodes/
│   ├── index.html                  ← folha com o QR geral + 9 QR codes para imprimir
│   ├── geral.png                   ← QR code GERAL (abre a lista de músicas)
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
`assets/letras.js`) e `qrcode.png` (aponta para `https://cecapescs.com.br/musica/<pasta>/`).

## Como publicar (cPanel, sem terminal)

1. Compacte a pasta `musica` em um arquivo `musica.zip`.
2. No cPanel → **Gerenciador de Arquivos**, entre em `public_html` (raiz do
   domínio `cecapescs.com.br`).
3. Envie o `musica.zip` e use **Extrair**. Deve ficar `public_html/musica/index.html`.
4. Teste em `https://cecapescs.com.br/musica/` e em uma música, por exemplo
   `https://cecapescs.com.br/musica/peneirei-fuba/`.
5. Abra `https://cecapescs.com.br/musica/qrcodes/` e clique em **Imprimir folha**
   para gerar os cartões: o **QR geral** (lista completa) e um por música.

Os QR codes só funcionam depois da publicação, pois apontam para o domínio.

## Logo oficial

O arquivo `musica/assets/logo-seeduc.png` é um **logo provisório** gerado
automaticamente. Substitua pelo logo oficial da SEEDUC mantendo o mesmo nome
de arquivo (`logo-seeduc.png`, de preferência com fundo transparente e largura
mínima de 600 px). Todas as páginas e a folha de QR codes usam esse único arquivo.

## Letras das músicas (como cadastrar)

Todas as letras ficam em **`musica/assets/letras.js`**. No cPanel, abra o arquivo
com **Editar** (Gerenciador de Arquivos), localize a música e cole a letra entre as
crases do campo `letra`:

```js
letra: `Primeiro verso da estrofe 1
Segundo verso da estrofe 1

Primeiro verso da estrofe 2
Segundo verso da estrofe 2`
```

Regras: um verso por linha, uma linha em branco entre estrofes, e não usar o
caractere crase ( ` ) dentro da letra. Salve e recarregue a página: a letra
aparece na página principal e na página individual, sem mais nada a fazer.

- **Peneirei Fubá** (cantiga popular, domínio público) já está preenchida.
- As demais músicas estão com `letra` vazia. Enquanto estiverem vazias, a página
  mostra o botão "Ver letra completa no Letras.mus.br" com o link oficial. A
  decisão de publicar as letras protegidas, com base na finalidade educacional
  e sem fins comerciais, é da Secretaria; o site já está preparado para isso.
- **Stand by Me** tem também o campo `traducao`: preenchido, aparece o botão
  "Ver tradução" que alterna entre original e tradução.

## Alterar cores, textos ou músicas

- Cores e visual: `musica/assets/estilo.css`. Cada página define `--cor` e
  `--cor2` (as duas cores do gradiente) no `<style>` do `<head>`.
- Título, artista, estilo, emoji, cores e link de cada música: `musica/assets/letras.js`.
- Para regenerar tudo de uma vez (inclusive QR codes), em um computador com
  Python: `pip install segno pillow` e `python3 ferramentas/gerar_paginas.py`.
  O script não sobrescreve `logo-seeduc.png` se o arquivo já existir.
