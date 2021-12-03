#!/usr/bin/env python
"""
Salamis is a turn-based strategy game for 2 players that is mostly text-based. The one goal of the game is to destroy all enemy ships. 

"""
import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt
import random
import os


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def requestinteger(prompt, min, max):
    while True:
        test=input(prompt)
        try:
            number=int(test)
            if (number >= min) & (number <=max):
                return(number)
            else:
                print('Outside allowed range')
        except:
            print('Not the right input type')

def visualise(ISLANDARRAY, blockornot=True):
    """
    Plot map with information
    """
    fig = plt.figure()
    fig.set_size_inches(8, 8)
    ax = fig.gca()
    ax.set_xticks(np.arange(0, 21, 1))
    ax.set_yticks(np.arange(0, 21, 1))

    plt.plot(ISLANDARRAY.loc[ISLANDARRAY['owner'] == 0.]["xcoord"], ISLANDARRAY.loc[ISLANDARRAY['owner'] == 0.]["ycoord"],'.', color='grey')
    plt.plot(ISLANDARRAY.loc[ISLANDARRAY['owner'] == 1.]["xcoord"], ISLANDARRAY.loc[ISLANDARRAY['owner'] == 1.]["ycoord"],'bo')
    plt.plot(ISLANDARRAY.loc[ISLANDARRAY['owner'] == 2.]["xcoord"], ISLANDARRAY.loc[ISLANDARRAY['owner'] == 2.]["ycoord"],'ro')
    for i in range(ISLANDARRAY.shape[0]):
        plt.text(ISLANDARRAY['xcoord'][i]-0.5,ISLANDARRAY['ycoord'][i]-0.5,str(i),color='grey')
        plt.text(ISLANDARRAY['xcoord'][i],ISLANDARRAY['ycoord'][i],str(ISLANDARRAY['value'][i])+'_'+str(ISLANDARRAY['nships'][i]),color='grey')
    plt.grid(which='both')
    plt.show(block=blockornot)


def setupislands(nislands):
    """
    Set up basic game map with islands. All in Pandas data frame.
    """
    ISLANDS=pd.DataFrame(data=None, columns=['xcoord','ycoord','value','owner','nships'])
    STARTISLANDS=pd.DataFrame(data=[[0,0,10,1,0],[20,20,10,2,0]], columns=['xcoord','ycoord','value','owner', 'nships'])
    ISLANDS=ISLANDS.append(STARTISLANDS, ignore_index=True)
    for island in range(nislands):
        print(island)
        xpos=random.randint(1,19)
        ypos=random.randint(1,19)
        value=random.randint(3,9)
        THISISLAND=pd.DataFrame(data=[[xpos,ypos,value,0,0]], columns=['xcoord','ycoord','value','owner', 'nships'])
        ISLANDS=ISLANDS.append(THISISLAND, ignore_index=True)
        THISISLAND=pd.DataFrame(data=[[20.-ypos,20-xpos,value,0,0]], columns=['xcoord','ycoord','value','owner', 'nships'])
        ISLANDS=ISLANDS.append(THISISLAND, ignore_index=True)
    return(ISLANDS)

def whowon(ISLANDS, SAILING):
    """
    Test if any player has 0 ships and has therefore lost the game.
    """
    shipsplayer1=ISLANDS.loc[ISLANDS['owner'] == 1]["nships"].sum()+SAILING.loc[SAILING['owner'] == 1]['nships'].sum()
    shipsplayer2=ISLANDS.loc[ISLANDS['owner'] == 2]["nships"].sum()+SAILING.loc[SAILING['owner'] == 2]['nships'].sum()
    whowon=0
    if shipsplayer1 < 1 and shipsplayer2 > 0: 
        print('Player 2 won')
        return(2)
    if shipsplayer2 < 1 and shipsplayer1 > 0: 
        print('Player 1 won')
        return(1)        
    return(0)


def sendships(ISLANDS, activeplayer, speed):
    YOURISLANDS=ISLANDS[ISLANDS['owner'].isin([activeplayer])]
    intfromwhere=requestinteger('From what island?',0,99)
    while not (intfromwhere in YOURISLANDS.index):
        intfromwhere=requestinteger('Not your island. From what island?',0,99)
            
    for island in ISLANDS.index:
        distance=np.sqrt(  (ISLANDS.loc[intfromwhere, 'xcoord']-ISLANDS.loc[island, 'xcoord'])**2 + (ISLANDS.loc[intfromwhere, 'ycoord']-ISLANDS.loc[island, 'ycoord'])**2)
        takesturns=int(round(distance/speed+0.5))
        print('To island '+str(island)+' takes '+str(takesturns)+' turns. It is value '+str(ISLANDS.loc[island, 'value'])+' and is held by player'+str(ISLANDS.loc[island, 'owner'])+' with '+str(ISLANDS.loc[island, 'nships'])+' ships.' )
    inttowhere=requestinteger('To which island?',0,99)

    while not (inttowhere in ISLANDS.index):
        inttowhere=requestinteger('Island doesn\'t exist. To which island?',0,99)
    intnships=requestinteger('How many ships?',0,9999)
    while (intnships > (YOURISLANDS.loc[intfromwhere,'nships'] )): # && (intnships > 0): 

        intnships=requestinteger('More than you have there. How many ships?',0,9999)

    ISLANDS.loc[intfromwhere, 'nships'] -= intnships
    distance=np.sqrt(  (ISLANDS.loc[intfromwhere, 'xcoord']-ISLANDS.loc[inttowhere, 'xcoord'])**2 + (ISLANDS.loc[intfromwhere, 'ycoord']-ISLANDS.loc[inttowhere, 'ycoord'])**2)
    #print(distance, distance/speed, round(distance/speed+0.5))
    takesturns=round(distance/speed+0.5)
    #print('This takes '+str(takesturns)+' turns. Are you sure?')
    THISSAILING=pd.DataFrame(data=[[activeplayer,intnships,inttowhere,takesturns]], columns=['owner','nships','toisland','arriveinnturns'])
    print('done - ships are sent. They will arrive in '+str(takesturns)+' turns.')
    return(ISLANDS, THISSAILING)

def getships(ISLANDS):
    """Both players get their ships at the start of turn"""
    for index in ISLANDS.index:
        if ISLANDS.loc[index, 'owner'] > 0:
            ISLANDS.loc[index, 'nships']=ISLANDS.loc[index, 'nships']+ISLANDS.loc[index, 'value']
    return(ISLANDS)

def showsailingplan(SAILING, activeplayer):
    YOURSAILING=SAILING[SAILING['owner'].isin([activeplayer])]
    print(YOURSAILING)

def measuredistance(ISLANDS, speed):
    intfromwhere=requestinteger('From what island?',0,99)
    while not (intfromwhere in ISLANDS.index):
        intfromwhere=requestinteger('Not an island. From what island?',0,99)
        
    for island in ISLANDS.index:
        distance=np.sqrt(  (ISLANDS.loc[intfromwhere, 'xcoord']-ISLANDS.loc[island, 'xcoord'])**2 + (ISLANDS.loc[intfromwhere, 'ycoord']-ISLANDS.loc[island, 'ycoord'])**2)
        takesturns=int(round(distance/speed+0.5))
        print('To island '+str(island)+' takes '+str(takesturns)+' turns. It is value '+str(ISLANDS.loc[island, 'value'])+' and is held by player'+str(ISLANDS.loc[island, 'owner'])+' with '+str(ISLANDS.loc[island, 'nships'])+' ships.' )

def shipsarrive(ISLANDS, SAILING):
    bonusfactor=1.25  #25% defense bonus
    SAILING['arriveinnturns']=SAILING['arriveinnturns']-1
    for index in ISLANDS.index:
        owner=ISLANDS.loc[index, 'owner']
        value=ISLANDS.loc[index, 'value']
        shipsonisland=ISLANDS.loc[index, 'nships']
        player1=SAILING[(SAILING['owner'] == 1) & (SAILING['toisland'] == index) & (SAILING['arriveinnturns'] < 0.5)]["nships"].sum()
        player2=SAILING[(SAILING['owner'] == 2) & (SAILING['toisland'] == index) & (SAILING['arriveinnturns'] < 0.5)]["nships"].sum()
        diff=player1-player2
        victor=0
        if (player1 > 0.5) or (player2 > 0.5):
            print('+++++++++++++++')
            print('Player 1 gets '+str(player1)+' ships to island '+str(index))
            print('Player 2 gets '+str(player2)+' ships to island '+str(index))
            if (player1 > 0.5) and (player2 > 0.5):
                print('Sea Battle')
            player1=player1-player2
            if player1 < 0: 
                player2=abs(player1)
                player1=0
                print('Player 2 gets to island with '+str(player2)+' ships left')                
                victor=2
            elif player1 > 0.5:
                player2=0
                print('Player 1 gets to island with '+str(player1)+' ships left')                
                victor=1
            else:
                print('All ships destroyed in sea battle.')
            print('Island (value='+str(value)+') was owned by player '+str(owner)+' with '+str(shipsonisland)+' ships.')

            if victor == 0: 
                print('Not enough ships left, all sink.')
            elif victor == owner:
                ISLANDS.loc[index, 'nships']=ISLANDS.loc[index, 'nships']+player1+player2
            elif owner == 0:
                if value < player1+player2:
                    ISLANDS.loc[index, 'owner']=victor
                    ISLANDS.loc[index, 'nships']=player1+player2
                    print('Player '+str(victor)+' conquered the inhabited island')
                else:
                    print('Not enough ships to take the island. They sink.')
            elif victor != owner:
                print('Fight for the island!')
                shipsleft=round(player1+player2-ISLANDS.loc[index, 'nships']*bonusfactor)
                if shipsleft > 0.5:
                    ISLANDS.loc[index, 'owner']=victor
                    ISLANDS.loc[index, 'nships']=shipsleft
                    print('Island conquered by Player'+str(victor)+'. '+str(shipsleft)+' ships left.')
                else:
                    ISLANDS.loc[index, 'nships']=ISLANDS.loc[index, 'nships']-round((player1+player2)/bonusfactor)
                    print('Island succesfully defended by Player'+str(owner)+'. '+str(ISLANDS.loc[index, 'nships'])+' ships left.')
    SAILING=SAILING[SAILING['arriveinnturns'] > 0.5 ]
    return(ISLANDS, SAILING)




def main():
    print('Welcome to Salamis')
    nislands=4  #actually half the number
    speed=8.    #distance units per turn
    ISLANDS=setupislands(nislands)
    SAILING=pd.DataFrame(data=None, columns=['owner','nships','toisland','arriveinnturns'])

    print('Starting game')
    turn=0
    while whowon(ISLANDS, SAILING) == 0:
        turn+=1
        ISLANDS = getships(ISLANDS)

        for player in range(1,3):
            cls()
            print('============= To Player '+str(player)+'===============')
            turn=True
            while turn is True:
                print('Options:')
                print('    Show map=m')
                print('    Show distances between islands=d')
                print('    Send ships=s')
                print('    Show sailing plan=r')
                print('    End turn=x')
 
                do=input('What do you want to do?: ')
                if do == 'x': turn=False
                if do == 'd': measuredistance(ISLANDS, speed)
                if do == 'm': visualise(ISLANDS, False)
                if do == 's': 
                    ISLANDS, THISSAILING = sendships(ISLANDS,player,speed)
                    SAILING=SAILING.append(THISSAILING, ignore_index=True)

                if do == 'r': showsailingplan(SAILING,player)
                if do != 'x' and do != 'm' and do != 's' and do != 'r' and do != 'd':
                    print('No valid option. Try again')
        cls()
        print('Both players have sent their ships.')

        ISLANDS, SAILING = shipsarrive(ISLANDS, SAILING)


        visualise(ISLANDS)
        input('Press key to continue')


if __name__ == '__main__':
    main()

