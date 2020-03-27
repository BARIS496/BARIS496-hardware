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

def helloCallBack():
   tkinter.messagebox.showinfo( "Hello Python", "Hello World")

def beforeFilling():
    tkinter.messagebox.showinfo("b", "bb")

def afterFilling():
    tkinter.messagebox.showinfo("a", "aa")
    
def exitProgram():
    mainWindow.destroy()
    
B1 = tkinter.Button(mainWindow, text = "Before filling", command = beforeFilling)
B2 = tkinter.Button(mainWindow, text = "After filling", command = afterFilling)
B3 = tkinter.Button(mainWindow, text = "Quit", command = exitProgram)


B1.pack()
B2.pack()
B3.pack()

mainWindow.mainloop()