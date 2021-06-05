import mysql.connector
import credential

def match_herb(classNo):
    cnx = mysql.connector.connect(user=credential.user, password=credential.password,
                                  host='localhost',
                                  database='herbDB')

    cursor = cnx.cursor()

    query = "SELECT herb_No, herb_name, herb_desc FROM `herbDB`.`herb`"
    query += "WHERE herb_No = %s"
    
    cursor.execute(query, (classNo,))

    __name = 0
    __desc = 0
    for (idx, name, desc) in cursor:
        __name = name
        __desc = desc

    cursor.close()
    cnx.close()

    return __name,__desc
