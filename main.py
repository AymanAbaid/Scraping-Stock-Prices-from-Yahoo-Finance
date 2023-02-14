import pandas as pd
import requests
from bs4 import BeautifulSoup

base_url = 'https://finance.yahoo.com'
table_names = ['crypto','trending-tickers','most-active','gainers']
col_list=[10,8,5,8]

def get_table(ncol,url):
    col_names=[]
    # Create request object 
    page = requests.get(url).text

    # Creating BeautifulSoup object
    soup = BeautifulSoup(page, 'html.parser')

    # Verifying tables and their classes
    table = soup.find('table')


    for row in table.thead.find_all('tr'):
        table_header=row.find_all('th')
        for i in range(0,ncol):
            col_names.append(table_header[i].text)
    
    df = pd.DataFrame(columns=col_names)
    for row in table.tbody.find_all('tr'):    
        # Find all data for each column
        row_content = row.find_all('td')
        values=[]
        #Store each cell value for a row in values list
        for i in range(0,ncol):
            values.append(row_content[i].text)    
        # append value list as row in data frame   
        df=df.append(pd.Series(values, index=col_names),ignore_index=True)
    return df


for i in range(0,len(table_names)-1):
    url = base_url+'/' + table_names[i]
    df = get_table(col_list[i],url)
    file_name = table_names[i] +".csv"
    df.to_csv(file_name,index = False)