## Solitaire Player

Creates a game of solitaire, PositionClass.py stores the position and all possible moves (still work in progress)  
  
Then idea is to try different strategies to see which is best.  
Hopefully will try reinforcement learning 

Key codes for moves:  
    q = quit  
    h = help  
    1 = move stock to waste (and back)  
    2 = move waste to foundation  
    10-16 = move tableau piles 0 to 6 to foundation  
    20-26 = move waste to tableau pile 0 to 6  
    100 - 136 = code - 1ij - move foundation pile i to tableau pile j  
    10000 - 16613 = code - 1ijkl - move kl cards from tableau pile i to tableau pile j  