from collections import defaultdict, deque
from itertools import chain

def shortened_words(word):
    for i in range(len(word)):
        yield word[:i] + word[i + 1:], i

def prepare_graph(d):
    g = defaultdict(list)
    for word in d:
        for short in shortened_words(word):
            g[short].append(word)
    return g


def walk_graph(g, d, start, end):
    todo = deque([start])
    seen = {start: None}
    while todo:
        word = todo.popleft()
        if word == end: # end is reachable
            break

        same_length = chain(*(g[short] for short in shortened_words(word)))
        one_longer = chain(*(g[word, i] for i in range(len(word) + 1)))
        one_shorter = (w for w, i in shortened_words(word) if w in d)
        for next_word in chain(same_length, one_longer, one_shorter):
            if next_word not in seen:
                seen[next_word] = word
                todo.append(next_word)
    else: # no break, i.e. not reachable
        return None # not reachable

    path = [end]
    while path[-1] != start:
        path.append(seen[path[-1]])
    return path[::-1]

dictionary = open('words_alpha.csv', "r").read().split() # list words
graph = prepare_graph(dictionary)
print(" -> ".join(walk_graph(graph, dictionary, "head", "tail")))
print(" -> ".join(walk_graph(graph, dictionary, "head", "tea ")))