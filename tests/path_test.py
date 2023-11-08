import os, sys, unittest
sys.path.append(os.path.abspath('./src'))

class pathTest(unittest.TestCase):

    def path_test(self):
        from pyprocess import projectPaths
        current_dir = os.path.dirname(__file__)
        current_dir = os.path.join(current_dir, 'integration')
        teste = projectPaths(project_path = current_dir, script_name='data/hello.txt')
        with open(teste.script_path) as arquivo:
            hello = arquivo.read()
        self.assertEqual(hello,'ola mundo')

if __name__ == "__main__":
    unittest.main()