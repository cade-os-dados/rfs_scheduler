# use the command bellow in the root of project
# python -m unittest discover tests

# built-in
import unittest
from datetime import datetime

# my libs
from pyagenda3 import timeops

def print_hello():
    print("Hello, world!")

class TestScheduler(unittest.TestCase):

    def test_weekday(self):     
        horario = timeops.next_weekday(1)
        self.assertTrue(horario.weekday() == 1,"Erro no dia da semana")
    
    def test_weekday_interval(self):
        new_scheduled = timeops.calculate_next_period(datetime(2022,1,1),'W')
        self.assertTrue(new_scheduled.weekday() == 5, "Erro no cálculo do dia da semana")
        self.assertTrue(new_scheduled.day == 8, "Erro no cálculo do dia")
    
    def test_month_interval(self):
        new_scheduled = timeops.calculate_next_period(datetime(2022,1,1),'M')
        self.assertTrue(new_scheduled == datetime(2022,2,1), "Erro no scheduling mensal")
    
    def test_daily_interval(self):
        new_scheduled = timeops.calculate_next_period(datetime(2022,1,1),'D')
        self.assertTrue(new_scheduled == datetime(2022,1,2), "Erro no scheduling diário")

if __name__ == '__main__':
    unittest.main()