from configset import *
import cognitive_face as CF
from time import gmtime, strftime
import json
import picamera
import cv2
import io
import numpy
import os
import time
import sys
import config
import MySQLdb


ending = False
amount = '0'

while (amount == '0' ):
	
	stream = io.BytesIO()
	with picamera.PiCamera() as camera:
		camera.resolution = (320, 240)
		camera.capture(stream, format='jpeg')	
	buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)	
	image = cv2.imdecode(buff, 1)	
	face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')	
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)	
	faces = face_cascade.detectMultiScale(gray, 1.1, 5)
	amount = str(len(faces))
	if str(len(faces)) == '0':
		print errorDetectFace
		print errorAdjustPosition
	elif str(len(faces)) != '0':
		cv2.imwrite( "deposit.jpg",image)
		print DetectFace
		
img_url = "deposit.jpg"
		
CreateFaceId = CF.face.detect("deposit.jpg")
if CreateFaceId == []:
	print errorRecognize
if CreateFaceId != []:
	faceId = (CreateFaceId[0]["faceId"])
	identify = CF.face.identify([faceId] , person_group_id, max_candidates_return=1, threshold = 0.7 )
	candidates = (identify[0]["candidates"])
	if candidates == []:
		print errorRecognize
	if candidates != []:  
		personIdU = (candidates[0]["personId"])
		confidence = (candidates[0]["confidence"])
		if confidence < 0.6:
			print errorRecognize
		if confidence >= 0.6:
			getName = CF.person.get(person_group_id, personIdU)
			CF.person.add_face(img_url, person_group_id, personIdU, user_data=None,target_face=None)
			resultN = (getName["name"])
			sql1 = """SELECT Balance FROM %s WHERE personId = '%s'""" % (table, personIdU)
			cursor.execute(sql1)
			result = cursor.fetchall()
			balance = result[0][0]
			print ("Hello! Are you " + resultN +" ?")
			respond = raw_input("Yes/No   ")
			if respond == "Yes" or respond == "yes" or respond == "YES" or respond == "Y" or respond == "y":
				print ("Please tell the stuco store manager to give the permission!")
				amount = '0'
				while (amount == '0' ):
					stream = io.BytesIO()
					with picamera.PiCamera() as camera:
						camera.resolution = (320, 240)
						camera.capture(stream, format='jpeg')	
					buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)	
					image = cv2.imdecode(buff, 1)	
					face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')	
					gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)	
					faces = face_cascade.detectMultiScale(gray, 1.1, 5)
					amount = str(len(faces))
					if str(len(faces)) == '0':
						print errorDetectFace
						print errorAdjustPosition
					elif str(len(faces)) != '0':
						cv2.imwrite( "admin.jpg",image)
						print CaptureFace	
						img_url = "admin.jpg"
						person_group_id = 'pas'
						CreateFaceId = CF.face.detect("admin.jpg")
						if CreateFaceId == []:
							print errorRecognizeAdmin
						if CreateFaceId != []:
							faceId = (CreateFaceId[0]["faceId"])
							identify = CF.face.identify([faceId] , person_group_id, max_candidates_return=1, threshold = 0.7 )
							candidates = (identify[0]["candidates"])
							if candidates == []:
								print errorRecognizeAdmin
							if candidates != []:  
								personId = (candidates[0]["personId"])
								confidence = (candidates[0]["confidence"])
								if confidence < 0.6:
									print errorRecognizeAdmin
								if confidence >= 0.6:
									getName = CF.person.get(person_group_id, personId)
									CF.person.add_face(img_url, person_group_id, personId, user_data=None,target_face=None)
									sql2 = """SELECT Admin, First_Name, Last_Name FROM %s WHERE personId = '%s'""" % (table, personId)
									cursor.execute(sql2)
									result1 = cursor.fetchall()
									AdminFirstName = result1[0][1]
									AdminLastName = result1[0][2]
									AdminName = AdminFirstName + " " +AdminLastName
									print "Hello! Admin "+ AdminName
									tf = result1[0][0]
									 
									if tf == 1:
										while(ending == False):
											item = input("Please enter deposit: ")
											if item < 0:
												print "Error! Deposit cannot be negative!"
												ending = False
											else:
												sql3 = """SELECT Balance FROM %s WHERE personId = '%s' """ % (table, personIdU)
												cursor.execute(sql3)
												result3 = cursor.fetchall()
												balanceB = result3[0][0]
												
												int(item)
												int(balanceB)
												balance = balanceB + item
												
												sql4 = """UPDATE %s SET Balance = '%s' WHERE personId = '%s'""" % (table, balance, personIdU)
												cursor.execute(sql4)
												item = str(item)
												itemdeposit = "Deposit $ "+item
												Status = "Deposit"
												sql5 = """INSERT INTO %s (Admin, Date, Items, Status, User, Balance) VALUES('%s', '%s','%s', '%s', '%s', '%s');""" % (Log, AdminName, date, itemdeposit, Status, resultN, balance)
												cursor.execute(sql5)
												
												sql6 = """SELECT Balance, First_Name, Last_Name, Email FROM %s WHERE personId = '%s' """ % (table, personIdU)
												cursor.execute(sql6)
												result6 = cursor.fetchall()
												balanceA = "$" + str(result6[0][0] )
												UN = result6[0][1] +" "+ result6[0][2]
												email = result6[0][3]
												print ("Thank You! "+ UN +"! You have "+ balanceA +" in your account")
												db.commit()
												db.close()
												
												email = str(email)
												date = str(date)
												UN = str(UN)
												item = str(item)
												strSubject = "PAS Stuco - Deposit"
												strContent = "Hi, "+UN+", You have deposited $ "+item+" on "+date + ". Your account balance is now "+ balanceA+"."
												sendGmailSmtp('stucopas@gmail.com','sciencefair',email,strSubject,strContent)
												sendGmailSmtp('stucopas@gmail.com','sciencefair',"stucopas@gmail.com",strSubject,strContent)
												ending = True
									else:
										print "You do not have the permission to access!!"
									
																											
			else:
				print ("Error! Please contact any Stuco members for further information!")						
			
				
