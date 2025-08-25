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

@app.route("/", methods=["GET", "POST"])
def play():
    global answer
    msg = 'Welcome to the guess the album game!'
    
    image = session.get("image")
    answer = session.get("answer")
    start_time = session.get("start_time", time.time())
    
    if request.method == "POST":
        guess = request.form.get("guess", "")
        best_match = handlers.close_matching(guess)
        start_time = session.get("start_time", time.time())
        taken = time.time() - start_time
        
        if best_match == answer:
            msg = f"Well done! The answer was {answer}.\nTime taken: {round(taken,2)}s"
            outcome = 1
        else:
            msg = f"Nope! =( The answer was {answer}.\nTime taken: {round(taken,2)}s"
            outcome = 0
    
    albums = handlers.get_albums()
    selection, hex_colors, answer, fig, ax = handlers.generate_drawing()
    fig.savefig(config.path)
    plt.close(fig)
    
    session["start_time"] = time.time()
    session["answer"] = answer
    session["image"] = config.path
    display_image = image if image else config.path
    
    return render_template("index.html", image=display_image, message=msg, message_type=outcome timestamp=int(time.time()*1000))
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)