import unittest
from datetime import datetime 
from DateBeforeCurrentDate import Date_Before_Current_Date

class TestVerifyDateBeforeCurrentDate(unittest.TestCase):

    def test_date_before_current_date(self):
        # Test a date before the current date
        self.assertTrue(Date_Before_Current_Date('01 Jan 2022'))

    def test_date_same_as_current_date(self):
        # Test a date the same as the current date
        self.assertFalse(Date_Before_Current_Date('01 Oct 2023'))

    def test_date_after_current_date(self):
        # Test a date after the current date
        self.assertFalse(Date_Before_Current_Date('01 Nov 2023'))

    def test_invalid_date_format(self):
        # Test an invalid date format
        self.assertFalse(Date_Before_Current_Date('2022-01-01'))

    def test_na_string(self):
        # Test with 'NA' string, should return True
        self.assertTrue(Date_Before_Current_Date('NA'))

if __name__ == '__main__':
    unittest.main()