
from datetime import datetime, date

def find_children(people, family_id):
    return [person for person in people if person.get('FAMC') == family_id]

def check_male_last_names(people, families):
    for family in families:
        husband_id = family.get('HUSB', '')
        children = find_children(people, family.get('FAM', ''))

        # Skip processing if husband or children are not present
        if not husband_id or not children:
            continue

        # Get the last name of the husband
        husband_last_name = next(
            (person.get('NAME', '').split('/')[1] for person in people if person.get('INDI', '') == husband_id), '')

        if not husband_last_name:
            continue

        # Check the last names of male children in the family
        for child in children:
            child_id = child.get('INDI', '')
            sex = child.get('SEX', '')

            if sex == 'M':
                child_last_name = next(
                    (person.get('NAME', '').split('/')[1] for person in people if person.get('INDI', '') == child_id), '')

                if child_last_name != husband_last_name:
                    error_message = f"ERROR: FAMILY: US16: {family.get('FAM', '')}: Male child ({child_id}) has a different last name ({child_last_name}) than the husband ({husband_id}) ({husband_last_name})."
                    print(error_message)
                    return False

    return True
