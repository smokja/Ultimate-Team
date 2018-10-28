# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import urllib.request
import csv
import json
import aiohttp
import async_timeout
import asyncio
import time
import os

START = time.monotonic()

raw_data = dict()
failed = list()
counter = 0
length = 0
class RateLimiter:
    RATE = 1  # three request per second
    MAX_TOKENS = 1

    def __init__(self, client):
        self.client = client
        self.tokens = self.MAX_TOKENS
        self.updated_at = time.monotonic()

    async def get(self, *args, **kwargs):
        await self.wait_for_token()
        now = time.monotonic() - START
        # print(f'{now:.0f}s: ask {args[0]}')
        return self.client.get(*args, **kwargs)

    async def wait_for_token(self):
        while self.tokens < 1:
            self.add_new_tokens()
            await asyncio.sleep(0.1)
        self.tokens -= 1

    def add_new_tokens(self):
        now = time.monotonic()
        time_since_update = now - self.updated_at
        new_tokens = time_since_update * self.RATE
        if self.tokens + new_tokens >= 1:
            self.tokens = min(self.tokens + new_tokens, self.MAX_TOKENS)
            self.updated_at = now


# read the player list so we are able to make the request links
def get_player_addresses():
    values = dict()
    with open('players_search_list.csv', newline='', encoding='utf-8' ) as csvfile:
        print(csvfile)
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in list(reader):
            number = row[0]
            new_name = row[1].replace(' ', '-')
            link = 'https://fbref.com/en/players/'+number+'/'+new_name
            values[link] = number + new_name
        return values

# makes a get request and parses the html to a dictionary
async def get_raw_data(session, url, name): 
    global counter
    fail = False
    try:
        async with await session.get(url) as response:
            html = await response.read()
            soup = BeautifulSoup(html, 'html.parser') 
            table_data = [[cell.text for cell in row('th') + row('td')]
                             for row in soup('tr')]
            # register keys
            keys = table_data[1]
            information_table = dict()
            
            # get the years he played
            first_age = table_data[2][1]
            last_age = table_data[len(table_data) - 2][1]
            length_of_play = int(last_age) - int(first_age)
            information_table['years_served'] = length_of_play

            # the last row has the overall stats that are needed for evaluation
            data_row = table_data[len(table_data) - 1]
            # loop throguh all elements and connect key to data
            for y in range (len(data_row)):
                key = keys[y]
                value = data_row[y]
                information_table[key] = value

            raw_data[name] = information_table
            fail = False

            as_dict = dict()
            as_dict[name] = information_table
            write_data_to_file(as_dict)
            return await response.release()
    except:
        fail = True
        failed.append(url) 
        write_fail(url)
    finally:
        counter = counter + 1
        if (fail):
            print('(%s/%s) error %s'%(counter, length, url))
        else:
            print('(%s/%s) success %s'%(counter, length, url))

def write_fail(data):
    with open('failed.json', 'a') as f:
        json.dump(data, f)
        f.write(os.linesep)

def write_data_to_file(data):
    with open('players.json', 'a') as f:
        json.dump(data, f)
        f.write(os.linesep)
   
async def main(loop):
    global length  
    urls = get_player_addresses()
    length = len(urls)
    async with aiohttp.ClientSession(loop=loop) as session:
        session = RateLimiter(session)
        tasks = [get_raw_data(session, url, name) for url, name in urls.items()]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
