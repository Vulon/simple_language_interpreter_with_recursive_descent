import sys
from syntax_analyzer import Tree_Builder
import tree_executor
import AssemblerCompiler

builder = Tree_Builder("arith expr.txt", verbose=0)
tree = builder.program()
print("\nPRINTING TREE\n")
print(tree.__str__())
print()
node = tree.get_root()
expr = node.get_expression()
assembler = AssemblerCompiler.Translator(tree, "output.asm", verbose=True)
assembler.translate()