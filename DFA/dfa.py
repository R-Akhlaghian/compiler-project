import json


class State:
    def __init__(self):
        self.is_final = False
        self.id = 0
        self.name = None

    def transmit(self , c):
        data_file = open("dfa.json")
        data = json.load(data_file)
        data_file.close()
        transitions = data["transitions"]
        accept_all_dst = None
        for t in transitions:
            if t["state_src_id"] == self.id:
                if c in t["symbols"]:
                    return DFA().get_state_by_id(t["state_dst_id"])
                if "_" in t["symbols"]:
                    accept_all_dst = DFA().get_state_by_id(t["state_dst_id"])
        if accept_all_dst is not None:
            return accept_all_dst

    def get_type(self):
        if self.name == "com":
            return "COMMENT"
        if self.name == "num":
            return "NUM"
        if self.name == "id":
            return "ID"
        if self.name in ("sym", "eq"):
            return "SYMBOL"
        if self.name == "ws":
            return "WHITESPACE"

    def __str__(self):
        return f"[id: {self.id}, name: {self.name}, is_final: {self.is_final}]"


class DFA:

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self):
        self.states = []
        self.initial_state = None
        data_file = open("dfa.json")
        data = json.load(data_file)
        data_file.close()
        for s in data["states"]:
            new_s = State()
            new_s.id = s["id"]
            new_s.name = s["name"]
            new_s.is_final = s["end"]
            if s["start"]:
                self.initial_state = new_s

            self.states.append(new_s)

    def get_state_by_id(self, id):
        for s in self.states:
            if s.id == id:
                return s