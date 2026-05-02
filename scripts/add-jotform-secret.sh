#!/usr/bin/env bash
# Afegeix el secret JOTFORM_API_KEY al repo cbgrupbarna-info de GitHub
# La clau no surt del teu ordinador (es xifra abans d'enviar-la a GitHub).
#
# Ús:  bash scripts/add-jotform-secret.sh
#      (et demanarà la clau, l'enganxes, premes Enter)

set -euo pipefail

REPO="voluntarisgrupbarna-pixel/cbgrupbarna-info"
SECRET_NAME="JOTFORM_API_KEY"
WORKFLOW_FILE="update-counters.yml"

# 1. Llegim el token de GitHub del Keychain (el mateix que git fa servir)
TOKEN=$(printf "host=github.com\nprotocol=https\n\n" | git credential fill 2>/dev/null | awk -F= '/^password=/{print $2}')
if [ -z "$TOKEN" ]; then
  echo "❌ No tens token de GitHub al Keychain. Fes un 'git push' una vegada per què hi quedi guardat."
  exit 1
fi

# 2. Demanem la clau de JotForm (input ocult)
echo ""
echo "📋 Pas 1: vés a https://www.jotform.com/myaccount/api"
echo "   Clica 'Create New Key' (Read Only) i copia el valor."
echo ""
echo -n "🔑 Enganxa la teva JotForm API key i prem Enter: "
read -rs JOTFORM_KEY
echo ""
if [ -z "$JOTFORM_KEY" ]; then
  echo "❌ No has enganxat cap clau. Sortint."
  exit 1
fi

# 3. Comprovem que la clau funciona
echo "🔍 Comprovant la clau a JotForm..."
TEST=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 \
  "https://api.jotform.com/user?apiKey=$JOTFORM_KEY")
if [ "$TEST" != "200" ]; then
  echo "❌ JotForm rebutja la clau (HTTP $TEST). Tornar a copiar-la i provar-la."
  exit 1
fi
echo "✅ Clau vàlida."

# 4. Demanem el public key del repo per xifrar
PK_JSON=$(curl -s -H "Authorization: token $TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO/actions/secrets/public-key")
KEY_ID=$(echo "$PK_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['key_id'])")
PUBLIC_KEY=$(echo "$PK_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['key'])")

# 5. Comprovem que pynacl està instal·lat (per xifrar el secret)
if ! python3 -c "import nacl" 2>/dev/null; then
  echo "📦 Instal·lant pynacl per xifrar el secret (només fa falta una vegada)..."
  python3 -m pip install --user --quiet pynacl
fi

# 6. Xifrem el secret amb la public key del repo
ENCRYPTED=$(JOTFORM_KEY="$JOTFORM_KEY" PUBLIC_KEY="$PUBLIC_KEY" python3 - <<'PYEOF'
import os, base64, nacl.public, nacl.encoding
key = os.environ['JOTFORM_KEY'].encode()
pk = nacl.public.PublicKey(os.environ['PUBLIC_KEY'].encode(), nacl.encoding.Base64Encoder())
sealed = nacl.public.SealedBox(pk).encrypt(key)
print(base64.b64encode(sealed).decode())
PYEOF
)

# 7. PUT del secret xifrat a GitHub
RESP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO/actions/secrets/$SECRET_NAME" \
  -d "{\"encrypted_value\":\"$ENCRYPTED\",\"key_id\":\"$KEY_ID\"}")

case "$RESP_CODE" in
  201) echo "✅ Secret '$SECRET_NAME' creat correctament." ;;
  204) echo "✅ Secret '$SECRET_NAME' actualitzat." ;;
  *) echo "❌ Error pujant el secret a GitHub (HTTP $RESP_CODE)."; exit 1 ;;
esac

# 8. Disparem el workflow per actualitzar data.json al moment
echo "🚀 Disparant el workflow per actualitzar data.json..."
curl -s -X POST -H "Authorization: token $TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO/actions/workflows/$WORKFLOW_FILE/dispatches" \
  -d '{"ref":"main"}' > /dev/null

echo ""
echo "🎉 Tot llest. En 30-60 segons cbgrupbarna.info mostrarà els números reals de JotForm."
echo "   Comprova-ho a: https://github.com/$REPO/actions"
