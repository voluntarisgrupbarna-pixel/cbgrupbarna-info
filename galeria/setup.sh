#!/usr/bin/env bash
# CB Grup Barna Galeria — Setup automàtic
# Necessites: Node.js, npm, i els tokens de Supabase i Vercel
# Ús: bash setup.sh

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "🏀 CB Grup Barna — Galeria Setup"
echo "=================================="
echo ""

# Check dependencies
command -v node >/dev/null 2>&1 || { echo "${RED}Error: Node.js no trobat. Instal·la'l a https://nodejs.org${NC}"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "${RED}Error: npm no trobat${NC}"; exit 1; }

echo -e "${GREEN}✓ Node.js $(node --version) trobat${NC}"

# Install Supabase CLI
echo ""
echo "📦 Instal·lant Supabase CLI..."
npm install -g supabase 2>/dev/null || npx supabase --version

# Install Vercel CLI
echo "📦 Instal·lant Vercel CLI..."
npm install -g vercel 2>/dev/null || vercel --version

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PAS 1: Configuració de Supabase"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}Obre https://supabase.com i crea un compte gratuït.${NC}"
echo "Després ves a: Account → Access Tokens → New token"
echo ""
read -p "Enganxa el teu Supabase Access Token: " SUPABASE_ACCESS_TOKEN

# Login to Supabase
echo ""
echo "🔐 Iniciant sessió a Supabase..."
supabase login --token "$SUPABASE_ACCESS_TOKEN"

# Create Supabase project
echo ""
echo "Quin nom vols per al projecte Supabase? (ex: cbgrupbarna-galeria)"
read -p "Nom del projecte: " PROJECT_NAME
echo ""
echo "Contrasenya de la base de dades (mínim 6 caràcters):"
read -sp "Password: " DB_PASSWORD
echo ""
echo "Regió (eu-west-1 per a Irlanda/Europa):"
read -p "Regió [eu-west-1]: " REGION
REGION=${REGION:-eu-west-1}

echo ""
echo "🚀 Creant projecte Supabase '$PROJECT_NAME'..."
PROJECT_JSON=$(supabase projects create "$PROJECT_NAME" --db-password "$DB_PASSWORD" --region "$REGION" --output json)
PROJECT_REF=$(echo "$PROJECT_JSON" | node -e "let d=''; process.stdin.on('data',c=>d+=c); process.stdin.on('end',()=>console.log(JSON.parse(d).id))" 2>/dev/null || echo "$PROJECT_JSON" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$PROJECT_REF" ]; then
  echo -e "${RED}Error creant el projecte. Comprova les credencials.${NC}"
  echo "Crea el projecte manualment a https://supabase.com/dashboard"
  exit 1
fi

echo -e "${GREEN}✓ Projecte creat: $PROJECT_REF${NC}"

# Wait for project to be ready
echo "⏳ Esperant que el projecte estigui llest (30s)..."
sleep 30

# Get API keys
echo "🔑 Obtenint claus API..."
KEYS_JSON=$(supabase projects api-keys --project-ref "$PROJECT_REF" --output json)
ANON_KEY=$(echo "$KEYS_JSON" | node -e "let d=''; process.stdin.on('data',c=>d+=c); process.stdin.on('end',()=>{ const keys=JSON.parse(d); const anon=keys.find(k=>k.name==='anon'); console.log(anon?anon.api_key:''); })" 2>/dev/null)
SERVICE_KEY=$(echo "$KEYS_JSON" | node -e "let d=''; process.stdin.on('data',c=>d+=c); process.stdin.on('end',()=>{ const keys=JSON.parse(d); const svc=keys.find(k=>k.name==='service_role'); console.log(svc?svc.api_key:''); })" 2>/dev/null)

SUPABASE_URL="https://${PROJECT_REF}.supabase.co"

echo -e "${GREEN}✓ Claus obtingudes${NC}"

# Run schema
echo ""
echo "🗄️  Executant l'esquema de base de dades..."
supabase db push --project-ref "$PROJECT_REF" 2>/dev/null || \
  supabase db execute --project-ref "$PROJECT_REF" --file ./supabase/schema.sql || \
  echo -e "${YELLOW}⚠ No s'ha pogut executar l'esquema automàticament. Executa-ho manualment al SQL Editor de Supabase.${NC}"

# Create .env.local
echo ""
echo "📝 Creant .env.local..."
cat > .env.local << EOF
NEXT_PUBLIC_SUPABASE_URL=${SUPABASE_URL}
NEXT_PUBLIC_SUPABASE_ANON_KEY=${ANON_KEY}
SUPABASE_SERVICE_ROLE_KEY=${SERVICE_KEY}
EOF

echo -e "${GREEN}✓ .env.local creat${NC}"

# Install npm deps
echo ""
echo "📦 Instal·lant dependències..."
npm install

# Test build
echo ""
echo "🔨 Compilant l'aplicació..."
npm run build

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PAS 2: Deploy a Vercel"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}Obre https://vercel.com i crea un compte gratuït.${NC}"
echo "Després ves a: Settings → Tokens → Create Token"
echo ""
read -p "Enganxa el teu Vercel Token: " VERCEL_TOKEN

echo ""
echo "🚀 Fent deploy a Vercel..."
VERCEL_TOKEN="$VERCEL_TOKEN" vercel deploy --prod \
  --env NEXT_PUBLIC_SUPABASE_URL="$SUPABASE_URL" \
  --env NEXT_PUBLIC_SUPABASE_ANON_KEY="$ANON_KEY" \
  --env SUPABASE_SERVICE_ROLE_KEY="$SERVICE_KEY" \
  --yes 2>&1 | tee /tmp/vercel_output.txt

DEPLOY_URL=$(grep "https://" /tmp/vercel_output.txt | tail -1 | tr -d ' ')

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ GALERIA DESPLEGADA!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "URL:     ${GREEN}${DEPLOY_URL}${NC}"
echo -e "Supabase: ${GREEN}https://supabase.com/dashboard/project/${PROJECT_REF}${NC}"
echo ""
echo "PROPER PAS:"
echo "1. Ves a Supabase → Storage → New bucket → Nom: 'photos' → Public ✓"
echo "2. Entra a la galeria, crea el teu compte"
echo "3. A Supabase → Table Editor → profiles → canvia el teu role a 'admin'"
echo ""
