import sqlite3
import csv
import PySimpleGUI as sg
import os.path

class DB:
    def __init__(self):

    # -------
    # Init db
    # -------

        self.conn = sqlite3.connect("parking.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                    sqlite3.PARSE_COLNAMES)
        self.cur = self.conn.cursor()
        self.cur.execute("PRAGMA foreign_keys = ON")
        self.conn.commit()

    # -------------
    # Create tables
    # -------------

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
        self.conn.commit() 
        
        self.conn.close()


    def openDb(self):
        self.conn = sqlite3.connect("parking.db")
        self.cur = self.conn.cursor()

    def closeDb(self):
        self.conn.close()   
            
    def viewCustomers(self):
        self.cur.execute("SELECT * FROM tbl_customers")
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
    
fileExists = os.path.isfile('parking.db')

mydatabase = DB()
mydatabase.openDb()

# -------------
# Import spaces
# -------------

print(fileExists)

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