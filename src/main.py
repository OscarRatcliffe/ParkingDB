import PySimpleGUI as sg
import os.path
import importStarting
import GuiElements
from dbClass import DB 
    
fileExists = os.path.isfile('../data/parking.db')

mydatabase = DB()
mydatabase.openDb()

# --------------------
# Import starting data
# --------------------

print(fileExists)

importStarting.importStartingData(fileExists, mydatabase)

sg.theme('DarkAmber') 

# -----------
# Main window
# -----------

layout = [  [sg.Text("Please pick an option")],
            [sg.Button('Add car'), sg.Button('Add customer'), sg.Button('Add space'), sg.Button('Add term')],
            [sg.Button('Make sale')],
            [sg.Button('exit')]
        ]


window = sg.Window('Parking DB', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'exit':
        break

    if event == 'Add car':
        GuiElements.insertCarGUI(sg, mydatabase)

    if event == 'Add customer':
        GuiElements.insertCustomerGUI(sg, mydatabase)

    if event == 'Add space':
        GuiElements.insertSpaceGUI(sg, mydatabase)

    if event == 'Add term':
        GuiElements.insertTermGUI(sg, mydatabase)

    if event == 'Make sale':
        GuiElements.makeSaleGui(sg, mydatabase)

mydatabase.closeDb()
window.close()