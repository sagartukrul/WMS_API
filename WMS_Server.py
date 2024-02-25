from flask import Flask, request,render_template,jsonify, redirect, json
import pyodbc
import os

try:
    output = os.path.join('Files/', "SQLSetting.json")
    with open(output,'r') as conf:
        params = json.load(conf) ['SQLParameter']
        conf.close()
except:
    log = {'SQLParameter':{'Host_Ip':'', 'User': '', 'Database': '', 'Password': '', 'Key':''}}
    json_object = json.dumps(log, indent = 4)
    output = os.path.join('Files/', "SQLSetting.json")
    with open(output, "w+") as outfile:  
        outfile.write(json_object)
        outfile.close()

from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsScene, QGraphicsPixmapItem, QMessageBox, QFileDialog, QVBoxLayout, QPushButton

# QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
# QtWidgets.QApplication.setWindowIcon(QtGui.QIcon('Logo.ico'))

app = QApplication([])

def ShowPopup(status, message):
    msg = QMessageBox()
    msg.setWindowTitle(status)
    if status == 'Error!!!':
        msg.setIcon(QMessageBox.Critical) #Critical,Warning,Information,Question
    else: msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.exec_()


DB_Status = False

output = os.path.join('Files/', "SQLSetting.json")
with open(output,'r') as conf:
    params = json.load(conf) ['SQLParameter']
    Host = params['Host_Ip']
    User = params['User']
    Database = params['Database']
    Pass = params['Password']
    conf.close()

server = Host 
database = Database 
username = User 
password = Pass 
try:
    print("Try to connect database...")
    cnxn = pyodbc.connect(driver='{SQL Server}', host=server, database=database,user=username, password=password)
    cursor = cnxn.cursor()
    DB_Status = True
except:ShowPopup('Error!!!', "Database not connected.")


app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def Main():
    global cursor

    if request.method == 'POST':

        content = request.json

        
        if content['Process'] == "Putaway":
            response = ""
            Status = ""

            Matrial_Code = content["Barcode"]
            Putaway_Location = content['Location']
            try:
                cursor.execute(f"select Status, Location from tblPOC_Stock where Barcode='{Matrial_Code}'")
                dbData = cursor.fetchall()
                Matcode = Matrial_Code.split('|')
                for x in dbData:
                    if x[0] == 1: 
                        cursor.execute(f"update tblPOC_Stock set Status = 2, Location ='{Putaway_Location}' where Barcode = '{Matrial_Code}'")
                        cursor.execute(f"update tblPOC_Import_Data set Status = 2 where Mat_Code = '{Matcode[0]}'")
                        cursor.execute(f"update tblPOC_Pick set Status = 2 where MatCode = '{Matcode[0]}'")
                        cursor.commit()
                        

                        Status = "Successful"
                        response = "Putaway Successful"
                    elif x[0] == 2:
                        Status = "Unsuccessful"
                        response = "Already Putaway complete"
                    else:
                        Status = "Unsuccessful"
                        response = "Please complete in process"
            except Exception as ex: 
                Status = "Error"
                response = "Got Error, Please try again"
                print(ex)

            context = {
                "Status" : Status,
                "Message" : response
            }
            return json.dumps(context)
        
        elif content['Process'] == "GetDeliveryList":
            cursor.execute(f"select DISTINCT  Delivery from tblPOC_Pick")
            exc_data = cursor.fetchall()
            # print(exc_data)
            temp = []
            for x in exc_data: 
                temp.append(x[0])

            context = {
                "Delivery_list":temp
            }
            return json.dumps(context)


    elif request.method == 'GET':
        return "<h1> WMS Server is running </h1>"





if DB_Status: app.run(host='0.0.0.0',debug=False)