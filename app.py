from flask import Flask, render_template, request

app = Flask(__name__)

class LexicalAnalyzer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.current_token = None
        self.current_lexeme = None

    def get_next_token(self):
        if self.input_string:
            self.input_string = self.input_string.strip()
            if self.input_string.startswith("do"):
                self.current_token = "do"
                self.current_lexeme = "do"
                self.input_string = self.input_string[2:]
            elif self.input_string.startswith("while"):
                self.current_token = "while"
                self.current_lexeme = "while"
                self.input_string = self.input_string[5:]
            elif self.input_string.startswith("{"):
                self.current_token = "{"
                self.current_lexeme = "{"
                self.input_string = self.input_string[1:]
            elif self.input_string.startswith("}"):
                self.current_token = "}"
                self.current_lexeme = "}"
                self.input_string = self.input_string[1:]
            elif self.input_string.startswith("("):
                self.current_token = "("
                self.current_lexeme = "("
                self.input_string = self.input_string[1:]
            elif self.input_string.startswith(")"):
                self.current_token = ")"
                self.current_lexeme = ")"
                self.input_string = self.input_string[1:]
            elif self.input_string.startswith("="):
                self.current_token = "="
                self.current_lexeme = "="
                self.input_string = self.input_string[1:]
            elif self.input_string.startswith(";"):
                self.current_token = ";"
                self.current_lexeme = ";"
                self.input_string = self.input_string[1:]
            elif self.input_string.startswith("+"):
                self.current_token = "operator"
                self.current_lexeme = "+"
                self.input_string = self.input_string[1:]
            elif self.input_string.startswith("-"):
                self.current_token = "operator"
                self.current_lexeme = "-"
                self.input_string = self.input_string[1:]
            elif self.input_string.startswith("=="):
                self.current_token = "comparison"
                self.current_lexeme = "=="
                self.input_string = self.input_string[2:]
            elif self.input_string.startswith(">="):
                self.current_token = "comparison"
                self.current_lexeme = ">="
                self.input_string = self.input_string[2:]
            elif self.input_string.startswith("<="):
                self.current_token = "comparison"
                self.current_lexeme = "<="
                self.input_string = self.input_string[2:]
            elif self.input_string.startswith("<"):
                self.current_token = "comparison"
                self.current_lexeme = "<"
                self.input_string = self.input_string[1:]
            elif self.input_string.startswith(">"):
                self.current_token = "comparison"
                self.current_lexeme = ">"
                self.input_string = self.input_string[1:]
            elif self.input_string.startswith("a"):
                self.current_token = "variable"
                self.current_lexeme = "a"
                self.input_string = self.input_string[1:]
            elif self.input_string.startswith("b"):
                self.current_token = "variable"
                self.current_lexeme = "b"
                self.input_string = self.input_string[1:]
            else:
                self.current_token = "error"
                self.current_lexeme = self.input_string[0]
                self.input_string = self.input_string[1:]
        else:
            self.current_token = "EOF"
            self.current_lexeme = ""

    def analyze(self):
        tokens = []
        while self.current_token != "EOF":
            self.get_next_token()
            tokens.append((self.current_token, self.current_lexeme))
        return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def match(self, expected_token):
        if self.tokens[self.current_token_index][0] == expected_token:
            self.current_token_index += 1
        else:
            raise SyntaxError("Syntax error: Expected '{}' but found '{}'.".format(expected_token,
                                                                                   self.tokens[self.current_token_index][1]))

    def parse_variable(self):
        if self.tokens[self.current_token_index][0] == "variable":
            self.match("variable")

    def parse_operator(self):
        if self.tokens[self.current_token_index][0] == "operator":
            self.match("operator")

    def parse_comparison(self):
        if self.tokens[self.current_token_index][0] == "comparison":
            self.match("comparison")

    def parse_expression(self):
        self.parse_variable()
        self.parse_operator()
        self.parse_variable()

    def parse_condition(self):
        self.match("(")
        self.parse_variable()
        self.parse_comparison()
        self.parse_variable()
        self.match(")")
        self.match(";")

    def parse_action(self):
        self.match("{")
        self.parse_variable()
        self.match("=")
        self.parse_expression()
        self.match(";")
        self.match("}")

    def parse_statement(self):
        self.match("do")
        self.parse_action()
        self.match("while")
        self.parse_condition()

    def parse(self):
        try:
            self.parse_statement()
            if self.tokens[self.current_token_index][0] == "EOF":
                print("Parsing completed successfully.")
                return True
            else:
                print("Parsing failed. Unexpected token '{}'.".format(self.tokens[self.current_token_index][1]))
        except SyntaxError as e:
            print("Parsing failed. {}".format(str(e)))
        return False
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_string = request.form['code']
        lexer = LexicalAnalyzer(input_string)
        tokens = lexer.analyze()

        # Create a list of token codes
        token_codes = [token[1] for token in tokens]

        parser = Parser(tokens)
        if parser.parse():
            result = "Input diterima."
        else:
            result = "Input ditolak."

        return render_template('index.html', token_codes=token_codes, result=result)
    else:
        return render_template('index.html', token_codes=None, result=None)

if __name__ == '__main__':
    app.run(debug=True)
