EXPIRE = 3600

import time
import os

import numpy as np
import PIL, urllib
from fuzzywuzzy import fuzz, process

import handlers

def play():
    albums = handlers.get_albums()
    selection, hex_colors, answer, fig, ax = handlers.generate_drawing()
    fig.show()
    
    now = time.time()
    n = input("Which album is missing?:  ")
    choices = set(albums.keys())
    similarities = [fuzz.ratio(n, choice) for choice in choices]
    best_match = process.extractOne(n, choices)[0]
    
    if best_match == answer:
        msg = f"Well done! The answer was {answer}"
        print(msg)
    else:
        msg = f"Nope! The answer was {answer}"
        print(msg)
        return msg
    end = time.time() - now
    
    print(f"Your time was: {round(end,2)}s")
    return msg

play()