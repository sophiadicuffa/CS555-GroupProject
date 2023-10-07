# Nadeya De Diago 
# "I pledge my honor that I have abided by the Stevens Honor System."

from datetime import datetime, date
import unittest

def Date_Before_Current_Date(dateString):
    if dateString == 'NA':
        return True
    
    try:
        # Assuming the input date string is in 'YYYY-MM-DD' format
        compareDate = datetime.strptime(dateString, '%d %b %Y').date()
    except ValueError:
        # Handle invalid date formats here
        return False

    today = date.today()
    return compareDate < today

if __name__ == '__main__':
    unittest.main()
