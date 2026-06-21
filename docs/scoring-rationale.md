# Scoring Rationale

This document defines how scoring justifications and rationales must be structured and verified.

## Rationale Structure

When scoring decision criteria, every score above 0 must provide a clear rationale. The rationale should be placed in the evidence or rationale column of the criteria table and must describe:

* The specific evidence from the research ledger supporting the score.
* The justification for selecting the score level (1, 2, or 3).
* Any remaining uncertainties or documentation gaps.

## Verification

Rationales are verified through:

1. **Automated Schema Checks**: The validation script checks that any non-zero score has non-empty evidence references (Claim ID and Source ID).
2. **Reviewer Assessment**: Peer review verifies that the rationale matches the criteria description and ledger evidence.

## Current Limits

Do not include subjective reasoning or scientific prose. Rationales must remain strictly neutral and objective.
