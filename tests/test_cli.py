import unittest
from unittest.mock import patch
from bin.cli import main, build_parser


class TestCLI(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args')
    @patch('surrogate.core.review.run_review_engine')
    def test_all_flag_explicit(self, mock_run_review_engine, mock_parse_args):
        # --all supplied (True)
        mock_parse_args.return_value = argparse.Namespace(all_issues=True)
        main()
        mock_run_review_engine.assert_called_once_with(multi_issue_mode=True)

        mock_run_review_engine.reset_mock()
        # --no-all supplied (False)
        mock_parse_args.return_value = argparse.Namespace(all_issues=False)
        main()
        mock_run_review_engine.assert_called_once_with(multi_issue_mode=False)

    def test_default_is_true(self):
        parser = build_parser()
        args = parser.parse_args([])          # no flag on the command line
        self.assertTrue(args.all_issues)      # default must be True


if __name__ == '__main__':
    unittest.main()