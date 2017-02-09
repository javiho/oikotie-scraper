# -*- coding: utf-8 -*-
import requests
import json as js_library
import io
import sqlite3
import collections

"""
Kehitysehdotus: estä SQL-injektiohyökkäykset.
"""

def from_site_to_databse():
    all_cards = []
    limit = 24
    for offset in range(0, 3*limit, limit):
        cards_subset = get_set_of_cards(offset=offset, limit=limit)
        all_cards.extend(cards_subset)
    save_cards_to_db(all_cards)

def get_set_of_cards(offset, limit):
    r = requests.get('https://asunnot.oikotie.fi/api/cards?cardType=100&limit=' + str(limit) +
                     '&offset=' + str(offset) +
                     '&sortBy=published_desc')
    as_json = r.json()
    # Card dictionaries are dictionaries with a subset of card attributes. The attributes
    # are converted in the correct from.
    card_dictionaries = get_card_dictionaries(as_json)
    return card_dictionaries

def get_card_dictionaries(json):
    card_count = len(json['cards'])
    #print(card_count)
    cds = []
    for i in range(0, card_count):
        cd = get_card_dict(json, i)
        cds.append(cd)
    return cds

def get_card_dict(json, card_index):
    d = collections.OrderedDict()
    attribute_names = json_attribute_names
    for attribute_name in attribute_names:
        add_attribute_to_dict(d, json, card_index, attribute_name)
    return d
    
def add_attribute_to_dict(card_dict, json, card_index, attribute_name):
    if(attribute_name == 'price'):
        price_str = json['cards'][card_index][attribute_name]
        card_dict[attribute_name] = price_string_to_int(price_str)
    else:
        card_dict[attribute_name] = json['cards'][card_index][attribute_name]
    
def price_string_to_int(price_str):
    #price_str = price_str.replace('\\xa', '')
    #price_str = price_str.replace('€', '')
    #print("replaced: ", price_str)
    only_digits = ''.join(filter(lambda x: x.isdigit(), price_str))
    as_int = int(only_digits)
    #print(as_int)
    return as_int

def save_cards_to_db(card_dicts):
    # New database is created if one doesn't exist.
    conn = sqlite3.connect(db_path)
    print("opened database")
    for card in card_dicts:
        insert_card(conn, card)
    conn.commit()
    conn.close()
    print("database connection closed")
    
def insert_card(conn, card_dict):
    attr_values_list = [val for val in card_dict.values()]
    conn.execute('INSERT INTO apartment(id, description, rooms, room_configuration, price, size, size_lot) ' +
                 'VALUES (?, ?, ?, ?, ?, ?, ?)', attr_values_list)

def json_attr_to_sql_attr(json_attr_name):
    """Returns the name of the database table attribute which corresponds to the
    attribute in card object of the json data.
    """
    for json_attr in json_attribute_names:
        if json_attr_name == json_attr:
            return json_attr_name
    raise Exception("Attribute name not found: " + json_attr_name)   

#r = requests.get('https://api.github.com/events')
apartements_table_attr_names = ['id', 'description', 'rooms', 'room_configuration', 'price', 'size', 'size_lot']
json_attribute_names = ['id', 'description', 'rooms', 'roomConfiguration', 'price', 'size', 'sizeLot']
db_path = 'testdb.db'

conn = sqlite3.connect(db_path)
cursor = conn.execute('SELECT * FROM apartment')
for row in cursor:
    print('id: ', row[0])
    print('description: ', row[1])

#r = requests.get('https://asunnot.oikotie.fi/api/cards?cardType=100&limit=24&offset=0&sortBy=published_desc')
#r.encoding = 'ISO-8859-1'
#print(as_json['cards'][0]['price'])


#print(all_cards)
#print(len(all_cards))
#print("cd count: ", len(card_dictionaries))
#print(card_dictionaries)

############################

#print(as_json)
#dump = json.dumps(as_json, indent=4, ensure_ascii=False)
#print(dump)
#with io.open('test1.txt', 'w', encoding='utf-8') as f:
#    f.write(dump)


##################### KÄYTETTYJÄ KOMENTOJA ############################

#conn.execute('DROP TABLE apartement')

"""conn.execute('''
CREATE TABLE apartment
(id INT PRIMARY KEY NOT NULL,
description NVARCHAR(1000),
rooms INT,
room_configuration NVARCHAR(200),
price INT,
size DECIMAL,
size_lot DECIMAL
);
''')"""

"""conn.execute('''
INSERT INTO apartment(id, description, rooms, room_configuration, price, size, size_lot)
VALUES (999999999, 'Tämä on testikuvaus', 5, '4k, wc', 105000, 85.5, 1200.0)
''')"""
#conn.commit()

"""cursor = conn.execute('SELECT * FROM apartment')
for row in cursor:
    print('id: ', row[0])
    print('description: ', row[1])"""