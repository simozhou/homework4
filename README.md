
#Equivalent words
>The algorithm(s) works as follows:
1. Takes two words in input, one will be the starting one, the other the final one.
2. Rolls over the graph built on the distances of all the elemnts in the [dictionary](https://github.com/dwyl/english-words/blob/master/words.txt), checking if it's possible to actually transform the two words.
3. returns all the nodes it encountered throughout the path.

- The dictionary-graph is a non-directional graph where each node is a word of the dictionary, and the edges are bult ad follows: `edge = (EditDistance(w,v) == 1)`, so that if the edit distance is equal to 1, the two nodes are linked.

>>## Simple Generalized equivalent words
>>Transforms one English word *v* into another word *w* by going through a series of intermediate English words, where each word in the sequence differs from the next by only one substitution (1 character).

>>## Generalized equivalent words
>>An algorithm which solves a generalization of the Equivalent Words problem when insertions, deletions, and substitutions are allowed (rather than only substitutions).

# *4*-dimensional pebble game
Pebble game solved for 4 towers. To check **what is a pebble game** take a look at [this](https://en.wikipedia.org/wiki/Pebble_game).
