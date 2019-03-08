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

def initGraph(data):
    ''' Initialize a graph using the different paper ids
    '''

def addEdgesGraph(data):
    ''' Adds edges between different nodes
    '''


test = readJSON("data/")
