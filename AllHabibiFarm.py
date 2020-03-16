import base64
import hashlib
import os
import sys


from flask import Flask, render_template, request, flash, url_for, send_from_directory, jsonify, session, abort, redirect
import pymysql
from datetime import datetime

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/UPLOADS/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


'''pEKa_p=P-y2]
bdpibkmt_al_habibi_farm
bdpibkmt_flask_all_habibi_farm
'''
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
        print('getAnimalLastID : ', str(data[0]['AnimalID']), flush=True)

        if len(data)>0:
            return data[0]['AnimalID'], True
        else:
            return data, False

    def getAnimalByTag(self, tag):
        sql_qry = 'SELECT * FROM animal WHERE AnimalTag = "{0}";'.format(tag)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAnimalByTag : ', str(data[0]), flush=True)

        if len(data) > 0:
            return data[0], True
        else:
            return data, False


    def updateCommonData(self, CAT, TYPE):

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
                        sql = 'UPDATE commondata SET SET TotalGoat = {0}, DiedGoat = {1} WHERE CdID = {2};'.format(
                            data[0]['TotalGoat'] - 1, data[0]['DiedGoat'] + 1, data[0]['CdID'])
                    elif TYPE == 'SLAUGHTER':
                        sql = 'UPDATE commondata SET TotalGoat = {0}, SlaughterGoat = {1} WHERE CdID = {2};'.format(
                            data[0]['TotalGoat'] - 1, data[0]['SlaughterGoat'] + 1, data[0]['CdID'])
                elif CAT == 'SHEEP':
                    if TYPE == 'ADD':
                        sql = 'UPDATE commondata SET TotalSheep = {0} WHERE CdID = {1};'.format(data[0]['TotalGoat'] + 1,
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
                elif CAT == 'CAMEL':
                    if TYPE == 'ADD':
                        sql = 'UPDATE commondata SET TotalCamel = {0} WHERE CdID = {1};'.format(data[0]['TotalGoat'] + 1,
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
                elif CAT == 'HORSE':
                    if TYPE == 'ADD':
                        sql = 'UPDATE commondata SET TotalHorse = {0} WHERE CdID = {1};'.format(data[0]['TotalGoat'] + 1,
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
            user = self.getUserByEmail(Email)
            if user['UserPass'] == Pass:
                return user['Type'], True
            else:
                return 'NULL', False
        else:
            return 'NULL', False

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
        sql_qry = 'SELECT * FROM vaccindetails WHERE AnimalTag = "{0}";'.format(AnimalTag)
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
    def addAnimal(self, AnimalCategory, AnimalBreed, AnimalSex, AnimalOwner, AnimalDOB, AnimalFather, AnimalMother, AnimalWeight, AnimalPictureBlob):

        try:
            last_id, sts = self.getAnimalLastID()
            print('last ID = ' + str(last_id), flush=True)
            animal_id = int(last_id) + 1
            animal_tag = AnimalCategory[0:2]+'-'+AnimalBreed[0:3]+'-'+str(animal_id)


            # current date and time
            now = datetime.now()

            addedDate = str(now.strftime("%d-%m-%Y"))

            # Adding
            sql1 = 'INSERT INTO animal(AnimalID, AnimalTag, AnimalCategory, AnimalBreed, AnimalSex, AnimalOwner, AnimalDOB, AnimalFather, AnimalMother, AnimalWeight, AnimalStatus, AddedDate, UpdatedDate)' \
                   ' VALUES({0},"{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}",{9},"ALIVE","{10}","{11}");'.format(animal_id, animal_tag, AnimalCategory, AnimalBreed, AnimalSex,
                                                                                                                    AnimalOwner, AnimalDOB, AnimalFather, AnimalMother, AnimalWeight, addedDate, addedDate)
            print(sql1, flush=True)
            self.cursor.execute(sql1)
            self.conection.commit()



            sql2 = 'INSERT INTO animalpicture (AnimalID, AnimalPictureBlob) VALUES({0}, "{1}")'.format(animal_id, AnimalPictureBlob)
            self.cursor.execute(sql2)
            self.conection.commit()

            print(sql2, flush=True)

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
                self.updateCommonData(animal['AnimalCategory'], 'DIED')

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
                self.updateCommonData(animal['AnimalCategory'], 'MISS')

            # current date and time
            now = datetime.now()
            dateNow = now.strftime("%d-%m-%Y")
            sts = 'MISSING'
            cause = 'NULL'
            # Adding Dish
            sql1 = 'UPDATE Animal SET AnimalStatus = "{0}",  AnimalStatusDate = "{1}", AnimalStatusCause = "{2}", UpdateDate = "{3}" WHERE AnimalTag = "{4}";'.format(
                sts, Date, cause, dateNow, AnimalTag)
            self.cursor.execute(sql1)
            self.conection.commit()

            print(sql1, flush=True)


            return True

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
                self.updateCommonData(animal['AnimalCategory'], 'SLAUGHTER')

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

        except:
            print('Error on addSlaughterAnimal()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    # #17
    def addVaccineDetails(self, AnimalTag, Date, details):

        try:

            # Adding addVaccineDetails
            sql1 = 'INSERT INTO vaccinedetails(AnimalTag, VDetails, VDate) VALUES("{0}", "{1}", "{2}");'.format(AnimalTag, Date, details)
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
    def updateAnimal(self, AnimalID, AnimalSex, AnimalOwner, AnimalDOB, AnimalFather, AnimalMother, AnimalWeight, AnimalPictureBlob):

        try:
            # current date and time
            now = datetime.now()
            dateNow = now.strftime("%d-%m-%Y")

            # Update
            sql1 = 'UPDATE Animal SET AnimalSex = "{0}",  AnimalOwner = "{1}", AnimalDOB = "{2}", AnimalFather = "{3}", AnimalMother = "{4}", ' \
                   'AnimalWeight = {5}, UpdatedDate = "{6}" WHERE AnimalID = {7};'.format(
                                                                        AnimalSex, AnimalOwner, AnimalDOB, AnimalFather,AnimalMother, AnimalWeight, dateNow, AnimalID)
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

    #22
    def getAnimalPictureByID(self, id):
        sql_qry = 'SELECT * FROM animalpicture WHERE AnimalID = {0};'.format(id)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print(data[0]['AnimalPictureBlob'], flush=True)

        blob = data[0]['AnimalPictureBlob']

        encrypted_text = base64.b64encode(blob)

        print(str(type(encrypted_text))+' '+encrypted_text, flush=True)

        print('getAnimalPictureByID : ', str(data[0]), flush=True)

        if len(data) > 0:
            return data[0], True
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
    type, status = DB.Login(email, passs)

    if status:
        return jsonify({"status": 1, "type": type}), 200
    else:
        return jsonify({"status": 0, "type": type}), 200

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
        AnimalWeight = contentJSON["AnimalWeight"]
        AnimalPictureBlob = contentJSON["AnimalPictureBlob"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400

    DB = DatabaseByPyMySQL()
    status = DB.addAnimal(AnimalCategory, AnimalBreed, AnimalSex, AnimalOwner, AnimalDOB, AnimalFather, AnimalMother, AnimalWeight, AnimalPictureBlob)

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
@app.route('/API/SearchAnimal', methods=['POST'])
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
        return jsonify({"status": 0, "data": "NULL"}), 400

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
        AnimalWeight = contentJSON["AnimalWeight"]
        AnimalPictureBlob = contentJSON["AnimalPictureBlob"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400

    DB = DatabaseByPyMySQL()
    status = DB.updateAnimal(AnimalID, AnimalSex, AnimalOwner, AnimalDOB, AnimalFather, AnimalMother, AnimalWeight, AnimalPictureBlob)

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

# 22
@app.route('/API/AnimalPictureByID', methods=['POST'])
def AnimalPictureByID():
    contentJSON = request.json
    try:
        ID = contentJSON["ID"]

    except:
        print('Error = ', str(sys.exc_info()[0]), flush=True)
        return jsonify({"status": 0, "data": "NULL"}), 400

    DB = DatabaseByPyMySQL()
    data, status = DB.getAnimalPictureByID(ID)

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

            DishName = request.form['DishName']
            DishDes = request.form['DishDes']
            DishPrice = request.form['DishPrice']
            isAvailable = request.form['isAvailable']
            DishMenu = request.form['DishMenu']

            db = DatabaseByPyMySQL()
            status = db.addDish(dishName=DishName, dishDes=DishDes, dishPrice=DishPrice, dishPic=filename,
                                isAvailable=isAvailable, menu_id=DishMenu)

def uploadFileTuto():
    @app.route('/file-upload', methods=['POST'])
    def upload_file():
        # check if the post request has the file part
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resp = jsonify({'message': 'File successfully uploaded'})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
            resp.status_code = 400
            return resp

#################### API END ####################################

#################### WEBSITE ####################################
@app.route('/')
def home():
    db = DatabaseByPyMySQL()
    data = db.getAnimalPictureByID(1)
    return 'HELLO'
    #return render_template('')

#################### WEBSITE END ####################################

if __name__ == '__main__':
    app.debug = True
    app.run()

