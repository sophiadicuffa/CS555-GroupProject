import datetime

def check_birth_before_marriage(people, families):
    print("{:<15} {:<15} {:<20} {:<20}".format("Husband Birth", "Wife Birth", "Marriage Date", "Result"))
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')
        marriage_date = family.get('MARR', {}).get('DATE', '')

        if not husband_id or not wife_id:
            continue
        
        husband_birth = "N/A"
        wife_birth = "N/A"
        result = "Pass"

        if husband_id:
            husband_birth_date = next((person.get('BIRTH', {}).get('DATE', '') for person in people if person.get('INDI', '') == husband_id), '')
            if husband_birth_date:
                husband_birth = datetime.strptime(husband_birth_date, "%d %b %Y").strftime("%d %b %Y")

        if wife_id:
            wife_birth_date = next((person.get('BIRTH', {}).get('DATE', '') for person in people if person.get('INDI', '') == wife_id), '')
            if wife_birth_date:
                wife_birth = datetime.strptime(wife_birth_date, "%d %b %Y").strftime("%d %b %Y")

        if marriage_date and husband_birth_date and wife_birth_date:
            if datetime.strptime(husband_birth_date, "%d %b %Y") > datetime.strptime(marriage_date, "%d %b %Y") or datetime.strptime(wife_birth_date, "%d %b %Y") > datetime.strptime(marriage_date, "%d %b %Y"):
                result = "Fail"

        print("{:<15} {:<15} {:<20} {:<20}".format(husband_birth, wife_birth, marriage_date, result))

check_birth_before_marriage(people, families)