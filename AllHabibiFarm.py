import os
import sys
import time

from flask import Flask, render_template, request, flash, url_for, jsonify, session, redirect
import pymysql
from datetime import datetime
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/UPLOADS/'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}  # {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'SECRETKEYXIAN'

# Lambda Function
current_milli_time = lambda: int(round(time.time() * 1000))


#################### DATABASE ####################################


class DatabaseByPyMySQL:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = ""
        db = "flask_all_habibi"

        self.conection = pymysql.connect(host=host, user=user, password=password, db=db,
                                         cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conection.cursor()

    '''def addSome(self):
      self.cursor.execute("INSERT INTO demo VALUES(" + str(32154) + "," + str(85746) + ");")
      self.conection.commit()
      print("DATA ADDED")

       def getSome(self):
          self.cursor.execute("SELECT * from demo;")
          data = self.cursor.fetchall()
          print(data)'''

    def isEmailExist(self, email):
        self.cursor.execute('SELECT * FROM user WHERE UserEmail = "{0}";'.format(email))
        data = self.cursor.fetchall()
        if len(data) > 0:
            print('EMAIL EXIST', flush=True)
            return True
        else:
            print('EMAIL DO NOT EXIST', flush=True)
            return False

    def getUserByEmail(self, email):

        sql_all = 'SELECT * FROM user WHERE UserEmail = "{0}"'.format(email)
        self.cursor.execute(sql_all)
        data = self.cursor.fetchall()

        if len(data)>0:
            return data[0], True
        else:
            return data, False

    def getAnimalLastID(self):
        sql_qry = 'SELECT * FROM animal ORDER BY AnimalID DESC LIMIT 1'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAnimalLastID : ', str(data), flush=True)

        if len(data)>0:
            print('getAnimalLastID : ', str(data[0]['AnimalID']), flush=True)
            return data[0]['AnimalID'], True
        else:
            return 0, False

    def getAnimalByTag(self, tag):
        sql_qry = 'SELECT * FROM animal WHERE AnimalTag = "{0}";'.format(tag)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAnimalByTag : ', str(data[0]), flush=True)

        if len(data) > 0:
            return data[0], True
        else:
            return data, False


    def updateCommonData(self, CAT, TYPE, STATUS='null'):

        sql_qry = 'SELECT * FROM commondata LIMIT 1'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('updateCommonData : ', str(data), flush=True)

        try:
            if len(data) > 0:

                if CAT == 'GOAT':
                    if TYPE == 'ADD':
                        sql = 'UPDATE commondata SET TotalGoat = {0} WHERE CdID = {1};'.format(data[0]['TotalGoat'] + 1,
                                                                                           data[0]['CdID'])
                    elif TYPE == 'MISS':
                        sql = 'UPDATE commondata SET TotalGoat = {0}, MissingGoat = {1} WHERE CdID = {2};'.format(
                            data[0]['TotalGoat'] - 1, data[0]['MissingGoat'] + 1, data[0]['CdID'])
                    elif TYPE == 'DIED':
                        sql = 'UPDATE commondata SET TotalGoat = {0}, DiedGoat = {1} WHERE CdID = {2};'.format(
                            data[0]['TotalGoat'] - 1, data[0]['DiedGoat'] + 1, data[0]['CdID'])
                    elif TYPE == 'SLAUGHTER':
                        sql = 'UPDATE commondata SET TotalGoat = {0}, SlaughterGoat = {1} WHERE CdID = {2};'.format(
                            data[0]['TotalGoat'] - 1, data[0]['SlaughterGoat'] + 1, data[0]['CdID'])
                    elif TYPE == 'DELETE':
                        if STATUS == 'ALIVE':
                            sql = 'UPDATE commondata SET TotalGoat = {0} WHERE CdID = {1};'.format(data[0]['TotalGoat'] - 1, data[0]['CdID'])
                        elif STATUS == 'SLAUGHTER':
                            sql = 'UPDATE commondata SET SlaughterGoat = {0} WHERE CdID = {1};'.format(data[0]['SlaughterGoat'] - 1, data[0]['CdID'])
                        elif STATUS == 'MISSING':
                            sql = 'UPDATE commondata SET MissingGoat = {0} WHERE CdID = {1};'.format(data[0]['MissingGoat'] - 1, data[0]['CdID'])
                        elif STATUS == 'DIED':
                            sql = 'UPDATE commondata SET DiedGoat = {0} WHERE CdID = {1};'.format(data[0]['DiedGoat'] - 1, data[0]['CdID'])

                elif CAT == 'SHEEP':
                    if TYPE == 'ADD':
                        sql = 'UPDATE commondata SET TotalSheep = {0} WHERE CdID = {1};'.format(data[0]['TotalSheep'] + 1,
                                                                                            data[0]['CdID'])
                    elif TYPE == 'MISS':
                        sql = 'UPDATE commondata SET TotalSheep = {0}, MissingSheep = {1} WHERE CdID = {2};'.format(
                            data[0]['TotalSheep'] - 1, data[0]['MissingSheep'] + 1, data[0]['CdID'])
                    elif TYPE == 'DIED':
                        sql = 'UPDATE commondata SET TotalSheep = {0}, DiedSheep = {1} WHERE CdID = {2};'.format(
                            data[0]['TotalSheep'] - 1, data[0]['DiedSheep'] + 1, data[0]['CdID'])
                    elif TYPE == 'SLAUGHTER':
                        sql = 'UPDATE commondata SET TotalSheep = {0}, SlaughterSheep = {1} WHERE CdID = {2};'.format(
                            data[0]['TotalSheep'] - 1, data[0]['SlaughterSheep'] + 1, data[0]['CdID'])

                    elif TYPE == 'DELETE':
                        if STATUS == 'ALIVE':
                            sql = 'UPDATE commondata SET TotalSheep = {0} WHERE CdID = {1};'.format(data[0]['TotalSheep'] - 1, data[0]['CdID'])
                        elif STATUS == 'SLAUGHTER':
                            sql = 'UPDATE commondata SET SlaughterSheep = {0} WHERE CdID = {1};'.format(data[0]['SlaughterSheep'] - 1, data[0]['CdID'])
                        elif STATUS == 'MISSING':
                            sql = 'UPDATE commondata SET MissingSheep = {0} WHERE CdID = {1};'.format(data[0]['MissingSheep'] - 1, data[0]['CdID'])
                        elif STATUS == 'DIED':
                            sql = 'UPDATE commondata SET DiedSheep = {0} WHERE CdID = {1};'.format(data[0]['DiedSheep'] - 1, data[0]['CdID'])

                elif CAT == 'CAMEL':
                    if TYPE == 'ADD':
                        sql = 'UPDATE commondata SET TotalCamel = {0} WHERE CdID = {1};'.format(data[0]['TotalCamel'] + 1,
                                                                                            data[0]['CdID'])
                    elif TYPE == 'MISS':
                        sql = 'UPDATE commondata SET TotalCamel = {0}, MissingCamel = {1} WHERE CdID = {2};'.format(
                            data[0]['TotalCamel'] - 1, data[0]['MissingCamel'] + 1, data[0]['CdID'])
                    elif TYPE == 'DIED':
                        sql = 'UPDATE commondata SET TotalCamel = {0}, DiedCamel = {1} WHERE CdID = {2};'.format(
                            data[0]['TotalCamel'] - 1, data[0]['DiedCamel'] + 1, data[0]['CdID'])
                    elif TYPE == 'SLAUGHTER':
                        sql = 'UPDATE commondata SET TotalCamel = {0}, SlaughterCamel = {1} WHERE CdID = {2};'.format(
                            data[0]['TotalCamel'] - 1, data[0]['SlaughterCamel'] + 1, data[0]['CdID'])

                    elif TYPE == 'DELETE':
                        if STATUS == 'ALIVE':
                            sql = 'UPDATE commondata SET TotalCamel = {0} WHERE CdID = {1};'.format(data[0]['TotalCamel'] - 1, data[0]['CdID'])
                        elif STATUS == 'SLAUGHTER':
                            sql = 'UPDATE commondata SET SlaughterCamel = {0} WHERE CdID = {1};'.format(data[0]['SlaughterCamel'] - 1, data[0]['CdID'])
                        elif STATUS == 'MISSING':
                            sql = 'UPDATE commondata SET MissingCamel = {0} WHERE CdID = {1};'.format(data[0]['MissingCamel'] - 1, data[0]['CdID'])
                        elif STATUS == 'DIED':
                            sql = 'UPDATE commondata SET DiedCamel = {0} WHERE CdID = {1};'.format(data[0]['DiedCamel'] - 1, data[0]['CdID'])

                elif CAT == 'HORSE':
                    if TYPE == 'ADD':
                        sql = 'UPDATE commondata SET TotalHorse = {0} WHERE CdID = {1};'.format(data[0]['TotalHorse'] + 1,
                                                                                            data[0]['CdID'])
                    elif TYPE == 'MISS':
                        sql = 'UPDATE commondata SET TotalHorse = {0}, MissingHorse = {1} WHERE CdID = {2};'.format(
                            data[0]['TotalHorse'] - 1, data[0]['MissingHorse'] + 1, data[0]['CdID'])
                    elif TYPE == 'DIED':
                        sql = 'UPDATE commondata SET TotalHorse = {0}, DiedHorse = {1} WHERE CdID = {2};'.format(
                            data[0]['TotalHorse'] - 1, data[0]['DiedHorse'] + 1, data[0]['CdID'])
                    elif TYPE == 'SLAUGHTER':
                        sql = 'UPDATE commondata SET TotalHorse = {0}, SlaughterHorse = {1} WHERE CdID = {2};'.format(
                            data[0]['TotalHorse'] - 1, data[0]['SlaughterHorse'] + 1, data[0]['CdID'])

                    elif TYPE == 'DELETE':
                        if STATUS == 'ALIVE':
                            sql = 'UPDATE commondata SET TotalHorse = {0} WHERE CdID = {1};'.format(data[0]['TotalHorse'] - 1, data[0]['CdID'])
                        elif STATUS == 'SLAUGHTER':
                            sql = 'UPDATE commondata SET SlaughterHorse = {0} WHERE CdID = {1};'.format(data[0]['SlaughterHorse'] - 1, data[0]['CdID'])
                        elif STATUS == 'MISSING':
                            sql = 'UPDATE commondata SET MissingHorse = {0} WHERE CdID = {1};'.format(data[0]['MissingHorse'] - 1, data[0]['CdID'])
                        elif STATUS == 'DIED':
                            sql = 'UPDATE commondata SET DiedHorse = {0} WHERE CdID = {1};'.format(data[0]['DiedHorse'] - 1, data[0]['CdID'])

                print(sql, flush=True)
                self.cursor.execute(sql)
                self.conection.commit()

                return True

            else:
                return False
        except:
            print('Error on updateCommonData update', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    #1
    def Login(self, Email, Pass):
        print(Email, Pass, flush=True)
        if self.isEmailExist(Email):
            user, sts = self.getUserByEmail(Email)
            if user['UserPass'] == Pass:
                return user['Type'], user['UserName'], True
            else:
                return 'NULL','NULL', False
        else:
            return 'NULL','NULL', False

    #2
    def getCommonData(self):
        sql_qry = 'SELECT * FROM commondata;'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getCommonData : ', str(data), flush=True)

        if len(data)>0:
            return data[0], True
        else:
            return data, False

    #3
    def getAllAnimals(self):
        sql_qry = 'SELECT * FROM animal;'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAllAnimals : ', str(data), flush=True)

        if len(data)>0:
            return data, True
        else:
            return data, False

    #4
    def getAllAnimalsRange(self, page, range):
        fromm = page * range;

        sql_all = 'SELECT * FROM animal ORDER BY AnimalID ASC LIMIT {0}, {1};'.format(fromm, range)
        self.cursor.execute(sql_all)
        data = self.cursor.fetchall()

        print('getAllAnimalsRange : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    #5
    def getAnimalByCategory(self, cat):

        sql_qry = 'SELECT * FROM animal WHERE AnimalCategory = "{0}";'.format(cat)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAnimalByCategory : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    #6
    def getAnimalByID(self, id):
        sql_qry = 'SELECT * FROM animal WHERE AnimalID = {0};'.format(id)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAnimalByID : ', str(data[0]), flush=True)

        if len(data) > 0:
            return data[0], True
        else:
            return data, False

    # #7
    def SearchAnimal(self,searchText):
        sql_qry = 'SELECT * FROM animal WHERE AnimalCategory LIKE "%{0}%" OR AnimalTAG LIKE "%{0}%" OR AnimalOwner LIKE "%{0}%" OR AnimalBreed LIKE "%{0}%";'.format(searchText)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('SearchAnimal : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    # #8
    def getAllSlaughterAnimal(self):

        sql_qry = 'SELECT * FROM animal WHERE AnimalStatus = "{0}";'.format('SLAUGHTER')
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAllSlaughterAnimal : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    # #9
    def getAllMissingAnimal(self):
        sql_qry = 'SELECT * FROM animal WHERE AnimalStatus = "{0}";'.format('MISSING')
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAllMissingAnimal : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    # #10
    def getVaccineHistory(self, AnimalTag):
        sql_qry = 'SELECT * FROM vaccinedetails WHERE AnimalTag = "{0}";'.format(AnimalTag)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getVaccineHistory : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    # 11
    def getAllOwner(self):
        sql_qry = 'SELECT * FROM owner;'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAllOwner : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    # #12
    def getAllEmployee(self):
        sql_qry = 'SELECT * FROM user WHERE Type = "{0}";'.format('EMPLOYEE')
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAllEmployee : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    # 13
    def addAnimal(self, AnimalCategory, AnimalBreed, AnimalSex, AnimalOwner, AnimalDOB, AnimalFather, AnimalMother, AnimalPictureName):

        try:
            last_id, sts = self.getAnimalLastID()
            print('last ID = ' + str(last_id), flush=True)
            animal_id = int(last_id) + 1
            animal_tag = AnimalCategory[0:2]+'-'+AnimalBreed[0:3]+'-'+str(animal_id)


            # current date and time
            now = datetime.now()

            addedDate = str(now.strftime("%d-%m-%Y"))

            # Adding
            sql1 = 'INSERT INTO animal(AnimalID, AnimalTag, AnimalCategory, AnimalBreed, AnimalSex, AnimalOwner, AnimalDOB, AnimalFather, AnimalMother, AnimalStatus, AddedDate, UpdatedDate, AnimalPictureName)' \
                   ' VALUES({0},"{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","ALIVE","{9}","{9}","{10}");'.format(animal_id, animal_tag, AnimalCategory, AnimalBreed, AnimalSex,
                                                                                                                    AnimalOwner, AnimalDOB, AnimalFather, AnimalMother, addedDate, AnimalPictureName)
            print(sql1, flush=True)
            self.cursor.execute(sql1)
            self.conection.commit()

            self.updateCommonData(AnimalCategory, 'ADD')

            return True

        except:
            print('Error on addAnimal()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    # #14
    def addDiedAnimal(self, AnimalTag, Date, Cause):

        try:

            animal, stsb  = self.getAnimalByTag(AnimalTag)
            print('AnimalCategory '+animal['AnimalCategory']+ ' status : '+animal['AnimalStatus'], flush=True)
            if animal['AnimalStatus'] != 'DIED':
                status = self.updateCommonData(animal['AnimalCategory'], 'DIED')

            if status:
                # current date and time
                now = datetime.now()
                dateNow = now.strftime("%d-%m-%Y")
                sts = 'DIED'
                # Adding Dish
                sql1 = 'UPDATE Animal SET AnimalStatus = "{0}",  AnimalStatusDate = "{1}", AnimalStatusCause = "{2}", UpdatedDate = "{3}" WHERE AnimalTag = "{4}";'.format(sts, Date, Cause, dateNow, AnimalTag)
                self.cursor.execute(sql1)
                self.conection.commit()

                print(sql1, flush=True)

                return True
            else:
                return False

        except:
            print('Error on addDiedAnimal()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    # #15
    def addMissinAnimal(self, AnimalTag, Date):

        try:
            animal, stsb = self.getAnimalByTag(AnimalTag)
            print('AnimalCategory ' + animal['AnimalCategory'] + ' status : ' + animal['AnimalStatus'], flush=True)
            if animal['AnimalStatus'] != 'MISSING':
                status = self.updateCommonData(animal['AnimalCategory'], 'MISS')

            if status:
                # current date and time
                now = datetime.now()
                dateNow = now.strftime("%d-%m-%Y")
                sts = 'MISSING'
                cause = 'NULL'
                # Adding Dish
                sql1 = 'UPDATE Animal SET AnimalStatus = "{0}",  AnimalStatusDate = "{1}", AnimalStatusCause = "{2}", UpdatedDate = "{3}" WHERE AnimalTag = "{4}";'.format(
                    sts, Date, cause, dateNow, AnimalTag)
                self.cursor.execute(sql1)
                self.conection.commit()

                print(sql1, flush=True)
                return True
            else:
                return False

        except:
            print('Error on addMissinAnimal()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    # #16
    def addSlaughterAnimal(self, AnimalTag, Date):

        try:
            animal, stsb = self.getAnimalByTag(AnimalTag)
            print('AnimalCategory '+animal['AnimalCategory']+ ' status : '+animal['AnimalStatus'], flush=True)
            if animal['AnimalStatus'] != 'SLAUGHTER':
                status = self.updateCommonData(animal['AnimalCategory'], 'SLAUGHTER')

            if status:

                # current date and time
                now = datetime.now()
                dateNow = now.strftime("%d-%m-%Y")
                sts = 'SLAUGHTER'
                cause = 'NULL'
                # Adding Dish
                sql1 = 'UPDATE Animal SET AnimalStatus = "{0}",  AnimalStatusDate = "{1}", AnimalStatusCause = "{2}", UpdatedDate = "{3}" WHERE AnimalTag = "{4}";'.format(
                    sts, Date, cause, dateNow, AnimalTag)
                self.cursor.execute(sql1)
                self.conection.commit()

                print(sql1, flush=True)
                return True
            else:
                return False

        except:
            print('Error on addSlaughterAnimal()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    # #17
    def addVaccineDetails(self, AnimalTag, Date, details):

        try:

            # Adding addVaccineDetails
            sql1 = 'INSERT INTO vaccinedetails(AnimalTag, VDetails, VDate) VALUES("{0}", "{1}", "{2}");'.format(AnimalTag, details, Date)
            self.cursor.execute(sql1)
            self.conection.commit()

            print(sql1, flush=True)

            return True

        except:
            print('Error on addVaccineDetails()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    # #18
    def addEmployee(self, UserName, UserEmail, UserPhone, UserAddress, UserPass):

        try:
            # current date and time
            now = datetime.now()

            addedDate = now.strftime("%d-%m-%Y")
            updatedDate = addedDate
            # Adding Employee
            sql1 = 'INSERT INTO user(UserName, UserPhone, UserEmail, UserPass, UserAddress, AddedDate, UpdateDate, Type) VALUES("{0}","{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "EMPLOYEE");'.format(
                UserName, UserPhone, UserEmail, UserPass, UserAddress, addedDate, updatedDate)
            self.cursor.execute(sql1)
            self.conection.commit()

            print(sql1, flush=True)

            return True

        except:
            print('Error on addEmployee()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    # #19
    def addOwner(self, OwnerName):

        try:
            # Adding Employee
            sql1 = 'INSERT INTO owner(OwnerName) VALUES("{0}");'.format(OwnerName)
            self.cursor.execute(sql1)
            self.conection.commit()

            print(sql1, flush=True)

            return True

        except:
            print('Error on addOwner()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    # #20
    def updateAnimal(self, AnimalID, AnimalSex, AnimalOwner, AnimalDOB, AnimalFather, AnimalMother, AnimalPictureBlob):

        try:
            # current date and time
            now = datetime.now()
            dateNow = now.strftime("%d-%m-%Y")

            # Update
            sql1 = 'UPDATE Animal SET AnimalSex = "{0}",  AnimalOwner = "{1}", AnimalDOB = "{2}", AnimalFather = "{3}", AnimalMother = "{4}", ' \
                   ' UpdatedDate = "{5}" WHERE AnimalID = {6};'.format(
                                                                        AnimalSex, AnimalOwner, AnimalDOB, AnimalFather,AnimalMother, dateNow, AnimalID)
            self.cursor.execute(sql1)
            self.conection.commit()

            print(sql1, flush=True)

            sql2 = 'UPDATE AnimalPicture SET AnimalPictureBlob = "{0}" WHERE AnimalID = {1};'.format(AnimalPictureBlob, AnimalID)
            self.cursor.execute(sql2)
            self.conection.commit()

            print(sql2, flush=True)

            return True

        except:
            print('Error on updateAnimal()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    # 21
    def getAnimalByCategoryAndGender(self, cat, sex):

        sql_qry = 'SELECT * FROM animal WHERE AnimalCategory = "{0}" AND AnimalSex = "{1}";'.format(cat, sex)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAnimalByCategoryAndGender : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    #23
    def getAnimalByCategoryAndSubCat(self, cat, sub):

        sql_qry = 'SELECT * FROM animal WHERE AnimalCategory = "{0}" AND AnimalBreed = "{1}";'.format(cat,sub)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAnimalByCategoryAndSubCat : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    # 24
    def deleteAnimalByID(self, id):

        anim, stss = self.getAnimalByID(id)
        print(anim['AnimalStatus'])
        sts = self.updateCommonData(anim['AnimalCategory'],'DELETE', str(anim['AnimalStatus']))

        if sts:
            try:

                sql1 = 'DELETE FROM animal WHERE AnimalID = {0};'.format(id)
                self.cursor.execute(sql1)
                self.conection.commit()

                print(sql1, flush=True)

                return True

            except:
                print('Error on deleteAnimalByID()', flush=True)
                print('Error = ', str(sys.exc_info()[0]), flush=True)
                return False
        else:
            return False

    # 25
    def deleteEmployeeByID(self, id):
        try:
            # Adding Employee
            sql1 = 'DELETE FROM user WHERE UserID = {0};'.format(id)
            self.cursor.execute(sql1)
            self.conection.commit()

            print(sql1, flush=True)

            return True

        except:
            print('Error on deleteEmployeeByID()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    # NEW CODES 17-03-2020

    def getSubCategory(self,cat):
        sql_qry = 'SELECT * FROM animalcategory WHERE AcCat = "{0}";'.format(cat)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getSubCategory : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False


#################### DATABASE END ####################################

#################### API ####################################

@app.route('/API/testReturn', methods=['POST'])
def testReturnData():
    return jsonify({"error": "OK OK OK "}), 200

@app.route('/API/testReceive/<id>', methods=['POST'])
def testReceive(id):
    posss = ''
    if request.method == 'POST':
        posss = request.args['FFF']

    contentJSON = request.json

    return jsonify({"ID": id, "JSON":contentJSON, "POST": posss}), 200


#1
@app.route('/API/Login', methods=['POST'])
def Login():

    contentJSON = request.json
    try:
        email = contentJSON["Email"]
        passs = contentJSON["Pass"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "type": "NULL"}), 400

    DB = DatabaseByPyMySQL()
    type, name, status = DB.Login(email, passs)

    if status:
        return jsonify({"status": 1, "type": type, 'name': name}), 200
    else:
        return jsonify({"status": 0, "type": type, 'name': name}), 200

# 2
@app.route('/API/CommonData', methods=['POST'])
def CommonData():

    DB = DatabaseByPyMySQL()
    data, status = DB.getCommonData()

    if status:
        return jsonify({"status": 1, "data": data}), 200
    else:
        return jsonify({"status": 0, "type": data}), 200

# 3
@app.route('/API/AllAnimals', methods=['POST'])
def AllAnimals():

    DB = DatabaseByPyMySQL()
    data, status = DB.getAllAnimals()

    if status:
        return jsonify({"status": 1, "data": data}), 200
    else:
        return jsonify({"status": 0, "type": data}), 200

# 4
@app.route('/API/AllAnimalsRange', methods=['POST'])
def AllAnimalsRange():

    contentJSON = request.json

    try:
        page = contentJSON["page"]
        range = contentJSON["total"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400


    DB = DatabaseByPyMySQL()
    data, status = DB.getAllAnimalsRange(page, range)

    if status:
        return jsonify({"status": 1, "data": data}), 200
    else:
        return jsonify({"status": 0, "data": data}), 200

# 5
@app.route('/API/AnimalsByCategory', methods=['POST'])
def AnimalsByCategory():

    contentJSON = request.json

    try:
        cat = contentJSON["category"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400



    DB = DatabaseByPyMySQL()
    data, status = DB.getAnimalByCategory(cat)

    if status:
        return jsonify({"status": 1, "data": data}), 200
    else:
        return jsonify({"status": 0, "data": data}), 200

# 6
@app.route('/API/AnimalByID', methods=['POST'])
def AnimalByID():
    contentJSON = request.json
    try:
        ID = contentJSON["ID"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400

    DB = DatabaseByPyMySQL()
    data, status = DB.getAnimalByID(ID)

    if status:
        return jsonify({"status": 1, "data": data}), 200
    else:
        return jsonify({"status": 0, "data": data}), 200
# 7
@app.route('/API/SearchAnimal', methods=['POST'])
def SearchAnimal():
    contentJSON = request.json
    try:
        search = contentJSON["SearchString"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400

    DB = DatabaseByPyMySQL()
    data, status = DB.SearchAnimal(search)

    if status:
        return jsonify({"status": 1, "data": data}), 200
    else:
        return jsonify({"status": 0, "data": data}), 200
# 8
@app.route('/API/AllSlaughterAnimals', methods=['POST'])
def AllSlaughterAnimals():

    DB = DatabaseByPyMySQL()
    data, status = DB.getAllSlaughterAnimal()

    if status:
        return jsonify({"status": 1, "data": data}), 200
    else:
        return jsonify({"status": 0, "type": data}), 200

# 9
@app.route('/API/AllMissingAnimals', methods=['POST'])
def AllMissingAnimals():

    DB = DatabaseByPyMySQL()
    data, status = DB.getAllSlaughterAnimal()

    if status:
        return jsonify({"status": 1, "data": data}), 200
    else:
        return jsonify({"status": 0, "type": data}), 200

# 10
@app.route('/API/VaccineHistory', methods=['POST'])
def VaccineHistory():
    contentJSON = request.json
    try:
        AnimalTag = contentJSON["AnimalTag"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400

    DB = DatabaseByPyMySQL()
    data, status = DB.getVaccineHistory(AnimalTag)

    if status:
        return jsonify({"status": 1, "data": data}), 200
    else:
        return jsonify({"status": 0, "data": data}), 200

# 11
@app.route('/API/AllOwner', methods=['POST'])
def AllOwner():

    DB = DatabaseByPyMySQL()
    data, status = DB.getAllOwner()

    if status:
        return jsonify({"status": 1, "data": data}), 200
    else:
        return jsonify({"status": 0, "type": data}), 200
# 12
@app.route('/API/AllEmployee', methods=['POST'])
def AllEmployee():

    DB = DatabaseByPyMySQL()
    data, status = DB.getAllEmployee()

    if status:
        return jsonify({"status": 1, "data": data}), 200
    else:
        return jsonify({"status": 0, "type": data}), 200
# 13
@app.route('/API/AddAnimal', methods=['POST'])
def AddAnimal():
    contentJSON = request.json
    try:
        AnimalCategory = contentJSON["AnimalCategory"]
        AnimalBreed = contentJSON["AnimalBreed"]
        AnimalSex = contentJSON["AnimalSex"]
        AnimalOwner = contentJSON["AnimalOwner"]
        AnimalDOB = contentJSON["AnimalDOB"]
        AnimalFather = contentJSON["AnimalFather"]
        AnimalMother = contentJSON["AnimalMother"]
        AnimalPictureName = contentJSON["AnimalPictureName"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0}), 400

    DB = DatabaseByPyMySQL()
    status = DB.addAnimal(AnimalCategory, AnimalBreed, AnimalSex, AnimalOwner, AnimalDOB, AnimalFather, AnimalMother, AnimalPictureName)

    if status:
        return jsonify({"status": 1}), 200
    else:
        return jsonify({"status": 0}), 200
# 14
@app.route('/API/DiedAnimal', methods=['POST'])
def AddDiedAnimal():
    contentJSON = request.json
    try:
        AnimalTag = contentJSON["AnimalTag"]
        Date = contentJSON["Date"]
        Cause = contentJSON["Cause"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400

    DB = DatabaseByPyMySQL()
    status = DB.addDiedAnimal(AnimalTag, Date, Cause)

    if status:
        return jsonify({"status": 1}), 200
    else:
        return jsonify({"status": 0}), 200
# 15
@app.route('/API/MissingAnimal', methods=['POST'])
def MissingAnimal():
    contentJSON = request.json
    try:
        AnimalTag = contentJSON["AnimalTag"]
        Date = contentJSON["Date"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400

    DB = DatabaseByPyMySQL()
    status = DB.addMissinAnimal(AnimalTag, Date)

    if status:
        return jsonify({"status": 1}), 200
    else:
        return jsonify({"status": 0}), 200
# 16
@app.route('/API/SlaughterAnimal', methods=['POST'])
def SlaughterAnimal():
    contentJSON = request.json
    try:
        AnimalTag = contentJSON["AnimalTag"]
        Date = contentJSON["Date"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400

    DB = DatabaseByPyMySQL()
    status = DB.addSlaughterAnimal(AnimalTag, Date)

    if status:
        return jsonify({"status": 1}), 200
    else:
        return jsonify({"status": 0}), 200

# 17
@app.route('/API/AddVaccineDetails', methods=['POST'])
def AddVaccineDetails():
    contentJSON = request.json
    try:
        AnimalTag = contentJSON["AnimalTag"]
        Date = contentJSON["Date"]
        Details = contentJSON["Details"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400

    DB = DatabaseByPyMySQL()
    status = DB.addVaccineDetails(AnimalTag, Date, Details)

    if status:
        return jsonify({"status": 1}), 200
    else:
        return jsonify({"status": 0}), 200

# 18
@app.route('/API/AddEmployee', methods=['POST'])
def AddEmployee():
    contentJSON = request.json
    try:
        UserName = contentJSON["UserName"]
        UserEmail = contentJSON["UserEmail"]
        UserPhone = contentJSON["UserPhone"]
        UserAddress = contentJSON["UserAddress"]
        UserPass = contentJSON["UserPass"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0}), 400

    DB = DatabaseByPyMySQL()
    status = DB.addEmployee(UserName, UserEmail, UserPhone, UserAddress, UserPass)

    if status:
        return jsonify({"status": 1}), 200
    else:
        return jsonify({"status": 0}), 200
# 19
@app.route('/API/AddOwner', methods=['POST'])
def AddOwner():
    contentJSON = request.json
    try:
        OwnerName = contentJSON["OwnerName"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400

    DB = DatabaseByPyMySQL()
    status = DB.addOwner(OwnerName)

    if status:
        return jsonify({"status": 1}), 200
    else:
        return jsonify({"status": 0}), 200
# 20
@app.route('/API/UpdateAnimal', methods=['POST'])
def UpdateAnimal():
    contentJSON = request.json
    try:
        AnimalID = contentJSON["AnimalID"]
        AnimalSex = contentJSON["AnimalSex"]
        AnimalOwner = contentJSON["AnimalOwner"]
        AnimalDOB = contentJSON["AnimalDOB"]
        AnimalFather = contentJSON["AnimalFather"]
        AnimalMother = contentJSON["AnimalMother"]
        AnimalPictureBlob = contentJSON["AnimalPictureBlob"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400

    DB = DatabaseByPyMySQL()
    status = DB.updateAnimal(AnimalID, AnimalSex, AnimalOwner, AnimalDOB, AnimalFather, AnimalMother, AnimalPictureBlob)

    if status:
        return jsonify({"status": 1}), 200
    else:
        return jsonify({"status": 0}), 200

# 21
@app.route('/API/AnimalsByCategoryAndGender', methods=['POST'])
def AnimalsByCategoryAndGender():

    contentJSON = request.json

    try:
        cat = contentJSON["category"]
        sex = contentJSON["gender"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400



    DB = DatabaseByPyMySQL()
    data, status = DB.getAnimalByCategoryAndGender(cat,sex)

    if status:
        return jsonify({"status": 1, "data": data}), 200
    else:
        return jsonify({"status": 0, "data": data}), 200


#23
@app.route('/API/AnimalsByCategoryAndSubCat', methods=['POST'])
def AnimalsByCategoryAndSubCat():

    contentJSON = request.json

    try:
        cat = contentJSON["category"]
        sub = contentJSON["sub"]

    except:
        print('Error AnimalsByCategoryAndSubCat = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400



    DB = DatabaseByPyMySQL()
    data, status = DB.getAnimalByCategoryAndSubCat(cat, sub)

    if status:
        return jsonify({"status": 1, "data": data}), 200
    else:
        return jsonify({"status": 0, "data": data}), 200

#24
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def uploadFile():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'AnimalPic' not in request.files:
            print('No file part', flush=True)
            return redirect(request.url)
        file = request.files['dishPic']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = str("FILE") + filename[-4:]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            '''db = DatabaseByPyMySQL()
            status = db.addDish(dishName=DishName, dishDes=DishDes, dishPrice=DishPrice, dishPic=filename,
                                isAvailable=isAvailable, menu_id=DishMenu)'''

@app.route('/API/uploadFileAnimalPicture', methods=['POST'])
def uploadFileAnimalPicture():
    contentJSON = request.json

    # check if the post request has the file part
    if 'AnimalPictureFile' not in request.files:
        print('No file part in the request',flush=True)
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['AnimalPictureFile']
    if file.filename == '':
        print('No file selected for uploading', flush=True)
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        fileName = str(current_milli_time()) + filename[-4:]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))

        print('File successfully uploaded',flush=True)
        resp = jsonify({'message': 'File successfully uploaded', 'fileName':fileName})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp



#################### API END ####################################

#################### WEBSITE ####################################


@app.route('/')
def admin():

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        db = DatabaseByPyMySQL()
        data = db.getCommonData()

        return render_template('admin.html', data=data[0])

    else:
        return redirect(url_for('login'))


@app.route('/Admin/Add/Animal', methods=['POST', 'GET'])
def admin_add_animal():

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        db = DatabaseByPyMySQL()
        owner, bool = db.getAllOwner()
        data = {
            'cat': {'GOAT', 'SHEEP', 'HORSE', 'CAMEL'},
            'owner': owner
        }
        if request.method == 'POST':
            print('POST', flush=True)

            # check if the post request has the file part
            if 'AnimalPic' not in request.files:
                print('No file part', flush=True)
                return render_template('admin_add_animal.html', msg='False', data=data)
            file = request.files['AnimalPic']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                print('No selected file', flush=True)
                return render_template('admin_add_animal.html', msg='False', data=data)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = str(current_milli_time()) + filename[-4:]
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                print(filename, flush=True)

                try:
                    father = request.form['AnimalFather']
                except:
                    father = 'NULL'
                    print('Error = ', str(sys.exc_info()[0]), flush=True)

                try:
                    mother = request.form['AnimalMother']
                except:
                    mother = 'NULL'
                    print('Error = ', str(sys.exc_info()[0]), flush=True)

                try:
                    category = request.form['AnimalCategory']
                    breed = request.form['AnimalBreed']
                    sex = request.form['AnimalSex']
                    owner = request.form['AnimalOwner']
                    dob = request.form['AnimalDOB']
                    dob = dob[8:10] + '-' + dob[5:7] + '-' + dob[0:4]  # 0123 4 56 7 89
                except:
                    return render_template('admin_add_animal.html', msg='False', data=data)
                    print('Error = ', str(sys.exc_info()[0]), flush=True)

                print('DOB : ' + str(dob), flush=True)

                db = DatabaseByPyMySQL()
                status = db.addAnimal(category, breed, sex, owner, dob, father, mother, filename)

                print(str(status), flush=True)
                return render_template('admin_add_animal.html', msg=str(status), data=data)

        return render_template('admin_add_animal.html', data=data)

    else:
        return redirect(url_for('login'))


@app.route('/Admin/Add/GetDetailsSelect', methods=['POST'])
def get_all_options():

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        cat = request.form.get('cat')

        db = DatabaseByPyMySQL()
        data, bool1 = db.getSubCategory(cat)
        animalMale, bool2 = db.getAnimalByCategoryAndGender(cat, 'Male')
        animalFemale, bool3 = db.getAnimalByCategoryAndGender(cat, 'Female')

        if not bool2:
            animalMale = []
        if not bool3:
            animalFemale = []

        allData = {
            'breed': data,
            'male': animalMale,
            'female': animalFemale
        }

        if bool:
            print('FOUND DATA =  ' + str(len(allData)), flush=True)
            return jsonify(allData)
        else:
            print('NOT FOUND ANY DATA!! ', flush=True)
            return jsonify("")

    else:
        return redirect(url_for('login'))


@app.route('/Admin/Add/Employee', methods=['POST', 'GET'])
def admin_add_employee():

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        if request.method == 'POST':
            try:
                EmployeeName = request.form['EmployeeName']
                EmployeePhoneNumber = request.form['EmployeePhoneNumber']
                EmployeeEmail = request.form['EmployeeEmail']
                EmployeeAddress = request.form['EmployeeAddress']
                EmployeePass = request.form['EmployeePass']
                # EmployeePass = hashlib.md5(EmployeePass.decode("utf").hexdigest())

                print(EmployeeName, EmployeePhoneNumber, EmployeeEmail, EmployeeAddress, EmployeePass)

            except:
                print('Error = ', str(sys.exc_info()[0]), flush=True)
                return render_template('admin_add_employee.html', msg='failed')

            db = DatabaseByPyMySQL()
            sts = db.isEmailExist(EmployeeEmail)

            if not sts:
                sts1 = db.addEmployee(EmployeeName, EmployeeEmail, EmployeePhoneNumber, EmployeeAddress, EmployeePass)
                if sts1:
                    return render_template('admin_add_employee.html', msg='success')
                else:
                    return render_template('admin_add_employee.html', msg='failed')
            else:
                return render_template('admin_add_employee.html', msg='user_exist')

        return render_template('admin_add_employee.html')

    else:
        return redirect(url_for('login'))


@app.route('/Admin/Add/Owner', methods=['POST', 'GET'])
def admin_add_owner():

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        if request.method == 'POST':
            try:
                OwnerName = request.form['OwnerName']

                db = DatabaseByPyMySQL()
                sts = db.addOwner(OwnerName)

                return render_template('admin_add_owner.html', msg=str(sts))

            except:
                return render_template('admin_add_owner.html', msg='False')
                print('Error = ', str(sys.exc_info()[0]), flush=True)

        return render_template('admin_add_owner.html')

    else:
        return redirect(url_for('login'))


@app.route('/Admin/Animals/Goat', methods=['GET'])
def goats():

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        db = DatabaseByPyMySQL()
        data, sts = db.getAnimalByCategory('GOAT')

        return render_template('animals_list.html', data=data, title='Goats')

    else:
        return redirect(url_for('login'))


@app.route('/Admin/Animals/Sheep', methods=['GET'])
def Sheeps():

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        db = DatabaseByPyMySQL()
        data, sts = db.getAnimalByCategory('SHEEP')

        return render_template('animals_list.html', data=data, title='Sheeps')

    else:
        return redirect(url_for('login'))


@app.route('/Admin/Animals/Camel', methods=[ 'GET'])
def Camels():

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        db = DatabaseByPyMySQL()
        data, sts = db.getAnimalByCategory('CAMEL')

        return render_template('animals_list.html', data=data, title='Camels')

    else:
        return redirect(url_for('login'))


@app.route('/Admin/Animals/Horse', methods=['GET'])
def Horses():

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        db = DatabaseByPyMySQL()
        data, sts = db.getAnimalByCategory('HORSE')

        return render_template('animals_list.html', data=data, title='Horses')

    else:
        return redirect(url_for('login'))


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%d-%m-%Y")
    d2 = datetime.strptime(d2, "%d-%m-%Y")
    print(d1,d2,flush=True)
    return abs((d2 - d1).days)

@app.route('/Admin/Animals/Details/<tag>', methods=['GET'])
def AnimalsDetails(tag):

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        db = DatabaseByPyMySQL()
        data, sts = db.getAnimalByTag(tag)
        print(data, flush=True)
        vaccine, sts2 = db.getVaccineHistory(data['AnimalTag'])
        ageDays = days_between(data['AnimalDOB'], datetime.today().strftime('%d-%m-%Y'))
        ageYears = str(round(ageDays / 365, 4))
        age = {
            'days': ageDays,
            'years': ageYears
        }

        return render_template('animals_details.html', animal=data, vac=vaccine, age=age)

    else:
        return redirect(url_for('login'))


@app.route('/Admin/More/Employee', methods=['GET'])
def all_employee():

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        db = DatabaseByPyMySQL()
        data, sts = db.getAllEmployee()

        return render_template('employee_list.html', data=data, title='Employee')

    else:
        return redirect(url_for('login'))


@app.route('/Admin/More/Owner', methods=['GET'])
def all_owner():

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        db = DatabaseByPyMySQL()
        data, sts = db.getAllOwner()

        return render_template('owner_list.html', data=data, title='Owner')

    else:
        return redirect(url_for('login'))


@app.route('/Admin/Animals/Delete/<id>')
def del_animal(id):

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        db = DatabaseByPyMySQL()
        stats = db.deleteAnimalByID(id)

        return redirect(url_for('admin'))

    else:
        return redirect(url_for('login'))


@app.route('/Admin/Delete/Emp/<id>')
def del_employee(id):

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        db = DatabaseByPyMySQL()
        stats = db.deleteEmployeeByID(id)

        return redirect(url_for('all_employee'))

    else:
        return redirect(url_for('login'))




@app.route('/Admin/Animals/Vaccine/<tag>', methods=['GET', 'POST'])
def animal_vaccine(tag):

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        if request.method == 'POST':
            try:
                VaccineDetails = request.form['VaccineDetails']
                VaccineDate = request.form['VaccineDate']
                VaccineDate = VaccineDate[8:10] + '-' + VaccineDate[5:7] + '-' + VaccineDate[0:4]  # 0123 4 56 7 89

                db = DatabaseByPyMySQL()
                sts = db.addVaccineDetails(tag,VaccineDate, VaccineDetails)


                return redirect(url_for('AnimalsDetails',tag=tag))

            except:
                return redirect(url_for('AnimalsDetails',tag=tag))
                print('Error on animal_vaccine = ', str(sys.exc_info()[0]), flush=True)


        return render_template('animal_vaccine.html', animalTag=tag)

    else:
        return redirect(url_for('login'))

@app.route('/Admin/Animals/Slaughter/<tag>', methods=['POST', 'GET'])
def animal_slaughter(tag):
    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        if request.method == 'POST':
            try:
                SlaughterDate = request.form['SlaughterDate']
                SlaughterDate = SlaughterDate[8:10] + '-' + SlaughterDate[5:7] + '-' + SlaughterDate[0:4]  # 0123 4 56 7 89

                db = DatabaseByPyMySQL()
                sts = db.addSlaughterAnimal(tag, SlaughterDate)

                return redirect(url_for('AnimalsDetails', tag=tag))

            except:
                return redirect(url_for('AnimalsDetails', tag=tag))
                print('Error on animal_slaughter = ', str(sys.exc_info()[0]), flush=True)


        return render_template('animal_slaughter.html', animalTag=tag)

    else:
        return redirect(url_for('login'))

@app.route('/Admin/Animals/Died/<tag>', methods=['GET', 'POST'])
def animal_died(tag):

    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        if request.method == 'POST':
            try:
                DiedDetails = request.form['DiedDetails']
                DiedDate = request.form['DiedDate']
                DiedDate = DiedDate[8:10] + '-' + DiedDate[5:7] + '-' + DiedDate[0:4]  # 0123 4 56 7 89

                db = DatabaseByPyMySQL()
                sts = db.addDiedAnimal(tag,DiedDate, DiedDetails)


                return redirect(url_for('AnimalsDetails',tag=tag))

            except:
                return redirect(url_for('AnimalsDetails',tag=tag))
                print('Error on animal_died = ', str(sys.exc_info()[0]), flush=True)


        return render_template('animal_died.html', animalTag=tag)

    else:
        return redirect(url_for('login'))

@app.route('/Admin/Animals/Missing/<tag>', methods=['POST', 'GET'])
def animal_missing(tag):
    if session.get('UserID') is not None and session.get('Type') == 'ADMIN':
        if request.method == 'POST':
            try:
                MissingDate = request.form['MissingDate']
                MissingDate = MissingDate[8:10] + '-' + MissingDate[5:7] + '-' + MissingDate[0:4]  # 0123 4 56 7 89

                db = DatabaseByPyMySQL()
                sts = db.addMissinAnimal(tag, MissingDate)

                return redirect(url_for('AnimalsDetails', tag=tag))

            except:
                return redirect(url_for('AnimalsDetails', tag=tag))
                print('Error on animal_slaughter = ', str(sys.exc_info()[0]), flush=True)


        return render_template('animal_missing.html', animalTag=tag)

    else:
        return redirect(url_for('login'))




@app.route('/test/<dob>')
def test(dob):
    dob = dob.split('-')
    print(dob[0], flush=True)
    print(dob[1], flush=True)
    print(dob[2], flush=True)
    dobbb = ''
    if int(dob[0])<10:
        dobbb+='0'+str(dob[0])
    else:
        dobbb += str(dob[0])

    dobbb += '-'

    if int(dob[1]) < 10:
        dobbb += '0' + str(dob[1])
    else:
        dobbb += str(dob[1])

    dobbb += '-'

    dobbb += dob[2]


    return dobbb

@app.route('/Login')
def login():

    if session.get('id') is not None:
        return redirect(url_for('admin'))
    else:
        return render_template('login.html')

@app.route('/Login', methods=['POST'])
def login_request():
    if request.method == 'POST':
        Email = request.form['emailOrPhone']
        Password = request.form['pass']

        print(Email+' '+Password, flush=True)

        db = DatabaseByPyMySQL()

        user_type, user_name, status = db.Login(Email, Password)

        if status and user_type == 'ADMIN':
            user, sts = db.getUserByEmail(Email)

            session['UserID'] = user['UserID']
            session['UserName'] = user['UserName']
            session['UserEmail'] = user['UserEmail']
            session['Type'] = user['Type']

            return redirect(url_for('admin'))
        else:
            return render_template('login.html')

    return render_template('login.html')

@app.route('/Logout')
def logout():
    session.pop('UserID', None)
    session.pop('UserName', None)
    session.pop('UserEmail', None)
    session.pop('Type', None)

    return redirect(url_for('login'))

#################### WEBSITE END ####################################

if __name__ == '__main__':
    app.debug = True
    app.run()

