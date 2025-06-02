import re

class Lexeme:
    """Represents a single token with its category, content, and line position."""
    def __init__(self, category, content, line_position):
        self.category = category
        self.content = content
        self.line_position = line_position

    def __str__(self):
        return f"[{self.category}: {self.content}, line={self.line_position}]"

class QueryTokenizer:
    """Tokenizes a query string into lexical units for analysis."""
    def __init__(self):
        # Define token categories and their regex patterns
        self.token_patterns = [
            ('COMMENT', r'#.*$'),              # Lines starting with # for comments
            ('KEYWORD', r'select|where|LIMIT'), # Query keywords
            ('VARIABLE', r'\?[a-zA-Z][a-zA-Z]*'), # Query variables like ?name
            ('LANG_STRING', r'"[^"]*"@[a-z]{2}'), # Strings with language tags
            ('PLAIN_STRING', r'"[^"]*"'),      # Plain quoted strings
            ('URI', r'[a-z]+:[a-zA-Z][a-zA-Z]*'), # URI patterns like dbo:artist
            ('NUMBER', r'\d+'),                # Integer numbers
            ('SYMBOL', r'[{}.,]'),             # Special symbols
            ('WHITESPACE', r'\s+'),            # Whitespace characters
            ('WORD', r'[a-zA-Z]+'),            # Generic words
        ]
        # Combine patterns into a single regex for matching
        self.combined_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_patterns)

    def parse_tokens(self, query_text):
        """Break down the query text into a list of lexical units."""
        token_list = []
        current_line = 1
        
        # Process each line of the query
        for line_text in query_text.splitlines():
            for match in re.finditer(self.combined_regex, line_text):
                for token_category, _ in self.token_patterns:
                    token_content = match.group(token_category)
                    if token_content is not None:
                        # Skip whitespace tokens
                        if token_category != 'WHITESPACE':
                            token_list.append(Lexeme(token_category, token_content, current_line))
                        break
            current_line += 1
            
        return token_list

# Test the tokenizer with a sample query
def test_tokenizer():
    sample_query = """
    # DBPedia: works by Ella Fitzgerald
    select 
     ?title ?summary 
    where {
     ?s a dbo:MusicalArtist .
     ?s foaf:name "Ella Fitzgerald"@en .
     ?w dbo:artist ?s .
     ?w foaf:name ?title .
     ?w dbo:abstract ?summary
    } LIMIT 500
    """
    
    tokenizer = QueryTokenizer()
    tokens = tokenizer.parse_tokens(sample_query)
    
    # Display the identified tokens
    print("=== Identified Tokens ===")
    for token in tokens:
        print(token)

if __name__ == "__main__":
    test_tokenizer()