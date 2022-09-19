import json
from pymongo import MongoClient

#Connect to port number
def connect():
    
    while (1):
        try:
            port_number = input('Please enter a port number: ')
            client = MongoClient(port_number)
        except:
            print('Invalid port number. ')
        else:
            return client

def main():
    
    client = connect()
    database = client['291db']
        
    #Create the collection if not existed and insert documents
    for collection, file in [['name_basics', 'name.basics.json'], ['title_basics', 'title.basics.json'], 
                             ['title_principals', 'title.principals.json'], ['title_ratings', 'title.ratings.json']]:
        
        #Reset/Create the collections
        if (collection not in database.list_collection_names()):
            database[collection]
        else:
            if (collection == 'name_basics'):
                database.name_basics.delete_many({})
            elif (collection == 'title_basics'):
                database.title_basics.delete_many({})
            elif (collection == 'title_principals'):
                database.title_principals.delete_many({})
            else:   
                database.title_ratings.delete_many({})
                
        #Add documents to the collections
        f = open(file, 'r')
        content = f.readline()
        documents = []
        while (content):
            if (len(documents) < 1000):
                documents.append(json.loads(content))
            else:
                database[collection].insert_many(documents)
                documents = [json.loads(content)]
            content = f.readline()
        database[collection].insert_many(documents)
        f.close()
        
if __name__ == "__main__":
    main()