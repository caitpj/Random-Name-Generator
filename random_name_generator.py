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
    for i in range(parser().number):
        last_name_df = fetch_names('last-names.pkl')
        last_name = random.choices(last_name_df['Name'], weights=last_name_df['probability'])[0]
        last_name = last_name.replace("^\'|\'$", "").capitalize()
        
        first_name_df = fetch_names('first-names.pkl')
        first_name_df['all names'] = first_name_df['all names'].apply(lambda x: x[:].split(', '))
        
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
            country = random.choice(first_name_df.country.values.tolist())

        first_name_df = first_name_df.query(f"country == @country")
        
        try:
            first_names = first_name_df['all names'].iloc[g]
        except:
            sys.exit('Invalid country')
        
        first_name = random.choice(first_names)
        
        # deal with 'nan' names
        tries = 0
        while first_name == 'nan' or tries == 20:
            first_name = random.choice(first_names)
            tries += 1
    
        print(first_name, last_name)

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
    
    parser.add_argument('--number', '-n', default=1,
                        type=int,
                        help='the number of random names to be printed')

    args = parser.parse_args()

    return args

def fetch_names(filename):
    """
    Returns a dataframe with names, either from local file or Wikipedia
    """
    # Only fetches names from wikipedia if csv file does not exist or is over a day old
    # if os.path.isfile('names.csv') and time.time() - os.path.getmtime('names.csv') < (60 * 60 * 24):
    if os.path.isfile(filename) and time.time() - os.path.getmtime(filename) < (60 * 60 * 24):
        df = pd.read_pickle(filename)
    else:
        if filename == 'last-names.pkl':
            df = fetch_last_names_from_web()
        elif filename == 'first-names.pkl':
            df = fetch_first_names_from_web()
        else:
            sys.exit('Invalid filename')
    
    return df

def fetch_first_names_from_web():
    """
    Returns a dataframe with first names from the wikipedia page 'List_of_most_popular_given_names'
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

    df.to_pickle('first-names.pkl')
 
    return df

def fetch_last_names_from_web():
    """
    Returns a dataframe with last names from the namecensus.com page 'last-names'
    """
    # get the response in the form of html
    url = "https://namecensus.com/last-names/"
    response = requests.get(url)

    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    indiatable = soup.find('table', {'class':"table is-narrow is-bordered is-fullwidth mb-3"})
    df = pd.read_html(str(indiatable))
    df = pd.concat(df)

    # clean up table
    df = pd.DataFrame(df)
    df['Count'] = df['Count'].astype(int)
    df['probability'] = df['Count'] / df['Count'].sum()
    df = df[['Name', 'probability']]

    df.to_pickle('last-names.pkl')
 
    return df

if __name__ == "__main__":
    main()
