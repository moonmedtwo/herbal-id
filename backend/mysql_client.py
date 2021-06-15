import mysql.connector
import credential

def match_herb(classNo):
    cnx = mysql.connector.connect(user=credential.user, password=credential.password,
                                  host='localhost',
                                  database='herbDB')

    cursor = cnx.cursor()

    query = "SELECT * FROM `herbDB`.`herb`"
    query += "WHERE herb_No = %s"
    
    cursor.execute(query, (classNo,))

    __name = 0
    __intro = 0
    __desc = 0
    __attr = 0
    __function = 0
    __usage = 0
    __storage = 0
    for (idx, name, intro, desc, attr, function, usage, storage) in cursor:
        __name = name
        __intro = intro
        __desc = desc
        __attr = attr
        __function = function
        __usage = usage
        __storage = storage

    cursor.close()
    cnx.close()

    ret = {"name":__name,
            "intro":__intro,
            "desc":__desc,
            "attr":__attr,
            "function":__function,
            "usage":__usage,
            "storage":__storage}
    return ret
