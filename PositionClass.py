# PositionClass.py
# Laurence Smith
# 27/09/2021

# To hold the position of the cards for playing solitaire (Canfield)
# also related useful classes: 
# CardClass - to hold card details
# values 1 is A, 13 is king

# alternative idea is to just have a deck of cards and give each card a position which is it's place in the game, 
# then just need to change positions of cards around. Might be easier for machine learning

# used https://github.com/suryadutta/solitaire/blob/master/card_elements.py for help with coding

# ToDo 
#   - create index for each card, with a value if don't know what card is
#   - create index for positions
#   - reading in positions
#   - writing out positions
#   - create index for moves
#   - scoring function or check if won function

#   - game class for playing games / simulating games
#   - commit and push to GitHub


import numpy as np
import random
from copy import deepcopy
import pandas as pd

deckDetails = pd.read_csv("deckdetails.csv") #dataframe of card details


global CLUBS
CLUBS = "clubs"
global DIAMONDS
DIAMONDS = "diamonds"
global HEARTS
HEARTS = "hearts"
global SPADES
SPADES = "spades"
global RED
RED = "red"
global BLACK
BLACK = "black"

class CardClass:
    """ class to hold a single card """
    def __init__(self, idIn, valueTextIn, valueNumIn, suitTextIn, suitUnicodeIn, colourIn):
        # global CLUBS
        # global DIAMONDS
        # #global HEARTS
        # global SPADES
        # global RED
        # global BLACK
        
        self.id = idIn
        self.valueText = valueTextIn
        self.value = valueNumIn
        self.suit = suitTextIn 
        self.suitUnicode = suitUnicodeIn 
        self.colour = colourIn
        self.visible = False
    #end __init__
    
    def flip(self):
        self.visible = not self.visible
    
    def __str__(self):        
        return "{0}{1} visible: {2}".format(self.valueText,chr(self.suitUnicode), self.visible)

    def gameStr(self): 
        if self.visible:
            return "{0}{1}".format(self.valueText,chr(self.suitUnicode))
        else:
            return "##"
# end CardClass

class DeckClass:
    """ class to hold full deck of cards """
    def __init__(self, cardDetails, shuffle=True):
        self.cards = []
        self.populate(cardDetails)
        if shuffle:
            self.shuffle()
    
    def populate(self, cardDetails):
        for i in np.arange(0,52):
            self.cards.append(CardClass(
                cardDetails["ID"][i]
                ,cardDetails["ValueText"][i]
                ,cardDetails["ValueNum"][i]
                ,cardDetails["SuitText"][i]
                ,cardDetails["SuitUnicode"][i]
                ,cardDetails["Colour"][i]
                ))
    #end populate

    def shuffle(self):
        random.shuffle(self.cards)

    def __str__(self):
        return ", ".join([str(card) for card in self.cards])
# end DeckClass

class StockClass:
    """ top left pile from which cards are turned to waste pile """
    def __init__(self) -> None:
        self.cards = []
    
    def __str__(self):
        return ", ".join([str(card) for card in self.cards])

    def gameStr(self):
        return ", ".join([card.gameStr() for card in self.cards])

    def addCard(self, cardIn):
        cardIn.visible = True   #make all visible as could always just go through them all first
        self.cards.append(cardIn)
# end StockClass

class WasteClass:
    """ top second left pile from which cards are turned into from stock pile """
    def __init__(self) -> None:
        self.cards = []
    
    def __str__(self):
        return ", ".join([str(card) for card in self.cards])

    def gameStr(self):
        return ", ".join([card.gameStr() for card in self.cards])

    def addCard(self, cardIn):
        cardIn.visible = True
        self.cards.append(cardIn)
# end WasteClass

class FoundationPileClass:
    """ Foundation pile where you build up suits from A to K to win, will need 4 of these, one for each suit """
    def __init__(self, suitIn) -> None:
        self.cards = []
        self.suit = suitIn
    
    def __str__(self):
        if len(self.cards) == 0:
            return "empty foundation pile for suit " + str(self.suit)
        else: 
            return ", ".join([str(card) for card in self.cards])

    def gameStr(self):
        if len(self.cards) == 0:
            return "empty foundation pile for suit " + str(self.suit)
        else: 
            return ", ".join([card.gameStr() for card in self.cards])

    def addCard(self, cardIn):
        # check to see if can add it
        if not isinstance(cardIn, CardClass):
            return False
        elif not cardIn.suit == self.suit:
            return False
        elif len(self.cards) == 0 and (not cardIn.value == 1):  #empty pile and an ace
            return False
        elif len(self.cards) == 0:  # must be an ace
            self.cards.append(cardIn) # add card
            return True
        elif self.cards[-1].value == 13: #already a King on pile
            return False
        elif self.cards[-1].value == (cardIn.value - 1): # last card on pile is one less than card trying to put on
            self.cards.append(cardIn) # add card
            return True
        else: # must be same suit but not right number
            return False
        # end if
    # end addCard
# end FoundationPileClass

def testFoundationPileClass():
    # testing
    print("\nTest: can add correct ace to right empty pile")
    heartPile = FoundationPileClass(HEARTS)
    HA = CardClass(26,"A",1,"hearts", 9829, "red")
    HA.flip()
    print(heartPile.addCard(HA))
    print(str(heartPile))
    print(heartPile.gameStr())

    print("\nTest: can't add wrong ace to right empty pile")
    heartPile = FoundationPileClass(HEARTS)
    SA = CardClass(39,"A",1,"spades", 9824, "black")
    SA.flip()
    print(heartPile.addCard(SA))
    print(str(heartPile))
    print(heartPile.gameStr())
    
    
    #deck = DeckClass()
#end testFoundationPileClass

#testFoundationPileClass()

class TableauPileClass:
    # Tableau pile where you build down cards and start with some face down
    def __init__(self) -> None:
        self.cards = []
    
    def __str__(self):
        return ", ".join([str(card) for card in self.cards])

    def gameStr(self):
        return ", ".join([card.gameStr() for card in self.cards])

    def addCard(self, cardIn):
        # for adding cards during the game
        # check to see if can add it
        if not isinstance(cardIn, CardClass):
            return False
        elif len(self.cards) == 0 and (not cardIn.value == 13):  #empty pile and not a king
            return False
        elif len(self.cards) == 0:  # must be a king
            self.cards.append(cardIn) # add card
            return True
        elif cardIn.colour == self.cards[-1].colour:  #same colour
            return False
        elif self.cards[-1].value == (cardIn.value + 1): # last card on pile is one more than card trying to put on
            self.cards.append(cardIn) # add card
            return True
        else: # must be different colour but not right number
            return False
        # end if
    # end addCard

    def addSetUpCard(self, cardIn):
        # for adding cards during set up period
        self.cards.append(cardIn)
    #end addSetUpCard
# end TableauPileClass

def testTableauPileClass():
    print("\ntestTableauPileClass")
    print("\nAdd King to empty pile:")


    print("\nAdd non-King to empty pile:")
# end testTableauPileClass
    

class PositionClass():
    """ hold all the cards needed for a game """
    def __init__(self):
        self.stock = StockClass()
        self.waste = WasteClass()
        self.foundationPiles = []
        self.foundationPiles.append(FoundationPileClass(CLUBS))
        self.foundationPiles.append(FoundationPileClass(DIAMONDS))
        self.foundationPiles.append(FoundationPileClass(HEARTS))
        self.foundationPiles.append(FoundationPileClass(SPADES))
        self.tableauPiles = []
        for i in np.arange(0,7):
            self.tableauPiles.append(TableauPileClass())
        #end for
    #end __init__

    def __str__(self) -> str:
        foundStr0 = "Foundation Clubs: " + str(self.foundationPiles[0])
        foundStr1 = "Foundation Diamonds: " + str(self.foundationPiles[1])
        foundStr2 = "Foundation Hearts: " + str(self.foundationPiles[2])
        foundStr3 = "Foundation Spades: " + str(self.foundationPiles[3])
        stockStr = "Stock: " + str(self.stock)
        wasteStr = "Waste: " + str(self.waste)
        tableauStr = "Tableau:\n"
        for i in np.arange(0,7):
            tableauStr = tableauStr + "Pile " + str(i) + ": " + str(self.tableauPiles[i]) + "\n"

        return "Position:\n" + foundStr0 + "\n" + foundStr1 + "\n" + foundStr2 + "\n" + foundStr3 + "\n" + stockStr + "\n" + wasteStr + "\n" + tableauStr
    #end __str__

    def gameStr(self) -> str:
        foundStr0 = "Foundation Clubs: " + self.foundationPiles[0].gameStr()
        foundStr1 = "Foundation Diamonds: " + self.foundationPiles[1].gameStr()
        foundStr2 = "Foundation Hearts: " + self.foundationPiles[2].gameStr()
        foundStr3 = "Foundation Spades: " + self.foundationPiles[3].gameStr()
        stockStr = "Stock: " + self.stock.gameStr()
        wasteStr = "Waste: " + self.waste.gameStr()
        tableauStr = "Tableau:\n"
        for i in np.arange(0,7):
            tableauStr = tableauStr + "Pile " + str(i) + ": " + self.tableauPiles[i].gameStr() + "\n"

        return "Position:\n" + foundStr0 + "\n" + foundStr1 + "\n" + foundStr2 + "\n" + foundStr3 + "\n" + stockStr + "\n" + wasteStr + "\n" + tableauStr
    #end __str__

    def setUp(self):
        """put everything into position to start a random game"""
        deck = DeckClass(deckDetails)
        #fill tableau
        for i in np.arange(0,7):
            for j in np.arange(0, i+1):
                #print("i=",i," j=",j)
                self.tableauPiles[i].addSetUpCard(deepcopy(deck.cards[0])) #ToDo do we need a copy here - but can't copy the class?
                deck.cards.pop(0)
        #end for 1

        #flip top card
        for i in np.arange(0,7):
            self.tableauPiles[i].cards[i].flip()
        
        #put rest of cards in stock
        for card in deck.cards:
            self.stock.addCard(card)
    #end setUp

    def moveStockToWaste(self):
        """ moves cards from stock to waste or all back to stock if stock is empty """
        if len(self.stock.cards) == 0:
            if len(self.waste.cards) == 0:
                # no stock or waste so can't do move
                return False
            else:
                # move waste back to stock, the bottom card in waste needs to become top card in stock
                for card in self.waste.cards:
                    self.stock.cards.insert(0, deepcopy(card)) #need to copy otherwise it is removed when we delete it, insert at start to get correct order
                    #self.waste.cards.remove(card) # doesn't work as removing messes up iteration add in another for loop below
                self.waste.cards = [] #no cards in waste
                #for card in self.stock.cards:
                #    card.visible = False
                return True
        else: # cards in stock so move 3 cards from stock to waste (or fewer if fewer available)
            for i in np.arange(0,3):
                if len(self.stock.cards) > 0:
                    card = self.stock.cards[-1]
                    self.waste.addCard(deepcopy(card))
                    self.stock.cards.remove(card)
            return True
    #end moveStockToWaste        

    def moveWasteToFoundation(self):
        """ moves a card from Stock to correct Foundation """
        if len(self.waste.cards) == 0:
            return False
        else:
            card = deepcopy(self.waste.cards[-1])
            for pile in self.foundationPiles:
                if card.suit == pile.suit:
                    ret = pile.addCard(card)
                    if ret == True:
                        self.waste.cards.remove(self.waste.cards[-1])
            return ret
    #end moveWasteToFoundation

    def moveTableauToFoundation(self, tableauNum):
        """ moves a card from Tableau to correct Foundation """
        if tableauNum < 0 or tableauNum > 6:
            print("tableauNum:", tableauNum, " not allowed!")
            return False
        elif len(self.tableauPiles[tableauNum].cards) == 0:
            return False
        else:
            card = deepcopy(self.tableauPiles[tableauNum].cards[-1])
            for pile in self.foundationPiles:
                if card.suit == pile.suit:
                    ret = pile.addCard(card)
                    if ret == True:
                        self.tableauPiles[tableauNum].cards.remove(self.tableauPiles[tableauNum].cards[-1]) # remove card from pile
                        if len(self.tableauPiles[tableauNum].cards) > 0: # if any cards left in tableau
                            self.tableauPiles[tableauNum].cards[-1].visible = True # make new top card visible
            return ret
    #end moveTableauToFoundation

    def moveFoundationToTableau(self, foundationNum, tableauNum):
        """ moves a card from Foundation to stock """
        if tableauNum < 0 or tableauNum > 6:
            print("tableauNum:", tableauNum, " not allowed!")
            return False
        elif foundationNum < 0 or foundationNum > 3:
            print("foundationNum:", foundationNum, " not allowed!")
            return False    
        elif len(self.foundationPiles[foundationNum].cards) == 0:  #no cards in foundation pile
            return False
        else:
            card = deepcopy(self.foundationPiles[foundationNum].cards[-1])
            ret = self.tableauPiles[tableauNum].addCard(card)
            if ret == True: # move was ok
                self.foundationPiles[foundationNum].cards.pop(-1) #remove card from foundation pile
            # else: #move not ok return False
            return ret
        #ToDo need to test this function
    #end moveFoundationToTableau

    def moveWasteToTableau(self, tableauNum):
        """ moves card from Waste to Tableau """
        if tableauNum < 0 or tableauNum > 6:
            print("tableauNum:", tableauNum, " not allowed!")
            return False
        elif len(self.waste.cards) == 0:
            print("No cards in waste to move")
            return False
        else:
            card = deepcopy(self.waste.cards[-1])
            ret = self.tableauPiles[tableauNum].addCard(card)
            if ret == True: # move was ok
                self.waste.cards.pop(-1) #remove card from foundation pile
            # else: #move not ok return False
            return ret

    def moveTableauToTableau(self, startTableauNum, endTableauNum, numCards):
        """ moves cards from Tableau to another Tableau """
        ok_to_move = False
        if startTableauNum < 0 or startTableauNum > 6:
            print("startTableauNum:", startTableauNum, " not allowed!")
            ok_to_move = False
        elif endTableauNum < 0 or endTableauNum > 6:
            print("endTableauNum:", endTableauNum, " not allowed!")
            ok_to_move = False        
        elif len(self.tableauPiles[startTableauNum].cards) < numCards:  #trying to move more cards than exist
            ok_to_move = False
        elif self.tableauPiles[startTableauNum].cards[-numCards].visible == False:   # check whether top card in start Tableau is visible
            ok_to_move = False
        elif len(self.tableauPiles[endTableauNum].cards) == 0:  #moving to an empty pile
            if self.tableauPiles[startTableauNum].cards[-numCards].value == 13:  #It is a king so can move to empty pile
                ok_to_move = True
            else:
                ok_to_move = False  # Not a king
        # don't need to do all below checks as done as part of addCard but might be useful
        elif self.tableauPiles[endTableauNum].cards[-1].visible == False:   # check whether bottom card in end tableau is visible
            ok_to_move = False
        elif self.tableauPiles[startTableauNum].cards[-numCards].colour == self.tableauPiles[endTableauNum].cards[-1].colour:   # check whether bottom card in end tableau is the right colour
            ok_to_move = False
        elif self.tableauPiles[startTableauNum].cards[-numCards].value != self.tableauPiles[endTableauNum].cards[-1].value - 1: # check whether bottom card in end tableau is the wrong value
            ok_to_move = False
        else: # move the cards
            ok_to_move = True

        if ok_to_move:
            #move cards
            #put cards in end pile
            for i in np.arange(-numCards, 0,1):
                card = deepcopy(self.tableauPiles[startTableauNum].cards[i])
                ret = self.tableauPiles[endTableauNum].addCard(card)
            
            #remove cards from start pile
            for i in np.arange(-numCards, 0,1):
                self.tableauPiles[startTableauNum].cards.pop(-1)
            
            # if card left in start pile then make it visible
            if len(self.tableauPiles[startTableauNum].cards) > 0:
                self.tableauPiles[startTableauNum].cards[-1].visible = True # make new top card visible
            return True
        else:
            return False
    #end moveTableauToTableau

    def moveByNumber(self, num):
        """ takes a number in, which controls what move to do """
        if num==1:
            ret=self.moveStockToWaste()
        elif num==2:
            ret=self.moveWasteToFoundation()
        elif num>=10 and num <= 16:  # move tableau to foundation
            lastDigit = int(str(num)[-1]) # gets final digit
            ret=self.moveTableauToFoundation(lastDigit)
        elif num>=20 and num <= 26:  # move waste to tableau pile 0 to 6
            lastDigit = int(str(num)[-1]) # gets final digit
            ret=self.moveWasteToTableau(lastDigit) #still need to code!
        elif num>=100 and num <= 136:  # code - 1ij - move foundation pile i to tableau pile j
            foundationNum = int(str(num)[-2])
            tableauNum = int(str(num)[-1])
            ret=self.moveFoundationToTableau(foundationNum,tableauNum)
        elif num >= 10000 and num <= 16613:  # code - 1ijkl - move kl cards from tableau pile i to tableau pile j
            tableauFromNum = int(str(num)[1])
            print("tableauFromNum = ", tableauFromNum)
            tableauToNum = int(str(num)[2])
            print("tableauToNum = ", tableauToNum)
            cardsToMove = int(str(num)[3] + str(num)[4])
            print("cardsToMove = ", cardsToMove)
            ret=self.moveTableauToTableau(tableauFromNum, tableauToNum, cardsToMove)
        else:
            ret=False
        return ret
    #end moveByNumber
#end PositionClass

def testPositionClass():
    print("testing PositionClass")
    position = PositionClass()
    print("position created")
    position.setUp()
    print("finished set up")
    print("Print position")
    print(str(position))
    print(position.gameStr())

    # test moving each tableau to foundation
    for i in np.arange(0,7):
        moved = position.moveTableauToFoundation(i)
        print("Moved: ", moved)
        if moved:
            print(str(position))

    # test moving stock to waste and back
    # print(str(position))
    # print("Testing moveStock")
    # print("moveWasteToFoundation: ", position.moveWasteToFoundation())
    # position.moveStockToWaste()
    # print(str(position))
    # print("Testing moveStock")
    # print("moveWasteToFoundation: ", position.moveWasteToFoundation())
    # position.moveStockToWaste()
    # print(str(position))
    # print("Testing moveStock")
    # print("moveWasteToFoundation: ", position.moveWasteToFoundation())
    # position.moveStockToWaste()
    # print(str(position))
    # print("Testing moveStock")
    # print("moveWasteToFoundation: ", position.moveWasteToFoundation())
    # position.moveStockToWaste()
    # print(str(position))
    # print("Testing moveStock")
    # print("moveWasteToFoundation: ", position.moveWasteToFoundation())
    # position.moveStockToWaste()
    # print(str(position))
    # print("Testing moveStock")
    # print("moveWasteToFoundation: ", position.moveWasteToFoundation())
    # position.moveStockToWaste()
    # print(str(position))
    # print("Testing moveStock")
    # print("moveWasteToFoundation: ", position.moveWasteToFoundation())
    # position.moveStockToWaste()
    # print(str(position))
    # print("Testing moveStock")
    # print("moveWasteToFoundation: ", position.moveWasteToFoundation())
    # position.moveStockToWaste()
    # print(str(position))
    # print("Testing moveStock")
    # print("moveWasteToFoundation: ", position.moveWasteToFoundation())
    # position.moveStockToWaste()
    # print(str(position))
#end testPositionClass

if __name__ == "__main__":
    #testPositionClass()
    #test
    #deck = DeckClass(deckDetails,shuffle=False)
    #print(str(deck))
    #testFoundationPileClass()

    #test
    pass
# End if __name__ == "__main__":