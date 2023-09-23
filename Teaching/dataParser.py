import random, string
import subprocess
import zipfile
import csv
import os
ALLOWED_EXTENSIONS = {'zip'}

def getToken():
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(20))

def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def checkFileUploaded(filePath):
    if (os.path.exists("./UPLOAD/{}".format(filePath))):
        return "PASS"
    else:
        return "FAIL"

def parseProgram(token, fileName):
    filePath = './UPLOAD/{}'.format(fileName)
    if (zipfile.is_zipfile(filePath)):
        
        ### create folder
        folderPath = "mkdir {}".format(token)
        if (not os.path.exists(token)):
            os.system(folderPath)

        ### unzip
        ZIP = zipfile.ZipFile(filePath)
        ZIP.extractall("./{}".format(token))
        ZIP.close()

        ### Find .c and .h
        print("Finding .c and .h...")
        folder = "./{}/{}".format(token, fileName[:-4])
        cmd_findSrc = "find " + folder + " -name \"*.c\""
        src_c_list = str(subprocess.Popen(cmd_findSrc, shell=True, stdout=subprocess.PIPE).communicate()[0])[2:].split("\\n")
        cmd_findSrc = "find " + folder + " -name \"*.h\""
        src_h_list = str(subprocess.Popen(cmd_findSrc, shell=True, stdout=subprocess.PIPE).communicate()[0])[2:].split("\\n")

        src_c_list = src_c_list[:-1]
        src_h_list = src_h_list[:-1]

        if len(src_c_list) == 1 and src_c_list[0] == "b''" and len(src_h_list) == 1 and src_h_list[0] == "b''":
            return False

        ### Generate global variable List
        print("Finding Global Variables...")
        cmd_generateGlobalVariable = "ctags -x --sort=yes --c-kinds=v "
        variableName = []
        variablePath = []
        for src in src_c_list:
            variable_list = str(subprocess.Popen(cmd_generateGlobalVariable + src + " | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).communicate()[0]).split("\\n")
            path_list     = str(subprocess.Popen(cmd_generateGlobalVariable + src + " | awk '{print $4}'", shell=True, stdout=subprocess.PIPE).communicate()[0]).split("\\n")
            variable_list = variable_list[:-1]
            path_list = path_list[:-1]
            if len(variable_list) != 0:
                variable_list[0] = variable_list[0][2:]
                path_list[0] = path_list[0][2:]
            for l in range(len(variable_list)):
                variableName.append(variable_list[l])
                variablePath.append(path_list[l])

        for src in src_h_list:
            variable_list = str(subprocess.Popen(cmd_generateGlobalVariable + src + " | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).communicate()[0]).split("\\n")
            path_list     = str(subprocess.Popen(cmd_generateGlobalVariable + src + " | awk '{print $4}'", shell=True, stdout=subprocess.PIPE).communicate()[0]).split("\\n")
            variable_list = variable_list[:-1]
            path_list = path_list[:-1]
            if len(variable_list) != 0:
                variable_list[0] = variable_list[0][2:]
                path_list[0] = path_list[0][2:]
            for l in range(len(variable_list)):
                variableName.append(variable_list[l])
                variablePath.append(path_list[l])

        ### CSV writting
        print("CSV Writting...")
        with open('./{}/report.csv'.format(token), 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ITEM', 'Variable Name', 'In Which Program'])
            for i in range(len(variableName)):
                writer.writerow([i, variableName[i], variablePath[i]])
            
        ### Log
        print("Done")

        return True
    
    else :
        return False