import csv

with open("sample.csv","r") as f:
    for line in csv.reader(f):
        print(line)
