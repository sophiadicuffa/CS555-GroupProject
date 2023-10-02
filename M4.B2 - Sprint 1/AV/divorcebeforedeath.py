import unittest
from datetime import datetime

def is_divorce_before_death(individual):
    death_date = individual.get("death_date")
    divorce_date = individual.get("divorce_date")
    indi_id = individual.get("INDI", "")

    if death_date and divorce_date:
        death_date = datetime.strptime(death_date, "%Y-%m-%d")
        divorce_date = datetime.strptime(divorce_date, "%Y-%m-%d")

        if divorce_date < death_date:
            return True
        else:
            error_message = f"ERROR: INDIVIDUAL: US06: {indi_id}: Divorced {divorce_date} after death on {death_date}"
            print(error_message)
            return False

    return True  # If no divorce date or no death date, consider it valid
