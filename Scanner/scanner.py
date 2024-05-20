import re

from DFA import DFA


class Scanner:
    def __init__(self):
        self.line_number = 1
        self.dfa = DFA()
        self.symbol_table = []
        self.input_file = open("input.txt")
        self.current_char = None

    def get_next_token(self):
        current_token = ""
        current_state = self.dfa.initial_state
        while True:
            if self.current_char is None:
                c = self.input_file.read(1)
                if c == "":
                    return "", "$"
            else:
                c = self.current_char
                self.current_char = None
            current_token += c
            new_c = Scanner.char_to_type(c)
            prev_state = current_state
            current_state = current_state.transmit(new_c)
            if current_state is None:
                self.current_char = c
                if c == "\n":
                    self.line_number += 1
                current_token = current_token[:-1]
                if prev_state.is_final:
                    if current_token in ("if", "else", "void", "int", "for", "break", "return", "endif"):
                        return "KEYWORD", current_token
                    return prev_state.get_type(), current_token
                else:
                    if c == "":
                        return "", "$"
                    return None

    @staticmethod
    def char_to_type(c):
        if re.search("[A-Za-z]", c) is not None:
            return "a"
        if re.search("[0-9]", c) is not None:
            return "d"
        if re.search("\\s", c) is not None:
            return "w"
        if re.search("[;:,\\[\\](){}+\\-<]", c) is not None:
            return "s"
        return c
