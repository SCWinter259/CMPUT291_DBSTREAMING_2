# About

This is the Mini-project 2 of CMPUT 291, University of Alberta, Winter 2022. This is a model of a movie streaming service, using Python and MongoDB.

This Mini-project was done in cooperation with Dinh Dang Viet Anh (dangviet@ualberta.ca)

# Project Specifications

## Task

You are given four tab-separated files named as `name.basics.tsv`, `title.basics.tsv`, `title.principals.tsv`, and `title.ratings.tsv`, which you will convert to `json` before loading them into MongoDB. The data is obtained from IMDb and includes information about movies, principal cast/crew members, and ratings. More information about these files, their fieldsas well as larger files is available
at [imdb.com/interfaces](imdb.com/interfaces). Your job is to create MongoDB collections, following Phase 1, and support searches and updates in Phases 2.

## Phase 1: Building a document store

For this part, you will write 2 programs. One program, named `tsv-2-json.py`, will read the four tsv files in the current directory and convert them to json files. The file names should remain the same except the extension which will change to json. the columns `primaryProfession`, `knownForTitles`, `genres` and `characters` are of type array and should be represented as nested arrays in json.

Another program, named `load-json.py`, will take those four json files in the current directory and constructs a MongoDB collection for each. Your program will take as input a port number under which the MongoDB server is running, will connect to the server and will create a database named `291db` (if it does not exist). Your program then will create four collections named `name_basics`, `title_basics`, `title_principals` and `title_ratings` respectively for `name.basics.json`, `title.basics.json`, `title.principals.json`, and `title.ratings.json`. If those collections exist, your program should drop them and create new collections. Your program for this phase ends after building collections.

Note that none of the files can be fully loaded into memory. The input files are expected to be too large to fit in memory and you can only process them as one-row-at-a-time.

## Phase 2: Operating on the document store

Write a program that supports the following operations on the MongoDB database created in Phase 1. Your program will take as input a port number under which the MongoDB server is running, and will connect to a database named `291db` on the server.

Next, users should be able to perform the following tasks:

1. Search for titles: The user should be able to provide one or more keywords, and the system should retrieve all titles that match all those keywords (not any of them, but matching all of them). A keyword matches if it appears in the primaryTitle field (the matches should be case-insensitive). A keyword also matches if it has the same value as the year field. For each matching title, display all the fields in `title_basics`. The user should be able to select a title to see the rating, the number of votes, the names of cast/crew members and their characters (if any).
2. Search for genres: The user should be able to provide a genre and a minimum vote count and see all titles under the provided genre (again case-insensive match) that have the given number of votes or more. The result should be sorted based on the average rating with the highest rating on top.
3. Search for cast/crew members: the user should be able to provide a cast/crew member name and see all professions of the member and for each title the member had a job, the primary title, the job and character (if any). Matching of the member name should be case-insensitive.
4. Add a movie: The user should be able to add a row to `title_basics` by providing a unique id, a title, a start year, a running time and a list of genres. Both the primary title and the original titile will be set to the provided title, the title type is set to `movie` and `isAdult` and `endYear` are set to `Null` (denoted as `\N`).
5. Add a cast/crew member: The user should be able to add a row to `title_principals` by providing a cast/crew member id, a title id, and a category. The provided title and person ids should exist in `name_basics` and `title_basics` respectively (otherwise, proper messages should be given), the ordering should be set to the largest ordering listed for the title plus one (or 1 if the title is not listed in `title_principals`) and any other field that is not provided (including job and characters) set to Null.

After each action, the user should be able to return to the main menu for further operations. There should be also an option to end the program.