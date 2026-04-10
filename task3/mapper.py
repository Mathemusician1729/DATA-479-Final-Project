import sys
import csv
import io

# force utf output for windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    # use csv.reader to deal with quotes around values
    # because some values have commas in them so a simple split will not working
    try:
        fields = next(csv.reader([line]))
    except StopIteration:
        continue
    
    # skip header
    if fields[0].strip() == 'STATION':
        continue
    
    # make sure there's enough columns
    if len(fields) < 7:
        continue
    
    # extract and clean the needed columns
    station     = fields[0].strip().strip('"')
    date        = fields[1].strip().strip('"')
    temp_str    = fields[6].strip().strip('"')

    # extract year from data
    year = date[:4]

    # validate and convert TEMP
    # GSOD uses 9999.9 in place of missing data
    try:
        temp = float(temp_str)
    except ValueError:
        continue
    
    if temp == 9999.9:
        continue
    
    # emit (station, year)
    # value: (temp, 1)
    print(f"{station},{year}\t{temp},1")