import numpy as np
import pandas as pd
import networkx as nx
import json

from os import listdir
from networkx.readwrite import json_graph

def readData(path):
    ''' Read in data required to make graphs
    @param path String: Specifies the CSV file to read in
    '''
    data = pd.read_csv(path)
    return data

def createGraph(data, year):
    ''' Initialize a graph using paper venues
    @param data DataFrame: Data frame containing grouped citation information
    @param year Integer: Specifies year of data to use
    '''
    data = data[data['year'] == year]
    graph = nx.DiGraph()
    venues = data.paper_venue
    for venue in venues:
        graph.add_node(venue)
    community_dict = dict(zip(data.paper_venue, data.paper_community))
    nx.set_node_attributes(graph, community_dict, 'community')
    for _, row in data.iterrows():
        paper_venue = row['paper_venue']
        reference_venue = row['reference_venue']
        citations = row['citations']
        graph.add_weighted_edges_from([(paper_venue, reference_venue, citations)])
    return graph

def generateGraphPos(graph):
    ''' Function to generate graph layout
    @param graph Graph: Graph containing nodes from initGraph()
    '''
    pos = nx.spring_layout(graph)
    for n, p in pos.items():
        graph.node[n]['x'] = p[0]
        graph.node[n]['y'] = p[1]
    return graph

def writeGraph(graph, fileloc):
    ''' Function to write graph to JSON format
    @param graph Graph: A graph created from createGraph()
    @param fileloc String: A string location of where to save the graphs
    '''
    json_data = json_graph.node_link_data(graph)
    with open(fileloc, 'w') as outfile:
        json.dump(json_data, outfile)
    return 'Wrote file'

def loadGraph(fileloc):
    ''' Function to load graph adjacency matrices
    @param fileloc String: A string location of what to read. Assumes that the
    graph is referenced as 'graph' in the .npz archive
    '''
    archive = np.load(fileloc)
    graph = archive['graph']
    return graph

citation_data = prepareData('data/', ['2017', '2016', '2015', '2014', '2013'], 25)
graph_directed = createGraph(citation_data, 'directed')
graph_undirected = createGraph(citation_data, 'undirected')

writeGraph(graph_undirected, 'graphs/undirected.npz')
undirected = loadGraph('graphs/undirected.npz')
