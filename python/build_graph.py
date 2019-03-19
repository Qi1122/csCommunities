import numpy as np
import pandas as pd
import networkx as nx

from os import listdir

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

def preprocessData(data, years, min_citations):
    ''' Preprocess and clean the data
    @param data DataFrame: Data frame containing citation information
    @param years List: List containing the years to include
    @param min_citations Int: Integer containing the minimum number of citations
    '''
    data = data[data['year'].isin(years)]
    data = data[data['n_citation'] >= min_citations]
    data = data.apply(lambda x: x.astype(str).str.lower())
    return data

def initGraph(data):
    ''' Initialize a graph using the different paper ids
    @param data DataFrame: Data frame containing citation information
    '''
    G = nx.DiGraph()
    for id in data['id']:
        G.add_node(id)
    community_dict = dict(zip(data.id,data.community))
    nx.set_node_attributes(G, community_dict, 'community')
    year_dict = dict(zip(data.id,data.year))
    nx.set_node_attributes(G, year_dict, 'year')
    venue_dict = dict(zip(data.id,data.venue))
    nx.set_node_attributes(G, venue_dict, 'venue')
    return G

def addEdgesDirected(graph, data):
    ''' Adds directed edges between different nodes
    @param graph Graph: Graph containing nodes from initGraph()
    @param data DataFrame: Data frame containing citation information
    '''
    for index, row in data.iterrows():
        id = row['id']
        refs = row['references']
        for ref in refs:
            graph.add_weighted_edges_from([(id, ref, 1)])
    return graph

def addEdgesUndirected(graph, data):
    ''' Adds undirected edges between different nodes
    @param graph Graph: Graph containing nodes from initGraph()
    @param data DataFrame: Data frame containing citation information
    '''
    for index, row in data.iterrows():
        id = row['id']
        refs = row['references']
        for ref in refs:
            graph.add_edge(id, ref)
    return graph

def prepareData(path, years, min_cit):
    ''' Function to prepare the data
    @param path String: Specifies the directory to search for JSON files
    @param years List: List containing the years to include
    @param min_citations Int: Integer containing the minimum number of citations
    '''
    citation_data = readJSON(path)
    citation_data = preprocessData(citation_data, years)
    citation_data = defineCommunity(citation_data)
    return citation_data

def createGraph(data, type):
    ''' Function to create a specified graph
    @param data DataFrame: Data frame containing citation information
    @param type String: Either 'directed' or 'undirected'
    '''
    if type == 'directed':
        graph = initGraph(data)
        graph = addEdgesDirected(graph, data)
    else:
        graph = initGraph(data)
        graph = addEdgesUndirected(graph, data)
    return graph

def writeGraph(graph, fileloc):
    ''' Function to save graphs
    @param graph Graph: A graph created from createGraph()
    @param fileloc String: A string location of where to save the graphs
    '''
    adj_mat = nx.to_numpy_matrix(graph)
    np.savez_compressed(fileloc, graph = adj_mat)
    return 'Saved file location at ' + fileloc

def loadGraph(fileloc):
    ''' Function to load graph adjacency matrices
    @param fileloc String: A string location of what to read. Assumes that the
    graph is referenced as 'graph' in the .npz archive
    '''
    archive = np.load(fileloc)
    graph = archive['graph']
    return graph

citation_data = prepareData('data/', ['2017', '2016', '2015', '2014', '2013'], 30)
graph_directed = createGraph(citation_data, 'directed')
graph_undirected = createGraph(citation_data, 'undirected')

writeGraph(graph_undirected, 'graphs/undirected.npz')
undirected = loadGraph('graphs/undirected.npz')
