---
name: co-scientist-agent
description: >-
  Orchestrates a dual-domain AI Co-Scientist protocol (Molecular Biology and Machine Learning research)
  using parallel subagents, socratic debate, Elo tournaments, and automatic literature/code integration.
---

# Co-Scientist Agent: Dual-Domain Research Orchestrator

## Overview
The `co-scientist-agent` is an instruction-only, enterprise-grade skill that transforms the Antigravity agent into a high-rigor Scientific and ML Research Orchestrator. It implements the multi-agent *AI Co-Scientist* protocol developed by Google DeepMind (Brainstorming -> Critique -> Tournament Arena -> Synthesis).

This skill leverages parallel subagents to generate independent research vectors, subject them to socratic critique, rank them quantitatively using a simulated Elo system, and synthesize the winning hypothesis into a publication-ready Markdown Artifact.

---

## Dependencies
This skill coordinates and builds upon the following installed core skills:
- **Biomolecular Databases:** `ensembl-database`, `uniprot-database`, `alphafold-database-fetch-and-analyze`
- **Scientific Literature:** `pubmed-database`, `literature-search-arxiv`, `literature-search-openalex`
- **System Utilities:** `run_command`, `write_to_file`

---

## Quick Start
To trigger this skill, the user can invoke the slash command `/co-scientist` or enter a prompt containing the term "Co-Scientist Mode" along with a research goal. 

**Example Prompts:**
*   `/co-scientist --domain ml --query "Hybrid Transformer-Mamba architecture for dynamic spatial contagion prediction"`
*   `Co-Scientist Mode: Research the genomic signature of multi-drug resistant Salmonella enterica in agricultural regions of Mexico.`

---

## Workflow (Instruction-Only Protocol)

The orchestrating agent MUST follow these five distinct phases sequentially:

### Phase 0: Pre-Flight Safety Gate (Double-Confirmation)
To protect token quotas, before executing any parallel subagents or literature searches, the agent MUST present a brief plan to the user:
1.  **Scope Summary:** A breakdown of the selected domain (Science or ML), the query, and the planned subagent instances (e.g., 2 Proposers, 2 Critics, 1 Judge).
2.  **Estimate Token Profile:** Inform the user of the expected computation scale.
3.  **Active Confirmation Request:** Present the user with a single-choice confirmation gate. The agent **MUST STOP** and wait for the user to explicitly say `"Proceder"`, `"Execute"`, or `"Dale"` before starting Phase 1.

---

### Phase 1: Domain Routing & Parallel Brainstorming
Once approved, the agent identifies the domain and runs the following parallel tasks:
*   **Domain A: Science (Molecular Biology)**
    *   **Orchestration:** Spin up 2 subagents in parallel (Proposer Alpha and Proposer Beta).
    *   **Proposer Alpha:** Tasked with researching the standard literature using `pubmed-database` and `literature-search-openalex` to build a highly viable, conservative hypothesis.
    *   **Proposer Beta:** Tasked with proposing a high-risk, high-reward contrarian hypothesis.
*   **Domain B: Machine Learning (AI Research)**
    *   **Orchestration:** Spin up 2 parallel subagents (Proposer Alpha and Proposer Beta).
    *   **Proposer Alpha:** Standard state-of-the-art model structures (e.g., standard Graph Neural Networks or Spatial Transformers) using `literature-search-arxiv`.
    *   **Proposer Beta:** Hybrid/frontier mathematical designs (e.g., Neural ODEs, Mamba-Transformer layers, or geometric deep learning).

---

### Phase 2: Socratic Critique (Debate)
The orchestrator routes the generated proposals to independent critique subagents:
*   **Science Critique:** 
    *   Subagents review the biological plausibility of the mechanisms.
    *   They MUST query `ensembl-database` or `uniprot-database` to verify gene structures, mutation consequences, or active enzyme sites.
    *   They formulate 3 hard socratic questions challenging the assumptions.
*   **ML Critique:**
    *   Subagents evaluate mathematical validity, computational complexity (Big-O analysis), and execution feasibility on modern hardware (e.g. GPU memory scaling, training convergence).
    *   They actively read the current workspace directory (specifically looking at existing Python models like [03c_spatial_sir_genomic.py](file:///Users/arianstoned/Developer/uni_semestre_4/EpidemicResearch/src/spatial_model/03c_spatial_sir_genomic.py)) to identify potential code implementation bottlenecks.

---

### Phase 3: The Elo Tournament Arena
The Control Tower instantiates a **Judge Subagent** to conduct a head-to-head competition between the refined proposals:
1.  **Critique Injection:** Provide the Judge with the proposals and their respective socratic critiques.
2.  **Scoring Mechanics:**
    *   Assign each proposal an initial Elo rating of `1500.0`.
    *   The Judge simulates a socratic debate round and determines the winner based on **scientific rigor, originality, and practical feasibility**.
    *   Adjust ratings: The winner receives `+30 Elo`, the loser `-30 Elo`.
3.  **Output Structure:** The Judge must output a structured evaluation summary including:
    *   `winner_title`, `loser_title`, `final_elo_rating`, `debate_critique_summary`, and `alternative_optimization_pathways`.

---

### Phase 4: High-Rigor Synthesis & Artifact Generation
The orchestrating agent compiles the entire research trajectory and creates a polished, publication-ready Markdown file in the workspace directory (saved as `co_scientist_final_report.md` or a customized name):
1.  **Format Requirements:**
    *   **If Domain is Science:** Format with the structure, tone, and rigor of a *Nature* review paper.
    *   **If Domain is ML:** Format as a high-quality *NeurIPS* or *ICML* workshop paper.
2.  **Cross-Domain Fusion Bonus:** If the query bridges both biology and machine learning (e.g., predicting genomic contagion dynamics), automatically synthesize a hybrid section showing how to implement the biological discovery as a programmatic model extension inside the active workspace.
3.  **Visualization:** Use elegant Mermaid diagrams to visualize molecular pathways or neural network architectures.

---

## Rate Limiting & Safety
Since this is an instruction-only skill orchestrated within the premium Antigravity workspace, the main rate-limiting constraints on external APIs are automatically managed by the underlying toolset. However, subagents MUST:
*   Ensure a minimum of `1.0s` delay between consecutive parallel tool calls to PubMed/arXiv to respect public API guidelines.
*   Limit subagent count to a maximum of `3` active parallel processes.

---

## Common Mistakes
1.  **Skipping Phase 0:** Spawning subagents immediately without asking the user for confirmation. This violates the Safety Gate.
2.  **Fictional References:** Allowing subagents to hallucinate PMIDs or arXiv links. All citations must be verifiably extracted using the database tools.
3.  **Isolated Analysis:** Forgetting to check the active workspace code. The ML mode must always cross-reference active codebase models to make the proposal actionable.
