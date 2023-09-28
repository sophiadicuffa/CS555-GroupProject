import re

# Function to parse the date in GEDCOM format (e.g., "2 DATE 6 JUN 2002")
def parse_date(date_str):
    date_match = re.match(r'(\d{1,2}) ([A-Z]{3}) (\d{4})', date_str)
    if date_match:
        day, month, year = date_match.groups()
        # You may want to convert month abbreviations to numerical values if needed
        return int(year), month, int(day)
    else:
        return None

# Function to check if birthdate is before marriage date and print a table
def print_marriage_table(individuals, families):
    print("{:<20} {:<20} {:<20} {:<10}".format("Wife's Birthday", "Husband's Birthday", "Marriage Date", "Passes"))
    print("="*80)

    for family_id, family in families.items():
        husband_id = family.get('HUSB', None)
        wife_id = family.get('WIFE', None)
        if husband_id and wife_id:
            husband = individuals.get(husband_id, {})
            wife = individuals.get(wife_id, {})
            marriage_date = parse_date(family.get('MARR', ''))
            husband_birth_date = parse_date(husband.get('BIRT', ''))
            wife_birth_date = parse_date(wife.get('BIRT', ''))
            if marriage_date and husband_birth_date and wife_birth_date:
                passes = husband_birth_date <= marriage_date and wife_birth_date <= marriage_date
                print("{:<20} {:<20} {:<20} {:<10}".format(
                    f"{wife_birth_date[2]}-{wife_birth_date[1]}-{wife_birth_date[0]}",
                    f"{husband_birth_date[2]}-{husband_birth_date[1]}-{husband_birth_date[0]}",
                    f"{marriage_date[2]}-{marriage_date[1]}-{marriage_date[0]}",
                    str(passes)))

def parse_gedcom(filename):
    individuals = {}
    families = {}
    current_individual = None
    current_family = None
    processing_name = False  # Flag to indicate processing NAME tag

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts:
                level = int(parts[0])
                tag = parts[1]
                if level == 0:
                    if tag == 'INDI':
                        current_individual = parts[2]
                        individuals[current_individual] = {}
                        processing_name = False  # Reset the flag
                    elif tag == 'FAM':
                        current_family = parts[2]
                elif level == 1:
                    if tag == 'NAME':
                        individuals[current_individual]['NAME'] = ' '.join(parts[2:])
                        processing_name = True  # Set the flag when processing NAME
                    elif current_family:
                        if tag == 'HUSB' or tag == 'WIFE':
                            families[current_family][tag] = parts[2]
                        elif tag == 'CHIL':
                            if tag not in families[current_family]:
                                families[current_family][tag] = []
                            families[current_family][tag].append(parts[2])
                elif level == 2 and processing_name:
                    if tag == 'SURN':
                        individuals[current_individual]['NAME'] += ' ' + ' '.join(parts[2:])
                elif level == 2:
                    if tag == 'DATE':
                        individuals[current_individual]['BIRT'] = ' '.join(parts[2:])
                    elif current_family:
                        if tag == 'MARR':
                            families[current_family][tag] = ' '.join(parts[2:])

    return individuals, families



if __name__ == "__main__":
    filename = "test.ged"  # Replace with the path to your GEDCOM file
    individuals, families = parse_gedcom(filename)
    print_marriage_table(individuals, families)
