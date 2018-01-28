import os

debug=1
turnoG=1 #turno del giocatore

#pile
p=[int(input('Inserisci combinazione per iniziare il gioco \nA: ')), int(input('T: ')), int(input('G: ')), int(input('C: '))]
nm=['A', 'T', 'G', 'C'] #nomi delle pile

#Controlla se ci siano pile vuote
def CheckLose(s=[]):
    l = 0
    for i in s:
        if (i == 0):
            l+=1
    return l

#mostra le pile
def mostraPile():
    print("\n\tElementi   | %s | %s | %s | %s | \n\t_____________^___^___^___^___\n"
		"\tPile         A   T   G   C  \n" %(p[0],p[1],p[2],p[3]))

#cosa e' successo
def mostraMossa(a,b,c,d):
	print("\nIl computera ha eseguito il suo turno\n")
	v=[a,b,c,d]
	for i in range(4):
		if((p[i]-v[i])!=0):
			print("- CPU ha rimosso %s elementi dalla pila %s" %(p[i]-v[i] ,nm[i]))

#modifica le pile
def pcSet(a,b,c,d):
	p[0],p[1],p[2],p[3]=a,b,c,d # <<<< mhh

#trova se una combinazione sia rischiosa
def combRisc(a,b,c,d):
    # Combinazione rischiose
    # Permette di evitare di dare una combinazione al giocatore che lo porta a vincere, per es.0 0 2 2
    #in quanto il giocatore può togliere una pila vincendo !
    #Procedimento quasi identico a quello per trovare le mosse valide
    #Immaginiamo che a,b,c,d rappresentano la combinazione che ha generato il computer prima di richiamare
    #questa funzione , proviamo tutte le combinazioni possibili e
    #vediamo se è presente una combinazione vincente !!
    #Significa che se diamo a,b,c,d al giocatore , potrà vincere ( sempre se è abbastanza astuto xD)
    #Quindi la combinazione a,b,c,d è rischiosa e il giocatore non l'avrà mai !!

    cr= [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 1, 1, 0, 0,1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1]
    casiP = [1, 1, 1, 1,1, 2, 2, 0,1, 0, 2, 2,1, 2, 0, 2,0, 2, 1, 2,0, 1, 2, 2,0, 2, 2, 1,2, 0, 2, 1,2, 0, 1, 2,2, 2, 0, 1,2, 1, 2, 0,2, 2, 1, 0,2, 1, 0, 2,1, 1, 2, 2,1, 2, 1, 2,1, 2, 2, 1,2, 1, 1, 2,2, 1, 2, 1,2, 2, 1, 1]
    for j in range(0,len(casiP),4):
        if ((a == casiP[j]) & (b == casiP[j+1]) & (c == casiP[j+2]) & (d == casiP[j+3])):
            return True

    for i in range(0,len(cr), 4):
        cr[i] = a-cr[i]
        cr[i+1]= b-cr[i+1]
        cr[i+2] = c-cr[i+2]
        cr[i+3] = d-cr[i+3]
        if ((cr[i] < 0) | (cr[i+1] < 0) | (cr[i+2] < 0) | (cr[i+3] < 0)):
            cr[i],cr[i+1],cr[i+2],cr[i+3]=0,0,0,0
        s=[cr[i],cr[i+1], cr[i+2], cr[i+3]]
        if (CheckLose(s) == 3):
            return True
    return False


def setPile(y,z):
    p[y - 1] -= 1
    if (z !=0) :
        p[z - 1] -= 1

def posSicura(a,b,c,d):
	x=(a & ~b) | (~a & b)
	y=(c & ~d) | (~c & d)
	z=(x & ~y) | (~x & y)
	return z


def trovaComb(a,b,c,d):
#Array che contiene tutte le mosse possibili che si possono fare
    cr= [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 1, 1, 0, 0, 1,0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1]
    s=[]
    trvS = 0

#Procedimento per trovare la mossa perfetta del computer
    #Procedimento per trovare la mossa perfetta del computer
	#1 . Ciclo a contatore che modifica l'array generando tutte le mosse possibili
	    #All'interno del ciclo ci sono diversi controllo

    #2 . Ripulisci l'array rimuovendo le combinazioni con elementi negativi
	#3 . Verifica se è stata generata una combinazione vincente
	#4 . Escludi combinazioni a rischio  che possono far vincere il giocatore
    #5 . Se trovo una combinazione sicura la salvo , altrimenti salva una combinazione insicura
	    # Combinazione sicura permete di mantenere in equilibrio il gioco ,ovvero
	    # riduce la durata del gioco e diminuisce la probabilità che il computer abbia difficoltà
	    # A differenza del nim (la posizione sicura fornisce vittoria al computer ed non è possibile uscirne)
        #le regole di questo gioco fanno si che il giocatore possa uscire dalla posizione sicura
	    #ma questo non compremette l'algortimo neanche se il pc fornisce una posizione insicura al giocatore.
	    #L'algoritmo è abbastanza efficace grazie al punto numeo 4 il quale tramite una funzione è in grado di
	    #escludere tutte le combinazione che porta il giocatore a vincere( ehehe, caro giocatore non mi avrai mai)
	    #se vogliamo essere ottimisti , e il computer esclude tutte le combinazioni generate ( ben 12 )
	    #il risulato è in situazione di stallo (fino ad ora non mi è successo)
        #-1

    for i in range(0,len(cr),4):
        # Modifica array creando una combinazione
        cr[i] = a-cr[i]
        cr[i+1]= b-cr[i+1]
        cr[i+2] = c-cr[i+2]
        cr[i+3] = d-cr[i+3]
        # - 2
        if ((cr[i] < 0) | (cr[i+1] < 0) | (cr[i+2] < 0) | (cr[i+3] < 0)):
            if (debug == 1):
                print("Combinazione : %s %s %s %s <-Negativa \n" % (cr[i], cr[i+1], cr[i+2], cr[i+3]))
                cr[i],cr[i+1],cr[i+2],cr[i+3]=0,0,0,0
        else:
        # - 3
            s=[cr[i],cr[i+1], cr[i+2], cr[i+3]]
            if (CheckLose(s) == 3):
                if (debug == 1):
                    print("Combinazione : %s %s %s %s <-Vincente \n" % (cr[i], cr[i+1], cr[i+2], cr[i+3]))
                mostraMossa(cr[i], cr[i+1], cr[i+2], cr[i+3]) # Mostra qual'è la mossa eseguita
                pcSet(cr[i], cr[i+1], cr[i+2], cr[i+3])
                return # Inutile controllare altre combinazioni, esci dalla funzione

            else:
                # - 4
                if (combRisc(cr[i], cr[i + 1], cr[i + 2], cr[i + 3])):
                    if (debug == 1):
                        print("Combinazione : %s %s %s %s <-Rischiosa \n" % (cr[i], cr[i+1], cr[i+2], cr[i+3]))
                        cr[i],cr[i+1],cr[i+2],cr[i+3]=0,0,0,0

                else:
                    if (debug == 1):
                        print("Combinazione : %s %s %s %s <-Mossa valida " % (cr[i], cr[i+1], cr[i+2], cr[i+3]))
                    # - 5
                    if (posSicura(cr[i], cr[i+1], cr[i+2], cr[i+3]) == 0):
                        if (debug == 1):
                            print("<---Posizione sicura\n")
                        if (trvS == 0):
                            trvS,a1,b1,c1,d1=1,cr[i],cr[i+1],cr[i+2],cr[i+3]
                    else:
                        if (debug == 1):
                            print("<---Posizione insicura\n")
                        if (trvS == 0):
                            a1, b1, c1, d1 =cr[i], cr[i + 1], cr[i + 2], cr[i + 3]
    mostraMossa(a1, b1, c1, d1) #<<<<< a,b,c,d are not declared elsewhere
    #Esegui combinazione ricavata dal punto 5
    pcSet(a1, b1, c1, d1) #<<<<idem

def cambiaTurno(turnoG):
    if(turnoG==1):
        return 2
    return 1

def playT():
    x,y,z=0,0,0
    #x : numero di elementi da togliere
    #y : prima pila da cui rimuovere
	#z : seconda pila da cui rimuovere
    if(turnoG==2):
        print('\n'+'-'*20) #or os.system('cls') but doesn't clear the IDLE as it is supposed to do(?)
        mostraPile()
        print("\n**** Turno COMPUTER  ****\n")
        trovaComb(p[0],p[1],p[2],p[3]) #Avvia la ricerca della combinazione perfetta!?!
        mostraPile()
    else:
        print('\n'+'+'*20) #or os.system('cls') but doesn't clear the IDLE as it is supposed to do(?)
        mostraPile() #Niente di particolare , mostra le pile
        print("\n**** Turno Giocatore  ****\n")
        while(x != 1 and x != 2): #elementi da togliere
            x=int(input("Quanti elementi vuoi togliere ? ( 1 o 2 ):"))# <<<< causa problemi
            if(x!=1 and x!=2):
                print("Errore, inserire 1 o 2\n")
        while((y<1 or y>4) or p[y-1]==0): #pila deve essere tra 1-4
            y=int(input("Inserisci la pila da cui rimuovere un elemento : "))
            if((y<1 or y>4) or p[y-1]==0):
                print("Errore, le pile vanno da 1 a 4 (inclusi) e non devono essere vuote \n")

        if(x==2):
            while((z < 1 or z > 4) or p[z-1]==0):#pila deve essere tra 1-4 <<<<< se la pila y==1, z non puo' rimuovere dalla stessa pila
                z=int(input("Inserisci la seconda pila da cui rimuovere un elemento(puoi inserire la stessa pila) : "))
                if((z<1 or z>4) or (p[z-1]==0)):
                    print("Errore, le pile vanno da 1 a 4 (inclusi) e non devono essere vuote \n")
        setPile(y,z)
    os.system('pause')

if __name__ == "__main__":
    while (CheckLose(p) != 3): #Controlla se la partita è finita
        playT()#Gioca il turno
        turnoG=cambiaTurno(turnoG) #Alterna i turni tra i due giocatori
    os.system("cls")# Ripulisci la console
    if (turnoG == 2): # Se è il turno del computer significa che l'ultima mossa l'ha fatta il giocatori
        print("*** Complimenti, hai battuto il computer !! ***\n Ps. Avrei dovuto prevederlo\n")
    else: # in questo caso il computer ha fatto l'ultima mossa e ha vinto la partita
        print("*** Il computer ha vinto !! ***\n Ps. Non mi batterai mai\n ")
    os.system("pause") # Premere un tasto per continuare