// musica/assets/app.js
// Lógica compartilhada: lista de músicas, exibição da letra, tradução,
// navegação anterior/próxima, tamanho da fonte e compartilhamento.
// Os dados vêm de assets/letras.js (window.MUSICAS).

(function () {
  'use strict';

  var MUSICAS = window.MUSICAS || [];
  var BASE_URL = 'https://cecapescs.com.br/seeduc/musica/';

  // ---------- utilidades ----------
  function esc(txt) {
    return String(txt)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // Converte o texto da letra (estrofes separadas por linha em branco) em HTML
  function letraParaHtml(texto) {
    var estrofes = String(texto || '').trim().split(/\n\s*\n/);
    return estrofes.map(function (e) {
      var versos = e.split('\n').map(function (v) { return esc(v.trim()); });
      return '<p>' + versos.join('<br>') + '</p>';
    }).join('\n');
  }

  function porSlug(slug) {
    for (var i = 0; i < MUSICAS.length; i++) {
      if (MUSICAS[i].slug === slug) return MUSICAS[i];
    }
    return null;
  }

  function aplicarCores(m) {
    var r = document.documentElement.style;
    r.setProperty('--cor', m ? m.cor : '#2563eb');
    r.setProperty('--cor2', m ? m.cor2 : '#ec4899');
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', m ? m.cor : '#2563eb');
  }

  // ---------- tamanho da letra ----------
  var tamanho = Number(localStorage.getItem('tamanhoLetra') || 0);
  function aplicarFonte() {
    document.documentElement.style.setProperty('--escala', (1 + tamanho * 0.15).toFixed(2));
    localStorage.setItem('tamanhoLetra', tamanho);
  }
  window.mudarFonte = function (delta) {
    tamanho = Math.max(-2, Math.min(4, tamanho + delta));
    aplicarFonte();
  };
  aplicarFonte();

  // ---------- compartilhar ----------
  window.compartilhar = function (titulo, url) {
    var dados = { title: document.title, text: titulo, url: url };
    if (navigator.share) {
      navigator.share(dados).catch(function () {});
    } else if (navigator.clipboard) {
      navigator.clipboard.writeText(url).then(function () { alert('Link copiado: ' + url); });
    } else {
      prompt('Copie o link desta página:', url);
    }
  };

  // ---------- tradução ----------
  window.alternarTraducao = function (btn) {
    var sec = btn.closest('.bloco-letra');
    var mostrandoTraducao = sec.classList.toggle('mostrar-traducao');
    btn.textContent = mostrandoTraducao ? '🎤 Ver original' : '🇧🇷 Ver tradução';
  };

  // ---------- HTML da letra ----------
  function htmlLetra(m) {
    var temLetra = m.letra && m.letra.trim().length > 0;
    var temTrad = m.traducao && m.traducao.trim().length > 0;
    var linkTexto = m.linkTexto || 'Ver letra completa no Letras.mus.br';

    if (!temLetra) {
      return (
        '<section class="letra letra-externa" aria-label="Letra da música">' +
          '<div class="aviso-letra">' +
            '<div class="aviso-icone">' + m.emoji + '</div>' +
            '<p>A letra desta música ainda não foi cadastrada.<br>' +
            'Toque no botão para abrir a letra oficial e cantar junto!</p>' +
            (m.link ? '<a class="botao" href="' + esc(m.link) + '" target="_blank" rel="noopener">' + esc(linkTexto) + ' ↗</a>' : '') +
            '<p class="dica-admin">Para cadastrar, edite o campo <code>letra</code> em <code>assets/letras.js</code>.</p>' +
          '</div>' +
        '</section>'
      );
    }

    var h = '<div class="bloco-letra">';
    if (temTrad) {
      h += '<div class="ferramentas"><button type="button" onclick="alternarTraducao(this)">🇧🇷 Ver tradução</button></div>';
    }
    h += '<section class="letra letra-original" aria-label="Letra da música">' + letraParaHtml(m.letra) + '</section>';
    if (temTrad) {
      h += '<section class="letra letra-traducao" aria-label="Tradução da letra">' + letraParaHtml(m.traducao) + '</section>';
    }
    h += '</div>';
    return h;
  }

  // ---------- HTML de uma música completa ----------
  function htmlMusica(m, opcoes) {
    opcoes = opcoes || {};
    var url = BASE_URL + m.slug + '/';
    var idx = MUSICAS.indexOf(m);
    var ant = MUSICAS[idx - 1];
    var prox = MUSICAS[idx + 1];
    var prefixo = opcoes.prefixo || '';  // '' no índice, '../' nas páginas individuais
    var hrefMusica = function (x) { return opcoes.modoIndice ? '#' + x.slug : prefixo + x.slug + '/'; };
    var linkTexto = m.linkTexto || 'Ver letra completa no Letras.mus.br';

    var h = '';
    if (opcoes.modoIndice) {
      h += '<a class="voltar" href="#">‹ Todas as músicas</a>';
    }
    h +=
      '<div class="cabecalho">' +
        '<span class="estilo">' + m.emoji + ' ' + esc(m.estilo) + '</span>' +
        '<h1>' + esc(m.titulo) + '</h1>' +
        '<p class="artista">' + esc(m.artista) + '</p>' +
      '</div>' +
      '<div class="ferramentas" role="toolbar" aria-label="Opções de leitura">' +
        '<button type="button" onclick="mudarFonte(-1)" title="Diminuir letra">A−</button>' +
        '<button type="button" onclick="mudarFonte(1)" title="Aumentar letra">A+</button>' +
        '<button type="button" onclick="window.print()" title="Imprimir">🖨️ Imprimir</button>' +
        '<button type="button" onclick="compartilhar(\'' + esc(m.titulo + ' — ' + m.artista).replace(/'/g, "\\'") + '\', \'' + url + '\')" title="Compartilhar">📤 Compartilhar</button>' +
      '</div>' +
      htmlLetra(m) +
      '<nav class="navegacao" aria-label="Outras músicas">' +
        (ant ? '<a href="' + hrefMusica(ant) + '" class="nav-btn">‹ ' + esc(ant.titulo) + '</a>' : '<span></span>') +
        (prox ? '<a href="' + hrefMusica(prox) + '" class="nav-btn nav-prox">' + esc(prox.titulo) + ' ›</a>' : '<span></span>') +
      '</nav>' +
      '<footer class="rodape">' +
        '<div class="qr">' +
          '<img src="' + prefixo + 'qrcodes/' + m.slug + '.png" alt="QR Code desta música" width="120" height="120">' +
          '<small>Aponte a câmera para abrir esta música</small>' +
        '</div>' +
        '<div class="rodape-texto">' +
          (m.link ? '<a class="link-externo" href="' + esc(m.link) + '" target="_blank" rel="noopener">' + esc(linkTexto) + ' ↗</a>' : '') +
          '<a class="link-externo" href="' + (opcoes.modoIndice ? '#' : prefixo) + '">🎵 Todas as músicas</a>' +
          '<p>Projeto <strong>Músicas com Letras</strong><br>SEEDUC — Secretaria de Educação de São Caetano do Sul</p>' +
        '</div>' +
      '</footer>';
    return h;
  }

  // ---------- HTML da lista ----------
  function htmlLista() {
    var h =
      '<div class="cabecalho">' +
        '<span class="estilo">🎵 Repertório</span>' +
        '<h1>Músicas com Letras</h1>' +
        '<p class="artista">Toque em uma música para ver a letra</p>' +
      '</div>' +
      '<nav class="lista" aria-label="Lista de músicas">';
    MUSICAS.forEach(function (m) {
      var temLetra = m.letra && m.letra.trim().length > 0;
      h +=
        '<a class="item" href="#' + m.slug + '" style="--cor:' + m.cor + ';--cor2:' + m.cor2 + ';">' +
          '<span class="num">' + m.n + '</span>' +
          '<span class="emoji">' + m.emoji + '</span>' +
          '<span class="info">' +
            '<strong>' + esc(m.titulo) + '</strong>' +
            '<span>' + esc(m.artista) + '</span>' +
            '<em>' + esc(m.estilo) + (temLetra ? '' : ' · letra no site oficial') + '</em>' +
          '</span>' +
          '<span class="seta">›</span>' +
        '</a>';
    });
    h +=
      '</nav>' +
      '<footer class="rodape">' +
        '<div class="qr">' +
          '<img src="qrcodes/geral-com-logo.png" alt="QR Code geral do repertório" width="120" height="120">' +
          '<small>QR code geral: abre esta lista</small>' +
        '</div>' +
        '<div class="rodape-texto">' +
          '<a class="link-externo" href="qrcodes/">📱 Folha de QR codes para imprimir</a>' +
          '<p>Projeto <strong>Músicas com Letras</strong><br>SEEDUC — Secretaria de Educação de São Caetano do Sul</p>' +
        '</div>' +
      '</footer>';
    return h;
  }

  // ---------- montagem do índice (lista + letra na mesma página) ----------
  window.montarIndice = function (containerId) {
    var el = document.getElementById(containerId);
    function render() {
      var slug = decodeURIComponent(location.hash.replace(/^#/, ''));
      var m = slug ? porSlug(slug) : null;
      var selo = document.getElementById('selo');
      if (m) {
        aplicarCores(m);
        document.title = m.titulo + ' — ' + m.artista + ' | Músicas SEEDUC';
        if (selo) selo.textContent = 'Música ' + m.n + ' de ' + MUSICAS.length;
        el.innerHTML = htmlMusica(m, { modoIndice: true, prefixo: '' });
      } else {
        aplicarCores(null);
        document.title = 'Músicas com Letras | SEEDUC São Caetano do Sul';
        if (selo) selo.textContent = MUSICAS.length + ' músicas';
        el.innerHTML = htmlLista();
      }
      el.classList.remove('trocando');
      void el.offsetWidth;          // reinicia a animação de entrada
      el.classList.add('trocando');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    window.addEventListener('hashchange', render);
    render();
  };

  // ---------- montagem de uma página individual ----------
  window.montarPagina = function (containerId, slug) {
    var el = document.getElementById(containerId);
    var m = porSlug(slug);
    if (!m) {
      el.innerHTML = '<p class="aviso-letra">Música não encontrada. <a href="../">Voltar à lista</a>.</p>';
      return;
    }
    aplicarCores(m);
    document.title = m.titulo + ' — ' + m.artista + ' | Músicas SEEDUC';
    var selo = document.getElementById('selo');
    if (selo) selo.textContent = 'Música ' + m.n + ' de ' + MUSICAS.length;
    el.innerHTML = htmlMusica(m, { modoIndice: false, prefixo: '../' });
  };
})();
