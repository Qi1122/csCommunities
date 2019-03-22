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
        print("Reading ", file)
        filePath = path + file
        data = data.append(pd.read_json(filePath, lines = True))
    return data

def cleanData(data, years):
    ''' Cleans the data to prepare it for processing
    @param data DataFrame: Data frame containing citation information
    @param years List: List containing the years to include
    '''
    data['zero_refs'] = data.references.str.len() == 0
    data = data[data['zero_refs'] == False]
    data = data[data['year'].isin(years)]
    data = data.apply(lambda x: x.astype(str).str.lower())
    data['nan_refs'] = data.references == 'nan'
    data = data[data['nan_refs'] == False]
    data = data[['id', 'year', 'venue', 'references']]
    return data

def transformData(data):
    ''' Transform data into easier to work with format
    @param data DataFrame: Data frame containing clean citation information
    '''
    id, year, venue, references = [], [], [], []
    for _, row in data.iterrows():
        id.append(row.id)
        year.append(row.year)
        venue.append(row.venue)
        references.append(literal_eval(row.references))
    new_data = pd.DataFrame({
        "id": id,
        "year": year,
        "venue": venue,
        "references": references
    })
    new_data = new_data.references.apply(pd.Series).merge(new_data, left_index = True, right_index = True).drop(['references'], axis = 1).melt(id_vars = ['id', 'year', 'venue'], value_name = 'reference').drop('variable', axis = 1).dropna()
    return new_data

def prepareData(path, years):
    ''' Function to prepare the data
    @param path String: Specifies the directory to search for JSON files
    @param years List: List containing the years to include
    '''
    print("----- Reading in data -----")
    citation_data = readJSON(path)
    print("----- Cleaning data -----")
    citation_data = cleanData(citation_data, years)
    print("----- Transforming the data -----")
    citation_data = transformData(citation_data)
    #citation_data = defineCommunity(citation_data)
    return citation_data

citation_data = prepareData('data/', ['2017', '2016', '2015', '2014', '2013', '2012'])

def defineCommunity(data):
    ''' Defines different computer science research communities by venue
    @param data DataFrame: Data frame containing citation information
    '''
    communities = pd.read_csv("communities.csv")
    venues = communities.venue
    dataFiltered = data[data.venue.isin(venues)]
    dataFiltered = dataFiltered.merge(communities, on = "venue", how = "left")
    return dataFiltered
