import unittest
from unittest.mock import patch
from datetime import datetime, date
from io import StringIO

# Import the check_gender function from your FamilyTables module
from FamilyTables import validate_date_format, living_single, print_upcoming_birthdays, parse_date, print_deceased_from_gedcom

class TestFamilyFunctions(unittest.TestCase):
    #testing validate_date_format
    def test_validate_date_correct_format(self):
        self.assertTrue(validate_date_format("12 MAR 1990", "Test Identifier"))

    def test_validate_date_incorrect_format(self):
        self.assertFalse(validate_date_format("MAR 12 1990", "Test Identifier"))

    @patch('sys.stdout', new_callable=StringIO)
    def test_validate_date_error_message(self, mock_stdout):
        validate_date_format("MAR 12 1990", "Test Identifier")
        self.assertIn("ERROR: US42: The date MAR 12 1990 for Test Identifier is in the wrong format.", mock_stdout.getvalue())
    
    #testing living_single
    def test_single_and_over_30(self):
        people = [
            {"INDI": "@I1@", "BIRTH": {"BDATE": "1 JAN 1980"}, "DEATH": {}},
            {"INDI": "@I2@", "BIRTH": {"BDATE": "1 JAN 1970"}, "FAMS": []},
        ]
        result = living_single(people)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(person["INDI"] in ["@I1@", "@I2@"] for person in result))

    def test_single_but_under_30(self):
        people = [
            {"INDI": "@I1@", "BIRTH": {"BDATE": "1 JAN 1995"}, "DEATH": {}},
        ]
        result = living_single(people)
        self.assertEqual(len(result), 0)

    def test_married_individuals(self):
        people = [
            {"INDI": "@I1@", "BIRTH": {"BDATE": "1 JAN 1980"}, "FAMS": ["@F1@"], "DEATH": {}},
        ]
        result = living_single(people)
        self.assertEqual(len(result), 0)

  

if __name__ == '__main__':
    unittest.main()