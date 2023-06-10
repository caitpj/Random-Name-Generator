import time
# start_time = time.time()
import argparse
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import sys
import os.path


def main():
    my_df = fetch_names()
    country = parser().country
    gender = parser().gender

    # If user hasn't selected gener and/or country then randomly assign
    if gender == 'random':
        g = random.choice([0, -1])  
    elif gender == 'male' or gender == 'm':
        g = 0
    elif gender == 'female' or gender == 'f':
        g = -1
    
    if country == 'random':
        country = random.choice(my_df.country.values.tolist())

    my_df = my_df.query(f"country == @country")
    
    try:
        names = my_df['all names'].iloc[g]
    except:
        sys.exit('Invalid country')
    
    name = random.choice(names)
    
    # deal with 'nan' names
    tries = 0
    while name == 'nan' or tries == 20:
        name = random.choice(names)
        tries += 1
 
    print(name)

    # print('My program took', time.time() - start_time, "to run")

def parser():
    """
    Uses argparse to fetch arguments for name creation
    """
    parser = argparse.ArgumentParser(
                    prog='random_name',
                    description='Prints a random popular name from specified country and/or gender')
    
    parser.add_argument('--country', '-c', default='random',
                        help='select country of random name')
    
    parser.add_argument('--gender', '-g', default='random',
                        choices=['male', 'm', 'female', 'f', 'random'],
                        help='select gender of random name')

    args = parser.parse_args()

    return args

def fetch_names():
    """
    Returns a dataframe with names, either from local file or Wikipedia
    """
    # Only fetches names from wikipedia if csv file does not exist or is over a day old
    # if os.path.isfile('names.csv') and time.time() - os.path.getmtime('names.csv') < (60 * 60 * 24):
    if os.path.isfile('names.pkl') and time.time() - os.path.getmtime('names.pkl') < (60 * 60 * 24):
        # df = pd.read_csv('names.csv')
        df = pd.read_pickle('names.pkl')
        # df = df.drop(columns='Unnamed: 0') 
    else:
        df = fetch_names_from_wiki()

    # create list from 'all names'
    df['all names'] = df['all names'].apply(lambda x: x[:].split(', '))

    return df

def fetch_names_from_wiki():
    """
    Returns a dataframe with names from the wikipedia page 'List_of_most_popular_given_names'
    """
    # get the response in the form of html
    wikiurl = "https://en.wikipedia.org/wiki/List_of_most_popular_given_names"
    response = requests.get(wikiurl)

    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    indiatable = soup.find_all('table',{'class':"wikitable"})

    df = pd.read_html(str(indiatable))
    df = pd.concat(df)
    # convert list to dataframe
    df = pd.DataFrame(df)

    # clean up table
    df['all names'] = df['No. 1'].astype(str) + ', ' + df['No. 2'].astype(str) + ', ' + df['No. 3'].astype(str) + ', ' + df['No. 4'].astype(str) + ', ' + df['No. 5'].astype(str) + ', ' + df['No. 6'].astype(str) + ', ' + df['No. 7'].astype(str) + ', ' + df['No. 8'].astype(str) + ', ' + df['No. 9'].astype(str) + ', ' + df['No. 10'].astype(str)
    df = df[['Region (year)', 'all names']]
    df = df.rename({'Region (year)': 'country'}, axis=1)

    # remove country values extra info, e.g. 'Egypt (2004, Coptic Christians, unofficial)[2]' to 'Egypt'
    pat = r'^(([a-z]|[A-Z]| )*)( \(|\[).*$'
    repl = lambda m: m.group(1)
    df['country'] = df['country'].str.replace(pat, repl, regex=True)

    df.to_pickle('names.pkl')
 
    return df

if __name__ == "__main__":
    main()