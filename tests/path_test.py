# use the command bellow in the root of project
# python -m unittest discover . -p "*_test.py"

import os, sys, unittest
sys.path.append(os.path.abspath('./src'))

from datetime import datetime

from pyprocess import projectPaths, pyProcess

class pathTest(unittest.TestCase):

    def test_path(self):
        
        current_dir = os.path.dirname(__file__)
        current_dir = os.path.join(current_dir, 'integration')
        teste = projectPaths(
            project_path = current_dir, 
            script_name='data/hello.txt'
        )
        with open(teste.script_path) as arquivo:
            hello = arquivo.read()
        self.assertEqual(hello,'ola mundo')

    def test_args_api(self):
        teste = projectPaths(
            project_path = 'hello',
            script_name = 'world.py',
            args = '--br  --translate'
        )
        processo = pyProcess(process_name='ola', scheduled_time=datetime.now(), paths = teste)
        self.assertEqual(
            processo.processes_args, 
            ['hello/venv/Scripts/python.exe', 'hello/world.py', '--br', '--translate'], 
            "A api que unifica os argumentos do path do python, script e argumentos adicionais não está funcionando corretamente"
        )

        # mudando a estrutura de dados para verificar se continuará funcionando
        teste.args = ['--br', ' --translate']
        processo = pyProcess(process_name='ola', scheduled_time=datetime.now(), paths = teste)
        self.assertEqual(
            processo.processes_args, 
            ['hello/venv/Scripts/python.exe', 'hello/world.py', '--br', '--translate'], 
            "A api que unifica os argumentos do path do python, script e argumentos adicionais não está funcionando corretamente"
        )

        teste.args = None
        processo = pyProcess(process_name='ola', scheduled_time=datetime.now(), paths = teste)
        self.assertEqual(
            processo.processes_args, 
            ['hello/venv/Scripts/python.exe', 'hello/world.py'], 
            "A api que unifica os argumentos do path do python, script e argumentos adicionais não está funcionando corretamente"
        )
    
if __name__ == "__main__":
    unittest.main()
