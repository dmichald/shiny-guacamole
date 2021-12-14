#!/usr/bin/env python
import csv
import matplotlib.pyplot as plt
import numpy as np
import operator
from itertools import islice

"""
Detect DDOS attack
"""
def measure_intensity_of_requests(rows):
    intensity = {}
    for row in rows:
        if int(row[0]) in intensity.keys():
            intensity[int(row[0])] += 1
        else:
            intensity[int(row[0])] = 1
    return intensity


def draw_intensity_measurments(intensity):
    x = np.mean(np.array( list(intensity.keys())[0:len(intensity.keys())-2] ).reshape(-1, 62), axis=1)
    y = np.mean(np.array( list(intensity.values())[0:len(intensity.keys())-2] ).reshape(-1, 62), axis=1)

    plt.plot(x, y,
             color='green', linestyle='dashed', linewidth = 2,
             marker='o', markerfacecolor='blue', markersize=8)
    plt.xlabel('Czas w sekundach (epoch time format)')
    plt.ylabel('Ilość żądań i odpowiedzi')
    plt.title('Natężenie ruchu w danej chwili')
    plt.show()


def get_most_loaded_devices_in_given_second(rows, second):
    devices_load  = {}
    for row in rows:
        if int(row[0]) == second:
            if row[2] in devices_load:
                devices_load[row[2]] += 1
            else:
                devices_load[row[2]] = 1
    devices_load = sorted(devices_load.items(), key=operator.itemgetter(1), reverse=True)
    return devices_load


def get_number_of_devices_in_most_intensive_seconds(rows, intensity):
    sorted_intensity = sorted(intensity.items(), key=operator.itemgetter(1), reverse=True)
    load = []
    for intensity_ in sorted_intensity[:3]:
        devices = get_most_loaded_devices_in_given_second(rows, intensity_[0])
        load.append(len(devices))
    print(load)


def get_average_duration_in_most_intensive_seconds(rows, intensity):
    sorted_intensity = sorted(intensity.items(), key=operator.itemgetter(1), reverse=True)
    avg_duration = []
    for intensity_ in sorted_intensity[:3]:
        counter = 0
        duration = 0
        for row in rows:
            if int(row[0]) == intensity_[0]:
                duration += int(row[1])
                counter += 1
        avg_duration.append(duration / counter)
    print(avg_duration)
    return avg_duration


"""
Detect scanning
"""
def get_count_of_distinct_ports_in_span_of_time(rows, time_span):
    count_of_distinct_ports = []
    start_time = int(rows[0][0])
    for i in range(len(rows)):
        if int(rows[i][0]) <= start_time + time_span:
            continue
        start_time = int(rows[i][0])
        ports = []
        count = 0
        for j in range(i + 1, len(rows)):
            if int(rows[j][0]) < start_time or int(rows[j][0]) > int(start_time) + time_span:
                break;
            if rows[j][6] not in ports:
                ports.append(rows[j][6])
            else:
                count += 1
        count_of_distinct_ports.append(count)
    return count_of_distinct_ports


def get_how_much_port_different_traffic_is_being_generated_by_single_device(rows):
    distinct_port_computer_dict = {}
    for row in rows:
        if (row[4] != "6" and row[4] != "17") or int(row[7]) > 4 or int(row[8]) > 4:
            continue
        
        if row[2] in distinct_port_computer_dict.keys():
            distinct_port_computer_dict[row[2]].add(row[6])
        else:
            distinct_port_computer_dict[row[2]] = set()
            distinct_port_computer_dict[row[2]].add(row[6])

    for key, value in distinct_port_computer_dict.items():
        distinct_port_computer_dict[key] = len(value)
        
    return dict(sorted(distinct_port_computer_dict.items(), key=operator.itemgetter(1), reverse=True))


def get_span_of_time_the_device_was_active(rows, device):
    start = 0
    end = 0
    for row in rows:
        if row[2] == device and start == 0:
            start = row[0]
        elif row[2] == device:
            end = row[0]
    return (start, end)


def get_count_of_distinct_dst_devices(rows, device):
    dst_devices = set()
    for row in rows:
        if row[2] == device:
            dst_devices.add(row[5])
            
    return len(dst_devices)


# TODO: refactor function name
def get_asdf(rows, devices):
    for device in devices:
        start, end = get_span_of_time_the_device_was_active(rows, device)
        print(device, ": czas trwania komunikacji=", int(end) - int(start))
        print(device, ": liczba różnych urządzeń dst=", get_count_of_distinct_dst_devices(rows, device))


def main():
    f = open("final.csv", "r")
    csv_reader = csv.reader(f)
    fields = next(csv_reader)
    rows = []

    for row in csv_reader:
        rows.append(row)

    #intensity = measure_intensity_of_requests(rows)
    #draw_intensity_measurments(intensity)
    #get_number_of_devices_in_most_intensive_seconds(rows, intensity)
    #get_average_duration_in_most_intensive_seconds(rows, intensity)
    #print(get_count_of_distinct_ports_in_span_of_time(rows, 250))
    print(list(islice(get_how_much_port_different_traffic_is_being_generated_by_single_device(rows).items(), 5)))
    get_asdf(rows, ["Comp073202", "Comp623258", "Comp044772", "Comp607982", "Comp364445"])

    
if __name__ == '__main__':
    main()
