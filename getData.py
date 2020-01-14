import csv
def getUrls():
    urls = []
    with open('list.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            urls.append(row[1])
    return urls