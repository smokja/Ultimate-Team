from bs4 import BeautifulSoup
import urllib.request
import csv
import json

# gets the information for a set of users
# returns all users split into 2 sections: user_list and didnt_work
# didnt_work will be looped until it has no rows
def get_information(values):
    counter = 0
    user_list = dict()
    didnt_work = dict()
    for val in values:
        counter += 1
        position = '('+str(counter)+'/'+str(len(values))+')'
        try:
            user_list[val] = get_raw_data(values[val])
            print('succes, '+ position)
        except:
            didnt_work[val] = values[val]
            print('fail '+ position)
    return user_list, didnt_work

# makes a get request and parses the html to a dictionary
def get_raw_data(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser') 
    table_data = [[cell.text for cell in row('th') + row('td')]
                             for row in soup('tr')]
   
    # register keys
    keys = table_data[1]
     
    # loop throguh all elements and connect key to data
    information_table = dict()
    data_row = table_data[len(table_data) - 1]
    
    for y in range (len(data_row)):
        key = keys[y]
        value = data_row[y]
        information_table[key] = value
    return information_table


def write_data_to_file(result):
    with open('data.json', 'w') as outfile:
        json.dump(result, outfile)

def load_data():  
    result = list()
    values = dict()
    didnt_work = dict()
    
    # read the player list so we are able to make the request links
    with open('players_search_list.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in list(reader):
            number = row[0]
            new_name = row[1].replace(' ', '-')
            link = 'https://fbref.com/en/players/'+number+'/'+new_name
            values[number+new_name] = link
            
    
    values = {k: values[k] for k in list(values)[:5]}
    didnt_work = values
    last_didnt_work_count = 0
    
    # as long as didnt_work's length changes from iteration to iteration, get_information will be called
    while True:
        user_list, didnt_work = get_information(didnt_work)
        
        result.append(user_list)
        if len(didnt_work) == 0 or len(didnt_work) == last_didnt_work_count:
            break
        last_didnt_work_count = len(didnt_work)
        
    # write results to json
    write_data_to_file(result)
        

load_data()


