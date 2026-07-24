#!/usr/bin/env node
/**
 * fetch-instagram.mjs — Recol·lector de dades de la Instagram Graph API per al
 * Panell d'Instagram del CB Grup Barna (@cbgrupbarna).
 *
 * S'executa des del GitHub Action `instagram-panel.yml`. Fa servir un token
 * d'accés guardat a GitHub Secrets (mai al codi) i escriu `panel-instagram/data.json`,
 * que la pàgina estàtica llegeix. Zero servidor, token segur.
 *
 * Variables d'entorn necessàries:
 *   IG_ACCESS_TOKEN   Token d'accés de llarga durada (User o System User) amb permisos
 *                     instagram_basic, instagram_manage_insights, instagram_manage_comments,
 *                     pages_read_engagement, pages_show_list.
 *   IG_USER_ID        ID del compte de Instagram Business/Creator (ig-user-id numèric).
 *   IG_API_VERSION    (opcional) versió de l'API, per defecte v21.0.
 *
 * Filosofia: robust. Cada crida va dins d'un try/catch; si un endpoint falla
 * (permís que falta, mètrica desactivada en la versió...), es registra a `meta.errors`
 * i la resta del panell segueix funcionant amb el que sí que ha arribat.
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const OUT_DIR = join(ROOT, 'panel-instagram');
const OUT_FILE = join(OUT_DIR, 'data.json');

const TOKEN = process.env.IG_ACCESS_TOKEN;
const IG_ID = process.env.IG_USER_ID;
const API = process.env.IG_API_VERSION || 'v21.0';
const BASE = `https://graph.facebook.com/${API}`;
const HISTORY_MAX = 180; // dies de sèrie temporal que acumulem nosaltres

const errors = [];
const now = new Date();

/** Crida a l'API amb gestió d'errors. Retorna l'objecte JSON o null. */
async function ig(path, params = {}) {
  const url = new URL(`${BASE}/${path}`);
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  url.searchParams.set('access_token', TOKEN);
  try {
    const res = await fetch(url);
    const json = await res.json();
    if (json.error) {
      errors.push(`${path}: ${json.error.message} (code ${json.error.code})`);
      return null;
    }
    return json;
  } catch (e) {
    errors.push(`${path}: ${e.message}`);
    return null;
  }
}

/** ISO YYYY-MM-DD en zona local del runner (UTC al Action). */
function ymd(d) {
  return d.toISOString().slice(0, 10);
}

async function main() {
  if (!TOKEN || !IG_ID) {
    console.error('❌ Falten IG_ACCESS_TOKEN o IG_USER_ID. Deixo data.json intacte (mode demo).');
    process.exit(0); // no trenquem el panell; segueix amb la demo existent
  }

  // ── 1. Perfil ────────────────────────────────────────────────────────────
  const profile = await ig(IG_ID, {
    fields: 'username,name,biography,followers_count,follows_count,media_count,profile_picture_url,website',
  }) || {};

  // ── 2. Insights del compte (últims 30 dies) ──────────────────────────────
  // Les mètriques a nivell de compte canvien entre versions; provem les robustes.
  const since = Math.floor((now.getTime() - 29 * 864e5) / 1000);
  const until = Math.floor(now.getTime() / 1000);

  const accountInsights = {};
  for (const metric of ['reach', 'profile_views']) {
    const r = await ig(`${IG_ID}/insights`, {
      metric,
      period: 'day',
      since,
      until,
      metric_type: 'total_value',
    });
    // total_value dona un únic agregat; provem també sèrie diària com a fallback
    if (r?.data?.[0]?.total_value?.value != null) {
      accountInsights[metric] = { total: r.data[0].total_value.value };
    } else {
      const r2 = await ig(`${IG_ID}/insights`, { metric, period: 'day', since, until });
      if (r2?.data?.[0]?.values) {
        const values = r2.data[0].values.map((v) => ({ date: v.end_time?.slice(0, 10), value: v.value }));
        accountInsights[metric] = { total: values.reduce((a, b) => a + (b.value || 0), 0), series: values };
      }
    }
  }

  // Demografia d'audiència (pot no estar disponible per a comptes petits)
  let demographics = null;
  const demo = await ig(`${IG_ID}/insights`, {
    metric: 'follower_demographics',
    period: 'lifetime',
    metric_type: 'total_value',
    breakdown: 'city',
  });
  if (demo?.data?.[0]?.total_value?.breakdowns?.[0]?.results) {
    demographics = {
      byCity: demo.data[0].total_value.breakdowns[0].results
        .map((r) => ({ label: r.dimension_values?.[0], value: r.value }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 8),
    };
  }

  // ── 3. Publicacions recents amb insights ─────────────────────────────────
  const mediaFields =
    'id,caption,media_type,media_product_type,media_url,thumbnail_url,permalink,timestamp,like_count,comments_count,insights.metric(reach,saved,shares,total_interactions,views)';
  const mediaResp = await ig(`${IG_ID}/media`, { fields: mediaFields, limit: 30 });
  const media = (mediaResp?.data || []).map((m) => {
    const ins = {};
    for (const row of m.insights?.data || []) ins[row.name] = row.values?.[0]?.value ?? 0;
    const engagement = (m.like_count || 0) + (m.comments_count || 0) + (ins.saved || 0) + (ins.shares || 0);
    return {
      id: m.id,
      caption: (m.caption || '').slice(0, 160),
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
      interactions: ins.total_interactions || engagement,
      engagement,
      engagementRate: ins.reach ? +((engagement / ins.reach) * 100).toFixed(2) : null,
    };
  });

  // Barreja de contingut (reels / imatge / carrusel)
  const contentMix = media.reduce((acc, m) => {
    const key = m.type === 'REELS' ? 'Reels' : m.mediaType === 'CAROUSEL_ALBUM' ? 'Carrusel' : m.mediaType === 'VIDEO' ? 'Vídeo' : 'Imatge';
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});

  // ── 4. Etiquetes / mencions — "Qui ens etiqueta" (estil Hootsuite) ────────
  const tagsResp = await ig(`${IG_ID}/tags`, {
    fields: 'id,username,caption,media_type,media_url,thumbnail_url,permalink,timestamp,like_count,comments_count',
    limit: 30,
  });
  const mentions = (tagsResp?.data || []).map((t) => ({
    id: t.id,
    username: t.username,
    caption: (t.caption || '').slice(0, 140),
    type: t.media_type,
    thumb: t.thumbnail_url || t.media_url,
    permalink: t.permalink,
    timestamp: t.timestamp,
    likes: t.like_count || 0,
    comments: t.comments_count || 0,
  }));

  // ── 5. Sèrie temporal pròpia (acumulem un snapshot diari) ─────────────────
  let history = [];
  if (existsSync(OUT_FILE)) {
    try {
      history = JSON.parse(readFileSync(OUT_FILE, 'utf8')).history || [];
    } catch { /* ignore */ }
  }
  const today = ymd(now);
  const snapshot = {
    date: today,
    followers: profile.followers_count ?? null,
    following: profile.follows_count ?? null,
    posts: profile.media_count ?? null,
    reach30: accountInsights.reach?.total ?? null,
    profileViews30: accountInsights.profile_views?.total ?? null,
  };
  history = history.filter((h) => h.date !== today);
  history.push(snapshot);
  history = history.slice(-HISTORY_MAX);

  // Δ vs snapshot anterior
  const prev = history.length > 1 ? history[history.length - 2] : null;
  const deltas = {
    followers: prev?.followers != null && snapshot.followers != null ? snapshot.followers - prev.followers : null,
  };

  // Taxa d'engagement mitjana de les publicacions amb reach
  const withReach = media.filter((m) => m.engagementRate != null);
  const avgEngagementRate = withReach.length
    ? +(withReach.reduce((a, b) => a + b.engagementRate, 0) / withReach.length).toFixed(2)
    : null;

  // ── 6. Escriure data.json ────────────────────────────────────────────────
  const out = {
    meta: {
      generatedAt: now.toISOString(),
      mode: 'live',
      account: profile.username ? `@${profile.username}` : '@cbgrupbarna',
      apiVersion: API,
      errors,
    },
    profile,
    kpis: {
      followers: profile.followers_count ?? null,
      followersDelta: deltas.followers,
      following: profile.follows_count ?? null,
      posts: profile.media_count ?? null,
      reach30: accountInsights.reach?.total ?? null,
      profileViews30: accountInsights.profile_views?.total ?? null,
      avgEngagementRate,
      mentionsCount: mentions.length,
    },
    history,
    media: media.sort((a, b) => b.engagement - a.engagement),
    contentMix,
    mentions,
    demographics,
  };

  if (!existsSync(OUT_DIR)) mkdirSync(OUT_DIR, { recursive: true });
  writeFileSync(OUT_FILE, JSON.stringify(out, null, 2));
  console.log(`✅ data.json escrit — ${media.length} posts, ${mentions.length} mencions, ${errors.length} errors.`);
  if (errors.length) console.log('⚠️  Errors:', errors.join(' | '));
}

main().catch((e) => {
  console.error('Fatal:', e);
  process.exit(1);
});
