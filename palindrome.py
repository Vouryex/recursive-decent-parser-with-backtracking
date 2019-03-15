# <palindrome> := a<palindrome>a | b<palindrome>b | ... | z<palindrome>z | A<palindrome>A | B<palindrome>B | ... | 1<palindrome>1 ... `<palindrome>` | *<palindrome* ...
# <palindrome> := a | b | ... | z | A | B | ... | 1 | ` | * | ε | ... 

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


string = "Was It A Rat I Saw"
savedCursors = []
cursor = 0
root = Node("<palindrome>")

def tokenize():
    global string
    string = string.replace(" ", "").lower()

def parse():
    if palindrome() and (cursor == len(string)):
        print("String: {}\n".format(string))
        print("Valid\n")
        print("Derivation")
        print("----------\n")
        # print(Node.derivation(root))
    else:
        print("Invalid")


def term(expected):
    # print(expected)
    return (cursor < len(string)) and  (string[cursor] == expected)


def palindrome():
    global cursor

    if len(string) == 1:
        cursor += 1
        return True

    current_cursor = cursor
    if current_cursor < len(string) and term(string[current_cursor]):
        cursor += 1
    else:
        return palindrome2()

    if not palindrome():
        cursor = current_cursor
        return palindrome2()

    if current_cursor < len(string) and term(string[current_cursor]):
        cursor += 1
        return True
    else:
        cursor = current_cursor
        return palindrome2()


def palindrome2():
    global cursor
    current_cursor = cursor
    if current_cursor < len(string) and term(string[current_cursor]):
        cursor += 1
    else:
        return True

    if cursor < len(string) and term(string[cursor]):
        cursor += 1
    else:
        cursor = current_cursor
        return True

    if current_cursor < len(string) and term(string[current_cursor]):
        cursor += 1
        return True
    else:
        cursor = current_cursor
        return True


tokenize()
parse()
