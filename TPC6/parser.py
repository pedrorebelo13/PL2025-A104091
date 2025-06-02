from tokenizer import Tokenizer

class Token:
    """Represents a single token with its type and value."""
    def __init__(self, category, content):
        self.category = category
        self.content = content

class MathExpressionParser:
    """Parses and evaluates arithmetic expressions using an LL(1) recursive descent approach."""
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.get_next_token()

    def raise_error(self, message):
        """Raises a parsing error with a custom message."""
        raise Exception(f"Parsing error: {message}")

    def consume(self, expected_type):
        """Consumes the current token if it matches the expected type."""
        if self.current_token.category == expected_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            self.raise_error(f"Expected {expected_type}, found {self.current_token.category}")

    def parse_expression(self):
        """Expr → Term ExprTail"""
        value = self.parse_term()
        value = self.parse_expression_tail(value)
        return value

    def parse_expression_tail(self, accumulated_value):
        """ExprTail → + Term ExprTail | - Term ExprTail | ε"""
        if self.current_token.category == 'PLUS':
            self.consume('PLUS')
            next_term = self.parse_term()
            new_value = accumulated_value + next_term
            return self.parse_expression_tail(new_value)
        elif self.current_token.category == 'MINUS':
            self.consume('MINUS')
            next_term = self.parse_term()
            new_value = accumulated_value - next_term
            return self.parse_expression_tail(new_value)
        return accumulated_value  # Epsilon production

    def parse_term(self):
        """Term → Factor TermTail"""
        value = self.parse_factor()
        value = self.parse_term_tail(value)
        return value

    def parse_term_tail(self, accumulated_value):
        """TermTail → * Factor TermTail | ε"""
        if self.current_token.category == 'TIMES':
            self.consume('TIMES')
            next_factor = self.parse_factor()
            new_value = accumulated_value * next_factor
            return self.parse_term_tail(new_value)
        return accumulated_value  # Epsilon production

    def parse_factor(self):
        """Factor → ( Expr ) | num"""
        if self.current_token.category == 'NUM':
            number = int(self.current_token.content)
            self.consume('NUM')
            return number
        elif self.current_token.category == 'LPAREN':
            self.consume('LPAREN')
            value = self.parse_expression()
            self.consume('RPAREN')
            return value
        else:
            self.raise_error("Expected a number or an opening parenthesis")

    def evaluate(self):
        """Starts parsing from the initial expression rule."""
        result = self.parse_expression()
        if self.current_token.category != 'EOF':
            self.raise_error("Incomplete expression")
        return result

def main():
    expression = input("Enter an arithmetic expression: ")
    tokenizer = Tokenizer(expression)
    parser = MathExpressionParser(tokenizer)
    try:
        result = parser.evaluate()
        print(f"Evaluation result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()