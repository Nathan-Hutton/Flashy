from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
card = {}

def create_card():
    global card, timer
    window.after_cancel(timer)
    card = random.choice(data_dict)
    create_french_card()
    timer = window.after(3000, create_english_card)

def create_french_card():
    canvas.itemconfig(card_image, image=front_of_card)
    canvas.itemconfig(language_text, text="French", fill='black')
    canvas.itemconfig(word_text, text=card['French'], fill='black')

def create_english_card():
    canvas.itemconfig(card_image, image=back_of_card)
    canvas.itemconfig(language_text, text="English", fill='white')
    canvas.itemconfig(word_text, text=card['English'], fill='white')

def discard_card():
    global data
    data_dict.remove(card)
    data = pandas.DataFrame.from_dict(data_dict)
    data.to_csv("data/words_to_learn.csv", index=False)

#Window

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.geometry('+5+5')
timer = window.after(0, create_card)

#Pandas
try:
    data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    data = pandas.read_csv('data/french_words.csv')
data_dict = data.to_dict(orient='records')

#Canvas

front_of_card = PhotoImage(file='images/card_front.png')
back_of_card = PhotoImage(file='images/card_back.png')
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image = canvas.create_image(400, 268, image=front_of_card)
canvas.grid(column=0, row=0, columnspan=2)
language_text = canvas.create_text(400, 150, text="Language", font=["Arial", 40, "italic"])
word_text = canvas.create_text(400, 263, text="Word", font=["Arial", 60, "bold"])

#Buttons

x_image = PhotoImage(file='images/wrong.png')
x_button = Button(image=x_image, highlightthickness=0, command=create_card)
x_button.grid(column=0, row=1)
check_image = PhotoImage(file='images/right.png')
check_button = Button(image=check_image, highlightthickness=0, command=lambda: [discard_card(), create_card()])
check_button.grid(column=1, row=1)

window.mainloop()