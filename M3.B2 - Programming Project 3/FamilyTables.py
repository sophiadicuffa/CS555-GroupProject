# Sophia DiCuffa, Nadeya De Diago, Amanda Vu
# CS555 M3.B2

from datetime import datetime, date, timedelta

people = []
families = []
current_person = {}
current_family = {}


def calculate_age(birthdate, deathdate):
    if not birthdate:
        return "N/A"
    try:
        birthdate = datetime.strptime(birthdate, "%d %b %Y")
    except ValueError:
        return "N/A"  # Invalid date format

    today = date.today()
    age = today.year - birthdate.year - \
        ((today.month, today.day) < (birthdate.month, birthdate.day))

    if deathdate:
        try:
            deathdate = datetime.strptime(deathdate, "%d %b %Y")
        except ValueError:
            return f"{age} (Died: Invalid date format)"
        age_at_death = deathdate.year - birthdate.year - \
            ((deathdate.month, deathdate.day) < (birthdate.month, birthdate.day))
        return f"{age} (Died at {age_at_death})"
    return age


def process_line(line):
    global current_person
    global current_family
    line = line.strip()
    parts = line.split()
    level = int(parts[0])
    tag = parts[1]

    if len(parts) > 2:
        special_tag = parts[2]
    else:
        special_tag = ''

    if level == 0:
        if special_tag == 'INDI':
            if current_person:
                people.append(current_person)
            current_person = {"INDI": tag}
        elif special_tag == 'FAM':
            if current_family:
                families.append(current_family)
            current_family = {"FAM": tag}
    elif level == 1:
        if tag == 'NAME':
            current_person['NAME'] = ' '.join(parts[2:])
        elif tag == 'SEX':
            current_person['SEX'] = parts[2]
        elif tag == 'BIRT':
            current_person['BIRTH'] = {}
        elif tag == 'FAMS':
            current_person.setdefault('FAMS', []).append(parts[2])
        elif tag == 'FAMC':
            current_person['FAMC'] = parts[2]
        elif tag == 'DEAT':
            current_person['DEATH'] = {}
        elif tag == 'HUSB':
            current_family['HUSB'] = parts[2]
        elif tag == 'WIFE':
            current_family['WIFE'] = parts[2]
        elif tag == 'MARR':
            current_family['MARR'] = {}
        elif tag == 'DIV':
            current_family['DIV'] = {}
        elif tag == 'CHIL':
            current_family['CHIL'] = parts[2]
    elif level == 2:
        if 'DEATH' in current_person:
            if tag == 'DATE':
                current_person['DEATH']['DATE'] = ' '.join(parts[2:])
        elif 'BIRTH' in current_person:
            if tag == 'DATE':
                current_person['BIRTH']['BDATE'] = ' '.join(parts[2:])
        if 'DIV' in current_family and tag == 'DATE':
            current_family['DIV']['DATE'] = ' '.join(parts[2:])
        elif 'MARR' in current_family and tag == 'DATE':
            current_family['MARR']['DATE'] = ' '.join(parts[2:])


with open('test.ged', 'r') as gedcom_file:
    for line in gedcom_file:
        process_line(line)

if current_person:
    people.append(current_person)
if current_family:
    families.append(current_family)

people = sorted(people, key=lambda k: k['INDI'])
families = sorted(families, key=lambda k: k['FAM'])

# Function to find children for a family


def find_children(family_id):
    return [person for person in people if person.get('FAMC') == family_id]

# Function to find parents for a family


def find_parents(family_id):
    return [person for person in people if family_id in person.get('FAMS', [])]


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y").date()
    except ValueError:
        return None


print("{:<10} {:<30} {:<10} {:<15} {:<20} {:<10} {:<20}".format(
    "ID", "Name", "Sex", "Birthday", "Age", "Spouse", "Parent"))
for person in people:
    indi_id = person.get('INDI', '')
    name = person.get('NAME', '')
    sex = person.get('SEX', '')
    birthday = person.get('BIRTH', {}).get('BDATE', '')
    death_date = person.get('DEATH', {}).get('DATE', '')
    age = calculate_age(birthday, death_date)

    # Find the family tag they belong to (as husband or wife)
    spouse_tag = 'N/A'
    parent_tag = 'N/A'

    if 'FAMC' in person:
        family_id = person['FAMC']
        parents = find_parents(family_id)
        parent_names = [parent.get('NAME', '') for parent in parents]
        parent_tag = family_id

    for family in families:
        fam_id = family.get('FAM', '')

        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')
        if indi_id == husband_id or indi_id == wife_id:
            spouse_tag = family.get('FAM', '')
            break

    print("{:<10} {:<30} {:<10} {:<15} {:<20} {:<10} {:<20}".format(
        indi_id, name, sex, birthday, age, spouse_tag, parent_tag))

print("\nFamilies:")
print("{:<10} {:<15} {:<15} {:<20} {:<20} {:<15} {:<35} {:<40}".format(
    "ID", "Married Date", "Divorced Date", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"))

for family in families:
    fam_id = family.get('FAM', '')
    marriage_date = family.get('MARR', {}).get('DATE', '')
    divorced_date = family.get('DIV', {}).get('DATE', '')
    if not divorced_date:
        divorced_date = "N/A"
    husband_id = family.get('HUSB', '')
    husband_name = next((person.get('NAME', '')
                        for person in people if person.get('INDI', '') == husband_id), '')
    wife_id = family.get('WIFE', '')
    wife_name = next((person.get('NAME', '')
                     for person in people if person.get('INDI', '') == wife_id), '')
    children = find_children(fam_id)

    # Skip printing if the family has only one child or none
    if (not husband_id and not wife_id) or not children:
        continue

    children_names = ', '.join([child.get('INDI', '') for child in children])

    print("{:<10} {:<15} {:<15} {:<20} {:<20} {:<15} {:<35} {:<40}".format(
        fam_id, marriage_date, divorced_date, husband_id, husband_name, wife_id, wife_name, children_names))

print()
print()

# SPRINT 1 - SD - Birth before Marriage


def get_birth_date(person_id, people):
    birth_date = next((person.get('BIRTH', {}).get('BDATE', '')
                      for person in people if person.get('INDI', '') == person_id), '')
    return datetime.strptime(birth_date, "%d %b %Y") if birth_date else None


def get_death_date(person_id, people):
    death_date = next((person.get('DEATH', {}).get('DATE', '')
                      for person in people if person.get('INDI', '') == person_id), '')
    return datetime.strptime(death_date, "%d %b %Y") if death_date else None


def check_birth_before_marriage(people, families):
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')
        marriage_date = family.get('MARR', {}).get('DATE', '')

        if not husband_id or not wife_id or not marriage_date:
            continue

        husband_birth_date = get_birth_date(husband_id, people)
        wife_birth_date = get_birth_date(wife_id, people)

        marriage_date_format = datetime.strptime(marriage_date, "%d %b %Y")

        if husband_birth_date and wife_birth_date and marriage_date:
            if husband_birth_date > marriage_date_format:
                error_message = f"ERROR: FAMILY: US02: {family.get('FAM', '')}: Husband's birthday of {
                    husband_birth_date} is after marriage date of {marriage_date_format}."
                print(error_message)
                return False
            elif wife_birth_date > marriage_date_format:
                error_message = f"ERROR: FAMILY: US02: {family.get('FAM', '')}: Wife's birthday of {
                    wife_birth_date} is after marriage date of {marriage_date_format}."
                print(error_message)
                return False
    return True


def check_marriage_before_death(people, families):
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')
        marriage_date = family.get('MARR', {}).get('DATE', '')

        if not husband_id or not wife_id or not marriage_date:
            continue

        husband_death_date = get_death_date(husband_id, people)
        wife_death_date = get_death_date(wife_id, people)

        marriage_date_format = datetime.strptime(marriage_date, "%d %b %Y")

        if husband_death_date and husband_death_date < marriage_date_format:
            error_message = f"ERROR: FAMILY: US05: {family.get('FAM', '')}: Husband's death of {
                husband_death_date} is before marriage date of {marriage_date_format}"
            print(error_message)
            return False

        if wife_death_date and wife_death_date < marriage_date_format:
            error_message = f"ERROR: FAMILY: US05: {family.get('FAM', '')}: Wife's death of {
                wife_death_date} is before marriage date of {marriage_date_format}"
            print(error_message)
            return False
    return True


check_birth_before_marriage(people, families)
check_marriage_before_death(people, families)

# Create a set to keep track of individuals for whom we've already checked the birth before death condition
checked_birth_before_death = set()


def is_birth_before_death(individual):
    indi_id = individual.get("INDI", "")

    # Check if we have already checked this individual
    if indi_id in checked_birth_before_death:
        return True

    birth_date = individual.get("BIRTH", {}).get("BDATE", "")
    death_date = individual.get("DEATH", {}).get("DATE", "")

    if birth_date and death_date:
        birth_date_format = datetime.strptime(birth_date, "%d %b %Y")
        death_date_format = datetime.strptime(death_date, "%d %b %Y")

        if birth_date_format > death_date_format:
            error_message = f"ERROR: INDIVIDUAL: US03: {indi_id}: Died {death_date_format.strftime(
                '%d %b %Y')} before born {birth_date_format.strftime('%d %b %Y')}"
            print(error_message)
            checked_birth_before_death.add(indi_id)

    return True  # If no birth date or no death date, consider it valid


for person in people:
    is_birth_before_death(person)

# Also, check the birth before death for spouses in families
for family in families:
    husband_id = family.get('HUSB', '')
    wife_id = family.get('WIFE', '')

    # Check husband's birth date
    if husband_id:
        husband = next((person for person in people if person.get(
            'INDI', '') == husband_id), None)
        if husband:
            is_birth_before_death(husband)

    # Check wife's birth date
    if wife_id:
        wife = next((person for person in people if person.get(
            'INDI', '') == wife_id), None)
        if wife:
            is_birth_before_death(wife)


def is_divorce_before_death(individuals, families):
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')
        divorce_date = family.get('DIV', {}).get('DATE', '')

        if husband_id:
            husband = next((person for person in individuals if person.get(
                'INDI', '') == husband_id), None)
            if husband:
                death_date = husband.get("DEATH", {}).get("DATE", "")
                if death_date and divorce_date:
                    death_date_format = datetime.strptime(
                        death_date, "%d %b %Y")
                    divorce_date_format = datetime.strptime(
                        divorce_date, "%d %b %Y")

                    if divorce_date_format > death_date_format:
                        error_message = f"ERROR: FAMILY: US06: {family.get('FAM', '')}: Divorced {divorce_date_format.strftime(
                            '%Y-%m-%d')} after husband's death on {death_date_format.strftime('%Y-%m-%d')}"
                        print(error_message)
                        return False

        if wife_id:
            wife = next((person for person in individuals if person.get(
                'INDI', '') == wife_id), None)
            if wife:
                death_date = wife.get("DEATH", {}).get("DATE", "")
                if death_date and divorce_date:
                    death_date_format = datetime.strptime(
                        death_date, "%d %b %Y")
                    divorce_date_format = datetime.strptime(
                        divorce_date, "%d %b %Y")

                    if divorce_date_format > death_date_format:
                        error_message = f"ERROR: FAMILY: US06: {family.get('FAM', '')}: Divorced {divorce_date_format.strftime(
                            '%Y-%m-%d')} after wife's death on {death_date_format.strftime('%Y-%m-%d')}"
                        print(error_message)
                        return False

    return True


is_divorce_before_death(people, families)


def MarriageBeforeDivorce(families):
    for family in families:
        family_id = family.get('FAM', '')
        marriage_date = family.get('MARR', {}).get('DATE', '')
        divorce_date = family.get('DIV', {}).get('DATE', '')

        if marriage_date and divorce_date:  # Checking only when both marriage and divorce dates are available
            marriage_date_format = datetime.strptime(marriage_date, "%d %b %Y")
            divorce_date_format = datetime.strptime(divorce_date, "%d %b %Y")

            if divorce_date_format < marriage_date_format:
                print(
                    f"ERROR: FAMILY: US04: {family_id}: bf02: Divorced {divorce_date_format.strftime('%Y-%m-%d')} before married {marriage_date_format.strftime('%Y-%m-%d')}")


MarriageBeforeDivorce(families)


def Date_Before_Current_Date(individuals, families):
    for individual in individuals:
        indi_id = individual.get('INDI', '')
        name = individual.get('NAME', '')

        birth_date = individual.get('BIRTH', {}).get('BDATE', '')
        death_date = individual.get('DEATH', {}).get('DATE', '')

        # For birth date
        if birth_date:
            birth_date_format = datetime.strptime(
                birth_date, "%d %b %Y").date()
            if birth_date_format > date.today():
                print(
                    f"ERROR: INDIVIDUAL: US01: {indi_id}: {name}: Birthday {birth_date_format.strftime('%Y-%m-%d')} occurs in the future")

        # For death date
        if death_date:
            death_date_format = datetime.strptime(
                death_date, "%d %b %Y").date()
            if death_date_format > date.today():
                print(
                    f"ERROR: INDIVIDUAL: US01: {indi_id}: {name}: Death {death_date_format.strftime('%Y-%m-%d')} occurs in the future")

    for family in families:
        fam_id = family.get('FAM', '')
        marriage_date = family.get('MARR', {}).get('DATE', '')
        divorce_date = family.get('DIV', {}).get('DATE', '')

        # For marriage date
        if marriage_date:
            marriage_date_format = datetime.strptime(
                marriage_date, "%d %b %Y").date()
            if marriage_date_format > date.today():
                print(
                    f"ERROR: FAMILY: US01: {fam_id}: Marriage date {marriage_date_format.strftime('%Y-%m-%d')} occurs in the future")

        # For divorce date
        if divorce_date:
            divorce_date_format = datetime.strptime(
                divorce_date, "%d %b %Y").date()
            if divorce_date_format > date.today():
                print(
                    f"ERROR: FAMILY: US01: {fam_id}: Divorce date {divorce_date_format.strftime('%Y-%m-%d')} occurs in the future")


Date_Before_Current_Date(people, families)

# PAIR PROGRAMMING - SD - Fewer than 15 siblings


def check_fewer_than_15_siblings(people, families):
    errors = []
    for family in families:
        children_ids = family.get('CHIL', [])

        if len(children_ids) >= 15:
            family_id = family.get('FAM', '')
            error_message = f"ERROR: FAMILY: US15: {
                family_id}: More than 15 siblings in the family."
            errors.append(error_message)
            print(error_message)
    return errors


check_fewer_than_15_siblings(people, families)

# PAIR PROGRAMMING - SD - Birth before marriage of parents


def check_birth_before_parents_marriage(people, families):
    for family in families:
        fam_id = family.get('FAM', '')
        children = find_children(fam_id)
        marriage_date = family.get('MARR', {}).get('DATE', '')

        if not marriage_date:
            continue

        marriage_date_format = datetime.strptime(
            marriage_date, "%d %b %Y").date()

        for child in children:
            child_birth_date = child.get("BIRTH", {}).get("BDATE", "")
            if child_birth_date:
                child_birth_date = child_birth_date.strip()
                if child_birth_date:
                    child_birth_date_format = datetime.strptime(
                        child_birth_date, "%d %b %Y").date()
                    if child_birth_date_format < marriage_date_format:
                        error_message = f"ERROR: INDIVIDUAL: US08: {child.get('INDI', '')}: Born {child_birth_date_format.strftime(
                            '%Y-%m-%d')} before parents' marriage on {marriage_date_format.strftime('%Y-%m-%d')}"
                        print(error_message)

    return "ERROR"


check_birth_before_parents_marriage(people, families)


def birth_before_death_of_parents(people, families):
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')
        children = find_children(family.get('FAM', ''))

        # Check if husband and wife are present
        if not husband_id or not wife_id:
            continue

        # Get the death dates of husband and wife
        husband_death_date = get_death_date(husband_id, people)
        wife_death_date = get_death_date(wife_id, people)

        for child in children:
            child_id = child.get('INDI', '')
            child_birth_date = child.get('BIRTH', {}).get('BDATE', '')

            if child_birth_date:
                child_birth_date_format = datetime.strptime(
                    child_birth_date, "%d %b %Y").date()

                if wife_death_date:
                    wife_death_date_format = wife_death_date.date()
                    if child_birth_date_format > wife_death_date_format:
                        error_message = f"ERROR: INDIVIDUAL: US09: {child_id}: Child born {child_birth_date_format.strftime(
                            '%d %b %Y')} after mother's death {wife_death_date.strftime('%d %b %Y')}"
                        print(error_message)

                if husband_death_date:
                    # Calculate the date nine months after the death of the father
                    nine_months_after_death = husband_death_date + \
                        timedelta(days=270)
                    nine_months_after_death_date = nine_months_after_death.date()
                    if child_birth_date_format > nine_months_after_death_date:
                        error_message = f"ERROR: INDIVIDUAL: US09: {child_id}: Child born {child_birth_date_format.strftime(
                            '%d %b %Y')} after nine months of father's death {husband_death_date.strftime('%d %b %Y')}"
                        print(error_message)


birth_before_death_of_parents(people, families)


def check_male_last_names(people, families):
    for family in families:
        husband_id = family.get('HUSB', '')
        children = find_children(family.get('FAM', ''))

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
                    error_message = f"ERROR: FAMILY: US16: {family.get('FAM', '')}: Male child ({child_id}) has a different last name ({
                        child_last_name}) than the husband ({husband_id}) ({husband_last_name})."
                    print(error_message)
                    return False

    return True


# Call the function with both individuals and families
check_male_last_names(people, families)


def less_than_150(people):
    for person in people:
        birth_date_str = person.get('BIRTH', {}).get('BDATE', '')
        death_date_str = person.get('DEATH', {}).get('DATE', '')

        if birth_date_str:
            birth_date = parse_date(birth_date_str)
            if death_date_str:
                death_date = parse_date(death_date_str)
                age_at_death = (death_date - birth_date).days / 365.25
                if age_at_death > 150:
                    error_message = f"ERROR: INDIVIDUAL: US07: {person.get('INDI', '')}: bi{person.get(
                        'LINE_NUM', '')}: More than 150 years old - Birth {birth_date_str}: Death {death_date_str}."
                    print(error_message)


# Call the less_than_150 function
less_than_150(people)


def check_marriage_validity(people, families):
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')
        marriage_date_str = family.get('MARR', {}).get('DATE', '')

        if not husband_id or not wife_id or not marriage_date_str:
            continue

        husband_birth_date = get_birth_date(husband_id, people)
        wife_birth_date = get_birth_date(wife_id, people)
        marriage_date = parse_date(marriage_date_str)

        if husband_birth_date and marriage_date and husband_birth_date > datetime.combine(marriage_date, datetime.min.time()):
            error_message = f"ERROR: INDIVIDUAL: US10: {husband_id}: Birthday {husband_birth_date.strftime(
                '%d %b %Y')} should be at least 14 years before marriage in family {family.get('FAM', '')}."
            print(error_message)

        if wife_birth_date and marriage_date and wife_birth_date > datetime.combine(marriage_date, datetime.min.time()):
            error_message = f"ERROR: INDIVIDUAL: US10: {wife_id}: Birthday {wife_birth_date.strftime(
                '%d %b %Y')} should be at least 14 years before marriage in family {family.get('FAM', '')}."
            print(error_message)


# Call the function check_marriage_validity
check_marriage_validity(people, families)


def check_sibling_married_to_child(people, families):
    for person in people:
        if 'FAMS' in person:
            siblings_ids = person['FAMS']  # Get IDs of siblings
            for sibling_id in siblings_ids:
                # Get sibling's details
                sibling = next((p for p in people if p.get(
                    'INDI', '') == sibling_id), None)
                if sibling and 'FAMS' in sibling:
                    # Get IDs of sibling's spouses
                    spouse_ids = sibling['FAMS']
                    for spouse_id in spouse_ids:
                        # Get spouse's details
                        spouse = next((p for p in people if p.get(
                            'INDI', '') == spouse_id), None)
                        # Check if spouse is the child
                        if spouse and spouse.get('FAMC', '') == person.get('FAMC', ''):
                            error_message = f"ERROR: INDIVIDUAL: US18: {
                                sibling_id}: Sibling is married to their child {person.get('INDI', '')}."
                            print(error_message)
                            return False
    return True


check_sibling_married_to_child(people, families)

# Sprint 3 -  List Siblings by Age


def list_siblings_by_age(people, families):
    print(f"Siblings Sorted by Age: ")
    siblings_by_age = {}  # Dictionary to store siblings grouped by family and ordered by age

    for family in families:
        family_id = family.get('FAM', '')
        # Get children for the family using find_children function
        children = find_children(family_id)

        if children:
            # Sort children by age in descending order
            children.sort(key=lambda x: datetime.strptime(
                x.get('BIRTH', {}).get('BDATE', '01 JAN 1900'), "%d %b %Y"))

            # Add sorted children to the dictionary
            siblings_by_age[family_id] = children

    # Print siblings grouped by family and ordered by age
    for family_id, siblings in siblings_by_age.items():
        print(f"  Family ID: {family_id}")
        i = 1
        for sibling in siblings:
            name = sibling.get('NAME', '')
            print(f"     {i}, {name}")
            i += 1
    return True


# Call the function to list siblings by age
list_siblings_by_age(people, families)


def check_unique_name_and_birth(people):
    name_birth_dict = {}
    errors = []

    for person in people:
        name = person.get('NAME', '')
        birth_date = person.get('BIRTH', {}).get('BDATE', '')

        if name and birth_date:
            name_birth_key = (name, birth_date)
            if name_birth_key in name_birth_dict:
                error_message = f"ERROR: INDIVIDUAL: US23: Duplicate individual found with the same name '{
                    name}' and birthdate '{birth_date}'."
                errors.append(error_message)
            else:
                name_birth_dict[name_birth_key] = person['INDI']

    for error in errors:
        print(error)

    return not errors


if check_unique_name_and_birth(people):
    print("No individuals with the same name and birthdate found.")
else:
    print("Duplicate individuals with the same name and birthdate found.")


def check_gender(people, families):
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')

        if husband_id:
            husband = next((person for person in people if person.get(
                'INDI', '') == husband_id), None)
            if husband:
                husband_gender = husband.get('SEX', '')
                if husband_gender != 'M':
                    error_message = f"ERROR: INDIVIDUAL: US21: {
                        husband_id}: Should be a male."
                    print(error_message)

        if wife_id:
            wife = next((person for person in people if person.get(
                'INDI', '') == wife_id), None)
            if wife:
                wife_gender = wife.get('SEX', '')
                if wife_gender != 'F':
                    error_message = f"ERROR: INDIVIDUAL: US21: {
                        wife_id}: Should be a female."
                    print(error_message)


# Call the check_gender function
check_gender(people, families)


def check_siblings_not_married(people, families):
    errors = []
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')
        husband = next(
            (p for p in people if p.get('INDI') == husband_id), None)
        wife = next((p for p in people if p.get('INDI') == wife_id), None)

        if husband and wife:
            husband_famc = husband.get('FAMC')
            wife_famc = wife.get('FAMC')

            if husband_famc and wife_famc and husband_famc == wife_famc:
                error_message = f"ERROR: FAMILY: US18: {family.get('FAM', '')}: Siblings {
                    husband_id} and {wife_id} are married to each other."
                errors.append(error_message)

    for error in errors:
        print(error)
    return not errors


check_siblings_not_married(people, families)


def check_unique_ids(individuals, families):
    individual_ids = set()
    family_ids = set()

    for individual in individuals:
        indi_id = individual.get('INDI', '')
        if indi_id in individual_ids:
            error_message = f"ERROR: INDIVIDUAL: US22: Duplicate individual ID {
                indi_id} found."
            print(error_message)
            return False
        individual_ids.add(indi_id)

    for family in families:
        fam_id = family.get('FAM', '')
        if fam_id in family_ids:
            error_message = f"ERROR: FAMILY: US22: Duplicate family ID {
                fam_id} found."
            print(error_message)
            return False
        family_ids.add(fam_id)

    return True


check_unique_ids(people, families)
