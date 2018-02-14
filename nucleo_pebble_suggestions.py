import nucleo_pebble_strategy as st
import numpy as np


def play_suggested(piles):
    """used in the game, activated y 'h' on the keyboard. returns a string with a suggestion for the user""" 
    piles = piles.items()
    piles_num, piles_name = list(), list()
    for k,v in piles:
        piles_name.append(k)
        piles_num.append(v)
    piles = np.array(piles_num)
    predicted = outcome(piles)
    delta_piles = piles - predicted
    # if one elem is taken
    if sum(delta_piles) == 1.0:
        return "try to remove 1 pile from %s" % piles_name[list(delta_piles).index(1.0)]
    # if two elements are taken
    elif sum(delta_piles) == 2.0:
        # check if non zero elems are more than 1 (elems taken from 2 different piles)
        if np.count_nonzero(delta_piles) != 1.0:
            piles_of_interest = tuple(piles_name[i] for i in range(len(delta_piles)) if list(delta_piles)[i] == 1.0)
            return "try to remove 2 piles from %s and %s" % piles_of_interest
        else:
            return "try to remove 2 piles from %s" % piles_name[list(delta_piles).index(2.0)]


def insertion():
    print('insert your sequence:')
    pile = []
    for i in ['A:', "T:", 'G:', "C:"]:  # insert the element present in each nucleotide-pile
        value = 'a'
        while (not (value.isdigit())):  # ask again until the player inserts a valid number
            value = input(i).strip()
        pile.append(int(value))

    pile = tuple(sorted(pile))
    if sum(pile) % 3 == 0:
        st.case1(st.pos, pile[:-1])

    elif sum(pile) % 3 == 1:
        st.case2(st.pos, pile[:-1])

    else:
        st.case3(st.pos, pile[:-1])

    return pile


def state_position(x):
    """true --> P, false --> N"""
    x = tuple(x)
    # differenciate each case.
    # return True you are in a P state.
    if (sum(x) % 3 == 0):
        exept = [(0, 0, 1), (0, 0, 2), (0, 1, 1), (0, 1, 2), (0, 1, 3), (0, 2, 2), (0, 2, 3), (1, 1, 1), (1, 1, 2),
                 (1, 1, 3), (1, 2, 2), (1, 2, 3), (1, 2, 4), (1, 3, 3), (2, 2, 2), (2, 2, 3), (2, 2, 4), (2, 3, 3)]
        if x not in exept:
            return True

    elif (sum(x) % 3 == 1):
        exept = [(0, 0, 0), (1, 1, 1)]
        if x in exept:
            return True

    else:
        exept = [(0, 1, 2), (0, 2, 2), (1, 2, 3), (1, 2, 2), (2, 2, 2), (2, 2, 3), (0, 0, 0)]
        if x in exept:
            return True

    return False


def outcome(x):
    """
    Function taking a state of the game and returning the best possible move (aka a move to a P state)
    """
    outputs = []  # list for best possible move
    randMov = []  # list for random positions (because you are already in a P state)
    # generate all the possible moves
    moves = (*np.identity(4), *2 * np.identity(4), *(np.eye(3, 4) + np.eye(3, 4, 1)), np.array([1, 0, 1, 0]),
             np.array([1, 0, 0, 1]), np.array([0, 1, 0, 1]))

    for i in range(len(moves)):
        out = np.array(x) - moves[i]  # generate all the possible combinations
        if (sum(out >= 0) == 4):  # if all the pile are non-negative...
            if state_position(out[:-1]):  # check if it is possible to move to a P state
                outputs.append(out)
            elif not state_position(out[:-1]):  # otherwise, consider it as a randomic move
                randMov.append(out)

    if outputs:  # if it is possible to make a good move, take the combination that let finish the game quickly
        return min(outputs, key=sum)
    elif randMov:  # otherwise, make a randomic move
        return min(randMov, key=sum)
    else:  # extra case: if you are in the default P state (all piles are 0)
        return np.array([0, 0, 0, 0])


if __name__ == "__main__":
    piles = dict(A=1,T=2,C=2,G=1)
    print(play_suggested(piles))
