# 🧬 Co-Scientist Agent Skill: Quick Start & Test Cases

This directory contains the native Antigravity skill configuration for `co-scientist-agent`. 

Since this folder resides inside your active workspace at `.gemini/skills/co-scientist-agent/`, it is automatically detected by the Antigravity runtime during execution and is fully version-controlled, allowing you to back it up on your GitHub repository.

---

## 🚀 How to Activate

Simply type a prompt containing `/co-scientist` or "Co-Scientist Mode" in the chat interface. The system will activate the multi-agent planning loops defined in `SKILL.md`.

---

## 🧪 Domain-Specific Test Prompts

You can use the following pre-calibrated test cases to verify the orchestration:

### 1. Biomolecular Zoonotics (Biology Domain)
> **Prompt:** 
> `/co-scientist --domain science --query "Investigate the molecular mechanism of beta-lactamase (ESBL) resistance selection induced by veterinary enrofloxacin in Salmonella enterica isolates from Veracruz"`

*Expected Behavior:*
- Passes through Phase 0 (Safety Gate).
- Spawns parallel proposers to fetch papers from PubMed/OpenAlex.
- Evaluates resistance pathways and structure predictions using AlphaFold/UniProt.
- Generates a `co_scientist_salmonella_esbl_report.md` Nature-style paper.

### 2. High-Performance ML Architectures (ML Domain)
> **Prompt:** 
> `/co-scientist --domain ml --query "Design a Spatial-Genomic hybrid neural operator that dynamically scales contagion rate beta in a network of Mexican highways, leveraging Transformer-Mamba integration"`

*Expected Behavior:*
- Spawns parallel proposers using arXiv database tools.
- Evaluates spatial scaling complexity (Big-O spatial memory scaling).
- Actively reads `src/spatial_model/03c_spatial_sir_genomic.py` to tailor dynamic parameter injection.
- Generates a `co_scientist_mamba_sir_report.md` NeurIPS-style paper.

---

## 📦 Version Control

This skill is structured to be committed to Git:
```bash
git add .gemini/skills/co-scientist-agent/
git commit -m "feat: integrate native co-scientist-agent Antigravity skill with subagent arena"
git push origin main
```
This guarantees that even if your IDE state is reset, your research workflows are permanently backed up alongside your codebase.
