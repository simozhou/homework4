import nucleo_pebble_suggestions as nps
import os

# insert the piles
player = 1
p = {}

print('****insert your nucleotidic-piles: ****')
# create a dictionary in which the key is nucleotide and the value is the size of the pile
for i in ['A:', "T:", 'G:', "C:"]:
    value = ''
    while not (value.isdigit()):  # ask until a valid input is given(a non-negative value)
        value = input(i).strip()
    p[i[:-1]] = int(value)


def show():
    # Shows the piles associated to their lenght
    print("\n\tElements   | %s | %s | %s | %s | \n\t_____________^___^___^___^___\n"
          "\tPiles        A   T   G   C  \n" % (p['A'], p['T'], p['G'], p['C']))


def CheckLose(s):
    # checks if the game is finished: if only one pile is non-empty, the game is over
    emp = 0
    for i in s:
        if i == 0:  # counts all the empty piles
            emp += 1
    return emp


def SetPile(pp, el):  # update the piles
    # pp are the sorted piles (A,T,G,C)
    # el are the new values for the piles
    for i in range(4):
        p[pp[i]] = int(el[i])


def change(player):  # change the turn from the user to the computer, or viceversa
    "1 is the user. 2 is the computer"
    if player == 1:
        return 2
    return 1


def playT():
    nucl1, nucl2 = 'x', 'x'  # nucleotides to remove
    sortp = sorted(p, key=p.get)  # sort the keys (nucleotides) according to their values

    if (player == 2):  # Computer's turn
        print('\n' + '-' * 20)
        show()  # show the situation
        print("\n****  COMPUTER  ****\n")
        # choose a move for the computer, by moving to a P position if it is possible
        # otherwise move to a random position (the one to end quickly the game)
        new = nps.outcome(sorted(p.values()))
        SetPile(sortp, new)  # update the situation

    else:  # User's turn
        print('\n' + '+' * 20)
        show()
        print("\n**** YOU  ****\n")
        print('Choose the pile from which you want to remove the element or hit h to get a hint')
        while nucl1 not in p.keys() or nucl1 != 'h':  # ask which nucleotide he/she wants to remove. it must be present among the keys
            nucl1 = input('first element from--->').strip().upper()
            if nucl1 == 'H':
                print(nps.play_suggested(p))
                nucl1 = 'x'
            if nucl1 in p:
                if p[nucl1] == 0:
                    print('This pile is empty! Try another one.')
                    nucl1 = 'x'
                else:
                    break
        p[nucl1] -= 1  # remove 1 element from that pile

        while nucl2 not in p.keys() and nucl2 != '':  # ask if he/she wants to remove a second nucleotide.
            nucl2 = input('second element from (**otherwise just skip**)--->').strip().upper()
            if nucl2 in p:
                if p[nucl2] == 0:
                    print('This pile is empty! Try another one.')
                    nucl2 = 'x'
                else:
                    break
        if nucl2:
            p[nucl2] -= 1  # remove the second element, if required


if __name__ == "__main__":
    while CheckLose(p.values()) < 3:  # repeat the game untill only 0 or 1 piles are non-negative
        playT()  # play the turn
        player = change(player)  # change player
        os.system("cls")  # clean the screen
    show()

    if player == 2:
        print('\t**** Congratulations!!! YOU ARE THE WINNER!! ****',
              '\t         \(*0*)/ \t \(^-^)/ \t \(^0^)/', sep='\n')
    else:
        print('\t ----> Damn, YOU LOSE THE GAME, but...<----\n',
              '\t|A winner is just a loser who tried one more time|',
              '\t[cit. G.M.Moore Jr.]\n',
              'see you next time :)', sep='\n')
