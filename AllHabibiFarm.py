import hashlib
import sys


from flask import Flask, render_template, request, flash, url_for, send_from_directory, jsonify, session, abort, redirect
import pymysql
from datetime import datetime

app = Flask(__name__)

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
        sql_qry = 'SELECT TOP 1 * FROM animal ORDER BY AnimalID DESC'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAnimalLastID : ', str(data), flush=True)

        if len(data)>0:
            return data[0]['AnimalID'], True
        else:
            return data, False


    #1
    def Login(self, Email, Pass):
        print(Email, Pass, flush=True)
        if self.isEmailExist(Email):
            user = self.getUserByEmail(Email)
            if user['UserPass'] == Pass:
                return True, user['Type']
            else:
                return False, 'NULL'
        else:
            return False, 'NULL'

    #2
    def getCommonData(self):
        sql_qry = 'SELECT * FROM commondata;'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getCommonData : ', str(data), flush=True)
        return data[0]

    #3
    def getAllAnimals(self):
        sql_qry = 'SELECT * FROM animal;'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAllAnimals : ', str(data), flush=True)
        return data

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

        sql_qry = 'SELECT * FROM animal WHERE AnimalStatus = {0};'.format('SLAUGHTER')
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAllSlaughterAnimal : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    # #9
    def getAllMissingAnimal(self):
        sql_qry = 'SELECT * FROM animal WHERE AnimalStatus = {0};'.format('MISSING')
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
        sql_qry = 'SELECT * FROM user WHERE Type = {0};'.format('EMPLOYEE')
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
            last_id = self.getAnimalLastID()
            animal_id = (int)(last_id) + 1
            animal_tag = AnimalCategory[0:2]+'-'+AnimalBreed[0:3]+'-'+str(animal_id)

            # current date and time
            now = datetime.now()

            addedDate = now.strftime("%d-%m-%Y")
            updatedDate = addedDate

            # Adding Dish
            sql1 = 'INSERT INTO animal(AnimalID, AnimalTag, AnimalCategory, AnimalBreed, AnimalSex, AnimalOwner, AnimalDOB, AnimalFather, AnimalMother, AnimalWeight, AnimalStatus, AddedDate, UpdateDate)' \
                   ' VALUES({0},"{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}",{9},"ALIVE","{10}","{11}");'.format(animal_id, animal_tag, AnimalCategory, AnimalBreed, AnimalSex,
                                                                                                                    AnimalOwner, AnimalDOB, AnimalFather, AnimalMother, AnimalWeight, addedDate, updatedDate)
            self.cursor.execute(sql1)
            self.conection.commit()

            print(sql1, flush=True)

            sql2 = 'INSERT INTO animalpicture (AnimalID, AnimalPictureBlob) VALUES({0}, "{1}")'.format(animal_id, AnimalPictureBlob)
            self.cursor.execute(sql2)
            self.conection.commit()

            print(sql2, flush=True)

            return True

        except:
            print('Error on addAnimal()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    # #14
    def addDiedAnimal(self, AnimalTag, Date, Cause):

        try:
            # current date and time
            now = datetime.now()
            dateNow = now.strftime("%d-%m-%Y")
            sts = 'DIED'
            # Adding Dish
            sql1 = 'UPDATE Animal SET AnimalStatus = "{0}",  AnimalStatusDate = "{1}", AnimalStatusCause = "{2}", UpdateDate = "{3}" WHERE AnimalTag = "{4}";'.format(sts, Date, Cause, dateNow, AnimalTag)
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
            # current date and time
            now = datetime.now()
            dateNow = now.strftime("%d-%m-%Y")
            sts = 'SLAUGHTER'
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

            # Adding Dish
            sql1 = 'UPDATE Animal SET AnimalSex = "{0}",  AnimalOwner = "{1}", AnimalDOB = "{2}", AnimalFather = "{3}", AnimalMother = "{4}", ' \
                   'AnimalWeight = {5}, AnimalPictureBlob = "{6}", UpdateDate = "{7}" WHERE AnimalID = "{8}";'.format(
                                                                        AnimalSex, AnimalOwner, AnimalDOB, AnimalFather,AnimalMother, AnimalWeight, AnimalPictureBlob, dateNow, AnimalID)
            self.cursor.execute(sql1)
            self.conection.commit()

            print(sql1, flush=True)

            return True

        except:
            print('Error on updateAnimal()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

#################### DATABASE END ####################################

#################### API ####################################

@app.route('/API/testReturn', methods=['POST'])
def returnData():
    return jsonify({"error": "OK OK OK "}), 200

@app.route('/API/testReceive/<id>', methods=['POST'])
def testReceive(id):
    posss = ''
    if request.method == 'POST':
        posss = request.args['FFF']

    contentJSON = request.json

    return jsonify({"ID": id, "JSON":contentJSON, "POST": posss}), 200


#1
@app.route('/API/login', methods=['POST'])
def Login():

    contentJSON = request.json
    email = contentJSON["Email"]
    passs = contentJSON["Pass"]

    DB = DatabaseByPyMySQL()
    status, type = DB.Login(email, passs)

    if status:
        return jsonify({"status": 1, "type": type}), 200
    else:
        return jsonify({"status": 0, "type": type}), 200

#2
#3
# 4
# 5
# 6
# 7
# 8
# 9
# 10
# 11
# 12
# 13
# 14
# 15
# 16
# 17
# 18
# 19
# 20
@app.route('/API/testReturn', methods=['POST', 'GET'])
def returnDataasd():
    return jsonify({"error": "OK OK OK "}), 200


#################### API END ####################################

#################### WEBSITE ####################################
@app.route('/')
def home():
   return render_template('')

#################### WEBSITE END ####################################

if __name__ == '__main__':
    app.debug = True
    app.run()

