from tkinter import *
from gameboard import WordleGame


window = Tk()
window.title("Wordle: By Tariq Brown")

current_game = WordleGame(window,"trees")


window.mainloop()
