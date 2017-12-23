import networkx as nx
import itertools

"""
A module containing all the functions we want to create to facilitate the graphing procedure
of the dictionary of words. 
"""
global G
global dictionary_len

def edit_distance(word1, word2):
    pass


def edit_distance_reducer(mapped_pair) -> tuple:
    """returns the edit distance between two words"""
    H = {}
    words_pairs = mapped_pair[1]
    for pair in words_pairs:
        if pair in H.keys():
            return H[pair], pair
        else:
            c = edit_distance(*pair)
            H[pair] = c
            return c, pair


def load_words(filename="words.txt"):
    try:
        with open(filename, "r") as english_dictionary:
            valid_words = english_dictionary.read().split('\n')
            valid_words.pop()
            return valid_words
    except Exception as e:
        return str(e)


def subgraph_length(graph=None, length=None):
    """Purpose: equivalent words; returns a subgraph of words with equal length from the general dictGraph"""
    return nx.subgraph(G, dictionary_len[length])


def graph_build(options=None):
    """
    Purpose: Generalized equivalent words; returns a  non-directed graph of words
    with edges representing function func which will return 1. Levenshtein distance is used as default.
    """
    # list of words
    dictionary = load_words()
    dictionary_len = word_len_selector(dictionary)
    # graph object instance
    G = nx.Graph(name="English dictionary")
    # adding all the nodes from the dict
    G.add_nodes_from(dictionary)
    # to build the edges between words following the edit_distance function, all the computations are given to
    # Databricks to execute.
    dictionary = sc.parallelize([i for i in itertools.combinations(dictionary, 2)])
    edges = dictionary.flatMap(init_str_mapper) \
        .reduceByKey(lambda x: x[0]) \
        .reduce(edit_distance_reducer)


def init_str_mapper(pair):
    return (pair[0][:2], pair[1][:2]), pair


# to get the dictionary to use when solving simple equivalent words
def word_len_selector(dictionary):
    subgraph_nodes = {}
    dictionary = sc.parallelize(dictionary)
    len_map = dictionary \
        .flatMap(len_mapper) \
        .reduceByKey(lambda x: x[0])
    for length, lister in len_map:
        subgraph_nodes[length] = lister
    return subgraph_nodes


def len_mapper(word):
    return len(word), word


if __name__ == '__main__':
    print(load_words())
