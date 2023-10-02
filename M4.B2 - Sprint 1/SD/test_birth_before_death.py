#Amanda Vu
import unittest
from datetime import datetime
from birthbeforedeath import is_birth_before_death  #\

class TestBirthBeforeDeath(unittest.TestCase):
    def test_birth_before_death_valid(self):
        individual = {"birth_date": "1990-01-01", "death_date": "2020-12-31"}
        result = is_birth_before_death(individual)
        self.assertTrue(result)

    def test_birth_equal_death(self):
        individual = {"birth_date": "2000-05-15", "death_date": "2000-05-15"}
        result = is_birth_before_death(individual)
        self.assertTrue(result)

    def test_birth_after_death(self):
        individual = {"birth_date": "1980-08-20", "death_date": "1975-04-10"}
        result = is_birth_before_death(individual)
        self.assertFalse(result)

    def test_missing_birth_date(self):
        individual = {"death_date": "1995-11-28"}
        result = is_birth_before_death(individual)
        self.assertFalse(result)

    def test_missing_death_date(self):
        individual = {"birth_date": "1988-02-15"}
        result = is_birth_before_death(individual)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
