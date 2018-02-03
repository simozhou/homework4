import networkx as nx
from collections import defaultdict
from itertools import groupby, combinations
import pickle


def grapher(wordFile):
    """
    Input: a .txt file containing you dictionary (separator \n)
    Output: a graph of all the words connected by edit distance value = 1

    The basic concept is "bucketing": dividing words with respect to some pseudo-words (have a placeholder instead
    of a letter each time). after this process is done, we have buckets of words which needs to get connected within the
    graph and by takiing the combination of the values in each bucket we have our graph cooked. This bad boy of a
    function allow us to solve the problem of the graph building in a quasi-linear time complexity ( O((2s+1)^2*n*b^2)
    s = avg word len, n = dict size, b = avg size of buckets, both b and s are relatively small with respect to n,
    so they can be considered as constant and cut off).
    """
    dictionary = {}
    g = nx.Graph()
    wfile = open(wordFile, 'r')
    # create buckets of words that differ by one letter
    for line in wfile:
        word = line[:-1]
        for bucket in word_cooker(word):
            if bucket in dictionary:
                if word not in dictionary[bucket]:
                    dictionary[bucket].append(word)
            else:
                dictionary[bucket] = [word]
    # add vertices and edges for words in the same bucket
    for bucket in dictionary.keys():
        g.add_edges_from(combinations(dictionary[bucket], 2))
    return g


def data_baker_len(filename="words_alpha.txt"):
    """
    function that takes in a text file of words and bake it into a dict of struct:
    ---> {len(word): [word1, word2, etc]}
    """
    with open(filename) as f:
        words = f.read().split()

    words_len = defaultdict(list)
    for key, values in groupby(words, key=len):
        words_len[key] += list(values)

    return words_len


def word_cooker(word):
    """actual creator of the buckets names"""
    yield "_" + word
    for i in range(len(word)):
        yield word[:i] + "_" + word[i + 1:]
        yield word[:i + 1] + "_" + word[i + 1:]


def equivalent_words(start, end, gameplay="general"):
    """
    the actual game function. Takes in a start and end word an a gameplay (simple or general).
    return a string with the path from start to end.

    Raises ValueError if in simple mode words of different length are plugged in.

    """
    # the graph we're using has been previously pickled to avoid those seconds of waiting for the graph get built
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
    except nx.NodeNotFound:
        return "One of the two words doesn't exist or is not in this graph. Try to be serious for once."
    result_string = "Path:\n" + ' -> '.join(result_list)
    return result_string


if __name__ == "__main__":
    # just some raw benchmark for the grapher function
    import time

    start = time.time()
    graph = grapher("words_alpha.txt")
    end = time.time() - start
    print(end)
    print(equivalent_words("head", "tail", "simple"))
