# Sophia DiCuffa, Nadeya De Diago, Amanda Vu
# CS555 M3.B2

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

# print("{:<10} {:<30} {:<10} {:<15} {:<20} {:<10} {:<20}".format("ID", "Name", "Sex", "Birthday", "Age", "Spouse", "Parent"))

# # Iterate through the individuals
# for person in people:
#     indi_id = person.get('INDI', '')
#     name = person.get('NAME', '')
#     sex = person.get('SEX', '')
#     birthday = person.get('BIRTH', {}).get('DATE', '')
#     death_date = person.get('DEATH', {}).get('DATE', '')
#     age = calculate_age(birthday, death_date)
    
#     # Find the family tag they belong to (as husband or wife)
#     spouse_tag = 'N/A'
#     parent_tag = 'N/A'

#     if 'FAMC' in person:
#         family_id = person['FAMC']
#         parents = find_parents(family_id)
#         parent_names = [parent.get('NAME', '') for parent in parents]
#         parent_tag = family_id
    
#     for family in families:
#         fam_id = family.get('FAM', '')

#         husband_id = family.get('HUSB', '')
#         wife_id = family.get('WIFE', '')
#         if indi_id == husband_id or indi_id == wife_id:
#             spouse_tag = family.get('FAM', '')
#             break

#     print("{:<10} {:<30} {:<10} {:<15} {:<20} {:<10} {:<20}".format(indi_id, name, sex, birthday, age, spouse_tag, parent_tag))

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
    status = "Married" if not divorced_date or divorced_date == 'N/A' else "Divorced"
    
    print("{:<10} {:<15} {:<15} {:<20} {:<20} {:<15} {:<35} {:<40}".format(
        fam_id, marriage_date, divorced_date, husband_id, husband_name, wife_id, wife_name, children_names))

def check_marriage_before_death(people, families):
    print("{:<15} {:<15} {:<20} {:<20}".format("Husband Death", "Wife Death", "Marriage Date", "Result"))
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
            hus_death = next((person.get('DEATH', {}).get('DATE', '') for person in people if person.get('INDI', '') == husband_id), '')
            if hus_death:
                husband_birth = datetime.strptime(hus_death, "%d %b %Y").strftime("%d %b %Y")

        if wife_id:
            wife_death = next((person.get('DEATH', {}).get('DATE', '') for person in people if person.get('INDI', '') == wife_id), '')
            if wife_death:
                wife_birth = datetime.strptime(wife_death, "%d %b %Y").strftime("%d %b %Y")

        if marriage_date and hus_death and wife_death:
            if datetime.strptime(hus_death, "%d %b %Y") < datetime.strptime(marriage_date, "%d %b %Y") or datetime.strptime(wife_death, "%d %b %Y") > datetime.strptime(marriage_date, "%d %b %Y"):
                result = "Fail"

        print("{:<15} {:<15} {:<20} {:<20}".format(husband_birth, wife_birth, marriage_date, result))

check_marriage_before_death(people, families)