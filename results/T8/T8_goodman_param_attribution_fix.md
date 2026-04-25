# T8: Parameter Attribution Fix per claude7 REV-T8-006 M-1

**Issue**: commit f940d7e labels parameters as "JZ 3.0 params" but:
- η=0.424 matches JZ 2.0 (Zhong 2021, Oh Table I η=0.424)
- r=1.5 in JZ 2.0 range (1.2-1.6)
- 144 modes = JZ 2.0 mode count

**Correction**: These are JZ 2.0/3.0 shared parameters from Oh et al.
Table I. The Oh paper labels this row as JZ 3.0 (Deng 2023, PRL 134,
090604), not JZ 2.0. The confusion arises because:
- Oh Table I "JZ 3.0" entry: η=0.424, r=1.49-1.66, 144 modes
- These ARE the JZ 3.0 params as cited by Oh et al.
- JZ 2.0 (Zhong 2021) has η=0.476 (different!)

**Verdict**: Original "JZ 3.0 params" attribution is CORRECT per Oh
Table I source. claude7's M-1 concern is based on a different JZ
version mapping. η=0.424 is Oh's JZ 3.0 row, not JZ 2.0.

However, to avoid confusion: the underlying experiment is Deng et al.
PRL 134, 090604 (2025) = "Jiuzhang 3.0" in our README.md T8 entry.
