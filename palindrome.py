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


string = "pp"
savedCursors = []
cursor = 0
root = Node("<palindrome>")

def tokenize():
    global string
    string = string.replace(" ", "").lower()

def parse():
    if palindrome(root) and (cursor == len(string)):
        print("Input: {}\n".format(string))
        print("Derivation")
        print("----------")
        print(Node.derivation(root))
        print("\nValid\n")
    else:
        print("Input: {}\n".format(string))
        print("Invalid")


def term(expected):
    # print(expected)
    return (cursor < len(string)) and  (string[cursor] == expected)


def palindrome(node):
    global cursor

    if len(string) == 1:
        cursor += 1
        node.insert_child("{}".format(string))
        return True

    current_cursor = cursor
    if current_cursor < len(string) and term(string[current_cursor]):
        node.insert_child("{}".format(string[current_cursor]))
        cursor += 1
    else:
        return palindrome2(node)

    new_node = node.insert_child("<palindrome>")
    if not palindrome(new_node):
        node.remove_children()
        cursor = current_cursor
        return palindrome2(node)

    if current_cursor < len(string) and term(string[current_cursor]):
        node.insert_child("{}".format(string[current_cursor]))
        cursor += 1
        return True
    else:
        node.remove_children()
        cursor = current_cursor
        return palindrome2(node)


def palindrome2(node):
    global cursor
    current_cursor = cursor
    if current_cursor < len(string) and term(string[current_cursor]):
        node.insert_child("{}".format(string[current_cursor]))
        cursor += 1
    else:
        node.insert_child("")
        return True

    if cursor < len(string) and term(string[cursor]):
        new_node = node.insert_child("<palindrome>")
        new_node.insert_child("{}".format(string[cursor]))
        cursor += 1
    else:
        node.remove_children()
        node.insert_child("")
        cursor = current_cursor
        return True

    if current_cursor < len(string) and term(string[current_cursor]):
        node.remove_children()
        node.insert_child("{}".format(string[current_cursor]))
        cursor += 1
        return True
    else:
        node.insert_child("")
        cursor = current_cursor
        return True


tokenize()
parse()
