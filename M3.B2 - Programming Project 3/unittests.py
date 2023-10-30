import unittest
from datetime import datetime
from FamilyTables import check_fewer_than_15_siblings, check_birth_before_parents_marriage, birth_before_death_of_parents, check_male_last_names, less_than_150, check_marriage_validity, check_sibling_married_to_child

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

        # Test case for a parent's sibling being married to their child
    def test_sibling_married_to_child(self):
        fake_family = {
            "FAM": "F101",
            "HUSB": "I50",  # Father
            "WIFE": "I51",  # Mother
            "MARR": {"DATE": "01 JAN 1990"},  # Marriage date of parents
            "CHIL": ["I52"],  # Child
        }

        fake_aunt = {
            "INDI": "I52",
            "NAME": "Aunt Name",
            "SEX": "F",  # Female
            "FAMC": "F102",  # Parent's family ID
        }

        people = [fake_aunt]
        families = [fake_family]

        # Assert that the function detects the error
        self.assertFalse(check_sibling_married_to_child(people, families))

    class TestBirthBeforeDeathOfParents(unittest.TestCase):
        def test_birth_before_death_pass(self):
            # Test case for children born before parents' deaths (pass scenario)
            people = [
                {
                    'INDI': 'I1',
                    'BIRT': {'DATE': '10 MAR 1980'},
                    'DEAT': {'DATE': '15 MAY 2018'}
                },
                {
                    'INDI': 'I2',
                    'BIRT': {'DATE': '10 MAR 1990'},
                    'DEAT': {'DATE': '15 MAY 2010'}
                },
                {
                    'INDI': 'I3',
                    'BIRT': {'DATE': '10 MAR 2005'},
                    'DEAT': {}  
                }
            ]
            families = [
                {
                    'HUSB': 'I1',
                    'WIFE': 'I2',
                    'CHIL': ['I3']
                }
            ]
            result = birth_before_death_of_parents(people, families)
            self.assertFalse(result)


    def test_three_children_pass(self):
        # Test case for three different children 
        people = [
            {
                'INDI': 'F1',
                'BIRT': {'DATE': '10 MAR 1980'},
                'DEAT': {'DATE': '15 MAY 2000'}
            },
            {
                'INDI': 'F2',
                'BIRT': {'DATE': '10 MAR 1990'},
                'DEAT': {'DATE': '15 MAY 2010'}
            },
            {
                'INDI': 'F3',
                'BIRT': {'DATE': '10 MAR 1995'},
                'DEAT': {'DATE': '15 MAY 2005'}
            },
            {
                'INDI': 'F4',
                'BIRT': {'DATE': '13 MAR 2009'},
                'DEAT': {'DATE': '15 MAY 2010'}
            },
            {
                'INDI': 'F5',
                'BIRT': {'DATE': '3 Jan 2005'},
                'DEAT': {'DATE': '15 MAY 2015'}
            }
        ]
        families = [
            {
                'HUSB': 'F1',
                'WIFE': 'F2',
                'CHIL': ['F3', 'F4', 'F5']
            }
        ]
        result = birth_before_death_of_parents(people, families)
        self.assertFalse(result)

        def test_same_last_name(self):
        # Test case for male children having the same last name as the husband (pass scenario)
            people = [
            {
                'INDI': 'H1',
                'NAME': 'John /Smith/',
                'SEX': 'M'
            },
            {
                'INDI': 'W1',
                'NAME': 'Alice /Smith/',
                'SEX': 'F'
            },
            {
                'INDI': 'C1',
                'NAME': 'Tom /Smith/',
                'SEX': 'M'
            },
            {
                'INDI': 'C2',
                'NAME': 'Ben /Smith/',
                'SEX': 'M'
            }
        ]
        families = [
            {
                'FAM': 'F1',
                'HUSB': 'H1',
                'WIFE': 'W1',
                'CHIL': ['C1', 'C2']
            }
        ]
        result = check_male_last_names(people, families)
        self.assertTrue(result)

    def test_different_last_name(self):
        # Test case for male child having a different last name from the husband (fail scenario)
        people = [
            {
                'INDI': 'H2',
                'NAME': 'James /Smith/',
                'SEX': 'M'
            },
            {
                'INDI': 'W2',
                'NAME': 'Emily /Jones/',
                'SEX': 'F'
            },
            {
                'INDI': 'C3',
                'NAME': 'Sam /Brown/',
                'SEX': 'M'
            }
        ]
        families = [
            {
                'FAM': 'F2',
                'HUSB': 'H2',
                'WIFE': 'W2',
                'CHIL': ['C3']
            }
        ]
        result = check_male_last_names(people, families)
        self.assertTrue(result) 


if __name__ == '__main__':
    unittest.main()
