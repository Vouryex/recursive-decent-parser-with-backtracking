# <expr> ::= <expr>+<term> | <expr>-<term> | <term>
# <term> ::= <term>*<factor> | <term>/<factor> | <factor>
# <factor> ::= (<expr>) | <digit>
# <digit> ::= 0 | 1 | 2 | 3
# Note: Terminate every input string with '$'

# Eliminating Left Recursion
# <expr> ::= <term><E'>
# <E'> ::= +<term><E'> | -<term><E'> | ε
# <term> ::= <factor><F'>
# <F'> ::= *<factor><F'> | /<factor><F'> | ε
# <factor> ::= (<expr>) | <digit>
# <digit> ::= 0 | 1 | 2 | 3

# Reformat Grammar
# <expr> ::= <term><E'>
# <E'> ::= <E'1> | <E'2> | ε
# <E'1> ::= +<term><E'>
# <E'2> ::= -<term><E'>
# <term> ::= <factor><F'>
# <F'> ::= <F'1> | <F'2 | ε
# <F'1> ::= *<factor><F'>
# <F'2> ::= /<factor><F'>
# <factor> ::= <factor1> | <digit>
# <factor1> ::= (<expr>)
# <digit> ::= 0 | 1 | 2 | 3

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

string = "3/$"
savedCursors = []
cursor = 0
root = Node("<expr>")
grammar = """# <expr> ::= <term><E'>
# <E'> ::= <E'1> | <E'2> | ε
# <E'1> ::= +<term><E'>
# <E'2> ::= -<term><E'>
# <term> ::= <factor><F'>
# <F'> ::= <F'1> | <F'2 | ε
# <F'1> ::= *<factor><F'>
# <F'2> ::= /<factor><F'>
# <factor> ::= <factor1> | <digit>
# <factor1> ::= (<expr>)
# <digit> ::= 0 | 1 | 2 | 3"""


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
    new_node = node.insert_child("<term>")
    if not term(new_node):
        node.remove_child(new_node)
        return False

    new_node = node.insert_child("<E'>")
    if not e_prime(new_node):
        node.remove_child(new_node)
        return False

    return True


def e_prime(node):
    global cursor
    savedCursors.append(cursor)
    new_node = node.insert_child("<E'1>")
    if e_prime1(new_node):
        savedCursors.pop()
        return True
    node.remove_child(new_node)
    cursor = savedCursors[-1]

    new_node = node.insert_child("<E'2>")
    if e_prime2(new_node):
        savedCursors.pop()
        return True
    node.remove_child(new_node)
    cursor = savedCursors.pop()

    new_node = node.insert_child("ε")
    return True


def e_prime1(node):
    global cursor
    if not terminal('+'):
        return False
    cursor += 1
    node.insert_child('+')

    new_node = node.insert_child("<term>")
    if not term(new_node):
        node.remove_child(new_node)
        return False

    new_node = node.insert_child("<E'>")
    if not e_prime(new_node):
        node.remove_child(new_node)
        return False

    return True


def e_prime2(node):
    global cursor
    if not terminal('-'):
        return False
    cursor += 1
    node.insert_child('-')

    new_node = node.insert_child("<term>")
    if not term(new_node):
        node.remove_child(new_node)
        return False

    new_node = node.insert_child("<E'>")
    if not e_prime(new_node):
        node.remove_child(new_node)
        return False

    return True


def term(node):
    new_node = node.insert_child("<factor>")
    if not factor(new_node):
        node.remove_child(new_node)
        return False

    new_node = node.insert_child("<F'>")
    if not f_prime(new_node):
        node.remove_child(new_node)
        return False

    return True


def f_prime(node):
    global cursor
    savedCursors.append(cursor)
    new_node = node.insert_child("<F'1>")
    if f_prime1(new_node):
        savedCursors.pop()
        return True
    node.remove_child(new_node)
    cursor = savedCursors[-1]

    new_node = node.insert_child("<F'2>")
    if f_prime2(new_node):
        savedCursors.pop()
        return True
    node.remove_child(new_node)
    cursor = savedCursors.pop()

    node.insert_child("ε")
    return True


def f_prime1(node):
    global cursor
    if not terminal('*'):
        return False
    cursor += 1
    node.insert_child('*')

    new_node = node.insert_child("<factor>")
    if not factor(new_node):
        node.remove_child(new_node)
        return False

    new_node = node.insert_child("<F'>")
    if not f_prime(new_node):
        node.remove_child(new_node)
        return False

    return True


def f_prime2(node):
    global cursor
    if not terminal('/'):
        return False
    cursor += 1
    node.insert_child('/')

    new_node = node.insert_child("<factor>")
    if not factor(new_node):
        node.remove_child(new_node)
        return False

    new_node = node.insert_child("<F'>")
    if not f_prime(new_node):
        print("inside f prime false")
        node.remove_child(new_node)
        return False

    return True


def factor(node):
    global cursor
    savedCursors.append(cursor)
    new_node = node.insert_child("<factor1>")
    if factor1(new_node):
        savedCursors.pop()
        return True
    node.remove_child(new_node)
    cursor = savedCursors[-1]

    new_node = node.insert_child("<digit>")
    if digit(new_node):
        savedCursors.pop()
        return True
    node.remove_child(new_node)
    cursor = savedCursors.pop()

    return False


def factor1(node):
    global cursor
    if not terminal('('):
        return False
    cursor += 1
    node.insert_child('(')

    new_node = node.insert_child("<expr>")
    if not expr(new_node):
        node.remove_child(new_node)
        return False

    if not terminal(')'):
        return False
    cursor += 1
    node.insert_child(')')

    return True


def digit(node):
    global cursor
    if terminal('0') or terminal('1') or terminal('2') or terminal('3'):
        node.insert_child(string[cursor])
        cursor += 1
        return True
    return False


parse()
