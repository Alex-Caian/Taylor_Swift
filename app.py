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
    
    image = session.get("image")
    answer = session.get("answer")
    start_time = session.get("start_time", time.time())

    msg_prefix = config.msg_prefix
    outcome = config.outcome
    time_taken = config.time_taken

    if request.method == "POST":
        guess = request.form.get("guess", "")
        best_match = handlers.close_matching(guess)
        time_taken = round(time.time() - start_time, 2)

        if best_match == answer:
            msg_prefix = "Well done!"
            outcome = 1
        else:
            msg_prefix = "Nope!"
            outcome = 0

        selection, hex_colors, new_answer, fig, ax = handlers.generate_drawing()
        fig.savefig(config.path)
        plt.close(fig)

        session["start_time"] = time.time()
        session["answer"] = new_answer
        session["image"] = config.path
        display_image = config.path

    else:
        selection, hex_colors, new_answer, fig, ax = handlers.generate_drawing()
        fig.savefig(config.path)
        plt.close(fig)

        session["start_time"] = time.time()
        session["answer"] = new_answer
        session["image"] = config.path
        display_image = config.path

    return render_template(
        "index.html",
        image=display_image,
        msg_prefix=msg_prefix,
        msg_type=outcome,
        msg_answer=answer,   
        time_taken=time_taken,
        timestamp=int(time.time()*1000),
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
