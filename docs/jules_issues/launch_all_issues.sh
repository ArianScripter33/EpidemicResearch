#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# Jules Issues Launch Script — EpidemicResearch
# Run this AFTER: gh auth login
# ═══════════════════════════════════════════════════════════════
# Usage: bash docs/jules_issues/launch_all_issues.sh

set -e
REPO="ArianScripter33/EpidemicResearch"

echo "🚀 Launching 4 Jules issues to $REPO..."

# Create 'jules' label if it doesn't exist
gh label create "jules" --color "0E8A16" --description "Issues assigned to Jules async agent" --repo "$REPO" 2>/dev/null || echo "Label 'jules' already exists, continuing..."

# ── ISSUE 1: DGE Morbilidad 2018-2024 (HIGH PRIORITY) ────────

gh issue create \
  --repo "$REPO" \
  --title "[DATA] DGE Morbilidad 2018-2024: Find + extract updated CSV data beyond 2015-2017" \
  --label "jules" \
  --body-file "docs/jules_issues/issue_01_dge_2018_2024.md"

echo "✅ Issue 1 created: DGE 2018-2024"

# ── ISSUE 2: openFMD + Kaggle FMD Dataset (HIGH PRIORITY) ────
gh issue create \
  --repo "$REPO" \
  --title "[DATA] openFMD: Find real CSV download URL + Kaggle FMD dataset acquisition" \
  --label "jules" \
  --body-file "docs/jules_issues/issue_02_openfmd_kaggle.md"

echo "✅ Issue 2 created: openFMD + Kaggle"

# ── ISSUE 3: COFEPRIS Clausuras + PUCRA RAM (MEDIUM) ─────────
gh issue create \
  --repo "$REPO" \
  --title "[DATA] COFEPRIS clausuras + PUCRA RAM: extract antimicrobial resistance tables" \
  --label "jules" \
  --body-file "docs/jules_issues/issue_03_cofepris_pucra.md"

echo "✅ Issue 3 created: COFEPRIS + PUCRA"

# ── ISSUE 4: SENASICA Cuarentenas PDFs (MEDIUM) ───────────────
gh issue create \
  --repo "$REPO" \
  --title "[DATA] SENASICA: Extract quarterly quarantine PDFs 2023-2024 + API exploration" \
  --label "jules" \
  --body-file "docs/jules_issues/issue_04_senasica_cuarentenas.md"

echo "✅ Issue 4 created: SENASICA Cuarentenas"

echo ""
echo "═══════════════════════════════════════════════"
echo "🎯 All 4 Jules issues created!"
echo "View at: https://github.com/$REPO/issues?q=label:jules"
echo "═══════════════════════════════════════════════"
