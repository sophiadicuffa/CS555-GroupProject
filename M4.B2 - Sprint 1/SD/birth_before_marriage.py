from datetime import datetime

people = []
families = []
current_person = {}
current_family = {}

def calculate_age(birthdate, deathdate):

    if not birthdate:
        return "N/A"
        
    birthdate = datetime.strptime(birthdate, "%d %b %Y")
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    if deathdate:
        deathdate = datetime.strptime(deathdate, "%d %b %Y")
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
        if 'MARR' in current_family and tag == 'DATE':
            current_family['MARR']['DATE'] = ' '.join(parts[2:])
            
        if 'DIV' in current_family and tag == 'DATE':
            current_family['DIV']['DATE'] = ' '.join(parts[2:])
            


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

        husband_birth_date_format = datetime.strptime(husband_birth_date, "%d %b %Y")
        wife_birth_date_format = datetime.strptime(wife_birth_date, "%d %b %Y")

        if husband_birth_date and wife_birth_date and marriage_date:
            if husband_birth_date_format > datetime.strptime(marriage_date, "%d %b %Y"):
                error_message = f"ERROR: FAMILY: US02: {family.get('FAM', '')}: Husband's birthday of {husband_birth_date_format} is after marriage."
                print(error_message)
                return False
            elif wife_birth_date_format > datetime.strptime(marriage_date, "%d %b %Y"):
                error_message = f"ERROR: FAMILY: US02: {family.get('FAM', '')}: Wife's birthday of {wife_birth_date_format} is after marriage"
                print(error_message)
                return False
    return True

check_birth_before_marriage(people, families)