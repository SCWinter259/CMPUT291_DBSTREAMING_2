from pymongo import MongoClient
from pprint import pprint

#Connect to port number
def connect():
    
    while (1):
        try:
            port_number = input('Please enter a port number: ')
            client = MongoClient(port_number)
        except:
            print('Invalid port number. ')
        else:
            return client['291db']

#Main interface
def interface():
    
    print('Please enter a number corresponding to an option: ')
    print('1. Search for titles.')
    print('2. Search for genres. ')
    print('3. Search for cast/crew members. ')
    print('4. Add a movie. ')
    print('5. Add a cast/crew member. ')
    print('6. Exit. ')
    while (1):
        try:
            option = int(input('Option: '))
        except:
            print('Invalid option number. ')
        else:
            if ((option >= 1) and (option <= 6)):
                return option

#Prompt for either an input or stop command or go back command
def go_back(prompt, input_type, input_name, stop, lower_bound, upper_bound):
    
    while (1):
        
        #Prompt for input
        try:
            input_string = input(prompt).strip()
            if (input_type == 'int'):
                input_number = int(input_string)
                
        except:
            
            #Non-string input error
            if (input_type != 'string'):
                if (input_string == 'back'):
                    return None , 0, 1
                if (stop and (input_string == 'stop')):
                    return None, 1, 0
                else:
                    print('Invalid input. ')
                    
            #String input error       
            else:
                print('Invalid input. ')
                
        else:
            confirm = 0
            
            #Non-string input 
            if (input_type != 'string'):
                if (lower_bound == None):
                    if ((upper_bound == None) or (input_number <= upper_bound)):
                        return input_number, 0, 0
                    else:
                        print('Number inputted too large. ')
                else:
                    if (input_number >= lower_bound):
                        if ((upper_bound == None) or (input_number <= upper_bound)):
                            return input_number, 0, 0
                        else:
                            print('Number inputted too large. ')
                    else:
                        print('Number inputted too small. ')
                        
            #Stop or go back 
            elif (input_string == 'back'):
                while (not confirm):
                    try: 
                        go_back = input('Enter "back" to go back or anything else to use this {}: '.format(input_name))
                    except:
                        print("Invalid input. ")
                    else:
                        if (go_back == 'back'):
                            return None, 0, 1
                        else:
                            return input_string, 0, 0
            elif (input_string == 'stop'):
                if (stop):
                    while (not confirm):
                        try: 
                            stop = input('Enter "stop" to stop or anything else to use this {}: '.format(input_name))
                        except:
                            print("Invalid input. ")
                        else:
                            if (stop == 'stop'):
                                return None, 1, 0
                            else:
                                return input_string, 0, 0
                else:
                    return input_string, 0, 0
            
            #String input
            else:
                return input_string, 0, 0

#Search for titles task            
def task_1(db):
    
    #Add keywords
    keywords = []
    keyword_added = 0
    while (not keyword_added):
        keyword, stop, back = go_back('Please enter a keyword or "stop" to stop adding or "back" to go back: ', 'string', 
                                      'keyword', 1, None, None)
        
        #Go back to the main interface
        if (back):
            print('Redirected to the main interface... ')
            return
        
        #Stop adding keywords
        elif (stop):
            if (len(keywords) == 0):
                print('You have not added any keywords. ')
            else:
                keyword_added = 1
        
        #Keyword added successfully
        #Turn all keywords added into lowercase
        else:
            if (keyword.lower() in keywords):
                print('You have already added this keyword')
            else:
                keywords.append(keyword.lower())
                print('Keyword added. ')
    
    #Search for titles
    title_basics = db["title_basics"]

    results = _search_titles(db, keywords)
    tconst_list = []

    titles = title_basics.find({"primaryTitle":{'$in':results}})
    for title in titles:
        tconst_list.append(title["tconst"])
        pprint(title)

    if tconst_list:
        while 1:
            choice = input("Please enter the exact tconst of a movie above to view more information: ")
            if choice not in tconst_list:
                print("The choice is not listed above!")
            else:
                _display_info(db, choice)
                go_out = input("Press any key to go back to the main interface: ")
                return
    else:
        print("The search gives no result!")
        return

def _search_titles(db, keywords):
    '''
    Casper
    This is a support function for task_1
    This function takes in a list of keywords and
    returns a list of titles fitting task_2 spec
    '''
    title_basics = db["title_basics"]
    title_basics.create_index([('primaryTitle', 'text')])

    result_list = []
    temp1 = []
    temp2 = []
    temp3 = []

    for keyword in keywords:
        if not keyword.isdecimal():
            if not temp1: # first search
                results = title_basics.find({'$text': {'$search':keyword}})
                for result in results:
                    temp1.append(result["tconst"])
            else: # all other searches
                results = title_basics.find({'$and':[{'$text': {'$search':keyword}},
                                            {"tconst":{"$in":temp1}}]})
                for result in results:
                    temp1.append(result["tconst"])
        elif keyword.isdecimal():
            # numerical keywords in titles
            results = title_basics.find({'$text': {'$search':keyword}})
            for result in results:
                temp2.append(result["tconst"])
            # numerical keywords in start years
            results = title_basics.find({"startYear":{'$eq':keyword}})
            for result in results:
                temp3.append(result["tconst"])

    # union of the 3 lists, duplicates removed
    id_list = list(set(temp1 + temp2 + temp3))
    
    # combine titles with the years to perform search on one string
    results = title_basics.find({'tconst': {'$in': id_list}})
    for result in results:
        eliminate = False
        title_year_string = result["primaryTitle"] + ' ' + str(result["startYear"])
        for keyword in keywords:
            if keyword not in title_year_string.lower():
                eliminate = True
                break
        if eliminate == False:
            result_list.append(result["primaryTitle"])

    return result_list

def _display_info(db, choice):
    '''
    Casper
    This is a helper function for task_1
    This function take in a user choice
    and display all related information
    '''
    name_basics = db["name_basics"]
    title_principals = db["title_principals"]
    title_ratings = db["title_ratings"]

    # find the rating and the number of votes
    rates_and_votes = title_ratings.find({'tconst':choice})
    avg_ratings = rates_and_votes[0]["averageRating"]
    num_votes = rates_and_votes[0]["numVotes"]

    # find the casts/crew members ids and their characters
    member_ids = []
    characters = []
    member_ids_cursor = title_principals.find({'tconst':choice})
    for member_id in member_ids_cursor:
        member_ids.append(member_id["nconst"])
        characters.append(member_id["characters"])
    
    print("Extra information for " + choice + ":")
    print("Average ratings: " + avg_ratings)
    print("Number of votes: " + num_votes)
    for i in range(len(member_ids)):
        # find the name of the cast/crew member
        name_cursor = name_basics.find({'nconst':member_ids[i]})
        name = name_cursor[0]["primaryName"]
        print("Cast/crew member: " + name)
        if characters[i][0] != 'NULL':
            characters[i][len(characters[i]) - 1] = characters[i][len(characters[i]) - 1].rstrip("\"")
            print("Characters: ", end="")
            for idx in range(len(characters[i])-1):
                print(characters[i][idx] + ", ", end="")
            print(characters[i][len(characters[i])-1])

#Search for genres task
def task_2(db):
    
    #Prompt for a genre
    genre, stop, back = go_back('Please enter a genre or "back" to go back: ', 'string', 
                                'genre', 0, None, None)
    if (back):
        print('Redirected to the main interface... ')
        return
    genre = genre.lower()
    
    #Prompt for a minimum vote count number
    min_vote_count, stop, back = go_back('Please enter a minimum vote count number or "back" to go back: ', 'int', 
                                         'number', 0, 0, None)
    if (back):
        print('Redirected to the main interface... ')
        return
    
    #Search for genres
    result = {}
    r = []
    ratings = db.title_ratings.aggregate([{"$project": {"tconst": "$tconst",
                                                        "averageRating": {"$toDouble": "$averageRating"}, 
                                                        "numVotes": {"$toInt": "$numVotes"}}},
                                          {"$match": {"numVotes": {"$gte": min_vote_count}}}])
    index = 1
    print('{0:^5}:{1:^11}:{2:^16}'.format("Index", "Title", "Average Rating"))
    for rating in ratings:
        titles = db.title_basics.aggregate([{"$match": {"tconst": rating["tconst"]}}, 
                                            {"$unwind": "$genres"}, 
                                            {"$project": {"tconst": "$tconst", "genres": {"$toLower": "$genres"}}}, 
                                            {"$match": {"genres": genre}}]) 

        for title in titles:
            if (rating["averageRating"] not in result.keys()):
                result[rating["averageRating"]] = [rating["tconst"]]
                r.append(rating["averageRating"])
            else:
                result[rating["averageRating"]].append(rating["tconst"])         
                
    #Display results
    r.sort(reverse= True)
    eindex = 0
    while (eindex < len(r)):
        ts = result[r[eindex]]
        sindex = 0
        while (sindex < len(ts)):        
            print('{0:^5}:{1:^11}:{2:^16}'.format(index, ts[sindex], r[eindex]))
            index+= 1
            sindex+= 1
        eindex+= 1

#Search for cast/crew members task
def task_3(db):
    
    #Prompt for a name
    name, stop, back = go_back('Please enter a cast/crew member name or "back" to go back: ', 'string', 
                               'name', 0, None, None)
    if (back):
        print('Redirected to the main interface... ')
        return
    name = name.lower()
    
    #Display information about the given casts/crew members
    db.name_basics.create_index([("primaryName", 1)])
    casts = db.name_basics.find({"primaryName": name}).collation({"locale": 'en', "strength": 2})
    cast_index = 1
    print('List of casts/crew members: ', end='')
    try:
        casts[0]
    except:
        print('None\nRedirected to the main interface. ')
        return
    print('')
    for cast in casts:
        #Modify primary professions and titles
        professions = cast["primaryProfession"]
        if (professions == ["NULL"]):
            professions = []
        titles = cast["knownForTitles"]
        if (titles == ["NULL"]):
            titles = []
            
        #Display the professions
        print("{0}. {1}: ".format(cast_index, cast["primaryName"]), end= '')
        if (professions == []):
            print('None')
        for index in range(len(professions)):
            print(professions[index], end='')
            if (index < (len(professions) - 1)):
                print(', ', end='')
        print('')
        
        #Display all the titles
        print('This cast/crew member has the following titles: ', end='')
        if (titles == []):
            print('None')
            return
        for index in range(len(titles)):
            print(titles[index], end='')
            if (index < (len(titles) - 1)):
                print(', ', end='')
        print('')

        #Display the primary titles, job and characters for each titles
        if (titles !=  []):
            job_index = 1
            for title in titles:
                jobs = db.title_principals.find({"$and": [{"tconst": title},
                                                          {"nconst": cast["nconst"]}]})
                try:
                    jobs[0]
                except:
                    print('Title {} has no job and characters'.format(title))
                for job in jobs:
                    if (job['job'] != "NULL" or job['characters'] != ["NULL"]):
                        primary_title = db.title_basics.find({"tconst": title})[0]
                        j = job['job']
                        if (j == "NULL"):
                            j = "None"
                        print("{3}.{0}. Primary Title: {1}\n---> Job: {2}\n---> Characters: ".format(job_index, 
                                                                                                primary_title["primaryTitle"], 
                                                                                                j, 
                                                                                                cast_index), 
                                                                                                end='')
                        characters = job["characters"]
                        if (characters == ["NULL"]):
                            print("None")
                        else:
                            for iindex in range(len(characters)):
                                if (iindex != (len(characters) - 1)):
                                    print(characters[iindex], end='')
                                else:
                                    c = characters[iindex][:-1]
                                    print(c, end='')
                                if (iindex < (len(characters) - 1)):
                                    print(', ', end='')
                            print('')
                        job_index+= 1
                    else:
                        print('Title {} has no job and characters. '.format(title))
                    
        cast_index+= 1
    
    return

#Add a movie task
def task_4(db):
    
    #Prompt for a unique id
    unique = 0
    while (not unique):
        tid, stop, back = go_back('Please enter a unique movie id or "back" to go back: ', 'string', 
                                  'id', 0, None, None)
        if (back):
            print('Redirected to the main interface... ')
            return
        
        #Check uniqueness
        existed = 0
        documents = db.title_basics.find({"tconst": tid})
        for document in documents:
            existed+= 1
        if (existed >= 1):
            print('This movie ID is not unique. ')
        else:
            unique = 1
    
    #Prompt for a title
    title, stop, back = go_back('Please enter a title or "back" to go back: ', 'string', 
                                'title', 0, None, None)
    if (back):
        print('Redirected to the main interface... ')
        return
    
    #Prompt for a start year
    syear, stop, back = go_back('Please enter a start year or "back" to go back: ', 'int', 
                                'year', 0, 0, None)
    if (back):
        print('Redirected to the main interface... ')
        return
    
    #Prompt for a running time
    rtime, stop, back = go_back('Please enter a running time or "back" to go back: ', 'int', 
                                'running time', 0, 0, None)
    if (back):
        print('Redirected to the main interface... ')
        return
    
    #Prompt for genres
    genres = []
    genre_added = 0
    while (not genre_added):
        genre, stop, back = go_back('Please enter a genre or "stop" to stop adding or "back" to go back: ', 'string', 
                                    'genre', 1, None, None)
        
        #Go back to the main interface
        if (back):
            print('Redirected to the main interface... ')
            return
        
        #Stop adding keywords
        elif (stop):
            if (len(genres) == 0):
                print('You have not added any genres. ')
            else:
                genre_added = 1
        
        #Keyword added successfully
        else:
            if (genre.lower() in genres):
                print('You have already added this genre. ')
            else:
                genres.append(genre.lower())
                print('Genre added. ')
    
    #Add movie
    db['title_basics'].insert_one({"tconst": tid, 
                                   "titleTpye": "movie", 
                                   "primaryTitle": title, 
                                   "originalTitle": title,
                                   "isAdult": "NULL", 
                                   "startYear": "NULL",
                                   "endYear": syear,
                                   "runtimeMinutes": rtime,
                                   "genres": genres})
    print("Movie added successfully. ")
    return
    
#Add a cast/crew member task
def task_5(db):
    
    #Prompt for a cast/crew member id
    cid, stop, back = go_back('Please enter a cast/crew member ID or "back" to go back: ', 'string', 
                                'ID', 0, None, None)
    if (back):
        print('Redirected to the main interface... ')
        return
    
    #Check existence
    try:
        db.name_basics.find({"nconst": cid})[0]
    except IndexError:
        print('This cast/crew member ID is new. ')
    
    #Prompt for a title id
    tid, stop, back = go_back('Please enter a title ID or "back" to go back: ', 'string', 
                                'ID', 0, None, None)
    if (back):
        print('Redirected to the main interface... ')
        return
    
    #Check existence and compute the ordering
    try:
        db.title_basics.find({"tconst": tid})[0]
    except IndexError:
        print('This title ID is new. ')
    finally:
        ordering = 1
        documents = db.title_principals.aggregate([{"$group": {"_id": "$tconst", "ordering": {"$max": "$ordering"}}},
                                                   {"$match": {"_id": tid}}])
        for document in documents:
            ordering = int(document["ordering"]) + 1
    
    #Prompt for a category
    category, stop, back = go_back('Please enter a category or "stop" to stop adding or "back" to go back: ', 'string', 
                                   'category', 0, None, None)
    
    #Add cast/crew member
    db['title_principals'].insert_one({"tconst": tid,
                                       "ordering": ordering,
                                       "nconst": cid,
                                       "category": category,
                                       "job": "NULL",
                                       "characters": ["NULL"]})
    print("Cast/Crew member added successfully. ")
    return

def main():
    
    db = connect()
    
    while (1):
        
        option = interface()
        
        #Search for titles
        if (option == 1):
            task_1(db)
        
        #Search for genres
        elif (option == 2):
            task_2(db)
        
        #Search for cast/crew members
        elif (option == 3):
            task_3(db)
        
        #Add a movie
        elif (option == 4):
            task_4(db)
        
        #Add a cast/crew member
        elif (option == 5):
            task_5(db)
        
        #Exit
        else:
            print("The program is terminating... ")
            return
        
if __name__ == "__main__":
    
    main()
    '''
    Test for Search for titles (task_1)
    '''
# test for _search_title
# should give at least 'tt0073604
    #keywords = ["lake"]
    #keywords = ["lake", "legend"]
# should give no result
    #keywords = ["lake", "legend", "2000"]
# should give at least 'tt0073604
    #keywords = ["lake", "legend", "1981"]
    #keywords = ["1981", "lake", "legend"]
# should give no result
    #keywords = ["1981", "2012"]
# should give many results
    #keywords = ["1981"]

    #_search_titles(db, keywords)

# combined tests for _display_titles and task_1
# test case: keywords: ["lake", "1981"], ncfeuia, tt2147008
    # task_1(db)

    '''
    Test for Search for genres (task_2)
    '''
    # User provides:
    # Genre: Horror
    # Min vote count: 416
    # task_2(db)

    '''
    Test for Search for cast/crew members (task_3)
    '''
    # cast member name: Will Smith
    #task_3(db)

    '''
    Test for Add a movie (task_4)
    '''
    # User privides:
    # unique id: tt0000000
    # title: test title
    # start year: 2021
    # running time: 000
    # genre: horror, comedy
    # task_4(db)

    '''
    Test for Add a cast/crew member (task_5)
    '''
    # User provides:
    # cast/crew member id: nm0000000, nm0000001
    # title id: tt0000000, tt0073537
    # category: Crime
    # task_5(db)