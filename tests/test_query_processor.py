import unittest
import sys
import os

# Add parent directory to path to import plugin modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from query_processor import QueryProcessor

class TestQueryProcessor(unittest.TestCase):
    def test_parse_simple_query(self):
        processor = QueryProcessor(None)
        result = processor.parse_query("show me all parks")
        self.assertIn('parks', result['layers'])
    
    def test_distance_extraction(self):
        processor = QueryProcessor(None)
        result = processor.parse_query("within 500 meters of schools")
        self.assertEqual(result['distance'], 500)
        self.assertEqual(result['unit'], 'meters')

if __name__ == '__main__':
    unittest.main()
