import syntax_analyzer as syn
import lexical_analyzer as lex



class Tree_Executor:
    def __init__(self, tree : syn.Tree):
        self.tree = tree
        self.stack = {}

    reserved_arithmetic_operations = {
        '+': (lambda a, b: a + b),
        '-': (lambda a, b: a - b),
        '*': (lambda a, b: a * b),
        '/': (lambda a, b: a / b)
    }

    reserved_compare_operations = {
        '>': (lambda a, b: a > b),
        '>=': (lambda a, b: a >= b),
        '<': (lambda a, b: a < b),
        '<=': (lambda a, b: a <= b),
        '==': (lambda a, b: a == b)
    }

    def get_var(self, token : lex.Token):
        if token.token == lex.ID:
            if token.value in self.stack:
                return self.stack[token.value]
            else:
                print("Could not find variable in stack")
                return None
        else:
            print("WRONG token type, expected ID")
            return None

    def put_var(self, token : lex.Token, value : int):
        if token.token == lex.ID:
            self.stack[token.value] = value
            return True
        else:
            print("Expected ID token type")
            return None

    def get_expression_value(self, expression : syn.Arith_Expression):
        tokens = expression.tokens
        out = []
        stack = []
        def check_stack():
            for t in stack:
                if t.token in (lex.TIMES, lex.DIVIDE):
                    return False
            return True


        for t in tokens:
            if t.token in lex.ARITH_EXPRESSIONS:
                if t.token in (lex.PLUS, lex.MINUS):
                    if len(stack) < 1:
                        stack.append(t)
                    else:
                        out.append(stack.pop())
                        stack.append(t)
                else:

                    if (len(stack) < 1) or check_stack():
                        stack.append(t)
                    else:
                        while len(stack) > 0:
                            out.append(stack.pop())
                        stack.append(t)
            else:
                out.append(t)
        while len(stack) > 0:
            out.append(stack.pop())

        line = ""
        for t in out:
            line += '[' + t.__str__() + "] "
        print("POLISH NOTATION:", line)

        for t in out:
            if t.token == lex.CONST:
                stack.append(t.value)
            elif t.token == lex.ID:
                value = self.get_var(t)
                if not value:
                    return None
                stack.append(value)
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(self.reserved_arithmetic_operations[t.value](a, b))
        value = stack.pop()
        line = ""
        for t in expression.tokens:
            line += '[' + t.__str__() + "] "
        print("Expression value:", value, "For tokens:", line)

        return value

    def get_compare_expression_value(self, compare_expression : syn.Compare_Expression):
        a = self.get_expression_value(compare_expression.expression1)
        b = self.get_expression_value(compare_expression.expression2)
        if not a or not b:
            print("Could not get compare expression value")
            return None
        value = self.reserved_compare_operations[compare_expression.operator.value](a, b)
        print("Compare expression value: ", value)
        return value

    def find_unpassed_root(self, node : syn.Node):
        while node:
            if node.get_type() == syn.NODE_COMPARE and node.state == node.VISITED:
                return node
            node = node.get_root()
        return None

    def run(self):
        if self.tree is None:
            print("Tree is empty!")
            return None
        if self.tree.is_empty():
            print("Tree is empty!")
            return None
        node = self.tree.root
        while node is not None:
            if node.get_type() == syn.NODE_PRINT:
                print("print node")
                value = self.get_expression_value(node.get_expression())
                if not value:
                    print("Could not get expression value for print node")
                    return None
                print(value)
                if node.get_child():
                    node = node.get_child()
                else:
                    node = self.find_unpassed_root(node)

            elif node.get_type() == syn.NODE_ENTER:
                print("enter node")
                value = self.get_expression_value(node.get_expression())
                if not value:
                    print("Could not get expression value for enter node")
                    return None
                value = self.put_var(node.get_id(), value)
                if not value:
                    print("Could not place value to stack", value)
                    return None
                if node.get_child():
                    node = node.get_child()
                else:
                    node = self.find_unpassed_root(node)
            elif node.get_type() == syn.NODE_INPUT:
                print("INPUT NODE")
                print("Please enter romanian number")
                value = input()
                value = lex.get_number(value)
                print("Got value", value)
                self.put_var(node.get_id(), value)

                if node.get_child():
                    node = node.get_child()
                else:
                    node = self.find_unpassed_root(node)

            elif node.get_type() == syn.NODE_COMPARE:
                if node.state == syn.CompareNode.UNVISITED:
                    print("UNVISITED compare node")
                    value = self.get_compare_expression_value(node.get_expression())
                    if value is None:
                        print("Could not get compare expression value")
                        return None

                    if value:
                        node.state = node.VISITED
                        node = node.if_tree.root
                    elif node.else_tree:
                        node.state = node.VISITED
                        node = node.else_tree.root
                    elif node.get_child():
                        node.state = node.PASSED
                        node = node.get_child()
                    else:
                        node.state = node.PASSED
                        node = self.find_unpassed_root(node)
                elif node.state == syn.CompareNode.VISITED:
                    print("VISITED compare node")
                    if node.get_child():
                        node.state = syn.CompareNode.PASSED
                        node = node.get_child()
                    else:
                        node.state = syn.CompareNode.PASSED
                        node = self.find_unpassed_root(node)
                else:
                    print("PASSED compare node")
                    node = self.find_unpassed_root(node)

        print("Program finished")


