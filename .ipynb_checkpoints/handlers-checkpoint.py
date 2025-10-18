import json
import random
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

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

def close_matching(user_input, docs=get_albums()["colours"]):
    choices = set(docs.keys())
    similarities = [fuzz.ratio(user_input, choice) for choice in choices]
    best_match = process.extractOne(user_input, choices)[0]
    return best_match

def generate_session():
    albums = get_albums()["colours"]
    images = get_albums()["images"]
    
    selection = set(random.sample(list(albums.keys()), k=config.n_albums-1))
    hex_colors = [albums[album] for album in selection]
    answer = list(set(albums.keys()) - selection)[0]
    
    return selection, hex_colors, answer, images

def generate_drawing():
    fig, ax = plt.subplots(figsize=(9,4))
    
    selection, hex_colors, answer, images = generate_session()
    
    cols = 6
    rows = 2
    total_slots = rows * cols
    
    hex_colors = random.sample(hex_colors, k=len(hex_colors))
    for i, hex_color in enumerate(hex_colors):
        row = i // cols  
        col = i % cols  
        x = 0.01 + col * 0.25  
        y = 0.6 - row * 0.35
        
        square = plt.Rectangle((x, y), 0.2, 0.2, fill=True, color=hex_color)
        ax.add_patch(square)
        
    if len(hex_colors) < total_slots:
        q_index = len(hex_colors)
        row = q_index // cols
        col = q_index % cols
        x = 0.01 + col * 0.25
        y = 0.6 - row * 0.35
        
        question = np.array(Image.open(config.img_path).convert("RGBA"))
        ax.imshow(question, extent=(x, x + 0.16, y, y + 0.2))
        
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 1.48)
    ax.set_ylim(0.22, 0.82)
    
    ax.axis("off")
    ax.margins(0)
    
    fig.tight_layout(pad=0.35)
    
    return selection, hex_colors, answer, fig, ax, images

