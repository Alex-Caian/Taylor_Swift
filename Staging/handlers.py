import json
import random
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

def get_albums():
    with open('albums.json', 'rb') as temp:
            resp = json.load(temp)
    temp.close()
    return resp

def generate_session():
    albums = get_albums()
    
    selection = set(random.sample(list(albums.keys()), k=10))
    hex_colors = [albums[album] for album in selection]
    answer = list(set(albums.keys()) - selection)[0]
    
    return selection, hex_colors, answer

def generate_drawing():
    fig, ax = plt.subplots()
    selection, hex_colors, answer = generate_session()
    
    for i, hex_color in enumerate(hex_colors):
        row = i // 5  
        col = i % 5  
        x = 0.02 + col * 0.25  
        y = 0.6 - row * 0.4 

        square = plt.Rectangle((x, y), 0.2, 0.2, fill=True, color=hex_color)
        ax.add_patch(square)

    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 1.25)
    custom_image = mpimg.imread("https://github.com/Alex-Caian/Taylor_Swift/blob/main/Images/question.png?raw=True")

    custom_patch = OffsetImage(custom_image, zoom=0.08)
    ab = AnnotationBbox(custom_patch, (.63, 0), frameon=False)
    ax.add_artist(ab)
    ax.axis("off")
    
    return selection, hex_colors, answer, fig, ax