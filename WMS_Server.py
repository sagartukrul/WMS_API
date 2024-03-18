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

@app.route('/putaway', methods=['Get', 'Post'])
def putaway():
    global cursor

    if request.method == 'POST':

        content = request.json
        response = ""
        Status = ""

        Matrial_Barcode = content["Barcode"]
        Putaway_Location = content['Location']
        try:
            cursor.execute(f"select Status, Location from tblPOC_Stock where Barcode='{Matrial_Barcode}'")
            dbData = cursor.fetchall()
            Matcode = Matrial_Barcode.split('|')
            if len(dbData) > 0:
                for x in dbData:
                    if x[0] == 1: 
                        cursor.execute(f"update tblPOC_Stock set Status = 2, Location ='{Putaway_Location}' where Barcode = '{Matrial_Barcode}'")
                        # cursor.execute(f"update tblPOC_Import_Data set Status = 2 where Mat_Code = '{Matcode[0]}'")
                        # cursor.execute(f"update tblPOC_Pick set Status = 2 where MatCode = '{Matcode[0]}' and Batch = '{Matcode[1]}'")
                        cursor.commit()
                        

                        Status = "Successful"
                        response = "Putaway Successful"
                    elif x[0] == 2:
                        Status = "Unsuccessful"
                        response = "Already Putaway complete"
                    else:
                        Status = "Unsuccessful"
                        response = "Please complete Putaway process"
            else:
                Status = "Error"
                response = "Barcode not found"
        except Exception as ex: 
            print(ex)
            Status = "Error"
            response = "Got Error, Please try again"

        context = {
            "Status" : Status,
            "Message" : response
        }
        return json.dumps(context)
        
@app.route('/pickup', methods=['Get', 'Post'])
def pickup():
        global cursor
        Status = ""
        response = ""

        try:
            unsuccessful = False
            stocklist = {}
            DeliveryList = {}

            cursor.execute(f"select Delivery, MatCode, Batch, Req_Box_Qty from tblPOC_Pick where Batch != ''")
            exc_data = cursor.fetchall()
            if len(exc_data) > 0:
                for x in exc_data: 
                    data = {x[0]: f'{x[1]},{x[2]},{x[3]}'}
                    DeliveryList.update(data)
            else:
                unsuccessful = True

            cursor.execute(f"select Barcode, Mat_Code, Batch, Location from tblPOC_Stock where Status = 2231 and Location!=''")
            stockdata = cursor.fetchall()
            
            if len(stockdata) > 0:
                for x in stockdata : 
                    # print(x)
                    data = {x[0]: f'{x[1]},{x[2]},{x[3]}'}
                    stocklist.update(data)
            else:
                unsuccessful = True
            
            response = {'DeliveryList': DeliveryList, 'StockList':stocklist }
            print(response)
            if unsuccessful: Status="Unsuccessful"
            else: Status="Successful"


        except Exception as ex: 
            print(ex)
            Status = "Error"
            response = "Got Error, Please try again"

        context = {
            "Response":response,
            "Status" : Status
        }
        return json.dumps(context)

@app.route("/", methods=['POST','GET'])
def Main():
    return "<h1> WMS Server is running </h1>"





if DB_Status: app.run(host='0.0.0.0',debug=False)