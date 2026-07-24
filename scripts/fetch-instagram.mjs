#!/usr/bin/env node
/**
 * fetch-instagram.mjs — EXTRACTOR COMPLET de la Instagram Graph API per al
 * Panell d'Instagram del CB Grup Barna (@cbgrupbarna).
 *
 * Objectiu: treure de l'API TOT el que ofereix per a un compte Business/Creator,
 * amb degradació robusta. Cada bloc va dins d'un try/catch: si un permís o una
 * mètrica no està disponible en la versió de l'API, es registra a `meta.coverage`
 * i la resta segueix funcionant.
 *
 * S'executa des del GitHub Action `instagram-panel.yml`. El token viu a GitHub
 * Secrets (mai al codi) i s'escriu `panel-instagram/data.json`. Zero servidor.
 *
 * Variables d'entorn:
 *   IG_ACCESS_TOKEN   Token de llarga durada (User o System User) amb permisos:
 *                     instagram_basic, instagram_manage_insights,
 *                     instagram_manage_comments, pages_read_engagement,
 *                     pages_show_list, business_management (per business_discovery).
 *   IG_USER_ID        ID del compte Instagram Business/Creator.
 *   IG_API_VERSION    (opcional) versió de l'API, per defecte v21.0.
 *
 * Fitxers auxiliars (opcionals) a panel-instagram/:
 *   historic.json     mesos passats per a la comparativa any-rere-any.
 *   benchmark.json    { "usernames": ["sese_bc", ...] } rivals a monitoritzar.
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const OUT_DIR = join(ROOT, 'panel-instagram');
const OUT_FILE = join(OUT_DIR, 'data.json');
const HISTORIC_FILE = join(OUT_DIR, 'historic.json');
const BENCHMARK_FILE = join(OUT_DIR, 'benchmark.json');

const TOKEN = process.env.IG_ACCESS_TOKEN;
const IG_ID = process.env.IG_USER_ID;
const API = process.env.IG_API_VERSION || 'v21.0';
const BASE = `https://graph.facebook.com/${API}`;
const HISTORY_MAX = 365; // dies de sèrie temporal que acumulem nosaltres
const MEDIA_MAX = 200;    // sostre de publicacions a paginar

const errors = [];
const coverage = {}; // { bloc: 'ok' | 'buit' | 'error: ...' }
const now = new Date();

/** Crida a l'API amb gestió d'errors. Retorna l'objecte JSON o null. */
async function ig(path, params = {}) {
  const url = new URL(`${BASE}/${path}`);
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  url.searchParams.set('access_token', TOKEN);
  try {
    const res = await fetch(url);
    const json = await res.json();
    if (json.error) { errors.push(`${path}: ${json.error.message} (code ${json.error.code})`); return null; }
    return json;
  } catch (e) { errors.push(`${path}: ${e.message}`); return null; }
}

/** Segueix la paginació (.paging.next) fins a un màxim d'elements. */
async function igAll(path, params = {}, max = MEDIA_MAX) {
  const out = [];
  let next = null;
  const first = await ig(path, { ...params, limit: 50 });
  if (!first) return out;
  out.push(...(first.data || []));
  next = first.paging?.next;
  while (next && out.length < max) {
    try {
      const res = await fetch(next);
      const json = await res.json();
      if (json.error) { errors.push(`${path} (page): ${json.error.message}`); break; }
      out.push(...(json.data || []));
      next = json.paging?.next;
    } catch (e) { errors.push(`${path} (page): ${e.message}`); break; }
  }
  return out.slice(0, max);
}

const ymd = (d) => d.toISOString().slice(0, 10);
const sinceUntil = (days) => ({
  since: Math.floor((now.getTime() - (days - 1) * 864e5) / 1000),
  until: Math.floor(now.getTime() / 1000),
});

/** Insight total_value amb fallback a sèrie diària. Retorna {total, series?} o null. */
async function totalValue(metric, days = 30) {
  const { since, until } = sinceUntil(days);
  const r = await ig(`${IG_ID}/insights`, { metric, period: 'day', since, until, metric_type: 'total_value' });
  if (r?.data?.[0]?.total_value?.value != null) return { total: r.data[0].total_value.value };
  const r2 = await ig(`${IG_ID}/insights`, { metric, period: 'day', since, until });
  if (r2?.data?.[0]?.values) {
    const series = r2.data[0].values.map((v) => ({ date: v.end_time?.slice(0, 10), value: v.value }));
    return { total: series.reduce((a, b) => a + (b.value || 0), 0), series };
  }
  return null;
}

/** Demografia amb un breakdown concret (city|country|age|gender). */
async function demographic(breakdown) {
  const r = await ig(`${IG_ID}/insights`, {
    metric: 'follower_demographics', period: 'lifetime',
    metric_type: 'total_value', timeframe: 'this_month', breakdown,
  });
  const results = r?.data?.[0]?.total_value?.breakdowns?.[0]?.results;
  if (!results) return null;
  return results
    .map((x) => ({ label: x.dimension_values?.[0], value: x.value }))
    .filter((x) => x.label != null)
    .sort((a, b) => b.value - a.value);
}

async function main() {
  if (!TOKEN || !IG_ID) {
    console.error('❌ Falten IG_ACCESS_TOKEN o IG_USER_ID. Deixo data.json intacte (mode demo).');
    process.exit(0);
  }

  // ── 1. Perfil ─────────────────────────────────────────────────────────────
  const profile = await ig(IG_ID, {
    fields: 'username,name,biography,followers_count,follows_count,media_count,profile_picture_url,website,ig_id',
  }) || {};
  coverage.profile = profile.username ? 'ok' : 'error';

  // Límit de publicació de l'API
  const publishLimit = await ig(`${IG_ID}/content_publishing_limit`, { fields: 'config,quota_usage' });
  coverage.publishLimit = publishLimit?.data ? 'ok' : 'no disponible';

  // ── 2. Insights de compte (últims 30 dies) — SET COMPLET ──────────────────
  const METRICS = [
    'reach', 'profile_views', 'website_clicks', 'email_contacts', 'phone_call_clicks',
    'text_message_clicks', 'get_directions_clicks', 'accounts_engaged', 'total_interactions',
    'likes', 'comments', 'saves', 'shares', 'replies', 'profile_links_taps',
    'follows_and_unfollows', 'views',
  ];
  const accountInsights = {};
  for (const metric of METRICS) {
    const r = await totalValue(metric, 30);
    if (r) accountInsights[metric] = r;
  }
  coverage.accountInsights = `${Object.keys(accountInsights).length}/${METRICS.length} mètriques`;

  // Sèrie diària d'abast i de nous seguidors (per a la corba)
  const { since, until } = sinceUntil(30);
  const reachDaily = await ig(`${IG_ID}/insights`, { metric: 'reach', period: 'day', since, until });
  const followerDaily = await ig(`${IG_ID}/insights`, { metric: 'follower_count', period: 'day', since, until });
  const dailyReach = (reachDaily?.data?.[0]?.values || []).map((v) => ({ date: v.end_time?.slice(0, 10), value: v.value }));
  const dailyNewFollowers = (followerDaily?.data?.[0]?.values || []).map((v) => ({ date: v.end_time?.slice(0, 10), value: v.value }));

  // ── 3. Audiència completa (ciutat, país, edat, gènere) ────────────────────
  const audience = {
    byCity: await demographic('city'),
    byCountry: await demographic('country'),
    byAge: await demographic('age'),
    byGender: await demographic('gender'),
  };
  coverage.audience = Object.entries(audience).filter(([, v]) => v).map(([k]) => k).join(',') || 'buit';

  // ── 4. Publicacions (TOTES, paginades) amb insights per tipus ─────────────
  const mediaFields =
    'id,caption,media_type,media_product_type,media_url,thumbnail_url,permalink,timestamp,' +
    'like_count,comments_count,children{media_url,media_type},' +
    'insights.metric(reach,saved,shares,total_interactions,views,likes,comments,profile_visits,follows,' +
    'ig_reels_avg_watch_time,ig_reels_video_view_total_time)';
  const rawMedia = await igAll(`${IG_ID}/media`, { fields: mediaFields });
  const media = rawMedia.map((m) => {
    const ins = {};
    for (const row of m.insights?.data || []) ins[row.name] = row.values?.[0]?.value ?? 0;
    const engagement = (m.like_count || 0) + (m.comments_count || 0) + (ins.saved || 0) + (ins.shares || 0);
    return {
      id: m.id,
      caption: (m.caption || '').slice(0, 220),
      type: m.media_product_type || m.media_type,
      mediaType: m.media_type,
      thumb: m.thumbnail_url || m.media_url,
      permalink: m.permalink,
      timestamp: m.timestamp,
      likes: m.like_count || 0,
      comments: m.comments_count || 0,
      saved: ins.saved || 0,
      shares: ins.shares || 0,
      reach: ins.reach || 0,
      views: ins.views || 0,
      profileVisits: ins.profile_visits || 0,
      follows: ins.follows || 0,
      reelsAvgWatch: ins.ig_reels_avg_watch_time || 0,
      reelsWatchTotal: ins.ig_reels_video_view_total_time || 0,
      interactions: ins.total_interactions || engagement,
      engagement,
      engagementRate: ins.reach ? +((engagement / ins.reach) * 100).toFixed(2) : null,
    };
  });
  coverage.media = `${media.length} publicacions`;

  const contentMix = media.reduce((acc, m) => {
    const key = m.type === 'REELS' ? 'Reels' : m.mediaType === 'CAROUSEL_ALBUM' ? 'Carrusel' : m.mediaType === 'VIDEO' ? 'Vídeo' : 'Imatge';
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});

  // ── 5. Stories actives amb insights ───────────────────────────────────────
  const rawStories = await ig(`${IG_ID}/stories`, {
    fields: 'id,media_type,media_url,thumbnail_url,permalink,timestamp,' +
      'insights.metric(reach,replies,shares,total_interactions,navigation)',
  });
  const stories = (rawStories?.data || []).map((s) => {
    const ins = {};
    for (const row of s.insights?.data || []) ins[row.name] = row.values?.[0]?.value ?? 0;
    return {
      id: s.id, type: s.media_type, thumb: s.thumbnail_url || s.media_url, permalink: s.permalink,
      timestamp: s.timestamp, reach: ins.reach || 0, replies: ins.replies || 0,
      shares: ins.shares || 0, interactions: ins.total_interactions || 0,
    };
  });
  coverage.stories = rawStories ? `${stories.length} actives` : 'no disponible';

  // ── 6. Etiquetes — "Qui ens etiqueta" ─────────────────────────────────────
  const tagsResp = await ig(`${IG_ID}/tags`, {
    fields: 'id,username,caption,media_type,media_url,thumbnail_url,permalink,timestamp,like_count,comments_count',
    limit: 40,
  });
  const mentions = (tagsResp?.data || []).map((t) => ({
    id: t.id, username: t.username, caption: (t.caption || '').slice(0, 160),
    type: t.media_type, thumb: t.thumbnail_url || t.media_url, permalink: t.permalink,
    timestamp: t.timestamp, likes: t.like_count || 0, comments: t.comments_count || 0,
  }));
  coverage.mentions = tagsResp ? `${mentions.length} etiquetes` : 'no disponible';

  // ── 7. Hashtag #somclot — qui parla del barri ─────────────────────────────
  let hashtag = null;
  const hs = await ig('ig_hashtag_search', { user_id: IG_ID, q: 'somclot' });
  const hid = hs?.data?.[0]?.id;
  if (hid) {
    const recent = await ig(`${hid}/recent_media`, {
      user_id: IG_ID,
      fields: 'id,caption,media_type,permalink,like_count,comments_count',
      limit: 25,
    });
    hashtag = {
      tag: '#somclot',
      recent: (recent?.data || []).map((x) => ({
        id: x.id, caption: (x.caption || '').slice(0, 160), type: x.media_type,
        permalink: x.permalink, likes: x.like_count || 0, comments: x.comments_count || 0,
      })),
    };
  }
  coverage.hashtag = hashtag ? `${hashtag.recent.length} publicacions #somclot` : 'no disponible';

  // ── 8. Benchmark de rivals (business_discovery) ───────────────────────────
  let benchmark = null;
  if (existsSync(BENCHMARK_FILE)) {
    try {
      const usernames = JSON.parse(readFileSync(BENCHMARK_FILE, 'utf8')).usernames || [];
      const rivals = [];
      for (const u of usernames) {
        const r = await ig(IG_ID, {
          fields: `business_discovery.username(${u}){username,name,followers_count,media_count,follows_count}`,
        });
        const bd = r?.business_discovery;
        if (bd) rivals.push({ username: bd.username, name: bd.name, followers: bd.followers_count, posts: bd.media_count });
      }
      if (rivals.length) benchmark = { generatedAt: now.toISOString(), rivals: rivals.sort((a, b) => b.followers - a.followers) };
      coverage.benchmark = `${rivals.length} rivals`;
    } catch (e) { errors.push(`benchmark: ${e.message}`); coverage.benchmark = 'error'; }
  } else { coverage.benchmark = 'sense benchmark.json'; }

  // ── 9. Sèrie temporal pròpia (snapshot diari acumulat) ────────────────────
  let history = [];
  if (existsSync(OUT_FILE)) { try { history = JSON.parse(readFileSync(OUT_FILE, 'utf8')).daily || JSON.parse(readFileSync(OUT_FILE, 'utf8')).history || []; } catch { /* */ } }
  const today = ymd(now);
  const todayReach = dailyReach.find((d) => d.date === today)?.value ?? accountInsights.reach?.total ?? null;
  const todayNew = dailyNewFollowers.find((d) => d.date === today)?.value ?? null;
  const snapshot = {
    date: today,
    followers: profile.followers_count ?? null,
    newFollowers: todayNew,
    reach: todayReach,
    profileViews: dailyReach.length ? null : (accountInsights.profile_views?.total ?? null),
  };
  history = history.filter((h) => h.date !== today);
  history.push(snapshot);
  history = history.slice(-HISTORY_MAX);

  const prev = history.length > 1 ? history[history.length - 2] : null;
  const followersDelta = snapshot.newFollowers ?? (prev?.followers != null && snapshot.followers != null ? snapshot.followers - prev.followers : null);

  const withReach = media.filter((m) => m.engagementRate != null);
  const avgEngagementRate = withReach.length ? +(withReach.reduce((a, b) => a + b.engagementRate, 0) / withReach.length).toFixed(2) : null;

  // ── 10. Acumulació mensual + historic.json ────────────────────────────────
  let monthly = {};
  if (existsSync(HISTORIC_FILE)) { try { monthly = { ...(JSON.parse(readFileSync(HISTORIC_FILE, 'utf8')).months || {}) }; } catch { /* */ } }
  if (existsSync(OUT_FILE)) { try { monthly = { ...monthly, ...(JSON.parse(readFileSync(OUT_FILE, 'utf8')).monthly || {}) }; } catch { /* */ } }
  const monKey = today.slice(0, 7);
  const monHist = history.filter((h) => h.date >= `${monKey}-01`);
  const monPosts = media.filter((m) => (m.timestamp || '').slice(0, 7) === monKey);
  const monWR = monPosts.filter((m) => m.engagementRate != null);
  monthly[monKey] = {
    followers: snapshot.followers,
    newFollowers: monHist.reduce((a, b) => a + (b.newFollowers || 0), 0) || monthly[monKey]?.newFollowers || null,
    reach: accountInsights.reach?.total ?? monthly[monKey]?.reach ?? null,
    profileViews: accountInsights.profile_views?.total ?? monthly[monKey]?.profileViews ?? null,
    posts: monPosts.length || monthly[monKey]?.posts || null,
    avgEngagement: monWR.length ? +(monWR.reduce((a, b) => a + b.engagementRate, 0) / monWR.length).toFixed(2) : (monthly[monKey]?.avgEngagement ?? null),
  };

  // ── 11. Escriure data.json ────────────────────────────────────────────────
  const out = {
    meta: {
      generatedAt: now.toISOString(),
      mode: 'live',
      account: profile.username ? `@${profile.username}` : '@cbgrupbarna',
      apiVersion: API,
      coverage,
      errors,
    },
    profile,
    publishLimit: publishLimit?.data || null,
    kpis: {
      followers: profile.followers_count ?? null,
      followersDelta,
      following: profile.follows_count ?? null,
      posts: profile.media_count ?? null,
      reach30: accountInsights.reach?.total ?? null,
      profileViews30: accountInsights.profile_views?.total ?? null,
      accountsEngaged30: accountInsights.accounts_engaged?.total ?? null,
      totalInteractions30: accountInsights.total_interactions?.total ?? null,
      websiteClicks30: accountInsights.website_clicks?.total ?? null,
      avgEngagementRate,
      mentionsCount: mentions.length,
      storiesCount: stories.length,
    },
    accountInsights,
    dailyReach,
    dailyNewFollowers,
    history,
    daily: history,
    media: media.sort((a, b) => b.engagement - a.engagement),
    contentMix,
    stories,
    mentions,
    hashtag,
    benchmark,
    monthly,
    demographics: audience.byCity ? { byCity: audience.byCity } : null, // compat panell antic
    audience,
  };

  if (!existsSync(OUT_DIR)) mkdirSync(OUT_DIR, { recursive: true });
  writeFileSync(OUT_FILE, JSON.stringify(out, null, 2));
  console.log(`✅ data.json escrit.`);
  console.log('   Cobertura:', JSON.stringify(coverage));
  if (errors.length) console.log(`⚠️  ${errors.length} avisos:`, errors.slice(0, 8).join(' | '));
}

main().catch((e) => { console.error('Fatal:', e); process.exit(1); });
