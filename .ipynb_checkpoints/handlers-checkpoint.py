import json
import random
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
#import matplotlib.image as mpimg

import urllib
from PIL import Image
import numpy as np

from fuzzywuzzy import fuzz, process
import config

def get_albums():
    with open('albums.json', 'rb') as temp:
            resp = json.load(temp)
    temp.close()
    return resp

def close_matching(user_input, docs=get_albums()):
    choices = set(docs.keys())
    similarities = [fuzz.ratio(user_input, choice) for choice in choices]
    best_match = process.extractOne(user_input, choices)[0]
    return best_match

def generate_session():
    albums = get_albums()
    
    selection = set(random.sample(list(albums.keys()), k=10))
    hex_colors = [albums[album] for album in selection]
    answer = list(set(albums.keys()) - selection)[0]
    
    return selection, hex_colors, answer

# def generate_drawing():
#     fig, ax = plt.subplots()
#     selection, hex_colors, answer = generate_session()
    
#     for i, hex_color in enumerate(hex_colors):
#         row = i // 5  
#         col = i % 5  
#         x = 0.01 + col * 0.25  
#         y = 0.6 - row * 0.3 

#         square = plt.Rectangle((x, y), 0.2, 0.2, fill=True, color=hex_color)
#         ax.add_patch(square)

#     ax.set_aspect('equal')
#     ax.set_xticks([])
#     ax.set_yticks([])
#     ax.set_xlim(0, 1.25)
    
#     with urllib.request.urlopen(config.url) as response:
#         question = np.array(Image.open(response).convert("RGBA"))

#     custom_patch = OffsetImage(question, zoom=0.08)
#     ab = AnnotationBbox(custom_patch, (.63, 0), frameon=False)
#     ax.add_artist(ab)
#     ax.axis("off")
    
#     return selection, hex_colors, answer, fig, ax

def generate_drawing():
    fig, ax = plt.subplots(figsize=(6,4))
    
    selection, hex_colors, answer = generate_session()
    
    for i, hex_color in enumerate(hex_colors):
        row = i // 5  
        col = i % 5  
        x = 0.01 + col * 0.25  
        y = 0.6 - row * 0.3 

        square = plt.Rectangle((x, y), 0.2, 0.2, fill=True, color=hex_color)
        ax.add_patch(square)

    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 1.23)
    ax.set_ylim(0.18, 0.82)
    
    with urllib.request.urlopen(config.url) as response:
        question = np.array(Image.open(response).convert("RGBA"))

    custom_patch = OffsetImage(question, zoom=0.06)
    ab = AnnotationBbox(custom_patch, (.63, 0.2), frameon=False)
    ax.add_artist(ab)
    ax.axis("off")
    
    fig.tight_layout(pad=0.5)
    
    return selection, hex_colors, answer, fig, ax

