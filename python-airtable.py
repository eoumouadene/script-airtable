#!/usr/bin/env python3


import sys
import os
import requests
import json
from collections import OrderedDict

print("This has been made exclusively for Laurent Michaelis")

if 4 < len(sys.argv) < 7 :
    print("This program will take the first 100 records of the specified table")
else:
    print("WRONG INPUT")
    print("You have to add 4 arguments : api_key, base_id, table_name, name_of_the_file.csv")
    print("If you need to specify the view : api_key, base_id, table_name, view, name_of_the_file.csv")
    print("The file will be created inside this directory : " + os.path.dirname(os.path.abspath(__file__)))
    
    sys.exit()

ADDRESS = "https://api.airtable.com/v0/"
KEY = sys.argv[1]
BASE = sys.argv[2]
TABLE = sys.argv[3]
try: 
    if(len(sys.argv) == 6):
        FILE = sys.argv[5]
        VIEW = sys.argv[4]
        data = requests.get(ADDRESS + BASE + '/' + TABLE + '?api_key=' + KEY + '&view=' + VIEW)
    
    else: 
        FILE = sys.argv[4]
        data = requests.get(ADDRESS + BASE + '/' + TABLE + '?api_key=' + KEY)
    if "200" not in str(data):
        print("ERROR : REQUEST NOT SUPPORTED")
        sys.exit()
except:
    print("ERROR : ARGUMENTS INVALID")
    sys.exit()

def replace_all(text):
    ret = text + ''
    
    dic = OrderedDict([("\n", "; "), (",", ";"),("\r",""), ("[\'", ""), 
        ("\']", ""),("\'#","#"),("\';",";"),("; \'","; "), ("; #", " #"),("\"", "")])
    for i, j in dic.items():
        ret = ret.replace(i, j)
    
    if "OrderedDict" in ret or "NaN" in ret:
        ret = ''
    '''
    try:
        f = float(ret)
        if f.is_integer():
            ret = str(int(f))
        else:
            ret = str(round(f, 2))
    except:
        pass
    '''
    return '\"'+ret+'\"'

r = json.loads(data.text, object_pairs_hook=OrderedDict)
#print(r)
head_int = 0
doc = {}

for key_record in r:     
    for record in r[key_record]:
        for info in record:
            if info in "fields":
                for value in record[info]:
                    if replace_all(value) not in doc:
                        doc[ replace_all(value) ] = head_int 
                        head_int += 1
                        #print(head_int)                       
                        #print(replace_all(value) + " " + str(head_int) + " " + str(doc[replace_all(value)]))                       

records_list = []





for key_record in r:     
    for record in r[key_record]:
        for info in record:
            if info in "fields":
                line = [''] * head_int
                for value in record[info]:
                    #print( str(head_int) + str(doc[ replace_all(value) ]))
                    line[ doc[ replace_all(value) ] ] =   replace_all(str(record[info][value]))                        
                records_list.append(line)

#sys.exit()

with open(FILE,"w+", encoding='utf-16') as f:
    #print("-------")
    f.write(",".join((k) for k in doc) + "\n")
    #print( ",".join((k) for k in doc) )
    #print('\n'.join(",".join(str(line[k]) for k in range(head_int) )+"\n" for line in records_list))
    f.write('\n'.join(",".join(str(line[k]) for k in range(head_int) ) for line in records_list))

f.close() 

print("file created")

