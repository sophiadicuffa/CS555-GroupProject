import unittest
from checkmalelastnames import check_male_last_names

class TestCheckMaleLastNames(unittest.TestCase):
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
