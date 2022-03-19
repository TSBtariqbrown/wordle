from tkinter import *
import random

class WordleGame:
    def __init__(self, window, word=""):
        self.window = window
        self.createDict()
        if word == "":
            word = self.generateWord()
        self.word = word
        self.playBoard_matrix = []
        self.letterGrid_matrix = []
        self.attempt = 0
        self.createPlayBoard()
        self.createEntryBox()
        self.createLetterGrid()
        self.createUpdateBar()
        # ADD ERROR HANDLING

    def createPlayBoard(self):
        self.playBoard = Frame(self.window)
        self.playBoard.pack()

        for row in range (6):
            labelRow = []
            for col in range(5):
                label = Label(self.playBoard, text="", bg="white", font="Times 48", height=1, width=2, borderwidth=2, relief="solid")
                label.grid(row=row, padx=3, pady=5, column=col)
                labelRow.append(label)
            self.playBoard_matrix.append(labelRow)
        # ADD ERROR HANDLING
    

    def createEntryBox(self):
        self.entryBox = Frame(self.window)
        self.entryBox.pack()

        self.wordEntry = Entry(self.entryBox, width=20, bg="white", font="Times 12", justify="center")
        self.wordEntry.pack(side=LEFT, padx=3, pady=5)

        self.submitButton = Button(self.entryBox, text="ENTER", width=6, command=self.click)
        self.submitButton.pack(side=RIGHT)
        # ADD ERROR HANDLING


    def createLetterGrid(self):
        self.letterGrid = Frame(self.window)
        self.letterGrid.pack()

        letter = 65
        for row in range (2):
            labelRow = []
            for col in range(10):
                label = Label(self.letterGrid, text=chr(letter), bg="white", font="Times 20", height=1, width=2, borderwidth=2, relief="solid")
                label.grid(row=row, padx=3, pady=5, column=col)
                labelRow.append(label)
                letter += 1
            self.letterGrid_matrix.append(labelRow)
        labelRow = []
        for col in range(6):
                label = Label(self.letterGrid, text=chr(letter), bg="white", font="Times 20", height=1, width=2, borderwidth=2, relief="solid")
                label.grid(row=3, padx=3, pady=5, column=col)
                labelRow.append(label)
                letter += 1
        self.letterGrid_matrix.append(labelRow)
        # ADD ERROR HANDLING
    

    def createUpdateBar(self):
        self.updateBar = Frame(self.window)
        self.updateBar.pack(side=RIGHT)

        self.statusBar = Label(self.updateBar, text="Ready to play!", font="Times 12")
        self.statusBar.pack()
        #ADD ERROR HANDLING


    def click(self):
        right_count = 0
        guess = self.wordEntry.get()
        if len(guess) != 5:
            self.statusBar.config(text = "Word needs to be 5 letters long!")
        elif [1 if ord(i) in range(65,91) or ord(i) in range(97,123) else 0 for i in guess] != [1,1,1,1,1]:
            self.statusBar.config(text = "Word can only have letters!")
        elif guess.lower() not in self.dictionary:
            self.statusBar.config(text = "Must be a real word!")
        else:
            right_word = self.word.upper()
            for x,y in enumerate(guess):
                if y.upper() in right_word:
                    if x == right_word.find(y.upper()):
                        self.setGrid(1, "white", "green", self.attempt, x, y.upper())
                        self.setGrid(2, "white", "green", letter=y.upper())
                        right_word = list(right_word)
                        right_word[x] = " "
                        right_word = "".join(right_word)
                        right_count += 1
                    else:
                        self.setGrid(1, "black", "yellow", self.attempt, x, y.upper())
                        if self.getGridColor(y.upper()) != "green":
                            self.setGrid(2, "black", "yellow", letter=y.upper())
                else:
                    self.setGrid(1, "white", "grey", self.attempt, x, y.upper())
                    self.setGrid(2, "white", "grey", letter=y.upper())
            self.attempt += 1
            self.statusBar.config(text = "")
            self.checkGameEnd(right_count)
        self.wordEntry.delete(0, END)


    def setGrid(self, type, fg, bg, row=0, column=0, letter=""):
        if type == 1:
            self.playBoard_matrix[row][column].config(bg=bg, fg=fg, text=letter)
        elif type == 2:
            row = (ord(letter) - 65) // 10
            col = (ord(letter) - 65) % 10
            self.letterGrid_matrix[row][col].config(bg=bg, fg=fg)

    def getGridColor(self, letter):
        row = (ord(letter) - 65) // 10
        col = (ord(letter) - 65) % 10
        return self.letterGrid_matrix[row][col]["bg"]

    def checkGameEnd(self, right_count):
        if right_count == 5:
            self.wordEntry.config(state=DISABLED)
            self.statusBar.config(text = 'You found the word! Click "RESET" to start a new game.')
            self.submitButton.config(text="RESET", command=self.resetGame)
        if self.attempt == 6:
            self.wordEntry.config(state=DISABLED)
            self.statusBar.config(text = f'The word was "{self.word}". Click "RESET" to start a new game.')
            self.submitButton.config(text="RESET", command=self.resetGame)
    

    def generateWord(self):
        word = random.choice(self.dictionary)
        #print(word) ####################################################################
        return word

    def createDict(self):
        with open("dictionary.txt") as dictionary:
            all_words = dictionary.read()
            self.dictionary = list(map(str, all_words.split()))
    
    def resetGame(self):
        self.playBoard.pack_forget()
        self.entryBox.pack_forget()
        self.letterGrid.pack_forget()
        self.updateBar.pack_forget()
        self.__init__(self.window)
