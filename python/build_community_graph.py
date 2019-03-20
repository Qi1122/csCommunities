import numpy as np
import pandas as pd
import networkx as nx

from os import listdir
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

def defineCommunity(data):
    ''' Defines different computer science research communities by venue
    @param data DataFrame: Data frame containing citation information
    '''
    communities = pd.read_csv("communities.csv")
    venues = communities.venue
    dataFiltered = data[data.venue.isin(venues)]
    dataFiltered = dataFiltered.merge(communities, on = "venue", how = "left")
    return dataFiltered

def preprocessData(data, years):
    ''' Preprocess and clean the data
    @param data DataFrame: Data frame containing citation information
    @param years List: List containing the years to include
    '''
    data = data[data['year'].isin(years)]
    data = data.apply(lambda x: x.astype(str).str.lower())
    return data

def prepareData(path, years):
    ''' Function to prepare the data
    @param path String: Specifies the directory to search for JSON files
    @param years List: List containing the years to include
    '''
    citation_data = readJSON(path)
    citation_data = preprocessData(citation_data, years)
    citation_data = defineCommunity(citation_data)
    return citation_data
