import os
import time
import sqlite3
import hashlib
import xlsxwriter
import openpyxl
import re
import string


v_data_PERSON = {
    "PERID": 0,
    "NAME": "",
    "BIRTHDATE": "",
    "ADDRESS": "",
    "CITY": "",
    "PROVINCE": "",
    "COUNTRY": "",
    "POSTALCODE": "",
    "PHONE": "",
    "EMAIL": "",
    "MARRIED": "",
    "TYPE": 0,              #1 - PATIENT , 2 - DOCTOR,
    "SPECIALIZATION": "",
    "GENDER": 0 # 1-MASCULINE 2-FEMENINE
}

v_data_TRANSACTION = {
    "TRANSID": 0,
    "APT_DATE": "",
    "PRE_COMMENT": "",
    "POST_COMMENT": "",
    "PLACE": "",
    "PERID": "",
    "DOCID": "",
    "STATUS": 0,    #1 - PLANNED, 2 - EXECUTED , 3 - CANCELLED
    "TYPE": 0,      #1 - APPOINTMENTS , 1 - TREATMENTS
    "COST": 0,
    "PRICE": 0,
    "DESCRIPTION": "",
    "INITIAL_HOUR": "",
    "FINAL_HOUR": ""
}

v_database_name = "finaldatabase.db"
v_directory = "/Users/pablolopera/Dropbox/PERSONAL_PALL/PERSONAL2022/Conestoga2022/BIGDATAArchitecture/PROG8420-22W-Sec1-Programming for Big Data/Projects/FinalProject/"


def f_insert_data(p_table_name,p_connection, p_data_list_insert, p_data_dict_insert):

     v_sql = "insert into " + p_table_name + str(tuple(p_data_dict_insert.keys())) + " values " + str(tuple(p_data_dict_insert.values())) + ";"
     v_data_cursor = p_connection.cursor()
     v_data_cursor.execute(v_sql)
     p_connection.commit()

     return v_data_cursor.lastrowid

def main():
    v_data_PERSON['PERID'] = 20
    v_data_PERSON['NAME'] = "TEST2"
    v_data_PERSON['BIRTHDATE'] = "01/01/2021"
    v_data_PERSON['ADDRESS'] = ""
    v_data_PERSON['CITY'] = ""
    v_data_PERSON['PROVINCE'] = ""
    v_data_PERSON['COUNTRY'] = ""
    v_data_PERSON['POSTALCODE'] = ""
    v_data_PERSON['PHONE'] = ""
    v_data_PERSON['EMAIL'] = ""
    v_data_PERSON['MARRIED'] = ""
    v_data_PERSON['TYPE'] = 2
    v_data_PERSON['SPECIALIZATION'] = ""
    v_data_PERSON['GENDER'] = 1


    v_db_connection = sqlite3.connect(v_directory + v_database_name)
    v_data_list = ('', '', '', '')

    v_new_patient = f_insert_data('PERSONS',v_db_connection, v_data_list, v_data_PERSON)

    v_data_TRANSACTION['TRANSID'] = 20
    v_data_TRANSACTION['APT_DATE'] = "10/10/2022"
    v_data_TRANSACTION['PRE_COMMENT'] = "pre test"
    v_data_TRANSACTION['POST_COMMENT'] = "post comments"
    v_data_TRANSACTION['PLACE'] = "the place is..."
    v_data_TRANSACTION['PERID'] = 1
    v_data_TRANSACTION['DOCID'] = 1
    v_data_TRANSACTION['STATUS'] = 1
    v_data_TRANSACTION['COST'] = 0
    v_data_TRANSACTION['PRICE'] = 0
    v_data_TRANSACTION['TYPE'] = 1
    v_data_TRANSACTION['DESCRIPTION'] = "TREATMENT DESCRIPTION"
    v_data_TRANSACTION['MEDICINE'] = "MEDICINE DESCRIPTION"
    v_data_TRANSACTION['FREQUENCE'] = "FREQUENCE DESCRIPTION"
    v_data_TRANSACTION['INITIAL_HOUR'] = "12:30"
    v_data_TRANSACTION['FINAL_HOUR'] = "14:30"
    v_new_appointment = f_insert_data('TRANSACTIONS',v_db_connection, v_data_list, v_data_TRANSACTION)




    #principal_menu()


if __name__ == '__main__':
    main()

