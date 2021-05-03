from bs4 import BeautifulSoup
from urllib.request import urlopen
import string
import sqlite3

# Uncomment additional lines to see all output from entire collection of names.
url_list = [
    'https://www.behindthename.com/names/letter/a',
    'https://www.behindthename.com/names/letter/a/2',
    'https://www.behindthename.com/names/letter/a/3',
    'https://www.behindthename.com/names/letter/a/4',
    'https://www.behindthename.com/names/letter/a/5',
    'https://www.behindthename.com/names/letter/a/6',
    'https://www.behindthename.com/names/letter/a/7',
    'https://www.behindthename.com/names/letter/a/8',
    'https://www.behindthename.com/names/letter/a/9',
    'https://www.behindthename.com/names/letter/b',
    'https://www.behindthename.com/names/letter/b/2',
    'https://www.behindthename.com/names/letter/b/3',
    'https://www.behindthename.com/names/letter/b/4',
    'https://www.behindthename.com/names/letter/c',
    'https://www.behindthename.com/names/letter/c/2',
    'https://www.behindthename.com/names/letter/c/3',
    'https://www.behindthename.com/names/letter/c/4',
    'https://www.behindthename.com/names/letter/d',
    'https://www.behindthename.com/names/letter/d/2',
    'https://www.behindthename.com/names/letter/d/3',
    'https://www.behindthename.com/names/letter/d/4',
    'https://www.behindthename.com/names/letter/e',
    'https://www.behindthename.com/names/letter/e/2',
    'https://www.behindthename.com/names/letter/e/3',
    'https://www.behindthename.com/names/letter/e/4',
    'https://www.behindthename.com/names/letter/f',
    'https://www.behindthename.com/names/letter/f/2',
    'https://www.behindthename.com/names/letter/f/3',
    'https://www.behindthename.com/names/letter/g',
    'https://www.behindthename.com/names/letter/g/2',
    'https://www.behindthename.com/names/letter/g/3',
    'https://www.behindthename.com/names/letter/g/4',
    'https://www.behindthename.com/names/letter/h',
    'https://www.behindthename.com/names/letter/h/2',
    'https://www.behindthename.com/names/letter/h/3',
    'https://www.behindthename.com/names/letter/h/4',
    'https://www.behindthename.com/names/letter/i',
    'https://www.behindthename.com/names/letter/i/2',
    'https://www.behindthename.com/names/letter/i/3',
    'https://www.behindthename.com/names/letter/j',
    'https://www.behindthename.com/names/letter/j/2',
    'https://www.behindthename.com/names/letter/j/3',
    'https://www.behindthename.com/names/letter/j/4',
    'https://www.behindthename.com/names/letter/k',
    'https://www.behindthename.com/names/letter/k/2',
    'https://www.behindthename.com/names/letter/k/3',
    'https://www.behindthename.com/names/letter/k/4',
    'https://www.behindthename.com/names/letter/l',
    'https://www.behindthename.com/names/letter/l/2',
    'https://www.behindthename.com/names/letter/l/3',
    'https://www.behindthename.com/names/letter/l/4',
    'https://www.behindthename.com/names/letter/m',
    'https://www.behindthename.com/names/letter/m/2',
    'https://www.behindthename.com/names/letter/m/3',
    'https://www.behindthename.com/names/letter/m/4',
    'https://www.behindthename.com/names/letter/m/5',
    'https://www.behindthename.com/names/letter/m/6',
    'https://www.behindthename.com/names/letter/m/7',
    'https://www.behindthename.com/names/letter/n',
    'https://www.behindthename.com/names/letter/n/2',
    'https://www.behindthename.com/names/letter/n/3',
    'https://www.behindthename.com/names/letter/o',
    'https://www.behindthename.com/names/letter/o/2',
    'https://www.behindthename.com/names/letter/p',
    'https://www.behindthename.com/names/letter/p/2',
    'https://www.behindthename.com/names/letter/p/3',
    'https://www.behindthename.com/names/letter/q',
    'https://www.behindthename.com/names/letter/r',
    'https://www.behindthename.com/names/letter/r/2',
    'https://www.behindthename.com/names/letter/r/3',
    'https://www.behindthename.com/names/letter/r/4',
    'https://www.behindthename.com/names/letter/s',
    'https://www.behindthename.com/names/letter/s/2',
    'https://www.behindthename.com/names/letter/s/3',
    'https://www.behindthename.com/names/letter/s/4',
    'https://www.behindthename.com/names/letter/s/5',
    'https://www.behindthename.com/names/letter/s/6',
    'https://www.behindthename.com/names/letter/s/7',
    'https://www.behindthename.com/names/letter/t',
    'https://www.behindthename.com/names/letter/t/2',
    'https://www.behindthename.com/names/letter/t/3',
    'https://www.behindthename.com/names/letter/t/4',
    'https://www.behindthename.com/names/letter/u',
    'https://www.behindthename.com/names/letter/v',
    'https://www.behindthename.com/names/letter/v/2',
    'https://www.behindthename.com/names/letter/v/3',
    'https://www.behindthename.com/names/letter/w',
    'https://www.behindthename.com/names/letter/w/2',
    'https://www.behindthename.com/names/letter/x',
    'https://www.behindthename.com/names/letter/y',
    'https://www.behindthename.com/names/letter/y/2',
    'https://www.behindthename.com/names/letter/z',
    'https://www.behindthename.com/names/letter/z/2'
    ]

total_name_data = []
j=0
for url in url_list:
    page = urlopen(url_list[j])
    html = page.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    link_name_data = []
    
    for link in soup.find_all('span', class_='listname'):
        name_data = {'baby_name': link.text}
        link_name_data.append(name_data)

    i = 0
    for link in soup.find_all('span', class_='listgender'):
        link_name_data[i]['gender'] = link.string
        i += 1

    i = 0
    for link in soup.find_all('span', class_='listusage'):
        link_name_data[i]['usage'] = link.text
        i += 1

    j+=1
    total_name_data.append(link_name_data)

#print(total_name_data[0])

conn = sqlite3.connect('db.sqlite3')
curs = conn.cursor()

curs.execute('DROP TABLE IF EXISTS users_babynames;')
curs.execute('''CREATE TABLE IF NOT EXISTS users_babynames(
                id SERIAL PRIMARY KEY,
                baby_name varchar(100),
                gender varchar(6) NULL,
                usage varchar(150)
                );''')

k = 0
while k < len(url_list):
    for name_data in total_name_data[k]:
        curs.execute('INSERT INTO users_babynames (baby_name, gender, usage) VALUES ( :baby_name, :gender, :usage);', name_data)
        #print(name_data)
    k += 1

# curs.execute('select * from users_babynames')
# r = curs.fetchall()

# print(tuple(r))

conn.commit()
curs.close()