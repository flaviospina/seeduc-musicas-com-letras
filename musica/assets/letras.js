// musica/assets/letras.js
// ============================================================
// CADASTRO DAS MÚSICAS (título, artista, estilo, cores, link)
//
// AS LETRAS NÃO FICAM AQUI. Elas ficam em arquivos de texto simples na pasta
// musica/letras/, um por música, com o mesmo nome da pasta da música:
//
//   musica/letras/canta-canta-minha-gente.txt
//   musica/letras/stand-by-me.txt
//   musica/letras/stand-by-me.traducao.txt   (opcional: tradução)
//   ...
//
// Basta abrir o .txt no cPanel (Editar) e colar a letra: um verso por linha,
// uma linha em branco entre as estrofes. Sem aspas, sem crases, sem código.
// Se o arquivo não existir ou estiver vazio, a página mostra o link oficial.
//
// Os campos "letra" e "traducao" abaixo são só um fallback: se preenchidos,
// têm prioridade sobre o arquivo .txt. Deixe vazios (``) para usar o .txt.
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
    letra: ``
  }
];
