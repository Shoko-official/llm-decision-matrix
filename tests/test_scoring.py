import unittest
from unittest.mock import patch
from pathlib import Path
import sys

# Add root directory to sys.path so we can import scripts.validate_repo
sys.path.append(str(Path(__file__).resolve().parents[1]))
from scripts import validate_repo

# Keep a reference to the original is_file method
original_is_file = Path.is_file

def mock_is_file(self):
    path_str = str(self).replace("\\", "/")
    if "llm-architecture-taxonomy" in path_str:
        return False
    if "llm-systems-research-ledger" in path_str:
        return True
    return original_is_file(self)

class TestScoringValidation(unittest.TestCase):
    def setUp(self):
        # Monkey patch Path.is_file
        Path.is_file = mock_is_file

    def tearDown(self):
        # Restore original Path.is_file
        Path.is_file = original_is_file

    @patch("scripts.validate_repo.iter_text_files")
    @patch("scripts.validate_repo.read_text")
    def test_valid_scores(self, mock_read_text, mock_iter_text_files):
        # Setup mock files
        mock_iter_text_files.return_value = [validate_repo.ROOT / "matrix" / "test-criteria.md"]
        
        # Markdown table with valid scores
        mock_read_text.return_value = (
            "# Test Criteria\n\n"
            "| Item | State | Claim ID | Source ID | Score | Gap |\n"
            "|---|---|---|---|---|---|\n"
            "| item 1 | `ready` | claim-abc | source-xyz | 3 | None |\n"
            "| item 2 | `planning` | N/A | N/A | 0 | None |\n"
        )
        
        # Should run without raising SystemExit
        try:
            validate_repo.validate_matrix_evidence()
        except SystemExit as e:
            self.fail(f"validate_matrix_evidence raised SystemExit unexpectedly: {e}")

    @patch("scripts.validate_repo.iter_text_files")
    @patch("scripts.validate_repo.read_text")
    def test_invalid_score_range(self, mock_read_text, mock_iter_text_files):
        mock_iter_text_files.return_value = [validate_repo.ROOT / "matrix" / "test-criteria.md"]
        mock_read_text.return_value = (
            "# Test Criteria\n\n"
            "| Item | State | Claim ID | Source ID | Score | Gap |\n"
            "|---|---|---|---|---|---|\n"
            "| item 1 | `ready` | claim-abc | source-xyz | 4 | None |\n"
        )
        
        with self.assertRaises(SystemExit) as ctx:
            validate_repo.validate_matrix_evidence()
        self.assertIn("out of range", str(ctx.exception))

    @patch("scripts.validate_repo.iter_text_files")
    @patch("scripts.validate_repo.read_text")
    def test_missing_claim_for_score(self, mock_read_text, mock_iter_text_files):
        mock_iter_text_files.return_value = [validate_repo.ROOT / "matrix" / "test-criteria.md"]
        mock_read_text.return_value = (
            "# Test Criteria\n\n"
            "| Item | State | Claim ID | Source ID | Score | Gap |\n"
            "|---|---|---|---|---|---|\n"
            "| item 1 | `ready` | N/A | source-xyz | 2 | None |\n"
        )
        
        with self.assertRaises(SystemExit) as ctx:
            validate_repo.validate_matrix_evidence()
        self.assertIn("must be backed by a valid Claim ID", str(ctx.exception))

    @patch("scripts.validate_repo.iter_text_files")
    @patch("scripts.validate_repo.read_text")
    def test_missing_source_for_score(self, mock_read_text, mock_iter_text_files):
        mock_iter_text_files.return_value = [validate_repo.ROOT / "matrix" / "test-criteria.md"]
        mock_read_text.return_value = (
            "# Test Criteria\n\n"
            "| Item | State | Claim ID | Source ID | Score | Gap |\n"
            "|---|---|---|---|---|---|\n"
            "| item 1 | `ready` | claim-abc | N/A | 2 | None |\n"
        )
        
        with self.assertRaises(SystemExit) as ctx:
            validate_repo.validate_matrix_evidence()
        self.assertIn("must be backed by a valid Source ID", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
