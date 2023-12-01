import sqlite3

def insertCarGUI(sg, mydatabase):
    
    layout = [  [sg.Text("Reg Number"), sg.InputText(expand_x=True)],
            [sg.Text("Make"), sg.InputText(expand_x=True)],
            [sg.Text("Model"), sg.InputText(expand_x=True)],
            [sg.Button('Submit')] 
            ]


    window = sg.Window('Parking DB', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == 'Submit':
            try:
                mydatabase.insertCar(values[0], values[1], values[2])
                sg.popup("Car added")

            except (sqlite3.IntegrityError):
                sg.popup("Skipping value - Already exists in DB")




def insertCustomerGUI(sg, mydatabase):

    customerTypes = ["Student", "Staff"]

    layout = [  [sg.Text("Surname"), sg.InputText(expand_x=True)],
            [sg.Text("Forename"), sg.InputText(expand_x=True)],
            [sg.Text("Type"), sg.Combo(customerTypes, expand_x=True)],
            [sg.Checkbox("Is disabled?")],
            [sg.Button('Submit')] 
            ]


    window = sg.Window('Parking DB', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == 'Submit':
            try:
                mydatabase.insertCustomer(values[0], values[1], int(values[3]) ,values[2], 1)
                sg.popup("Customer added")
            
            except (sqlite3.IntegrityError):
                sg.popup("Skipping value - Already exists in DB")



def insertSpaceGUI(sg, mydatabase):

    layout = [  [sg.Text("SpaceID"), sg.InputText(expand_x=True)],
                [sg.Checkbox("Is disabled?")],
                [sg.Button('Submit')] 
            ]

    window = sg.Window('Parking DB', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == 'Submit':
            try:
                mydatabase.insertSpace(values[0], int(values[1]))
                sg.popup("Space added")

            except (sqlite3.IntegrityError):
                sg.popup("Skipping value - Already exists in DB")