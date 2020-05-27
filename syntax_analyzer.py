import lexical_analyzer as lex

NODE_PRINT = 0
NODE_COMPARE = 1
NODE_ENTER = 2
NODE_INPUT = 3

class Arith_Expression:
    def __init__(self, tokens):
        self.tokens = tokens
    def __str__(self):
        line = ""
        for token in self.tokens:
            line += str(token) + "; "
        return line

class Compare_Expression:
    def __init__(self, expression1 : Arith_Expression, operator : lex.Token, expression2 : Arith_Expression):
        self.expression1 = expression1
        self.operator = operator
        self.expression2 = expression2

    def __str__(self):
        return str(self.expression1) + " : " + str(self.operator) + " : " + str(self.expression2)


class Node:

    def get_child(self):
        pass
    def get_type(self):
        pass
    def get_root(self):
        pass

    def get_expression(self):
        pass
    def append(self, node):
        pass

class PrintNode(Node):
    def __init__(self, arith_expression : Arith_Expression):
        self.expression = arith_expression
        self.type = NODE_PRINT
        self.child = None
        self.root = None

    def get_expression(self):
        return self.expression



    def get_child(self):
        return self.child
    def get_type(self):
        return self.type
    def append(self, node : Node):
        self.child = node
        node.root = self
    def get_root(self):
        return self.root
    def __str__(self):
        return "Print Node, expr:" + str(self.expression)

class EnterNode(Node):
    def __init__(self, id_token : lex.Token, arith_expression : Arith_Expression):
        self.id = id_token
        self.expression = arith_expression
        self.type = NODE_ENTER
        self.child = None
        self.root = None

    def get_expression(self):
        return self.expression

    def get_id(self):
        return self.id

    def get_child(self):
        return self.child
    def get_type(self):
        return self.type

    def append(self, node: Node):
        self.child = node
        node.root = self

    def get_root(self):
        return self.root

    def __str__(self):
        return "Enter Node, var: " + str(self.id) + ", expr: " + str(self.expression)

class InputNode(Node):
    def __init__(self, id_token : lex.Token):
        self.id_token = id_token

        self.type = NODE_INPUT
        self.child = None
        self.root = None

    def get_id(self):
        return self.id_token

    def get_child(self):
        return self.child
    def get_type(self):
        return self.type

    def append(self, node: Node):
        self.child = node
        node.root = self

    def get_root(self):
        return self.root

    def __str__(self):
        return "Input node, var: " + str(self.id_token)

class CompareNode(Node):
    def __init__(self, compare_expression : Compare_Expression):
        self.expression = compare_expression
        self.type = NODE_COMPARE
        self.child = None
        self.if_tree = None
        self.else_tree = None
        self.root = None
        self.state = self.UNVISITED

    UNVISITED = 0
    VISITED = 1
    PASSED = 2

    def get_expression(self):
        return self.expression

    def get_child(self):
        return self.child
    def get_type(self):
        return self.type

    def append(self, node: Node):
        self.child = node
        node.root = self

    def get_root(self):
        return self.root

    def append_if_tree(self, if_tree):
        self.if_tree = if_tree
        self.if_tree.root.root = self
    def append_else_tree(self, else_tree):
        self.else_tree = else_tree
        self.else_tree.root.root = self

    def __str__(self):
        return "Compare node, expr: " + str(self.expression) + "\nif-tree:\n" + str(self.if_tree) + "\n else-tree:\n" + str(self.else_tree)

class Tree:
    def __init__(self, root: Node = None):
        self.root = None
        self.child = None

    def is_empty(self):
        return self.root is None

    def append_node(self, node : Node):
        if not self.root:
            self.root = node
            self.child = node
        else:
            self.child.append(node)
            self.child = node

    def append_tree(self, tree):
        if not tree.is_empty():
            self.append_node(tree.get_root())
            self.child = tree.get_child()

    def get_root(self):
        return self.root

    def get_child(self):
        return self.child

    def __str__(self):
        line = ""
        node = self.root
        while not(node is None):
            line += str(node) + "\n"
            node = node.get_child()

        return line


class Tree_Builder:
    def __init__(self, path, verbose=0):

        self.tokens = lex.getTokensFromFile(path)
        line = ""
        for i, token in enumerate(self.tokens):
            line += "[" + str(i) + " - " + token.__str__() + "] "
        if verbose:
            print("Tokens: ", line)
        self.init_size = len(self.tokens)
        self.tree = Tree()
        self.verbose = verbose

    def peek(self):
        return self.tokens[0]

    def pop(self):
        return self.tokens.pop(0)

    def var(self):
        if self.peek().token in (lex.CONST, lex.ID):
            return self.pop()
        else:
            return None

    def arith(self):
        if self.peek().token in lex.ARITH_EXPRESSIONS:
            return self.pop()
        else:
            return None

    def comp(self):
        if self.peek().token in lex.COMPARE_EXPRESSIONS:
            return self.pop()
        else:
            return None

    def skip(self, message):
        if self.verbose:
            print(message, " Position:", self.init_size - len(self.tokens), "Token:", self.peek())
        line = ""

        while self.peek().token not in (lex.SEMI, lex.EOF):
            line = line + self.pop().__str__()
        if self.verbose:
            print(message, " Position:", self.init_size - len(self.tokens), "Token:", self.peek())
            print("Skipped tokens:", line)

    def expr(self):
        tokens = []
        if self.verbose == 1:
            print("Expression call")

        t = self.var()
        if not t:
            return None
        tokens.append(t)

        t = self.arith()
        if t:
            tokens.append(t)

            t = self.expr()
            if not t:
                return None
            else:
                tokens.extend(t)
                if self.verbose == 1:
                    line = ""
                    for token in tokens:
                        line += "[" + token.__str__() + "] "
                    print("Tokens", line)
                return tokens
        else:
            if self.verbose == 1:
                line = ""
                for token in tokens:
                    line += "[" + token.__str__() + "] "
                print("Tokens", line)
            return tokens



    def print_st(self):
        if self.verbose == 1:
            print("Print statement call")
        if self.pop().token == lex.PRINT:
            tokens = self.expr()
            if not tokens:
                self.skip("ARITHMETIC EXPRESSION EXPECTED")
                return None
            if self.peek().token != lex.SEMI:
                self.skip("SEMICOLON EXPECTED")
                return None
            self.pop()
            if self.verbose == 1:
                print("Returned print node")
            return PrintNode(Arith_Expression(tokens))
        else:
            return None



    def enter_st(self):
        var = self.var()
        if self.verbose == 1:
            print("Enter statement call")
        if not var:
            self.skip("Expected variable")
            return None
        if self.peek().token != lex.ENTER:
            self.skip("ENTER TOKEN EXPECTED")
            return None
        self.pop()
        t = self.expr()
        if not t:
            self.skip("EXPRESSION EXPECTED")
            return None
        if self.peek().token != lex.SEMI:
            self.skip("SEMICOLON EXPECTED")
            return None
        self.pop()
        if self.verbose == 1:
            print("Returned Enter node")
        return EnterNode(var, Arith_Expression(t))

    def input_st(self):
        if self.verbose == 1:
            print("Input statement call")
        if self.pop().token != lex.INPUT:
            self.skip("INPUT EXPECTED")
            return None
        if self.peek().token != lex.ID:
            self.skip("ID expected for input statement")
            return None
        var = self.pop()
        if self.peek().token != lex.SEMI:
            self.skip("SEMICOLON EXPECTED")
            return None
        self.pop()
        input_node = InputNode(var)
        return input_node

    def if_st(self):
        if self.verbose == 1:
            print("If statement call")
        if self.pop().token != lex.IF:
            self.skip("IF EXPECTED")
            return None
        expr1 = self.expr()
        if not expr1:
            self.skip("EXPRESSION EXPECTED")
            return None

        comp = self.comp()
        if not comp:
            self.skip("COMPARISON OPERATOR EXPECTED")
            return None

        expr2 = self.expr()
        if not expr2:
            self.skip("EXPRESSION EXPECTED")
            return None
        if self.peek().token != lex.THEN:
            self.skip("EXPECTED THEN TOKEN")
            return None
        self.pop()
        compare_expression = Compare_Expression(Arith_Expression(expr1), comp, Arith_Expression(expr2))
        tree = Tree()
        compare_node = CompareNode(compare_expression)

        block_tree = self.block()
        if not block_tree:
            return None
        if self.peek().token == lex.END:
            tree.append_tree(block_tree)
            if self.verbose == 1:
                print("Returned if tree")
            return compare_node, tree
        else:
            self.skip("EXPECTED END TOKEN IN AN IF ROUTE")
            return None

    def else_st(self):
        if self.peek().token == lex.END:
            self.pop()
        while self.peek().token == lex.SEMI:
            self.pop()

        if self.verbose == 1:
            print("Else statement call")
        if self.peek().token != lex.ELSE:
            self.skip("ELSE EXPECTED")
            return None
        self.pop()

        block_tree = self.block()

        if not block_tree:
            return None
        if self.peek().token == lex.END:
            self.pop()
            if self.verbose == 1:
                print("Returned else tree")
            return block_tree
        else:
            self.skip("EXPECTED END TOKEN")
            return None

    def block(self):
        if self.verbose == 1:
            print("Block call")
        tree = Tree()
        if self.peek().token == lex.PRINT:
            print_node = self.print_st()
            if not print_node:
                self.skip("Could not create block, print_node = None")
                return None
            tree.append_node(print_node)

        elif self.peek().token == lex.ID:
            enter_node = self.enter_st()
            if not enter_node:
                self.skip("Could not create block, enter_node = None")
                return None
            tree.append_node(enter_node)
        elif self.peek().token == lex.INPUT:
            input_node = self.input_st()
            if not input_node:
                self.skip("Could not create block, input_node = None")
                return None
            tree.append_node(input_node)

        elif self.peek().token == lex.IF:
            return_value = self.if_st()
            if not return_value:
                self.skip("Could not create block for if route, if_tree or compare_node is None")
                return None
            compare_node = return_value[0]
            if_tree = return_value[1]
            compare_node.append_if_tree(if_tree)

            if self.peek().token == lex.END:
                self.pop()
            if self.peek().token == lex.SEMI:
                self.pop()

            if self.peek().token == lex.ELSE:
                if self.verbose:
                    print("Found else route")
                else_tree = self.else_st()
                if not else_tree:
                    self.skip("Could not create block for else route, else_tree is None")
                    return None
                compare_node.append_else_tree(else_tree)
            else:
                if self.verbose:
                    print("Else route not found")
            tree.append_node(compare_node)

        elif self.peek().token == lex.END:
            if self.verbose == 1:
                print("Returned empty block tree")
            return tree
        elif self.peek().token == lex.SEMI:
            self.pop()
        else:
            self.skip("Could not create block, Unexpected token")
            return None

        if self.peek().token in (lex.EOF, lex.END):
            if self.verbose == 1:
                print("Returned block tree with one statement")
            return tree

        elif self.peek().token in (lex.PRINT, lex.ID, lex.IF, lex.INPUT):
            sub_tree = self.block()
            if not sub_tree:
                print("Could not create sub tree for block")
                return None
            tree.append_tree(sub_tree)

            if self.verbose == 1:
                print("Returned block tree")
            return tree
        else:
            self.skip("Could not create block, Unexpected token (2)")
            return None

    def program(self):
        if self.verbose == 1:
            print("Program call")
        self.tree = self.block()
        if self.peek().token != lex.EOF:
            if self.verbose:
                print("Could not create tree. EOF token not found. Remained tokens:")
                for token in self.tokens:
                    print(token.__str__())
            return None
        if self.verbose == 1:
            print("Returned program tree")
        return self.tree