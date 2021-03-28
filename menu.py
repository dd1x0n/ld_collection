import sys
import csv
import random
import pandas as pd

W  = '\033[0m'
R  = '\033[31m'
G  = '\033[32m'
O  = '\033[33m'
B  = '\033[34m'
P  = '\033[35m'

def menu():
    print("")
    print(W+"*/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\*")
    print("")
    print(P+"                E N T E R 1 - 9 to:                 ")
    print("")
    print(B+" - 1 to view entire collection - ")
    print("")
    print(G+" - 2 to search By film title - ")
    print("")
    print(O+" - 3 to see total number of games in collection - ")
    print("")
    print(P+" - 4 to search by film genre (case sensitive) - ")
    print("")
    print(W+" - 5 to search films by release year - ")
    print("")
    print(B+" - 6 to Graph Genre popularity by amount of films in collection - ")
    print("")
    print(G+" - 7 to Graph Video Games by System - ")
    print("")
    print(O+" - 8 see total amount of LaserDiscs in collection - ")
    print("")
    print(R+" - - 0 to QUIT - - ")
    print(W+"___________________________________________________")
    print("")

menu()
option = int(input("Enter your choice: "))

# Master Loop Requirement
while option != 0:
    if option == 1:
        
        with open('collection.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            #next(csv_reader)
            for line in csv_reader:
                print(line[1])
                pass
        
        print ("You Chose to view the entire collection.")

    elif option == 2:
        print()
        print("Seach is case sensitive! ")
        print()

        df = pd.read_csv('collection.csv')

        title = df[(df['Title'] == input("Search for a Title: "))]

        print((title))

    elif option == 3:

        with open("games.csv") as f:
            lines = sum(1 for line in f)
            line_number = random.randrange(lines)
        print("")
        print("There are " + str(lines) + " Videogames in this n.")

    elif option == 4:
        print()
        print("Please choose from the following, remember, they're case sensitive!")
        print()
        print("Action - Anime - Comedy - Drama - Family - Holiday - Romance ")
        print() 
        df = pd.read_csv('collection.csv')

        genre = df[(df['Genre'] == input("Search for a genre: "))]
        print((genre))
    
    elif option == 5:
        print()
        print("1900-1999, these are Laserdiscs afterall...")
        print()
        df = pd.read_csv('collection.csv')

        release = df[(df['Release'] == input("Search for a release year: "))]

        print((release))
    
    elif option == 6:
       exec(open('gmz.py').read())

    elif option == 7:
        exec(open('gamestash.py').read())
    
    elif option == 8:
        with open("collection.csv") as f:
            lines = sum(1 for line in f)
            line_number = random.randrange(lines)
        print()
        print("There are " + str(lines) + " LaserDiscs in this collection.")
        print()
    
    else:
        print()
        print("???????????????????")
        print("")
        print(R+"Not an option hoss!")

    print()
    menu()
    option = int(input("Enter your choice: "))

print("")
print(G+"Thanks for checking it out, PEACE! ")
print("")