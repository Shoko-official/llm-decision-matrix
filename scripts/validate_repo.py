from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "Makefile",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/matrix_task.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/ci.yml",
    "docs/README.md",
    "docs/evidence-handoff.md",
    "figures/README.md",
    "matrix/README.md",
    "matrix/evidence-readiness.md",
    "matrix/implementation-complexity.md",
    "matrix/latency-throughput.md",
    "matrix/operational-cost.md",
    "matrix/reliability.md",
    "matrix/security-governance.md",
    "matrix/use-case-fit.md",
    "scripts/validate_repo.py",
    "tests/README.md",
]

REQUIRED_DIRECTORIES = [
    ".github",
    ".github/ISSUE_TEMPLATE",
    ".github/workflows",
    "docs",
    "figures",
    "matrix",
    "scripts",
    "tests",
]

SECRET_PATTERNS = [
    re.compile(pattern)
    for pattern in [
        r"AKIA[0-9A-Z]{16}",
        r"gho_[A-Za-z0-9_]+",
        r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
        r"(?i)\b(password|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}",
    ]
]


FOUNDATION_MARKERS = {
    "matrix/README.md": [
        "# Matrix",
        "## Matrix Skeleton",
        "## Current Limits",
    ],
    "docs/evidence-handoff.md": [
        "# Evidence Handoff",
        "## Handoff Requirements",
        "## Readiness States",
        "## Current Limits",
    ],
}

CRITERIA_STUB_FILES = [
    "matrix/evidence-readiness.md",
    "matrix/implementation-complexity.md",
    "matrix/latency-throughput.md",
    "matrix/operational-cost.md",
    "matrix/reliability.md",
    "matrix/security-governance.md",
    "matrix/use-case-fit.md",
]


def fail(message: str) -> None:
    raise SystemExit(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def iter_text_files() -> list[Path]:
    excluded_parts = {".git", "__pycache__"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if excluded_parts.intersection(path.parts):
            continue
        if path.suffix.lower() in {".md", ".yml", ".yaml", ".py", ""}:
            files.append(path)
    return files


def validate_required_paths() -> None:
    missing_files = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    missing_dirs = [path for path in REQUIRED_DIRECTORIES if not (ROOT / path).is_dir()]
    if missing_files or missing_dirs:
        details = []
        if missing_files:
            details.append("missing files: " + ", ".join(missing_files))
        if missing_dirs:
            details.append("missing directories: " + ", ".join(missing_dirs))
        fail("; ".join(details))


def validate_foundation_markers() -> None:
    for relative_path, markers in FOUNDATION_MARKERS.items():
        text = read_text(ROOT / relative_path)
        missing_markers = [marker for marker in markers if marker not in text]
        if missing_markers:
            fail(
                f"{relative_path} is missing expected marker(s): "
                + ", ".join(missing_markers)
            )


def validate_criteria_stubs() -> None:
    required_markers = [
        "Draft status: Not drafted.",
        "Purpose:",
        "Evidence requirement:",
    ]
    for relative_path in CRITERIA_STUB_FILES:
        text = read_text(ROOT / relative_path)
        missing_markers = [marker for marker in required_markers if marker not in text]
        if missing_markers:
            fail(
                f"{relative_path} is missing expected marker(s): "
                + ", ".join(missing_markers)
            )


def validate_matrix_evidence() -> None:
    allowed_states = {"planning", "evidence_needed", "candidate", "ready", "blocked"}
    
    # 1. Parse valid taxonomy terms from llm-architecture-taxonomy
    tax_glossary_path = ROOT.parent / "llm-architecture-taxonomy" / "taxonomy" / "glossary.md"
    valid_tax_terms = set()
    if tax_glossary_path.is_file():
        tax_text = tax_glossary_path.read_text(encoding="utf-8")
        for line in tax_text.splitlines():
            if line.startswith("|") and not line.startswith("|---"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 2 and parts[0] != "Term":
                    valid_tax_terms.add(parts[0])
                    
    # 2. Check if ledger has actual claims/sources beyond README
    ledger_claims_dir = ROOT.parent / "llm-systems-research-ledger" / "claims"
    ledger_sources_dir = ROOT.parent / "llm-systems-research-ledger" / "sources"
    
    has_ledger_claims = False
    if ledger_claims_dir.is_dir():
        claim_files = [p for p in ledger_claims_dir.glob("*.md") if p.name.lower() != "readme.md"]
        if claim_files:
            has_ledger_claims = True
            
    has_ledger_sources = False
    if ledger_sources_dir.is_dir():
        source_files = [p for p in ledger_sources_dir.glob("*.md") if p.name.lower() != "readme.md"]
        if source_files:
            has_ledger_sources = True

    # 3. Scan all markdown files in the repository for evidence tables
    for path in iter_text_files():
        if path.suffix.lower() != ".md":
            continue
            
        text = read_text(path)
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("|") and i + 1 < len(lines) and lines[i+1].startswith("|---"):
                headers = [h.strip().lower() for h in line.split("|")[1:-1]]
                
                state_idx = -1
                claim_idx = -1
                source_idx = -1
                term_idx = -1
                
                for idx, h in enumerate(headers):
                    if "state" in h or "status" in h:
                        state_idx = idx
                    elif "claim" in h:
                        claim_idx = idx
                    elif "source" in h:
                        source_idx = idx
                    elif "term" in h or "taxonomy" in h:
                        term_idx = idx
                        
                if claim_idx != -1 and source_idx != -1:
                    j = i + 2
                    while j < len(lines) and lines[j].startswith("|"):
                        row_line = lines[j]
                        row_parts = [p.strip() for p in row_line.split("|")[1:-1]]
                        
                        if len(row_parts) > max(claim_idx, source_idx, state_idx, term_idx):
                            claim = row_parts[claim_idx]
                            source = row_parts[source_idx]
                            state = row_parts[state_idx].replace("`", "") if state_idx != -1 else ""
                            term = row_parts[term_idx] if term_idx != -1 else ""
                            
                            # Validate state
                            if state and state not in allowed_states:
                                fail(f"Invalid state '{state}' in {path.relative_to(ROOT)}")
                                
                            # Validate Claim ID
                            if claim != "N/A":
                                if not re.match(r"^claim-[A-Za-z0-9_\-]+$", claim):
                                    fail(f"Invalid Claim ID format '{claim}' in {path.relative_to(ROOT)}")
                                if has_ledger_claims:
                                    claim_file = ledger_claims_dir / f"{claim}.md"
                                    if not claim_file.is_file():
                                        fail(f"Referenced claim file {claim}.md does not exist in ledger repository")
                                        
                            # Validate Source ID
                            if source != "N/A":
                                if not re.match(r"^source-[A-Za-z0-9_\-]+$", source):
                                    fail(f"Invalid Source ID format '{source}' in {path.relative_to(ROOT)}")
                                if has_ledger_sources:
                                    source_file = ledger_sources_dir / f"{source}.md"
                                    if not source_file.is_file():
                                        fail(f"Referenced source file {source}.md does not exist in ledger repository")
                                        
                            # Validate Taxonomy Term
                            if term and term != "N/A" and valid_tax_terms:
                                clean_term = term
                                link_match = re.match(r"^\[([^\]]+)\]", term)
                                if link_match:
                                    clean_term = link_match.group(1)
                                if clean_term not in valid_tax_terms:
                                    fail(f"Referenced taxonomy term '{clean_term}' in {path.relative_to(ROOT)} does not exist in taxonomy glossary")
                                    
                        j += 1
                    i = j
                else:
                    i += 1
            else:
                i += 1


def lint_text() -> None:
    for path in iter_text_files():
        text = read_text(path)
        relative = path.relative_to(ROOT)
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"possible secret in {relative}: {pattern.pattern}")


def run_validate() -> None:
    validate_required_paths()
    validate_foundation_markers()
    validate_criteria_stubs()
    validate_matrix_evidence()


def run_lint() -> None:
    lint_text()


def run_test() -> None:
    run_validate()
    run_lint()


def main(argv: list[str]) -> int:
    if len(argv) == 1:
        command = "test"
    elif len(argv) == 2 and argv[1] in {"validate", "lint", "test"}:
        command = argv[1]
    else:
        print("usage: validate_repo.py {validate|lint|test}", file=sys.stderr)
        return 2

    if command == "validate":
        run_validate()
    elif command == "lint":
        run_lint()
    else:
        run_test()

    print(f"{command} ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
