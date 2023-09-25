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

        elif tag == 'DATE':

            if 'BIRTH' in current_person:

                current_person['BIRTH']['DATE'] = ' '.join(parts[2:])

            elif 'DEATH' in current_person:

                current_person['DEATH']['DATE'] = ' '.join(parts[2:])

        elif tag == 'HUSB':

            current_family['HUSB'] = parts[2]

        elif tag == 'WIFE':

            current_family['WIFE'] = parts[2]

        elif tag == 'MARR':

            current_family['MARR'] = {}



    elif level == 2:

        if 'BIRTH' in current_person and tag == 'DATE':

            current_person['BIRTH']['DATE'] = ' '.join(parts[2:])

        elif 'MARR' in current_family and tag == 'DATE':

            current_family['MARR']['DATE'] = ' '.join(parts[2:])

        elif tag == 'CHIL':

            current_family.setdefault('CHIL', []).append(parts[2])



with open('test.ged', 'r') as gedcom_file:

    for line in gedcom_file:

        process_line(line)



if current_person:

    people.append(current_person)



if current_family:

    families.append(current_family)



people = sorted(people, key=lambda k: k['INDI'])

families = sorted(families, key=lambda k: k['FAM'])



print("people:")

print("{:<10} {:<30} {:<10} {:<15} {:<20} {:<10}".format("ID", "Name", "Sex", "Birthday", "Age", "Status"))

for person in people:

    indi_id = person.get('INDI', '')

    name = person.get('NAME', '')

    sex = person.get('SEX', '')

    birthday = person.get('BIRTH', {}).get('DATE', '')

    death_date = person.get('DEATH', {}).get('DATE', '')

    age = calculate_age(birthday, death_date)

    status = "Alive" if not death_date else "Dead"

    print("{:<10} {:<30} {:<10} {:<15} {:<20} {:<10}".format(indi_id, name, sex, birthday, age, status))



# ... (your existing code)

# Function to find children for a family
def find_children(family_id):
    return [person for person in people if person.get('FAMC') == family_id]

# Table to print families
print("\nFamilies:")
print("{:<10} {:<15} {:<15} {:<20} {:<20} {:<30} {:<10}".format(
    "ID", "Married Date", "Divorced Date", "Husband Name", "Wife Name", "Children", "Status"))

def extract_date(event):
    date = event.get('DATE')
    if date:
        return ' '.join(date.split()[1:])
    return 'N/A'

for family in families:
    fam_id = family.get('FAM', '')
    marriage_date = extract_date(family.get('MARR', {}))
    divorced_date = extract_date(family.get('DIV', {}))
    husband_id = family.get('HUSB', '')
    husband_name = next((person.get('NAME', '') for person in people if person.get('INDI', '') == husband_id), '')
    wife_id = family.get('WIFE', '')
    wife_name = next((person.get('NAME', '') for person in people if person.get('INDI', '') == wife_id), '')
    
    # Find children associated with this family
    children = find_children(fam_id)
    
    # Format children names
    children_names = ', '.join([child.get('NAME', '') for child in children])
    
    status = "Married" if not divorced_date or divorced_date == 'N/A' else "Divorced"
    
    print("{:<10} {:<15} {:<15} {:<20} {:<20} {:<30} {:<10}".format(
        fam_id, marriage_date, divorced_date, husband_name, wife_name, children_names, status))
