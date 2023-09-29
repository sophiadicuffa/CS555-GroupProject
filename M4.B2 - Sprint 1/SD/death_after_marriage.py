from datetime import datetime

def check_marriage_before_death(people, families):
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')
        marriage_date = family.get('MARR', {}).get('DATE', '')

        if not husband_id or not wife_id or not marriage_date:
            continue

        husband_birth_date = next((person.get('DEATH', {}).get('DATE', '') for person in people if person.get('INDI', '') == husband_id), '')
        wife_birth_date = next((person.get('DEATH', {}).get('DATE', '') for person in people if person.get('INDI', '') == wife_id), '')

        if husband_birth_date and wife_birth_date and marriage_date:
            if datetime.strptime(husband_birth_date, "%d %b %Y") < datetime.strptime(marriage_date, "%d %b %Y") or datetime.strptime(wife_birth_date, "%d %b %Y") > datetime.strptime(marriage_date, "%d %b %Y"):
                return False
    return True
pass

check_marriage_before_death(people, families)