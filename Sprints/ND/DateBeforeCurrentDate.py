# Nadeya De Diago 
# "I pledge my honor that I have abided by the Stevens Honor System."

from datetime import datetime, date
import unittest

def Date_Before_Current_Date(dateString):
    if dateString == 'NA':
        return True
    
    try:
        compareDate = datetime.strptime(dateString, '%d %b %Y').date()
    except ValueError:
        return False

    today = date.today()
    return compareDate < today

if __name__ == '__main__':
    unittest.main()
