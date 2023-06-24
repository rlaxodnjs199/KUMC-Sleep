import re

log_path = "/Users/kimtaecircle/Codes/kumc/scripts/sdmlog.txt"

with open(log_path, "r") as f:
    count = 0
    total_time = 0
    for line in f:
        match = re.match("\d+m \d+s", line)
        min, s = match.group().split(" ")
        time = int(min[:-1]) * 60 + int(s[:-1])
        if time < 90:
            continue
        else:
            count += 1
            total_time += time
    print(f"Average: {total_time / count}s, {count}")
