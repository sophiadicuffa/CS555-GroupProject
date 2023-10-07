import unittest
from datetime import datetime

# Function to check if birth date is before death date
def is_birth_before_death(individual):
    birth_date = individual.get("birth_date")
    death_date = individual.get("death_date")
    
    if birth_date and death_date:
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        death_date = datetime.strptime(death_date, "%Y-%m-%d")
        
        if birth_date <= death_date:
            return True
        else:
            error_message = f"ERROR: INDIVIDUAL: US03: {individual.get('INDI', '')}: Died {death_date} before born {birth_date}"
            print(error_message)
            return False
    
    return False

