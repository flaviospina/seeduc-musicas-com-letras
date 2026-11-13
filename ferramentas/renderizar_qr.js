// ferramentas/renderizar_qr.js — rasteriza o QR estilizado (SVG) e o telão em PNG
// Uso: node ferramentas/renderizar_qr.js   (requer playwright + chromium)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const dir = path.resolve(__dirname, '..', 'musica', 'qrcodes');
(async () => {
  const b = await chromium.launch();
  // QR quadrado 2000 px
  const pg = await b.newPage({ viewport: { width: 2000, height: 2000 }, deviceScaleFactor: 1 });
  const svg = fs.readFileSync(path.join(dir, 'geral-estilizado.svg'), 'utf8');
  await pg.setContent(`<html><body style="margin:0;background:#fff"><img src="data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}" style="width:2000px;height:2000px;display:block"></body></html>`);
  await pg.waitForTimeout(300);
  await pg.screenshot({ path: path.join(dir, 'geral-estilizado.png') });
  // Telão 1920x1080 (2x para nitidez = 3840x2160)
  const pg2 = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  await pg2.goto('file://' + path.join(dir, 'telao.html'));
  await pg2.waitForTimeout(1200); // fonte do Google
  await pg2.screenshot({ path: path.join(dir, 'telao.png') });
  await b.close();
  console.log('PNGs gerados em', dir);
})();
