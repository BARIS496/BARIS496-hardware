import tkinter
from tkinter import messagebox
from tkinter import *

mainWindow = tkinter.Tk()

windowWidth = mainWindow.winfo_reqwidth()
windowHeight = mainWindow.winfo_reqheight()

positionRight = int(mainWindow.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(mainWindow.winfo_screenheight()/2 - windowHeight/2)
 

mainWindow.attributes('-fullscreen', True)

photo = tkinter.PhotoImage(file = "pic1.png")
background_label = tkinter.Label(mainWindow, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

T = tkinter.Text(mainWindow, height=2, width=24, bg = "navajowhite2")
T.configure(font=("Comic Sans MS", 17))
T.pack()
T.place(relx = 0.5, rely = 0.2, anchor = CENTER)
T.insert(tkinter.END, "Welcome to ZoologicalFooding!\n           Container Id:761\n")
T.configure(state='disabled')

def beforeFilling():
    tkinter.messagebox.showinfo("b", "bb")

def afterFilling():
    tkinter.messagebox.showinfo("a", "aa")
    
def exitProgram():
    mainWindow.destroy()
    
B1 = tkinter.Button(mainWindow, text = "Before filling", command = beforeFilling, height = 2, width = 15, bg = "orange", font = ("Comic Sans MS", 14))
B2 = tkinter.Button(mainWindow, text = "After filling", command = afterFilling, height = 2, width = 15, bg = "orange", font = ("Comic Sans MS", 14))
B3 = tkinter.Button(mainWindow, text = "Quit", command = exitProgram, height = 2, width = 15, bg = "orange", font = ("Comic Sans MS", 14))


B1.pack()
B2.pack()
B3.pack()

B1.place(relx=0.5, rely=0.50, anchor=CENTER)
B2.place(relx=0.5, rely=0.60, anchor=CENTER)
B3.place(relx=0.5, rely=0.80, anchor=CENTER)

mainWindow.mainloop()