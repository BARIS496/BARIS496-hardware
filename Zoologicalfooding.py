import tkinter
from tkinter import messagebox
from tkinter import *
import lcddriver
import time
import RPi.GPIO as GPIO
import requests
import json
import time
from hx711 import HX711
from urllib.request import urlopen
import threading
import sys

headers={'Content-type':'application/json', 'Accept':'application/json'}

beforeWeight = -237.132
beforeTime = -237.132

afterWeight = -237.132
afterTime = -237.132

weight = -12512134123

display = lcddriver.lcd()

hx = None

def tare():
    hx.zero()

B1 = None
B2 = None

def complete(adminWindow, hx, T1, mainWindow, B0, B1, B2):
    global weight
    adminWindow.destroy()
    B0["state"] = "disabled"
    B1["state"] = "active"
    
    T1.config(text = "Status: Working fine!", bg = "green")
    
    sendStatusHTML = urlopen("http://ipinfo.io/json").read()
    mainWindow.update()
    data = json.loads(sendStatusHTML.decode('utf-8'))
    sendStatusIP=data['ip']
    sendStatusOrg=data['org']
    sendStatusCity = data['city']
    sendStatusCountry=data['country']
    sendStatusRegion=data['region']
    sendStatusLoc=data['loc']
    sendStatusLong = sendStatusLoc[:sendStatusLoc.index(',')]
    sendStatusLat = sendStatusLoc[sendStatusLoc.index(',')+1:]
            
    sendStatusHeaders={'Content-type':'application/json', 'Accept':'application/json'}
    sendStatusURL = "https://restservices496.herokuapp.com/editContainer/761"
    sendStatus = {'name':'real container','type':'cat','longitude':sendStatusLat,'latitude':sendStatusLong,'address':'406.Sok Birlik Mah.','weight':0, 'status':'Working fine', 'ip':sendStatusIP,'city':sendStatusCity,'region':sendStatusRegion,'country':sendStatusCountry}
    requests.put(url = sendStatusURL, data=json.dumps(sendStatus),headers=sendStatusHeaders)
    
    wl = tkinter.Label(mainWindow, text="Weight:", height=1, width=20, bg = "navajowhite2")
    wl.configure(font=("Comic Sans MS", 17))
    wl.configure(bg = "lemon chiffon")
    wl.pack()
    wl.place(relx = 0.5, rely = 0.4, anchor = CENTER)
    
    tareButton = tkinter.Button(mainWindow, text = "Tare", command = tare, height = 2, width = 15, bg = "orange", font = ("Comic Sans MS", 14))
    tareButton.pack()
    tareButton.place(relx = 0.5, rely = 0.8, anchor=CENTER)


    mainWindow.update()
    URL3 = "https://restservices496.herokuapp.com/editContainer/761"
    last_time_measured = time.time()
        
    while True:
        mainWindow.update()
        
        try:
            wght = hx.get_weight_mean(20)
        except:
            T1.config(text = "Status: Hardware Problem", bg = "red")
            sendStatusHTML = urlopen("http://ipinfo.io/json").read()
            mainWindow.update()
            data = json.loads(sendStatusHTML.decode('utf-8'))
            sendStatusIP=data['ip']
            sendStatusOrg=data['org']
            sendStatusCity = data['city']
            sendStatusCountry=data['country']
            sendStatusRegion=data['region']
            sendStatusLoc=data['loc']
            sendStatusLong = sendStatusLoc[:sendStatusLoc.index(',')]
            sendStatusLat = sendStatusLoc[sendStatusLoc.index(',')+1:]
                    
            sendStatusHeaders={'Content-type':'application/json', 'Accept':'application/json'}
            sendStatusURL = "https://restservices496.herokuapp.com/editContainer/761"
            sendStatus = {'name':'real container','type':'cat','longitude':sendStatusLat,'latitude':sendStatusLong,'address':'406.Sok Birlik Mah.','weight':0, 'status':'Hardware problem', 'ip':sendStatusIP,'city':sendStatusCity,'region':sendStatusRegion,'country':sendStatusCountry}
            requests.put(url = sendStatusURL, data=json.dumps(sendStatus),headers=sendStatusHeaders)
            
            time.sleep(3)
            adminSetup(T1, mainWindow, B0, B1, B2)
            
            
            
        a = float("{0:.2f}".format(wght))
        wl.config(text= "Weight: "+str(a)+" gr")
        print("%.2f" % wght, 'gr')
        mainWindow.update()
        display.lcd_display_string("Weight:", 1)
        display.lcd_display_string("                             ", 2)
        mainWindow.update()
        display.lcd_display_string("%5.2f gr"%wght, 2)
            
        mainWindow.update()
        
        weight = float("{0:.2f}".format(wght))
        if int(time.time() - last_time_measured) > 15:
            mainWindow.update()
            html = urlopen("http://ipinfo.io/json").read()
            mainWindow.update()
            data = json.loads(html.decode('utf-8'))
            IP=data['ip']
            org=data['org']
            city = data['city']
            country=data['country']
            region=data['region']
            loc=data['loc']
            long = loc[:loc.index(',')]
            lat = loc[loc.index(',')+1:]

            headers={'Content-type':'application/json', 'Accept':'application/json'}
            mainWindow.update()
            URL3 = "https://restservices496.herokuapp.com/editContainer/761"
            #data = {'name':'real container','type':'dosdsdsg','longitude':1,'latitude':1,'address':'a','weight':0, 'ip':'a','city':'a','region':'a','country':'a'}
            data = {'name':'real container','type':'cat','longitude':lat,'latitude':long,'address':'406.Sok Birlik Mah.','weight':weight, 'status':'Working fine', 'ip':IP,'city':city,'region':region,'country':country}
            r3 = requests.put(url = URL3, data=json.dumps(data),headers=headers)
            mainWindow.update()

            w = str(weight)
            print("Weight : " + w + " gr , Location: " + lat + ", " + long + ", " + city + ", " + country + ", IP: " + IP + " sent to database")

            last_time_measured = time.time()
            
    
def adminWindowGetWeight(adminWindow, reading, hx, e1, T1, mainWindow, B0, B1, B2):
    known_weight_grams = e1.get()
    
        
    try:
        value = float(known_weight_grams)

    except ValueError:
        T1.config(text = "Status: Hardware Problem", bg = "red")
        sendStatusHTML = urlopen("http://ipinfo.io/json").read()
        mainWindow.update()
        data = json.loads(sendStatusHTML.decode('utf-8'))
        sendStatusIP=data['ip']
        sendStatusOrg=data['org']
        sendStatusCity = data['city']
        sendStatusCountry=data['country']
        sendStatusRegion=data['region']
        sendStatusLoc=data['loc']
        sendStatusLong = sendStatusLoc[:sendStatusLoc.index(',')]
        sendStatusLat = sendStatusLoc[sendStatusLoc.index(',')+1:]
                
        sendStatusHeaders={'Content-type':'application/json', 'Accept':'application/json'}
        sendStatusURL = "https://restservices496.herokuapp.com/editContainer/761"
        sendStatus = {'name':'real container','type':'cat','longitude':sendStatusLat,'latitude':sendStatusLong,'address':'406.Sok Birlik Mah.','weight':0, 'status':'Hardware problem', 'ip':sendStatusIP,'city':sendStatusCity,'region':sendStatusRegion,'country':sendStatusCountry}
        requests.put(url = sendStatusURL, data=json.dumps(sendStatus),headers=sendStatusHeaders)

    ratio = reading / value
    hx.set_scale_ratio(ratio)
    #print('Scaling done')
    long_string(display, "Scaling done", 1)
    time.sleep(1)
    display.lcd_display_string("                            ", 1)
    display.lcd_display_string("                            ", 2)
    #else:
        #raise ValueError('Cannot calculate the incoming value')


    a7 = tkinter.Button(adminWindow, text='Complete the setup and start measuring (exits admin mode)', command = lambda: complete(adminWindow, hx, T1, mainWindow, B0, B1, B2))
    a7.place(relx = 0.5, rely = 0.7, anchor=CENTER)
    a7.configure(bg = "lemon chiffon")
       
    
                
    
def adminWindowWeightPut(adminWindow, reading, hx, T1, mainWindow, B0, B1, B2):
    reading = hx.get_data_mean()
    if reading:
            
            
        a4 = tkinter.Label(adminWindow, text="Weight of the object:")
        a4.place(relx = 0.5, rely = 0.45, anchor=CENTER)
        a4.configure(bg = "lemon chiffon")
        e1 = tkinter.Entry(adminWindow)
        e1.configure(bg = "lemon chiffon")
        e1.place(relx = 0.5, rely = 0.5, anchor=CENTER)
        a5 = tkinter.Button(adminWindow, text='enter', command = lambda: adminWindowGetWeight(adminWindow, reading, hx, e1, T1, mainWindow, B0, B1, B2))
        a5.configure(bg = "lemon chiffon")
        a5.place(relx = 0.5, rely = 0.55, anchor=CENTER)
        
        
       
        
  
    
    
#this func will be used if needed
def long_string(display, text = '', num_line = 1, num_cols = 20):
    if(len(text) > num_cols):
        display.lcd_display_string(text[:num_cols],num_line)
        time.sleep(1)
        for i in range(len(text) - num_cols + 5):
            text_to_print = text[i:i+num_cols]
            display.lcd_display_string(text_to_print,num_line)
            time.sleep(0.2)
    else:
        display.lcd_display_string(text,num_line)
        display = lcddriver.lcd()

def startHardware(adminWindow, T1, mainWindow, B0, B1, B2):
    try:
        display.lcd_display_string("Hi!", 1)
        display.lcd_display_string(":)", 2)
        GPIO.setmode(GPIO.BCM)

        global hx
        hx = HX711(dout_pin=5, pd_sck_pin=6)

        error=None
        try:
            error = hx.zero()
        except:
            T1.config(text = "Status: Hardware Problem", bg = "red")
            sendStatusHTML = urlopen("http://ipinfo.io/json").read()
            mainWindow.update()
            data = json.loads(sendStatusHTML.decode('utf-8'))
            sendStatusIP=data['ip']
            sendStatusOrg=data['org']
            sendStatusCity = data['city']
            sendStatusCountry=data['country']
            sendStatusRegion=data['region']
            sendStatusLoc=data['loc']
            sendStatusLong = sendStatusLoc[:sendStatusLoc.index(',')]
            sendStatusLat = sendStatusLoc[sendStatusLoc.index(',')+1:]
                    
            sendStatusHeaders={'Content-type':'application/json', 'Accept':'application/json'}
            sendStatusURL = "https://restservices496.herokuapp.com/editContainer/761"
            sendStatus = {'name':'real container','type':'cat','longitude':sendStatusLat,'latitude':sendStatusLong,'address':'406.Sok Birlik Mah.','weight':0, 'status':'Hardware problem', 'ip':sendStatusIP,'city':sendStatusCity,'region':sendStatusRegion,'country':sendStatusCountry}
            requests.put(url = sendStatusURL, data=json.dumps(sendStatus),headers=sendStatusHeaders)
            
            raise ValueError('fix cables')
        
        reading=None
        try:
            reading = hx.get_raw_data_mean()
        except:
            T1.config(text = "Status: Hardware Problem", bg = "red")
            sendStatusHTML = urlopen("http://ipinfo.io/json").read()
            mainWindow.update()
            data = json.loads(sendStatusHTML.decode('utf-8'))
            sendStatusIP=data['ip']
            sendStatusOrg=data['org']
            sendStatusCity = data['city']
            sendStatusCountry=data['country']
            sendStatusRegion=data['region']
            sendStatusLoc=data['loc']
            sendStatusLong = sendStatusLoc[:sendStatusLoc.index(',')]
            sendStatusLat = sendStatusLoc[sendStatusLoc.index(',')+1:]
                    
            sendStatusHeaders={'Content-type':'application/json', 'Accept':'application/json'}
            sendStatusURL = "https://restservices496.herokuapp.com/editContainer/761"
            sendStatus = {'name':'real container','type':'cat','longitude':sendStatusLat,'latitude':sendStatusLong,'address':'406.Sok Birlik Mah.','weight':0, 'status':'Hardware problem', 'ip':sendStatusIP,'city':sendStatusCity,'region':sendStatusRegion,'country':sendStatusCountry}
            requests.put(url = sendStatusURL, data=json.dumps(sendStatus),headers=sendStatusHeaders)
            
            raise ValueError('fix cables')
        
        if not reading:
            T1.config(text = "Status: Hardware Problem", bg = "red")
            sendStatusHTML = urlopen("http://ipinfo.io/json").read()
            mainWindow.update()
            data = json.loads(sendStatusHTML.decode('utf-8'))
            sendStatusIP=data['ip']
            sendStatusOrg=data['org']
            sendStatusCity = data['city']
            sendStatusCountry=data['country']
            sendStatusRegion=data['region']
            sendStatusLoc=data['loc']
            sendStatusLong = sendStatusLoc[:sendStatusLoc.index(',')]
            sendStatusLat = sendStatusLoc[sendStatusLoc.index(',')+1:]
                    
            sendStatusHeaders={'Content-type':'application/json', 'Accept':'application/json'}
            sendStatusURL = "https://restservices496.herokuapp.com/editContainer/761"
            sendStatus = {'name':'real container','type':'cat','longitude':sendStatusLat,'latitude':sendStatusLong,'address':'406.Sok Birlik Mah.','weight':0, 'status':'Hardware problem', 'ip':sendStatusIP,'city':sendStatusCity,'region':sendStatusRegion,'country':sendStatusCountry}
            requests.put(url = sendStatusURL, data=json.dumps(sendStatus),headers=sendStatusHeaders)

            input('hardware problem')
       
   
    
  


        a2 = tkinter.Label(adminWindow, text="Place a known weighted object and press")
        a2.place(relx = 0.5, rely = 0.25, anchor=CENTER)
        a2.configure(bg = "lemon chiffon")
        a3 = tkinter.Button(adminWindow, text='here', command= lambda: adminWindowWeightPut(adminWindow, reading, hx, T1, mainWindow, B0, B1, B2))
        a3.place(relx = 0.5, rely = 0.3, anchor=CENTER)
        a3.configure(bg = "lemon chiffon")
        
        
        
        
        
    except (KeyboardInterrupt, SystemExit):
        print('The program ended')    
            

def adminSetup(T1, mainWindow, B0, B1, B2):
    count = 0
    while True:
        msgBox = takeInput('Admin password:', 'Admin confirmation', True)
        msgBox.waitForInput()
        answer = msgBox.getString()
        if answer != "Zoologicalfooding2020":
            if count == 2:
                a = tkinter.messagebox.showinfo("Error", "Too many unsuccessful attempts!")
                return
            tkinter.messagebox.showinfo("Error", "Wrong Password!")    
            count = count + 1
        else:
            break
    tkinter.messagebox.showinfo("Success", "Logged in succesfully")
    
    adminWindow = tkinter.Tk()
    awindowWidth = 600 
    awindowHeight = 600 
   
    apositionRight = int(adminWindow.winfo_screenwidth()/2 - awindowWidth/2)
    apositionDown = int(adminWindow.winfo_screenheight()/2 - awindowHeight/2)
 
    adminWindow.geometry("+{}+{}".format(apositionRight, apositionDown))
    adminWindow.geometry('600x600')
    adminWindow.title("setup")
    adminWindow.configure(bg = "papaya whip")
    
    a1 = tkinter.Button(adminWindow, text='Start the hardware', command= lambda: threading.Thread(target=startHardware(adminWindow, T1, mainWindow, B0, B1, B2)).start())
    a1.place(relx = 0.5, rely = 0.1, anchor = CENTER)
    a1.configure(bg = "lemon chiffon")
    



    
    
    
#   e1 = tkinter.Entry(adminWindow)
#   e2 = tkinter.Entry(adminWindow)

#   e1.grid(row=2, column=1)
#   e2.grid(row=3, column=1)

    

def aboutTheDestroy(wind, txt, which):
    aa = tkinter.Label(wind, text=txt, height=1, width=70, bg = "papaya whip")
    aa.configure(font=("Comic Sans MS", 12))
    aa.pack()
    aa.place(relx = 0.5, rely = 0.3, anchor = CENTER)

    bb = tkinter.Label(wind, text="5", height=1, width=1, bg = "papaya whip")
    bb.configure(font=("Comic Sans MS", 17))
    bb.pack()
    bb.place(relx = 0.5, rely = 0.6, anchor = CENTER)
    wind.update()
    time.sleep(1)
    bb.config(text = "4")
    wind.update()
    time.sleep(1)
    bb.config(text = "3")
    wind.update()
    time.sleep(1)
    bb.config(text = "2")
    wind.update()
    time.sleep(1)
    bb.config(text = "1")
    wind.update()
    time.sleep(1)
    wind.destroy()
    
    
    global beforeWeight
    global beforeTime
    global afterTime
    global afterWeight
    
    global B1
    global B2
    
    global mainWindow
    
    if which == "before":
        
        beforeWeight = weight
        beforeTime = time.time()
        
        
        if afterTime == -237.132:
            print("no guesses on the first time")
        else:   
            timeChange = beforeTime - afterTime
            weightChange = beforeWeight - afterWeight
            
            
            timeChange = float("{0:.2f}".format(timeChange))
            weightChange = float("{0:.2f}".format(weightChange))
        
            print(weightChange, " gr food exhausted in ", timeChange, " second")
            
    B1["state"] = "disabled"
    B2["state"] = "active"
    mainWindow.update()        
    
    if which == "after":
        
        afterWeight = weight
        afterTime = time.time()
      
        weightPut = afterWeight - beforeWeight
        
        
        
        weightPut = float("{0:.2f}".format(weightPut))
        
        
        print("weight put: ", weightPut)
        
        B1["state"] = "active"
        B2["state"] = "disabled"
        mainWindow.update()
        
    
def beforeFilling():
    bFillingWindow = tkinter.Tk()
    awindowWidth = 700 
    awindowHeight = 300 
   
    apositionRight = int(bFillingWindow.winfo_screenwidth()/2 - awindowWidth/2)
    apositionDown = int(bFillingWindow.winfo_screenheight()/2 - awindowHeight/2)
 
    bFillingWindow.geometry("+{}+{}".format(apositionRight, apositionDown))
    bFillingWindow.geometry('700x300')
    bFillingWindow.title("setup")
    bFillingWindow.configure(bg = "papaya whip")
    
    x = tkinter.Button(bFillingWindow, text='Ready', command= lambda: aboutTheDestroy(bFillingWindow, "The weight will be saved after this window closes", "before"))
    x.place(relx = 0.5, rely = 0.1, anchor = CENTER)
    x.configure(bg = "lemon chiffon")
    
    
    
    
    
        

def afterFilling():
    
    aFillingWindow = tkinter.Tk()
    awindowWidth = 700 
    awindowHeight = 300 
   
    apositionRight = int(aFillingWindow.winfo_screenwidth()/2 - awindowWidth/2)
    apositionDown = int(aFillingWindow.winfo_screenheight()/2 - awindowHeight/2)
 
    aFillingWindow.geometry("+{}+{}".format(apositionRight, apositionDown))
    aFillingWindow.geometry('700x300')
    aFillingWindow.title("setup")
    aFillingWindow.configure(bg = "papaya whip")
    
    x = tkinter.Button(aFillingWindow, text='Ready', command= lambda: aboutTheDestroy(aFillingWindow, "Approximate food exhaustion time will  be calculated after this window closes", "after"))
    x.place(relx = 0.5, rely = 0.1, anchor = CENTER)
    x.configure(bg = "lemon chiffon")
    
def exitProgram():
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
            sys.exit()
    
    


class takeInput(object):

    def __init__(self,requestMessage, windowName, isPassw):
        self.root = Tk()
        self.root.configure(bg = "papaya whip")
        windowWidth = 400 
        windowHeight = 50 
   
        positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.root.winfo_screenheight()/2 - windowHeight/2)
 
        self.root.geometry("+{}+{}".format(positionRight, positionDown))
        self.root.geometry('400x50')
        self.root.title(windowName)
    
        self.string = ''
        self.frame = Frame(self.root)
        self.frame.configure(bg = "lemon chiffon")
        self.frame.pack()        
        self.acceptInput(requestMessage, isPassw)
        
    def acceptInput(self,requestMessage, isPassw):
        r = self.frame

        k = Label(r,text=requestMessage)
        k.configure(bg = "lemon chiffon")
        k.pack(side='left')
        self.e = Entry(r,text='Name')
        if isPassw:
            self.e.config(show="*");
        self.e.pack(side='left')
        self.e.focus_set()
        b = Button(r,text='okay',command=self.gettext)
        b.configure(bg = "lemon chiffon")
        b.pack(side='right')

    def gettext(self):
        self.string = self.e.get()
        self.root.destroy()

    def getString(self):
        return self.string

    def waitForInput(self):
        self.root.wait_window()
        
        
URL = "http://restservices496.herokuapp.com/containers"
id = 1
PARAMS = {'container_id':id}
r = requests.get(url = URL, params = PARAMS)
data = r.json()
print("Existing containers:")
print(data)


mainWindow = tkinter.Tk()
mainWindow.title("Zoologicalfooding")


       
    
mainWindow.attributes('-fullscreen', True)

photo = tkinter.PhotoImage(file = "pic1.png")
background_label = tkinter.Label(mainWindow, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

T = tkinter.Label(mainWindow, text="Welcome to ZoologicalFooding!\nContainer Id:761", height=2, width=26, bg = "navajowhite2")
T.configure(font=("Comic Sans MS", 17))
T.pack()
T.place(relx = 0.5, rely = 0.2, anchor = CENTER)

T1 = tkinter.Label(mainWindow, text="Status: Setup needed", height=2, width=26, bg = "red")
T1.configure(font=("Comic Sans MS", 17))
T1.pack()
T1.place(relx = 0.5, rely = 0.3, anchor = CENTER)



B0 = tkinter.Button(mainWindow, text = "Setup (Admin)", command = lambda: adminSetup(T1, mainWindow, B0, B1, B2), height = 2, width = 15, bg = "orange", font = ("Comic Sans MS", 14))

B2 = tkinter.Button(mainWindow, text = "After filling", command = afterFilling, height = 2, width = 15, bg = "orange", font = ("Comic Sans MS", 14))
B3 = tkinter.Button(mainWindow, text = "Quit (Admin)", command = exitProgram, height = 2, width = 15, bg = "orange", font = ("Comic Sans MS", 14))
B1 = tkinter.Button(mainWindow, text = "Before filling", command = beforeFilling, height = 2, width = 15, bg = "orange", font = ("Comic Sans MS", 14))

B0.pack()
B1.pack()
B2.pack()
B3.pack()

B0.place(relx = 0.5, rely = 0.50, anchor=CENTER)
B1.place(relx=0.5, rely=0.60, anchor=CENTER)
B2.place(relx=0.5, rely=0.70, anchor=CENTER)
B3.place(relx=0.5, rely=0.90, anchor=CENTER)

B1["state"] = "disabled"
B2["state"] = "disabled"

html = urlopen("http://ipinfo.io/json").read()
data = json.loads(html.decode('utf-8'))
IP=data['ip']
org=data['org']
city = data['city']
country=data['country']
region=data['region']
loc=data['loc']
long = loc[:loc.index(',')]
lat = loc[loc.index(',')+1:]
headers={'Content-type':'application/json', 'Accept':'application/json'}
URL3 = "https://restservices496.herokuapp.com/editContainer/761"
data = {'name':'real container','type':'cat','longitude':lat,'latitude':long,'address':'406.Sok Birlik Mah.','weight':0, 'status': 'setup needed', 'ip':IP,'city':city,'region':region,'country':country}
r33 = requests.put(url = URL3, data=json.dumps(data),headers=headers)
            
mainWindow.mainloop()


