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

| Area | Criterion | ID | Related Taxonomy Layer | Related Ledger Claim | Related Ledger Source | Readiness State | Score |
|---|---|---|---|---|---|---|---|
| Use Case Fit | Use Case Alignment | uc-fit-alignment | Tool Call | claim-attention-transformer | source-attention-2017 | `ready` | 3 |
| Evidence Readiness | Data Quality Maturity | ev-readiness-maturity | Accuracy Metric | claim-attention-transformer | source-attention-2017 | `ready` | 3 |
| Operational Cost | Compute Expense | op-cost-compute | Fine-tuning | claim-attention-transformer | source-attention-2017 | `ready` | 2 |
| Latency and Throughput | Request Latency | perf-latency | Batching | claim-kv-cache-paged-attention | source-kv-cache-2023 | `ready` | 2 |
| Latency and Throughput | System Throughput | perf-throughput | Batching | claim-kv-cache-paged-attention | source-kv-cache-2023 | `ready` | 3 |
| Latency and Throughput | Telemetry Context Overhead | perf-telemetry-overhead | Telemetry | claim-tracing-context-propagation-overhead | source-opentelemetry-2023 | `ready` | 2 |
| Reliability | Service Availability | rel-availability | State Cache | claim-kv-cache-paged-attention | source-kv-cache-2023 | `ready` | 2 |
| Security and Governance | Access Policy Enforcement | sec-access-policy | Safety Filter | claim-adversarial-prompt-injection | source-adversarial-2024 | `ready` | 2 |
| Security and Governance | Telemetry Audit Logs | sec-telemetry-audit | Audit | claim-dapper-distributed-tracing | source-dapper-2010 | `ready` | 3 |
| Implementation Complexity | Integration Effort | compl-integration-effort | Vector Search | claim-kv-cache-paged-attention | source-kv-cache-2023 | `ready` | 2 |



## Current Limits

Do not add scores, rankings, recommendations, decision rules, diagrams, or
paper-ready wording from this skeleton issue.
