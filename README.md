# Film & Videogame Libary Console App

# Intro:

A console application that allows users to search, graph and read CSV dataframes. Uses both Pandas, matplotlib and Python3's baked in CSV search feature. Data for the project was pulled from lddb.com and refactored in order to work well with this project. I was in need of a searching software that wasn't hosted online so using Python to accomplish this was perfect. 

# How to run:

Users must have Pandas & matplotlib installed if not already on machine. Can be installed with pip (or your preferred package manager) via [pip install pandas] & [pip install matplotlib]

Users simply need to navigate to menu.py, and run application via 'python menu.py' (or 'python3 menu.py' if their system requires it).

application is hosted at  https://github.com/dd1x0n/ld_collection.git

# Project Requirements:

> Implement a “master loop” console application where the user can repeatedly enter commands/perform actions, including choosing to exit the program 

   Master loop is seen in menu.py.

> Create a class, then create at least one object of that class and populate it with data. The value of at least one object must be used somewhere in your code 

   Classes are used throughout the program, value generated and parsed from both .csv files are used to properly graph data. 

> Create a dictionary or list, populate it with several values, retrieve at least one value, and use it in your program 

   This is used in gmz.py & gamestash.py to count the occurrences of a particular genre and system in order to build two graphs. 

> Read data from an external file, such as text, JSON, CSV, etc and use that data in your application 

   This application reads from two .csv files, collection.csv & games.csv. 

> Analyze text and display information about it (ex: how many words in a paragraph 
    
   Program counts the total amount of media in both .csv collections. 

> Visualize data in a graph, chart, or other visual representation of data 

   Two bar charts are used with data populated from both .csv files to visualize amount of a particular genre of film and video game system with the most games. 

> Use pandas, matplotlib, and/or numpy to perform a data analysis project. Ingest 2 or more pieces of data, analyze that data in some manner, and display a new result to a graph, chart, or other display 

   This is seen in gamestash.py gmz.py &  feature using matplotlib to display data from the CSV files and graph them. 


# Future Additions:

-Optimized search
-Search by ref number/other parameters 
-Nested menus (ran out of time)
-API connection to Price Charting
-Export Feature 

           Built w/ Python 3.9 on macOS & OpenBSD for Code Lou Spring 2021.
