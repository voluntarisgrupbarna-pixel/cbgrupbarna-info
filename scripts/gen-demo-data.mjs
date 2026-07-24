// Genera panel-instagram/data.json de DEMOSTRACIÓ (determinista, sense random).
// Inclou sèrie DIÀRIA multi-any (2024-01-01 → 2026-07-24) perquè el BI pugui
// comparar dies i mesos d'anys anteriors. En mode real, el fetcher acumula
// aquestes mateixes dades dia a dia.
import { writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __d = dirname(fileURLToPath(import.meta.url));
const OUT_DIR = join(__d, '..', 'panel-instagram');
const REF = '2026-07-24';

// ── Deterministic pseudo-noise (sense Math.random) ────────────────────────
function hash(s) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return ((h >>> 0) % 1000) / 1000; }

const MONTH_F = [0.80, 0.75, 0.95, 0.85, 0.90, 1.30, 1.45, 0.55, 1.85, 1.20, 1.00, 0.65]; // gen..des
const WD_F = [0.80, 0.90, 1.00, 1.00, 1.10, 1.40, 1.30]; // dl..dg (getDay: 0=dg)
const WD_IDX = (d) => (d.getUTCDay() + 6) % 7; // 0=dilluns
const YEAR_G = { 2024: 0.82, 2025: 1.00, 2026: 1.18 };

function eachDay(from, to) {
  const out = []; const d = new Date(from + 'T00:00:00Z'); const end = new Date(to + 'T00:00:00Z');
  while (d <= end) { out.push(d.toISOString().slice(0, 10)); d.setUTCDate(d.getUTCDate() + 1); }
  return out;
}

// ── Sèrie diària ──────────────────────────────────────────────────────────
const daily = [];
let followers = 1585;
for (const date of eachDay('2024-01-01', REF)) {
  const dt = new Date(date + 'T00:00:00Z');
  const y = dt.getUTCFullYear(), m = dt.getUTCMonth();
  const wf = WD_F[WD_IDX(dt)], mf = MONTH_F[m], yg = YEAR_G[y];
  const noise = 0.7 + 0.6 * hash(date);
  const nf = Math.max(0, Math.round(1.7 * mf * wf * yg * noise));
  followers += nf;
  const reach = Math.round((nf * 240 + 1350) * (0.85 + 0.3 * (wf - 0.8)) * (0.9 + 0.2 * hash('r' + date)));
  const profileViews = Math.round(reach * (0.11 + 0.05 * hash('p' + date)));
  daily.push({ date, followers, newFollowers: nf, reach, profileViews });
}

// ── Mensual (agregat des del diari) ───────────────────────────────────────
const monthly = {};
for (const r of daily) {
  const key = r.date.slice(0, 7);
  const mm = (monthly[key] ||= { followers: 0, newFollowers: 0, reach: 0, profileViews: 0, posts: 0, avgEngagement: 0, _n: 0 });
  mm.followers = r.followers; // últim del mes
  mm.newFollowers += r.newFollowers;
  mm.reach += r.reach;
  mm.profileViews += r.profileViews;
  mm._n++;
}
for (const [key, mm] of Object.entries(monthly)) {
  const m = +key.slice(5, 7);
  mm.posts = [8, 7, 9, 8, 9, 11, 10, 6, 13, 10, 9, 7][m - 1];
  mm.avgEngagement = +(5.4 + (MONTH_F[m - 1] / 1.85) * 2.6).toFixed(2);
  delete mm._n;
}

// ── Publicacions recents (per als blocs de posts i el filtre per tipus) ────
const posts = [
  { id:'d1', caption:'🏆 SÈNIOR FEMENÍ imparable! Victòria al Clot i seguim líders. #somclot', type:'REELS', mediaType:'VIDEO', thumb:'', permalink:'https://instagram.com/cbgrupbarna', timestamp:'2026-07-22T18:30:00Z', likes:412, comments:38, saved:96, shares:71, reach:9840, views:14200, interactions:617, engagement:617, engagementRate:6.27 },
  { id:'d2', caption:"Portes Obertes 25-26: la primera cistella no s'oblida mai. Reserva prova 👇", type:'REELS', mediaType:'VIDEO', thumb:'', permalink:'https://instagram.com/cbgrupbarna', timestamp:'2026-07-20T17:00:00Z', likes:298, comments:24, saved:73, shares:44, reach:7120, views:9800, interactions:439, engagement:439, engagementRate:6.17 },
  { id:'d3', caption:'MVP de la jornada 🌟 Quins números! Enhorabona campiona.', type:'FEED', mediaType:'IMAGE', thumb:'', permalink:'https://instagram.com/cbgrupbarna', timestamp:'2026-07-19T12:00:00Z', likes:356, comments:19, saved:41, shares:22, reach:5980, views:0, interactions:438, engagement:438, engagementRate:7.32 },
  { id:'d4', caption:'Campus Time Chamber Estiu 26 · Setmana 1 en marxa 🔥', type:'REELS', mediaType:'VIDEO', thumb:'', permalink:'https://instagram.com/cbgrupbarna', timestamp:'2026-07-17T10:30:00Z', likes:241, comments:15, saved:52, shares:33, reach:5210, views:7400, interactions:341, engagement:341, engagementRate:6.54 },
  { id:'d5', caption:'3x3 Westfield Glòries: el barri no para de botar 🏀', type:'CAROUSEL_ALBUM', mediaType:'CAROUSEL_ALBUM', thumb:'', permalink:'https://instagram.com/cbgrupbarna', timestamp:'2026-07-15T19:00:00Z', likes:203, comments:11, saved:28, shares:14, reach:4360, views:0, interactions:256, engagement:256, engagementRate:5.87 },
  { id:'d6', caption:'Benvinguda al club! Nou fitxatge per al projecte femení 💪', type:'FEED', mediaType:'IMAGE', thumb:'', permalink:'https://instagram.com/cbgrupbarna', timestamp:'2026-07-13T18:00:00Z', likes:389, comments:42, saved:37, shares:29, reach:6100, views:0, interactions:497, engagement:497, engagementRate:8.15 },
  { id:'d7', caption:'Entrenament de tecnificació · detall que marca la diferència.', type:'REELS', mediaType:'VIDEO', thumb:'', permalink:'https://instagram.com/cbgrupbarna', timestamp:'2026-07-11T16:00:00Z', likes:167, comments:9, saved:61, shares:38, reach:6890, views:11200, interactions:275, engagement:275, engagementRate:3.99 },
  { id:'d8', caption:'Escoleta: 4 a 7 anys, pura diversió 🧡', type:'FEED', mediaType:'IMAGE', thumb:'', permalink:'https://instagram.com/cbgrupbarna', timestamp:'2026-07-09T11:00:00Z', likes:214, comments:13, saved:24, shares:9, reach:3980, views:0, interactions:260, engagement:260, engagementRate:6.53 },
];

const mentions = [
  { id:'m1', username:'westfield.glories', caption:'Gràcies @cbgrupbarna pel 3x3 més vibrant de l\'estiu! 🏀', type:'IMAGE', thumb:'', permalink:'https://instagram.com/westfield.glories', timestamp:'2026-07-23T14:20:00Z', likes:820, comments:31 },
  { id:'m2', username:'timechamber.bcn', caption:'Setmana 1 del Campus amb @cbgrupbarna 🔥 nivellàs.', type:'VIDEO', thumb:'', permalink:'https://instagram.com/timechamber.bcn', timestamp:'2026-07-22T09:10:00Z', likes:340, comments:12 },
  { id:'m3', username:'basketcatala', caption:'El @cbgrupbarna, referent de bàsquet base al Clot. Gran feina!', type:'IMAGE', thumb:'', permalink:'https://instagram.com/basketcatala', timestamp:'2026-07-21T20:00:00Z', likes:512, comments:24 },
  { id:'m4', username:'familia.puig', caption:'La nostra petita ja bota amb @cbgrupbarna ❤️', type:'IMAGE', thumb:'', permalink:'https://instagram.com/familia.puig', timestamp:'2026-07-20T18:45:00Z', likes:96, comments:7 },
  { id:'m5', username:'clot.comerç', caption:'Orgullosos de patrocinar @cbgrupbarna, el club del barri.', type:'IMAGE', thumb:'', permalink:'https://instagram.com/clot.comerç', timestamp:'2026-07-18T12:30:00Z', likes:210, comments:9 },
  { id:'m6', username:'jugadora.10', caption:'Millor decisió: fitxar pel @cbgrupbarna 💪🏀', type:'VIDEO', thumb:'', permalink:'https://instagram.com/jugadora.10', timestamp:'2026-07-16T17:15:00Z', likes:430, comments:28 },
  { id:'m7', username:'ampa.escola', caption:'Sortida esportiva amb @cbgrupbarna, dia rodó!', type:'CAROUSEL_ALBUM', thumb:'', permalink:'https://instagram.com/ampa.escola', timestamp:'2026-07-14T10:00:00Z', likes:78, comments:4 },
];

const last = daily[daily.length - 1];
const history = daily.slice(-30); // el panell overview fa servir 30 dies
const reach30 = history.reduce((a, b) => a + b.reach, 0);
const pv30 = history.reduce((a, b) => a + b.profileViews, 0);

const out = {
  meta: { generatedAt: REF + 'T09:00:00.000Z', mode:'demo', account:'@cbgrupbarna', apiVersion:'v21.0',
    errors:[], note:'DADES DE DEMOSTRACIÓ — connecta el token de la Graph API perquè es substitueixin per dades reals.' },
  profile: { username:'cbgrupbarna', name:'CB Grup Barna', biography:'🏀 Club de bàsquet base · El Clot, BCN · Des de 1965 · #somclot',
    followers_count:last.followers, follows_count:218, media_count:last.followers>0?612:612, website:'https://cbgrupbarna.info' },
  kpis: { followers:last.followers, followersDelta:last.newFollowers, following:218, posts:612,
    reach30, profileViews30:pv30,
    avgEngagementRate:+(posts.reduce((a,b)=>a+b.engagementRate,0)/posts.length).toFixed(2), mentionsCount:mentions.length },
  history,
  daily,
  media: posts.sort((a,b)=>b.engagement-a.engagement),
  contentMix: posts.reduce((a,m)=>{const k=m.type==='REELS'?'Reels':m.mediaType==='CAROUSEL_ALBUM'?'Carrusel':m.mediaType==='VIDEO'?'Vídeo':'Imatge';a[k]=(a[k]||0)+1;return a;},{}),
  mentions,
  monthly,
  demographics: { byCity:[
    {label:'Barcelona',value:1840},{label:'Badalona',value:280},{label:"L'Hospitalet",value:190},
    {label:'Sant Adrià',value:120},{label:'Santa Coloma',value:96},{label:'Cornellà',value:64},
    {label:'Terrassa',value:41},{label:'Girona',value:33},
  ]},
};
if (!existsSync(OUT_DIR)) mkdirSync(OUT_DIR, { recursive:true });
writeFileSync(join(OUT_DIR,'data.json'), JSON.stringify(out,null,2));
console.log(`✅ demo data.json — ${daily.length} dies, ${Object.keys(monthly).length} mesos, ${posts.length} posts`);
