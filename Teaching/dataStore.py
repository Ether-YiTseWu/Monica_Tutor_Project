import mysql.connector

def insertData(select, timestamp, email, token, program, variable):

    connection = mysql.connector.connect(database='VariableDB', user='admin', passwd='admin')

    # Add data
    if select == "tokenDataSet":
        sql = "INSERT INTO {} (TIMESTAMP, EMAIL, TOKEN) VALUES ({}, '{}', '{}');".format(select, timestamp, email, token)
    elif select == "programDataSet":
        sql = "INSERT INTO {} (TIMESTAMP, TOKEN, PROGRAM, VARIABLES) VALUES ({}, '{}', '{}');".format(select, timestamp, token, program, variable)
    cursor = connection.cursor()
    cursor.execute(sql)

    # Check
    connection.commit()

    return True

def getEmailList():
    result = []
    connection = mysql.connector.connect(database='VariableDB', user='admin', passwd='admin')

    # Add data
    sql = "SELECT EMAIL FROM tokenDataSet;"
    cursor = connection.cursor(buffered = True)
    cursor.execute(sql)

    # Check
    connection.commit()

    for i in list(cursor):
        result.append(str(i)[2:-3])

    return result

def getTokenList():
    result = []
    connection = mysql.connector.connect(database='VariableDB', user='admin', passwd='admin')

    # Add data
    sql = "SELECT TOKEN FROM tokenDataSet;"
    cursor = connection.cursor(buffered = True)
    cursor.execute(sql)

    # Check
    connection.commit()

    for i in list(cursor):
        result.append(str(i)[2:-3])

    return result