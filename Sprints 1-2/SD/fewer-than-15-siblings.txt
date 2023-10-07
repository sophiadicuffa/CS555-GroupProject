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