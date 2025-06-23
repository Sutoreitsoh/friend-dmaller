class MessageManager:
    def __init__(self, messages_file='messages.txt'):
        self.messages_file = messages_file

    def read_messages(self):
        try:
            with open(self.messages_file, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return ""

    def write_messages(self, new_content):
        with open(self.messages_file, 'w', encoding='utf-8') as file:
            file.write(new_content)