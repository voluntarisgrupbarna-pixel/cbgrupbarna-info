# Backup automàtic del repositori

`.github/workflows/backup-mirror.yml` fa cada nit un `git push` incremental
de `main` cap a un repositori de backup separat. Substitueix el procediment
manual que hi havia documentat a la skill `mapa-web-cbgb` (§9): abans calia
que algú se'n recordés d'executar-lo a mà; ara corre sol.

Perquè funcioni cal donar d'alta **dos secrets, un sol cop**:

## 1. Crear el repositori de backup (si encara no existeix)

Amb el compte `voluntarisgrupbarna-pixel` (o qui tingui accés):
[github.com/new](https://github.com/new) → nom `cbgrupbarna-info-backup` →
**privat** → sense README ni `.gitignore` (ha de quedar completament buit).

Si ja existeix un repositori de backup fet amb el procediment manual antic,
fes servir aquest mateix i salta aquest pas.

## 2. Crear un token amb accés només a aquest repositori

[github.com/settings/personal-access-tokens/new](https://github.com/settings/personal-access-tokens/new)
→ **fine-grained token** → "Repository access" → **Only select repositories**
→ tria `cbgrupbarna-info-backup` → permís **Contents: Read and write**.
Copia el token (comença per `github_pat_…`).

Un token fine-grained limitat a aquest sol repositori: si mai es filtrés,
només afectaria la còpia de backup, no tot el compte ni el repositori
principal.

## 3. Donar d'alta els dos secrets al repositori principal

Al repositori `cbgrupbarna-info` (el principal, no el de backup):
**Settings → Secrets and variables → Actions → New repository secret**.

| Secret | Valor |
|---|---|
| `BACKUP_REPO_URL` | `https://github.com/voluntarisgrupbarna-pixel/cbgrupbarna-info-backup.git` |
| `BACKUP_REPO_TOKEN` | el token `github_pat_…` del pas 2 |

## Fet

A partir d'aquí, cada nit a les 03:00 UTC el workflow fa un `git push`
incremental cap al backup. Es pot llançar a mà en qualsevol moment des de la
pestanya **Actions → backup · mirall del repositori → Run workflow**.

Si algun dels dos secrets no s'ha donat d'alta encara, el workflow ho diu
(`::notice::`) i surt en verd sense fer res — no és un error, només falta
aquest pas manual d'un cop.

## Coses a saber

- **Només `main`.** Si es vol protegir també una altra branca de llarga
  vida, cal afegir-hi el mateix `git push backup HEAD:refs/heads/<branca>`
  amb un altre pas.
- **El primer push pot trigar.** El repositori pesa uns 5,3 GB (sobretot
  fotos): la primera vegada que el backup existeixi buit, aquest workflow
  hi pujarà tot l'historial de cop, cosa que pot ser lenta o fer `time-out`
  al runner (`timeout-minutes: 30` de marge). Si passa, fes el primer
  mirall a mà seguint el procediment per trossos de `mapa-web-cbgb` §9 (un
  commit darrere l'altre) i deixa que aquest workflow s'encarregui només
  dels pushos incrementals posteriors, que sí que són ràpids.
- **Per Supabase** (dades de `galeria/`, no viuen a git): aquest workflow
  no les toca. Cal un `pg_dump` a part — vegeu `mapa-web-cbgb` §9, «Nivell
  2».
- **Si el workflow falla** (per exemple, secrets caducats), s'obre
  automàticament un issue etiquetat `robot-caigut` al repositori, igual que
  la resta de robots del web.
