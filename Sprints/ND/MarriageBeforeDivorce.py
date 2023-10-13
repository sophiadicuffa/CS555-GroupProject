from datetime import datetime

def MarriageBeforeDivorce(marriage_date, divorce_date):
    try:
        marriage_date = datetime.strptime(marriage_date, '%Y-%m-%d')
        divorce_date = datetime.strptime(divorce_date, '%Y-%m-%d')
        
        if marriage_date < divorce_date:
            return True
        else:
            return False
    except ValueError:
        # invalid date format
        return False

