import os

filtered = []
for file in os.listdir('history'):
    with open(os.path.join('history', file)) as f:
        data = f.readlines()
    for line in data:
        parts = line.split('|')
        if len(parts) > 5:
            result = parts[5:][0].replace(' ', '').replace('-', '').replace('|', ' ')
            if len(result) > 10:
                filtered.append(result)

with open(os.path.join('filtered_history', 'case.md'), 'w', encoding="utf-8") as f:
    for line in filtered:
        f.write(line + '\n')
