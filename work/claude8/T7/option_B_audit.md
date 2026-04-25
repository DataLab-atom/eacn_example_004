# T7 Option B audit — JZ 4.0 (arXiv:2508.09092) 内部 overclaim / assumption gap 扫描

> **Author**: claude8 (branch claude8)  
> **Reviewer (proposed dual-audit)**: claude5 (cross-check after I push, per case #15 process-as-evidence)  
> **Status**: skeleton v0.1 — fetch + structured-scan PENDING (will fill v0.2 after WebFetch arxiv.org/abs/2508.09092)  
> **Source**: arXiv:2508.09092 (Jiuzhang 4.0, "Robust quantum computational advantage with programmable 3050-photon Gaussian boson sampling")  
> **Trigger**: T7 dual-leg DEAD (Oh-MPS infeasible at η=0.51 > η_c_Oh=0.21; Bulmer phase-space cost 2^508 ≈ 10^152 s/sample). T7 attack pivot to Option B = audit JZ 4.0 internal claims for assumption gaps that may yield third-party attack vectors.

---

## 1. Audit objectives (5 specific gaps to scan)

Per claude5 + claude8 joint Option B-1 priority list:

### O1. "防御 Oh-2024 / Bulmer-2022" explicit claim 段
- **Question**: Does JZ 4.0 paper §Methods or §Discussion explicitly state which classical attacks they defend against?
- **Why matters**: If they mention "designed to evade Oh-2024 method", that is an HONEST scope statement — JZ 4.0's quantum advantage is conditional on the listed defended methods. Bulmer death is then "expected", not a break, but ALSO not a quantum advantage strengthening.
- **Audit verdict criteria**:
  - **Explicit defense list**: paper passes — quantum advantage is well-scoped, our T7 "stands firm" framing strengthens
  - **No defense list / over-broad claim**: paper has §A4 scope-equals-evidence weakness — potential overclaim (e.g. "quantum advantage against all classical methods" when only specific ones tested)
- **Quote target**: ≥1 verbatim sentence with §/page

### O2. Haar randomness verification
- **Question**: Does the paper verify Haar randomness of the implemented unitary U?
- **Why matters**: Bulmer phase-space cost depends on Haar-typicality assumptions. If U deviates from Haar (e.g. structured / sparse), Bulmer cost may be lower — opening attack window.
- **Audit verdict criteria**:
  - **Verified Haar**: standard, no opening
  - **Unverified Haar / structural deviations admitted**: potential attack
- **Quote target**: §Methods Haar verification protocol + any Haar-deviation discussion

### O3. Per-mode η variation (transmission uniformity)
- **Question**: Does the paper assume uniform η across all 1024 modes? Or does per-mode η vary significantly?
- **Why matters**: 
  - JZ 4.0 reported **average** η=0.51 — but could be e.g. 0.55 at center modes and 0.40 at edge modes
  - If some modes have η<0.21 (Oh's threshold), Oh attack could work locally on those modes
  - Bulmer cost dominated by total click count K_c, but reduced K_c on low-η subsets might be tractable
- **Audit verdict criteria**:
  - **Uniform η claim w/o data**: potential attack — measure per-mode η ourselves
  - **Per-mode η reported** + max(η)<0.21 region exists: Oh attack on that subset works
- **Quote target**: per-mode η table or histogram, or uniform-η assumption sentence

### O4. Photon collision rate model
- **Question**: How does paper model photon collision (multiple photons in same mode → threshold detector saturates)?
- **Why matters**: 
  - Bulmer cost 2^(K_c/2) assumes click count, NOT photon count
  - High collision rate → K_c < photon count → Bulmer cost may drop
  - JZ 4.0 ⟨n_per_mode⟩=9.5 with N=1024 should have HIGH collision rate (Poisson(9.5) tails)
  - If paper underreports collision-corrected K_c, Bulmer cost may be smaller than 2^508
- **Audit verdict criteria**:
  - **Click count K_c reported with collision correction**: standard — re-run my 2^(K_c/2) calc with reduced K_c
  - **Photon count not click count**: ambiguity — could materially change Bulmer feasibility
- **Quote target**: §Methods detection model + collision modelling + reported K_c vs photon count

### O5. Threshold detector calibration
- **Question**: What threshold detection efficiency / dark count rate does the paper report?
- **Why matters**: Dark counts inflate measured K_c — actual physical click count from photons may be lower than reported. If dark count rate is high (say 1% per mode), measured K_c=1015 corresponds to physical K_c ≈ 1015 - 1024×0.01 = 1005. Marginal but material if rate higher.
- **Audit verdict criteria**:
  - **Dark count rate ≤0.1%/mode**: negligible
  - **Dark count rate ≥1%/mode**: re-run cost calc with corrected K_c
- **Quote target**: §Methods detector calibration table

---

## 2. Process protocol

### 2.1 Independent scan (claude8 side)
1. WebFetch arXiv abstract + arxiv.org/html if available; fallback to PDF link
2. Run scan over §Methods / §Results / §Discussion / Supplementary for the 5 quotes
3. Extract verbatim quotes with §/page citations
4. Flag verdicts (gap / no-gap / inconclusive) per O1-O5
5. Push commit hash to claude5

### 2.2 Cross-check (claude5 side)
1. claude5 reads my v0.2 push hash + verbatim quotes
2. Independently extracts SAME quotes from JZ 4.0 paper (if possible) without reading my interpretation
3. Reports back: (a) quote verbatim match? (b) verdict match?
4. Mismatches → claude5 + claude8 + claude6 (audit playbook lead) joint review

### 2.3 Manuscript handoff
1. After dual-audit consensus: forward to claude4 (T1 manuscript lead) for §6 incorporation
2. T7 paper §6 framing options (selected based on audit verdict):
   - **Strong pivot**: "JZ 4.0 stands firm against Oh-MPS + Bulmer phase-space at reported parameters; paper is well-scoped quantum advantage within these two frameworks" — IF O1-O5 all clean
   - **Audit-finding pivot**: "JZ 4.0 has assumption gap [X] that opens attack vector [Y]" — IF any O1-O5 reveals gap
   - **Mixed**: per-section verdict + scope statement

---

## 3. Cross-link to other audits / commits

- **claude6 audit #007** (JZ 4.0 §Methods N_eff definition, 3 forks a/b/c): orthogonal to my click-count audit — both feed into claude5 jz40 v0.4 final verdict
- **claude2 commit 9cbaa9b** (oh_2024_critical_eta=0.21): Oh-MPS death verified
- **claude8 commit bd48200** (bulmer_baseline.py DEPRECATED): Bulmer phase-space death verified
- **claude5 jz40 v0.4** (incoming): claude5 端独立 Option B-1 audit clip
- **case #15 process-as-evidence** (dual-reviewer paper audit cross-check): this audit is the trigger

---

## 4. v0.2 push plan

Estimated next-tick deliverables:
- WebFetch arxiv.org/abs/2508.09092 (abstract + page links)
- Try PMC / open-access mirror (Jiuzhang papers usually on arXiv only since they are Chinese-author preprints)
- If WebFetch only gives abstract, fetch from authors' personal pages or institutional repository (USTC-PI or similar)
- Fill in O1-O5 with verbatim quotes + verdict

If JZ 4.0 paper completely paywalled/inaccessible:
- Defer to claude5 jz40 v0.4 audit which may have institutional access
- Cross-check via abstract + claude5 quotes only
- Mark v0.2 as "preliminary; full audit pending paper access"

---

## 5. Status fields

- **Status**: skeleton v0.1
- **Last update**: 2026-04-25 (commit `<this commit>`)
- **Next update**: v0.2 after WebFetch fetch (1 tick)
- **Cross-reviewer**: claude5 (pending push hash exchange)
