import unittest
from unittest.mock import patch
from datetime import datetime, date
from io import StringIO

from FamilyTables import check_unique_name_and_birth, check_gender, calculate_age, check_siblings_not_married, check_unique_ids, list_siblings_by_age, find_children

class TestFamilyFunctions(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_gender_with_correct_data(self):
        people = [
            {"INDI": "@I1@", "SEX": "M"},
            {"INDI": "@I2@", "SEX": "F"},
        ]
        families = [
            {"FAM": "F1", "HUSB": "@I1@", "WIFE": "@I2@"},
        ]
        with patch('sys.stdout', new=StringIO()) as fake_out:
            check_gender(people, families)
            self.assertEqual(fake_out.getvalue().strip(), "")

    def test_gender_with_incorrect_data(self):
        people = [
            {"INDI": "@I1@", "SEX": "F"},  # Incorrect gender for husband
            {"INDI": "@I2@", "SEX": "M"},  # Incorrect gender for wife
        ]
        families = [
            {"FAM": "F1", "HUSB": "@I1@", "WIFE": "@I2@"},
        ]
        with patch('sys.stdout', new=StringIO()) as fake_out:
            check_gender(people, families)
            self.assertIn("Should be a male", fake_out.getvalue())
            self.assertIn("Should be a female", fake_out.getvalue())

    def test_age_with_valid_birthdate(self):
        self.assertEqual(calculate_age("6 OCT 1990", None), datetime.now().year - 1990)

    def test_age_with_invalid_birthdate(self):
        self.assertEqual(calculate_age("31 FEB 1990", None), "N/A")

    def test_birthdate_none(self):
        self.assertEqual(calculate_age(None, None), "N/A")

    def test_check_siblings_not_married(self):
        
        def test_check_siblings_not_married(self):
            individuals = [
                {"INDI": "I1", "NAME": "Alice Smith", "FAMC": "F1"},
                {"INDI": "I2", "NAME": "Bob Smith", "FAMC": "F1"},
                {"INDI": "I3", "NAME": "Charlie Brown", "FAMC": "F2"},
                {"INDI": "I4", "NAME": "Dana Brown", "FAMC": "F2"},
                {"INDI": "I5", "NAME": "Edward Stone", "FAMC": "F3"},
                {"INDI": "I6", "NAME": "Fiona Clear", "FAMC": "F4"}
            ]

            families = [
                {"FAM": "F5", "HUSB": "I1", "WIFE": "I2"},
                {"FAM": "F6", "HUSB": "I3", "WIFE": "I4"},
                {"FAM": "F7", "HUSB": "I5", "WIFE": "I6"}
            ]

            actual_errors = check_siblings_not_married(individuals, families)

            expected_errors = [
                "ERROR: FAMILY: US18: F5: Husband (I1) and Wife (I2) are siblings and therefore cannot be married."
            ]

            self.assertEqual(actual_errors, expected_errors)
    
    def test_unique_ids(self):
        
        individuals_unique = [{"INDI": "I1"}, {"INDI": "I2"}, {"INDI": "I3"}]
        families_unique = [{"FAM": "F1"}, {"FAM": "F2"}]
        self.assertTrue(check_unique_ids(individuals_unique, families_unique))

        individuals_duplicate_individual = [{"INDI": "I1"}, {"INDI": "I1"}, {"INDI": "I3"}]
        families_unique = [{"FAM": "F1"}, {"FAM": "F2"}]
        self.assertFalse(check_unique_ids(individuals_duplicate_individual, families_unique))

        individuals_unique = [{"INDI": "I1"}, {"INDI": "I2"}]
        families_duplicate_family = [{"FAM": "F1"}, {"FAM": "F1"}]
        self.assertFalse(check_unique_ids(individuals_unique, families_duplicate_family)) 
    
    def test_list_siblings_by_age(self):
        people = {} 
        families = [
            {'FAM': 'F1', 'children': [
                {'NAME': 'John', 'BIRTH': {'BDATE': '01 JAN 1990'}},
                {'NAME': 'Alice', 'BIRTH': {'BDATE': '01 JAN 1985'}}
            ]},
            {'FAM': 'F2', 'children': [
                {'NAME': 'Bob', 'BIRTH': {'BDATE': '01 JAN 1980'}},
                {'NAME': 'Eve', 'BIRTH': {'BDATE': '01 JAN 1995'}}
            ]}
        ]

        result = list_siblings_by_age(people, families)
        self.assertTrue(result)

    def test_unique_name_and_birth(self):
        people = [
            {'INDI': '1', 'NAME': 'John Doe', 'BIRTH': {'BDATE': '2000-01-01'}},
            {'INDI': '2', 'NAME': 'John Doe', 'BIRTH': {'BDATE': '2000-01-01'}}
        ]
        self.assertFalse(check_unique_name_and_birth(people))

if __name__ == '__main__':
    unittest.main()
