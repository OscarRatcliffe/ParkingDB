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



def makeSaleGui(sg, mydatabase):

    names = []
    spaces = []

    customerQuery = mydatabase.viewCustomers()

    for i in customerQuery:
        names.append(i[2]+ " " + i[1])

    for i in mydatabase.viewSpaces():
        spaces.append(i[0])

    for i in mydatabase.viewTerms():
        termPrices = [i[1], i[2], i[3]] # Overwritting so that only latest version is used

    layout = [  [sg.Text("Space sold"), sg.Combo(spaces, expand_x=True)],
                [sg.Text("Customer ID"), sg.Combo(names, expand_x=True)],
                [sg.Text("Price paid"), sg.Combo(termPrices, expand_x=True)], 
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

                # --------------------
                # Find index of values
                # --------------------

                for i in customerQuery:
                    
                    comboreturnexpected = i[2]+ " " + i[1]

                    if values[1] == comboreturnexpected:
                        CustomerID = i[0]

                # ---------
                # Add to DB
                # ---------

                lastTerm = ""

                for i in mydatabase.viewTerms():
                    lastTerm = i[0]

                mydatabase.makeSale(lastTerm, values[0], int(CustomerID), int(values[2]))
                sg.popup("Sale made")

            except (sqlite3.IntegrityError):
                sg.popup("Skipping value - Already exists in DB")


def insertTermGUI(sg, mydatabase):

    layout = [  [sg.Text("TermID"), sg.InputText(expand_x=True)],
                [sg.Text("Staff Price"), sg.InputText(expand_x=True)],
                [sg.Text("Student Price"), sg.InputText(expand_x=True)],
                [sg.Text("Disabled Price"), sg.InputText(expand_x=True)],
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
                mydatabase.insertTerm(values[0], int(values[1]), int(values[2]), int(values[3]))
                sg.popup("Term added")

            except (sqlite3.IntegrityError):
                sg.popup("Skipping value - Already exists in DB")


def assignOwnerGUI(sg, mydatabase):

    carRegs = []
    names = []

    customerQuery = mydatabase.viewCustomers()

    for i in customerQuery:
        names.append(i[2]+ " " + i[1])

    for i in mydatabase.viewCarsall():
        carRegs.append(i[0])

    for i in mydatabase.viewOwners():
        lastOwnerID = i[0];

    layout = [  [sg.Text("Car reg"), sg.Combo(carRegs, expand_x=True)],
                [sg.Text("Customer"), sg.Combo(names, expand_x=True)],
                [sg.Button('Submit')] 
            ]

    window = sg.Window('Parking DB', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == 'Submit':

            # --------------------
            # Find index of values
            # --------------------

            for i in customerQuery:
                
                comboreturnexpected = i[2]+ " " + i[1]

                if values[1] == comboreturnexpected:
                    CustomerID = i[0]

            # ---------
            # Add to DB
            # ---------

            try:
                mydatabase.newOwner(lastOwnerID + 1, values[0], int(CustomerID), 1)
                sg.popup("Owner Assigned")

            except (sqlite3.IntegrityError):
                sg.popup("Skipping value - Already exists in DB")

def updateCarDetailsGUI(sg, mydatabase): 

    carRegs = []
    carMakes = []
    carModels = []

    allCars = mydatabase.viewCarsall()

    for i in allCars:
        carRegs.append(i[0])
        carMakes.append(i[1])
        carModels.append(i[2])


    layout = [  [sg.Text("Car reg"), sg.Combo(carRegs, expand_x=True,key="CarRegs", enable_events=True)],
                [sg.Text("Car make"), sg.InputText(expand_x=True, key="CarMake")],
                [sg.Text("Car model"), sg.InputText(expand_x=True, key="CarModel")],
                [sg.Button('Update')] 
            ]

    window = sg.Window('Parking DB', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == 'CarRegs':
            carRegIndex = carRegs.index(values["CarRegs"])

            window["CarMake"].update(carMakes[carRegIndex])
            window["CarModel"].update(carModels[carRegIndex])

        if event == 'Update':
            mydatabase.UpdateCar(values["CarRegs"], values["CarMake"], values["CarModel"])
            sg.popup("Car updated")


def updateCustomerDetailsGUI(sg, mydatabase):  # TODO

    Name = []
    disability = []
    type = []
    current = []

    allCars = mydatabase.viewCustomers()

    for i in allCars:
        Name.append([i[1], i[2]])
        disability.append(i[3])
        type.append(i[4])
        current.append(i[5])


    layout = [  [sg.Text("Name"), sg.Combo(Name, expand_x=True,key="Name", enable_events=True)],
                [sg.Text("Type"), sg.Combo(["Student", "Staff"], expand_x=True, key="Type")],
                [sg.Checkbox("Disabled?", expand_x=True, key="Disability")], 
                [sg.Checkbox("Current?", expand_x=True, key="Current")], 
                [sg.Button('Update')] 
            ]

    window = sg.Window('Parking DB', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == 'Name':
            nameIndex = Name.index(values["Name"])

            window["Disability"].update(disability[nameIndex])
            window["Type"].update(type[nameIndex])
            window["Current"].update(current[nameIndex])

        if event == 'Update':
            mydatabase.UpdateCustomer(values["Name"][0], values["Name"][1], int(values["Disability"]), values["Type"], int(values["Current"]))
            sg.popup("Customer updated")