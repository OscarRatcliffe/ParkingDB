import sqlite3
from dbClass import *

conn = sqlite3.connect("../data/parking.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON")

testDB = DB()
testDB.openDb()

def test_view():
    realResult = testDB.viewCustomers()

    cur.execute("SELECT * FROM tbl_customers")
    expectedResult = cur.fetchall()

    assert realResult == expectedResult

def test_insert():
    testDB.insertSpace("TEST_DATA_SPACE_A", 0)
    testDB.insertSpace("TEST_DATA_SPACE_B", 1)

    allSpaces = testDB.viewSpaces()

    foundA = False
    foundB = False

    for i in allSpaces:
        if i[0] == "TEST_DATA_SPACE_A":
            foundA = True
        
        elif i[0] == "TEST_DATA_SPACE_B":
            foundB = True

    assert foundA and foundB

def test_Update():
    testDB.insertCar("TEST_DATA_REG", "TEST_DATA_MAKE_A", "TEST_DATA_MODEL_A")
    testDB.UpdateCar("TEST_DATA_REG", "TEST_DATA_MAKE_B", "TEST_DATA_MODEL_B")

    allCars = testDB.viewCarsall()

    updated = False

    for i in allCars:
        if i[0] == "TEST_DATA_REG" and i[1] == "TEST_DATA_MAKE_B" and i[2] == "TEST_DATA_MODEL_B":
            updated = True

    assert updated

    