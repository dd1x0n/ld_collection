# Film & Videogame Libary Console App

# Intro:

> A console application that allows users to search, graph and read CSV dataframes. Uses both Pandas and Python3 baked in CSV search feature.  

# How to run:

> Users must have Pandas installed if not already on machine. Can be installed via [pip install pandas]

> Users simply need to navigate to menu.py, and run application via 'python menu.py' (or 'python3 menu.py' if their system requires it).

> application is hosted at  https://github.com/dd1x0n/ld_collection/tree/main

# Project Requirements:

> Implement a “master loop” console application where the user can repeatedly enter commands/perform actions, including choosing to exit the program - master loop is in the main menu of program.

> Create a class, then create at least one object of that class and populate it with data. The value of at least one object must be used somewhere in your code - classes are used thought the program, value generated and parsed from both .csv files are used in order to properly graph data. 

> Create a dictionary or list, populate it with several values, retrieve at least one value, and use it in your program - This is used in gmz.py & gamestash.py to count the occurrences of a particular genre and system in order to build two graphs. 

> Read data from an external file, such as text, JSON, CSV, etc and use that data in your application - this application read from two .csv files, collection.csv & games.csv. 

> Analyze text and display information about it (ex: how many words in a paragraph - program counts the total amount of media in both .csv collections. 

> Visualize data in a graph, chart, or other visual representation of data - two Bar Charts are used with data populated from both .csv files to visualize amount of a particular genre of film and video game system with the most games. 

> Use pandas, matplotlib, and/or numpy to perform a data analysis project. Ingest 2 or more pieces of data, analyze that data in some manner, and display a new result to a graph, chart, or other display - This is seen in gamestash.py gmz.py &  feature using matplotlib to display data from the CSV files and graph them. 


# Future Additions:

> Optimized search
> Search by ref number/other parameters 
> Nested menus (ran out of time)
> API connection to Price Charting
> Export Feature 

Built in Python 3.9 w/ macOS & OpenBSD in 2021 for Code Louisville Python capstone project.