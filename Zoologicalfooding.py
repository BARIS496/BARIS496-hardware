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
import os

import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression

train_features = np.array([[0]])
train_results = np.array([0])

classifier = LinearRegression()

estimationLast = None
# helper method to predict_new_result and incremental_fit
def train(train_features, train_results):
    # train_features = minmax_scale.fit_transform(train_features)
 
    classifier.fit(train_features, train_results)


# new_train_features = [[5], [6]]
# new_train_results = [[10]]
def incremental_fit(new_train_features, new_train_results, train_features, train_results):
    train_features = np.append(train_features, new_train_features)
    train_features = np.array([train_features]).reshape(-1, 1)

    train_results = np.append(train_results, new_train_results)
    train_results = np.array([train_results]).reshape(-1, 1)
    train(train_features, train_results)
    return train_features, train_results

def predict_new_value(train_features, train_results, feature_to_be_predicted):
    train(train_features, train_results)
    # scaled_feature = minmax_scale.transform(np.array([feature_to_be_predicted]))
    predicted_result = classifier.predict(np.array([feature_to_be_predicted]))
    return predicted_result



URL = "http://restservices496.herokuapp.com/containers"
id = 1
PARAMS = {'container_id':id}
r = requests.get(url = URL, params = PARAMS)
data = r.json()

password = None
infoLabel = None

countt = 0

while countt < len(data):
    if data[countt]['containerID'] == 761:
        password = data[countt]['passCont']
        break
    countt = countt + 1


saveName = data[countt]['name']
saveType = data[countt]['type']
saveDonatesList = data[countt]['donatesList']
saveCommentsList = data[countt]['commentsList']



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
data = {'donatesList': saveDonatesList,'commentsList':saveCommentsList, 'name':saveName,'type':saveType,'longitude':lat,'latitude':long,'address':'406.Sok Birlik Mah.','weight':0, 'passCont': password,'status': '1', 'ip':IP,'city':city,'region':region,'country':country}
r33 = requests.put(url = URL3, data=json.dumps(data),headers=headers)



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
    global password
    global estimationLast
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
    
    URL = "http://restservices496.herokuapp.com/containers"
    id = 1
    PARAMS = {'container_id':id}
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()

    

    countt = 0

    while countt < len(data):
        if data[countt]['containerID'] == 761:
            password = data[countt]['passCont']
            break
        countt = countt + 1


    saveName = data[countt]['name']
    saveType = data[countt]['type']
    saveDonatesList = data[countt]['donatesList']
    saveCommentsList = data[countt]['commentsList']

    sendStatus = {'donatesList': saveDonatesList, 'commentsList':saveCommentsList, 'name':saveName,'type':saveType, 'passCont': password, 'longitude':sendStatusLat,'latitude':sendStatusLong,'address':'406.Sok Birlik Mah.','weight':0, 'status':'0', 'ip':sendStatusIP,'city':sendStatusCity,'region':sendStatusRegion,'country':sendStatusCountry}
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
        except SystemExit:
            os._exit(0)
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
            URL = "http://restservices496.herokuapp.com/containers"
            id = 1
            PARAMS = {'container_id':id}
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()

           

            countt = 0

            while countt < len(data):
                if data[countt]['containerID'] == 761:
                    password = data[countt]['passCont']
                    break
                countt = countt + 1


            saveName = data[countt]['name']
            saveType = data[countt]['type']
            saveDonatesList = data[countt]['donatesList']
            saveCommentsList = data[countt]['commentsList']
            sendStatus = {'donatesList': saveDonatesList, 'commentsList':saveCommentsList, 'name':saveName,'type':saveType, 'passCont': password, 'longitude':sendStatusLat,'latitude':sendStatusLong,'address':'406.Sok Birlik Mah.','weight':0, 'status':'2', 'ip':sendStatusIP,'city':sendStatusCity,'region':sendStatusRegion,'country':sendStatusCountry}
            requests.put(url = sendStatusURL, data=json.dumps(sendStatus),headers=sendStatusHeaders)
            
            time.sleep(3)
            adminSetup(T1, mainWindow, B0, B1, B2)
            
            
            
        a = float("{0:.2f}".format(wght))
        if a < 0:
            a = 0
        if wght < 0:
            wght = 0
        wl.config(text= "Weight: "+str(a)+" gr")
        print("%.2f" % wght, 'gr')
        mainWindow.update()
        display.lcd_display_string("Weight:", 1)
        display.lcd_display_string("                             ", 2)
        mainWindow.update()
        display.lcd_display_string("%5.2f gr"%wght, 2)
            
        mainWindow.update()
        
        weight = float("{0:.2f}".format(wght))
        
        if weight < 0:
            weight = 0
       
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
            
            URL = "http://restservices496.herokuapp.com/containers"
            id = 1
            PARAMS = {'container_id':id}
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()


            countt = 0

            while countt < len(data):
                if data[countt]['containerID'] == 761:
                    password = data[countt]['passCont']
                    break
                countt = countt + 1


            saveName = data[countt]['name']
            saveType = data[countt]['type']
            saveDonatesList = data[countt]['donatesList']
            saveCommentsList = data[countt]['commentsList']

            #data = {'name':'real container','type':'dosdsdsg','longitude':1,'latitude':1,'address':'a','weight':0, 'ip':'a','city':'a','region':'a','country':'a'}
            data = {'donatesList': saveDonatesList, 'commentsList': saveCommentsList, 'name':saveName,'type':saveType,'passCont':password,'longitude':lat,'latitude':long,'address':'406.Sok Birlik Mah.','weight':weight, 'status':'0', 'ip':IP,'city':city,'region':region,'country':country, 'passCont':'Zoologicalfooding2020', 'estimation':estimationLast}
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
        global password
        
        URL = "http://restservices496.herokuapp.com/containers"
        id = 1
        PARAMS = {'container_id':id}
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()

     
        countt = 0

        while countt < len(data):
            if data[countt]['containerID'] == 761:
                password = data[countt]['passCont']
                break
            countt = countt + 1


        saveName = data[countt]['name']
        saveType = data[countt]['type']
        saveDonatesList = data[countt]['donatesList']
        saveCommentsList = data[countt]['commentsList']


        sendStatusHeaders={'Content-type':'application/json', 'Accept':'application/json'}
        sendStatusURL = "https://restservices496.herokuapp.com/editContainer/761"
        sendStatus = {'donatesList': saveDonatesList, 'commentsList': saveCommentsList, 'name':saveName,'type':saveType, 'passCont':password,'longitude':sendStatusLat,'latitude':sendStatusLong,'address':'406.Sok Birlik Mah.','weight':0, 'status':'2', 'ip':sendStatusIP,'city':sendStatusCity,'region':sendStatusRegion,'country':sendStatusCountry}
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
    global password
    try:
        display.lcd_display_string("Hi!", 1)
        display.lcd_display_string(":)", 2)
        GPIO.setmode(GPIO.BCM)

        global hx
        hx = HX711(dout_pin=5, pd_sck_pin=6)

        error=None
        try:
            error = hx.zero()
        except SystemExit:
            os._exit(0)
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
            
            URL = "http://restservices496.herokuapp.com/containers"
            id = 1
            PARAMS = {'container_id':id}
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()

         
            countt = 0

            while countt < len(data):
                if data[countt]['containerID'] == 761:
                    password = data[countt]['passCont']
                    break
                countt = countt + 1


            saveName = data[countt]['name']
            saveType = data[countt]['type']
            saveDonatesList = data[countt]['donatesList']
            saveCommentsList = data[countt]['commentsList']


             
            sendStatusHeaders={'Content-type':'application/json', 'Accept':'application/json'}
            sendStatusURL = "https://restservices496.herokuapp.com/editContainer/761"
            sendStatus = {'commentsList': saveCommentsList, 'donatesList': saveDonatesList, 'name':saveName,'type':saveType, 'passCont': password,'longitude':sendStatusLat,'latitude':sendStatusLong,'address':'406.Sok Birlik Mah.','weight':0, 'status':'2', 'ip':sendStatusIP,'city':sendStatusCity,'region':sendStatusRegion,'country':sendStatusCountry}
            requests.put(url = sendStatusURL, data=json.dumps(sendStatus),headers=sendStatusHeaders)
            
            raise ValueError('fix cables')
        
        reading=None
        try:
            reading = hx.get_raw_data_mean()
        except SystemExit:
            os._exit(0)
            
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
                 
                 
            URL = "http://restservices496.herokuapp.com/containers"
            id = 1
            PARAMS = {'container_id':id}
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()


            countt = 0

            while countt < len(data):
                if data[countt]['containerID'] == 761:
                    password = data[countt]['passCont']
                    break
                countt = countt + 1


            saveName = data[countt]['name']
            saveType = data[countt]['type']
            saveDonatesList = data[countt]['donatesList']
            saveCommentsList = data[countt]['commentsList']


            sendStatusHeaders={'Content-type':'application/json', 'Accept':'application/json'}
            sendStatusURL = "https://restservices496.herokuapp.com/editContainer/761"
            sendStatus = {'donatesList': saveDonatesList, 'commentsList': saveCommentsList, 'name':saveName,'type':saveType, 'passCont': password, 'longitude':sendStatusLat,'latitude':sendStatusLong,'address':'406.Sok Birlik Mah.','weight':0, 'status':'2', 'ip':sendStatusIP,'city':sendStatusCity,'region':sendStatusRegion,'country':sendStatusCountry}
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
            
            
            URL = "http://restservices496.herokuapp.com/containers"
            id = 1
            PARAMS = {'container_id':id}
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()

         

            countt = 0

            while countt < len(data):
                if data[countt]['containerID'] == 761:
                    password = data[countt]['passCont']
                    break
                countt = countt + 1


            saveName = data[countt]['name']
            saveType = data[countt]['type']
            saveDonatesList = data[countt]['donatesList']
            saveCommentsList = data[countt]['commentsList']


            sendStatusHeaders={'Content-type':'application/json', 'Accept':'application/json'}
            sendStatusURL = "https://restservices496.herokuapp.com/editContainer/761"
            sendStatus = {'donatesList': saveDonatesList, 'commentsList':saveCommentsList, 'name':saveName,'type':saveType,'passCont':password,'longitude':sendStatusLat,'latitude':sendStatusLong,'address':'406.Sok Birlik Mah.','weight':0, 'status':'2', 'ip':sendStatusIP,'city':sendStatusCity,'region':sendStatusRegion,'country':sendStatusCountry}
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
    global password
    global windowChecker
    while True:
        msgBox = takeInput('Admin password:', 'Admin confirmation', True)
        msgBox.waitForInput()
        answer = msgBox.getString()
        if windowChecker:
            windowChecker = False
            return
        print(answer)
        print(password)
        if answer != password:
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

afterFillingCounter = 0
estimationLabel = None
estimation = ""

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
    
    global afterFillingCounter
    global estimationLabel
    global estimation
    
    global infoLabel
    
    global train_features
    global train_results
    
    global estimationLast
    
    if which == "before":
        
        beforeWeight = weight
        beforeTime = time.time()
       

        if afterTime == -237.132:
            print("no guesses on the first time")
            
        
        
        else:   
            timeChange = beforeTime - afterTime
            weightChange = afterWeight - beforeWeight
            
            new_train_features = np.array([weightChange])
            new_train_results = np.array([timeChange])
            train_features, train_results = incremental_fit(new_train_features, new_train_results, train_features, train_results)
             
            timeChange = float("{0:.2f}".format(timeChange))
            weightChange = float("{0:.2f}".format(weightChange))
            
            
        
            print(weightChange, " gr food exhausted in ", timeChange, " second")
            infoLabel.config(text = str(weightChange) + " gr food exhausted in " + str(timeChange) + " second")
            
    B1["state"] = "disabled"
    B2["state"] = "active"
    mainWindow.update()        
    
    if which == "after":
        
        afterWeight = weight
        afterTime = time.time()
      
        weightPut = afterWeight - beforeWeight
        
        
        
        weightPut = float("{0:.2f}".format(weightPut))
        
        
        print("weight put: ", weightPut)
        
         
        if afterFillingCounter > 1:
            #estimation = ?
            
            infoLabel.config(text = "Weight put: " + str(weightPut))
            
            estimation = predict_new_value(train_features, train_results, [weight])
            estimationS = str(estimation)
            print(estimationS)
            estimationF = estimationS[2:-2]
            
            estimationF = "{0:.2f}".format(float(estimationF))
            print(estimationF)
            
            estimationHelper = float(estimationF)
            
            
            
            estimationLast = str(int(estimationHelper/3600)) + " hour " + str((int((estimationHelper%3600)/60))) + " minute " + str(((int((estimationHelper%3600))%60))) + " second" 
            
            print(weight)
            
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
            
            URL = "http://restservices496.herokuapp.com/containers"
            id = 1
            PARAMS = {'container_id':id}
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()

            

            countt = 0

            while countt < len(data):
                if data[countt]['containerID'] == 761:
                    password = data[countt]['passCont']
                    break
                countt = countt + 1


            saveName = data[countt]['name']
            saveType = data[countt]['type']
            saveDonatesList = data[countt]['donatesList']
            saveCommentsList = data[countt]['commentsList']


            URL3 = "https://restservices496.herokuapp.com/editContainer/761"
            #data = {'name':'real container','type':'dosdsdsg','longitude':1,'latitude':1,'address':'a','weight':0, 'ip':'a','city':'a','region':'a','country':'a'}
            data = {'donatesList' : saveDonatesList, 'commentsList':saveCommentsList, 'name':saveName,'type':saveType,'passCont':password,'longitude':lat,'latitude':long,'address':'406.Sok Birlik Mah.','weight':weight, 'status':'0', 'ip':IP,'city':city,'region':region,'country':country, 'passCont':'Zoologicalfooding2020', 'estimation':estimationLast}
            r3 = requests.put(url = URL3, data=json.dumps(data),headers=headers)
            
            
            
            
            
            estimationLabel.config(text="Approximate exhaustion time: " + estimationLast)
            
        if afterFillingCounter == 1:
            estimation = predict_new_value(train_features, train_results, [weight])
            
            estimationS = str(estimation)
            print(estimationS)
            estimationF = estimationS[2:-2]
            
            estimationF = "{0:.2f}".format(float(estimationF))
            print(estimationF)
            
            estimationHelper = float(estimationF)
            
            
            
            estimationLast = str(int(estimationHelper/3600)) + " hour " + str((int((estimationHelper%3600)/60))) + " minute " + str(((int((estimationHelper%3600))%60))) + " second" 
            
            print(weight)
            
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
            
            URL = "http://restservices496.herokuapp.com/containers"
            id = 1
            PARAMS = {'container_id':id}
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()

         

            countt = 0

            while countt < len(data):
                if data[countt]['containerID'] == 761:
                    password = data[countt]['passCont']
                    break
                countt = countt + 1


            saveName = data[countt]['name']
            saveType = data[countt]['type']
            saveDonatesList = data[countt]['donatesList']
            saveCommentsList = data[countt]['commentsList']


            headers={'Content-type':'application/json', 'Accept':'application/json'}
            mainWindow.update()
            URL3 = "https://restservices496.herokuapp.com/editContainer/761"
            #data = {'name':'real container','type':'dosdsdsg','longitude':1,'latitude':1,'address':'a','weight':0, 'ip':'a','city':'a','region':'a','country':'a'}
            data = {'donatesList': saveDonatesList, 'commentsList': saveCommentsList, 'name':saveName,'type':saveType,'passCont':password,'longitude':lat,'latitude':long,'address':'406.Sok Birlik Mah.','weight':weight, 'status':'0', 'ip':IP,'city':city,'region':region,'country':country, 'passCont':'Zoologicalfooding2020', 'estimation':estimationLast}
            r3 = requests.put(url = URL3, data=json.dumps(data),headers=headers)
            
                        
            estimationLabel = tkinter.Label(mainWindow, text="Approximate exhaustion time: " + estimationLast, height=2, width=50, bg = "navajowhite2")
            
            estimationLabel.configure(font=("Comic Sans MS", 17))
            estimationLabel.pack()
            estimationLabel.place(relx = 0.2, rely = 0.8, anchor = CENTER)
            afterFillingCounter = afterFillingCounter + 1
            infoLabel.config(text = "Weight put: " + str(weightPut))
                 
            
            
            
        if afterFillingCounter == 0:
            afterFillingCounter = afterFillingCounter + 1
            infoLabel = tkinter.Label(mainWindow, text="Weight put: " + str(weightPut), height=2, width=50, bg = "navajowhite2")
            infoLabel.configure(font=("Comic Sans MS", 17))
            infoLabel.pack()
            infoLabel.place(relx = 0.2, rely = 0.7, anchor = CENTER)
            
            
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
    bFillingWindow.title("Before Filling")
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
    aFillingWindow.title("After Filling")
    aFillingWindow.configure(bg = "papaya whip")
    
    x = tkinter.Button(aFillingWindow, text='Ready', command= lambda: aboutTheDestroy(aFillingWindow, "Approximate food exhaustion time will  be calculated after this window closes", "after"))
    x.place(relx = 0.5, rely = 0.1, anchor = CENTER)
    x.configure(bg = "lemon chiffon")
    
def exitProgram():
    global password
    count = 0
    global windowChecker
    while True:
        msgBox = takeInput('Admin password:', 'Admin confirmation', True)
        msgBox.waitForInput()
        answer = msgBox.getString()
        if windowChecker:
            windowChecker = False
            return
        
        if answer != password:
            if count == 2:
                tkinter.messagebox.showinfo("Error", "Too many unsuccessful attempts!")
                return
            tkinter.messagebox.showinfo("Error", "Wrong Password!")    
            count = count + 1
        else:
            URL = "http://restservices496.herokuapp.com/containers"
            id = 1
            PARAMS = {'container_id':id}
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()

     
            countt = 0

            while countt < len(data):
                if data[countt]['containerID'] == 761:
                    password = data[countt]['passCont']
                    break
                countt = countt + 1


            saveName = data[countt]['name']
            saveType = data[countt]['type']
            saveDonatesList = data[countt]['donatesList']
            saveCommentsList = data[countt]['commentsList']



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
            data = {'donatesList': saveDonatesList,'commentsList':saveCommentsList, 'name':saveName,'type':saveType,'longitude':lat,'latitude':long,'address':'406.Sok Birlik Mah.','weight':0, 'passCont': password,'status': '3', 'ip':IP,'city':city,'region':region,'country':country}
            r33 = requests.put(url = URL3, data=json.dumps(data),headers=headers)
            os._exit(0)
    
    

windowChecker = False
class takeInput(object):
    
    
    def closeWindow(self):
        global windowChecker
        
        windowChecker = True
        self.root.destroy()
    
    
    def __init__(self,requestMessage, windowName, isPassw):
        self.root = Tk()
        self.root.configure(bg = "papaya whip")
        self.root.protocol('WM_DELETE_WINDOW', self.closeWindow)  # root is your root window


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




mainWindow.mainloop()


            



