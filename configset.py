import MySQLdb
from time import gmtime, strftime
from datetime import datetime
from emailsending import *
db = MySQLdb.connect("SERVERIP","USERNAME","PASSWORD","TABLE", charset='utf8' )
cursor = db.cursor()
person_group_id = "pas"
table = "Users"
Log = "Log"
Items = "Items"
date = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
errorDetectFace = "Cannot detect any faces."
errorAdjustPosition = "Please adjust your position to the camera."
DetectFace = "The face has been detected!"
errorRecognize = "The system cannot recognize your face. \nPlease contact the nearest STUCO member for help."
alreadyReg = "You are already registered!"
errorCapture = "Unable to analyze your facial features. Press retry to restart the program!"
CaptureFace = "The face has been captured!"
errorRecognizeAdmin = "The system cannot recognize your face!"
Registration_Completed = "Registration completed!"
errorBonusPoint = "Your value for bonus points is not valid!"
errorBonusPayment = "You can only use bonus points by paying from account!"
mutiface_mesg = "The system detected more than one face! Please take a picture by yourself only!"
stucoPermission = "Please tell the nearest stuco store managers! \nThe system needs the stuco store managers' facial features to grant the permission!"
currentPath = "/home/pi/Desktop/FacePython/Photos/"
threshold = 0
bonusPointValue = "0.01"



