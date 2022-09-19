import json

#Convert TSV file to JSON file
def convert(input_file, output_file):

    #Get the titles
    file = open(input_file, 'r', encoding='utf-8')
    first_line = file.readline()
    titles = []
    for title in first_line.split('\t'):
        titles.append(title.strip())
    result = []
    
    #Get the dictionaries storing the document
    for line in file:
        row = {}
        for title, value in zip(titles, line.split('\t')):
            if (value.strip() == u'\\N'):
                value = 'NULL'
                if ((title == 'primaryProfession') or (title == 'knownForTitles') or (title == 'genres') or (title == 'characters')):
                    row[title] = ['NULL']
                else:
                    row[title] = 'NULL'
            elif ((title == 'primaryProfession') or (title == 'knownForTitles') or (title == 'genres')):
                row[title] = value.strip().split(',')
            elif (title == 'characters'):
                items = value[1:-1]
                items = items.split(',')
                for index in range(len(items)):
                    items[index] = items[index][1:-1]
                row[title] = items
            else:
                row[title] = value.strip()
        result.append(row)
    
    #Add the dictionaries to the JSON file
    with open(output_file, 'w', encoding='utf-8') as output_file:
        for row in result:
            output_file.write(json.dumps(row))
            output_file.write('\n')
    
def main():
    
    for input_file, output_file in [['name.basics.tsv', 'name.basics.json'], ['title.basics.tsv', 'title.basics.json'], 
                                    ['title.principals.tsv', 'title.principals.json'], ['title.ratings.tsv', 'title.ratings.json']]:
        convert(input_file, output_file)

if __name__ == "__main__":
    main()