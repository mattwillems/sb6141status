# import libraries
import urllib
import pandas as pd
import re
from tabulate import tabulate
from bs4 import BeautifulSoup

# specify the url
quote_page = 'http://192.168.100.1/cmSignalData.htm'

# query the website and return the html to the variable 'page'
page = urllib.request(quote_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

# grab downstream table
table = soup.find_all('table') # Grab the first table

#read tables into dataframe df
df = pd.read_html(str(table))

############################
# Downstream, table 1
############################
#down is element 0 in dataframe list
down = df[0]
down.at[5, 0] = 'Power Level'
down.at[5, 1] = ''
down.drop(down[0].tail(2).index,inplace=True) # drop last n rows
down.drop(down.head(1).index,inplace=True)
down.drop(down.index[3],inplace=True)

count = 1
max = len(down.columns) - 1
while count < max:
    old = count
    new = count + 1
    count += 1
    down.at[5,old] = down.at[5,new]

down.columns = ['a','b','c','d','e','f','g','h','i','j']
down = down.drop(columns=['j'],axis=1)

#print( tabulate(down, headers='keys', tablefmt='psql' ))
############################
# Downstream, table 2
############################

down2 = df[4]
down2.drop(down2.head(1).index,inplace=True)
down2.drop(down2.index[0],inplace=True)
down2.columns = ['a','b','c','d','e','f','g','h','i']
#print(tabulate(down2, headers='keys', tablefmt='psql'))

############################
# Downstream, combined table
############################

down = pd.concat([down, down2], ignore_index=True)
down = down.replace(" dB", "", regex=True)
down = down.replace("mV", "", regex=True)
down = down.replace(" Hz", "", regex=True)
down['a'] = ['Channel ID','Frequency','SnR','Power Level','Unerrored','Correctable','Uncorrectable']
down.set_index('a', inplace=True)
down['c'] = down['c'].astype(int)
down['d'] = down['d'].astype(int)
down['e'] = down['e'].astype(int)
down['f'] = down['f'].astype(int)
down['g'] = down['g'].astype(int)
down['h'] = down['h'].astype(int)
down['i'] = down['i'].astype(int)
down.b = pd.to_numeric(down.b, errors='coerce')
down.c = pd.to_numeric(down.c, errors='coerce')

#print final downstream table
print( tabulate(down, headers='keys', tablefmt='psql' ))

############################
# Upstream
############################
up = df[3]
up.set_index(0, inplace=True)
up.drop(up.head(1).index,inplace=True)
up.drop(['Upstream Modulation','Symbol Rate'],inplace=True)

print(tabulate(up, headers='keys', tablefmt='psql'))

