#Amanda Vu

import unittest
from datetime import datetime
from divorcebeforedeath import is_divorce_before_death  

class TestDivorceBeforeDeath(unittest.TestCase):
    def test_divorce_before_death_valid(self):
        individual = {"divorce_date": "2000-01-01", "death_date": "2020-12-31"}
        result = is_divorce_before_death(individual)
        self.assertTrue(result)

    def test_divorce_equal_death(self):
        individual = {"divorce_date": "1990-05-15", "death_date": "1990-05-15"}
        result = is_divorce_before_death(individual)
        self.assertFalse(result)

    def test_divorce_after_death(self):
        individual = {"divorce_date": "1985-08-15", "death_date": "1980-04-10"}
        result = is_divorce_before_death(individual)
        self.assertFalse(result)

    def test_missing_divorce_date(self):
        individual = {"death_date": "1995-11-28"}
        result = is_divorce_before_death(individual)
        self.assertTrue(result)

    def test_missing_death_date(self):
        individual = {"divorce_date": "1988-02-15"}
        result = is_divorce_before_death(individual)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
