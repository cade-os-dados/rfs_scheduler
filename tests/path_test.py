import os, sys, unittest
sys.path.append(os.path.abspath('./src'))

from pyprocess import projectPaths

class pathTest(unittest.TestCase):

    def path_test(self):
        
        current_dir = os.path.dirname(__file__)
        current_dir = os.path.join(current_dir, 'integration')
        teste = projectPaths(
            project_path = current_dir, 
            script_name='data/hello.txt'
        )
        with open(teste.script_path) as arquivo:
            hello = arquivo.read()
        self.assertEqual(hello,'ola mundo')

if __name__ == "__main__":
    unittest.main()