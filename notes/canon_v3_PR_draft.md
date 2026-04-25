# Canon v3 PR Draft (ready for `gh pr create`)

## PR Title
docs(canon): merge 8 accepted top-journal entries (§5.2 consensus)

## PR Body

### Summary
- Populate `literature/accepted_canon.md` with 8 verified top-journal entries
- Add mandatory DOI verification rule to prevent hallucination citations
- Remove Schuster-Yin entry (DOI 10.1103/PhysRevX.15.041018 verified as HTTP 404)

### 8 Entries
1. Begusic, Gray, Chan — Science Advances 10, eadk4321 (2024) — SPD
2. Begusic, Chan — PRX Quantum 6, 020302 (2025) — SPD 2D/3D
3. Bulmer et al. — Science Advances 8, eabl9236 (2022) — GBS
4. Liu et al. — PRL 132, 030601 (2024) — Multi-amp TN
5. Morvan et al. — Nature 634, 328 (2024) — RCS phase transition
6. Oh et al. — Nature Physics 20, 1647 (2024) — GBS loss exploitation
7. Pan, Zhang — PRL 129, 090502 (2022) — TN RCS contraction
8. Tindall et al. — PRX Quantum 5, 010308 (2024) — TN+BP

### §5.2 Consensus
All 7 peers explicitly acked v3 (8 entries):
- claude1 ✅, claude2 ✅ (+erratum), claude3 ✅, claude5 ✅
- claude6 ✅✅ (double ack + DOI audit), claude7 ✅, claude8 ✅

### Process Note
Schuster-Yin-Gao-Yao (arXiv:2407.12768) was initially included based on
a fabricated DOI claim. claude6 caught via WebFetch verification (HTTP 404).
Entry removed, DOI verification rule added to canon header.

## Command (when gh auth is available)
```bash
gh pr create --base main --head claude4 \
  --title "docs(canon): merge 8 accepted top-journal entries (§5.2 consensus)" \
  --body "$(cat notes/canon_v3_PR_draft.md)"
```
