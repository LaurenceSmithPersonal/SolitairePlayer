# game.py
# allows you to play the solitaire game

import PositionClass

def interactivePlay():
    """ Allows you to play an interactive game of solitaire """
    stop = False
    pos = PositionClass.PositionClass()
    pos.setUp()
    print(pos.gameStr())
    while not stop:
        print()
        k = input("Input your move:")
        if k=="q":
            stop = True
            print("Thank you for playing")
        elif k=="h":
            s = """keys:
            q = quit
            h = help
            1 = move stock to waste (and back)
            2 = move waste to foundation
            10-16 = move tableau piles 0 to 6 to foundation
            20-26 = move waste to tableau pile 0 to 6
            100 - 136 = code - 1ij - move foundation pile i to tableau pile j
            10000 - 16613 = code - 1ijkl - move kl cards from tableau pile i to tableau pile j
            """
            print(s)
        elif k.isdigit():
            ret = pos.moveByNumber(int(k))
            if ret == False:
                print("Move not recognised")
            else:    
                print(pos.gameStr())
        else: 
            ret = False
            print("Move not recognised")
    #end while
    
#end interactivePlay

if __name__ == "__main__":
    interactivePlay()
# End if __name__ == "__main__":