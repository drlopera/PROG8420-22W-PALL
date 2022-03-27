import sqlite3


def f_field_name():
    return "NAME"
def f_field_birthdate():
    return "BIRTHDATE"
def f_field_address():
    return "ADDRESS"
def f_field_city():
    return "CITY"
def f_field_province():
    return "PROVINCE"
def f_field_country():
    return "COUNTRY"
def f_field_postalcode():
    return "POSTALCODE"
def f_field_phone():
    return "PHONE"
def f_field_email():
    return "EMAIL"
def f_field_married():
    return "MARRIED"
def f_field_gender():
    return "GENDER"
def default():
    return "Incorrect Field"

v_switcher = {
    1: f_field_name,
    2: f_field_birthdate,
    3: f_field_address,
    4: f_field_city,
    5: f_field_province,
    6: f_field_country,
    7: f_field_postalcode,
    8: f_field_phone,
    9: f_field_email,
    10: f_field_married,
    11: f_field_gender
    }

def f_switch(p_ColTable):
    return v_switcher.get(p_ColTable, default)()


# function to insert in the database one record
def f_insert_data(p_table_name,
                  p_data_dict_insert,
                  p_directory,
                  p_database_name):
    v_db_connection = sqlite3.connect(p_directory + p_database_name)
    v_sql = "insert into " + p_table_name + str(tuple(p_data_dict_insert.keys())) + " values " + str(
        tuple(p_data_dict_insert.values())) + ";"
    v_data_cursor = v_db_connection.cursor()
    v_data_cursor.execute(v_sql)
    v_db_connection.commit()

    return v_data_cursor.lastrowid



# function to search in the database one record
def f_search_data(p_table_name,
                  p_table_key,
                  p_data,
                  p_directory,
                  p_database_name):
    v_output = 0
    v_db_connection = sqlite3.connect(p_directory + p_database_name)
    v_sql1 = "select count(*) from "+ p_table_name + " where " + p_table_key + "= '" + p_data + "'" + ";"
    v_data_cursor = v_db_connection.cursor()
    v_data_cursor.execute(v_sql1)
    rows = v_data_cursor.fetchall()

    for row in rows:
        # print('The LOGIN is : ',row[1],' The number of ACCESS COUNT : ',row[3])
        v_output = row[0]

    return v_output


#function to select record in a database
def f_search_all_data(p_table_name,
                      p_table_key,
                      p_data,
                      p_directory,
                      p_database_name):
    v_output = -1
    v_db_connection = sqlite3.connect(p_directory + p_database_name)
    v_sql1 = "select * from "+ p_table_name + " where " + p_table_key + "= '" + p_data + "'" + ";"
    v_data_cursor = v_db_connection.cursor()
    v_data_cursor.execute(v_sql1)
    rows = v_data_cursor.fetchall()

    for row in rows:
        # print('The LOGIN is : ',row[1],' The number of ACCESS COUNT : ',row[3])
        v_output = row[3]

    return rows

#function to update record in a database.
def f_update_person(p_table_name,
                    p_table_key,
                    p_data,
                    p_condition,
                    p_newvalue,
                    p_directory,
                    p_database_name):
    v_output = -1
    v_db_connection = sqlite3.connect(p_directory + p_database_name)

    v_condition = f_switch(int(p_condition))
    v_sql1 = "update "+ p_table_name + " SET  " + v_condition + " = " + "'"  + p_newvalue +  "' where " + p_table_key + "='" + p_data  + "';"
    print(v_sql1)
    v_db_connection.execute(v_sql1)
    v_db_connection.commit()
    return v_output



# function to query max value of a ID in the database of a specific table
def f_search_max_id(p_table_name,
                    p_table_key,
                    p_directory,
                    p_database_name):
    v_output = 0
    v_db_connection = sqlite3.connect(p_directory + p_database_name)
    v_sql1 = "select max(" + p_table_key + ") from "+ p_table_name  + ";"
    v_data_cursor = v_db_connection.cursor()
    v_data_cursor.execute(v_sql1)
    rows = v_data_cursor.fetchall()
    for row in rows:
        v_output = row[0]

    if v_output is None:
       return 0
    else:
     return v_output