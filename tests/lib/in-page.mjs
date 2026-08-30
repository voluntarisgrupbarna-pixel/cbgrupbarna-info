// Tot el que s'executa DINS del navegador. S'injecta com a text amb
// page.evaluate, per això és una funció sola i sense dependències.

export function collect(opts) {
  const MIN_TAP = opts.minTap;          // px, mida mínima de zona tocable
  const MIN_FONT = opts.minFont;        // px, mida mínima de text llegible
  const CONTRAST_TEXT = opts.contrastText;   // 4.5 per a text normal
  const CONTRAST_LARGE = opts.contrastLarge; // 3.0 per a text gran
  const dpr = window.devicePixelRatio || 1;
  const out = {
    overflow: null,
    tapTargets: [],
    smallText: [],
    contrast: [],
    images: { upscaled: [], noAlt: [], noDims: [], broken: [], oversized: [] },
    headings: { h1: 0, order: [], skips: [] },
    duplicateIds: [],
    unnamed: [],
    landmarks: {},
    viewportMeta: null,
    focus: [],
    tables: [],
    stats: {},
    palette: [],
  };

  const vw = window.innerWidth;

  // Un element és visible si ell i TOTS els seus pares ho són. Mirar només
  // l'element enganya: els fills d'un panell amb opacity:0 diuen opacity:1
  // cadascun, i el panell tancat del xat es colava a totes les llistes.
  const visible = (el) => {
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') return false;
      if (n.hasAttribute('hidden') || n.getAttribute('aria-hidden') === 'true') return false;
      if (cs.contentVisibility === 'hidden') return false;
    }
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };

  // Text propi de l'element, no el dels seus fills.
  const hasOwnText = (el) => {
    for (const n of el.childNodes) {
      if (n.nodeType === 3 && n.textContent.trim().length > 1) return true;
    }
    return false;
  };

  const where = (el) => {
    const id = el.id ? `#${el.id}` : '';
    const cls = typeof el.className === 'string' && el.className
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.')
      : '';
    const txt = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
    return `${el.tagName.toLowerCase()}${id}${cls}${txt ? ` «${txt}»` : ''}`;
  };

  // ---------- desbordament horitzontal ----------
  const docW = document.documentElement.scrollWidth;
  if (docW > vw + 1) {
    const guilty = [];
    for (const el of document.querySelectorAll('body *')) {
      if (!visible(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.right > vw + 1 || r.left < -1) {
        const cs = getComputedStyle(el);
        // Només culpem el que desborda per si mateix, no els seus pares.
        if (el.scrollWidth <= el.clientWidth + 1 || cs.overflowX === 'visible') {
          guilty.push({ el: where(el), right: Math.round(r.right), left: Math.round(r.left), width: Math.round(r.width) });
        }
      }
      if (guilty.length > 12) break;
    }
    out.overflow = { docWidth: docW, viewport: vw, excess: docW - vw, elements: guilty };
  }

  // ---------- zones tocables ----------
  const interactive = document.querySelectorAll(
    'a[href], button, input:not([type=hidden]), select, textarea, summary, [role=button], [role=link], [tabindex]:not([tabindex="-1"])'
  );
  const seenTap = new Set();
  for (const el of interactive) {
    if (!visible(el)) continue;
    let r = el.getBoundingClientRect();
    // Una casella d'1×1 amb una etiqueta gran al costat es toca per l'etiqueta:
    // la zona real és la unió de totes dues.
    if (/^(input|select|textarea)$/.test(el.tagName.toLowerCase())) {
      // Dues formes d'associar una etiqueta, i totes dues fan de zona tocable:
      // label[for=id] al costat, o un <label> que embolcalla el camp.
      const lab = (el.id && document.querySelector(`label[for="${CSS.escape(el.id)}"]`))
        || el.closest('label');
      if (lab && visible(lab)) {
        const lr = lab.getBoundingClientRect();
        r = {
          width: Math.max(r.right, lr.right) - Math.min(r.left, lr.left),
          height: Math.max(r.bottom, lr.bottom) - Math.min(r.top, lr.top),
          top: Math.min(r.top, lr.top),
        };
      }
    }
    const w = r.width, h = r.height;
    if (w >= MIN_TAP && h >= MIN_TAP) continue;
    const key = where(el) + Math.round(r.top);
    if (seenTap.has(key)) continue;
    seenTap.add(key);
    out.tapTargets.push({ el: where(el), w: Math.round(w), h: Math.round(h) });
  }
  out.tapTargets.sort((a, b) => a.w * a.h - b.w * b.h);
  out.tapTargetsTotal = out.tapTargets.length;
  out.tapTargets = out.tapTargets.slice(0, 25);

  // ---------- coses tapades per altres coses ----------
  // Un botó que existeix però que en queda a sota d'una barra fixa no es pot
  // prémer. Ho comprovem preguntant qui hi ha realment en aquell punt.
  out.occluded = [];
  const vh = window.innerHeight;

  // Una capa que tapa gairebé tota la pantalla és una finestra modal o una
  // pantalla d'accés: tapar-ho tot és exactament la seva feina.
  const isOverlay = (node) => {
    for (let n = node; n && n !== document.body; n = n.parentElement) {
      if (n.getAttribute('role') === 'dialog' || n.getAttribute('aria-modal') === 'true') return true;
      const cs = getComputedStyle(n);
      if (cs.position === 'fixed' || cs.position === 'absolute') {
        const nr = n.getBoundingClientRect();
        if (nr.width * nr.height > vw * vh * 0.7) return true;
      }
    }
    return false;
  };

  for (const el of interactive) {
    if (!visible(el)) continue;
    const r = el.getBoundingClientRect();
    // Només els que caben sencers a la pantalla: si en surt una part, el punt
    // de prova cauria fora i acusaríem el veí.
    if (r.top < 0 || r.left < 0 || r.bottom > vh || r.right > vw) continue;
    if (r.width < 4 || r.height < 4) continue;

    // Cinc punts: el centre i quatre cantonades cap endins. Si tots cinc
    // responen a un altre element, l'original no es pot prémer enlloc.
    const ix = Math.max(1, Math.min(r.width / 4, 8));
    const iy = Math.max(1, Math.min(r.height / 4, 8));
    const probes = [
      [r.left + r.width / 2, r.top + r.height / 2],
      [r.left + ix, r.top + iy], [r.right - ix, r.top + iy],
      [r.left + ix, r.bottom - iy], [r.right - ix, r.bottom - iy],
    ];
    let blocked = 0, culprit = null;
    for (const [x, y] of probes) {
      const hit = document.elementFromPoint(x, y);
      if (!hit || hit === el || el.contains(hit) || hit.contains(el)) continue;
      // L'etiqueta d'un camp és el seu destí de clic legítim.
      if (hit.tagName === 'LABEL' && el.id && hit.getAttribute('for') === el.id) continue;
      if (isOverlay(hit)) { blocked = 0; break; }
      blocked++;
      culprit = culprit || hit;
    }
    if (blocked === probes.length) {
      out.occluded.push({ el: where(el), tapat_per: where(culprit), cobreix: 100 });
    }
    if (out.occluded.length > 15) break;
  }

  // Nota: aquí hi va haver una prova de col·lisions (text damunt de text) que
  // s'ha retirat. Donava 133 avisos en només 4 pàgines perquè tot el que hi ha
  // dins d'una capçalera enganxada té les coordenades de la finestra i
  // "trepitja" el que passa per sota en fer scroll. Un test que crida el llop
  // 133 vegades fa que ningú miri la 134a. El solapament de la capçalera a
  // partir de 1366 px es va trobar amb les captures i està a l'informe.

  // ---------- text: mida i contrast ----------
  const luminance = (r, g, b) => {
    const f = (c) => {
      c /= 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const parseColor = (str) => {
    const m = str.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(/[\s,/]+/).filter(Boolean).map(Number);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  };
  const over = (fg, bg) => ({
    r: fg.r * fg.a + bg.r * (1 - fg.a),
    g: fg.g * fg.a + bg.g * (1 - fg.a),
    b: fg.b * fg.a + bg.b * (1 - fg.a),
    a: 1,
  });
  const bgOf = (el) => {
    let node = el;
    let stack = [];
    while (node && node !== document.documentElement.parentNode) {
      const cs = getComputedStyle(node);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return { unknown: true };
      const c = parseColor(cs.backgroundColor);
      if (c && c.a > 0) {
        stack.push(c);
        if (c.a === 1) break;
      }
      node = node.parentElement;
    }
    let base = { r: 255, g: 255, b: 255, a: 1 };
    for (let i = stack.length - 1; i >= 0; i--) base = over(stack[i], base);
    return base;
  };
  const ratio = (a, b) => {
    const la = luminance(a.r, a.g, a.b), lb = luminance(b.r, b.g, b.b);
    return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
  };

  const seenContrast = new Set();
  for (const el of document.querySelectorAll('body *')) {
    if (!hasOwnText(el) || !visible(el)) continue;
    const cs = getComputedStyle(el);
    const size = parseFloat(cs.fontSize);
    const weight = parseInt(cs.fontWeight, 10) || 400;

    if (size < MIN_FONT) {
      out.smallText.push({ el: where(el), size: +size.toFixed(1) });
    }

    const fg = parseColor(cs.color);
    const bg = bgOf(el);
    if (!fg || bg.unknown) continue;
    const eff = fg.a < 1 ? over(fg, bg) : fg;
    const r = ratio(eff, bg);
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const need = large ? CONTRAST_LARGE : CONTRAST_TEXT;
    if (r < need) {
      const key = `${cs.color}|${cs.fontSize}|${Math.round(r * 100)}`;
      if (seenContrast.has(key)) continue;
      seenContrast.add(key);
      out.contrast.push({
        el: where(el), ratio: +r.toFixed(2), need,
        fg: cs.color, bg: `rgb(${Math.round(bg.r)}, ${Math.round(bg.g)}, ${Math.round(bg.b)})`,
        size: +size.toFixed(1), weight,
      });
    }
  }
  out.counts = { smallText: out.smallText.length, contrast: out.contrast.length };
  out.smallText.sort((a, b) => a.size - b.size);
  out.contrast.sort((a, b) => a.ratio - b.ratio);
  out.smallText = out.smallText.slice(0, 25);
  out.contrast = out.contrast.slice(0, 25);

  // ---------- imatges ----------
  for (const img of document.querySelectorAll('img')) {
    const r = img.getBoundingClientRect();
    const shown = visible(img);
    if (img.complete && img.naturalWidth === 0 && img.getAttribute('src')) {
      out.images.broken.push({ src: img.getAttribute('src') });
      continue;
    }
    if (!img.hasAttribute('alt')) out.images.noAlt.push({ src: img.getAttribute('src') || '(sense src)' });
    if (shown && r.width > 0) {
      // Regla del club: cap foto ampliada. En retina calen 2x els píxels.
      const needed = r.width * dpr;
      if (img.naturalWidth > 0 && img.naturalWidth < needed * 0.75) {
        out.images.upscaled.push({
          src: (img.currentSrc || img.src).split('/').pop(),
          natural: img.naturalWidth, css: Math.round(r.width), dpr,
          shortfall: +(needed / img.naturalWidth).toFixed(2),
        });
      }
      // Al revés: baixar 3000 px per pintar-ne 300 és pes regalat.
      if (img.naturalWidth > needed * 2.5 && img.naturalWidth > 1000) {
        out.images.oversized.push({
          src: (img.currentSrc || img.src).split('/').pop(),
          natural: img.naturalWidth, css: Math.round(r.width),
        });
      }
      if (!img.getAttribute('width') || !img.getAttribute('height')) {
        if (!getComputedStyle(img).aspectRatio || getComputedStyle(img).aspectRatio === 'auto') {
          out.images.noDims.push({ src: (img.getAttribute('src') || '').split('/').pop() });
        }
      }
    }
  }
  for (const k of Object.keys(out.images)) out.images[k] = out.images[k].slice(0, 20);

  // ---------- encapçalaments ----------
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(visible);
  out.headings.h1 = hs.filter((h) => h.tagName === 'H1').length;
  let prev = 0;
  for (const h of hs) {
    const lvl = +h.tagName[1];
    out.headings.order.push(lvl);
    if (prev && lvl > prev + 1) {
      out.headings.skips.push({ from: `h${prev}`, to: `h${lvl}`, text: (h.textContent || '').trim().slice(0, 40) });
    }
    prev = lvl;
  }

  // ---------- IDs duplicats ----------
  const ids = new Map();
  for (const el of document.querySelectorAll('[id]')) {
    ids.set(el.id, (ids.get(el.id) || 0) + 1);
  }
  for (const [id, n] of ids) if (n > 1) out.duplicateIds.push({ id, count: n });

  // ---------- controls sense nom accessible ----------
  const nameOf = (el) => (
    (el.getAttribute('aria-label') || '').trim() ||
    (el.getAttribute('title') || '').trim() ||
    (el.textContent || '').trim() ||
    [...el.querySelectorAll('img[alt]')].map((i) => i.alt.trim()).join(' ').trim() ||
    (el.querySelector('svg title')?.textContent || '').trim() ||
    (el.getAttribute('aria-labelledby') ? 'ref' : '')
  );
  for (const el of document.querySelectorAll('a[href], button, [role=button]')) {
    if (!visible(el)) continue;
    if (!nameOf(el)) out.unnamed.push({ el: where(el), href: el.getAttribute('href') || '' });
  }
  out.unnamed = out.unnamed.slice(0, 20);

  // ---------- estructura ----------
  out.landmarks = {
    lang: document.documentElement.getAttribute('lang') || null,
    main: document.querySelectorAll('main, [role=main]').length,
    nav: document.querySelectorAll('nav, [role=navigation]').length,
    header: document.querySelectorAll('header, [role=banner]').length,
    footer: document.querySelectorAll('footer, [role=contentinfo]').length,
    skipLink: !!document.querySelector('a[href^="#"]:first-of-type'),
  };
  const vp = document.querySelector('meta[name=viewport]');
  out.viewportMeta = vp ? vp.getAttribute('content') : null;

  // ---------- taules que desborden ----------
  for (const t of document.querySelectorAll('table')) {
    if (!visible(t)) continue;
    const parent = t.parentElement;
    const pcs = parent ? getComputedStyle(parent) : null;
    const scrollable = pcs && (pcs.overflowX === 'auto' || pcs.overflowX === 'scroll');
    if (t.scrollWidth > vw + 1 && !scrollable) {
      out.tables.push({ el: where(t), width: t.scrollWidth });
    }
  }

  // El focus es comprova amb tabulació de debò des del runner: cridar
  // element.focus() no activa :focus-visible i donaria un fals positiu.

  // ---------- colors realment pintats ----------
  const tally = new Map();
  for (const el of document.querySelectorAll('body *')) {
    if (!visible(el)) continue;
    const cs = getComputedStyle(el);
    for (const prop of ['color', 'backgroundColor', 'borderTopColor']) {
      const c = parseColor(cs[prop]);
      if (!c || c.a === 0) continue;
      // Ens interessen els colors saturats: els grisos no diuen res de marca.
      const max = Math.max(c.r, c.g, c.b), min = Math.min(c.r, c.g, c.b);
      if (max - min < 40) continue;
      const hex = '#' + [c.r, c.g, c.b].map((v) => Math.round(v).toString(16).padStart(2, '0')).join('');
      tally.set(hex, (tally.get(hex) || 0) + 1);
    }
  }
  out.palette = [...tally.entries()].sort((a, b) => b[1] - a[1]).slice(0, 14).map(([hex, n]) => ({ hex, n }));

  // ---------- mides ----------
  out.stats = {
    domNodes: document.getElementsByTagName('*').length,
    images: document.images.length,
    scripts: document.scripts.length,
    inlineStyleBytes: [...document.querySelectorAll('style')].reduce((n, s) => n + s.textContent.length, 0),
    textBytes: (document.body.innerText || '').length,
    scrollHeight: document.documentElement.scrollHeight,
  };

  return out;
}
