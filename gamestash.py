import csv
from collections import Counter
from matplotlib import pyplot as plt

plt.style.use("bmh")

#Plot/graph req. + matplotlib "Stretch” Feature"

with open ('games.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    #Int derieved w/ use of counter 
    system_counter = Counter()

    for row in csv_reader:
        system_counter.update(row['System'].split(','))

#Populate a List
systems =[]
popularity = []

for item in system_counter.most_common(15):
    systems.append(item[0])
    popularity.append(item[1])

systems.reverse()
popularity.reverse()

plt.barh(systems, popularity)

plt.title("Systems with the most games")
plt.xlabel("Amount in Collection")

plt.tight_layout()

plt.show()
