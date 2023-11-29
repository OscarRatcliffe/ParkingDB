import PySimpleGUI as sg
import os.path
import importStarting
from dbClass import DB 
    
fileExists = os.path.isfile('parking.db')

mydatabase = DB()
mydatabase.openDb()

# --------------------
# Import starting data
# --------------------

print(fileExists)

importStarting.importStartingData(fileExists, mydatabase)

sg.theme('DarkAmber') 

# Window setup
layout = [  [sg.Text("Reg Number"), sg.InputText(expand_x=True)],
          [sg.Text("Make"), sg.InputText(expand_x=True)],
          [sg.Text("Model"), sg.InputText(expand_x=True)],
            [sg.Button('Submit'), sg.Button('exit')] ]


window = sg.Window('Parking DB', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'exit':
        break
    if event == 'Submit':
        mydatabase.insertCar(values[0], values[1], values[2])
        print("Car added")

mydatabase.closeDb()
window.close()