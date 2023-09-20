# Nadeya DeDiago, Sophia DiCuffa, Amanda Vu - CS555 M3.B2

# Reads each line of the GEDCOM file
def process_line(line):
    line = line.strip()
    parts = line.split(' ', 2)

# Read the GEDCOM file
with open('My-Family.ged', 'r') as gedcom_file:
    for line in gedcom_file:
        process_line(line)
