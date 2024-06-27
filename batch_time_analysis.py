import datetime
import re
import csv

def parse_line(line):
    config = line.split('BF:')[1].split(':')[0]
    time = datetime.datetime.strptime(line.split(': ')[0], "%Y-%m-%d-%H:%M:%S")
    return [config, time]

with open('batch-AIQ-5.log', 'r') as file:
    log_lines = file.readlines()[1:-1] 

config = []
total_duration = datetime.timedelta()

for index, row in enumerate(log_lines[:-1]): 
    if parse_line(row)[0] == parse_line(log_lines[index+1])[0]:
        start = parse_line(row)
        end = parse_line(log_lines[index+1])[1]
        duration = end - start[1]
        total_duration += duration
        start.extend([end, duration])
        config.append(start)

avg_duration = total_duration / len(config)

with open('config_times.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Config", "Start Time", "End Time", "Duration"])
    for item in config:
        writer.writerow([item[0], item[1], item[2], item[3]])

print(f"Average Duration: {avg_duration}")
print(f"Total Duration: {total_duration}")