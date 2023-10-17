import unittest
from datetime import datetime
from FamilyTables import birth_before_death_of_parents, check_male_last_names

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
