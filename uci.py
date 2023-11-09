class UCIEngine:
    def __init__(self, board):
        self.board = board

    def parse_uci_command(self, command):
        # Parse and handle UCI commands here
        pass

    def run(self):
        while True:
            command = input()
            self.parse_uci_command(command)