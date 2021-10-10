# game.py
# allows you to play the solitaire game

import PositionClass

def interactivePlay():
    stop = False
    pos = PositionClass.PositionClass()
    while not stop:
        print()
        k = input("Input your move:")
        if k=="q":
            stop = True
    #end while
#end interactivePlay

interactivePlay()