import sys
from syntax_analyzer import Tree_Builder
import AssemblerCompiler

builder = Tree_Builder("my_program.txt", verbose=0)
tree = builder.program()
print("\nPRINTING TREE\n")
print(tree.__str__())
print()
node = tree.get_root()
expr = node.get_expression()
assembler = AssemblerCompiler.Translator(tree, "my_program.asm", verbose=True)
assembler.translate()