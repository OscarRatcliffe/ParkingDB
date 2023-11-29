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