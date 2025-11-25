import time
import os
from dotenv import load_dotenv

import matplotlib.pyplot as plt
import numpy as np
import PIL, urllib
from fuzzywuzzy import fuzz, process

from flask import Flask, render_template, request, session
import handlers, config

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

answer = config.answer
SESSION_KEYS = ["image", "answer", "start_time", "best_album", "best"]
uf_dict = {'debut':'Taylor Swift',
           'rep':'Reputation',
           'ttpd':'The Tortured Poets Department',
           'tloas':'The Life of a Showgirl'} 

@app.route("/", methods=["GET", "POST"])
def play():
    if request.method == "GET":
        for skey in SESSION_KEYS:
            session.pop(skey, None)
    global answer
    
    image = session.get("image")
    answer = session.get("answer")
    start_time = session.get("start_time", time.time())
    best_album = session.get("best_album", None)

    msg_prefix = config.msg_prefix
    outcome = config.outcome
    time_taken = config.time_taken
    old_guess = config.old_guess
    
    new_best = None
    
    selection, hex_colors, new_answer, fig, ax, album_pics = handlers.generate_drawing()

    if request.method == "POST":
        guess = request.form.get("guess", "")
        guess = uf_dict[guess] if guess.lower() in uf_dict.keys() else guess
        best_match = handlers.close_matching(guess)
        time_taken = round(time.time() - start_time, 2)  

        if best_match == answer:
            msg_prefix = "Well done!"
            outcome = 1
            new_best = None
            if time_taken < session["best"]:
                session["best"] = min(session["best"], time_taken)
                new_best = 'New personal best!'
                session["best_album"] = album_pics[session["answer"]]
                best_album = session["best_album"]
        else:
            msg_prefix = "Nope!"
            outcome = 0
            new_best = None

        selection, hex_colors, new_answer, fig, ax, album_pics = handlers.generate_drawing()
        fig.savefig(config.path, bbox_inches="tight", pad_inches=0.15, dpi=100)
        plt.close(fig)

        session["start_time"] = time.time()
        old_guess = album_pics[session["answer"]]
        session["answer"] = new_answer
        session["image"] = config.path
        display_image = config.path

    else:
        selection, hex_colors, new_answer, fig, ax, album_pics = handlers.generate_drawing()
        fig.savefig(config.path, bbox_inches="tight", pad_inches=0.15, dpi=100)
        plt.close(fig)

        session["start_time"] = time.time()
        session["answer"] = new_answer
        session["image"] = config.path
        session["best"] = 999
        session["best_answer"] = None
        best_album = session.get("best_album", None)
        display_image = config.path

    return render_template(
        "index.html",
        image=display_image,
        msg_prefix=msg_prefix,
        msg_type=outcome,
        msg_answer=answer,   
        time_taken=time_taken,
        timestamp=int(time.time()*1000),
        new_best=new_best,
        best_score=session["best"] if session["best"]<999 else "No score set yet.",
        album_img=old_guess,
        best_album=best_album
    )

@app.route("/robots.txt")
def robots():
    return "User-agent: *\nDisallow:", 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
