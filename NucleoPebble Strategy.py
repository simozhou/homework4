import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools as it
import numpy as np

#This code is going to show the winning and the losing positions.
#The nucleotide sequence is divided in four heap and the sum of their sizes is important to define 3 cases.
#Everytime, the player moves from a case to another, due to mathematical reasons. If the player
# does the right moves, it's impossible to change the predicted result.
#The strategy and plots consider ONLY THE THREE SMALLER HEAPS.
#A priori, the player LOSES if three of the four heaps are empty.

pos=[i for i in it.combinations_with_replacement([0,1,2,3,4], 3)] #generate some of the possible positions

#CASE 1= The sum of all the heaps is multiple of three
#       -Winning positions= The exeptions conteined in the variable 'exept'
#       -Losing positions= if the larger two heaps are >= 5 (highlighted in the graph by a red surface); or the cases not included in the exeptions
def case1(pos):
    exept=[(0,0,1), (0,0,2), (0,1,1), (0,1,2), (0,1,3), (0,2,2), (0,2,3), (1,1,1), (1,1,2), (1,1,3), (1,2,2), (1,2,3), (1,2,4), (1,3,3), (2,2,2), (2,2,3), (2,2,4), (2,3,3)]
    Graph(pos,exept,U_limit=True)

    plt.title('Sum == 3n')

#CASE 2= The sum of all the heaps is 1 more the multiple of three
#       -Winning positions= All the positions, excluding the two exeptions
#       -Losing positions= The case 1/1/1/3n+1 and the default case (0/0/0/3n+1)
def case2(pos):
    exept = [(0, 0, 0), (1, 1, 1)]
    Graph(pos,exept,True)
    plt.title('Sum == 3n+1')

#CASE 3= The sum is 2 more the multiple of three
#       -Winning positions= All the positions, excluding the exeptions
#       -Losing positions= The exeptions
def case3(pos):
    exept=[(0,1,2), (0,2,2), (1,2,3), (1,2,2), (2,2,2), (2,2,3), (0,0,0)]
    Graph(pos,exept)

    plt.title('Sum == 3n+2')


#Function required to show the position in 3D
def Graph(Win, Lose, L_plane=False, U_limit=False):
    #Collect all the winning positions
    Win = [Win[w] for w in range(len(Win)) if (pos[w] not in Lose)]

    fig = plt.figure()#Create the plot
    ax = fig.add_subplot(111, projection='3d')

    #insertion of all the Winning positions in the scatter plot 3D
    Xax = [Win[x][0] for x in range(len(Win))]
    Yax = [Win[y][1] for y in range(len(Win))]
    Zax = [Win[z][2] for z in range(len(Win))]
    W = ax.scatter(Xax, Yax, Zax, s=50, marker='o', c='red')

    #insertion of the losing positions in the scatter plot 3D
    Xax = [Lose[x][0] for x in range(len(Lose))]
    Yax = [Lose[y][1] for y in range(len(Lose))]
    Zax = [Lose[z][2] for z in range(len(Lose))]
    L = ax.scatter(Xax, Yax, Zax, s=50, marker='^', c='blue')

    if L_plane: #If the last move can be a losing one, the plot shows a yellow surface at the bottom
        Final='Final Winning\Losing move'
        cm='autumn_r'
    else: #otherwise it shows a green surface, meaning that it is the last winning move
        Final='Final Winning move'
        cm='Set2'
    Wx,Wy= np.meshgrid(np.arange(0, 5, 1), np.arange(0, 5, 1))
    ax.plot_surface(Wx,Wy, np.asarray([[1,1,1,1,1]]*len(Wx)),shade=0.2, cmap=cm)
    ax.text(3, 3,1.2,Final, color='red')

    if U_limit: #The upper limint means that, from that position on, they are all losing positions (red surface)
        ax.plot_surface(Wx, Wy, np.asarray([[5,5,5,5,5]] * len(Wx)), shade=0.2, cmap='Pastel1')
        ax.text(3, 3, 5.2, 'UpperLimit', color='red')

    #additional features (limits,scale,labels, legend)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_xscale('linear')
    ax.set_yscale('linear')
    ax.set_zscale('linear')
    ax.set_xlabel('Heap 1')
    ax.set_ylabel('Heap 2')
    ax.set_zlabel('Heap 3')
    ax.legend((L,W), ('Losing positions', 'Winning positions'))

#Questions to interact with the player
def Questions():
    answ_l=[False,False]
    print('Please, typt only ONE of the following answers:','\t-"ALL" if you want to see all the strategies',
          '\t-"ONLY" if you want to see your specific situation', sep='\n')
    answ=input('-->').strip()
    if answ.upper()=='ALL':
        answ_l[0]=not(answ_l[0])
    elif answ.upper()=='ONLY':
        answ_l[1] = not (answ_l[1])

    if answ_l[0]: #if the player wants to see the positions of all the cases, plot all of them
        print('loading...')
        case1(pos)
        case2(pos)
        case3(pos)

    elif answ_l[1]: #otherwise, ask the total size of the heaps to infer the specific case
        Tot_Sum=''
        while(not (isinstance(Tot_Sum, int))):
            Tot_Sum=int(input('Please, insert the sum of all the four heaps: ').strip())

        if (Tot_Sum%3==0):
            case1(pos)
        elif (Tot_Sum%3==0):
            case2(pos)
        else:
            case3(pos)
    plt.show()

Questions()