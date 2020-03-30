import tkinter
from tkinter import messagebox
from tkinter import *

class takeInput(object):

    def __init__(self,requestMessage, windowName, isPassw):
        self.root = Tk()
        
        windowWidth = 400 
        windowHeight = 50 
   
        positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.root.winfo_screenheight()/2 - windowHeight/2)
 
        self.root.geometry("+{}+{}".format(positionRight, positionDown))
        self.root.geometry('400x50')
        self.root.title(windowName)
    
        self.string = ''
        self.frame = Frame(self.root)
        self.frame.pack()        
        self.acceptInput(requestMessage, isPassw)
        
    def acceptInput(self,requestMessage, isPassw):
        r = self.frame

        k = Label(r,text=requestMessage)
        k.pack(side='left')
        self.e = Entry(r,text='Name')
        if isPassw:
            self.e.config(show="*");
        self.e.pack(side='left')
        self.e.focus_set()
        b = Button(r,text='okay',command=self.gettext)
        b.pack(side='right')

    def gettext(self):
        self.string = self.e.get()
        self.root.destroy()

    def getString(self):
        return self.string

    def waitForInput(self):
        self.root.wait_window()

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
    count = 0
    while True:
        msgBox = takeInput('Admin password:', 'Admin confirmation', True)
        msgBox.waitForInput()
        answer = msgBox.getString()
        if answer != "Zoologicalfooding2020":
            if count == 2:
                tkinter.messagebox.showinfo("Error", "Too many unsuccessful attempts!")
                return
            tkinter.messagebox.showinfo("Error", "Wrong Password!")    
            count = count + 1
        else:
            break
    tkinter.messagebox.showinfo("Success", "Logged in succesfully")
    
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
