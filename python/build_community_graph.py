import numpy as np
import pandas as pd
import networkx as nx

from os import listdir
from ast import literal_eval
from networkx.readwrite import json_graph

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

def cleanData(data, years):
    ''' Cleans the data to prepare it for transformation
    @param data DataFrame: Data frame containing citation information
    @param years List: List containing the years to include
    '''
    data['zero_refs'] = data.references.str.len() == 0
    data = data[data['zero_refs'] == False]
    data = data[data['year'].isin(years)]
    data = data.apply(lambda x: x.astype(str).str.lower())
    data['nan_refs'] = data.references == 'nan'
    data = data[data['nan_refs'] == False]
    communities = pd.read_csv('communities.csv')
    venues = communities.venue
    data = data[data.venue.isin(venues)]
    data = data.merge(communities, on = 'venue', how = 'left')
    data = data[['id', 'year', 'venue', 'community', 'references']]
    return data

def transformData(data):
    ''' Transform data into easier to work with format
    @param data DataFrame: Data frame containing clean citation information
    '''
    id, year, venue, community, references = [], [], [], [], []
    for _, row in data.iterrows():
        id.append(row.id)
        year.append(row.year)
        venue.append(row.venue)
        community.append(row.community)
        references.append(literal_eval(row.references))
    new_data = pd.DataFrame({
        "id": id,
        "year": year,
        "venue": venue,
        "community": community,
        "references": references
    })
    new_data = new_data.references.apply(pd.Series).merge(new_data, left_index = True, right_index = True).drop(['references'], axis = 1).melt(id_vars = ['id', 'year', 'venue', 'community'], value_name = 'reference').drop('variable', axis = 1).dropna()
    return new_data

def assignCommunity(data, paper_data):
    ''' Defines different computer science research communities by venue
    @param data DataFrame: Data frame containing citation information
    @param paper_data DataFrame: Data frame containing venue info for all papers
    '''
    paper_data = paper_data[['id', 'venue']]
    paper_data.columns = ['id', 'reference_venue']
    data = data.merge(paper_data, left_on = 'reference', right_on = 'id')
    communities = pd.read_csv('communities.csv')
    communities.columns = ['venue', 'reference_community']
    data = data.merge(communities, left_on = 'reference_venue', right_on = 'venue')
    return data

def prepareData(path, years):
    ''' Function to prepare the data
    @param path String: Specifies the directory to search for JSON files
    @param years List: List containing the years to include
    '''
    print("----- Reading in data -----")
    unclean_data = readJSON(path)
    print("----- Cleaning data -----")
    citation_data = cleanData(unclean_data, years)
    print("----- Transforming the data -----")
    citation_data = transformData(citation_data)
    print("----- Finding communities for references -----")
    citation_data = assignCommunity(citation_data, unclean_data)
    return citation_data

citation_data = prepareData('data/', ['2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003'])
