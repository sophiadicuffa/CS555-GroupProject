import unittest
from datetime import datetime
from FamilyTables import check_fewer_than_15_siblings, check_birth_before_parents_marriage

class TestFamilyFunctions(unittest.TestCase):
    def test_check_fewer_than_15_siblings(self):
        '''UnitTest for US15 - Fewer than 15 siblings '''
        families = [
            {
                'FAM': 'F01',
                'HUSB': 'I01',
                'WIFE': 'I02',
                'CHIL': ['I03', 'I04', 'I05', 'I06', 'I07', 'I08', 'I09', 'I10', 'I11', 'I12', 'I13', 'I14', 'I15', 'I16', 'I17', 'I18']
            }
        ]
        
        # Check if the correct error message is raised
        expected_errors = ["ERROR: FAMILY: US15: F01: More than 15 siblings in the family."]
        self.assertEqual(check_fewer_than_15_siblings([], families), expected_errors)

            
    def test_birth_before_parents_marriage(self):
        family_data = {
            'FAM': 'F1',
            'MARR': {'DATE': '01 Jan 2000'},
        }
        
        child_data = {
            'INDI': 'I1',
            'BIRTH': {'BDATE': '15 Dec 1995'},
        }

        families = [family_data]
        people = [child_data]

        expected_errors = "ERROR"
        self.assertEqual(check_birth_before_parents_marriage(people, families), expected_errors)

    def test_less_than_150(self):
        person = {
            'INDI': 'I01',
            'BIRTH': {'BDATE': '01 Jan 1950'},
            'DEATH': {'DATE': '01 Jan 2000'}
        }
        people = [person]

        import sys
        from io import StringIO
        captured_output = StringIO()
        sys.stdout = captured_output

        less_than_150(people)

        sys.stdout = sys.__stdout__

        expected_output = "" 
        self.assertEqual(captured_output.getvalue(), expected_output)

    def test_marriage_validity(self):
        family = {
            'FAM': 'F01',
            'HUSB': 'I01',
            'WIFE': 'I02',
            'MARR': {'DATE': '01 Jan 2000'}
        }
        people = [
            {'INDI': 'I01', 'BIRTH': {'BDATE': '01 Jan 1985'}},
            {'INDI': 'I02', 'BIRTH': {'BDATE': '01 Jan 1987'}}
        ]
        families = [family]

        import sys
        from io import StringIO
        captured_output = StringIO()
        sys.stdout = captured_output

        check_marriage_validity(people, families)

        sys.stdout = sys.__stdout__

        expected_output = ""  
        self.assertEqual(captured_output.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()
