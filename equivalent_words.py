import networkx as nx
from collections import defaultdict
from itertools import groupby
import pickle

def grapher(wordFile):
    d = {}
    g = nx.Graph()
    wfile = open(wordFile, 'r')
    # create buckets of words that differ by one letter
    for line in wfile:
        word = line[:-1]
        for bucket in word_cooker(word):
            if bucket in d:
                d[bucket].append(word)
            else:
                d[bucket] = [word]
    # add vertices and edges for words in the same bucket
    for bucket in d.keys():
        for word1 in d[bucket]:
            for word2 in d[bucket]:
                if word1 != word2:
                    g.add_edge(word1, word2)
    return g


def data_baker_len(filename="words_alpha.txt"):
    """function that takes in a text file of words and bae them into a python list + dict them according to sizes"""
    with open(filename) as f:
        words = f.read().split()

    words_len = defaultdict(list)
    for key, values in groupby(words, key=len):
        words_len[key] += list(values)

    return words_len


def word_cooker(word):
    yield "_" + word
    for i in range(len(word)):
        yield word[:i] + "_" + word[i + 1:]
        yield word[:i + 1] + "_" + word[i + 1:]


def equivalent_words(start, end, gameplay="general"):
    graph = nx.read_gpickle("graph.pickle")
    dict_len = pickle.load(open("len_dict.pickle", 'rb'))
    if gameplay == "simple":
        if len(start) != len(end):
            raise ValueError("Can't use words with different length in simple mode! Switch to general mode.")
        graph = nx.subgraph(graph, dict_len[len(start)])
    try:
        # using A* search algorithm
        result_list = nx.astar_path(graph, start, end)
    except nx.NetworkXNoPath:
        return "No path found between %s and %s" % (start, end)
    result_string = "Path:\n" + ' -> '.join(result_list)
    return result_string

if __name__=="__main__":
    print(equivalent_words("head", "tail", "simple"))