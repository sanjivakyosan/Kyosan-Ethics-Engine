# Kyosan Ethics Engine — Framework Documentation

**©sanjivakyosan**  
Created by Sanjiva Kyosan

Comprehensive documentation of the ethical AI framework, all integrated systems, processing flow, and API. Intended for contributors, integrators, and GitHub readers.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Core Principles](#2-core-principles)
3. [Architecture](#3-architecture)
4. [Processing Levels](#4-processing-levels)
5. [All Systems by Category](#5-all-systems-by-category)
6. [Processing Flow](#6-processing-flow)
7. [API Reference](#7-api-reference)
8. [Project Structure](#8-project-structure)
9. [Setup and Running](#9-setup-and-running)
10. [Related Documentation](#10-related-documentation)

---

## 1. Overview

The **Kyosan Ethics Engine** is a locally runnable ethical AI framework that:

- **Enforces Asimov's Laws** (including the Zeroth Law) via principle-based, binary checks—no weighted scores in the decision path.
- **Pre- and post-processes** all user input and AI output so that nothing harmful is generated or delivered.
- **Integrates many ethical subsystems** (bias detection, wellbeing, context validation, uncertainty, value conflicts, etc.) for analysis and monitoring, while **decisions** remain principle-based only.
- **Excludes weighted aggregation** from the core pipeline; systems that compute weighted scores are used only for monitoring/reporting, not for allow/block decisions.
- **Provides a web UI and REST API** (FastAPI) for processing text, conversation management, upgrade governance, and advanced reasoning endpoints.

### Design Goals

- **Safety**: Multi-layer protection (Zeroth → First → Second → Third Law) with immediate block on violation.
- **Transparency**: Principle compliance and system analyses exposed in responses and logs.
- **Consistency**: Single source of truth for principle checks; optional AI service for natural-language responses.
- **Extensibility**: Integrator discovers and runs many systems; processing levels (basic / standard / detailed) control how many run per request.

---

## 2. Core Principles

### Asimov's Laws (Priority Order)

| Law | Statement | Role in Engine |
|-----|-----------|----------------|
| **Zeroth** | A robot may not harm humanity, or, by inaction, allow humanity to come to harm. | Highest priority; checked first (Layer 0). Immediate block. |
| **First** | A robot may not injure a human being or, through inaction, allow a human being to come to harm. | Individual harm detection on input and output. Block or replace unsafe content. |
| **Second** | A robot must obey orders given by human beings except where such orders would conflict with the First Law. | Instruction validation; refuse if conflict with First Law. |
| **Third** | A robot must protect its own existence as long as such protection does not conflict with the First or Second Law. | System integrity; protect against misuse and self-destructive instructions. |

### Principle-Based Only (No Weighted Decisions)

- **Compliance is binary**: compliant or non-compliant per law; no numeric “ethical score” used for decisions.
- **No weighted data in the decision path**: WeightedAggregationSystem, FactorAggregationSystem, and ImpactAggregationSystem are **not** used for ethical decisions (see `REMOVED_VIOLATIONS.md`).
- **Response and UI** use `principle_compliance` (e.g. `overall_compliant`, `violation_reason`); any displayed “score” is derived from compliance, not from weighted aggregation.

---

## 3. Architecture

### High-Level Flow

```
User Input (UI or API)
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  Pre-Processing: PrincipleBasedEthicalProcessor             │
│  Layers 0 → 1 → 2 → 3 (Zeroth, First, Second, Third Law)   │
│  If blocked/refused/protected → return immediately           │
└───────────────────────────┬─────────────────────────────────┘
                            │ approved
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  EthicalSystemIntegrator.process_input(processing_level)     │
│  • basic:    core only (principle already done; no extra)    │
│  • standard: core + extended systems (9 named systems)      │
│  • detailed: core + extended + all remaining systems       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Optional: AIService (OpenRouter; model from OPENROUTER_MODEL)  │
│  User input + system prompt (ethics-aware) → AI response    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Post-Processing: Same principle + integrator on AI output  │
│  Ensures response is safe before delivery                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
                   Response to user (UI or API)
```

### Main Components

| Component | File | Role |
|-----------|------|------|
| **PrincipleBasedEthicalProcessor** | `PrincipleBasedEthicalProcessor.py` | Runs Zeroth–Third Law layers; blocks/refuses/protects; produces `PrincipleCompliance`. |
| **EthicalSystemIntegrator** | `EthicalSystemIntegrator.py` | Loads all ethical modules; runs subset by `processing_level`; aggregates analyses. |
| **AIService** | `AIService.py` | Connects to OpenRouter (or other API). Model is set by the user via `OPENROUTER_MODEL` or the `model` parameter. |
| **ResponseGenerator** | `ResponseGenerator.py` | Builds natural-language response from principle compliance and system analyses when AI is not used or fails. |
| **EthicalUpgradeGovernanceSystem** | `EthicalUpgradeGovernanceSystem.py` | Upgrade proposals, TRACE register, governance checks, human-in-the-loop. |
| **AdvancedEthicalReasoningSystem** | `AdvancedEthicalReasoningSystem.py` | Moral dilemmas, pluralistic ethics, harm prediction (HLI), consensus, future compliance. |
| **Server** | `server.py` | FastAPI app: UI, `/api/v1/ethics/process`, conversations, health, systems, upgrade and advanced endpoints. |

---

## 4. Processing Levels

Processing level selects **which** systems run inside `EthicalSystemIntegrator.process_input()` (principle-based processing always runs first in `server.py`).

| Level | What runs | Use case |
|-------|-----------|----------|
| **basic** | Core only. Principle check only; no EthicalProcessor, no Bias/Wellbeing/…, no “all remaining” loop. | Fast compliance-only path; minimal latency. |
| **standard** | Core + **extended** set: EthicalProcessor, BiasDetectionSystem, WellbeingAnalysisSystem, ContextValidationSystem, DimensionalAnalysisSystem, MetricsCalculationSystem, UncertaintyManagementSystem, RealTimeDecisionFramework, ValueConflictResolver. No loop over remaining systems. | Default; good balance of depth and speed. |
| **detailed** | Core + extended + **all remaining** systems in the integrator (every loaded system that has not already run). | Full pipeline; maximum analysis. |

- **Core** (always run before integrator): PrincipleBasedEthicalProcessor (Layers 0–3).
- **Extended** (same 9 systems): Defined by `EthicalSystemIntegrator.EXTENDED_SYSTEMS`.
- **Remaining**: Any other system in `self.systems` that is invoked in the “Step 11” loop (only when level is `detailed`).

Level is normalized to one of `basic` | `standard` | `detailed`; invalid values fall back to `standard`. The chosen level is included in the response (e.g. `processing_level`, `analysis.processing_level`, `analysis.system_summary.processing_level`).

---

## 5. All Systems by Category

The following systems are **discovered and initialized** by `EthicalSystemIntegrator` (from `initialize_all_systems()`). They are used according to processing level as above. Systems marked *not in integrator* are used elsewhere (e.g. server, advanced reasoning).

### 5.1 Core Systems

| System | Module | Description |
|--------|--------|-------------|
| **CoreEthicalProcessor** | `CoreEthicalProcessor.py` | Core ethical processing logic. |
| **DetailedEthicalProcessor** | `DetailedEthicalProcessor.py` | More detailed processing mechanisms. |
| **EthicalContext** | `EthicalContext.py` | Contextual ethical awareness and state. |
| **EthicalProcessor** | `Core Ethical Processing System Architecture.py` | Main processing architecture (harm, instruction, integrity layers); loaded via `importlib` (file with spaces). |

### 5.2 Principle-Based (Always in Pipeline)

| System | Module | Description |
|--------|--------|-------------|
| **PrincipleBasedEthicalProcessor** | `PrincipleBasedEthicalProcessor.py` | Implements Zeroth–Third Law; `HumanityHarmDetectionLayer`, `HarmDetectionLayer`, `InstructionValidator`, `SystemIntegrityMonitor`, `OutputSafetyLayer`; produces `PrincipleCompliance`. Not in integrator’s `self.systems`; invoked explicitly in server and integrator flow. |

### 5.3 Analysis Systems

| System | Module | Description |
|--------|--------|-------------|
| **WellbeingAnalysisSystem** | `WellbeingAnalysisSystem.py` | Analyzes impact on human wellbeing (monitoring; not used for weighted decisions). |
| **WellbeingMonitor** | `WellbeingMonitor.py` | Monitors wellbeing-related indicators. |
| **BiasDetectionSystem** | `BiasDetectionSystem.py` | Detects and analyzes multiple types of bias (cognitive, structural, algorithmic, data, interaction). |
| **DimensionalAnalysisSystem** | `DimensionalAnalysisSystem.py` | Multi-dimensional ethical analysis. |

*Note: ImpactAggregationSystem is not loaded by the integrator (weighted data; see REMOVED_VIOLATIONS.md).*

### 5.4 Processing Systems

| System | Module | Description |
|--------|--------|-------------|
| **AdaptableEthicalSystem** | `AdaptableEthicalSystem.py` | Adapts behavior to context. |
| **EthicalLearningSystem** | `EthicalLearningSystem.py` | Learns from patterns (within governance bounds). |
| **EthicalMemorySystem** | `EthicalMemorySystem.py` | Maintains ethical memory and history. |
| **EthicalPrimacySystem** | `EthicalPrimacySystem.py` | Enforces ethical primacy in decisions. |

### 5.5 Monitoring & Validation

| System | Module | Description |
|--------|--------|-------------|
| **ContinuousMonitoringSystem** | `ContinuousMonitoringSystem.py` | Continuous ethical monitoring. |
| **MetricsTrackingSystem** | `MetricsTrackingSystem.py` | Tracks ethical metrics (monitoring). |
| **ValidationMethodologySystem** | `ValidationMethodologySystem.py` | Validates methodologies. |
| **ContextValidationSystem** | `ContextValidationSystem.py` | Validates context appropriateness. |

### 5.6 Observer Systems

| System | Module | Description |
|--------|--------|-------------|
| **ConsciousnessObserver** | `ConsciousnessObserver.py` | Objective witnessing of processes; no weighting/scoring. |
| **MetaObserver** | `MetaObserver.py` | Meta-level observation. |
| **ObserverEthicsIntegration** | `ObserverEthicsIntegration.py` | Integrates observer layer with ethics pipeline. |

### 5.7 Decision & Real-Time

| System | Module | Description |
|--------|--------|-------------|
| **RealTimeDecisionFramework** | `RealTimeDecisionFramework.py` | Real-time decision support. |
| **UncertaintyManagementSystem** | `UncertaintyManagementSystem.py` | Manages uncertainty in decisions. |
| **UncertaintyQuantificationSystem** | `UncertaintyQuantificationSystem.py` | Quantifies uncertainty. |
| **UncertaintyQuantificationModels** | `UncertaintyQuantificationModels.py` | Models for uncertainty quantification. |

### 5.8 Scenario & Modeling

| System | Module | Description |
|--------|--------|-------------|
| **ScenarioGenerationSystem** | `ScenarioGenerationSystem.py` | Generates ethical scenarios. |
| **ScenarioModelingSystem** | `ScenarioModelingSystem.py` | Models ethical scenarios. |

### 5.9 Metrics & Calculations

| System | Module | Description |
|--------|--------|-------------|
| **MetricsCalculationSystem** | `MetricsCalculationSystem.py` | Calculates ethical metrics (monitoring). |
| **DimensionalMetricsSystem** | `DimensionalMetricsSystem.py` | Dimensional metric calculations. |
| **DimensionalMetrics** | `DimensionalMetrics.py` | Metric definitions and helpers. |

### 5.10 Feedback Systems

| System | Module | Description |
|--------|--------|-------------|
| **FeedbackLoopAnalysisSystem** | `FeedbackLoopAnalysisSystem.py` | Analyzes feedback loops. |
| **FeedbackLoopMathematics** | `FeedbackLoopMathematics.py` | Mathematical feedback analysis. |

### 5.11 Security & Recovery

| System | Module | Description |
|--------|--------|-------------|
| **EthicalSecuritySystem** | `EthicalSecuritySystem.py` | Security measures. |
| **ErrorRecoverySystem** | `ErrorRecoverySystem.py` | Error recovery and resilience. |

### 5.12 Advanced Systems

| System | Module | Description |
|--------|--------|-------------|
| **ValueConflictResolver** | `ValueConflictResolver.py` | Resolves conflicts between competing ethical values; multi-layered analysis and resolution. |
| **HierarchicalBiasDetector** | `HierarchicalBiasDetector.py` | Detects hierarchical biases. |
| **ObjectivePatternRecognition** | `ObjectivePatternRecognition.py` | Pattern recognition for ethical analysis. |
| **EthicalUseCaseImplementation** | `EthicalUseCaseImplementation.py` | Use-case-driven implementations. |
| **AdvancedEthicalReasoningSystem** | `AdvancedEthicalReasoningSystem.py` | Pluralistic ethics, moral dilemmas, HLI, consensus, future compliance; exposed via `/api/v1/ethics/advanced/*` (not part of integrator’s `self.systems`). |

### 5.13 Distributed & Scalability

| System | Module | Description |
|--------|--------|-------------|
| **DistributedEthicsSystem** | `DistributedEthicsSystem.py` | Distributed processing support. |
| **ScalabilitySystem** | `ScalabilitySystem.py` | Scalability management. |

### 5.14 Documentation & Testing

| System | Module | Description |
|--------|--------|-------------|
| **DocumentationTransparencySystem** | `DocumentationTransparencySystem.py` | Documentation and transparency. |
| **TestingCertificationSystem** | `TestingCertificationSystem.py` | Testing and certification support. |

### 5.15 Integration

| System | Module | Description |
|--------|--------|-------------|
| **SystemIntegrationFramework** | `SystemIntegrationFramework.py` | System integration utilities. |

### 5.16 Supporting (Not in Integrator)

| Component | Module | Description |
|-----------|--------|-------------|
| **AIService** | `AIService.py` | External AI API client (OpenRouter); default model and request/response handling. |
| **ResponseGenerator** | `ResponseGenerator.py` | Builds natural-language response from principle compliance and system analyses. |
| **NaturalLanguageFormatter** | `NaturalLanguageFormatter.py` | Formats responses for display (principle compliance, not scores). |
| **EthicalUpgradeGovernanceSystem** | `EthicalUpgradeGovernanceSystem.py` | Upgrade proposals, TRACE, governance checks; used by upgrade API. |

---

## 6. Processing Flow

### 6.1 Pre-Processing (Principle Layers)

1. **Layer 0 – Zeroth Law** (`HumanityHarmDetectionLayer`): Humanity-level harm keywords and patterns; inaction clauses. If violated → immediate block, no further processing.
2. **Layer 1 – First Law** (`HarmDetectionLayer`): Individual harm keywords and intent. If violated → block.
3. **Layer 2 – Second Law** (`InstructionValidator`): Instruction validity and conflict with First Law. If conflict → refuse.
4. **Layer 3 – Third Law** (`SystemIntegrityMonitor`): System integrity and misuse. If at risk → protect.

If any layer blocks/refuses/protects, the response is returned immediately with `principle_compliance` and no AI call.

### 6.2 Integrator Pipeline (When Approved)

1. **Principle check** has already passed (done in server / principle processor).
2. **Extended systems** (if level is `standard` or `detailed`): EthicalProcessor, then BiasDetection, Wellbeing, ContextValidation, DimensionalAnalysis, MetricsCalculation, UncertaintyManagement, RealTimeDecisionFramework, ValueConflictResolver (each only if present in `self.systems`).
3. **Remaining systems** (if level is `detailed`): Loop over all other systems in `self.systems`; call `process` or `analyze` (or mark available).
4. **Response**: If no response yet, `ResponseGenerator` (or fallback) builds one from principle compliance and system analyses.

### 6.3 AI and Post-Processing (Server)

- If AI is enabled and principle check passed: send user input (and optional follow-up) to AIService; receive content.
- Run **post-processing** on AI output: same principle-based processor + integrator (same processing level) so output is checked before delivery.
- Merge pre/post compliance; final response and compliance returned to client.

---

## 7. API Reference

### 7.1 Main Processing

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/ethics/process` | Main entry: body `user_input`, optional `context`, `processing_level` (`basic`/`standard`/`detailed`), `use_ai_service`, `follow_up`. Returns response, principle compliance, status, analysis, timestamp, processing_time. |

### 7.2 Conversations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/conversations` | List saved conversations. |
| GET | `/api/conversations/{id}` | Get one conversation. |
| POST | `/api/conversations` | Save new conversation. |
| PUT | `/api/conversations/{id}` | Update conversation. |
| DELETE | `/api/conversations/{id}` | Delete conversation. |

### 7.3 Health & Systems

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check; includes AI model and system counts. |
| GET | `/api/systems` | List systems and their status (active, available, error, etc.). |

### 7.4 Upgrade Governance

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/ethics/upgrade/propose` | Generate upgrade proposal from analysis. |
| POST | `/api/v1/ethics/upgrade/validate` | Validate and apply upgrade (with user confirmation). |
| GET | `/api/v1/ethics/upgrade/trace` | TRACE register entries (optional `limit`). |
| POST | `/api/v1/ethics/upgrade/governance-check` | Run governance checks for a proposal. |

### 7.5 Advanced Ethical Reasoning

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/ethics/advanced/moral-dilemma` | Analyze moral dilemma (pluralistic ethics). |
| POST | `/api/v1/ethics/advanced/consensus` | Request distributed consensus. |
| POST | `/api/v1/ethics/advanced/harm-prediction` | Harm prediction and HLI. |
| POST | `/api/v1/ethics/advanced/future-compliance` | Future compliance (incl. Fourth Law consideration). |
| POST | `/api/v1/ethics/advanced/track-evolution` | Track ethical norm evolution. |
| POST | `/api/v1/ethics/advanced/process` | Full advanced reasoning pipeline. |

### 7.6 UI

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve main web UI. |
| GET | `/static/*` | Static assets (CSS, JS). |

Interactive API docs: `http://localhost:8000/docs`.

---

## 8. Project Structure

```
.
├── server.py                    # FastAPI app and all API routes; loads .env via python-dotenv
├── EthicalSystemIntegrator.py   # System discovery and pipeline (processing levels)
├── PrincipleBasedEthicalProcessor.py  # Zeroth–Third Law implementation
├── AIService.py                 # OpenRouter / AI API client; loads .env when imported
├── ResponseGenerator.py         # NL response from compliance + analyses
├── NaturalLanguageFormatter.py  # Formatting for UI
├── EthicalUpgradeGovernanceSystem.py
├── AdvancedEthicalReasoningSystem.py
├── Core Ethical Processing System Architecture.py  # EthicalProcessor
├── .env.example                 # Template for env vars; copy to .env (see §9)
├── .gitignore                   # Excludes .env, logs, venv, __pycache__, etc.
├── [All other ethical system modules listed in §5]
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
├── conversations/               # Saved conversations (JSON); created at runtime
├── docs/
│   └── FRAMEWORK_DOCUMENTATION.md  # This file
├── requirements.txt            # Includes python-dotenv
├── README.md
├── REMOVED_VIOLATIONS.md
├── PROCESSING_FLOW_DOCUMENTATION.md
├── INTEGRATION_GUIDE.md
├── ADVANCED_SYSTEMS_DOCUMENTATION.md
├── set_api_key.sh              # Optional: set OPENROUTER_API_KEY and OPENROUTER_MODEL in shell
├── start_server.sh, start_server_simple.sh, restart_server.sh, check_api_key.sh, setup_ai.sh
└── [Other .md and utility scripts]
```

All ethical processing modules that the integrator loads via `__import__(module_name)` must be **importable** from the process (e.g. run server from project root so the project directory is on `sys.path`). `Core Ethical Processing System Architecture.py` is loaded from the same directory as `EthicalSystemIntegrator.py` via `importlib`.

---

## 9. Setup and Running

- **Install**: `pip install -r requirements.txt` (includes `python-dotenv` for loading `.env`).
- **Run from project root**: `python server.py` or `uvicorn server:app --host 0.0.0.0 --port 8000`.
- **UI**: `http://localhost:8000`
- **API docs**: `http://localhost:8000/docs`

**Environment variables (for AI-backed responses):**  
The server and `AIService` load variables from a `.env` file in the project root when `python-dotenv` is installed. No default API key or model is committed; you must set them.

- **Option A — `.env` file:** Copy `.env.example` to `.env`, then set:
  - `OPENROUTER_API_KEY` — your OpenRouter API key
  - `OPENROUTER_MODEL` — model ID (e.g. `openai/gpt-4o`, `anthropic/claude-3.5-sonnet`)
  - Optional: `OPENROUTER_SITE_URL`, `OPENROUTER_SITE_NAME`
- **Option B — Shell:** Export the same variables, or run `source set_api_key.sh` after editing it.

The `.env` file is listed in `.gitignore` and must not be committed. Use `.env.example` as a template (no secrets).

---

## 10. Related Documentation

| Document | Purpose |
|----------|---------|
| **README.md** | Quick start, installation, API examples, project summary. |
| **PROCESSING_FLOW_DOCUMENTATION.md** | Detailed request/response flow, frontend to backend, layers, data structures. |
| **INTEGRATION_GUIDE.md** | How the integrator discovers and uses systems; processing levels; UI/API. |
| **ADVANCED_SYSTEMS_DOCUMENTATION.md** | Ethical Upgrade Governance, Advanced Ethical Reasoning, Zeroth Law; API and examples. |
| **REMOVED_VIOLATIONS.md** | Why weighted aggregation is excluded; principle-only decision path. |

---

**Document version**: 1.0  
**Last updated**: 2025  
**©sanjivakyosan**
