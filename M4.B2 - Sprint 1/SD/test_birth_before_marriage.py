import unittest
from birth_before_marriage import check_birth_before_marriage

class TestBirthBeforeMarriage(unittest.TestCase):
    def test_birth_before_marriage_pass(self):
        people = [
            {"INDI": "I1", "BIRTH": {"BDATE": "01 JAN 1990"}},
            {"INDI": "I2", "BIRTH": {"BDATE": "15 FEB 1992"}}
        ]
        families = [
            {"FAM": "F1", "HUSB": "I1", "WIFE": "I2", "MARR": {"DATE": "01 JAN 2010"}}
        ]
        result = check_birth_before_marriage(people, families)
        self.assertTrue(result)

    def test_birth_before_marriage_fail(self):
        people = [
            {"INDI": "I1", "BIRTH": {"BDATE": "01 JAN 1995"}},
            {"INDI": "I2", "BIRTH": {"BDATE": "15 FEB 1990"}}
        ]
        families = [
            {"FAM": "F1", "HUSB": "I1", "WIFE": "I2", "MARR": {"DATE": "01 JAN 1920"}}
        ]
        result = check_birth_before_marriage(people, families)
        self.assertFalse(result)

    def test_missing_birth_dates(self):
        people = [
            {"INDI": "I1", "BIRTH": {"BDATE": "01 JAN 1990"}},
            {"INDI": "I2"}
        ]
        families = [
            {"FAM": "F1", "HUSB": "I1", "WIFE": "I2", "MARR": {"DATE": "01 JAN 2010"}}
        ]
        result = check_birth_before_marriage(people, families)
        self.assertTrue(result)

    def test_missing_marriage_date(self):
        people = [
            {"INDI": "I1", "BIRTH": {"BDATE": "01 JAN 1990"}},
            {"INDI": "I2", "BIRTH": {"BDATE": "15 FEB 1992"}}
        ]
        families = [
            {"FAM": "F1", "HUSB": "I1", "WIFE": "I2"}
        ]
        result = check_birth_before_marriage(people, families)
        self.assertTrue(result)
        
    def test_empty_data(self):
        people = []
        families = []
        result = check_birth_before_marriage(people, families)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
