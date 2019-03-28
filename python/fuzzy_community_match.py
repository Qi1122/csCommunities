''' Script to take in scraped community names and fuzzy match them
'''
import pandas as pd
import difflib

from os import listdir

def readJSON(path):
    ''' Read and concatenate JSON files in a given directory
    @param path String: Specifies the directory to search for JSON files
    '''
    data = pd.DataFrame()
    files = listdir(path)
    for file in files:
        print('Reading ', file)
        filePath = path + file
        data = data.append(pd.read_json(filePath, lines = True))
    return data

data = readJSON('data/')
communities = pd.read_csv('scraped_communities.csv')
data = data.apply(lambda x: x.astype(str).str.lower())

venue, community = [], []
for _, row in communities.iterrows():
    closest_match = difflib.get_close_matches(row.venue, data.venue.unique(), 1, 0.8)
    if closest_match == []:
        print('no match for ' + row.venue)
    else:
        venue.append(closest_match[0])
        community.append(row.community)
        print(row.venue + ' was matched with ' + closest_match[0])

new_data = pd.DataFrame({
    "venue": venue,
    "community": community,
})
new_data.to_csv('communities.csv', index = False)
