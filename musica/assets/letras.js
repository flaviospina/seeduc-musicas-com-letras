// musica/assets/letras.js
// ============================================================
// CADASTRO DAS MÚSICAS E LETRAS
//
// Este é o ÚNICO arquivo que precisa ser editado para colocar as letras.
// Todas as páginas (índice e páginas individuais) leem daqui.
//
// Como preencher o campo "letra":
//   - Escreva a letra entre as crases ` ` (acento grave), uma linha por verso.
//   - Separe as estrofes com UMA LINHA EM BRANCO.
//   - Não use crase ( ` ) dentro da letra.
//
// Campo opcional "traducao": mesma regra, usado em músicas em outro idioma
// (aparece um botão para alternar entre original e tradução).
//
// Se "letra" ficar vazia (``), a página mostra um aviso e o link para a
// letra oficial no Letras.mus.br.
// ============================================================

window.MUSICAS = [
  {
    slug: "canta-canta-minha-gente",
    n: 1,
    estilo: "Samba",
    titulo: "Canta, Canta, Minha Gente",
    artista: "Martinho da Vila",
    emoji: "🥁",
    cor: "#f59e0b",
    cor2: "#ef4444",
    link: "https://www.letras.mus.br/martinho-da-vila/287326/",
    letra: ``
  },
  {
    slug: "eu-so-quero-um-xodo",
    n: 2,
    estilo: "Forró",
    titulo: "Eu Só Quero um Xodó",
    artista: "Dominguinhos",
    emoji: "🪗",
    cor: "#f97316",
    cor2: "#eab308",
    link: "https://www.letras.mus.br/dominguinhos/357861/",
    letra: ``
  },
  {
    slug: "estrada-da-vida",
    n: 3,
    estilo: "Caipira / Sertanejo raiz",
    titulo: "Estrada da Vida",
    artista: "Milionário & José Rico",
    emoji: "🎸",
    cor: "#84cc16",
    cor2: "#16a34a",
    link: "https://www.letras.mus.br/milionario-e-jose-rico/47389/",
    letra: ``
  },
  {
    slug: "e-preciso-saber-viver",
    n: 4,
    estilo: "Rock nacional",
    titulo: "É Preciso Saber Viver",
    artista: "Titãs",
    emoji: "🎸",
    cor: "#8b5cf6",
    cor2: "#ec4899",
    link: "https://www.letras.mus.br/titas/48967/",
    letra: ``
  },
  {
    slug: "stand-by-me",
    n: 5,
    estilo: "Rock internacional",
    titulo: "Stand by Me",
    artista: "Ben E. King",
    emoji: "🎤",
    cor: "#3b82f6",
    cor2: "#06b6d4",
    link: "https://www.letras.mus.br/king-ben-e/21189/traducao.html",
    linkTexto: "Ver letra e tradução no Letras.mus.br",
    letra: ``,
    traducao: ``
  },
  {
    slug: "o-sol",
    n: 6,
    estilo: "Pop",
    titulo: "O Sol",
    artista: "Vitor Kley",
    emoji: "☀️",
    cor: "#fbbf24",
    cor2: "#f97316",
    link: "https://www.letras.mus.br/vitor-kley/sol/",
    letra: ``
  },
  {
    slug: "tempos-modernos",
    n: 7,
    estilo: "MPB",
    titulo: "Tempos Modernos",
    artista: "Lulu Santos",
    emoji: "🎹",
    cor: "#14b8a6",
    cor2: "#3b82f6",
    link: "https://www.letras.mus.br/lulu-santos/47144/",
    letra: ``
  },
  {
    slug: "evidencias",
    n: 8,
    estilo: "Sertanejo",
    titulo: "Evidências",
    artista: "Chitãozinho & Xororó",
    emoji: "🤠",
    cor: "#ef4444",
    cor2: "#be185d",
    link: "https://www.letras.mus.br/chitaozinho-e-xororo/768469/",
    letra: ``
  },
  {
    slug: "peneirei-fuba",
    n: 9,
    estilo: "Brincadeira cantada",
    titulo: "Peneirei Fubá",
    artista: "Cantiga popular (domínio público)",
    emoji: "🎶",
    cor: "#22c55e",
    cor2: "#facc15",
    link: "",
    letra: `Peneirou fubá,
O fubá caiu.
Tornei a peneirar,
O fubá subiu.

Lá vêm as famílias,
Todas animadas,
Com a peneira na mão.
Não deixe cair o fubá no chão!

Peneirou fubá,
O fubá caiu.
Tornei a peneirar,
O fubá subiu.`
  }
];
