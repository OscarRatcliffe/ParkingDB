import csv
import PySimpleGUI as sg

def importStartingData(fileExists, mydatabase):
    if fileExists == False: #Check if DB already exists

        print("Adding starting data")

        # -------------
        # Import spaces
        # -------------

        f = open("../data/spaces_updated.txt", "r")

        for i in f:
            mydatabase.insertSpace(str(i), 0)

        f.close()

        # ------------
        # Import terms
        # ------------

        with open("../data/terms.csv", newline="") as csvfile:

            reader = csv.reader(csvfile)
            for row in reader:
                mydatabase.insertTerm(row[0], row[1], row[2], row[3])
                currentTerm = row[0] # Assume lastest term is current
                staffPrice = row[1]
                studentPrice = row[2]
                disabledPrice = row[3]

        # ---------------
        # Import main CSV
        # ---------------

        with open("../data/starting_data.csv", newline="") as csvfile:

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
                    if row[4] == "N": #Check if disabled
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

                # ---------------
                # Calc price paid
                # ---------------

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

