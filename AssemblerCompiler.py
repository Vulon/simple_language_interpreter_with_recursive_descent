from syntax_analyzer import *
import lexical_analyzer as lex

class Translator:
    def __init__(self, tree : Tree, output_path : str, verbose=False):
        self.tree = tree
        self.file = open(output_path, 'w')
        self.verbose = verbose
        self.variables = set()
        self.label_index = 0


    def finish(self):
        self.file.writelines([
            "\tret\n",
            "\n",
            "message:\n",
            "\tdb  '%d', 10, 0\n"
        ])

    def parse_expression(self, expression : Arith_Expression, tabulation : int):
        tokens = expression.tokens
        out = []
        stack = []
        v = self.verbose
        text = ""
        tabs = "".join(["\t" for i in range(tabulation)])
        if v:
            print("Tabs:", tabs, "len", len(tabs))

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
        if v:
            print("POLISH NOTATION:", line)

        for token in out:
            if token.token == lex.CONST:
                text += tabs + "push dword " + str(token.value) + "\n"
            elif token.token == lex.ID:
                text += tabs + "push dword [" + token.value + "]\n"

            elif token.token == lex.PLUS:
                text += tabs + "pop ebx " + "\n"
                text += tabs + "pop eax " + "\n"
                text += tabs + "add eax, ebx" + "\n"
                text += tabs + "push eax" + "\n"
            elif token.token == lex.MINUS:
                text += tabs + "pop ebx " + "\n"
                text += tabs + "pop eax " + "\n"
                text += tabs + "sub eax, ebx" + "\n"
                text += tabs + "push eax" + "\n"
            elif token.token == lex.TIMES:
                text += tabs + "pop ebx " + "\n"
                text += tabs + "pop eax " + "\n"
                text += tabs + "imul eax, ebx" + "\n"
                text += tabs + "push eax" + "\n"
            elif token.token == lex.DIVIDE:
                text += tabs + "pop ebx " + "\n"
                text += tabs + "pop eax " + "\n"
                text += tabs + "mov EDX, 0 " + "\n"
                text += tabs + "mov DX, 0 " + "\n"
                self.add_variable("temp")
                text += tabs + "mov [temp], ebx " + "\n"
                text += tabs + "div dword [temp]" + "\n"

                text += tabs + "push eax" + "\n"
        text += tabs + ";expression: " + line + "\n"

        return text

    def parse_enter_node(self, node : EnterNode, tabulation : int):
        text = self.parse_expression(node.get_expression(), tabulation)
        tabs = "".join(["\t" for i in range(tabulation)])
        text += tabs + "pop eax" + "\n"
        self.add_variable(node.get_id().value)
        text += tabs + "mov dword [" + node.get_id().value + "], eax" + "\n"
        text += tabs + "; enter expr to " + node.get_id().value + "\n"

        return text

    def parse_print_node(self, node : PrintNode, tabulation : int):
        text = self.parse_expression(node.get_expression(), tabulation)
        tabs = "".join(["\t" for i in range(tabulation)])
        text += tabs + "push message" + "\n"
        text += tabs + "call _printf" + "\n"
        text += tabs + "pop ebx" + "\n"
        text += tabs + "pop ebx" + "\n"
        text += tabs + "; print expr " + "\n"
        return text

    def add_variable(self, name):
        self.variables.add(name)

    def get_label(self):
        self.label_index += 1
        return "l" + str(self.label_index)

    def add_bss_section(self):
        self.file.write("section .bss\n")
        for name in self.variables:
            self.file.write("\t" + name + ": resd 1\n")
        self.file.write("\n")

    def parse_nodes(self, node, tabs : int):
        text = ""
        while not(node is None):
            if node.get_type() == NODE_ENTER:
                text += self.parse_enter_node(node, tabs)
            elif node.get_type() == NODE_PRINT:
                text += self.parse_print_node(node, tabs)
            elif node.get_type() == NODE_COMPARE:
                text += self.parse_CompareNode(node, tabs)
            node = node.get_child()
        return text

    def parse_CompareNode(self, node : CompareNode, tabulation : int):
        text = ""
        tabs = "".join(["\t" for i in range(tabulation)])

        comp_expr = node.get_expression()
        text += self.parse_expression(comp_expr.expression1, tabulation)
        text += self.parse_expression(comp_expr.expression2, tabulation)

        text += tabs + "pop ebx" + "\n"
        text += tabs + "pop eax" + "\n"
        text += tabs + "cmp eax, ebx" + "\n"
        else_label = self.get_label()
        exit_label = self.get_label()
        if comp_expr.operator.token == lex.GREATER:
            text += tabs + "jle " + else_label + "\n"
        elif comp_expr.operator.token == lex.LESSER:
            text += tabs + "jge " + else_label + "\n"
        elif comp_expr.operator.token == lex.EQUAL:
            text += tabs + "jne " + else_label + "\n"
        elif comp_expr.operator.token == lex.GREATER_EQ:
            text += tabs + "jl " + else_label + "\n"
        elif comp_expr.operator.token == lex.LESSER_EQ:
            text += tabs + "jg " + else_label + "\n"
        text += self.parse_nodes(node.if_tree.get_root(), tabulation + 1)

        if not(node.else_tree is None):
            text += tabs + "JMP " + exit_label + "\n"
            text += tabs + else_label + ":\n"
            text += self.parse_nodes(node.else_tree.get_root(), tabulation + 1)
            text += tabs + exit_label + ":\n"
        else:
            text += tabs + else_label + ":\n"


        return text



    def translate(self):
        node = self.tree.get_root()
        tabs = 1

        text = self.parse_nodes(node, tabs)

        self.add_bss_section()
        self.file.writelines([
            "\nsection .text\n",
            "\tglobal  _main\n",
            "\textern  _printf\n",
            "\n"
            "_main:\n"
        ])

        self.file.write(text)
        self.finish()
