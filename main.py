import os
import time
import hashlib
import xlsxwriter
import openpyxl
import re
import string
import datetime
from transactions_libs.transactionsDML import *

v_valid_entries_ppal = ["1", "2", "3", "4", "5"]
v_valid_entries_patient = ["1", "2", "3", "4"]
v_valid_entries_doctor = ["1", "2", "3", "4", "5"]
v_valid_entries_admin = ["1", "2", "3", "4"]
v_valid_entries_analytic = ["1", "2", "3", "4"]
v_valid_entries_married = ["1", "2"]
v_valid_entries_gender = ["1", "2"]
v_valid_field_patient_update = ["1", "2", "3", "4", "5","6","7", "8", "9", "10", "11"]
v_valid_field_doctor_update = ["1", "2", "3", "4", "5","6","7", "8", "9", "10", "11","12"]

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
    "GENDER": ""             # 1-MASCULINE 2-FEMENINE
}

v_data_TRANSACTION = {
    "TRANSID": 0,
    "APT_DATE": "",
    "PRE_COMMENT": "",
    "POST_COMMENT": "",
    "PLACE": "",
    "PERID": "",
    "DOCID": "",
    "STATUS": "",    #P - PLANNED, E - EXECUTED , C - CANCELLED
    "TYPE": "",      #A - APPOINTMENTS , T - TREATMENTS
    "COST": 0,
    "PRICE": 0,
    "DESCRIPTION": "",
    "INITIAL_HOUR": "",
    "FINAL_HOUR": ""
}

v_database_name = "finaldatabase.db"
#v_directory = "/Users/pablolopera/Dropbox/PERSONAL_PALL/PERSONAL2022/Conestoga2022/BIGDATAArchitecture/PROG8420-22W-Sec1-Programming for Big Data/Projects/FinalProject/"
v_directory = ""


def f_date_validation(p_date):
    v_format = "%d/%m/%Y"
    v_output = False
    try:
        datetime.datetime.strptime(p_date, v_format)
    except ValueError:
        v_output = True
    return v_output

def f_email_validation(p_email):
    v_output = True
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(regex, p_email):
        v_output = False

    return v_output


def f_value_gender(p_gender):
    if p_gender=="1":
        return 'Feminine'
    elif p_gender==2:
        return 'Masculine'


def f_value_married(p_married):
    if p_married == "1":
        return 'Yes'
    elif p_married == "2":
        return 'No'


#Update Person
def update_person():
    #print('...Modify Person...')

    v_PATID = input('Please write you identification: ')
    v_TABLEKEY = "PERID"
    if f_search_data('PERSONS',v_TABLEKEY,v_PATID,v_directory,v_database_name) > 0 :
        v_data_PERSON['PERID'] = v_PATID
        ch = input(
            'Please enter an option to Update : \n 1 - Name \n 2 - BirthDate \n 3 - Address \n 4 - City \n 5 - Province \n 6 - Country \n 7 - PostalCode \n 8 - Phone \n 9 - Email \n 10 - Married \n 11 - Gender \n')
        if ch not in v_valid_field_patient_update:
            print(
                '<ERROR> Please type : 1 - Name | 2 - Birthdate | 3 - Address | 4 - City | 5 - Province | 6 - Country | 7 - Postalcode | 8 - Phone | 9 - Email | 10 - Married | 11 - Gender <ERROR>')
            print(' ')
        else:
            v_C_MODIFY = ch
            v_C_NEWVALUE = input('Please write the New Value: ')
            f_update_person('PERSONS',v_TABLEKEY,v_PATID,v_C_MODIFY,v_C_NEWVALUE, v_directory,v_database_name)
            v_datarow = f_search_all_data('PERSONS',v_TABLEKEY,v_PATID,v_directory,v_database_name)
            for row in v_datarow:
                print("THI IS THE INFORMATION YOU HAVE : \n")
                print("Id: ", row[0])
                print("Name: ", row[1])
                print("Birthdate: ", row[2])
                print("Address: ", row[3])
                print("City: ", row[4])
                print("Province: ", row[5])
                print("Country: ", row[6])
                print("Postalcode: ", row[7])
                print("Phone: ", row[8])
                print("Email: ", row[9])
                print("Married: ", f_value_married(row[10]))
                #print("Type: ", f_value_married(row[11]))
                #print("Specialization: ", row[12])
                print("Gender: ", f_value_gender(row[13]))
                print("\n")
    else:
        print('<ERROR> This identification does not exist in the system <ERROR> ')
        print(' ')



#Create Person
def create_person(p_type):

    v_PATID = input('Please write you identification: ')
    if f_search_data('PERSONS','PERID',v_PATID,v_directory,v_database_name) > 0 :
        print('<ERROR> You already exists in the system <ERROR> ')
        print(' ')
    else:
        v_data_PERSON['PERID'] = v_PATID
        v_data_PERSON['NAME'] = input('Please write full name: ')
        v_data_PERSON['BIRTHDATE'] = input('Please write birthdate (DD/MM/YYYY) : ')
        if(f_date_validation(v_data_PERSON['BIRTHDATE'] )):
            print('<ERROR> Date Format Is incorrect, the correct is  DD/MM/YYYY <ERROR> ')
            print(' ')
        else:
            v_data_PERSON['ADDRESS'] = input('Please write home address: ')
            v_data_PERSON['CITY'] = input('Please write city where you live: ')
            v_data_PERSON['PROVINCE'] = input('Please write province where you live: ')
            v_data_PERSON['COUNTRY'] = input('Please write country where you live: ')
            v_data_PERSON['POSTALCODE'] = input('Please write your postal code: ')
            v_data_PERSON['PHONE'] = input('Please write your phone: ')
            v_data_PERSON['EMAIL'] = input('Please write your email address: ')
            if f_email_validation(v_data_PERSON['EMAIL']) :
                print('<ERROR> You wrote wrong email <ERROR> ')
            else:
                v_data_PERSON['MARRIED'] = input('Are your Married ? 1 - Yes / 2 - No : ')
                if v_data_PERSON['MARRIED']  not in v_valid_entries_married:
                    print(
                        '<ERROR> Please type : 1 - if your are Married | 2 - You are not Married <ERROR>')
                    print()
                else:
                    v_data_PERSON['GENDER'] = input('What is your Gender? 1 - Feminine / 2 - Masculine: ')
                    if v_data_PERSON['GENDER'] not in v_valid_entries_gender:
                        print(
                            '<ERROR> Please type : 1 - for Feminine | 2 - for Masculine <ERROR>')
                        print()
                    else:
                        if p_type == 2:
                            v_data_PERSON['SPECIALIZATION'] = input('What type of specialization do you have?  ')

                        v_data_PERSON['TYPE'] = p_type
                        v_new_patient = f_insert_data('PERSONS',v_data_PERSON,v_directory,v_database_name)
                        print('...Person Created No: '+str(v_new_patient))

def init_data_TRANSACTION():
    v_data_TRANSACTION['TRANSID'] = 0
    v_data_TRANSACTION['APT_DATE'] = ""
    v_data_TRANSACTION['PERID'] = 0
    v_data_TRANSACTION['PRE_COMMENT'] = ""
    v_data_TRANSACTION['POST_COMMENT'] = ""
    v_data_TRANSACTION['PLACE'] = ""
    v_data_TRANSACTION['DOCID'] = 0
    v_data_TRANSACTION['STATUS'] = ""
    v_data_TRANSACTION['COST'] = 0
    v_data_TRANSACTION['PRICE'] = 0
    v_data_TRANSACTION['TYPE'] = ""
    v_data_TRANSACTION['DESCRIPTION'] = ""
    v_data_TRANSACTION['MEDICINE'] = ""
    v_data_TRANSACTION['FREQUENCE'] = ""
    v_data_TRANSACTION['INITIAL_HOUR'] = ""
    v_data_TRANSACTION['FINAL_HOUR'] = ""


#Create Appointment
def create_appointment(p_whomadeid):
    print('...Creating New Appointment...')
    init_data_TRANSACTION()
    v_data_TRANSACTION['STATUS'] = "P"
    v_data_TRANSACTION['TYPE'] = "A"
    v_data_TRANSACTION['MEDICINE'] = ""
    v_data_TRANSACTION['FREQUENCE'] = ""
    v_data_TRANSACTION['PERID']  = input('Please write Patient identification: ')
    if f_search_data('PERSONS','PERID',v_data_TRANSACTION['PERID'] ,v_directory,v_database_name) > 0 :
        v_data_TRANSACTION['APT_DATE'] = input('Please write appoinment date (DD/MM/YYYY) : ')
        if (f_date_validation(v_data_TRANSACTION['APT_DATE'])):
            print('<ERROR> Date Format Is incorrect, the correct is  DD/MM/YYYY <ERROR> ')
            print(' ')
        else:
            if p_whomadeid==1:
                v_data_TRANSACTION['DOCID'] = input('Please write Doctor identification: ')
                if f_search_data('PERSONS', 'PERID', v_data_TRANSACTION['DOCID'], v_directory, v_database_name) > 0:
                    if v_data_TRANSACTION['PERID'] != v_data_TRANSACTION['DOCID']:
                        v_data_TRANSACTION['INITIAL_HOUR'] = input('Please write the initial appointment hour (HH:MM): ')
                        v_data_TRANSACTION['FINAL_HOUR'] = input('Please write the final appointment hour : ')
                        v_data_TRANSACTION['PLACE'] = input('Please write the place appointment  : ')
                        v_data_TRANSACTION['COST'] = input('Please write the appointment cost : ')
                        v_data_TRANSACTION['PRICE'] = input('Please write the appointment price : ')
                        v_data_TRANSACTION['PRE_COMMENT'] = input('Please write recommendations before appointment  : ')
                        v_data_TRANSACTION['POST_COMMENT'] = ""
                        v_data_TRANSACTION['DESCRIPTION'] = input('Please write the appointment description : ')
                    else:
                        print('<ERROR> The Doctor ID and Patient ID could not be the same <ERROR> ')
                else:
                    print('<ERROR> The Doctor ID Does NOT exists in the system<ERROR> ')
            elif p_whomadeid==2:
                    v_data_TRANSACTION['DESCRIPTION'] = input('Please write the appointment description : ')
            v_data_TRANSACTION['PLACE'] = input('Please write the place appointment  : ')
            v_data_TRANSACTION['TRANSID'] = f_search_max_id('TRANSACTIONS', 'TRANSID', v_directory, v_database_name) +1
            v_new_appointment = f_insert_data('TRANSACTIONS', v_data_TRANSACTION, v_directory, v_database_name)
            print('...Appointment Created No: ' + str(v_new_appointment))
    else:
        print('<ERROR> The Patient ID Does NOT exists in the system <ERROR> ')


#Create Treatment
def create_treatment(p_whomadeid):
    print('...Creating New Treatment...')
    init_data_TRANSACTION()
    v_data_TRANSACTION['STATUS'] = "P"
    v_data_TRANSACTION['TYPE'] = "T"
    v_data_TRANSACTION['PERID'] = input('Please write Patient identification: ')
    if f_search_data('PERSONS', 'PERID', v_data_TRANSACTION['PERID'], v_directory, v_database_name) > 0:
        v_data_TRANSACTION['APT_DATE'] = input('Please write initial date for treatment (DD/MM/YYYY) : ')
        if (f_date_validation(v_data_TRANSACTION['APT_DATE'])):
            print('<ERROR> Date Format Is incorrect, the correct is  DD/MM/YYYY <ERROR> ')
            print(' ')
        else:
            if p_whomadeid == 1:
                v_data_TRANSACTION['DOCID'] = input('Please write Doctor identification: ')
                if f_search_data('PERSONS', 'PERID', v_data_TRANSACTION['DOCID'], v_directory, v_database_name) > 0:
                    if v_data_TRANSACTION['PERID'] != v_data_TRANSACTION['DOCID']:
                        v_data_TRANSACTION['COST'] = input('Please write the appointment cost : ')
                        v_data_TRANSACTION['PRICE'] = input('Please write the appointment price : ')
                        v_data_TRANSACTION['MEDICINE'] = input('Please write the Medicine to apply  : ')
                        v_data_TRANSACTION['FREQUENCE'] = input('Please write the Frequency of the treatment to apply  : ')
                        v_data_TRANSACTION['PRE_COMMENT'] = input('Please write recommendations for the treatments  : ')
                    else:
                        print('<ERROR> The Doctor ID and Patient ID could not be the same <ERROR> ')
                else:
                    print('<ERROR> The Doctor ID Does NOT exists in the system<ERROR> ')
            v_data_TRANSACTION['PLACE'] = input('Please write the place for the treatment  : ')
            v_data_TRANSACTION['TRANSID'] = f_search_max_id('TRANSACTIONS', 'TRANSID', v_directory, v_database_name) + 1
            v_new_appointment = f_insert_data('TRANSACTIONS', v_data_TRANSACTION, v_directory, v_database_name)
            print('...Treatment Created No: ' + str(v_new_appointment))
    else:
        print('<ERROR> The Patient ID Does NOT exists in the system <ERROR> ')


#Menu patient
def patient_menu():
    v_loop = 'Y'
    while v_loop == 'Y':
        print('...................')
        print('...PATIENT MENU....')
        print('...................\n')
        ch = input('Please enter an option : \n 1 - Create Patient \n 2 - Update Patient \n 3 - Patient Appointment \n 4 - Previuos Menu \n')
        if ch not in v_valid_entries_patient:
            print('<ERROR> Please type : 1 - Create Patient | 2 - Update Patient | 3 - Appointment for a Patient |  4 - Previuos Menu  <ERROR>')
            print()
        elif ch == '1':
            print('====>>>>>>.....Create Patient...')
            create_person(1)
        elif ch == '2':
            print('====>>>>>>.....Update Patient...')
            update_person()
        elif ch == '3':
            print('====>>>>>>.....Patient Appointment...')
            create_appointment(2)
        elif ch == '4':
            v_loop = 'N'
            print()
            print('Chao Patient.')
            print()



#Menu doctor
def doctor_menu():
    v_loop = 'Y'
    while v_loop == 'Y':
        print('...................')
        print('...DOCTOR MENU.....')
        print('...................\n')
        ch = input('Please enter an option : \n 1 - Doctor Registration \n 2 - Create Patient \n 3 - Patient Appointment \n 4 - Treatments Assignment \n 5 - Previuos Menu \n')
        if ch not in v_valid_entries_doctor:
            print('<ERROR> Please type : 1 - Doctor Registration | 2 - Create Patient  | 3 - Appointment for a Patient  |  4 - Treatments for a Patient |  5 - Previuos Menu  <ERROR>')
            print()
        elif ch == '1':
            print('====>>>>>>.....Create Doctor...')
            create_person(2)
        elif ch == '2':
            print('====>>>>>>.....Create Patient...')
            create_person(1)
        elif ch == '3':
            print('====>>>>>>.....Patient Appointment...')
            create_appointment(1)
        elif ch == '4':
            print('====>>>>>>.....Patient Treatment...')
            create_treatment(1)
        elif ch == '5':
            v_loop = 'N'
            print()
            print('Chao Doctor.')
            print()

    # create treatment

#create exercise
def create_exercise():
    print('...Creating New Exercise...')
    x = 1

#create exercise
def create_users():
    print('...Creating New User...')
    x = 1



#Menu Admin
def admin_menu():
    v_loop = 'Y'
    while v_loop == 'Y':
        print('...................')
        print('...ADMIN MENU......')
        print('...................\n')
        ch = input(
            'Please enter an option : \n 1 - Doctor Registration \n 2 - Exercises \n 3 - Users \n 4 - Previuos Menu \n')
        if ch not in v_valid_entries_admin:
            print(
                '<ERROR> Please type : 1 - Doctor Registration | 2 - Exercises | 3 - Users | 4 - Previuos Menu   <ERROR>')
            print()
        elif ch == '1':
            print('====>>>>>>.....Create Doctor...')
            create_person(2)
        elif ch == '2':
            print('====>>>>>>.....Create  Exercise..')
            create_exercise()
        elif ch == '3':
            print('====>>>>>>.....Create Users...')
            create_users()
        elif ch == '4':
            v_loop = 'N'
            print()
            print('Chao Admin.')
            print()


#create Analysis1
def analysis1():
    print('...Analysis1...')
    x = 1

#create Analysis2
def analysis2():
    print('...Analysis2...')
    x = 1

#create Analysis3
def analysis3():
    print('...Analysis3...')
    x = 1


#Menu Analytics
def analytic_menu():
    v_loop = 'Y'
    while v_loop == 'Y':
        print('...................')
        print('...ANALYTIC MENU...')
        print('...................\n')
        ch = input(
            'Please enter an option : \n 1 - Analysis 1 \n 2 - Analysis 2 \n 3 - Analysis 3 \n 4 - Exit \n')
        if ch not in v_valid_entries_analytic:
            print(
                '<ERROR> Please type : 1 - Analysis 1 | 2 - Analysis 2 | 3 - Analysis 3 | 4 - Exit  <ERROR>')
            print()
        elif ch == '1':
            print('...Analysis 1..')
            analysis1()
        elif ch == '2':
            print('... Analysis 2..')
            analysis2()
        elif ch == '3':
            print('...Patient Appointment...')
            analysis3()
        elif ch == '4':
            v_loop = 'N'
            print()
            print('Chao Analysis.')
            print()

#General Menu
def general_menu():
    v_loop = 'Y'
    while v_loop == 'Y':
        print('...................')
        print('...MAIN MENU.......')
        print('...................\n')
        ch = input('Please enter an option : \n 1 - Patient \n 2 - Doctor \n 3 - Admin \n 4 - Analytics \n 5 - Exit \n')
        if ch not in v_valid_entries_ppal:
            print('<ERROR> Please type : 1 - Patient | 2 - Doctor | 3 - Admin | 4 - Analytics | 5 - Exit  <ERROR>')
            print()
        elif ch == '1':
            patient_menu()
        elif ch == '2':
            doctor_menu()
        elif ch == '3':
            admin_menu()
        elif ch == '4':
            analytic_menu()
        elif ch == '5':
            v_loop = 'N'
            print()
            print('Chao..')
            print()


if __name__ == '__main__':
    general_menu()

