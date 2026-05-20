import unittest
import os
import yaml

class TestAliasMapper(unittest.TestCase):
    def test_alias_mapping(self):
        aliases = {'alias1': 'kb_id1', 'alias2': 'kb_id2'}
        self.assertEqual(lookup_alias('alias1', aliases), 'kb_id1')
        self.assertEqual(lookup_alias('alias2', aliases), 'kb_id2')
        self.assertIsNone(lookup_alias('unknown_alias', aliases))

def lookup_alias(alias, aliases):
    return aliases.get(alias)

if __name__ == '__main__':
    unittest.main()