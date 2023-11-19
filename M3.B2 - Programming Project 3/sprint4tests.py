import unittest
from unittest.mock import patch
from datetime import datetime, date
from io import StringIO

# Import the check_gender function from your FamilyTables module
from FamilyTables import get_living_couples, validate_date_format, living_single, print_upcoming_birthdays, parse_date, print_deceased_from_gedcom

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

    def test_get_living_couples(self):
        people = [
            {'INDI': 'I1', 'NAME': 'John Doe', 'SEX': 'M', 'BIRTH': {'BDATE': '01 JAN 1980'}},
            {'INDI': 'I2', 'NAME': 'Jane Doe', 'SEX': 'F', 'BIRTH': {'BDATE': '15 FEB 1985'}},
        ]
        families = [
            {'FAM': 'F1', 'HUSB': 'I1', 'WIFE': 'I2', 'MARR': {'DATE': '01 JAN 2000'}},
        ]

        # Test for living couples
        couples = get_living_couples(people, families)
        self.assertEqual(len(couples), 1)
        self.assertEqual(couples[0]['Husband'], 'John Doe')
        self.assertEqual(couples[0]['Wife'], 'Jane Doe')
        self.assertEqual(couples[0]['MarriageDate'].strftime("%d %b %Y"), '01 Jan 2000')

  

if __name__ == '__main__':
    unittest.main()