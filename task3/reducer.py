import sys
import io

# force utf output for windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')

current_key     = None
current_sum     = 0.0
current_count   = 0

for line in sys.stdin:
    line = line.strip()

    try:
        key, value = line.split('\t', 1)
    except ValueError:
        continue
    
    # Parse value back into temp and count
    try:
        temp_str, count_str = value.split(',', 1)
        temp    = float(temp_str)
        count   = int(count_str)
    except ValueError:
        continue
    
    if  current_key == key:
        current_sum     += temp
        current_count   += count
    else:
        if current_key is not None:
            average = current_sum / current_count
            # split key back into station and year
            station, year = current_key.split(',', 1)
            print(f"{station}, {year}, {average:.2f}")
        
        current_key     = key
        current_sum     = temp
        current_count   = count

# final key
if current_key is not None:
    average = current_sum / current_count
    station, year = current_key.split(',', 1)
    print(f"{station}, {year}, {average:.2f}")