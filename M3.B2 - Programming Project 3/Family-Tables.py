# Sophia DiCuffa, Nadeya De Diago, Amanda Vu
# CS555 M3.B2

from datetime import datetime, date

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

    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    if deathdate:
        try:
            deathdate = datetime.strptime(deathdate, "%d %b %Y")
        except ValueError:
            return f"{age} (Died: Invalid date format)"

        age_at_death = deathdate.year - birthdate.year - ((deathdate.month, deathdate.day) < (birthdate.month, birthdate.day))
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

print("{:<10} {:<30} {:<10} {:<15} {:<20} {:<10} {:<20}".format("ID", "Name", "Sex", "Birthday", "Age", "Spouse", "Parent"))

# Iterate through the individuals
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

    print("{:<10} {:<30} {:<10} {:<15} {:<20} {:<10} {:<20}".format(indi_id, name, sex, birthday, age, spouse_tag, parent_tag))

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
    husband_name = next((person.get('NAME', '') for person in people if person.get('INDI', '') == husband_id), '')
    wife_id = family.get('WIFE', '')
    wife_name = next((person.get('NAME', '') for person in people if person.get('INDI', '') == wife_id), '')
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
def check_birth_before_marriage(people, families):
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')
        marriage_date = family.get('MARR', {}).get('DATE', '')

        if not husband_id or not wife_id or not marriage_date:
            continue

        husband_birth_date = next((person.get('BIRTH', {}).get('BDATE', '') for person in people if person.get('INDI', '') == husband_id), '')
        wife_birth_date = next((person.get('BIRTH', {}).get('BDATE', '') for person in people if person.get('INDI', '') == wife_id), '')
        
        marriage_date_format = datetime.strptime(marriage_date, "%d %b %Y")
        husband_birth_date_format = datetime.strptime(husband_birth_date, "%d %b %Y")
        wife_birth_date_format = datetime.strptime(wife_birth_date, "%d %b %Y")

        if husband_birth_date and wife_birth_date and marriage_date:
            if husband_birth_date_format > datetime.strptime(marriage_date, "%d %b %Y"):
                error_message = f"ERROR: FAMILY: US02: {family.get('FAM', '')}: Husband's birthday of {husband_birth_date_format} is after marriage date of {marriage_date_format}."
                print(error_message)
                return False
            elif wife_birth_date_format > datetime.strptime(marriage_date, "%d %b %Y"):
                error_message = f"ERROR: FAMILY: US02: {family.get('FAM', '')}: Wife's birthday of {wife_birth_date_format} is after marriage date of {marriage_date_format}."
                print(error_message)
                return False
    return True

check_birth_before_marriage(people, families)

# SPRINT 1 - SD - Marriage before Death

def check_marriage_before_death(people, families):
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')
        marriage_date = family.get('MARR', {}).get('DATE', '')

        if not husband_id or not wife_id or not marriage_date:
            continue

        husband_death_date = next((person.get('DEATH', {}).get('DATE', '') for person in people if person.get('INDI', '') == husband_id), '')
        wife_death_date = next((person.get('DEATH', {}).get('DATE', '') for person in people if person.get('INDI', '') == wife_id), '')

        marriage_date_format = datetime.strptime(marriage_date, "%d %b %Y")

        if husband_death_date:
            husband_death_date_format = datetime.strptime(husband_death_date, "%d %b %Y")
        else:
            husband_death_date_format = None
        
        if wife_death_date:
            wife_death_date_format = datetime.strptime(wife_death_date, "%d %b %Y")
        else:
            wife_death_date_format = None

        if husband_death_date_format is not None and marriage_date:
            if husband_death_date_format < datetime.strptime(marriage_date, "%d %b %Y"):
                error_message = f"ERROR: FAMILY: US05: {family.get('FAM', '')}: Husband's death of {husband_death_date_format} is before marriage date of {marriage_date_format}"
                print(error_message)
                return False

        if wife_death_date_format is not None and marriage_date:  
            if wife_death_date_format < datetime.strptime(marriage_date, "%d %b %Y"):
                error_message = f"ERROR: FAMILY: US05: {family.get('FAM', '')}: Wife's death of {wife_death_date_format} is before marriage date of {marriage_date_format}"
                print(error_message)
                return False
    return True

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
            error_message = f"ERROR: INDIVIDUAL: US03: {indi_id}: Died {death_date_format.strftime('%d %b %Y')} before born {birth_date_format.strftime('%d %b %Y')}"
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
        husband = next((person for person in people if person.get('INDI', '') == husband_id), None)
        if husband:
            is_birth_before_death(husband)

    # Check wife's birth date
    if wife_id:
        wife = next((person for person in people if person.get('INDI', '') == wife_id), None)
        if wife:
            is_birth_before_death(wife)

def is_divorce_before_death(individuals, families):
    for family in families:
        husband_id = family.get('HUSB', '')
        wife_id = family.get('WIFE', '')
        divorce_date = family.get('DIV', {}).get('DATE', '')

        if husband_id:
            husband = next((person for person in individuals if person.get('INDI', '') == husband_id), None)
            if husband:
                death_date = husband.get("DEATH", {}).get("DATE", "")
                if death_date and divorce_date:
                    death_date_format = datetime.strptime(death_date, "%d %b %Y")
                    divorce_date_format = datetime.strptime(divorce_date, "%d %b %Y")

                    if divorce_date_format > death_date_format:
                        error_message = f"ERROR: FAMILY: US06: {family.get('FAM', '')}: Divorced {divorce_date_format.strftime('%Y-%m-%d')} after husband's death on {death_date_format.strftime('%Y-%m-%d')}"
                        print(error_message)
                        return False

        if wife_id:
            wife = next((person for person in individuals if person.get('INDI', '') == wife_id), None)
            if wife:
                death_date = wife.get("DEATH", {}).get("DATE", "")
                if death_date and divorce_date:
                    death_date_format = datetime.strptime(death_date, "%d %b %Y")
                    divorce_date_format = datetime.strptime(divorce_date, "%d %b %Y")

                    if divorce_date_format > death_date_format:
                        error_message = f"ERROR: FAMILY: US06: {family.get('FAM', '')}: Divorced {divorce_date_format.strftime('%Y-%m-%d')} after wife's death on {death_date_format.strftime('%Y-%m-%d')}"
                        print(error_message)
                        return False

    return True

# Call the function with both individuals and families
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
                print(f"ERROR: FAMILY: US04: {family_id}: bf02: Divorced {divorce_date_format.strftime('%Y-%m-%d')} before married {marriage_date_format.strftime('%Y-%m-%d')}")

MarriageBeforeDivorce(families)

def Date_Before_Current_Date(individuals, families):
    for individual in individuals:
        indi_id = individual.get('INDI', '')
        name = individual.get('NAME', '')
        
        birth_date = individual.get('BIRTH', {}).get('BDATE', '')
        death_date = individual.get('DEATH', {}).get('DATE', '')

        # For birth date
        if birth_date:
            birth_date_format = datetime.strptime(birth_date, "%d %b %Y").date()
            if birth_date_format > date.today():
                print(f"ERROR: INDIVIDUAL: US01: {indi_id}: {name}: Birthday {birth_date_format.strftime('%Y-%m-%d')} occurs in the future")
        
        # For death date
        if death_date:
            death_date_format = datetime.strptime(death_date, "%d %b %Y").date()
            if death_date_format > date.today():
                print(f"ERROR: INDIVIDUAL: US01: {indi_id}: {name}: Death {death_date_format.strftime('%Y-%m-%d')} occurs in the future")

    for family in families:
        fam_id = family.get('FAM', '')
        marriage_date = family.get('MARR', {}).get('DATE', '')
        divorce_date = family.get('DIV', {}).get('DATE', '')

        # For marriage date
        if marriage_date:
            marriage_date_format = datetime.strptime(marriage_date, "%d %b %Y").date()
            if marriage_date_format > date.today():
                print(f"ERROR: FAMILY: US01: {fam_id}: Marriage date {marriage_date_format.strftime('%Y-%m-%d')} occurs in the future")

        # For divorce date
        if divorce_date:
            divorce_date_format = datetime.strptime(divorce_date, "%d %b %Y").date()
            if divorce_date_format > date.today():
                print(f"ERROR: FAMILY: US01: {fam_id}: Divorce date {divorce_date_format.strftime('%Y-%m-%d')} occurs in the future")

Date_Before_Current_Date(people, families)

# PAIR PROGRAMMING - SD - Fewer than 15 siblings

def check_fewer_than_15_siblings(people, families):
    for family in families:
        children_ids = family.get('CHIL', [])
        
        if len(children_ids) >= 15:
            family_id = family.get('FAM', '')
            error_message = f"ERROR: FAMILY: US15: {family_id}: More than 15 siblings in the family."
            print(error_message)

# Create a fake family with more than 15 siblings to test 
fake_family = {
    'FAM': 'F01 (FAKE FAMILY)',
    'HUSB': 'I01',
    'WIFE': 'I02',
    'CHIL': ['I03', 'I04', 'I05', 'I06', 'I07', 'I08', 'I09', 'I10', 'I11', 'I12', 'I13', 'I14', 'I15', 'I16', 'I17', 'I18', 'I19', 'I20']
}
families.append(fake_family)

check_fewer_than_15_siblings(people, families)




