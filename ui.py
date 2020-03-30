import tkinter
from tkinter import messagebox
from tkinter import *


mainWindow = tkinter.Tk()



mainWindow.attributes('-fullscreen', True)

photo = tkinter.PhotoImage(file = "pic1.png")
background_label = tkinter.Label(mainWindow, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

T = tkinter.Text(mainWindow, height=2, width=26, bg = "navajowhite2")
T.configure(font=("Comic Sans MS", 17))
T.pack()
T.place(relx = 0.5, rely = 0.2, anchor = CENTER)
T.insert(tkinter.END, "Welcome to ZoologicalFooding!\n           Container Id:761\n")
T.configure(state='disabled')

def adminSetup():
    window = tkinter.Toplevel(mainWindow)
    windowWidth = 600 #window.winfo_reqwidth()
    windowHeight = 600 #window.winfo_reqheight()

 
    # Gets both half the screen width/height and window width/height
    positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(window.winfo_screenheight()/2 - windowHeight/2)
 
    # Positions the window in the center of the page.
    window.geometry("+{}+{}".format(positionRight, positionDown))
    window.geometry('600x600')
    
def beforeFilling():
    tkinter.messagebox.showinfo("b", "bb")

def afterFilling():
    tkinter.messagebox.showinfo("a", "aa")
    
def exitProgram():
    mainWindow.destroy()

B0 = tkinter.Button(mainWindow, text = "Setup (Admin)", command = adminSetup, height = 2, width = 15, bg = "orange", font = ("Comic Sans MS", 14))
B1 = tkinter.Button(mainWindow, text = "Before filling", command = beforeFilling, height = 2, width = 15, bg = "orange", font = ("Comic Sans MS", 14))
B2 = tkinter.Button(mainWindow, text = "After filling", command = afterFilling, height = 2, width = 15, bg = "orange", font = ("Comic Sans MS", 14))
B3 = tkinter.Button(mainWindow, text = "Quit", command = exitProgram, height = 2, width = 15, bg = "orange", font = ("Comic Sans MS", 14))

B0.pack()
B1.pack()
B2.pack()
B3.pack()

B0.place(relx = 0.5, rely = 0.50, anchor=CENTER)
B1.place(relx=0.5, rely=0.60, anchor=CENTER)
B2.place(relx=0.5, rely=0.70, anchor=CENTER)
B3.place(relx=0.5, rely=0.90, anchor=CENTER)

mainWindow.mainloop()