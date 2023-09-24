# Sophia DiCuffa, Nadeya DeDiago, Amanda Vu
# CS555 M3.B2

from datetime import datetime

people = []
families = []
current_person = {}
current_family = {}

# Function to calculate age
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

# Read GEDCOM file
def process_line(line):

    global current_person
    global current_family

    line = line.strip()
    parts = line.split()
    level = int(parts[0]) # 0, 1 ,2 
    tag = parts[1] # INDI, FAM, etc.

    if len(parts) > 2:
        special_tag = parts[2]
    else:
        special_tag = ''

    if level == 0:
        if special_tag == 'INDI':
            if current_person:
                people.append(current_person)
            current_person = {}  # Initialize a new person dictionary
        elif special_tag == 'FAM':
            if current_family:
                families.append(current_family)
            current_family = {}
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
    elif level == 2:
        if 'BIRTH' in current_person:
            if tag == 'DATE':
                current_person['BIRTH']['DATE'] = ' '.join(parts[2:])
        elif 'MARR' in current_family:
            if tag == 'DATE':
                current_family['MARR']['DATE'] = ' '.join(parts[2:])
    

# open GEDCOM file
with open('test.ged', 'r') as gedcom_file:
    for line in gedcom_file:
        process_line(line)

# add last person
if current_person:
    people.append(current_person)


# table to print individuals 
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


