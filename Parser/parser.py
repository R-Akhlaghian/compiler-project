from . import grammer
from Scanner import scanner
from anytree import Node, RenderTree
class Parser:
    def __init__(self):
        grammer.load_grammar()
        grammer.load_first()
        self.scanner = scanner.Scanner()
        self.look_ahead = None
        self.root_node = None
        self.errors = []

    def match(self, token, parent):
        if token == "EPSILON":
            Node("epsilon", parent=parent)
            return True
        if self.look_ahead[0] in ["ID", "NUM"]:
            index = 0
        else:
            index = 1
        if self.look_ahead[index] == token:
            Node(f"({self.look_ahead[0]}, {self.look_ahead[1]})", parent=parent)
            self.update_look_ahead()
            return True
        else:
            self.errors.append("#" + str(self.scanner.line_number) + " : syntax error, missing " + token)
            # print("ERROR: missing", token)
            return False

    def nt_subroutine(self, nt, parent=None) -> bool:
        nt_node = Node(nt, parent=parent)
        if parent is None:
            self.root_node = nt_node

        if self.look_ahead[0] in ["ID", "NUM"]:
            index = 0
        else:
            index = 1
        result = False
        for rule in grammer.get_rules(nt):
            rule_items = rule.split()
            # print(grammer.get_first_set(rule_items[0]), self.look_ahead)
            if self.look_ahead[index] in grammer.get_first_set(rule_items[0]) or ("EPSILON" not in grammer.get_rules(nt) and "EPSILON" in grammer.get_first_set(rule_items[0])):
                result = True
                for item in rule_items:
                    if grammer.is_terminal(item):
                        result &= self.match(item, nt_node)
                    else:
                        result &= self.nt_subroutine(item, nt_node)
                    if not result:
                        break
                break
        if not result:
            if self.look_ahead[index] not in grammer.get_follow_set(nt):
                # print("ERROR: illegal " + self.look_ahead[index])
                self.errors.append("#" + str(self.scanner.line_number) + " : syntax error, illegal " + self.look_ahead[index])
                self.update_look_ahead()
                nt_node.parent = None
                result = self.nt_subroutine(nt, parent)
            elif "EPSILON" in grammer.get_rules(nt):
                self.match("EPSILON", nt_node)
                result = True
            else:
                nt_node.parent = None
                # print("ERROR: missing ", nt)
                self.errors.append("#" + str(self.scanner.line_number) + " : syntax error, missing " + nt)
                result = True

        # if not result:
        #     if "EPSILON" in grammer.get_rules(nt):
        #         self.match("EPSILON", nt_node)
        #         result = True


        # if self.look_ahead[1] == "$":
        #     if parent == self.root_node:
        #         Node("$", parent=parent)

        return result

    def print_tree(self):
        to_write = ""
        for pre, _, node in RenderTree(self.root_node):
            to_write += "%s%s" % (pre, node.name) + "\n"
            # print("%s%s" % (pre, node.name))
        with open("parse_tree.txt", "w", encoding="utf-8") as f:
            f.write(to_write)
            f.close()

    def print_errors(self):
        to_write = ""
        if len(self.errors) == 0:
            to_write = "There is no syntax error."
        else:
            for item in self.errors:
                to_write += item + "\n"
        with open("syntax_errors.txt", "w") as f:
            f.write(to_write)
            f.close()

    def parse(self):
        self.update_look_ahead()
        self.nt_subroutine(grammer.get_start_rule())
        Node("$", parent=self.root_node)
        self.print_tree()
        self.print_errors()

    def update_look_ahead(self):
        while True:
            self.look_ahead = self.scanner.get_next_token()
            if self.look_ahead[0] in ['COMMENT', 'WHITESPACE']:
                continue
            break