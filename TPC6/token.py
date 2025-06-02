class Token:
    """Represents a single token with its type and value."""
    def __init__(self, category, content):
        self.category = category
        self.content = content

class Tokenizer:
    """Breaks down an arithmetic expression into tokens."""
    def __init__(self, input_text):
        self.input_text = input_text
        self.position = 0
        self.current_symbol = self.input_text[self.position] if self.position < len(self.input_text) else None

    def move_forward(self):
        """Advances to the next character in the input text."""
        self.position += 1
        self.current_symbol = self.input_text[self.position] if self.position < len(self.input_text) else None

    def ignore_whitespace(self):
        """Skips over any whitespace characters."""
        while self.current_symbol is not None and self.current_symbol.isspace():
            self.move_forward()

    def extract_number(self):
        """Extracts a number from the input text."""
        digits = ''
        while self.current_symbol is not None and self.current_symbol.isdigit():
            digits += self.current_symbol
            self.move_forward()
        return int(digits)

    def get_next_token(self):
        """Returns the next token from the input text."""
        while self.current_symbol is not None:
            if self.current_symbol.isspace():
                self.ignore_whitespace()
                continue
            if self.current_symbol.isdigit():
                return Token('NUM', self.extract_number())
            if self.current_symbol == '+':
                self.move_forward()
                return Token('PLUS', '+')
            if self.current_symbol == '-':
                self.move_forward()
                return Token('MINUS', '-')
            if self.current_symbol == '*':
                self.move_forward()
                return Token('TIMES', '*')
            if self.current_symbol == '(':
                self.move_forward()
                return Token('LPAREN', '(')
            if self.current_symbol == ')':
                self.move_forward()
                return Token('RPAREN', ')')
            self.raise_error()
        return Token('EOF', None)

    def raise_error(self):
        """Raises an error for an invalid character."""
        raise Exception(f"Invalid character detected: {self.current_symbol}")