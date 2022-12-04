# Import Necessary Modules
from tkinter import *

import sqlite3

from datetime import date

import time

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib import style

from PIL import ImageTk, Image

import random

import math

from math import log10, floor

style.use("Solarize_Light2")

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]


def getDate():
    today = str(date.today())
    monthIndex = months[int(today[5:7]) - 1]
    # Date Superscript
    superscript = int(today[8:])
    if superscript == 1:
        superscript = today[8:] + "st"
    elif superscript == 2:
        superscript = today[8:] + "nd"
    else:
        superscript = today[8:] + "th"
    return superscript, monthIndex, today[0:4]


def getEntryText():
    # Connect to database
    with sqlite3.connect('Login_Details.db') as database:
        cursor = database.cursor()
    global usernameToPrint
    usernameToPrint = cursor.execute(
        "SELECT * FROM UserProgress WHERE lastSignOn = (SELECT MAX(lastSignOn) FROM UserProgress)")
    for row in usernameToPrint:
        daysSinceOn = str(round(((time.time()) - row[1]) // 86400))
        database.close()
        return ("Hi " + row[0] + " it has been " + daysSinceOn + " days since you last logged on.")


# Subprogram to add recurring widgets to every screen
def populateFrame(self, parent, controller, titleText):
    # Date and Title
    title = Label(self, text=titleText, font=("Times New Roman", 50, "underline"), pady=10, bg="#FFF2CC")
    title.grid(row=0, column=1, columnspan=2)
    date = Label(self, text=getDate(), pady=10, bg="#FFF2CC", font=("Times New Roman", 30))
    date.grid(row=0, column=0)

    # Grid width initializers
    gridInitializer = Label(self, width="40", height="1", bg="#FFF2CC")
    gridInitializer.grid(row=99, column=0)
    gridInitializer1 = Label(self, width="40", height="1", bg="#FFF2CC")
    gridInitializer1.grid(row=99, column=1)
    gridInitializer2 = Label(self, width="40", height="1", bg="#FFF2CC")
    gridInitializer2.grid(row=99, column=2)
    gridInitializer3 = Label(self, width="40", height="1", bg="#FFF2CC")
    gridInitializer3.grid(row=99, column=3)

    # Buttons to access different pages
    menuButton = Button(self, text="Menu", height=1, width=13,
                        command=lambda: controller.changeFrame(menuScreen), font=("Times New Roman", 50))
    menuButton.grid(row=1, column=0, pady=3)
    learnButton = Button(self, text="Learn", height=1, width=13,
                         command=lambda: controller.changeFrame(learnScreen), font=("Times New Roman", 50))
    learnButton.grid(row=1, column=1, pady=3)
    quizButton = Button(self, text="Quiz", height=1, width=13,
                        command=lambda: controller.changeFrame(quizScreen), font=("Times New Roman", 50))
    quizButton.grid(row=1, column=2, pady=3)
    calculatorButton = Button(self, text="Calculator", height=1, width=13,
                              command=lambda: controller.changeFrame(calculatorScreen), font=("Times New Roman", 50))
    calculatorButton.grid(row=1, column=3, pady=3)


# =======================================================Main Class========================================================================
class main(Tk):

    def changeFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def __init__(self, master):
        self.master = master

        mainFrame = Frame(self.master)
        mainFrame.grid(row=2, column=0)

        mainFrame.grid_rowconfigure(0, weight=1)
        mainFrame.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (menuScreen, learnScreen, quizScreen, calculatorScreen):
            frame = F(mainFrame, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.changeFrame(menuScreen)

#======================================================Main Menu Screen===========================================================
class menuScreen(Frame):

    # Show Subtopics
    def showSubtopic(self, number):
        subtopicsList = ["Algebra", "Graphs", "Integration", "Differentiation", "Trigonometry",
                         "Modelling", "Constant Acceleration", "Forces and Motion", "Variable Acceleration", "SUVAT",
                         "Data", "Probability", "Statistical Distribution", "Hypothesis Testing", "Location and Spread"]
        subtopic1.config(text=subtopicsList[number])
        subtopic2.config(text=subtopicsList[number + 1])
        subtopic3.config(text=subtopicsList[number + 2])
        subtopic4.config(text=subtopicsList[number + 3])
        subtopic5.config(text=subtopicsList[number + 4])

    def destroyProgress(self, graph):
        graph.grid_forget()

    def barGraph(self):
        # Bar Chart to show progress in different areas
        barProgressFrame = Frame(self, bg="#FFF2CC")

        figure1 = plt.Figure(figsize=(5, 4), dpi=100, facecolor="#FFF2CC")
        addBar = figure1.add_subplot(111)
        labels = ["All", "Pure", "Mechanics", "Stats"]
        # Retrieve Scores from database
        with sqlite3.connect('Login_Details.db') as database:
            cursor = database.cursor()
        allScores = cursor.execute(
            "SELECT * FROM UserProgress WHERE lastSignOn = (SELECT MAX(lastSignOn) FROM UserProgress)")
        for row in allScores:
            scores = [(100 * row[3] // row[2]), (100 * row[5] // row[4]), (100 * row[7] // row[6]),
                      (100 * row[9] // row[8])]
        addBar.bar(labels, scores, 0.5)
        addBar.set_title("Percentage in each area")
        addBar.set_xlabel("Area")
        addBar.set_ylabel("Percentage %")
        addBar.set_ylim(0, 100)
        addBar.set_facecolor("#ADD8E6")
        canvasBar = FigureCanvasTkAgg(figure1, master=barProgressFrame)
        canvasBar.draw()
        canvasBar.get_tk_widget().grid(row=3, column=2, columnspan=2, rowspan=4)

        # Change graph buttons
        Button(barProgressFrame, text="<", bg="white", height="2", font=("Times New Roman", 30, "bold"),
               command=lambda: [self.destroyProgress(barProgressFrame), self.pieChart()]).grid(row=7, column=2, pady=5)
        Button(barProgressFrame, text=">", bg="white", height="2", font=("Times New Roman", 30, "bold"),
               command=lambda: [self.destroyProgress(barProgressFrame), self.lineGraph()]).grid(row=7, column=3, pady=5)
        barProgressFrame.grid(row=3, column=2, columnspan=2, rowspan=5)

    def pieChart(self):
        # Pie Chart view
        pieProgressFrame = Frame(self, bg="#FFF2CC")

        figure2 = plt.Figure(figsize=(5, 4), dpi=100, facecolor="#FFF2CC")
        addPie = figure2.add_subplot(111)
        labels = ["All", "Pure", "Mechanics", "Stats"]
        colours = ["lightgreen", "gold", "lightskyblue", "red"]
        explode = [0.2, 0, 0, 0]
        # Retrieve Scores from database
        with sqlite3.connect('Login_Details.db') as database:
            cursor = database.cursor()
        allScores = cursor.execute(
            "SELECT * FROM UserProgress WHERE lastSignOn = (SELECT MAX(lastSignOn) FROM UserProgress)")
        for row in allScores:
            scores = [(100 * row[3] // row[2]), (100 * row[5] // row[4]), (100 * row[7] // row[6]),
                      (100 * row[9] // row[8])]
        addPie.pie(scores, explode=explode, labels=labels, colors=colours, autopct="%1.1f%%", startangle=100)
        addPie.set_title("Percentage in each area")
        canvasPie = FigureCanvasTkAgg(figure2, master=pieProgressFrame)
        canvasPie.draw()
        canvasPie.get_tk_widget().grid(row=3, column=2, columnspan=2, rowspan=4)
        # Change graph buttons
        Button(pieProgressFrame, text="<", bg="white", height="2", font=("Times New Roman", 30, "bold"),
               command=lambda: [self.destroyProgress(pieProgressFrame), self.lineGraph()]).grid(row=7, column=2, pady=5)
        Button(pieProgressFrame, text=">", bg="white", height="2", font=("Times New Roman", 30, "bold"),
               command=lambda: [self.destroyProgress(pieProgressFrame), self.barGraph()]).grid(row=7, column=3, pady=5)
        pieProgressFrame.grid(row=3, column=2, columnspan=2, rowspan=5)

    def lineGraph(self):
        # Line Chart View
        lineProgressFrame = Frame(self, bg="#FFF2CC") # Frame for graph
        lineProgressFrame.grid(row=3, column=2, columnspan=2, rowspan=5) # Grid location of graph

        figure3 = plt.Figure(figsize=(5, 4), dpi=100, facecolor="#FFF2CC") # Initialise figure size and colour
        addLine = figure3.add_subplot(111)
        labels = ["All", "Pure", "Mechanics", "Stats"] # Labels for each point
        # Retrieve Scores from database
        with sqlite3.connect('Login_Details.db') as database:
            cursor = database.cursor()
        allScores = cursor.execute("SELECT * FROM UserProgress WHERE lastSignOn = (SELECT MAX(lastSignOn) FROM UserProgress)")
        for row in allScores:
            scores = [(100 * row[3] // row[2]), (100 * row[5] // row[4]), (100 * row[7] // row[6]),
                      (100 * row[9] // row[8])] # Work out percentages
        addLine.plot(labels, scores, color="blue", linestyle="dashed", marker="o", ) # Line style
        addLine.set_title("Percentage in each area") #Graph title
        addLine.set_ylim(0, 100) #Limits y-axis 0 to 100%
        #Embed into tkinter
        canvasLine = FigureCanvasTkAgg(figure3, master=lineProgressFrame)
        canvasLine.draw()
        canvasLine.get_tk_widget().grid(row=3, column=2, columnspan=2, rowspan=4)
        # Change graph buttons
        Button(lineProgressFrame, text="<", bg="white", height="2", font=("Times New Roman", 30, "bold"),
               command=lambda: [self.destroyProgress(lineProgressFrame), self.barGraph()]).grid(row=7, column=2, pady=5)
        Button(lineProgressFrame, text=">", bg="white", height="2", font=("Times New Roman", 30, "bold"),
               command=lambda: [self.destroyProgress(lineProgressFrame), self.pieChart()]).grid(row=7, column=3, pady=5)
        lineProgressFrame.grid(row=3, column=2, columnspan=2, rowspan=5)

    def learnOrQuiz(self, controller):
        return

    # Main Menu Screen initialisation
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Frame.configure(self, bg="#FFF2CC")
        populateFrame(self, parent, controller, "Main Menu")

        # Welcome message and progress title
        welcomeText = Label(self, text=getEntryText(), padx=10, bg="#FFF2CC", font=("Times New Roman", 25))
        welcomeText.grid(row=2, column=0, columnspan=2, pady=20, sticky=W)
        progressTitle = Label(self, text="Progress", bg="#FFF2CC", font=("Times New Roman", 25))
        progressTitle.grid(row=2, column=2, columnspan=2)

        # Grid width initializers
        Label(self, width="40", bg="#FFF2CC").grid(row=100, column=0)
        Label(self, width="40", bg="#FFF2CC").grid(row=100, column=1)
        Label(self, width="40", bg="#FFF2CC").grid(row=100, column=2)
        Label(self, width="40", bg="#FFF2CC").grid(row=100, column=3)

        # Buttons for 3 maths topics
        pureButton = Button(self, text="Pure", bg="white", height=2, command=lambda: self.showSubtopic(0),
                            font=("Times New Roman", 30))
        pureButton.grid(row=3, column=0, pady=15)
        Label(self, text="", width="40", bg="#FFF2CC").grid(row=4, column=0)
        mechButton = Button(self, text="Mechanics", bg="white", height=2, command=lambda: self.showSubtopic(5),
                            font=("Times New Roman", 30))
        mechButton.grid(row=5, column=0, pady=15)
        Label(self, text="", width="40", bg="#FFF2CC").grid(row=6, column=0)
        statsButton = Button(self, text="Stats", bg="white", height=2, command=lambda: self.showSubtopic(10),
                             font=("Times New Roman", 30))
        statsButton.grid(row=7, column=0, pady=15)
        Label(self, text="", width="40", bg="#FFF2CC").grid(row=8, column=0, pady=5)

        # Subtopic Buttons
        global subtopic1
        subtopic1 = Button(self, text="Algebra", bg="white", height="2", font=("Times New Roman", 30))
        subtopic1.grid(row=3, column=1, pady=5)
        global subtopic2
        subtopic2 = Button(self, text="Graphs", bg="white", height="2", font=("Times New Roman", 30))
        subtopic2.grid(row=4, column=1, pady=5)
        global subtopic3
        subtopic3 = Button(self, text="Integration", bg="white", height="2", font=("Times New Roman", 30))
        subtopic3.grid(row=5, column=1, pady=5)
        global subtopic4
        subtopic4 = Button(self, text="Differentiation", bg="white", height="2", font=("Times New Roman", 30))
        subtopic4.grid(row=6, column=1, pady=5)
        global subtopic5
        subtopic5 = Button(self, text="Trigonometry", bg="white", height="2", font=("Times New Roman", 30))
        subtopic5.grid(row=7, column=1, pady=5)

        # Initial Graph Display
        self.barGraph()


# ================================================================Learn Screen=================================================================
class learnScreen(Frame):
    # Array for title and image display
    global learnContent
    learnContent = [["Algebra", "algebra.png"], ["Graphs", "graphs.jpg"], ["Integration", "integration.jpg"],
                    ["Differentiation", "differentiation.jpg"], ["Trigonometry", "trigonometry.jpg"],
                    ["Modelling", "modelling.jpg"],
                    ["Constant Acceleration", "constantAcceleration.jpg"], ["Forces and Motion", "forcesMotion.jpg"],
                    ["Variable Acceleration", "variableAcceleration.jpg"], ["SUVAT", "suvat.jpg"], ["Data", "data.jpg"],
                    ["Probability", "probability.jpg"], ["Statistical Distribution", "statisticalDistribution.jpg"],
                    ["Hypothesis Testing", "hypothesisTesting.jpg"], ["Location and Spread", "locationSpread.jpg"]]


    # Subprogram to choose subtopic for learning
    def learnSelection(self):
        # All subtopics shown in main menu
        subtopicsList = ["Algebra", "Graphs", "Integration", "Differentiation", "Trigonometry",
                         "Modelling", "Constant Acceleration", "Forces and Motion", "Variable Acceleration", "SUVAT",
                         "Data", "Probability", "Statistical Distribution", "Hypothesis Testing", "Location and Spread"]
        # Frame to contain all learn options
        learnTopicFrame = Frame(self, bg="#FFF2CC")
        learnTopicFrame.grid(row=2, column=0, columnspan=4, rowspan=6)

        # Title to indicate to choose subtopic
        Label(learnTopicFrame, bg="#FFF2CC", text="CHOOSE A TOPIC", font=("Times New Roman", 50)).grid(row=2,
                                                                                                      column=1)

        # All buttons for each topic to learn
        learnButton1 = Button(learnTopicFrame, text=subtopicsList[0], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showNotes(0), learnTopicFrame.grid_forget()])
        learnButton1.grid(row=3, column=0, pady=15)

        learnButton2 = Button(learnTopicFrame, text=subtopicsList[1], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showNotes(1), learnTopicFrame.grid_forget()])
        learnButton2.grid(row=4, column=0, pady=15)

        learnButton3 = Button(learnTopicFrame, text=subtopicsList[2], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showNotes(2), learnTopicFrame.grid_forget()])
        learnButton3.grid(row=5, column=0, pady=15)

        learnButton4 = Button(learnTopicFrame, text=subtopicsList[3], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showNotes(3), learnTopicFrame.grid_forget()])
        learnButton4.grid(row=6, column=0, pady=10)

        learnButton5 = Button(learnTopicFrame, text=subtopicsList[4], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showNotes(4), learnTopicFrame.grid_forget()])
        learnButton5.grid(row=7, column=0, pady=15)

        learnButton6 = Button(learnTopicFrame, text=subtopicsList[5], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showNotes(5), learnTopicFrame.grid_forget()])
        learnButton6.grid(row=3, column=1, pady=15)

        learnButton7 = Button(learnTopicFrame, text=subtopicsList[6], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showNotes(6), learnTopicFrame.grid_forget()])
        learnButton7.grid(row=4, column=1, pady=15)

        learnButton8 = Button(learnTopicFrame, text=subtopicsList[7], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showNotes(7), learnTopicFrame.grid_forget()])
        learnButton8.grid(row=5, column=1, pady=15)

        learnButton9 = Button(learnTopicFrame, text=subtopicsList[8], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showNotes(8), learnTopicFrame.grid_forget()])
        learnButton9.grid(row=6, column=1, pady=15)

        learnButton10 = Button(learnTopicFrame, text=subtopicsList[9], font=("Times New Roman", 35), height=2,
                              command=lambda: [self.showNotes(9), learnTopicFrame.grid_forget()])
        learnButton10.grid(row=7, column=1, pady=15)

        learnButton11 = Button(learnTopicFrame, text=subtopicsList[10], font=("Times New Roman", 35), height=2,
                              command=lambda: [self.showNotes(10), learnTopicFrame.grid_forget()])
        learnButton11.grid(row=3, column=2, pady=15)

        learnButton12 = Button(learnTopicFrame, text=subtopicsList[11], font=("Times New Roman", 35), height=2,
                              command=lambda: [self.showNotes(11), learnTopicFrame.grid_forget()])
        learnButton12.grid(row=4, column=2, pady=15)

        learnButton13 = Button(learnTopicFrame, text=subtopicsList[12], font=("Times New Roman", 35), height=2,
                              command=lambda: [self.showNotes(12), learnTopicFrame.grid_forget()])
        learnButton13.grid(row=5, column=2, pady=15)

        learnButton14 = Button(learnTopicFrame, text=subtopicsList[13], font=("Times New Roman", 35), height=2,
                              command=lambda: [self.showNotes(13), learnTopicFrame.grid_forget()])
        learnButton14.grid(row=6, column=2, pady=15)

        learnButton15 = Button(learnTopicFrame, text=subtopicsList[14], font=("Times New Roman", 35), height=2,
                              command=lambda: [self.showNotes(14), learnTopicFrame.grid_forget()])
        learnButton15.grid(row=7, column=2, pady=15)

        # Grid width initializers
        Label(learnTopicFrame, width="53", height="1", bg="#FFF2CC").grid(row=99, column=0)
        Label(learnTopicFrame, width="53", height="1", bg="#FFF2CC").grid(row=99, column=1)
        Label(learnTopicFrame, width="53", height="1", bg="#FFF2CC").grid(row=99, column=2)

    def showNotes(self, subtopicIndex):
        #Array of image file names for notes on each subtopic
        learnImages = ["algebra.png", "graphs.png", "integration.png", "differentiation.png", "trigonometry.png",
                         "modelling.png", "constantAcceleration.png", "forcesMotion.png", "variableAcceleration.png", "SUVAT.png",
                         "data.png", "probability.png", "statisticalDistribution.png", "hypothesisTesting.png", "locationSpread.png"]

        # Question Frame
        learnNotesFrame = Frame(self, bg="#FFF2CC")
        learnNotesFrame.grid(row=2, column=0, rowspan=4, columnspan=4, sticky="nsew")

        #Image of learn content
        learnImagePath = learnImages[subtopicIndex]
        learnImg = (Image.open(learnImagePath))
        resizedLearnImage = ImageTk.PhotoImage(learnImg.resize((1400, 600)))
        learnImageLabel = Label(learnNotesFrame, image=resizedLearnImage)
        learnImageLabel.image = resizedLearnImage
        learnImageLabel.grid(row=2, column=0, columnspan=4)

        # Buttons to change quiz topic
        if subtopicIndex == 14:
            nextIndex = 0
        else:
            nextIndex = subtopicIndex + 1

        if subtopicIndex == 0:
            prevIndex = 14
        else:
            prevIndex = subtopicIndex - 1
        prevLearnButton = Button(learnNotesFrame, bg="#FFF2CC", text="<", font=("Times New Roman", 30),
                                command=lambda: [self.showNotes(prevIndex)])
        prevLearnButton.grid(row=6, column=0, pady=15)

        nextLearnButton = Button(learnNotesFrame, bg="#FFF2CC", text=">", font=("Times New Roman", 30),
                                command=lambda: [self.showNotes(nextIndex)])
        nextLearnButton.grid(row=6, column=3, pady=15)

        backLearnButton = Button(learnNotesFrame, bg="#FFF2CC", text="Go Back to Topic Selection",
                                font=("Times New Roman", 30),
                                command=lambda: [learnNotesFrame.destroy(), self.learnSelection()])
        backLearnButton.grid(row=6, column=1, columnspan=2, pady=15)

        # Grid width initializers
        learnGridInitializer = Label(learnNotesFrame, width="40", height="1", bg="#FFF2CC")
        learnGridInitializer.grid(row=99, column=0)
        learnGridInitializer1 = Label(learnNotesFrame, width="40", height="1", bg="#FFF2CC")
        learnGridInitializer1.grid(row=99, column=1)
        learnGridInitializer2 = Label(learnNotesFrame, width="40", height="1", bg="#FFF2CC")
        learnGridInitializer2.grid(row=99, column=2)
        learnGridInitializer3 = Label(learnNotesFrame, width="40", height="1", bg="#FFF2CC")
        learnGridInitializer3.grid(row=99, column=3)

        # Show Question Frame
        learnNotesFrame.tkraise()

    # Learn Screen initialisation
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Frame.configure(self, bg="#FFF2CC")
        populateFrame(self, parent, controller, "Learn")

        self.learnSelection()


# =================================================================Quiz Screen==================================================================

class quizScreen(Frame):

    # Subprogram to choose subtopic for quiz
    def quizSelection(self):

        # All subtopics shown in main menu
        subtopicsList = ["Algebra", "Graphs", "Integration", "Differentiation", "Trigonometry",
                         "Modelling", "Constant Acceleration", "Forces and Motion", "Variable Acceleration", "SUVAT",
                         "Data", "Probability", "Statistical Distribution", "Hypothesis Testing", "Location and Spread"]
        # Frame to contain all quiz options
        quizTopicFrame = Frame(self, bg="#FFF2CC")
        quizTopicFrame.grid(row=2, column=0, columnspan=4, rowspan=6)

        # Title to indicate to choose subtopic
        Label(quizTopicFrame, bg="#FFF2CC", text="CHOOSE A TOPIC", font=("Times New Roman", 50)).grid(row=2, column=1)

        # All buttons for each quiz
        quizButton1 = Button(quizTopicFrame, text=subtopicsList[0], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showQuiz(0), quizTopicFrame.grid_forget()])
        quizButton1.grid(row=3, column=0, pady=15)

        quizButton2 = Button(quizTopicFrame, text=subtopicsList[1], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showQuiz(1), quizTopicFrame.grid_forget()])
        quizButton2.grid(row=4, column=0, pady=15)

        quizButton3 = Button(quizTopicFrame, text=subtopicsList[2], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showQuiz(2), quizTopicFrame.grid_forget()])
        quizButton3.grid(row=5, column=0, pady=15)

        quizButton4 = Button(quizTopicFrame, text=subtopicsList[3], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showQuiz(3), quizTopicFrame.grid_forget()])
        quizButton4.grid(row=6, column=0, pady=10)

        quizButton5 = Button(quizTopicFrame, text=subtopicsList[4], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showQuiz(4), quizTopicFrame.grid_forget()])
        quizButton5.grid(row=7, column=0, pady=15)

        quizButton6 = Button(quizTopicFrame, text=subtopicsList[5], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showQuiz(5), quizTopicFrame.grid_forget()])
        quizButton6.grid(row=3, column=1, pady=15)

        quizButton7 = Button(quizTopicFrame, text=subtopicsList[6], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showQuiz(6), quizTopicFrame.grid_forget()])
        quizButton7.grid(row=4, column=1, pady=15)

        quizButton8 = Button(quizTopicFrame, text=subtopicsList[7], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showQuiz(7), quizTopicFrame.grid_forget()])
        quizButton8.grid(row=5, column=1, pady=15)

        quizButton9 = Button(quizTopicFrame, text=subtopicsList[8], font=("Times New Roman", 35), height=2,
                             command=lambda: [self.showQuiz(8), quizTopicFrame.grid_forget()])
        quizButton9.grid(row=6, column=1, pady=15)

        quizButton10 = Button(quizTopicFrame, text=subtopicsList[9], font=("Times New Roman", 35), height=2,
                              command=lambda: [self.showQuiz(9), quizTopicFrame.grid_forget()])
        quizButton10.grid(row=7, column=1, pady=15)

        quizButton11 = Button(quizTopicFrame, text=subtopicsList[10], font=("Times New Roman", 35), height=2,
                              command=lambda: [self.showQuiz(10), quizTopicFrame.grid_forget()])
        quizButton11.grid(row=3, column=2, pady=15)

        quizButton12 = Button(quizTopicFrame, text=subtopicsList[11], font=("Times New Roman", 35), height=2,
                              command=lambda: [self.showQuiz(11), quizTopicFrame.grid_forget()])
        quizButton12.grid(row=4, column=2, pady=15)

        quizButton13 = Button(quizTopicFrame, text=subtopicsList[12], font=("Times New Roman", 35), height=2,
                              command=lambda: [self.showQuiz(12), quizTopicFrame.grid_forget()])
        quizButton13.grid(row=5, column=2, pady=15)

        quizButton14 = Button(quizTopicFrame, text=subtopicsList[13], font=("Times New Roman", 35), height=2,
                              command=lambda: [self.showQuiz(13), quizTopicFrame.grid_forget()])
        quizButton14.grid(row=6, column=2, pady=15)

        quizButton15 = Button(quizTopicFrame, text=subtopicsList[14], font=("Times New Roman", 35), height=2,
                              command=lambda: [self.showQuiz(14), quizTopicFrame.grid_forget()])
        quizButton15.grid(row=7, column=2, pady=15)

        # Grid width initializers
        Label(quizTopicFrame, width="53", height="1", bg="#FFF2CC").grid(row=99, column=0)
        Label(quizTopicFrame, width="53", height="1", bg="#FFF2CC").grid(row=99, column=1)
        Label(quizTopicFrame, width="53", height="1", bg="#FFF2CC").grid(row=99, column=2)

    # Show Quiz Subprogram
    def showQuiz(self, subtopicIndex):

        # 2D array of each subtopic and the corresponding image file
        quizContent = ["Algebra", "Graphs", "Integration", "Differentiation", "Trigonometry",
                       "Modelling", "Constant Acceleration", "Forces and Motion", "Variable Acceleration", "SUVAT",
                       "Data", "Probability", "Statistical Distribution", "Hypothesis Testing", "Location and Spread"]

        global quizSubtopicName
        quizSubtopicName = quizContent[subtopicIndex]

        # Question Frame
        questionFrame = Frame(self, bg="#FFF2CC")
        questionFrame.grid(row=2, column=0, rowspan=4, columnspan=4, sticky="nsew")

        # Subtopic Title
        quizTitle = Label(questionFrame, bg="#FFF2CC", text=quizSubtopicName, font=("Times New Roman", 60))
        quizTitle.grid(row=2, column=0, columnspan=4, pady=10)

        # Retrieve Questions from generator
        questionText1, questionText2, solution = self.generateQuestion(quizSubtopicName)

        # Question Display
        questionLabel1 = Label(questionFrame, bg="#FFF2CC", text=questionText1, font=("Times New Roman", 75))
        questionLabel1.grid(row=3, column=0, columnspan=4, pady=15)
        questionLabel2 = Label(questionFrame, bg="#FFF2CC", text=questionText2, font=("Times New Roman", 75))
        questionLabel2.grid(row=4, column=0, columnspan=4, pady=15)

        # Answer Input Boxes
        answer = StringVar()
        answerEntry = Entry(questionFrame, textvariable=answer, bd=5, font=('', 30), width=30)
        answerEntry.grid(row=5, column=0, columnspan=2, pady=15)

        # Answer Submit Button
        global answerSubmit
        answerSubmit = Button(questionFrame, text="Check", bd=3, font=('', 30), bg="#FFF2CC",
                              command=lambda: self.checkAnswer(float(answer.get()), solution, subtopicIndex))
        answerSubmit.grid(row=5, column=2, padx=5, pady=15)

        # Correct Label
        global correctLabel
        correctLabel = Label(questionFrame, bg="#FFF2CC", font=("Times New Roman", 70))

        # Buttons to change quiz topic
        if subtopicIndex == 14:
            nextIndex = 0
        else:
            nextIndex = subtopicIndex + 1

        if subtopicIndex == 0:
            prevIndex = 14
        else:
            prevIndex = subtopicIndex - 1
        prevQuizButton = Button(questionFrame, bg="#FFF2CC", text="<", font=("Times New Roman", 30),
                                command = lambda: [self.showQuiz(nextIndex)])
        prevQuizButton.grid(row=6, column=0, pady=15)

        nextQuizButton = Button(questionFrame, bg="#FFF2CC", text=">", font=("Times New Roman", 30),
                                command = lambda: [self.showQuiz(prevIndex)])
        nextQuizButton.grid(row=6, column=3, pady=15)

        backQuizButton = Button(questionFrame, bg="#FFF2CC", text="Go Back to Topic Selection",
                                font=("Times New Roman", 30),
                                command=lambda: [questionFrame.destroy(), self.quizSelection()])
        backQuizButton.grid(row=6, column=1, columnspan=2, pady=15)

        # Grid width initializers
        quizGridInitializer = Label(questionFrame, width="40", height="1", bg="#FFF2CC")
        quizGridInitializer.grid(row=99, column=0)
        quizGridInitializer1 = Label(questionFrame, width="40", height="1", bg="#FFF2CC")
        quizGridInitializer1.grid(row=99, column=1)
        quizGridInitializer2 = Label(questionFrame, width="40", height="1", bg="#FFF2CC")
        quizGridInitializer2.grid(row=99, column=2)
        quizGridInitializer3 = Label(questionFrame, width="40", height="1", bg="#FFF2CC")
        quizGridInitializer3.grid(row=99, column=3)

        # Show Question Frame
        questionFrame.tkraise()

    # Subprogram to generate questions
    def generateQuestion(self, subtopic):

        if subtopic == "Algebra": # Algebra question generation (binomial)
            exponent = random.randint(5, 16)
            powerToFind = random.randint(2, (exponent))
            binomialXCoefficient = random.randint(1, 11)
            questionLine1 = "In the expansion of (1 + " + str(binomialXCoefficient) + "x)^" + str(exponent) + ","
            questionLine2 = "what is the term in x to the power of " + str(powerToFind)
            answer = (math.factorial(exponent)) * (binomialXCoefficient ** powerToFind) / (
                        (math.factorial(exponent - powerToFind)) * (math.factorial(powerToFind)))
            print(int(answer))


        elif subtopic == "Graphs": #Graphs question on roots of a quadratic
            root1 = random.randint(0, 12)
            root2 = random.randint(0, 12)
            questionLine1 = "For the polynomial x^2 - " + str(root1 + root2) + "x + " + str(root1 * root2) + ":"
            questionLine2 = "What is the larger of the two roots?"
            if root1 > root2:
                answer = root1
            else:
                answer = root2
            print(int(answer))

        elif subtopic == "Integration":
            x1Integral = random.randint(2, 5)
            x2Integral = random.randint((x1Integral + 3), (x1Integral + 5))
            integralPoly1 = random.randint(1, 10)
            integralPoly2 = random.randint(1, 10)
            questionLine1 = "Find the area between the x-axis, x = " + str(x1Integral) + ", x = " + str(x2Integral)
            questionLine2 = "and y = x^2 + " + str(integralPoly1) + "x + " + str(
                integralPoly2) + " to the nearest integer."
            answer = (((x2Integral ** 3) - (x1Integral ** 3)) / 3) + (
                        integralPoly1 * ((x2Integral ** 2) - (x1Integral ** 2)) / 2) + (
                                 integralPoly2 * (x2Integral - x1Integral))
            answer = round(answer)
            print(int(answer))


        elif subtopic == "Differentiation":
            xDifferen = random.randint(-10, 10)
            diffPoly1 = random.randint(2, 10)
            diffPoly2 = random.randint(1, 10)
            questionLine1 = "What is the gradient of: x^2 + " + str(diffPoly1) + "x + " + str(diffPoly2) + ","
            questionLine2 = "at the point x = " + str(xDifferen) + " ?"
            answer = (2 * xDifferen) + diffPoly1

        elif subtopic == "Trigonometry":
            trigValue = round(random.random(), 2)
            questionLine1 = "Find the solution between 0 ≤ θ ≤ π/2 for:"
            questionLine2 = "cos(θ) = " + str(trigValue) + " in radians to 2dp"
            answer = round(math.acos(trigValue), 2)
            print(answer)

        elif subtopic == "Modelling":
            x1Model = random.randint(2, 6)
            x2Model = random.randint(1, 10)
            questionLine1 = "Height at 't' seconds = " + str(x1Model) + "t - " + str(x1Model * x2Model ** 2) + "t^3."
            questionLine2 = "After how many seconds does the ball fall?"
            answer = x2Model

        elif subtopic == "Constant Acceleration":
            speed1 = random.randint(10, 30)
            timeAccel = random.randint(5, 16)
            accel = random.randint(5, 11)
            speed2 = speed1 + (timeAccel * accel)
            questionLine1 = "Over " + str(timeAccel) + "s a car goes from " + str(speed1) + " m/s to " + str(
                speed2) + "m/s."
            questionLine2 = "What is its acceleration in m/s^2?"
            answer = accel

        elif subtopic == "Forces and Motion":
            force1 = random.randint(2, 20)
            force2 = random.randint(2, 20)
            questionLine1 = str(force1) + "N <--◯--> " + str(force2) + "N"
            questionLine2 = "What is the magnitude of the resultant force?"
            answer = abs(force2 - force1)
            print(answer)

        elif subtopic == "Variable Acceleration": # Variable acceleration question based on quadratics
            xCoVariable = random.randrange(2, 17, 2)
            constantVariable = random.randint(2, 20)
            questionLine1 = "Displacement from the origin= x^2 + " + str(xCoVariable) + "x + " + str(
                constantVariable) + ":"
            questionLine2 = "What is the least displacement from the origin?"
            answer = abs(constantVariable - (xCoVariable / 2) ** 2)

        elif subtopic == "SUVAT": # SUVAT question based on equation, rearrange and solve
            initialSpeed = random.randint(2, 10)
            accelSUVAT = random.randint(2, 6)
            finalSpeed = random.randrange(initialSpeed, 31, accelSUVAT)
            questionLine1 = "If v = " + str(finalSpeed) + "m/s, u = " + str(initialSpeed) + "m/s and a = " + str(
                accelSUVAT) + "m/s^2,"
            questionLine2 = "what is displacement (s) to the nearest metres?"
            answer = round(finalSpeed ** 2 - initialSpeed ** 2) / (2 * accelSUVAT)
            print(answer)

        elif subtopic == "Data":
            rainfall = random.sample(range(5, 15), 4)
            questionLine1 = "Rainfall per week in mm was: " + str(rainfall)
            questionLine2 = "What was the average rainfall in mm per week?"
            answer = (rainfall[0] + rainfall[1] + rainfall[2] + rainfall[3]) / 4

        elif subtopic == "Probability":
            noFlips = random.randint(5, 10)
            noHeads = random.randint(0, noFlips)
            questionLine1 = "If you flip a coin " + str(noFlips) + " times, what is"
            questionLine2 = "the probability of landing " + str(noHeads) + " heads to 2sf?"
            answer = (math.factorial(noFlips)) * (0.5 ** noFlips) / (
                        math.factorial(noFlips - noHeads) * math.factorial(noHeads))
            answer = round(answer, 1 - int(floor(log10(abs(answer)))))
            print(answer)

        elif subtopic == "Statistical Distribution":
            probList = [0.9999, 0.9936, 0.9527, 0.8338, 0.6230]
            bullseyeProb = round((random.random() / 2), 1)
            questionLine1 = "p(bullseye) = " + str(bullseyeProb) + ", across 10 attempts, what is"
            questionLine2 = "the probability of a bullseye up to 5 times?"
            answer = probList[int((10 * bullseyeProb) - 1)]

        elif subtopic == "Hypothesis Testing":
            probHypoth = round(20 * random.random()) / 20
            noTries = random.randint(5, 10)
            noSuccess = random.randint(0, noTries)
            questionLine1 = "p(success) = " + str(probHypoth) + " ,what is the probability"
            questionLine2 = "that at least " + str(noSuccess) + " out of " + str(noTries) + " are successful to 2dp?"
            answer = 0
            for prob in range(noSuccess, noTries + 1):
                nextProb = (math.factorial(noTries)) * (probHypoth ** prob) * ((1 - probHypoth) ** (noTries - prob)) / (
                            math.factorial(noTries - prob) * math.factorial(prob))
                answer = answer + nextProb
                prob = prob + 1
            answer = round(answer, 2)
            print(answer)


        elif subtopic == "Location and Spread":
            deviationList = random.sample(range(5, 15), 6)
            questionLine1 = "What is the standard deviation (σ) of the list:"
            questionLine2 = str(deviationList) + " to 2dp"
            averageList = (deviationList[0] + deviationList[1] + deviationList[2] + deviationList[3] + deviationList[
                4] + deviationList[5]) / 6
            sumSigma = 0
            for deviationIndex in range(0, 6):
                sumSigma += (deviationList[deviationIndex] - averageList) ** 2
            answer = round((sumSigma / 6) ** 0.5, 2)
            print(answer)

        return questionLine1, questionLine2, float(answer)

    # Subprogram to check answer
    def checkAnswer(self, userAnswer, correctAnswer, subtopicIndex):

        #Connect to database
        with sqlite3.connect('Login_Details.db') as database:
            cursor = database.cursor()
        # Display if right or wrong and upload to database
        if userAnswer == correctAnswer:
            correctLabel.config(text="✓", fg="green")

            #Update SQL Database
            if subtopicIndex < 5:
                cursor.execute(
                    "UPDATE UserProgress SET pureQDone = pureQDone + 1, pureQCorrect = pureQCorrect + 1 WHERE lastSignOn = (SELECT MAX(lastSignOn) FROM UserProgress)")
            elif subtopicIndex < 10:
                cursor.execute(
                    "UPDATE UserProgress SET mechQDone = mechQDone + 1, mechQCorrect = mechQCorrect + 1 WHERE lastSignOn = (SELECT MAX(lastSignOn) FROM UserProgress)")
            else:
                cursor.execute(
                    "UPDATE UserProgress SET statsQDone = statsQDone + 1, statsQCorrect = statsQCorrect + 1 WHERE lastSignOn = (SELECT MAX(lastSignOn) FROM UserProgress)")

            cursor.execute(
                "UPDATE UserProgress SET totalQCorrect = totalQCorrect + 1 WHERE lastSignOn = (SELECT MAX(lastSignOn) FROM UserProgress)")

        else:
            correctLabel.config(text="✗", fg="red")

            #Update SQL Database
            if subtopicIndex < 5:
                cursor.execute(
                    "UPDATE UserProgress SET pureQDone = pureQDone + 1 WHERE lastSignOn = (SELECT MAX(lastSignOn) FROM UserProgress)")
            elif subtopicIndex < 10:
                cursor.execute(
                    "UPDATE UserProgress SET mechQDone = mechQDone + 1 WHERE lastSignOn = (SELECT MAX(lastSignOn) FROM UserProgress)")
            else:
                cursor.execute(
                    "UPDATE UserProgress SET statsQDone = statsQDone + 1 WHERE lastSignOn = (SELECT MAX(lastSignOn) FROM UserProgress)")

        cursor.execute(
            "UPDATE UserProgress SET totalQDone = totalQDone + 1 WHERE lastSignOn = (SELECT MAX(lastSignOn) FROM UserProgress)")
        database.commit()
        correctLabel.grid(row=5, column=3)

        answerSubmit.config(text="Next Question", command=lambda: self.showQuiz(subtopicIndex))

    # Quiz Screen initialisation
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Frame.configure(self, bg="#FFF2CC")
        populateFrame(self, parent, controller, "Quiz")
        self.quizSelection()


# ================================================================Calculator Screen============================================================
class calculatorScreen(Frame):

    # Show and Hide more buttons
    def showAndHide(self, view):
        if view == "show":
            moreFrame.grid(row=3, column=3, rowspan=10, pady=5)
            showHideButton.config(text = "Hide", command = lambda:self.showAndHide("hide"))
        else:
            moreFrame.grid_forget()
            showHideButton.config(text = "Show", command = lambda:self.showAndHide("show"))

    # Calculator Screen initialisation
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Frame.configure(self, bg="#FFF2CC")
        populateFrame(self, parent, controller, "Calculator")
        global expression
        expression = ""

        # PLace image in background for calculator outline
        calcImgPath = Image.open("CalculatorBG.png")
        calculatorImg = ImageTk.PhotoImage(calcImgPath.resize((1440, 720)))
        calcBGlabel = Label(self, image=calculatorImg, highlightthickness=0)
        calcBGlabel.image = calculatorImg
        calcBGlabel.place(x=0, y=155)

        # Previous results section

        #Uniform fonts for questions and answers
        questionFont = ("Times New Roman", 30)
        resultFont = ("Times New Roman", 40, "bold")

        #Previous results label
        prevResultsLabel = Label(self, text="Previous Results:", font = ("Times New Roman", 30), bg="#FFF2CC")
        prevResultsLabel.grid(row = 2, column = 0, padx = 10, pady=15, sticky = W)

        #Stacks to display previous results
        global prevResultArray
        prevResultArray = ["", "", "", "", ""]
        global prevQArray
        prevQArray = ["", "", "", "", ""]

        #Global labels to be updated in subprogram
        global prevQ1
        prevQ1 = Label(self, text = prevQArray[-5], font=questionFont, bg="#FFF2CC")
        prevQ1.grid(row = 3, column = 0, padx = 10, sticky = W)
        global prevResult1
        prevResult1 = Label(self, text = prevResultArray[-5], font=resultFont, bg = "#FFF2CC")
        prevResult1.grid(row = 4, column = 0, padx = 10, sticky = E)

        global prevQ2
        prevQ2 = Label(self, text = prevQArray[-4], font=questionFont, bg="#FFF2CC")
        prevQ2.grid(row = 5, column = 0, padx = 10, sticky = W)
        global prevResult2
        prevResult2 = Label(self, text = prevResultArray[-4], font=resultFont, bg="#FFF2CC")
        prevResult2.grid(row = 6, column = 0, padx = 10, sticky = E)

        global prevQ3
        prevQ3 = Label(self, text = prevQArray[-3], font=questionFont, bg="#FFF2CC")
        prevQ3.grid(row = 7, column = 0, padx = 10, sticky = W)
        global prevResult3
        prevResult3 = Label(self, text = prevResultArray[-3], font=resultFont, bg="#FFF2CC")
        prevResult3.grid(row = 8, column = 0, padx = 10, sticky = E)

        global prevQ4
        prevQ4 = Label(self, text=prevQArray[-2], font=questionFont, bg="#FFF2CC")
        prevQ4.grid(row=9, column=0, padx=10, sticky=W)
        global prevResult4
        prevResult4 = Label(self, text = prevResultArray[-2], font=resultFont, bg="#FFF2CC")
        prevResult4.grid(row = 10, column = 0, padx = 10, sticky = E)

        global prevQ5
        prevQ5 = Label(self, text=prevQArray[-1], font=questionFont, bg="#FFF2CC")
        prevQ5.grid(row=11, column=0, padx=10, sticky=W)
        global prevResult5
        prevResult5 = Label(self, text = prevResultArray[-1], font=resultFont, bg="#FFF2CC")
        prevResult5.grid(row = 12, column = 0, padx = 10, sticky = E)

        #Frame for calculator buttons
        calculatorFrame = Frame(self, bg = "white")
        calculatorFrame.grid(row = 3, column = 1, rowspan = 10, columnspan = 2)
        calculatorFont = (("Times New Roman", 40))

        # Calculator expression initialisation
        global calculatorExpression
        calculatorExpression = StringVar()

        # Calculator Input Box
        calculatorEntry = Entry(calculatorFrame, textvariable=calculatorExpression, bd=5, font=('', 60), width=15, state="readonly")
        calculatorEntry.grid(row = 0, column = 0, columnspan = 4, pady = 10)

        #Buttons for numbers
        button1 = Button(calculatorFrame, text = "1", font = calculatorFont, height = 2, width = 5,
                         command = lambda: self.buttonPress("1"))
        button1.grid(row = 1, column = 0, padx = 5, pady = 5)
        button2 = Button(calculatorFrame, text = "2", font = calculatorFont, height = 2, width = 5,
                         command = lambda: self.buttonPress("2"))
        button2.grid(row = 1, column = 1, padx = 5, pady = 5)
        button3 = Button(calculatorFrame, text = "3", font = calculatorFont, height = 2, width = 5,
                         command = lambda: self.buttonPress("3"))
        button3.grid(row = 1, column = 2, padx = 5, pady = 5)
        button4 = Button(calculatorFrame, text = "4", font = calculatorFont, height = 2, width = 5,
                         command = lambda: self.buttonPress("4"))
        button4.grid(row = 2, column = 0, padx = 5, pady = 5)
        button5 = Button(calculatorFrame, text = "5", font = calculatorFont, height = 2, width = 5,
                         command = lambda: self.buttonPress("5"))
        button5.grid(row=2, column=1, padx = 5, pady = 5)
        button6 = Button(calculatorFrame, text = "6", font = calculatorFont, height = 2, width = 5,
                         command = lambda: self.buttonPress("6"))
        button6.grid(row=2, column=2, padx = 5, pady = 5)
        button7 = Button(calculatorFrame, text = "7", font = calculatorFont, height = 2, width = 5,
                         command = lambda: self.buttonPress("7"))
        button7.grid(row=3, column=0, padx = 5, pady = 5)
        button8 = Button(calculatorFrame, text = "8", font = calculatorFont, height = 2, width = 5,
                         command = lambda: self.buttonPress("8"))
        button8.grid(row=3, column=1, padx = 5, pady = 5)
        button9 = Button(calculatorFrame, text = "9", font = calculatorFont, height = 2, width = 5,
                         command = lambda: self.buttonPress("9"))
        button9.grid(row=3, column=2, padx = 5, pady = 5)
        button0 = Button(calculatorFrame, text = "0", font = calculatorFont, height = 2, width = 5,
                          command = lambda: self.buttonPress("0"))
        button0.grid(row = 4, column = 1, padx = 5, pady = 5)

        #Button to clear calculator input
        clearButton = Button(calculatorFrame, text = "Clear", font = calculatorFont, height = 2, width = 5,
                             command = lambda:self.clearEntry())
        clearButton.grid(row = 4, column = 0, padx = 5, pady = 5)

        #Equals Button
        equalsButton = Button(calculatorFrame, text = "=", font = calculatorFont, height = 2, width = 5,
                              command = lambda:self.equalsPress())
        equalsButton.grid(row = 4, column = 2, padx = 5, pady = 5)

        #Button for basic arithmetic functions
        addButton = Button(calculatorFrame, text = "+", font = calculatorFont, height = 2, width = 4,
                          command = lambda: self.buttonPress(" + "))
        addButton.grid(row = 1, column = 3, padx = 5, pady = 5)
        minusButton = Button(calculatorFrame, text="—", font=calculatorFont, height=2, width=4,
                          command = lambda: self.buttonPress(" - "))
        minusButton.grid(row=2, column=3, padx=5, pady=5)
        timesButton = Button(calculatorFrame, text="x", font=calculatorFont, height=2, width=4,
                          command = lambda: self.buttonPress(" * "))
        timesButton.grid(row=3, column=3, padx=5, pady=5)
        divideButton = Button(calculatorFrame, text="÷", font=calculatorFont, height=2, width=4,
                          command = lambda: self.buttonPress(" ÷ "))
        divideButton.grid(row=4, column=3, padx=5, pady=5)

        global showHideButton
        showHideButton = Button(self, text="Hide", font = (("Times New Roman", 23)), height=2, width=5,
                            command=lambda:self.showAndHide("hide"))
        showHideButton.grid(row=2, column=3, padx=5, pady=5, columnspan=2)

        #More buttons frame for additional functionality
        global moreFrame
        moreFrame = Frame(self, bg = "#FFF2CC")
        moreFrame.grid(row = 3, column = 3, rowspan = 10, pady = 5)
        moreFont = (("Times New Roman", 23))


        #Buttons for complex calculations
        decimalButton = Button(moreFrame, text=".", font = moreFont, height=2, width=5,
                          command = lambda: self.buttonPress("."))
        decimalButton.grid(row=1, column=0, padx=5, pady=5)
        pctButton = Button(moreFrame, text="%", font = moreFont, height=2, width=5,
                          command = lambda: self.buttonPress("%"))
        pctButton.grid(row=1, column=1, padx=5, pady=5)
        powerButton = Button(moreFrame, text="^", font = moreFont, height=2, width=5,
                             command = lambda: self.buttonPress("^"))
        powerButton.grid(row=2, column=0, padx=5, pady=5)
        fractionButton = Button(moreFrame, text="a/b", font = moreFont, height=2, width=5,
                                command = lambda: self.buttonPress("/"))
        fractionButton.grid(row=2, column=1, padx=5, pady=5)
        logButton = Button(moreFrame, text="log₁₀(a)", font = moreFont, height=2, width=5,
                           command = lambda: self.buttonPress("log₁₀("))
        logButton.grid(row=3, column=0, padx=5, pady=5)
        lnButton = Button(moreFrame, text="ln(a)", font = moreFont, height=2, width=5,
                           command = lambda: self.buttonPress("ln("))
        lnButton.grid(row=3, column=1, padx=5, pady=5)
        sinButton = Button(moreFrame, text="sin", font = moreFont, height=2, width=5,
                           command = lambda: self.buttonPress("sin("))
        sinButton.grid(row=4, column=0, padx=5, pady=5)
        cosButton = Button(moreFrame, text="cos", font = moreFont, height=2, width=5,
                           command = lambda: self.buttonPress("cos("))
        cosButton.grid(row=4, column=1, padx=5, pady=5)
        tanButton = Button(moreFrame, text="tan", font = moreFont, height=2, width=5,
                           command = lambda: self.buttonPress("tan("))
        tanButton.grid(row=5, column=0, padx=5, pady=5)
        piButton = Button(moreFrame, text="π", font = moreFont, height=2, width=5,
                              command = lambda: self.buttonPress("π"))
        piButton.grid(row=5, column=1, padx=5, pady=5)
        sqrtButton = Button(moreFrame, text="√", font = moreFont, height=2, width=5,
                              command = lambda: self.buttonPress("√("))
        sqrtButton.grid(row=6, column=0, padx=5, pady=5)
        eButton = Button(moreFrame, text="e", font = moreFont, height=2, width=5,
                              command = lambda: self.buttonPress("e"))
        eButton.grid(row=6, column=1, padx=5, pady=5)
        openBracketButton = Button(moreFrame, text="(", font = moreFont, height=2, width=5,
                           command = lambda: self.buttonPress("("))
        openBracketButton.grid(row=7, column=0, padx=5, pady=5)
        closeBracketButton = Button(moreFrame, text=")", font = moreFont, height=2, width=5,
                           command = lambda: self.buttonPress(")"))
        closeBracketButton.grid(row=7, column=1, padx=5, pady=5)

    #Subprogram to update entry box upoon pressing button
    def buttonPress(self, character):
        global expression
        expression = expression + str(character)
        calculatorExpression.set(expression)

    #Subprogram to clear expression
    def clearEntry(self):
        global expression
        expression = ""
        calculatorExpression.set("")

    #Subprogram to evaluate expression
    def equalsPress(self):
        try:
            global expression
            expressionToAppend = expression
            expression = expression.replace("^", "**")
            expression = expression.replace("÷", "/")
            expression = expression.replace("log₁₀", "math.log10")
            expression = expression.replace("ln", "math.log")
            expression = expression.replace("sin", "math.sin")
            expression = expression.replace("cos", "math.cos")
            expression = expression.replace("tan", "math.tan")
            expression = expression.replace("π", "math.pi")
            expression = expression.replace("√", "math.sqrt")
            expression = expression.replace("e", "math.e")
            total = eval(expression)
            decimals = 0
            while (((total * (10**decimals)) % 1) != 0) and (decimals < 5):
                decimals = decimals + 1
            roundedTotal = str(round(total, decimals))
            calculatorExpression.set(roundedTotal)
            expression = ""

            #Updating previous questions and results
            global prevQArray
            prevQArray.append(str(expressionToAppend))
            prevQ1.config(text = prevQArray[-1])
            prevQ2.config(text = prevQArray[-2])
            prevQ3.config(text = prevQArray[-3])
            prevQ4.config(text = prevQArray[-4])
            prevQ5.config(text = prevQArray[-5])

            global prevResultArray
            prevResultArray.append(str(calculatorExpression.get()))
            prevResult1.config(text=prevResultArray[-1])
            prevResult2.config(text=prevResultArray[-2])
            prevResult3.config(text=prevResultArray[-3])
            prevResult4.config(text=prevResultArray[-4])
            prevResult5.config(text=prevResultArray[-5])


        except:
            calculatorExpression.set(" error ")
            expression = ""

# ==================================================================Main Program===============================================================
mainWindow = Tk()
mainWindow.geometry("1440x900")
mainWindow.title("Maths Revision Program")
mainWindow.configure(bg="#FFF2CC")
main(mainWindow)
mainWindow.mainloop()
