import numpy as np
import pandas as pd
import networkx as nx

from os import listdir

def readJSON(path):
    ''' Read and concatenate JSON files in a given directory
    @param path string: Specifies the directory to search for JSON files
    '''
    data = pd.DataFrame()
    files = listdir(path)
    for file in files:
        filePath = path + file
        data = data.append(pd.read_json(filePath, lines = True))
    return data

def defineCommunity(data):
    ''' Defines different computer science research communities by venue
    '''
    return None

def preprocessData(data):
    ''' Preprocess and clean the data
    @param data DataFrame: Data frame containing citation information
    '''
    data = data.apply(lambda x: x.astype(str).str.lower())
    return data

def initGraph(data):
    ''' Initialize a graph using the different paper ids
    @param data DataFrame: Data frame containing citation information
    '''
    G = nx.Graph()
    for id in data['id']:
        G.add_node(id)
    community_dict = data[['id', 'venue']]
    nx.set_node_attributes(G, 'community', community_dict)
    return G

def addEdgesGraph(graph, data):
    ''' Adds edges between different nodes
    @param graph Graph: Graph containing nodes from initGraph()
    @param data DataFrame: Data frame containing citation information
    '''
    for index, row in data.iterrows():
        id = row['id']
        refs = row['references']
        # if not there or NaN, then add no edges, else
        for ref in refs:
            graph.add_edge(id, ref)
    return graph

test = readJSON("data/")

for index, row in test.iterrows():
    print(row['id'])
