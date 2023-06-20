import csv
import json

def write_on_file(file, M):
    f = open(file, "w")

    for row in M:
        f.write('\t'.join(str(value) for value in row))
        f.write('\n')

    f.close()

def read_from_csv(file):
    positions = list()
    with open(file, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        positions = [int(item) for item in next(csv_reader)]
    
    return positions

def read_from_json(file):
    with open(file, 'r') as file:
        data = json.load(file)
    if isinstance(data, list):
        return [int(item) for item in data]
    else:
        raise ValueError("Invalid data. Expecting a list of integers.")

