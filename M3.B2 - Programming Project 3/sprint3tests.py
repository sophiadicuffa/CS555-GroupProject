import unittest
from unittest.mock import patch
from datetime import datetime, date
from io import StringIO

# Import the check_gender function from your FamilyTables module
from FamilyTables import check_gender, calculate_age, check_siblings_not_married, check_unique_ids

class TestFamilyFunctions(unittest.TestCase):
    
    def setUp(self):
        # Common setup for all tests if necessary
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

if __name__ == '__main__':
    unittest.main()
