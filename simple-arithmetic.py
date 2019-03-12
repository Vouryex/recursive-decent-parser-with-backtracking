# <expression> := (<expression>) | <literal> | ~<expression> | <expression> <operator> <expression> 
# <literal>    := x | y | z
# <operator>   := + | - | * | /

# Eliminating Left Recursion
# <expression> := (<expression>) <E'> | <literal> <E'> | ~<expression> <E'>
# <E'>         := <operator> <expression> <E'> | ε
# <literal>    := x | y | z
# <operator>   := + | - | * | /

# Reformat Grammar
# <expression>  := <expression1> | <expression2> | <expression3>
# <expression1> := (<expression>) <E'>
# <expression2> := <literal> <E'>
# <expression3> := ~<expression> <E'>
# <E'>          := <E'1> | ε
# <E'1>         := <operator> <expression> <E'>
# <literal>     := x | y | z
# <operator>    := + | - | * | /

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


string = "((y+z)-~(x+y))+z"
savedCursors = []
cursor = 0
root = Node("<expression>")


def parse():
    if expression(root) and (cursor == len(string)):
        print("Input: {}".format(string))
        print("")
        print("Derivation")
        print("----------")
        print(Node.derivation(root))
        print("")
        print("Valid\n")
    else:
        print("Input: {}".format(string))
        print("Invalid")


def term(expected):
    return (cursor < len(string)) and  (string[cursor] == expected)


def expression(node):
    global cursor
    savedCursors.append(cursor)
    new_node = node.insert_child("<expression1>")
    if expression1(new_node):
        savedCursors.pop()
        return True
    cursor = savedCursors[-1]
    node.remove_child(new_node)

    new_node = node.insert_child("<expression2>")
    if expression2(new_node):
        savedCursors.pop()
        return True
    cursor = savedCursors[-1]
    node.remove_child(new_node)

    new_node = node.insert_child("<expression3>")
    if expression3(new_node):
        savedCursors.pop()
        return True
    cursor = savedCursors.pop()
    node.remove_child(new_node)

    return False


def expression1(node):
    global cursor
    if term('('):
        node.insert_child("(")
        cursor += 1
    else:
        return False

    new_node = node.insert_child("<expression>")
    if not expression(new_node):
        node.remove_child(new_node)
        return False

    if term(')'):
        node.insert_child(")")
        cursor += 1
    else:
        return False

    new_node = node.insert_child("<E'>")
    if not e_prime(new_node):
        node.remove_child(new_node)
        return False

    return True


def expression2(node):
    new_node = node.insert_child("<literal>")
    if not literal(new_node):
        node.remove_child(new_node)
        return False

    new_node = node.insert_child("<E'>")
    if not e_prime(new_node):
        node.remove_child(new_node)
        return False

    return True


def expression3(node):
    global cursor
    new_node = node.insert_child("~")
    if not term("~"):
        node.remove_child(new_node)
        return False
    cursor += 1

    new_node = node.insert_child("<expression>")
    if not expression(new_node):
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
    cursor = savedCursors.pop()
    node.insert_child("ε")
    return True

def e_prime1(node):
    new_node = node.insert_child("<operator>")
    if not operator(new_node):
        node.remove_child(new_node)
        return False

    new_node = node.insert_child("<expression>")
    if not expression(new_node):
        node.remove_child(new_node)
        return False

    new_node = node.insert_child("<E'>")
    if not e_prime(new_node):
        node.remove_child(new_node)
        return False

    return True


def literal(node):
    global cursor
    if term('x') or term('y') or term('z'):
        node.insert_child(string[cursor])
        cursor += 1
        return True
    else:
        return False


def operator(node):
    global cursor
    if term('+') or term('-') or term('*') or term('/'):
        node.insert_child(string[cursor])
        cursor += 1
        return True
    else:
        return False

parse()
