with open("netflow_day-02.txt", "r") as f:
    lines = f.readlines()
with open("clean_data.csv", "w") as f:
    counter = 0
    for line in lines:
        if counter < 1000000:
            f.write(line)
        counter += 1
