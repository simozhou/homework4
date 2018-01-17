from collections import defaultdict, namedtuple
from heapq import heappush, heappop
from itertools import groupby
import editdistance as ed


def data_baker(filename="words_alpha.txt"):
    """function that takes in a text file of words and bae them into a python list + dict them according to sizes"""
    with open(filename) as f:
        words = f.read().split()

    words_len = defaultdict(list)
    for key, values in groupby(words, key=len):
        words_len[key] += list(values)

    return words, words_len


class PathNotFound(BaseException):
    pass

def edit_distance(word1, word2) -> int:
    # degenerate cases
    if word1 == word2:
        return 0
    if len(word1) == 0:
        return len(word2)
    if len(word2) == 0:
        return len(word1)
    v0, v1 = [], []
    for i in range(len(word2) + 1):
        v0.append(i)
        v1.append(0)

    for i in range(len(word1)):
        v1[0] = i + 1

        # use formula to fill in the rest of the row
        for j in range(len(word2)):
            cost = 0 if word1[i] == word2[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)

        # copy v1 (current row) to v0 (previous row) for next iteration
        for j in range(len(word2) + 1):
            v0[j] = v1[j]

    return v1[len(word2)]


def word_ladder(words, start, end, distance="hamming"):
    """Return a word ladder (a list of words each of which differs from
    the last by one letter) linking start and end, using the given
    collection of words. Raise NotFound if there is no ladder.

    >>> words = 'card care cold cord core ward warm'.split()
    >>> ' '.join(word_ladder(words, 'cold', 'warm'))
    'cold cord card ward warm'

    """
    # Find the neighbourhood of each word.
    placeholder = object()
    matches = defaultdict(list)
    neighbours = defaultdict(list)
    for word in words:
        for i in range(len(word)):
            pattern = tuple(placeholder if i == j else c
                            for j, c in enumerate(word))
            m = matches[pattern]
            m.append(word)
            neighbours[word] += [m]

    # A* algorithm: see https://en.wikipedia.org/wiki/A*_search_algorithm

    # Admissible estimate of the steps to get from word to end.
    def d_score(word):
        if distance is "hamming":
            return sum(a != b for a, b in zip(word, end))
        elif distance is "edit":
            return ed.eval(word, end)

    # Closed set: of words visited in the search.
    closed_set = set()

    # Open set: search nodes that have been found but not yet
    # processed. Accompanied by a min-heap of 4-tuples (f-score,
    # g-score, word, previous-node) so that we can efficiently find
    # the node with the smallest f-score.
    Node = namedtuple('Node', 'f g word previous')
    open_set = {start}
    open_heap = [Node(d_score(start), 0, start, None)]
    while open_heap:
        node = heappop(open_heap)
        if node.word == end:
            result = []
            while node:
                result.append(node.word)
                node = node.previous
            return result[::-1]
        open_set.remove(node.word)
        closed_set.add(node.word)
        g = node.g + 1
        for neighbourhood in neighbours[node.word]:
            for w in neighbourhood:
                if w not in closed_set and w not in open_set:
                    next_node = Node(d_score(w) + g, g, w, node)
                    heappush(open_heap, next_node)
                    open_set.add(w)

    raise PathNotFound("No ladder from %s to %s" % (start, end))


if __name__ == '__main__':
    import timeit
    words, words_len = data_baker()
    print(timeit.timeit('word_ladder(words_len[4],"heal", "toast", distance="edit")', number=1, globals=globals()))
