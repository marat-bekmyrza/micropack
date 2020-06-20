import networkx as nx
import matplotlib.pyplot as plt


OPERATORS = {'+', '-', '*', '/'}
PRECEDENCE = {'+': 0, '-': 0, '*': 1, '/': 1}


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.level = 0

    def set_value(self, value):
        self.value = value

    def set_level(self, level):
        self.level = level

    def insert_left(self, node):
        self.left = node

    def insert_right(self, node):
        self.right = node

    def insert_data(self, node):
        if self.left is None:
            self.left = node
        elif self.right is None:
            self.right = node

    def get_value(self):
        return self.value

    def get_level(self):
        return self.level

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right


class ExpressionTree:
    def __init__(self, equation):
        self.root = Node('')
        self.graph = nx.DiGraph()
        current_node = self.root
        roots_stack, currents_stack, op_stack = [], [], []
        last_op = ''
        root_value = equation[0]

        for element in equation[2:]:
            if element in OPERATORS:    # operator
                if last_op == '':   # first operator
                    current_node.set_value(element)
                elif PRECEDENCE[element] > PRECEDENCE[last_op]:     # go lower of current node
                    right_node = current_node.get_right()
                    current_node.insert_right(Node(element))
                    current_node = current_node.get_right()
                    current_node.insert_data(right_node)
                else:
                    new_node = Node(element)
                    if PRECEDENCE[element] == 0 or current_node == self.root:   # go upper of root node
                        new_node.insert_left(self.root)
                        self.root = new_node
                    else:   # go upper of current node
                        new_node.insert_left(current_node)
                        self.root.insert_right(new_node)
                    current_node = new_node
                last_op = element
            elif element == '(':
                roots_stack.append(self.root)
                currents_stack.append(current_node)
                op_stack.append(last_op)
                self.root = Node('')
                current_node = self.root
                last_op = ''
            elif element == ')':
                last_current = currents_stack.pop()
                last_current.insert_data(self.root)
                self.root = roots_stack.pop()
                current_node = last_current
                last_op = op_stack.pop()
            else:   # data
                current_node.insert_data(Node(element))

        if self.root.get_value() == '':
            self.root.set_value(root_value)
        else:
            root = self.root
            self.root = Node(root_value)
            self.root.insert_left(root)

        def assign_levels(node, level=0):
            self.graph.add_node(node)
            node.set_level(level)
            # print(node.get_value(), node.get_level())
            level += 1
            if node.left:
                self.graph.add_edge(node.get_left(), node)
                assign_levels(node.get_left(), level)
            if node.right:
                self.graph.add_edge(node.get_right(), node)
                assign_levels(node.get_right(), level)

        assign_levels(self.root)

    def draw(self):
        labels, pos = {}, {}
        node_color = ""
        size = []
        x = 0

        for node in self.graph.nodes:
            labels[node] = node.get_value()

            if node.get_value() in OPERATORS:
                node_color += "r"
            else:
                node_color += "c"

            pos[node] = (x, node.get_level())
            x += 1
            size.append(len(node.get_value())*200)

        nx.draw(self.graph, node_size=size, pos=pos, node_color=node_color, labels=labels, font_size=10, with_labels=True)
        plt.savefig('graph.png')


def get_equation(file_name):
    with open(file_name, "r") as file:
        equation = file.readline().strip().replace(' ', '')
    return equation


expression = get_equation('input.txt')
tree = ExpressionTree(expression)
tree.draw()

