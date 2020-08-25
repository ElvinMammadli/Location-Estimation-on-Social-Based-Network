import tkinter
import webbrowser

import tkinter as tk  # python 3
from _csv import reader
from functools import partial
from tkinter import *
from tkinter import font  as tkfont  # python 3
import folium

import pandas as pd

# import Tkinter as tk     # python 2
# import tkFont as tkfont  # python 2
app = None


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):


        tk.Tk.__init__(self, *args, **kwargs)
        self.username = None
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def set_username(self, username):
        self.username = username

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        global app

        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.title("Semester Project")
        # username label and text entry box
        usernameLabel = Label(self, text="User Id").grid(row=4, column=4)
        username = StringVar()
        usernameEntry = Entry(self, textvariable=username).grid(row=4, column=5)

        # password label and password entry box
        passwordLabel = Label(self, text="CategoryId").grid(row=5, column=4)
        password = StringVar()
        passwordEntry = Entry(self, textvariable=password).grid(row=5, column=5)

        newYorkLabel = Label(self, text="We have 1083 userId and 251 category in NewYork data")
        newYorkLabel.config(font=("Courier", 10))
        newYorkLabel.place(x=0,y=150)

        tokyoLabel = Label(self, text="We have 2293 userId and 247 category in Tokyo data")
        tokyoLabel.place(x=0,y=170)
        tokyoLabel.config(font=("Courier", 10))


        var = IntVar()
        var1 = IntVar()

        def validateLogin(username,password):
            controller.show_frame("PageOne")
            username = username.get()
            app.frames["PageOne"].set_username(username)
            category=password.get()
            app.frames["PageOne"].set_category(category)
            if( (var.get()==1 and var1.get()==1 )):
                app.frames["PageOne"].NewYorkItem()
            elif(var.get() == 1 and var1.get()==2):
                app.frames["PageOne"].NewYorkUser()
            elif (var.get()==2 and var1.get() == 1):
                app.frames["PageOne"].TokyoItem()
            elif (var.get()==2 and var1.get() == 2):
                app.frames["PageOne"].TokyoUser()
            return

        def sel():
            selection = "You selected the option " + str(var.get())


        def sel1():
            selection = "You selected the option " + str(var1.get())


        R1 = Radiobutton(self, text="NewYork", variable=var, value=1, command=sel).grid(row=8, column=5)
        R2 = Radiobutton(self, text="Tokyo", variable=var, value=2, command=sel).grid(row=8, column=4)
        R12 = Radiobutton(self, text="ItemBased", variable=var1, value=1, command=sel1).grid(row=9, column=5)
        R22 = Radiobutton(self, text="UserBased", variable=var1, value=2, command=sel1).grid(row=9, column=4)

        validateLogin = partial(validateLogin, username,password)
        # login button
        loginButton = tk.Button(self, text="Start",
                                command=validateLogin)
        loginButton.place(x=300, y=100)


class PageOne(tk.Frame):


    def __init__(self, parent, controller):
        controller.title("Semester Project")


        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.geometry("500x300")
        self.username = StringVar()
        self.category = StringVar()



    def NewYorkItem(self):

        def openMap():

            new=2
            url="newyorkItem.html"
            webbrowser.open(url,new=new)

        # loop through csv list
        tokyo = []

        with open('venv/include/predictionNewyorkItem.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                tokyo.append(row)
        for j in tokyo:
            user=int(self.username.get())-1
            searchedUser=str(user)
            if ( searchedUser== j[0] and self.category.get()==j[1] ):
                userId="Searched user Id: "+self.username.get()
                categoryId="Searched category Id: "+j[1]
                prediction="Your prediction value :"+str(round(float(j[3]),3))

                latitude=0.0
                longitude=0.0
                with open('venv/include/NewYorkCategory.csv', 'r') as read_obj:
                    predictionCsv_reader = reader(read_obj)
                    for row in predictionCsv_reader:
                        if (self.category.get() == row[0]):
                            latitude="Your latitude: "+row[2]
                            longitude="Your longitude: "+row[3]


                if j[2]=="0":
                    target="You haven't got any target"
                else:
                    target="Your target:"+str(j[2])

                usernameLabel = Label(self, text=userId)
                usernameLabel.place(x=150,y=10)

                categoryIdLabel =Label(self, text=categoryId)
                categoryIdLabel.place(x=150,y=40)

                targetLabel=Label(self, text=target)
                targetLabel.place(x=150,y=70)

                predictionLabel=Label(self,text=prediction)
                predictionLabel.place(x=150,y=100)

                latitudeLabel = Label(self, text=latitude)
                latitudeLabel.place(x=150, y=130)

                longitudeLabel = Label(self, text=longitude)
                longitudeLabel.place(x=150, y=150)

                correct= (1-0.021562)*100
                correctness=(str(round(correct))+"% correctness")
                correctLabel=Label(self,text=correctness)
                correctLabel.place(x=150,y=190)
                correctLabel.config(font=("Courier", 15))
                loginButton = tk.Button(self, text="Show Map",command=openMap)
                loginButton.place(x=150, y=230)

                def showmapItemNewyork(self):

                    predictions = []


                    with open('venv/include/predictionNewyorkItem.csv', 'r') as read_obj:
                        csv_reader = reader(read_obj)
                        for row in csv_reader:
                            predictions.append(row)

                    map_newyork = folium.Map(location=[40.71981038, -74.00258103, ], zoom_start=11)
                    max=-5.0
                    max2=-5.0
                    max3=-5.0
                    for j in predictions:
                        if (searchedUser == j[0] ):
                            if (float(j[3]) > float(max)):
                                max3=max2
                                max2=max
                                max = j[3]
                            elif (float(j[3]) > float(max2)):
                                max3 = max2
                                max2 = j[3]
                            elif (float(j[3]) > float(max3)):
                                max3 = j[3]

                    for j in predictions:

                        if (searchedUser == j[0]):
                            if(j[3]==max or j[3]==max2 or j[3]==max3):
                                color='green'
                            elif(float(j[3])<0):
                                color='red'
                            else:
                                color='blue'

                            latitude=0
                            longitude=0
                            with open('venv/include/NewYorkCategory.csv', 'r') as read_obj:
                                predictionCsv_reader = reader(read_obj)
                                for row in predictionCsv_reader:
                                    if (j[1] == row[0]):
                                        latitude =  row[2]
                                        longitude =  row[3]


                                        folium.CircleMarker([latitude, longitude],popup=str("Location name:"+row[1])+"\nprediction:"+str(round(float(j[3]),3)),radius=5,color=color,fill = True).add_to(map_newyork)
                                        break
                    map_newyork.save('newyorkItem.html')

                showmapItemNewyork(self)



    def NewYorkUser(self):

        def openMap():

            new=2
            url="newyorkUser.html"
            webbrowser.open(url,new=new)

        # loop through csv list
        tokyo = []

        with open('venv/include/predictionNewyorkUser.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                tokyo.append(row)
        for j in tokyo:
            user=int(self.username.get())-1
            searchedUser=str(user)
            if ( searchedUser== j[0] and self.category.get()==j[1] ):
                userId="Searched user Id: "+self.username.get()
                categoryId="Searched category Id: "+j[1]
                prediction="Your prediction value :"+str(round(float(j[3]),3))

                latitude=0.0
                longitude=0.0
                with open('venv/include/NewYorkCategory.csv', 'r') as read_obj:
                    predictionCsv_reader = reader(read_obj)
                    for row in predictionCsv_reader:
                        if (self.category.get() == row[0]):
                            latitude="Your latitude: "+row[2]
                            longitude="Your longitude: "+row[3]


                if j[2]=="0":
                    target="You haven't got any target"
                else:
                    target="Your target:"+str(j[2])

                usernameLabel = Label(self, text=userId)
                usernameLabel.place(x=150,y=10)

                categoryIdLabel =Label(self, text=categoryId)
                categoryIdLabel.place(x=150,y=40)

                targetLabel=Label(self, text=target)
                targetLabel.place(x=150,y=70)

                predictionLabel=Label(self,text=prediction)
                predictionLabel.place(x=150,y=100)

                latitudeLabel = Label(self, text=latitude)
                latitudeLabel.place(x=150, y=130)

                longitudeLabel = Label(self, text=longitude)
                longitudeLabel.place(x=150, y=150)

                correct= (1-0.021562)*100
                correctness=(str(round(correct))+"% correctness")
                correctLabel=Label(self,text=correctness)
                correctLabel.place(x=150,y=190)
                correctLabel.config(font=("Courier", 15))
                loginButton = tk.Button(self, text="Show Map",command=openMap)
                loginButton.place(x=150, y=230)

                def showmapItemNewyork(self):

                    predictions = []


                    with open('venv/include/predictionNewyorkUser.csv', 'r') as read_obj:
                        csv_reader = reader(read_obj)
                        for row in csv_reader:
                            predictions.append(row)

                    map_newyork = folium.Map(location=[40.71981038, -74.00258103, ], zoom_start=11)
                    max=-5.0
                    max2=-5.0
                    max3=-5.0
                    for j in predictions:
                        if (searchedUser == j[0] ):
                            if (float(j[3]) > float(max)):
                                max3=max2
                                max2=max
                                max = j[3]
                            elif (float(j[3]) > float(max2)):
                                max3 = max2
                                max2 = j[3]
                            elif (float(j[3]) > float(max3)):
                                max3 = j[3]

                    for j in predictions:

                        if (searchedUser == j[0]):
                            if(j[3]==max or j[3]==max2 or j[3]==max3):
                                color='green'

                            elif(float(j[3])<0):
                                color='red'
                            else:
                                color='blue'

                            latitude=0
                            longitude=0
                            with open('venv/include/NewYorkCategory.csv', 'r') as read_obj:
                                predictionCsv_reader = reader(read_obj)
                                for row in predictionCsv_reader:
                                    if (j[1] == row[0]):
                                        latitude =  row[2]
                                        longitude =  row[3]


                                        folium.CircleMarker([latitude, longitude],popup=str("Location name:"+row[1])+"\nprediction:"+str(round(float(j[3]),3)),radius=5,color=color,fill = True).add_to(map_newyork)
                                        break
                    map_newyork.save('newyorkUser.html')


                showmapItemNewyork(self)



    def TokyoItem(self):

        def openMap():

            new=2
            url="tokyoItem.html"
            webbrowser.open(url,new=new)

        # loop through csv list
        tokyo = []

        with open('venv/include/predictionTokyoItem.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                tokyo.append(row)
        for j in tokyo:
            user=int(self.username.get())-1
            searchedUser=str(user)
            if ( searchedUser== j[0] and self.category.get()==j[1] ):
                userId="Searched user Id: "+self.username.get()
                categoryId="Searched category Id: "+j[1]
                prediction="Your prediction value :"+str(round(float(j[3]),3))

                latitude=0.0
                longitude=0.0
                with open('venv/include/TokyoCategory.csv', 'r') as read_obj:
                    predictionCsv_reader = reader(read_obj)
                    for row in predictionCsv_reader:
                        if (self.category.get() == row[0]):
                            latitude="Your latitude: "+row[2]
                            longitude="Your longitude: "+row[3]


                if j[2]=="0.0":
                    target="You haven't got any target"
                else:
                    target="Your target:"+str(j[2])

                usernameLabel = Label(self, text=userId)
                usernameLabel.place(x=150,y=10)

                categoryIdLabel =Label(self, text=categoryId)
                categoryIdLabel.place(x=150,y=40)

                targetLabel=Label(self, text=target)
                targetLabel.place(x=150,y=70)

                predictionLabel=Label(self,text=prediction)
                predictionLabel.place(x=150,y=100)

                latitudeLabel = Label(self, text=latitude)
                latitudeLabel.place(x=150, y=130)

                longitudeLabel = Label(self, text=longitude)
                longitudeLabel.place(x=150, y=150)

                correct= (1-0.021562)*100
                correctness=(str(round(correct))+"% correctness")
                correctLabel=Label(self,text=correctness)
                correctLabel.place(x=150,y=190)
                correctLabel.config(font=("Courier", 15))
                loginButton = tk.Button(self, text="Show Map",command=openMap)
                loginButton.place(x=150, y=230)

                def showmapItemNewyork(self):

                    predictions = []


                    with open('venv/include/predictionTokyoItem.csv', 'r') as read_obj:
                        csv_reader = reader(read_obj)
                        for row in csv_reader:
                            predictions.append(row)

                    map_newyork = folium.Map(location=[35.70154378,139.7433847, ], zoom_start=11)
                    max=-5.0
                    max2=-5.0
                    max3=-5.0
                    for j in predictions:
                        if (searchedUser == j[0] ):
                            if (float(j[3]) > float(max)):
                                max3=max2
                                max2=max
                                max = j[3]
                            elif (float(j[3]) > float(max2)):
                                max3 = max2
                                max2 = j[3]
                            elif (float(j[3]) > float(max3)):
                                max3 = j[3]

                    for j in predictions:

                        if (searchedUser == j[0]):
                            if(j[3]==max or j[3]==max2 or j[3]==max3):
                                color='green'

                            elif(float(j[3])<0):
                                color='red'
                            else:
                                color='blue'

                            latitude=0
                            longitude=0
                            with open('venv/include/TokyoCategory.csv', 'r') as read_obj:
                                predictionCsv_reader = reader(read_obj)
                                for row in predictionCsv_reader:
                                    if (j[1] == row[0]):
                                        latitude =  row[2]
                                        longitude =  row[3]


                                        folium.CircleMarker([latitude, longitude],popup=str("Location name:"+row[1])+"\nprediction:"+str(round(float(j[3]),3)),radius=5,color=color,fill = True).add_to(map_newyork)
                                        break
                    map_newyork.save('tokyoItem.html')


                showmapItemNewyork(self)



    def TokyoUser(self):

        def openMap():

            new=2
            url="tokyoUser.html"
            webbrowser.open(url,new=new)

        # loop through csv list
        tokyo = []

        with open('venv/include/predictionTokyoUser.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                tokyo.append(row)
        for j in tokyo:
            user=int(self.username.get())-1
            searchedUser=str(user)
            if ( searchedUser== j[0] and self.category.get()==j[1] ):
                userId="Searched user Id: "+self.username.get()
                categoryId="Searched category Id: "+j[1]
                prediction="Your prediction value :"+str(round(float(j[3]),3))

                latitude=0.0
                longitude=0.0
                with open('venv/include/TokyoCategory.csv', 'r') as read_obj:
                    predictionCsv_reader = reader(read_obj)
                    for row in predictionCsv_reader:
                        if (self.category.get() == row[0]):
                            latitude="Your latitude: "+row[2]
                            longitude="Your longitude: "+row[3]


                if j[2]=="0":
                    target="You haven't got any target"
                else:
                    target="Your target:"+str(j[2])

                usernameLabel = Label(self, text=userId)
                usernameLabel.place(x=150,y=10)

                categoryIdLabel =Label(self, text=categoryId)
                categoryIdLabel.place(x=150,y=40)

                targetLabel=Label(self, text=target)
                targetLabel.place(x=150,y=70)

                predictionLabel=Label(self,text=prediction)
                predictionLabel.place(x=150,y=100)

                latitudeLabel = Label(self, text=latitude)
                latitudeLabel.place(x=150, y=130)

                longitudeLabel = Label(self, text=longitude)
                longitudeLabel.place(x=150, y=150)

                correct= (1-0.021562)*100
                correctness=(str(round(correct))+"% correctness")
                correctLabel=Label(self,text=correctness)
                correctLabel.place(x=150,y=190)
                correctLabel.config(font=("Courier", 15))
                loginButton = tk.Button(self, text="Show Map",command=openMap)
                loginButton.place(x=150, y=230)

                def showmapItemNewyork(self):

                    predictions = []

                    with open('venv/include/predictionTokyoUser.csv', 'r') as read_obj:
                        csv_reader = reader(read_obj)
                        for row in csv_reader:
                            predictions.append(row)

                    map_newyork = folium.Map(location=[35.70154378,139.7433847, ], zoom_start=11)
                    max=-5.0
                    max2=-5.0
                    max3=-5.0
                    for j in predictions:
                        if (searchedUser == j[0] ):
                            if (float(j[3]) > float(max)):
                                max3=max2
                                max2=max
                                max = j[3]
                            elif (float(j[3]) > float(max2)):
                                max3 = max2
                                max2 = j[3]
                            elif (float(j[3]) > float(max3)):
                                max3 = j[3]

                    for j in predictions:

                        if (searchedUser == j[0]):
                            if(j[3]==max or j[3]==max2 or j[3]==max3):

                                color='green'

                            elif(float(j[3])<0):
                                color='red'
                            else:
                                color='blue'

                            latitude=0
                            longitude=0
                            with open('venv/include/TokyoCategory.csv', 'r') as read_obj:
                                predictionCsv_reader = reader(read_obj)
                                for row in predictionCsv_reader:
                                    if (j[1] == row[0]):
                                        latitude =  row[2]
                                        longitude =  row[3]


                                        folium.CircleMarker([latitude, longitude],popup=str("Location name:"+row[1])+"\nprediction:"+str(round(float(j[3]),3)),radius=5,color=color,fill = True).add_to(map_newyork)
                                        break
                    map_newyork.save('tokyoUser.html')


                showmapItemNewyork(self)




    def set_username(self,username):
        self.username.set(username)
    def set_category(self,category):
        self.category.set(category)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
