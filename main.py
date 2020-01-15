import sys
from syntax_analyzer import Tree_Builder
import tree_executor

if(len(sys.argv) != 2):
    print('You must enter filename')
    builder = Tree_Builder("sample program.txt", verbose=1)
    tree = builder.program()
    executor = tree_executor.Tree_Executor(tree)
    print("STARTING TREE EXECUTOR __________________________________")
    executor.run()
else:
    builder = Tree_Builder(sys.argv[1])
    tree = builder.program()
    executor = tree_executor.Tree_Executor(tree)
    print("STARTING TREE EXECUTOR __________________________________")
    executor.run()
