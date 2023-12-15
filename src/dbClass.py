import sqlite3
import createTables

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

        createTables.createTables(self)

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

    def UpdateCar(self, rqreg, rqmake, rqmodel):
        self.cur.execute("UPDATE tbl_cars SET make = ?, model = ? WHERE reg = ?",(rqmake, rqmodel, rqreg))
        self.conn.commit()
    
    def UpdateCustomer(self, rqsurname, rqforename, rqdisability, rqtype, rqcurrent):
        self.cur.execute("UPDATE tbl_customers SET disabled = ?, type = ?, current = ? WHERE surname = ? AND forename = ?",(rqdisability, rqtype, rqcurrent, rqsurname, rqforename))
        self.conn.commit()
