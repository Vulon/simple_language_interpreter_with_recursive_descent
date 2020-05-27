import unittest as u
from syntax_analyzer import Tree_Builder
import AssemblerCompiler
from os import access, R_OK
from os.path import isfile

class TestTree(u.TestCase):
    def create_tree(self, path : str):
        builder = Tree_Builder(path, verbose=0)
        tree = builder.program()
        return tree

    def compare_programs(self, program_path : str, target_path : str):
        tree = self.create_tree(program_path)
        assembler = AssemblerCompiler.Translator(tree, "test_cases/temp.asm")
        assembler.translate()
        file1 = open("test_cases/temp.asm", "r")
        file2 = open(target_path, "r")
        lines1 = file1.readlines()
        lines2 = file2.readlines()
        file1.close()
        file2.close()
        self.assertListEqual(lines1, lines2)

    def setUp(self):
        print("Started testing")
        with open("test_cases/temp.asm", 'w'):
            pass
    def tearDown(self) -> None:
        print("Finished test")

    def test_sampleProgram(self):
        self.compare_programs("test_cases/sample.txt", "test_cases/sample.asm")
        print("Comparing", "test_cases/sample.txt", "test_cases/sample.asm")

    def test_conditionalProgram(self):
        self.compare_programs("test_cases/conditional.txt", "test_cases/conditional.asm")
        print("Comparing", "test_cases/conditional.txt", "test_cases/conditional.asm")

    def test_error(self):
        tree = self.create_tree("test_cases/error.txt")
        self.assertIsNone(tree)
        print("Trying to open ", "test_cases/error.txt")
    
    @u.skipIf(not isfile("none.txt") or not access("none.txt", R_OK), "Program none.txt not found")
    def test_NoneProgram(self):
        pass

if __name__ == "__main__":
    u.main()