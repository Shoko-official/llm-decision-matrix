# Matrix

This directory is reserved for future decision matrix files.

Milestone 1 defines the skeleton only. It does not add scores, rankings,
recommendations, diagrams, or paper-ready decision content.

## Matrix Skeleton

Initial planning areas:

| Area | File | Purpose | Status |
|---|---|---|---|
| Use Case Fit | [use-case-fit.md](use-case-fit.md) | Reserve space for matching system choices to use cases. | Stub created |
| Evidence Readiness | [evidence-readiness.md](evidence-readiness.md) | Reserve space for evaluating evidence maturity. | Stub created |
| Operational Cost | [operational-cost.md](operational-cost.md) | Reserve space for cost-related considerations. | Stub created |
| Latency and Throughput | [latency-throughput.md](latency-throughput.md) | Reserve space for runtime performance considerations. | Stub created |
| Reliability | [reliability.md](reliability.md) | Reserve space for availability, correctness, and failure-mode considerations. | Stub created |
| Security and Governance | [security-governance.md](security-governance.md) | Reserve space for policy, risk, and control considerations. | Stub created |
| Implementation Complexity | [implementation-complexity.md](implementation-complexity.md) | Reserve space for build, integration, and maintenance considerations. | Stub created |

This table is a planning scaffold. Future entries must stay neutral until
supported by approved research ledger and taxonomy evidence.

## Central Decision Matrix Table

The following table lists all current decision criteria, their target taxonomy layers, and evidence tracking properties. No final scores, weights, or rankings are assigned.

| Area | Criterion | ID | Related Taxonomy Layer | Related Ledger Claim | Readiness State |
|---|---|---|---|---|---|
| Use Case Fit | Use Case Alignment | `uc-fit-alignment` | `model-layer` | `claim-uc-fit-placeholder` | `evidence_needed` |
| Evidence Readiness | Data Quality Maturity | `ev-readiness-maturity` | `evaluation-layer` | `claim-ev-readiness-placeholder` | `evidence_needed` |
| Operational Cost | Compute Expense | `op-cost-compute` | `training-layer` | `claim-op-cost-placeholder` | `evidence_needed` |
| Latency and Throughput | Request Latency | `perf-latency` | `inference-layer` | `claim-perf-latency-placeholder` | `evidence_needed` |
| Latency and Throughput | System Throughput | `perf-throughput` | `inference-layer` | `claim-perf-throughput-placeholder` | `evidence_needed` |
| Reliability | Service Availability | `rel-availability` | `memory-layer` | `claim-rel-availability-placeholder` | `evidence_needed` |
| Security and Governance | Access Policy Enforcement | `sec-access-policy` | `governance-layer` | `claim-sec-policy-placeholder` | `evidence_needed` |
| Implementation Complexity | Integration Effort | `compl-integration-effort` | `agent-layer` | `claim-compl-integration-placeholder` | `evidence_needed` |

## Current Limits

Do not add scores, rankings, recommendations, decision rules, diagrams, or
paper-ready wording from this skeleton issue.
