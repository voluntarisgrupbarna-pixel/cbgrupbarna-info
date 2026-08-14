/**
 * CB Grup Barna · Premi Dona i Esport · Cercador amb IA
 * Cloudflare Worker + Workers AI (gratuït, sense clau d'API externa).
 *
 * Desplegament: veure premidonaesport/cf-worker/README.md
 */

const INDEX = [
  { t: "Portada", c: "Inici", u: "/premidonaesport/", k: "home inici experiència" },
  { t: "Resum Executiu", c: "Candidatura", u: "/premidonaesport/resum-executiu.html", k: "candidatura completa dossier presentació institut barcelona esports" },
  { t: "Candidatura CB Grup Barna 2026 (PDF)", c: "Candidatura · Document", u: "/premidonaesport/assets/docs/candidatura-cb-grup-barna-2026.pdf", k: "pdf descarregar projecte candidatura" },
  { t: "El Mètode Barna", c: "El Mètode", u: "/premidonaesport/el-metode.html", k: "3 pilars metode narrativa publica igualtat 60 anys" },
  { t: "Mètode Barna · Versió acadèmica completa", c: "El Mètode", u: "/premidonaesport/metode-extern.html", k: "academic doctoral UB INEFC investigacio marc teoric complet" },
  { t: "Mètode Barna · Document principal (DOCX)", c: "El Mètode · Document", u: "/premidonaesport/assets/docs/metode-barna.docx", k: "docx word descarregar metode" },
  { t: "Tesi Integrada · Model Barna (DOCX)", c: "El Mètode · Document", u: "/premidonaesport/assets/docs/tesi-integrada-model-barna.docx", k: "tesi model barna docx" },
  { t: "T1 · Mercat Invisible", c: "Les 5 Teories", u: "/premidonaesport/teories/t1.html", k: "teoria 1 mercat invisible" },
  { t: "T2 · Escala de Reconeixement", c: "Les 5 Teories", u: "/premidonaesport/teories/t2.html", k: "teoria 2 escala reconeixement" },
  { t: "T3 · Irreversibilitat", c: "Les 5 Teories", u: "/premidonaesport/teories/t3.html", k: "teoria 3 irreversibilitat" },
  { t: "T4 · Desfasament", c: "Les 5 Teories", u: "/premidonaesport/teories/t4.html", k: "teoria 4 desfasament" },
  { t: "T5 · Autenticitat", c: "Les 5 Teories", u: "/premidonaesport/teories/t5.html", k: "teoria 5 autenticitat" },
  { t: "Bibliografia", c: "Les 5 Teories", u: "/premidonaesport/bibliografia.html", k: "fonts referencies cites academic" },
  { t: "Informe Unificat BCN-CAT", c: "Investigació", u: "/premidonaesport/investigacio/informe-unificat.html", k: "informe unificat barcelona catalunya" },
  { t: "Informe Unificat BCN-CAT 2026 (DOCX)", c: "Investigació · Document", u: "/premidonaesport/assets/docs/informe-unificat.docx", k: "docx unificat def" },
  { t: "Informe Unificat Femení BCN-CAT versió extensa (DOCX)", c: "Investigació · Document", u: "/premidonaesport/assets/docs/informe-unificat-femeni-extens.docx", k: "docx femeni extens" },
  { t: "Informe Baloncesto Femenino Barcelona ES (DOCX)", c: "Investigació · Document", u: "/premidonaesport/assets/docs/informe-baloncesto-femenino-es.docx", k: "docx castella espanyol baloncesto" },
  { t: "Informe Complet", c: "Investigació", u: "/premidonaesport/investigacio/informe-complet.html", k: "informe complet basquet barcelona clubs" },
  { t: "Informe Complet Bàsquet Barcelona 2026 FINAL (DOCX)", c: "Investigació · Document", u: "/premidonaesport/assets/docs/informe-complet.docx", k: "docx final complet" },
  { t: "Informe Complet i Unificat amb Propostes (DOCX)", c: "Investigació · Document", u: "/premidonaesport/assets/docs/informe-complet-amb-propostes.docx", k: "docx propostes" },
  { t: "Informe Complet i Unificat versió formatada (DOCX)", c: "Investigació · Document", u: "/premidonaesport/assets/docs/informe-complet-format.docx", k: "docx format" },
  { t: "Recerca Macro a Micro", c: "Investigació", u: "/premidonaesport/investigacio/recerca.html", k: "recerca basquet catala macro micro" },
  { t: "Recerca Bàsquet Català De Macro a Micro (DOCX)", c: "Investigació · Document", u: "/premidonaesport/assets/docs/recerca-macro-micro.docx", k: "docx recerca" },
  { t: "Recerca versió extensa amb imatges (DOCX)", c: "Investigació · Document", u: "/premidonaesport/assets/docs/recerca-macro-micro-extens.docx", k: "docx extens imatges" },
  { t: "Patrons Ocults · Cum Laude", c: "Investigació", u: "/premidonaesport/investigacio/patrons.html", k: "patrons ocults cum laude tesi doctoral" },
  { t: "Mètode Barna · Patrons Ocults (DOCX)", c: "Investigació · Document", u: "/premidonaesport/assets/docs/patrons-ocults.docx", k: "docx patrons ocults" },
  { t: "Mètode Barna · Patrons Ocults versió 2 (DOCX)", c: "Investigació · Document", u: "/premidonaesport/assets/docs/patrons-ocults-v2.docx", k: "docx patrons ocults v2" },
  { t: "Tesi Doctoral · Bretxa Gènere Bàsquet 2026 (DOCX)", c: "Investigació · Document", u: "/premidonaesport/assets/docs/tesi-doctoral.docx", k: "docx tesi doctoral bretxa genere" },
  { t: "Talento sin Reconocer · Presentació (PPTX)", c: "Investigació · Document", u: "/premidonaesport/assets/docs/talento-sin-reconocer.pptx", k: "pptx powerpoint presentacio talento" },
  { t: "Fons Barna 8M", c: "Investigació", u: "/premidonaesport/investigacio/dossier-8m.html", k: "8m fons entrenadores beca fcbq" },
  { t: "Dossier 8M FCBQ CB Grup Barna DEF (DOCX)", c: "Investigació · Document", u: "/premidonaesport/assets/docs/dossier-8m.docx", k: "docx dossier 8m" },
  { t: "L'Efecte Ainhoa", c: "El Club", u: "/premidonaesport/el-club/ainhoa.html", k: "ainhoa embaixadora jugadora efecte" },
  { t: "Proposta Embaixadora Ainhoa v3 (DOCX)", c: "El Club · Document", u: "/premidonaesport/assets/docs/proposta-ainhoa.docx", k: "docx ainhoa proposta embaixadora" },
  { t: "Barna Màgics", c: "El Club", u: "/premidonaesport/el-club/magics.html", k: "magics equip inclusio" },
  { t: "Línia Femenina", c: "El Club", u: "/premidonaesport/el-club/linia.html", k: "linia femenina equips" },
  { t: "Pipeline Femení", c: "El Club", u: "/premidonaesport/pipeline-femeni.html", k: "pipeline 13 equips base senior cantera" },
  { t: "Visita de l'Alcalde", c: "Comunitat", u: "/premidonaesport/comunitat/alcalde.html", k: "alcalde berni escude 9 febrer ajuntament" },
  { t: "3x3 Westfield Glòries", c: "Comunitat", u: "/premidonaesport/comunitat/3x3-westfield.html", k: "3x3 westfield glories torneig carrer" },
  { t: "Instagram del club", c: "Comunitat", u: "/premidonaesport/comunitat/instagram.html", k: "instagram xarxes socials" },
  { t: "Dossier de Patrocinis", c: "Patrocinis", u: "/premidonaesport/patrocinis/index.html", k: "patrocinis sponsors dossier empreses" },
  { t: "Informe de lideratge · Clubs TOP Barcelona (XLSX)", c: "Patrocinis · Document", u: "/premidonaesport/assets/docs/informe-lideratge-cb-grup-barna.xlsx", k: "xlsx excel lideratge clubs top" },
  { t: "Dones Empresàries", c: "Patrocinis", u: "/premidonaesport/patrocinis/dones.html", k: "dones empresaries patrocini" },
  { t: "Presentació del Club", c: "Altres", u: "/premidonaesport/presentacio.html", k: "presentacio general club 450 families" },
  { t: "Tots els documents · Recopilació completa", c: "Índex", u: "/premidonaesport/documents.html", k: "tots documents recopilacio index cercar buscar llista completa" },
];

const ALLOWED_ORIGINS = new Set([
  "https://cbgrupbarna.info",
  "http://localhost:8099",
]);

function corsHeaders(origin) {
  const allow = ALLOWED_ORIGINS.has(origin) ? origin : "https://cbgrupbarna.info";
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json; charset=utf-8",
  };
}

function buildPrompt(query) {
  const list = INDEX.map((e, i) => `${i}. "${e.t}" [${e.c}] — paraules clau: ${e.k}`).join("\n");
  return (
    `Ets el cercador de la web de la candidatura del CB Grup Barna al Premi Dona i Esport. ` +
    `Aquest és l'índex complet de contingut (número, títol, categoria, paraules clau):\n\n${list}\n\n` +
    `Consulta de l'usuari: "${query}"\n\n` +
    `Retorna NOMÉS un array JSON amb els números (índexs) dels 5 elements més rellevants per a aquesta consulta, ` +
    `ordenats de més a menys rellevant. Interpreta la intenció encara que la consulta faci servir sinònims, ` +
    `un idioma diferent (castellà/català/anglès) o descrigui el contingut sense usar les paraules exactes del títol. ` +
    `Si cap element és clarament rellevant, retorna un array buit. ` +
    `Format de resposta obligatori, sense cap altre text: [2, 15, 0]`
  );
}

function extractJsonArray(text) {
  const match = text.match(/\[[\d,\s]*\]/);
  if (!match) return [];
  try {
    const arr = JSON.parse(match[0]);
    return Array.isArray(arr) ? arr.filter((n) => Number.isInteger(n) && n >= 0 && n < INDEX.length) : [];
  } catch {
    return [];
  }
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders(origin) });
    }

    let query = "";
    if (request.method === "POST") {
      try {
        const body = await request.json();
        query = (body.q || "").toString().slice(0, 200);
      } catch {
        query = "";
      }
    } else {
      const url = new URL(request.url);
      query = (url.searchParams.get("q") || "").slice(0, 200);
    }

    if (!query.trim()) {
      return new Response(JSON.stringify({ results: [] }), { headers: corsHeaders(origin) });
    }

    try {
      const aiResponse = await env.AI.run("@cf/meta/llama-3.1-8b-instruct", {
        messages: [{ role: "user", content: buildPrompt(query) }],
        max_tokens: 120,
      });
      const text = aiResponse.response || "";
      const indices = extractJsonArray(text);
      const results = indices.map((i) => INDEX[i]);
      return new Response(JSON.stringify({ results, query }), { headers: corsHeaders(origin) });
    } catch (err) {
      return new Response(JSON.stringify({ results: [], error: "ai_unavailable" }), {
        headers: corsHeaders(origin),
        status: 200, // 200 perquè el frontend faci fallback net, no un error de xarxa
      });
    }
  },
};
