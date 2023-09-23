from flask import Flask, send_from_directory, request, render_template
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

import os
from email_validator import validate_email
import time

import dataParser as dP
import dataStore as dS

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def indexHTML():
    return render_template('index.html')

@app.route("/CreateToken/<EMAIL>")
def createToken(EMAIL):
    if validate_email(EMAIL):
        if EMAIL not in dS.getEmailList():
            token = dP.getToken()
            timestamp = time.time_ns()
            if (dS.insertData("tokenDataSet", timestamp, EMAIL, token, None, None)):
                return token
            else:
                return "Can't insert data into table"
        else:
            return "Email is duplicate"
    else:
        return "Email is invalid"

# TEST TOKEN : 3ThjYRWj308jatUXmNlu
@app.route("/CheckToken/<TOKEN>", methods=['GET'])
def checkToken(TOKEN):
    if TOKEN in dS.getTokenList():
        return "PASS"
    else:
        return "FAIL"
    
@app.route("/CheckFileUploaded/<FILENAME>", methods=['GET'])
def checkFileUploaded(FILENAME):
    return dP.checkFileUploaded(FILENAME)

@app.route("/UploadFile", methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        file = request.files['file']
        if file and dP.allowedFile(file.filename):
            filename = secure_filename(file.filename)
            file.save("./UPLOAD/{}".format(filename))
            return "PASS"
    else:
        return "Not POST method"
    
@app.route("/ParseProgram/<DATA>", methods=['GET', 'POST'])
def parseProgram(DATA):
    token = DATA.split("&")[0]
    fileName = DATA.split("&")[1]
    status = dP.parseProgram(token, fileName)
    if status:
        return send_from_directory(directory = "/home/yitse/tutor/{}".format(token), filename = "report.csv", as_attachment=True)
    else:
        return "FAIL"

if __name__ == '__main__':
    os.system("sudo mysql &")
    app.run(host = '0.0.0.0', port = 11111, debug = True)