def createTables(self):

    self.cur.execute(
        """CREATE TABLE IF NOT EXISTS tbl_customers
(customer_id INTEGER PRIMARY KEY,
    surname TEXT NOT NULL,
    forename TEXT NOT NULL,
    disabled INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 0,
    type TEXT NOT NULL CHECK (type = "Staff" OR type = "Student"),
    current INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 1)
            """)
    self.conn.commit()
    
    self.cur.execute(
        """CREATE TABLE IF NOT EXISTS tbl_cars
(reg TEXT PRIMARY KEY,
make TEXT NOT NULL,
model TEXT NOT NULL)""")
    self.conn.commit()
    
    self.cur.execute(
        """CREATE TABLE IF NOT EXISTS tbl_terms
(term TEXT PRIMARY KEY,
staff_price REAL NOT NULL,
student_price REAL NOT NULL,
disabled_price REAL NOT NULL ON CONFLICT REPLACE DEFAULT 0)
""")
    self.conn.commit()
    
    self.cur.execute(
        """CREATE TABLE IF NOT EXISTS tbl_spaces
(space TEXT PRIMARY KEY,    
disabled INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 0)
""")        
    self.conn.commit()
    
    self.cur.execute(
        """CREATE TABLE IF NOT EXISTS tbl_sales
(sold_term TEXT NOT NULL,
sold_space TEXT NOT NULL,
customer_sold_id INTEGER NOT NULL,
price_paid REAL NOT NULL ON CONFLICT REPLACE DEFAULT 0,
PRIMARY KEY (sold_term, sold_space),
FOREIGN KEY (sold_term) REFERENCES tbl_terms(term),
FOREIGN KEY (sold_space) REFERENCES tbl_spaces(space),    
FOREIGN KEY (customer_sold_id) REFERENCES tbl_customers(customer_id)    
)
""")        
    self.conn.commit()       

    self.cur.execute(
        """CREATE TABLE IF NOT EXISTS tbl_owners
(car_owner INTEGER NOT NULL,
car_reg TEXT NOT NULL,
customer_sold_id INTEGER NOT NULL,
current_car INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 1,
PRIMARY KEY (car_owner, car_reg),
FOREIGN KEY (car_owner) REFERENCES tbl_customers(customer_id),
FOREIGN KEY (car_reg) REFERENCES tbl_cars(reg)    
)
""")        
    
import sqlite3

class DB:
    def __init__(self):

    # -------
    # Init db
    # -------

        self.conn = sqlite3.connect("../data/parking.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                    sqlite3.PARSE_COLNAMES)
        self.cur = self.conn.cursor()
        self.cur.execute("PRAGMA foreign_keys = ON")
        self.conn.commit()

    # -------------
    # Create tables
    # -------------

        createTables(self)

        self.conn.commit() 
        
        self.conn.close()

    # ------------
    # DB functions
    # ------------

    def openDb(self):
        self.conn = sqlite3.connect("../data/parking.db")
        self.cur = self.conn.cursor()

    def closeDb(self):
        self.conn.close()   
            
    def viewCustomers(self):
        self.cur.execute("SELECT * FROM tbl_customers")
        rows = self.cur.fetchall()
        return rows
    
    def viewSpaces(self):
        self.cur.execute("SELECT * FROM tbl_spaces")
        rows = self.cur.fetchall()
        return rows
    
    def viewTerms(self):
        self.cur.execute("SELECT * FROM tbl_terms")
        rows = self.cur.fetchall()
        return rows
    
    def viewOwners(self):
        self.cur.execute("SELECT * FROM tbl_owners")
        rows = self.cur.fetchall()
        return rows
    
    def insertCustomer(self, rqsurname  , rqforename, rqdisability, rqtype, rqcurrent):
        self.cur.execute("INSERT INTO tbl_customers (surname, forename, disabled, type, current) VALUES (?,?,?,?,?)",
                         (rqsurname  , rqforename, rqdisability, rqtype, rqcurrent))
        self.conn.commit()
    
    def insertSpace(self, rqspace, rqdisabled):
        self.cur.execute("INSERT INTO tbl_spaces (space, disabled) VALUES (?,?)",
                         (rqspace  , rqdisabled))
        self.conn.commit()

    def insertTerm(self, rqterm, rqstaff_price, rqstudent_price, rqdisabled_price):
        self.cur.execute("INSERT INTO tbl_terms (term, staff_price, student_price, disabled_price) VALUES (?,?,?,?)",
                         (rqterm, rqstaff_price, rqstudent_price, rqdisabled_price))
        self.conn.commit()
        
    def insertCar(self, rqreg, rqmake, rqmodel):
        self.cur.execute("INSERT INTO tbl_cars (reg, make, model) VALUES (?,?,?)",(rqreg, rqmake, rqmodel))
        self.conn.commit()

    def viewCarsall(self):
        self.cur.execute("SELECT * FROM tbl_cars")
        rows = self.cur.fetchall()
        return rows
    
    def viewCarsCurrent(self):
        self.cur.execute("SELECT * FROM tbl_owners WHERE current = 1")
        rows = self.cur.fetchall()
        return rows       
    
    def viewCarsNotcurrent(self):
        self.cur.execute("SELECT * FROM tbl_owners WHERE available = 0")
        rows = self.cur.fetchall()
        return rows
    
    def markNotcurrent(self, rqreg):
        self.cur.execute("UPDATE tbl_owners SET current = 0 WHERE reg = ? AND current = 1",(rqreg,))
        self.conn.commit()

    def markCurrent(self, rqreg):
        self.cur.execute("UPDATE tbl_owners SET current = 1 WHERE reg = ? AND current = 0",(rqreg,))
        self.conn.commit()

    def makeSale(self, rqsold_term, rqsold_space, rqcustomer_sold_id, rqprice_paid):
        self.cur.execute("INSERT INTO tbl_sales (sold_term, sold_space, customer_sold_id, price_paid) VALUES (?,?,?,?)",(rqsold_term, rqsold_space, rqcustomer_sold_id, rqprice_paid))
        self.conn.commit()

    def newOwner(self, rqowner, rqcar_reg, rqcustomer_sold_id, rqcurrent_car):
        self.cur.execute("INSERT INTO tbl_owners (car_owner, car_reg, customer_sold_id, current_car) VALUES (?,?,?,?)",(rqowner, rqcar_reg, rqcustomer_sold_id, rqcurrent_car))
        self.conn.commit()

import csv
import PySimpleGUI as sg

def importStartingData(fileExists, mydatabase):
    if fileExists == False:

        print("Adding starting data")

        f = open("data/spaces_updated.txt", "r")

        for i in f:
            mydatabase.insertSpace(str(i), 0)

        f.close()

        # --------------
        # Importing cars
        # --------------
        with open("data/terms.csv", newline="") as csvfile:

            reader = csv.reader(csvfile)
            for row in reader:
                mydatabase.insertTerm(row[0], row[1], row[2], row[3])
                currentTerm = row[0] # Assume lastest term is current
                staffPrice = row[1]
                studentPrice = row[2]
                disabledPrice = row[3]

        with open("data/starting_data.csv", newline="") as csvfile:

            knownCars = []
            knownCustomers = []
            knownSales = []
            customerID = 0
            ownerID = 0

            reader = csv.reader(csvfile)
            for row in reader:

                tempCustomerKey = row[1]+row[2]

                if tempCustomerKey in knownCustomers:
                    pass
                else:
                    if row[4] == "N":
                        mydatabase.insertCustomer(row[1], row[2], 0, row[3], 1)
                    else:
                        mydatabase.insertCustomer(row[1], row[2], 1, row[3], 1)
                
                    customerID += 1
                    
                    knownCustomers.append(tempCustomerKey) 

                if row[8] in knownCars:
                    pass
                else:  
                    mydatabase.insertCar(row[8], row[9], row[10])

                    mydatabase.newOwner(ownerID, row[8], customerID, 1)

                    ownerID += 1

                # Calc price paid
                if row[4] == "Y":
                    pricePaid = disabledPrice
                
                else: 

                    if row[3] == "Student":
                        pricePaid = studentPrice

                    else:
                        pricePaid = staffPrice

                tempSalesKey = currentTerm + row[7]

                if tempSalesKey in knownSales:
                    pass

                else:
                    mydatabase.makeSale(currentTerm, row[7], customerID, pricePaid)

                    knownSales.append(tempSalesKey)

                knownCars.append(row[8])

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

import PySimpleGUI as sg
import os.path
    
fileExists = os.path.isfile('../data/parking.db')

mydatabase = DB()
mydatabase.openDb()

# --------------------
# Import starting data
# --------------------

print(fileExists)

importStartingData(fileExists, mydatabase)

sg.theme('DarkAmber') 

# -----------
# Main window
# -----------

layout = [  [sg.Text("Please pick an option")],
            [sg.Button('Add car'), sg.Button('Add customer'), sg.Button('Add space'), sg.Button('Add term')],
            [sg.Button('Make sale'), sg.Button('Assign owner')],
            [sg.Button('exit')]
        ]


window = sg.Window('Parking DB', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'exit':
        break

    if event == 'Add car':
        insertCarGUI(sg, mydatabase)

    if event == 'Add customer':
        insertCustomerGUI(sg, mydatabase)

    if event == 'Add space':
        insertSpaceGUI(sg, mydatabase)

    if event == 'Add term':
        insertTermGUI(sg, mydatabase)

    if event == 'Make sale':
        makeSaleGui(sg, mydatabase)

    if event == 'Assign owner':
        assignOwnerGUI(sg, mydatabase)

mydatabase.closeDb()
window.close()