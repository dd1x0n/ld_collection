import csv
from collections import Counter
from matplotlib import pyplot as plt

plt.style.use("bmh")

with open ('collection.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    genre_counter = Counter()

    for row in csv_reader:
        genre_counter.update(row['Genre'].split(','))

#Populate a List
genres =[]
popularity = []

for item in genre_counter.most_common(10):
    genres.append(item[0])
    popularity.append(item[1])

genres.reverse()
popularity.reverse()

plt.bar(genres, popularity)

plt.title("Top Ten Most Popular Genres in this collection!")
plt.xlabel("Amount in Collection")

plt.tight_layout()

plt.show()
