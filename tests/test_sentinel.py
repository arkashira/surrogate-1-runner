import unittest
from unittest.mock import patch, mock_open
from bin.sentinel import scan_contracts

class TestSentinel(unittest.TestCase):
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open, read_data='pragma solidity ^0.8.0\nfunction test() public {}')
    def test_scan_contracts(self, mock_file, mock_walk):
        mock_walk.return_value = [('/test/path', [], ['contract1.sol'])]

        findings = scan_contracts('/test/path')
        self.assertEqual(len(findings), 2)  # one for pragma, one for public function
        for finding in findings:
            if finding['description'] == 'Solidity version pragma found':
                self.assertEqual(finding['severity'], 'info')
                self.assertEqual(finding['line'], 1)
            elif finding['description'] == 'Public function found':
                self.assertEqual(finding['severity'], 'warning')
                self.assertEqual(finding['line'], 2)
            else:
                self.fail("Unexpected finding")

if __name__ == '__main__':
    unittest.main()