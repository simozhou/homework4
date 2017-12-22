import similarity as sm
import networkx as nx
import DataIO

"""
A module containing all the functions we want to create to facilitate the graphing procedure
of the dictionary of words. Depends on the IOData module.
"""


def subgraph_length(graph=None, length=None):
    """Purpose: equivalent words; returns a subgraph of words with equal length from the general dictGraph"""
    pass


def graph_build(array, func=sm.edit_distance, options=None):
    """
    Purpose: Generalized equivalent words; returns a  non-directed graph of words
    with edges representing function func which will return 1. if no func is passed, use similarity.edit_distance
    as default.
    """
    G = nx.Graph()
    # the words of our dictionary passed in as nodes for the graph
    nodes = array.keys()

