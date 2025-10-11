import os

answer = None
path = "static/game.png"
img_path = os.path.join(os.getcwd(), 'Images', 'question.png')

n_albums=12 # How many albums did Taylor Swift currently release?

msg_prefix=''
outcome=None
time_taken=None
old_guess='https://github.com/Alex-Caian/Taylor_Swift/blob/main/Images/question.png?raw=True'