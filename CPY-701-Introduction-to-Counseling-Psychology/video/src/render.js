/*
 * CPY 701 - Introduction to Counseling Psychology
 * Master's Degree in Counseling Psychology
 *
 * Slide renderer: turns slides/wNN.json into 1920x1080 presentation slides (PNG)
 * using a professional academic design system (Inter + Poppins, navy & gold).
 *
 * Usage: node src/render.js [weekId e.g. w01]
 */
const fs = require('fs');
const path = require('path');
const { Resvg } = require('@resvg/resvg-js');

const W = 1920, H = 1080, M = 110;              // canvas + margin
const FONT_DIR = path.join(require('os').homedir(), '.fonts');

// ---------------------------------------------------------------- design system
const C = {
  navy:   '#0B1B3A',   // deep academic navy
  navy2:  '#12264F',
  ink:    '#16233F',   // body text on light
  slate:  '#5A6784',   // secondary text
  line:   '#D8DEEB',
  surface:'#F7F8FC',   // light slide background
  card:   '#FFFFFF',
  cardAlt:'#EEF2F9',
  gold:   '#C9962E',
  goldHi: '#E8B84B',
  teal:   '#0F766E',   // process / evidence
  rust:   '#9A3412',   // warning / limits
  white:  '#FFFFFF',
  mist:   '#C9D3E8',   // light text on navy
};

// rough per-character advance widths (fraction of font size) for wrapping
const NARROW = new Set('iljtfr.,;:\'!|()[]');
const WIDE = new Set('mwMW@%');
function charW(ch, weight) {
  let w = 0.545;
  if (NARROW.has(ch)) w = 0.30;
  else if (WIDE.has(ch)) w = 0.88;
  else if (ch === ' ') w = 0.27;
  else if (ch >= 'A' && ch <= 'Z') w = 0.70;
  if (weight >= 600) w *= 1.045;
  return w;
}
function textW(str, size, weight = 400) {
  let s = 0;
  for (const ch of str) s += charW(ch, weight);
  return s * size;
}
function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
// greedy word wrap for a list of runs [{t, weight}]
function wrapRuns(runs, maxWidth, size) {
  const words = [];
  for (const r of runs) for (const w of r.t.split(/(\s+)/)) if (w) words.push({ t: w, weight: r.weight });
  const lines = [];
  let line = [], lineW = 0;
  for (const w of words) {
    const ww = textW(w.t, size, w.weight);
    if (lineW + ww > maxWidth && line.length && w.t.trim()) {
      lines.push(line); line = []; lineW = 0;
      if (!w.t.trim()) continue;
    }
    line.push(w); lineW += ww;
  }
  if (line.length) lines.push(line);
  return lines
    .map(l => {
      while (l.length && !l[0].t.trim()) l.shift();
      while (l.length && !l[l.length - 1].t.trim()) l.pop();
      return { runs: l, w: l.reduce((a, x) => a + textW(x.t, size, x.weight), 0) };
    })
    .filter(l => l.runs.length);
}

// ---------------------------------------------------------------- svg primitives
function rect(x, y, w, h, fill, rx = 0, extra = '') {
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}"${rx ? ` rx="${rx}"` : ''}${extra ? ' ' + extra : ''}/>`;
}
function text(x, y, str, { size = 32, weight = 400, family = 'Inter', fill = C.ink, anchor = 'start', spacing = 0, opacity = 1 } = {}) {
  return `<text x="${x}" y="${y}" font-family="${family}" font-weight="${weight}" font-size="${size}" fill="${fill}" text-anchor="${anchor}" xml:space="preserve"${spacing ? ` letter-spacing="${spacing}"` : ''}${opacity !== 1 ? ` opacity="${opacity}"` : ''}>${esc(str)}</text>`;
}
function line(x1, y1, x2, y2, stroke, w = 2, dash = '') {
  return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
}
// one wrapped line as a single <text> with weighted tspans: the font engine
// handles inter-word spacing and kerning exactly
function lineText(x, y, runs, { size = 34, fill = C.ink, anchor = 'start', family = 'Inter' } = {}) {
  const tspans = runs.map(r =>
    `<tspan font-weight="${r.weight}"${r.fill ? ` fill="${r.fill}"` : ''}>${esc(r.t)}</tspan>`).join('');
  return `<text x="${x}" y="${y}" font-family="${family}" font-size="${size}" fill="${fill}" text-anchor="${anchor}" xml:space="preserve">${tspans}</text>`;
}
// rich text block: runs with mixed weights, wrapped; returns svg + height consumed
function richBlock(x, y, runs, { size = 34, maxW = W - 2 * M, lh = 1.42, fill = C.ink } = {}) {
  const lines = wrapRuns(runs, maxW * 0.985, size);
  let out = '', cy = y;
  for (const l of lines) { out += lineText(x, cy, l.runs, { size, fill }); cy += size * lh; }
  return { svg: out, h: cy - y };
}
function bulletMark(x, y, lvl) {
  if (lvl === 0) return rect(x, y - 16, 12, 12, C.gold, 2);
  if (lvl === 1) return rect(x + 2, y - 13, 8, 8, 'none', 1, `stroke="${C.slate}" stroke-width="2"`);
  return `<circle cx="${x + 6}" cy="${y - 9}" r="3.5" fill="${C.slate}"/>`;
}

// ---------------------------------------------------------------- slide chrome
function chrome(slideIdx, total, week, module, dark) {
  const fg = dark ? C.mist : C.slate;
  const rule = dark ? 'rgba(201,150,46,.55)' : C.line;
  let s = '';
  s += line(M, H - 86, W - M, H - 86, rule, 1.5);
  s += text(M, H - 48, 'CPY 701 · Introduction to Counseling Psychology', { size: 22, fill: fg, family: 'Inter', weight: 500 });
  s += text(W / 2, H - 48, "Master's Degree in Counseling Psychology", { size: 22, fill: fg, anchor: 'middle', weight: 400 });
  s += text(W - M, H - 48, `${slideIdx} / ${total}`, { size: 22, fill: fg, anchor: 'end', family: 'Inter', weight: 600 });
  if (week !== undefined) {
    s += rect(W - M - 305, 58, 305, 46, dark ? 'rgba(255,255,255,.10)' : '#E9EDF6', 23);
    s += text(W - M - 152, 89, `Week ${week} · ${module}`, { size: 22, fill: dark ? C.mist : C.slate, anchor: 'middle', weight: 600 });
    s += rect(M, 58, 132, 46, dark ? C.gold : C.navy, 23);
    s += text(M + 66, 89, 'CPY 701', { size: 22, fill: dark ? C.navy : C.white, anchor: 'middle', weight: 700, family: 'Poppins' });
  }
  return s;
}
function bgLight() {
  return rect(0, 0, W, H, C.surface)
    + rect(0, 0, W, 6, C.navy)
    + rect(0, 6, W, 3, C.gold);
}
function bgDark() {
  return `<defs><linearGradient id="bgd" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="${C.navy}"/><stop offset="1" stop-color="${C.navy2}"/></linearGradient></defs>`
    + rect(0, 0, W, H, 'url(#bgd)')
    + `<circle cx="${W - 220}" cy="${H - 190}" r="330" fill="none" stroke="${C.gold}" stroke-width="2" opacity="0.28"/>`
    + `<circle cx="${W - 220}" cy="${H - 190}" r="240" fill="none" stroke="${C.gold}" stroke-width="1.2" opacity="0.20"/>`
    + `<circle cx="150" cy="120" r="150" fill="${C.gold}" opacity="0.06"/>`;
}
function header(title, kicker) {
  let s = '';
  if (kicker) s += text(M, 178, kicker.toUpperCase(), { size: 24, weight: 700, fill: C.gold, family: 'Poppins', spacing: 3 });
  s += text(M, 236, title, { size: 52, weight: 600, fill: C.navy, family: 'Poppins' });
  s += rect(M, 262, 110, 6, C.gold, 3);
  return s;
}

// ---------------------------------------------------------------- layouts
function L_title(s) {
  let out = bgDark() + chrome(s.idx, s.total, undefined, undefined, true);
  out += rect(M, 150, 6, 0, C.gold);
  out += text(M, 250, s.kicker.toUpperCase(), { size: 26, weight: 700, fill: C.goldHi, family: 'Poppins', spacing: 4 });
  out += text(M, 340, s.title, { size: 76, weight: 700, fill: C.white, family: 'Poppins' });
  if (s.subtitle) out += text(M, 408, s.subtitle, { size: 36, weight: 500, fill: C.mist, family: 'Inter' });
  out += rect(M, 462, 150, 6, C.gold, 3);
  let y = 545;
  for (const l of s.meta || []) { out += text(M, y, l, { size: 27, fill: C.mist }); y += 42; }
  out += text(M, H - 150, s.footer || '', { size: 24, fill: C.mist, opacity: 0.8 });
  return out;
}
function L_section(s) {
  let out = bgDark() + chrome(s.idx, s.total, s.week, s.module, true);
  out += text(M, 400, s.kicker.toUpperCase(), { size: 26, weight: 700, fill: C.goldHi, family: 'Poppins', spacing: 4 });
  out += text(M, 490, s.title, { size: 64, weight: 700, fill: C.white, family: 'Poppins' });
  out += rect(M, 528, 150, 6, C.gold, 3);
  if (s.lede) {
    const b = richBlock(M, 600, [{ t: s.lede, weight: 400 }], { size: 32, maxW: 1250, fill: C.mist });
    out += b.svg;
  }
  return out;
}
function L_bullets(s) {
  let out = bgLight() + chrome(s.idx, s.total, s.week, s.module) + header(s.title, s.kicker);
  let y = 340;
  const maxW = W - 2 * M - 46;
  for (const it of s.items) {
    const lvl = it.lvl || 0;
    const x = M + lvl * 56;
    const size = lvl === 0 ? 34 : 29;
    const runs = [];
    if (it.lead) runs.push({ t: it.lead + '  ', weight: 700, fill: C.navy });
    runs.push({ t: it.text, weight: lvl === 0 ? 400 : 400 });
    const blk = richBlock(x + 46, y, runs, { size, maxW: maxW - lvl * 56 });
    out += bulletMark(x + 8, y - 6, lvl);
    out += blk.svg;
    y += Math.max(blk.h, size * 1.42) + (lvl === 0 ? 26 : 16);
  }
  if (s.callout) {
    const b = richBlock(M + 40, H - 86 - 150, [{ t: s.callout.label + '  ', weight: 700, fill: C.teal }, { t: s.callout.text, weight: 400 }], { size: 28, maxW: W - 2 * M - 80 });
    out += rect(M, H - 86 - 172, W - 2 * M, b.h + 44, '#E7F3F1', 12) + rect(M, H - 86 - 172, 8, b.h + 44, C.teal, 4);
    out += b.svg;
  }
  return out;
}
function L_table(s) {
  let out = bgLight() + chrome(s.idx, s.total, s.week, s.module) + header(s.title, s.kicker);
  const cols = s.cols;                     // [{t, w(fraction)}]
  const x0 = M, totalW = W - 2 * M;
  let xs = [], acc = x0;
  for (const c of cols) { xs.push(acc); acc += c.w * totalW; }
  xs.push(acc);
  const cell = (str, x, y, w, { size = 26, weight = 400, fill = C.ink, lh = 1.32 } = {}) =>
    richBlock(x + 22, y, [{ t: str, weight }], { size, maxW: w - 44, lh, fill }).svg;
  let y = 348;
  // header row
  const hh = 64;
  out += rect(x0, y, totalW, hh, C.navy);
  cols.forEach((c, i) => { out += text(xs[i] + 22, y + 42, c.t, { size: 26, weight: 700, fill: C.white, family: 'Poppins' }); });
  y += hh;
  // body rows with row heights computed from wrapped cells
  s.rows.forEach((row, ri) => {
    const lines = row.map((str, i) => wrapRuns([{ t: str, weight: i === 0 ? 600 : 400 }], (xs[i + 1] - xs[i]) - 44, 26));
    const rh = Math.max(...lines.map(l => l.length)) * 26 * 1.32 + 30;
    out += rect(x0, y, totalW, rh, ri % 2 ? C.cardAlt : C.card);
    row.forEach((str, i) => {
      let cy = y + 34;
      for (const l of lines[i]) { out += lineText(xs[i] + 22, cy, l.runs, { size: 26, fill: i === 0 ? C.navy : C.ink }); cy += 26 * 1.32; }
    });
    cols.forEach((c, i) => { if (i) out += line(xs[i], y, xs[i], y + rh, C.line, 1); });
    y += rh;
  });
  out += rect(x0, 348, totalW, y - 348, 'none', 0, `stroke="${C.line}" stroke-width="1.5"`);
  if (s.note) out += text(M, y + 44, s.note, { size: 24, fill: C.slate, weight: 500 });
  return out;
}
function L_cards(s) {
  let out = bgLight() + chrome(s.idx, s.total, s.week, s.module) + header(s.title, s.kicker);
  const n = s.cards.length, perRow = s.perRow || 3;
  const gap = 34, cw = (W - 2 * M - gap * (perRow - 1)) / perRow;
  const rows = Math.ceil(n / perRow);
  const ch = Math.min(300, (H - 348 - 120 - gap * (rows - 1)) / rows);
  s.cards.forEach((cd, i) => {
    const r = Math.floor(i / perRow), c = i % perRow;
    const x = M + c * (cw + gap), y = 352 + r * (ch + gap);
    out += rect(x, y, cw, ch, C.card, 14, `stroke="${C.line}" stroke-width="1.5"`) + rect(x, y, cw, 8, cd.color || C.gold, 0, `rx="0"`);
    out += rect(x, y, cw, 8, cd.color || C.gold);
    out += text(x + 30, y + 66, cd.title, { size: 29, weight: 600, fill: C.navy, family: 'Poppins' });
    const b = richBlock(x + 30, y + 106, [{ t: cd.text, weight: 400 }], { size: 24, maxW: cw - 60, fill: C.slate, lh: 1.4 });
    out += b.svg;
  });
  return out;
}
function L_flow(s) {
  let out = bgLight() + chrome(s.idx, s.total, s.week, s.module) + header(s.title, s.kicker);
  const steps = s.steps, n = steps.length;
  const gap = 26, sw = (W - 2 * M - gap * (n - 1)) / n;
  let y = 430, sh = 300;
  steps.forEach((st, i) => {
    const x = M + i * (sw + gap);
    out += rect(x, y, sw, sh, C.card, 14, `stroke="${C.line}" stroke-width="1.5"`);
    out += rect(x, y, sw, 10, st.color || C.navy);
    out += `<circle cx="${x + sw / 2}" cy="${y + 74}" r="34" fill="${st.color || C.navy}"/>`;
    out += text(x + sw / 2, y + 86, String(i + 1), { size: 32, weight: 700, fill: C.white, anchor: 'middle', family: 'Poppins' });
    out += text(x + sw / 2, y + 148, st.title, { size: 25, weight: 600, fill: C.navy, anchor: 'middle', family: 'Poppins' });
    const b = richBlock(x + 20, y + 182, [{ t: st.text, weight: 400 }], { size: 21, maxW: sw - 40, fill: C.slate, lh: 1.35 });
    out += b.svg;
    if (i < n - 1) {
      const ax = x + sw + 4;
      out += `<path d="M ${ax} ${y + sh / 2} l ${gap - 8} 0 m -12 -8 l 12 8 l -12 8" stroke="${C.gold}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
    }
  });
  if (s.note) { out += rect(M, y + sh + 46, W - 2 * M, 78, '#FFF7E6', 12) + rect(M, y + sh + 46, 8, 78, C.gold);
    out += text(M + 36, y + sh + 94, s.note, { size: 26, fill: '#6B4E10', weight: 500 }); }
  return out;
}
function L_twocol(s) {
  let out = bgLight() + chrome(s.idx, s.total, s.week, s.module) + header(s.title, s.kicker);
  const gap = 40, cw = (W - 2 * M - gap) / 2;
  [s.left, s.right].forEach((col, i) => {
    const x = M + i * (cw + gap);
    out += rect(x, 352, cw, H - 352 - 150, C.card, 14, `stroke="${C.line}" stroke-width="1.5"`);
    out += rect(x, 352, cw, 74, col.color || C.navy, 14);
    out += rect(x, 352 + 60, cw, 14, col.color || C.navy);
    out += text(x + 34, 402, col.title, { size: 30, weight: 600, fill: C.white, family: 'Poppins' });
    let y = 470;
    for (const it of col.items) {
      const b = richBlock(x + 46, y, [{ t: it, weight: 400 }], { size: 26, maxW: cw - 92, fill: C.ink, lh: 1.38 });
      out += bulletMark(x + 16, y - 4, 0);
      out += b.svg;
      y += b.h + 20;
    }
  });
  return out;
}
function L_continuum(s) {
  let out = bgLight() + chrome(s.idx, s.total, s.week, s.module) + header(s.title, s.kicker);
  const n = s.nodes.length, y = 610;
  const x0 = 320, x1 = W - 320;
  out += line(x0, y, x1, y, C.navy, 4);
  out += `<path d="M ${x1} ${y} l -22 -11 m 22 11 l -22 11" stroke="${C.navy}" stroke-width="4" fill="none" stroke-linecap="round"/>`;
  const bw = 380, dsize = 23, dlh = 1.35;
  s.nodes.forEach((nd, i) => {
    const x = x0 + (i / (n - 1)) * (x1 - x0);
    const up = i % 2 === 0;
    out += `<circle cx="${x}" cy="${y}" r="15" fill="${nd.color || C.gold}" stroke="${C.surface}" stroke-width="5"/>`;
    const lines = wrapRuns([{ t: nd.text, weight: 400 }], bw * 0.96, dsize);
    const descH = lines.length * dsize * dlh;
    const titleY = up ? y - 78 : y + 100;
    const descTop = up ? titleY - 40 - descH : titleY + 40;
    out += text(x, titleY, nd.title, { size: 31, weight: 600, fill: C.navy, anchor: 'middle', family: 'Poppins' });
    lines.forEach((l, k) => { out += lineText(x, descTop + k * dsize * dlh, l.runs, { size: dsize, fill: C.slate, anchor: 'middle' }); });
    out += line(x, up ? y - 22 : y + 22, x, up ? titleY + 16 : titleY - 30, C.line, 2, '4 5');
  });
  if (s.note) out += text(M, H - 150, s.note, { size: 26, fill: C.slate, weight: 500 });
  return out;
}
function L_triangle(s) {
  let out = bgLight() + chrome(s.idx, s.total, s.week, s.module) + header(s.title, s.kicker);
  const cx = W / 2, cy = 610, R = 225;
  const pts = [[cx, cy - R], [cx - R * 0.95, cy + R * 0.62], [cx + R * 0.95, cy + R * 0.62]];
  out += `<path d="M ${pts[0]} L ${pts[1]} L ${pts[2]} Z" fill="none" stroke="${C.line}" stroke-width="3"/>`;
  s.points.forEach((p, i) => {
    const [px, py] = pts[i];
    out += `<circle cx="${px}" cy="${py}" r="105" fill="${p.color || C.navy}" opacity="0.96"/>`;
    const lines = wrapRuns([{ t: p.title, weight: 600 }], 168, 26);
    const th = lines.length * 26 * 1.25;
    lines.forEach((l, k) => { out += lineText(px, py - th / 2 + 26 * 0.9 + k * 26 * 1.25, l.runs, { size: 26, fill: C.white, anchor: 'middle' }); });
  });
  out += `<circle cx="${cx}" cy="${cy}" r="86" fill="${C.gold}"/>`;
  out += text(cx, cy - 8, s.center[0], { size: 25, weight: 700, fill: C.navy, anchor: 'middle', family: 'Poppins' });
  out += text(cx, cy + 26, s.center[1], { size: 25, weight: 700, fill: C.navy, anchor: 'middle', family: 'Poppins' });
  const b = richBlock(M, 912, [{ t: s.lede, weight: 400 }], { size: 27, maxW: W - 2 * M, fill: C.slate });
  out += b.svg;
  return out;
}
function L_quote(s) {
  let out = bgDark() + chrome(s.idx, s.total, s.week, s.module, true);
  out += text(M, 330, '\u201C', { size: 200, fill: C.gold, family: 'Poppins', weight: 700 });
  const b = richBlock(M + 40, 430, [{ t: s.quote, weight: 500 }], { size: 44, maxW: W - 2 * M - 200, fill: C.white, lh: 1.45 });
  out += b.svg;
  out += rect(M + 40, 430 + b.h + 46, 110, 6, C.gold, 3);
  out += text(M + 40, 430 + b.h + 106, s.by, { size: 28, fill: C.goldHi, weight: 600, family: 'Poppins' });
  return out;
}
function L_summary(s) {
  let out = bgDark() + chrome(s.idx, s.total, s.week, s.module, true);
  out += text(M, 210, 'WEEK IN REVIEW', { size: 24, weight: 700, fill: C.goldHi, family: 'Poppins', spacing: 4 });
  out += text(M, 276, s.title, { size: 50, weight: 600, fill: C.white, family: 'Poppins' });
  let y = 372;
  s.items.forEach((it, i) => {
    out += rect(M, y - 34, 44, 44, C.gold, 10);
    out += text(M + 22, y - 2, String(i + 1), { size: 26, weight: 700, fill: C.navy, anchor: 'middle', family: 'Poppins' });
    const b = richBlock(M + 72, y, [{ t: it, weight: 400 }], { size: 29, maxW: W - 2 * M - 90, fill: C.mist, lh: 1.38 });
    out += b.svg;
    y += Math.max(b.h, 40) + 30;
  });
  return out;
}
function L_task(s) {
  let out = bgLight() + chrome(s.idx, s.total, s.week, s.module) + header(s.title, s.kicker);
  out += rect(M, 352, W - 2 * M, H - 352 - 150, C.card, 16, `stroke="${C.line}" stroke-width="1.5"`);
  out += rect(M, 352, W - 2 * M, 86, C.navy, 16);
  out += rect(M, 352 + 70, W - 2 * M, 16, C.navy);
  out += text(M + 40, 410, 'APPLIED TASK', { size: 28, weight: 700, fill: C.goldHi, family: 'Poppins', spacing: 3 });
  let y = 500;
  for (const it of s.items) {
    const b = richBlock(M + 80, y, [{ t: it, weight: 400 }], { size: 30, maxW: W - 2 * M - 160, fill: C.ink, lh: 1.42 });
    out += rect(M + 44, y - 20, 14, 14, C.gold, 3);
    out += b.svg;
    y += b.h + 26;
  }
  if (s.next) {
    out += rect(M + 40, H - 150 - 96, W - 2 * M - 80, 76, '#E9EDF6', 12);
    out += text(M + 72, H - 150 - 48, s.next, { size: 26, weight: 600, fill: C.navy });
  }
  return out;
}

const LAYOUTS = {
  title: L_title, section: L_section, bullets: L_bullets, table: L_table, cards: L_cards,
  flow: L_flow, twocol: L_twocol, continuum: L_continuum, triangle: L_triangle,
  quote: L_quote, summary: L_summary, task: L_task,
};

// ---------------------------------------------------------------- main
function render(weekId) {
  const dir = path.join(__dirname, '..', 'slides');
  const file = path.join(dir, `${weekId}.json`);
  const doc = JSON.parse(fs.readFileSync(file, 'utf8'));
  const slides = doc.slides;
  slides.forEach((s, i) => { s.idx = i + 1; s.total = slides.length; s.week = s.week ?? doc.week; s.module = s.module ?? doc.module; });
  const outDir = path.join(__dirname, '..', '..', 'dist', 'slides', weekId);
  fs.mkdirSync(outDir, { recursive: true });
  const manifest = [];
  slides.forEach((s, i) => {
    const builder = LAYOUTS[s.layout];
    if (!builder) throw new Error(`unknown layout ${s.layout}`);
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${builder(s)}</svg>`;
    const r = new Resvg(svg, { fitTo: { mode: 'width', width: W } });
    const png = r.render().asPng();
    const name = `${String(i + 1).padStart(2, '0')}-${(s.slug || s.layout).replace(/[^\w-]+/g, '-')}.png`;
    fs.writeFileSync(path.join(outDir, name), png);
    manifest.push({ i: i + 1, file: name, layout: s.layout, title: s.title || '', slug: s.slug || s.layout, narration: s.narration || '' });
  });
  fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify({ week: weekId, title: doc.title, slides: manifest }, null, 2));
  console.log(`${weekId}: rendered ${slides.length} slides -> ${outDir}`);
  return manifest;
}

if (require.main === module) {
  const arg = process.argv[2];
  const dir = path.join(__dirname, '..', 'slides');
  const weeks = arg ? [arg] : fs.readdirSync(dir).filter(f => f.endsWith('.json')).map(f => f.replace('.json', ''));
  weeks.forEach(render);
}
module.exports = { render };
