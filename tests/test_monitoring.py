import unittest
from unittest.mock import patch, MagicMock
from src.monitoring import DEXTransactionMonitor

class TestDEXTransactionMonitor(unittest.TestCase):
    @patch('web3.Web3')
    def setUp(self, mock_web3):
        self.rpc_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
        self.monitor = DEXTransactionMonitor(self.rpc_url)
        self.mock_web3 = mock_web3

    def test_monitor_transactions(self):
        mock_block = {'transactions': [{'hash': '0xabc', 'gasPrice': 150 * 10**9}, {'hash': '0xdef', 'gasPrice': 50 * 10**9}]}
        self.mock_web3.eth.get_block.return_value = mock_block
        self.monitor.monitor_transactions()
        self.assertTrue(self.mock_web3.eth.get_block.called)

    def test_detect_front_running(self):
        transaction = {'hash': '0xabc', 'gasPrice': 150 * 10**9}
        with self.assertLogs(level='WARNING') as cm:
            self.monitor.detect_front_running(transaction)
            self.assertIn('Potential front-running detected', cm.output[0])

    def test_detect_sandwich_attacks(self):
        transaction = {'hash': '0xabc', 'input': '0x...'}
        with self.assertLogs(level='WARNING') as cm:
            self.monitor.detect_sandwich_attacks(transaction)
            self.assertIn('Potential sandwich attack detected', cm.output[0])

if __name__ == '__main__':
    unittest.main()