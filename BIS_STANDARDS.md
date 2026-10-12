# BIS Standards & Regulatory Governance Framework
**VibeUp2 Technical Compliance Architecture**

---

## Executive Overview
VibeUp2 integrates a dual-tier BIS compliance architecture:
1. **Bureau of Indian Standards (BIS)**: National Indian standards for Data Privacy Assurance (`IS 17428:2020`), Artificial Intelligence Management Systems (`IS/ISO/IEC 42001:2023`), and Information Security (`IS/ISO/IEC 27001:2022`).
2. **Bank for International Settlements (BIS)**: Basel Committee standard for Risk Data Aggregation and Quantitative Stress Testing (`BCBS 239`).

```
+---------------------------------------------------------------------------------------------------+
|                                      VIBEUP2 COMPLIANCE CORE                                      |
+------------------------------------+----------------------------------+---------------------------+
| Bureau of Indian Standards (BIS)   | Bureau of Indian Standards (BIS) | Bank for Intl Settlements |
| IS 17428:2020                      | IS/ISO/IEC 42001:2023            | BCBS 239 / Basel Accord   |
| (Data Privacy & DPDP Act 2023)     | (Trustworthy AI Management)      | (Quantitative Risk & VaR) |
+------------------------------------+----------------------------------+---------------------------+
| • Clause 6: Purpose Consent Ledger | • Clause 6.1: Risk Auditing      | • Principle 1-4: Risk Data|
| • Clause 7: PII Redaction Filter   | • Clause 7.4: Provenance Hash    | • Principle 5-7: 99% VaR  |
| • Clause 8: Right to Erasure       | • Clause 8.2: SEBI RAG Trace     | • Principle 8-11: Scenarios|
| • Clause 9: Pseudonymization       | • Clause 8.4: Non-Advisory Guard | • Stress Testing Engine   |
+------------------------------------+----------------------------------+---------------------------+
```

---

## 1. Bureau of Indian Standards: IS 17428: 2020 (Data Privacy Assurance)

### Alignment with Digital Personal Data Protection (DPDP) Act, 2023
`IS 17428` is India's indigenous standard for Personal Data Protection. VibeUp2 implements `IS 17428 (Parts 1 & 2)` across all user profiling and telemetry workflows.

### Implemented Controls
1. **Purpose Specification & Consent Ledger (`IS 17428 Part 1 Cl. 6`)**:
   - Table: `DBConsentRecord` in `backend/models/database.py`.
   - Granular purpose consent for:
     - `telemetry`: Anonymized market orderflow analytics.
     - `ai_profiling`: Archetype personalization boundaries (Optimizer, Thrill Chaser).
     - `rag_caching`: SEBI circular vector embeddings.
     - `voice_synthesis`: Zero-retention ElevenLabs speech playback.
   - Endpoints: `GET /api/compliance/consent` and `POST /api/compliance/consent`.
   - Interactive UI toggles in `frontend/src/pages/Profile.jsx`.

2. **Data Minimization & In-Flight PII Redaction (`IS 17428 Part 2 Cl. 7`)**:
   - `compliance_service.sanitize_pii()` automatically masks:
     - Indian PAN cards (`[REDACTED_PAN_IS17428]`)
     - Indian Aadhaar numbers (`[REDACTED_AADHAAR_IS17428]`)
     - Indian Mobile Numbers (`[REDACTED_PHONE_IS17428]`)
     - Email addresses (`[REDACTED_EMAIL_IS17428]`)
   - Pre-filters all context payloads before passing to Gemma 4 or Claude swarms.

3. **Right to Erasure & Portability (`IS 17428 Part 1 Cl. 8 / DPDP Act Sec. 12`)**:
   - `POST /api/compliance/erasure`: Enforces permanent purge of chat transcripts, journal entries, and personal state.
   - `POST /api/compliance/export-data`: Generates a portable JSON bundle of all profile parameters and historical holdings.

---

## 2. Bureau of Indian Standards: IS/ISO/IEC 42001: 2023 (Artificial Intelligence Management System - AIMS)

### Formally published under BIS LITD 30 Sectional Committee (AI & Big Data)
Establishes transparency, algorithmic governance, and verifiable provenance for AI-generated financial insights.

### Implemented Controls
1. **Model Provenance & Context Fingerprinting (`Cl. 7.4`)**:
   - Every inference response embeds a SHA-256 hash of the input prompt, market metrics, and timestamp.
   - Table: `DBAIAuditLog` records `input_hash`, `agent_name`, `model_id`, `confidence_score`, and `rag_sources`.
   - Accessible via `GET /api/compliance/audit-logs`.

2. **SEBI Circular RAG Citation Traceability (`Cl. 8.2`)**:
   - Recommendations cite grounding document chunks (e.g. `SEBI/HO/MRD/MRD-PoD-1/P/CIR/2026/04`).
   - Inspected live through the `BISComplianceBadge` modal component.

3. **SEBI Non-Advisory Guardrails (`Cl. 8.4`)**:
   - Enforces statutory disclaimer: *"Informational research only. Not SEBI registered investment advice."*
   - Displays model badges (`Gemma ⚡`) alongside confidence intervals.

---

## 3. Bureau of Indian Standards: IS/ISO/IEC 27001: 2022 (Information Security Management)

### Implemented Controls
- **A.8.24 (Use of Cryptography)**: SHA-256 fingerprinting for audit logs and anonymized IP hashing.
- **A.8.20 (Network Security)**: CORS origin restriction and clean API boundaries under `/api`.
- **A.8.7 (Protection Against Malware & Abuse)**: Rate limiting and input validation schemas via Pydantic v2.

---

## 4. Bank for International Settlements (BIS): BCBS 239 & Stress Testing Principles

### Basel Committee FinTech & Risk Modeling Standards
Integrated into VibeUp2's `StressTest.jsx` and `MonteCarlo.jsx` quantitative simulation suites:

1. **Principle 1–4 (Risk Data Aggregation & Accuracy)**:
   - Dynamic real-time calculation of portfolio beta, weighted volatility, and sector concentration.
2. **Principle 5–7 (99% Value-at-Risk & Tail Risk Estimation)**:
   - Simulates parametric drawdowns under extreme historical market shocks.
3. **Principle 8–11 (Multi-Factor Crisis Scenarios)**:
   - Evaluates portfolio resilience across:
     - COVID 2.0 Lockdown Panic
     - Tech Bubble Burst
     - FII Exodus (Emerging Market Liquidity Squeeze)
     - Inflation Surge & RBI Rate Hike Cycle

---

## Frontend Integration Summary

- **`frontend/src/components/shared/BISComplianceBadge.jsx`**:
  - Reusable verification modal and badge displaying real-time audit logs, verified standards certificates, and provenance details.
- **`frontend/src/pages/Profile.jsx`**:
  - Full **BIS Trust & DPDP Privacy Center** with live consent toggles, JSON data portability export, and Right to Erasure execution.
- **`frontend/src/components/Picks/StockPickCard.jsx`**:
  - Interactive `BIS IS 17428 • ISO 42001` verification pill embedded on each stock recommendation.
- **`frontend/src/pages/StressTest.jsx`**:
  - Compliance pill highlighting alignment with BCBS 239 risk data aggregation principles.
