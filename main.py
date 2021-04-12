from tkinter import *
import random
import pandas as pd
import json

BACKGROUND_COLOR = "#B1DDC6"

df = pd.read_csv('data/Korean_English.csv')
dictionary = df.to_dict(orient='records')
side = ''
known_list = []
unknown_list = []
side = 'front'


# ------------------------------ FUNCTIONS ---------------------------------- #
def flip_card():
    global side
    if side == 'front':
        canvas.itemconfig(canvas_image, image=back_image)
        english = random_word["English"]
        canvas.itemconfig(canvas_text, text=english, fill='white')
        side = 'back'
    else:
        canvas.itemconfig(canvas_image, image=front_image)
        korean = random_word["Korean"]
        canvas.itemconfig(canvas_text, text=korean, fill='black')
        side = 'front'


def get_word():
    global random_word
    random_word = random.choice(dictionary)
    canvas.itemconfig(canvas_image, image=front_image)
    korean = random_word["Korean"]
    canvas.itemconfig(canvas_text, text=korean, fill='black')


def correct():
    known_list.append(random_word)
    try:
        with open('data/known_words.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError or json.decoder.JSONDecodeError:
        with open('data/known_words.json', 'w') as f:
            json.dump(known_list, f, indent=2)
    else:
        data.append(random_word)
        with open('data/known_words.json', 'w') as f:
            json.dump(data, f, indent=2)
    finally:
        dictionary.remove(random_word)
        get_word()


def wrong():
    unknown_list.append(random_word)
    try:
        with open('data/words_to_learn.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        with open('data/words_to_learn.json', 'w') as f:
            json.dump(unknown_list, f, indent=2)
    else:
        data.append(random_word)
        with open('data/words_to_learn.json', 'w') as f:
            json.dump(data, f, indent=2)
    get_word()


# ------------------------------ UI SETUP ---------------------------------- #
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title('Flashy')

canvas = Canvas()
canvas.config(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_image = PhotoImage(file='images/card_front.png')
back_image = PhotoImage(file='images/card_back.png')
canvas_image = canvas.create_image(400, 263, image=front_image)
canvas_text = canvas.create_text(400, 263, text='', font=('Arial', 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=3)
get_word()

# Buttons
correct_image = PhotoImage(file='images/right.png')
correct_button = Button(image=correct_image, command=correct, highlightthickness=0, bg=BACKGROUND_COLOR, relief='flat',
                        borderwidth=0,
                        activebackground=BACKGROUND_COLOR)
correct_button.grid(column=2, row=1)

wrong_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_image, command=wrong, highlightthickness=0, bg=BACKGROUND_COLOR, relief='flat',
                      borderwidth=0,
                      activebackground=BACKGROUND_COLOR)
wrong_button.grid(column=0, row=1)

flip_image = PhotoImage(file='images/flip.png')
flip_button = Button(image=flip_image, command=flip_card, highlightthickness=0, bg=BACKGROUND_COLOR, relief='flat',
                     borderwidth=0,
                     activebackground=BACKGROUND_COLOR)
flip_button.grid(column=1, row=1)

window.mainloop()
