class QueryProcessor:
    def __init__(self, iface):
        self.iface = iface
        self.layer_synonyms = {
            'schools': ['school', 'education', 'academy'],
            'parks': ['park', 'garden', 'recreation'],
        }
        self.operation_patterns = {
            'within': r'within (\d+) (\w+) of',
        }

    def parse_query(self, query_text):
        """
        Process a natural language query.
        
        Args:
            query_text: The natural language query string
            
        Returns:
            Dictionary containing interpretation and results
        """
        result = {
            'layers': [],
            'distance': None,
            'unit': None
        }
        
        # Simple keyword matching for layers
        for layer_type, synonyms in self.layer_synonyms.items():
            if layer_type in query_text or any(s in query_text for s in synonyms):
                result['layers'].append(layer_type)
        
        # Simple distance extraction (hardcoded for the example)
        if "within" in query_text:
            import re
            match = re.search(r'within (\d+) (\w+)', query_text)
            if match:
                result['distance'] = int(match.group(1))
                result['unit'] = match.group(2)
                
        return result
