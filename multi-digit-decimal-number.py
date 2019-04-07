# <expr> ::= +<num> | -<num> | <num>
# <num> ::= <digits> | <digits>.<digits>
# <digits> ::= <digits><digit> | <digit>
# <digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
# Note: Terminate every input string with '$'

# Eliminating Left Recursion 
# <expr> ::= +<num> | -<num> | <num>
# <num> ::= <digits> | <digits>.<digits>
# <digits> ::= <digit><E'>
# <E'> ::= <digit><E'> | ε
# <digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9

# Left Factoring to achieve Pairwise Disjointness
# <expr> ::= +<num> | -<num> | <num>
# <num> ::= <digits><N>
# <N> ::= .<digits> | ε 
# <digits> ::= <digit><E'>
# <E'> ::= <digit><E'> | ε
# <digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9

# Reformat Grammar
# <expr> ::= <expr1> | <expr2> | <num>
# <expr1> ::= +<num>
# <expr2> ::= -<num>
# <num> ::= <digits><N>
# <N> ::= .<digits> | ε 
# <digits> ::= <digit><E'>
# <E'> ::= <digit><E'> | ε
# <digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9


class Node:

    derive_queue = []

    def __init__(self, data):
        self.children = []
        self.data = data

    def insert_child(self, data):
        new_node = Node(data)
        self.children.append(new_node)
        return new_node

    def remove_child(self, node):
        self.children.remove(node)

    def remove_children(self):
        self.children.clear()

    @staticmethod
    def nodes_has_child(derive_queue):
        for curr in derive_queue:
            curr_node = curr["node"]
            if curr_node.children:
                return True
        return False

    @staticmethod
    def nodes_same_level(level, derive_queue):
        for curr in derive_queue:
            curr_level = curr["level"]
            if curr_level != level:
                return False
        return True

    @staticmethod
    def derivation(node):
        derivation = ""
        derive_queue = Node.derive_queue
        derive_queue.append({"node":node, "level":0})
        prev_level = 0

        while derive_queue:
            curr = derive_queue.pop(0)
            curr_node = curr["node"]
            curr_level = curr["level"]
            if prev_level < curr_level:
                derivation += "\n"
                prev_level = curr_level
            for child in curr_node.children:
                derive_queue.append({"node":child, "level":curr_level+1})
            if not curr_node.children and Node.nodes_has_child(derive_queue):
                derive_queue.append({"node":curr_node, "level":curr_level+1})
            elif not curr_node.children and not Node.nodes_same_level(curr_level, derive_queue):
                derive_queue.append({"node":curr_node, "level":curr_level+1})
            derivation += curr_node.data

        return derivation


string = "+9.99$"
savedCursors = []
cursor = 0
root = Node("<expr>")
grammar = """# <expr> ::= <expr1> | <expr2> | <num>
# <expr1> ::= +<num>
# <expr2> ::= -<num>
# <num> ::= <digits><N>
# <N> ::= .<digits> | ε
# <digits> ::= <digit><E'>
# <E'> ::= <digit><E'> | ε
# <digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9"""


def parse():
    print("Input: {}".format(string), end="\n\n")
    if expr(root) and string[cursor] == '$':
        print("Grammar")
        print("-------")
        print(grammar, end="\n\n")
        print("Derivation")
        print("----------")
        print(Node.derivation(root), end="\n\n")
        print("Valid")
    else:
        print("Invalid")


def terminal(expected):
    # print("expected: {}".format(expected))
    # print("string[cursor]: {}".format(string[cursor]))
    return string[cursor] != '$' and string[cursor] == expected


def expr(node):
    global cursor
    savedCursors.append(cursor)
    new_node = node.insert_child("<expr1>")
    if expr1(new_node):
        return True
    cursor = savedCursors[-1]
    node.remove_child(new_node)

    new_node = node.insert_child("<expr2>")
    if expr2(new_node):
        return True
    cursor = savedCursors[-1]
    node.remove_child(new_node)

    new_node = node.insert_child("<num>")
    if num(new_node):
        return True
    cursor = savedCursors.pop()
    node.remove_child(new_node)

    return False


def expr1(node):
    global cursor
    if not terminal('+'):
        return False
    cursor += 1
    node.insert_child('+')

    new_node = node.insert_child("<num>")
    if not num(new_node):
        return False

    return True


def expr2(node):
    global cursor
    if not terminal('-'):
        return False
    cursor += 1
    node.insert_child('-')

    new_node = node.insert_child("<num>")
    if not num(new_node):
        return False

    return True


def num(node):
    new_node = node.insert_child("<digits>")
    if not digits(new_node):
        return False

    new_node = node.insert_child("<N>")
    if not N(new_node):
        return False

    return True


def N(node):
    global cursor
    savedCursors.append(cursor)
    if not terminal('.'):
        savedCursors.pop()
        node.insert_child('ε')
        return True
    node.insert_child('.')
    cursor += 1

    new_node = node.insert_child("<digits>")
    if not digits(new_node):
        cursor = savedCursors.pop()
        node.remove_children()
        node.insert_child('ε')
        return True

    savedCursors.pop()
    return True


def digits(node):
    new_node = node.insert_child("<digit>")
    if not digit(new_node):
        return False

    new_node = node.insert_child("<E'>")
    if not e_prime(new_node):
        return False

    return True


def e_prime(node):
    global cursor
    savedCursors.append(cursor)
    new_node = node.insert_child("<digit>")
    if not digit(new_node):
        cursor = savedCursors.pop()
        node.remove_child(new_node)
        node.insert_child('ε')
        return True

    new_node = node.insert_child("<E'>")
    if not e_prime(new_node):
        cursor = savedCursors.pop()
        node.remove_children()
        node.insert_child('ε')
        return True

    return True


def digit(node):
    global cursor
    digits = range(0, 10)
    for digit in digits:
        if terminal(str(digit)):
            cursor += 1
            node.insert_child("{}".format(str(digit)))
            return True
    return False


parse()
