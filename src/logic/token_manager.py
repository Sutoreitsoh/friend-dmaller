import os
class TokenManager:
    def __init__(self, tokens_file='tokens.txt'):
        self.tokens_file = os.path.join(os.getcwd(), tokens_file)
        if not os.path.exists(self.tokens_file):
            with open(self.tokens_file, 'w', encoding='utf-8') as f:
                f.write("")

    def read_tokens(self):
        try:
            with open(self.tokens_file, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            with open(self.tokens_file, 'w', encoding='utf-8') as f:
                f.write("")
            return []

    def write_tokens(self, tokens):
        with open(self.tokens_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(tokens))

    def clear_tokens(self):
        self.write_tokens([])

    def count_tokens(self):
        tokens = self.read_tokens()
        return len(tokens)

    def save_tokens(self, tokens):
        with open(self.tokens_file, 'w', encoding='utf-8') as f:
            for token in tokens:
                f.write(token + '\n')