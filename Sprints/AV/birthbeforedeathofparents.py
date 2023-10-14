import unittest
from datetime import datetime

def check_birth_before_death_of_parents(people, families):
    for family in families:
        children = family.get("CHIL", [])
        husband_id = family.get("HUSB", "")
        wife_id = family.get("WIFE", "")
        
        for child_id in children:
            child = next((person for person in people if person.get('INDI', '') == child_id), None)
            mother = next((person for person in people if person.get('INDI', '') == wife_id), None)
            father = next((person for person in people if person.get('INDI', '') == husband_id), None)

            if child and mother and father:
                child_birth_date = child.get("BIRT", {}).get("DATE", "")
                mother_death_date = mother.get("DEAT", {}).get("DATE", "")
                father_death_date = father.get("DEAT", {}).get("DATE", "")

                if child_birth_date and mother_death_date:
                    child_birth_date_format = datetime.strptime(child_birth_date, "%d %b %Y")
                    mother_death_date_format = datetime.strptime(mother_death_date, "%d %b %Y")

                    if child_birth_date_format > mother_death_date_format:
                        error_message = f"ERROR: INDIVIDUAL: US09: {child_id}: Child born {child_birth_date_format.strftime('%d %b %Y')} after mother's death {mother_death_date_format.strftime('%d %b %Y')}"
                        print(error_message)

                if child_birth_date and father_death_date:
                    child_birth_date_format = datetime.strptime(child_birth_date, "%d %b %Y")
                    father_death_date_format = datetime.strptime(father_death_date, "%d %b %Y")

                    if child_birth_date_format > father_death_date_format:
                        error_message = f"ERROR: INDIVIDUAL: US09: {child_id}: Child born {child_birth_date_format.strftime('%d %b %Y')} after father's death {father_death_date_format.strftime('%d %b %Y')}"
                        print(error_message)

