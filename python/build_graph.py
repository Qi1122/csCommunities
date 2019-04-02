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

def generateYearlyGraph():
    ''' Function that generates and saves the graphs
    '''
    years = [2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970]
    citation_data = readData('graphs/graph_data/grouped_data.csv')
    for year in years:
        graph = createGraph(citation_data, year)
        #graph = generateGraphPos(graph)
        writeGraph(graph, 'graphs/' + str(year) + '_graph.json')
        print('Wrote graph for ' + str(year))
    return 'Wrote graphs'

citation_graph = generateYearlyGraph()
