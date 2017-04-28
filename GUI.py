from appJar import gui
from configset import *
from emailsending import *
import hashlib
import cognitive_face as CF
from cognitive_face.util import *
import json
import picamera
from blink import *
import cv2
import io
import numpy
import os
import time
import sys
import config
import MySQLdb
import base64
import shortuuid
import uuid
import hashlib
GPIO.setwarnings(False)
lcd = I2C_LCD_driver.lcd()
def home_lcd():
	lcd.lcd_clear()
	lcd.lcd_display_string("  STUCO STORE", 1)
	lcd.lcd_display_string("    Welcome! ", 2)
	
"""-----------------------GUI_Settings-----------------------"""
app = gui("Stuco Store System","500x120")
app.setResizable(canResize=True)
app.setLocation(850,50)
app.setFont(12)
home_lcd()
loading()

"""-----------------------Home_Functions-----------------------"""
def home_page(btn):
	home_lcd()
	app.removeAllWidgets()
	app.setGeometry("500x150")
	app.startLabelFrame("Activate")
	app.setSticky("new")
	app.addLabel("Activation_Code","Activation Code: ", 0 ,0 )
	app.addEntry("Activation_Code_entry",0,1)
	app.setSticky("new")
	app.addButton("Submit",submit_activate,1,0)
	app.stopLabelFrame()
	
def submit_activate(btn):
	ActivationCode = app.getEntry("Activation_Code_entry")
	sql = """SELECT First_Name, Last_Name, Email, Active, Salt, Passcode, Grade  FROM %s WHERE Activation_Code = '%s'""" % (table, ActivationCode)
	cursor.execute(sql)
	result = cursor.fetchall()
	if result ==():
		warning()
		app.errorBox("Error","Invalid Activation Code!")
	elif (ActivationCode == "" or ActivationCode == '0'):
		warning()
		app.errorBox("Error","Invalid Number!")
	else:
		app.infoBox("Message","Valid Activation Code! Please look into the camera!")
		salt = result[0][4]
		email = result[0][2]
		passcode = result[0][5]
		hash_pass = hashlib.sha256(salt+passcode).hexdigest()
		FirstName = result[0][0]
		LastName = result[0][1]
		grade = result[0][6]
		Name = FirstName + ' ' + LastName
		currentPath = "/home/pi/Desktop/FacePython/Photos/"
		folderPath = currentPath + Name + '/'
		img_url = folderPath + "active.jpg"
		
		lcd.lcd_clear()
		lcd.lcd_display_string("Valid Activation", 1)
		lcd.lcd_display_string("Code!", 2)
		time.sleep(1.5)
		lcd.lcd_clear()
		lcd.lcd_display_string("Please look into", 1)
		lcd.lcd_display_string("the camera!", 2)
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
				warning_reco()
			elif str(len(faces)) != '0':
				if not os.path.exists(folderPath):
						os.makedirs(folderPath)
				cv2.imwrite( folderPath + "active.jpg",image)
				CreateFaceId = CF.face.detect(img_url)
				correct()
				lcd.lcd_clear()
				lcd.lcd_display_string("The face has", 1)
				lcd.lcd_display_string("been detected!", 2)
				time.sleep(1)
				lcd.lcd_clear()
				lcd.lcd_display_string("Processing...", 1)
				CreateFaceId = CF.face.detect(img_url)
				if CreateFaceId == []:
					warning()
					lcd.lcd_clear()
					lcd.lcd_display_string("The lighting is", 1)
					lcd.lcd_display_string("not enough!", 2)
					time.sleep(3)
					home_page(btn)
				else:
					CreatePerson = CF.person.create(person_group_id, name=Name, user_data=grade)
					personId = (CreatePerson['personId'])
					AddToGroup = CF.person.add_face(img_url, person_group_id, personId, user_data=None,target_face=None)
					persistedfaceId = (AddToGroup['persistedFaceId'])
					CF.person_group.train(person_group_id)
					sql2 = """UPDATE %s SET Active = '%s', personId = '%s' , persistedFaceIds = '%s', Activation_Code = '%s'WHERE Email = '%s' &&  Salt = '%s' && grade = '%s'""" % (table, '0',personId, persistedfaceId, '0',email, salt, grade)
					cursor.execute(sql2)
					db.commit()
					strSubject = "PAS Stuco - Activation"
					strContent = "Hi, "+Name+"! Your account has been activated! \nOn "+date+"."
					correct_update()		
					lcd.lcd_clear()
					lcd.lcd_display_string("Activation", 1)
					lcd.lcd_display_string("Completed!", 2)
					sendGmailSmtp('stucopas@gmail.com','sciencefair',email,strSubject,strContent)
					sendGmailSmtp('stucopas@gmail.com','sciencefair',"stucopas@gmail.com",strSubject,strContent)
					home_page(btn)	
		
		
"""-----------------------Home_Code-----------------------"""
app.addToolbar("Activate",home_page,findIcon=True)
app.addLabel("Home_Welcom", "    Welcome to Stuco Store System! \n Please select the services in the toolbar!")

"""-----------------------Register_Functions-----------------------"""
def open_register(btn):
	home_lcd()
	app.removeAllWidgets()
	app.setGeometry("500x270")
	app.startLabelFrame("Registration")
	app.setSticky("new")
	app.addLabel("First_Name_Label","First Name: ",0,0)
	app.addEntry("First_Name_Entry",0,1)
	app.setEntryDefault("First_Name_Entry","First Name(Eg: John)")
	app.setEntryWidth("First_Name_Entry",27)
	app.setFocus("First_Name_Entry")
	app.addLabel("Last_Name_Label","Last Name: ",1,0)
	app.addEntry("Last_Name_Entry",1,1)
	app.setEntryDefault("Last_Name_Entry","Last Name(Eg: Chen)")
	app.setEntryWidth("Last_Name_Entry",27)
	app.addLabel("Grade_Label","Grade: ",2,0)
	app.addLabelOptionBox("Grade",["1","2","3","4","5","6","7","8","9","10","11","12","Teacher"],2,1)
	app.addLabel("PassCode_Label","PassCode(Eg: 0000): ",3,0)
	app.addSecretEntry("PassCode_Entry",3,1)
	app.setEntryDefault("PassCode_Entry","PassCode")
	app.addLabel("Email_Label","Email: ",4,0)
	app.addEntry("Email_Entry",4,1)
	app.setEntryDefault("Email_Entry","Email")
	app.setEntryWidth("Email_Entry",20)
	app.addLabel("Gender_Label","Gender: ",5,0)
	app.addLabelOptionBox("Gender",["Female","Male"],5,1)
	app.addButton("Submit", submit_register, 6,0,3)
	app.setButtonBg("Submit", "grey")
	app.addLabel("Face_Detection","Face Detection",7,0)
	app.addLabel("Identify_Authentication","Authentication",7,1)
	app.setLabelBg("Face_Detection","red")
	app.setLabelBg("Identify_Authentication","red")
	app.stopLabelFrame()
	
def submit_register(btn):
	Register_Warning = app.yesNoBox("Warning!", "Please confirm your information!")
	if(Register_Warning == True):
		FirstName = app.getEntry("First_Name_Entry")
		LastName = app.getEntry("Last_Name_Entry")
		email = app.getEntry("Email_Entry")
		passcode = app.getEntry("PassCode_Entry")
		grade = app.getOptionBox("Grade")
		gender = app.getOptionBox("Gender")
		str(passcode)
		salt_gen = uuid.uuid4().hex
		passcode = hashlib.sha256(salt_gen+passcode).hexdigest()
		if (FirstName == ""):
			warning()
			app.errorBox("Error", "First Name field cannot be blank!")
		if (LastName == ""):
			warning()
			app.errorBox("Error", "Last Name field cannot be blank!")
		if (email == ""):
			warning()
			app.errorBox("Error", "Email field cannot be blank!")
		if(FirstName != "" and LastName != "" and email != ""):
			FirstName = FirstName[:1].upper() + FirstName[1:].lower()
			LastName = LastName[:1].upper() + LastName[1:].lower()
			
			app.setEntryState("First_Name_Entry","disabled")
			app.setEntryState("Last_Name_Entry","disabled")
			app.setEntryState("Email_Entry","disabled")
			app.setEntryState("PassCode_Entry", "disabled")
			app.setOptionBoxState("Grade", "disabled")
			app.setOptionBoxState("Gender", "disabled")
			app.setButtonState("Submit","disabled")
			
			
			FirstNameAuthentic = 0
			LastNameAuthentic = 0
				
			sql = """SELECT First_Name, Last_Name, Grade  FROM %s WHERE Last_Name = '%s' && First_Name = '%s' && grade = '%s' """ % (table, LastName, FirstName, grade )
			cursor.execute(sql)
			result = cursor.fetchall()
			if (result != ()):	
				FirstNameAuthentic = result[0][0]
				LastNameAuthentic = result[0][1]
			
			if (FirstName == FirstNameAuthentic and LastName == LastNameAuthentic):
				warning()
				app.errorBox("Error", alreadyReg)
				open_register(btn)
			else:
				Name = FirstName +" "+ LastName
				lcd.lcd_clear()
				lcd.lcd_display_string("Please look into", 1)
				lcd.lcd_display_string("the camera!", 2)
				folderPath = currentPath + Name + '/'
				img_url = folderPath + "image.jpg"
				if not os.path.exists(folderPath):
						os.makedirs(folderPath)
				
				amount = '0'
				
				while (amount == '0' ):	
					stream = io.BytesIO()
					with picamera.PiCamera() as camera:
						camera.resolution = (360, 270)
						camera.capture(stream, format='jpeg')	
					buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)	
					image = cv2.imdecode(buff, 1)	
					face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')	
					gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)	
					faces = face_cascade.detectMultiScale(gray, 1.1, 5)
					amount = str(len(faces))
					if str(len(faces)) == '0':
						warning_reco()
					elif str(len(faces)) != '0':
						cv2.imwrite( folderPath + "image.jpg",image)
						correct()
						lcd.lcd_clear()
						lcd.lcd_display_string("The face has", 1)
						lcd.lcd_display_string("been detected!", 2)
						time.sleep(1)
						lcd.lcd_clear()
						lcd.lcd_display_string("Processing...", 1)
						app.setLabelBg("Face_Detection","green")
						
				person_group_id = 'pas'
				CreateFaceId = CF.face.detect(img_url)
				faceId = (CreateFaceId[0]["faceId"])
				if faceId == []:
					warning()
					faceId_result = app.retryBox("Error", errorCapture)
					app.setLabelBg("Face_Detection","red") 
					if (faceId_result == True):
						app.setEntryState("First_Name_Entry","normal")
						app.setEntryState("Last_Name_Entry","normal")
						app.setEntryState("Email_Entry","normal")
						app.setEntryState("PassCode_Entry", "normal")
						app.setOptionBoxState("Grade", "normal")
						app.setOptionBoxState("Gender", "normal")
						app.setButtonState("Submit","normal")
					else:
						app.stop()
				else:
					identify = CF.face.identify([faceId] , person_group_id, max_candidates_return=1, threshold = 0.7 )
					candidates = (identify[0]["candidates"])
					if mutiFace == True:
						warning()
						app.errorBox("Error", mutiface_mesg)
						app.setEntryState("First_Name_Entry","normal")
						app.setEntryState("Last_Name_Entry","normal")
						app.setEntryState("Email_Entry","normal")
						app.setEntryState("PassCode_Entry", "normal")
						app.setOptionBoxState("Grade", "normal")
						app.setOptionBoxState("Gender", "normal")
						app.setButtonState("Submit","normal")
					if faceId == []:
						warning()
						faceId_result = app.retryBox("Error", errorCapture)
						app.setLabelBg("Face_Detection","red")
						if (faceId_result == True):
							app.setEntryState("First_Name_Entry","normal")
							app.setEntryState("Last_Name_Entry","normal")
							app.setEntryState("Email_Entry","normal")
							app.setEntryState("PassCode_Entry", "normal")
							app.setOptionBoxState("Grade", "normal")
							app.setOptionBoxState("Gender", "normal")
							app.setButtonState("Submit","normal")
						else:
							app.stop()		
					else:		
						if candidates != []:
							warning()
							app.errorBox("Error", alreadyReg)
							open_register(btn)
					
						else:
							app.setLabelBg("Identify_Authentication","green")
							CreatePerson = CF.person.create(person_group_id, name=Name, user_data=grade)
							personId = (CreatePerson['personId'])
					
							AddToGroup = CF.person.add_face(img_url, person_group_id, personId, user_data=None,target_face=None)
							persistedfaceId = (AddToGroup['persistedFaceId'])
					
							CF.person_group.train(person_group_id)
					
							lcd.lcd_clear()
							lcd.lcd_display_string("Registration", 1)
							lcd.lcd_display_string("Completed!m", 2)
							sql = """INSERT INTO %s (Last_Name, First_Name, Date, Grade, personId, persistedFaceIds, Passcode, Admin, Email, Gender, Bonus_Points_Total, Bonus_Points_Current, Salt) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');""" % (table, LastName,FirstName,date, grade, personId, persistedfaceId, passcode, '0', email, gender,'0','1000',salt_gen)
							cursor.execute(sql)
							
							
							sql5 = """INSERT INTO %s (Date, User, Status) VALUES('%s', '%s', '%s');""" % (Log, date, Name, 'Register')
							cursor.execute(sql5)
							db.commit()
							
							strSubject = "PAS Stuco - Registration"
							strContent = "Hi, "+Name+"! Welcome to Stuco store system! Your account is now activated! \nOn "+date 
							sendGmailSmtp('stucopas@gmail.com','sciencefair',email,strSubject,strContent)
							sendGmailSmtp('stucopas@gmail.com','sciencefair',"stucopas@gmail.com",strSubject,strContent)
							open_register(btn)
	else:
		app.infoBox("Message","Please correct your information!")
		
"""-----------------------Register_Code-----------------------"""
app.addToolbar("Register",open_register,findIcon=True)

"""-----------------------Purchase_Functions-----------------------"""	
	
def open_purchase(btn):
	home_lcd()
	app.showToolbar()
	app.removeAllWidgets()
	app.setGeometry("500x420")
	app.addButton("Start Purchase", submit_purchase, 0, 0)
	app.setButtonAlign("Start Purchase", "center")
	app.startLabelFrame("Purchase")
	app.setSticky("new")
	app.addLabel("Face_Detection", "Face Detection", 1,0)
	app.setLabelSticky("Face_Detection","w")
	app.setLabelHeight("Face_Detection", 1)
	app.setLabelWidth("Face_Detection", 15)
	app.addLabel("Identify_Authentication","Authentication",1,1)
	app.setLabelSticky("Identify_Authentication","w")
	app.setLabelHeight("Identify_Authentication", 1)
	app.setLabelWidth("Identify_Authentication", 15)
	app.setLabelBg("Face_Detection","red")
	app.setLabelBg("Identify_Authentication","red")
	app.addLabel("User_Purchase_Label","Buyer: ",2,0)
	app.addLabel("User_Purchase","None",2,1)
	app.addLabel("AccountBalance_Purchase_Label","Account Balance: ",3,0)
	app.addLabel("AccountBalance_Purchase","0",3,1)
	app.addHorizontalSeparator(4,0,4, colour ="black")
	app.addLabel("Balance_Purchase_Label","TotalSpent: ",9,0)
	app.addLabel("Balance_Purchase","0",9,1)
	app.addHorizontalSeparator(8,0, colour ="black")
	app.addLabel("Discount_Purchase_Label"," -  Discount: ",7,0)
	app.setLabelSticky("Discount_Purchase_Label","w")
	app.addLabel("Discount_Purchase","0",7,1)
	app.addLabel("InCash_Purchase_Label","+ InCash: ",6,0)
	app.setLabelSticky("InCash_Purchase_Label","w")
	app.addLabel("InCash_Purchase","0",6,1)
	app.addLabel("FromAccount_Purchase_Label","    FromAccount: ",5,0)
	app.setLabelSticky("FromAccount_Purchase_Label","w")
	app.addLabel("FromAccount_Purchase","0",5,1)
	app.addHorizontalSeparator(10,0,4, colour ="black")
	app.addLabel("Total_Purchase_Account_Label","Account Balance: ",11,0)
	app.addLabel("Total_Purchase_Account","0",11,1)
	app.addButton("Calculate", Calculate, 12,1)
	app.setButtonState("Calculate","disabled")
	app.addLabel("Bonus_Point_Label","Bounus Point(s): ",13,0)
	app.addLabel("Bonus_Point","0",13,1)
	app.addLabel("Use","I want to use ",14,0)
	app.addEntry("Bonus_Point_Use",14,1)
	app.setEntryState("Bonus_Point_Use","disabled")
	app.setEntryWidth("Bonus_Point_Use",10)
	app.addLabel("Point(s)"," point(s)",14,2)
	app.addLabel("bonusvalue","1 Bonus Point = $",15,0)
	app.addLabel("bonusPointValue",bonusPointValue,15,1)
	app.stopLabelFrame()

def Calculate(btn):
	FromAccountTotal = 0
	InCashTotal = 0
	
	for i in range(counter):
		i = str(i)
		amount_calculate = app.getOptionBox("  Item "+i+":    Amount: ")
		paymethod_calculate = app.getOptionBox(i+":")
		itemprice_calculate = app.getLabel("Item"+i)
		
		itemprice_calculate = int(itemprice_calculate)
		if amount_calculate != "Cancel":
			amount_calculate = int(amount_calculate)
		if amount_calculate == "Cancel":
			amount_calculate = "0"
			amount_calculate = int(amount_calculate)	
			
		if(paymethod_calculate == "FromAccount"):			
			FromAccountTotal = FromAccountTotal + (itemprice_calculate*amount_calculate)
		if(paymethod_calculate == "InCash"):
			InCashTotal = InCashTotal + (itemprice_calculate*amount_calculate)
		
		i = int(i)
	Bonus_Points_use = app.getEntry("Bonus_Point_Use")
	Bonus_Points = app.getLabel("Bonus_Point")
	bonusPointValue = app.getLabel("bonusPointValue")
	if Bonus_Points_use == "" or Bonus_Points_use == " ":
		Bonus_Points_use = '0'
		Bonus_Points_use = int(Bonus_Points_use)
	Bonus_Points_use = int(Bonus_Points_use)
	Bonus_Points = int(Bonus_Points)
	if Bonus_Points_use > Bonus_Points or Bonus_Points_use < 0:
		app.errorBox("Error",errorBonusPoint)
	else:			
		BuyerBalance = app.getLabel("AccountBalance_Purchase")
		BuyerBalance = float(BuyerBalance)
		bonusPointValue = float(bonusPointValue)
		AfterPurchase =  BuyerBalance - FromAccountTotal+Bonus_Points_use*bonusPointValue
		TotalBalance = InCashTotal+FromAccountTotal-Bonus_Points_use*bonusPointValue
		discount = Bonus_Points_use*bonusPointValue
		if AfterPurchase < threshold:
			app.errorBox("Error","Insufficient fund! You can change your amount or pay in cash!")
		if Bonus_Points_use > 0 and FromAccountTotal == 0:
			app.errorBox("Error","You can only use bonus points by paying from account!")
		else:
			AfterAccount = FromAccountTotal - discount
			AfterPurchase = str(AfterPurchase)
			TotalBalance = str(TotalBalance)
			InCashTotal = str(InCashTotal)
			FromAccountTotal = str(FromAccountTotal)
			AfterAccount = str(AfterAccount)
			lcd.lcd_clear()
			lcd.lcd_display_string("Cash:"+InCashTotal, 1)
			lcd.lcd_display_string("Account:"+AfterAccount, 2)
			app.setLabel("InCash_Purchase", InCashTotal)
			app.setLabel("FromAccount_Purchase", FromAccountTotal)
			app.setLabel("Balance_Purchase", TotalBalance)
			app.setLabel("Total_Purchase_Account", AfterPurchase)	
			app.setLabel("Discount_Purchase", discount)
		
def submit_buy(btn):
	start_buy_time = time.time()
	FromAccountTotal = 0
	InCashTotal = 0
	for i in range(counter):
		i = str(i)
		amount_calculate = app.getOptionBox("  Item "+i+":    Amount: ")
		paymethod_calculate = app.getOptionBox(i+":")
		itemprice_calculate = app.getLabel("Item"+i)
		
		itemprice_calculate = int(itemprice_calculate)
		if amount_calculate != "Cancel":
			amount_calculate = int(amount_calculate)
		if amount_calculate == "Cancel":
			amount_calculate = "0"
			amount_calculate = int(amount_calculate)	
			
		if(paymethod_calculate == "FromAccount"):			
			FromAccountTotal = FromAccountTotal + (itemprice_calculate*amount_calculate)
		if(paymethod_calculate == "InCash"):
			InCashTotal = InCashTotal + (itemprice_calculate*amount_calculate)		
		i = int(i)
	Bonus_Points_use = app.getEntry("Bonus_Point_Use")
	Bonus_Points = app.getLabel("Bonus_Point")
	if Bonus_Points_use == "" or Bonus_Points_use == " ":
		Bonus_Points_use = '0'	
	Bonus_Points_use = int(Bonus_Points_use)
	Bonus_Points = int(Bonus_Points)
	bonusPointValue = app.getLabel("bonusPointValue")
	bonusPointValue = float(bonusPointValue)
	Bonus_Points_use_purchase = Bonus_Points - Bonus_Points_use
	if Bonus_Points_use > Bonus_Points or Bonus_Points_use < 0 or Bonus_Points_use_purchase < 0:
		app.errorBox("Error",errorBonusPoint)
	if Bonus_Points_use > 0 and FromAccountTotal == 0:
		app.errorBox("Error",errorBonusPayment)	
	if Bonus_Points_use_purchase >= 0 and Bonus_Points_use >= 0:
		BuyerBalance = app.getLabel("AccountBalance_Purchase")
		BuyerBalance = float(BuyerBalance)
		AfterPurchase =  BuyerBalance - FromAccountTotal+(Bonus_Points_use*bonusPointValue)
		TotalBalance = InCashTotal+FromAccountTotal
		InCashTotal = str(InCashTotal)
		FromAccountTotal = FromAccountTotal-Bonus_Points_use*bonusPointValue 
		bonusPointValue = str(bonusPointValue)
		FromAccountTotal = str(FromAccountTotal)
		AfterPurchase = str(AfterPurchase)
		Bonus_Points_use = str(Bonus_Points_use)
		Bonus_Points_use_purchase = str(Bonus_Points_use_purchase)
		lcd.lcd_clear()
		lcd.lcd_display_string("Please Confirm!", 1)
		time.sleep(1)
		lcd.lcd_clear()
		lcd.lcd_display_string("Cash:"+InCashTotal, 1)
		lcd.lcd_display_string("Account:"+FromAccountTotal, 2)
		Confirm_Purchase = app.yesNoBox("Please confirm your transaction!","You have to pay $"+InCashTotal+"(InCash) and $"+FromAccountTotal+"(FromAccount). Your leftover balance will be $"+AfterPurchase+".\n You use "+Bonus_Points_use+ " bonus point(s)! Your leftover bonus points will be "+Bonus_Points_use_purchase)
		if Confirm_Purchase == True:
			AfterPurchase = float(AfterPurchase)
			if AfterPurchase < threshold:
				warning()
				lcd.lcd_clear()
				lcd.lcd_display_string("  Insufficient ", 1)
				lcd.lcd_display_string("     fund!", 2)
				time.sleep(2)
				lcd.lcd_clear()
				lcd.lcd_display_string("Cash:"+InCashTotal, 1)
				lcd.lcd_display_string("Account:"+FromAccountTotal, 2)
				app.errorBox("Error","Insufficient fund! You should change your amount or pay in cash!")
			else:
				Transaction_Number = shortuuid.ShortUUID().random(length=6)
				Serial = "false"
				FromAccountTotal = 0
				InCashTotal = 0
				for i in range(counter):
					i = str(i)
					amount_calculate = app.getOptionBox("  Item "+i+":    Amount: ")
					paymethod_calculate = app.getOptionBox(i+":")
					itemprice_calculate = app.getLabel("Item"+i)
					result = app.getLabel("User_Purchase")
					itemname_sql = app.getLabel("itemname"+i)
					
					itemprice_calculate = int(itemprice_calculate)
					if amount_calculate != "Cancel":
						amount_calculate = int(amount_calculate)
					if amount_calculate == "Cancel":
						amount_calculate = "0"
						amount_calculate = int(amount_calculate)	
						
					if(paymethod_calculate == "FromAccount"):			
						Status = "Purchase (FromAccount)"
						balance = itemprice_calculate*amount_calculate
						ItemAmount = amount_calculate
						FromAccountTotal = FromAccountTotal + (itemprice_calculate*amount_calculate)
					if(paymethod_calculate == "InCash"):
						Status = "Purchase (InCash)"
						balance = itemprice_calculate*amount_calculate
						ItemAmount = amount_calculate
						InCashTotal = InCashTotal + (itemprice_calculate*amount_calculate)
										
					i = int(i)
					if Serial == "end" or Serial == "End":
						itemname_sql = None
					else:
						sql789 = """SELECT Serial_Number FROM %s WHERE Items_Name = '%s' """ % (Items, itemname_sql)
						cursor.execute(sql789)
						result789 = cursor.fetchall()
						Serial_Number = result789[0][0]
						sql = """INSERT INTO %s (Date,Status, User, Balance, Items, Items_Name, Amount, Single_Transaction, Transaction_Number) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s');""" % (Log, date, Status, result, balance, Serial_Number, itemname_sql, ItemAmount, i, Transaction_Number)
						cursor.execute(sql)
						db.commit()
				if counter == 0:
					lcd.lcd_clear()
					lcd.lcd_display_string("Buy something", 1)
					lcd.lcd_display_string("next time! ", 2)
					time.sleep(2)
					
				else:
					FromAccountTotal = int(FromAccountTotal)
					Bonus_Points_use = int(Bonus_Points_use)
					bonusPointValue = float(bonusPointValue)
					FromAccountTotal = FromAccountTotal-Bonus_Points_use*bonusPointValue
					InCashTotal = str(InCashTotal)
					FromAccountTotal = str(FromAccountTotal)
					Bonus_Points_use = str(Bonus_Points_use)
					bonusPointValue = str(bonusPointValue)
					Single_Transaction_Amount = "In Cash: "+InCashTotal+"\nFrom Account: "+FromAccountTotal+"\nUse Bonus Point: "+Bonus_Points_use+"\nBonus Point Value: "+bonusPointValue
					end_buy_time = time.time()
					global totaltime
					totaltime = totaltime_1+(end_buy_time - start_buy_time)
					totaltime = str(totaltime)
					sql2 = """INSERT INTO %s (Date, Single_Transaction_Amount, Identification_elapsed, Authentication_elapsed, Purchase_elapsed, Total_elapsed, Transaction_Number) VALUES('%s','%s','%s','%s','%s','%s','%s');""" % (Log, date, Single_Transaction_Amount, identify_elapsed, authentic_elapsed, purchasing_elapsed, totaltime,Transaction_Number)
					cursor.execute(sql2)	
					AfterPurchase = str(AfterPurchase)
					lcd.lcd_clear()
					lcd.lcd_display_string("Thank You!", 1)
					lcd.lcd_display_string("See u next time!", 2)
					lcd.lcd_clear()
					lcd.lcd_display_string("You now have", 1)
					lcd.lcd_display_string("$"+AfterPurchase, 2)
					time.sleep(2)
					lcd.lcd_clear()
					lcd.lcd_display_string(Bonus_Points_use_purchase, 1)
					lcd.lcd_display_string("bouns point(s)", 2)
					time.sleep(2)
					lcd.lcd_clear()
					lcd.lcd_display_string("in your account!", 1)
					time.sleep(1.2)
					app.infoBox("Message","Thank you for your purchase! The amount of transaction is $"+InCashTotal+"(InCash) and $"+FromAccountTotal+"(FromAccount). Your leftover balance is $"+AfterPurchase+".\nYou use "+Bonus_Points_use+ " bonus point(s)! Your leftover bonus points is "+Bonus_Points_use_purchase)
					sql10 = """UPDATE %s SET Balance = '%s' WHERE personId = '%s' """ % (table, AfterPurchase,personId)
					cursor.execute(sql10)
					sql101 = """UPDATE %s SET Bonus_Points_Current = '%s' WHERE personId = '%s' """ % (table, Bonus_Points_use_purchase, personId)
					cursor.execute(sql101)
					sql9 = """SELECT Email FROM %s WHERE personId = '%s' """ % (table, personId)
					cursor.execute(sql9)
					result9 = cursor.fetchall()
					email = result9[0][0]
					strSubject = "PAS Stuco - Purchase"
					strContent = "Hi, "+result+"! The amount of the transaction is $"+FromAccountTotal+"(From Account) and $"+InCashTotal+"(In Cash). Your account balance now is $"+AfterPurchase+".\nYou use "+Bonus_Points_use+ " bonus point(s)! Your leftover bonus points is "+Bonus_Points_use_purchase+". \nYour Transaction Number: "+Transaction_Number+" \nFor Details, see https://pasestore.com/Transaction.php \nOn "+date+"."
					sendGmailSmtp('stucopas@gmail.com','sciencefair',email,strSubject,strContent)
					sendGmailSmtp('stucopas@gmail.com','sciencefair',"stucopas@gmail.com",strSubject,strContent)
				
				db.commit()
				open_purchase(btn)
					
def submit_purchase(btn):
	start_purchase_time= time.time()
	app.hideToolbar()
	lcd.lcd_clear()
	lcd.lcd_display_string("Please look into", 1)
	lcd.lcd_display_string("the camera!", 2)
	app.setButtonState("Calculate","normal")
	app.setEntryState("Bonus_Point_Use","normal")
	app.setButtonState("Start Purchase","disabled")
	check_payment_method = False
	totalprice = 0
	amount = '0'
	global personId
	global result
	global ending
	global counter
	ending = False
	moremoney = 0
	row = 8
	height = 410
	counter = 0
	start_identify_time= time.time()
	while (amount == '0' ):	
		stream = io.BytesIO()
		with picamera.PiCamera() as camera:
			camera.resolution = (360, 270)
			camera.capture(stream, format='jpeg')	
		buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)	
		image = cv2.imdecode(buff, 1)	
		face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')	
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)	
		faces = face_cascade.detectMultiScale(gray, 1.1, 5)
		amount = str(len(faces))
		if str(len(faces)) == '0':
			warning_reco()
		elif str(len(faces)) != '0':
			cv2.imwrite( "/home/pi/Desktop/FacePython/identify.jpg",image)
			end_identify_time= time.time()
			correct()
			lcd.lcd_clear()
			lcd.lcd_display_string("The face has", 1)
			lcd.lcd_display_string("been detected!", 2)
			app.setLabelBg("Face_Detection","green")
			time.sleep(1)
			lcd.lcd_clear()
			lcd.lcd_display_string("Processing...", 1)
			
	img_url = "/home/pi/Desktop/FacePython/identify.jpg"
	person_group_id = 'pas'
	start_authentic_time= time.time()
	CreateFaceId = CF.face.detect("/home/pi/Desktop/FacePython/identify.jpg")
	if CreateFaceId == []:
		warning_auth()
		app.errorBox("Error", errorRecognize) 
		app.setLabelBg("Face_Detection","red")
		app.setButtonState("Start Purchase","normal")
		app.showToolbar()
	elif CreateFaceId != []:
		faceId = (CreateFaceId[0]["faceId"])
		identify = CF.face.identify([faceId] , person_group_id, max_candidates_return=1, threshold = 0.7 )
		candidates = (identify[0]["candidates"])
		if mutiFace == True:
			app.errorBox("Error", mutiface_mesg)
			app.showToolbar()
			app.setButtonState("Start Purchase","normal")
		if candidates == []:
			warning_auth()
			app.errorBox("Error", errorRecognize) 
			app.setLabelBg("Face_Detection","red")
			app.setButtonState("Start Purchase","normal")
			app.showToolbar()
		if candidates != []: 
			personId = (candidates[0]["personId"])
			confidence = (candidates[0]["confidence"])
			if confidence < 0.6:
				warning_auth()
				app.errorBox("Error", errorRecognize) 
				app.showToolbar()
				app.setLabelBg("Face_Detection","red")
				app.setButtonState("Start Purchase","normal")
			if confidence >= 0.6:
				end_authentic_time= time.time()
				app.setLabelBg("Identify_Authentication","green")
				getName = CF.person.get(person_group_id, personId)
				CF.person.add_face(img_url, person_group_id, personId, user_data=None,target_face=None)
				result = (getName["name"])
				sql100 = """SELECT Balance, Bonus_Points_Current, Bonus_Points_Total FROM %s WHERE personId = '%s' """ % (table, personId)
				cursor.execute(sql100)
				db.commit()
				result100 = cursor.fetchall()
				CurBalance = result100[0][0]
				global Bonus_Points_Current
				global Bonus_Points_Total
				Bonus_Points_Current = result100[0][1]
				Bonus_Points_Total = result100[0][2]
				OrignialBalance = result100[0][0]
				CurBalance = str(CurBalance)
				correct_auth()
				lcd.lcd_clear()
				lcd.lcd_display_string("Hi!"+result, 1)
				lcd.lcd_display_string("Account:"+CurBalance, 2)
				app.setLabel("User_Purchase", result)
				app.setLabel("AccountBalance_Purchase",CurBalance)
				app.setLabel("Bonus_Point",Bonus_Points_Current)
				start_purchasing_time = time.time()
				global Serial
				while ending == False:	
					Serial = raw_input("Click this windows!! Scan Your Item! ")
						
					sql = """SELECT Price, Serial_Number, Items_Name FROM %s WHERE Serial_Number = '%s'""" % (Items, Serial)
					cursor.execute(sql)
					item = cursor.fetchall()
					if Serial == "cancel":
						ans = app.yesNoBox("Confirm?","Cancel Transaction")
						if ans == True:
							if counter != 0:
								app.stopLabelFrame()
							open_purchase(btn)
							ending = True
					if Serial == "end" or Serial =="End":
						if counter == 0:
							height = height+50
							app.setGeometry(500, height)
							app.addButton("Buy", submit_buy,row+1,0)
							ending = True
						else:
							ending = True
							balance = 0	
							app.stopLabelFrame()
							height = height+65
							app.setGeometry(830, height)
							app.addButton("Buy", submit_buy,row+1,0)		
					if item == () and Serial != "end" and Serial != "cancel" and Serial !="End" :
						app.errorBox("Error", "Cannot find the item!") 
					if item != () and Serial !="end" and Serial != "cancel" and Serial != "End":
						if counter == 0:
							app.startLabelFrame("Items List")
						price = item[0][0]
						Serial_Number = item[0][1]
						itemname = item[0][2]	
						print itemname
						row = row + counter
						height = height+(14*counter)
						app.setGeometry(830, height)
						itemname = str(itemname)
						price = str(price)
						counter = str(counter)
						app.addLabelOptionBox(counter+":",["FromAccount","InCash"], row ,5)
						app.setSticky("w")
						app.addLabel("Payment_Method"+counter, "Payment Method", row ,4)
						app.setSticky("w")
						app.addLabelOptionBox("  Item "+counter+":    Amount: ",["1","2","3","4","5","6","7","8","9","10","11","12","13","15","16","17","18","19","20","Cancel"], row ,3)
						app.setSticky("w")
						app.addLabel("itemname"+counter, itemname, row ,2)
						app.setSticky("w")
						app.addLabel("Item"+counter, price, row ,1)
						app.setSticky("w")
						app.addLabel("moneysybol"+counter, "$", row ,0)
						app.setSticky("w")
						counter = int(counter)
						counter = counter + 1
				end_purchasing_time = time.time()
				end_purchase_time = time.time()
				global totaltime_1
				global identify_elapsed
				global authentic_elapsed
				global purchasing_elapsed
				purchasing_elapsed = end_purchasing_time - start_purchasing_time
				authentic_elapsed = end_authentic_time - start_authentic_time
				identify_elapsed = end_identify_time - start_identify_time
				totaltime_1 = (end_purchase_time - start_purchase_time)
				identify_elapsed = str(identify_elapsed)
				authentic_elapsed = str(authentic_elapsed)
				purchasing_elapsed = str(purchasing_elapsed)
				
				
"""-----------------------Purchase_Code-----------------------"""

app.addToolbar("Purchase",open_purchase,findIcon=True)

"""-----------------------Update_Functions-----------------------"""
def open_update(btn):
	home_lcd()
	app.removeAllWidgets()
	app.setGeometry("500x235")
	app.startLabelFrame("Update")
	app.setSticky("new")
	app.addLabel("email_update","Email: ", 0 ,0 )
	app.addEntry("email_entry",0,1)
	app.setSticky("new")
	app.setEntryDefault("email_entry","Email")
	app.setEntryWidth("email_entry",27)
	app.setFocus("email_entry")
	app.addLabel("Grade_update","Grade: ", 1,0 )
	app.setSticky("new")
	app.addLabelOptionBox("Grade",["1","2","3","4","5","6","7","8","9","10","11","12","Teacher"],1,1)
	app.addLabel("PassCode_Label","PassCode(Eg: 0000): ",2,0)
	app.setSticky("new")
	app.addSecretEntry("PassCode_Entry",2,1)
	app.setEntryDefault("PassCode_Entry","PassCode")
	app.addLabel("Face_Detection","Face Detection",3,0)
	app.addLabel("Identify_Authentication","Authentication",3,1)
	app.setLabelBg("Face_Detection","red")
	app.setLabelBg("Identify_Authentication","red")
	app.addButton("Submit",submit_update,4,0)
	app.stopLabelFrame()	

def submit_update(btn):
	
	email_update = app.getEntry("email_entry")
	passcode = app.getEntry("PassCode_Entry")
	grade = app.getOptionBox("Grade")
	person_group_id = 'pas'
	
	if (email_update == "" or passcode =="" or grade == ""):
		warning()
		app.errorBox("Error","Cannot be blank!")
	else:	
		sql = """SELECT personId, persistedFaceIds, Email, Active, Salt, Passcode, First_Name, Last_Name  FROM %s WHERE Email = '%s' && Grade = '%s'""" % (table, email_update, grade )
		cursor.execute(sql)
		result = cursor.fetchall()
		if result ==():
			warning()
			app.errorBox("Error","Incorrect Information!")
		elif result[0][3]==1:
			warning()
			app.errorBox("Error","Please use activate function to activate your account!")
		else: 
			if result !=():	
				salt = result[0][4]
				email = result[0][2]
				passcode_auth = result[0][5]
				FirstName = result[0][6]
				LastName = result[0][7]
				hash_pass = hashlib.sha256(salt+passcode).hexdigest()
				Name = FirstName + ' ' + LastName
				currentPath = "/home/pi/Desktop/FacePython/Photos/"
				folderPath = currentPath + Name + '/'
				img_url = folderPath + "update.jpg"
			
				if(hash_pass == passcode_auth and email_update==email):
					Active = result[0][3]
					email = result[0][2]
					app.setLabelBg("Identify_Authentication","green")
					lcd.lcd_clear()
					lcd.lcd_display_string("Please look into", 1)
					lcd.lcd_display_string("the camera!", 2)
					app.infoBox("Message","Please look into the camera!")
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
							warning_reco()
						elif str(len(faces)) != '0':
							if not os.path.exists(folderPath):
									os.makedirs(folderPath)
							cv2.imwrite( folderPath + "update.jpg",image)
							correct()
							lcd.lcd_clear()
							lcd.lcd_display_string("The face has", 1)
							lcd.lcd_display_string("been detected!", 2)
							time.sleep(1)
							lcd.lcd_clear()
							lcd.lcd_display_string("Processing...", 1)
					if Active == 1:
						strSubject = "PAS Stuco - Activation"
						strContent = "Hi, "+Name+"! Your account has been activated! \nOn "+date+"."
						CreateFaceId = CF.face.detect(img_url)
						if CreateFaceId == []:
							warning()
							lcd.lcd_clear()
							lcd.lcd_display_string("The lighting is", 1)
							lcd.lcd_display_string("not enough!", 2)
							time.sleep(3)
							open_update(btn)
						else:				
							faceId = (CreateFaceId[0]["faceId"])
							identify = CF.face.identify([faceId] , person_group_id, max_candidates_return=1, threshold = 0.7 )
							candidates = (identify[0]["candidates"])
							if mutiFace == True:
								warning()
								app.errorBox("Error", mutiface_mesg)
							if faceId == []:
								warning()
								faceId_result = app.errorBox("Error", errorCapture)
							else:		
								CreatePerson = CF.person.create(person_group_id, name=Name, user_data=grade)
								personId = (CreatePerson['personId'])
								AddToGroup = CF.person.add_face(img_url, person_group_id, personId, user_data=None,target_face=None)
								persistedfaceId = (AddToGroup['persistedFaceId'])
								CF.person_group.train(person_group_id)
								sql123123 = """UPDATE %s SET Active = '%s', personId = '%s' , persistedFaceIds = '%s' WHERE Last_Name = '%s' && First_Name = '%s' && passcode = '%s' && grade = '%s'""" % (table, '0',personId, persistedfaceId, LastName, FirstName, hash_pass, grade)
								cursor.execute(sql123123)
								db.commit()
								correct_update()		
								lcd.lcd_clear()
								lcd.lcd_display_string("Activation", 1)
								lcd.lcd_display_string("Completed!", 2)
								sendGmailSmtp('stucopas@gmail.com','sciencefair',email,strSubject,strContent)
								sendGmailSmtp('stucopas@gmail.com','sciencefair',"stucopas@gmail.com",strSubject,strContent)
								open_update(btn)		
					
					
					else:
						img_url = folderPath + "update.jpg"	
						CreateFaceId = CF.face.detect(folderPath + "update.jpg")
						if CreateFaceId == []:
							warning()
							app.errorBox("Error","There are more than 1 face in the image")
						else:
							person_id = result[0][0]
							persisted_face_id = result[0][1]
							AddToGroup = CF.person.add_face(img_url, person_group_id, person_id, user_data=None,target_face=None)
							persistedfaceId = (AddToGroup['persistedFaceId'])
							CF.person_group.train(person_group_id)
							sql2 = """UPDATE %s SET Active = '%s' ,persistedFaceIds = '%s' WHERE Last_Name = '%s' && First_Name = '%s' && Passcode = '%s' && Grade = '%s'""" % (table, '0',persistedfaceId, LastName, FirstName, passcode, grade )
							cursor.execute(sql2)
							result = cursor.fetchall()
							Status = "Update"
							sql5 = """INSERT INTO %s (Date, Status, User) VALUES('%s', '%s','%s');""" % (Log, date, Status, Name)
							cursor.execute(sql5)
							db.commit()
							strSubject = "PAS Stuco - Updating Data"
							strContent = "Hi, "+Name+"! Your facial recognition data has been updated! \nOn "+date+"."
							correct_update()		
							lcd.lcd_clear()
							lcd.lcd_display_string("Update", 1)
							lcd.lcd_display_string("Completed!", 2)
							sendGmailSmtp('stucopas@gmail.com','sciencefair',email,strSubject,strContent)
							sendGmailSmtp('stucopas@gmail.com','sciencefair',"stucopas@gmail.com",strSubject,strContent)
								
							open_update(btn)
				else:
					warning()
					app.errorBox("Error","Inccorect information")
				
					
			else:
				app.errorBox("Error","Inccorect information")
	
"""-----------------------Update_Code-----------------------"""
app.addToolbar("Update",open_update,findIcon=True)

"""-----------------------Deposit_Functions-----------------------"""

def open_deposit(btn):
	home_lcd()
	app.removeAllWidgets()
	app.setGeometry("500x300")
	app.addButton("Start Deposit",submit_deposit,0,0)
	app.startLabelFrame("Deposit")
	app.addLabel("Face_Detection_user","Face Detection - Buyer",2,0)
	app.addLabel("Identify_Authentication_user","Authentication - Buyer",2,1)
	app.setLabelBg("Face_Detection_user","red")
	app.setLabelBg("Identify_Authentication_user","red")
	app.addLabel("Identify_Authentication_sell","Authentication - Stuco Admin",4,0)
	app.setLabelBg("Identify_Authentication_sell","red")
	app.addLabel("buyer_deposit","Buyer: ",6,0)
	app.addLabel("buyer_depost_enter","None",6,1)
	app.addLabel("account_balance_deposit","Account Balance:",7,0)
	app.addLabel("account_balance_deposit_enter","0",7,1)
	app.addLabel("deposit_amount_deposit","Deposit Amount:",8,0)
	app.addEntry("Deposit_Amount_entry",8,1)
	app.addButton("Deposit", submit_deposit_check,9,0)
	app.setButtonState("Deposit","disabled")
	app.setEntryState("Deposit_Amount_entry","disabled")
	app.stopLabelFrame()

def submit_deposit(btn):
	global personIdU
	global AdminName
	global itemdeposit
	global resultN
	global balance
	ending = False
	amount = '0'
	person_group_id = "pas"
	app.setButtonState("Start Deposit","disabled")
	app.setEntryState("Deposit_Amount_entry","normal")
	app.setButtonState("Deposit","normal")
	lcd.lcd_clear()
	lcd.lcd_display_string("Please look", 1)
	lcd.lcd_display_string("into the camera!", 2)
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
			warning_reco()
		elif str(len(faces)) != '0':
			cv2.imwrite( "/home/pi/Desktop/FacePython/deposit.jpg",image)
			app.setLabelBg("Face_Detection_user","green")
			lcd.lcd_clear()
			correct()
			lcd.lcd_display_string("The face has", 1)
			lcd.lcd_display_string("been detected!", 2)
			time.sleep(1)
			lcd.lcd_clear()
			lcd.lcd_display_string("Processing...", 1)
			
	img_url = "/home/pi/Desktop/FacePython/deposit.jpg"
			
	CreateFaceId = CF.face.detect("/home/pi/Desktop/FacePython/deposit.jpg")
	if CreateFaceId == []:
		warning_auth()
		app.errorBox("Error",errorRecognize)
		open_deposit(btn)
	if CreateFaceId != []:
		faceId = (CreateFaceId[0]["faceId"])
		identify = CF.face.identify([faceId] , person_group_id, max_candidates_return=1, threshold = 0.7 )
		candidates = (identify[0]["candidates"])
		if candidates == []:
			warning_auth()
			app.errorBox("Error",errorRecognize)
			open_deposit(btn)
		if candidates != []:  
			personIdU = (candidates[0]["personId"])
			confidence = (candidates[0]["confidence"])
			if confidence < 0.6:
				warning_auth()
				app.errorBox("Error",errorRecognize) 
				open_deposit(btn)
			if confidence >= 0.6:
				getName = CF.person.get(person_group_id, personIdU)
				CF.person.add_face(img_url, person_group_id, personIdU, user_data=None,target_face=None)
				resultN = (getName["name"])
				sql1 = """SELECT Balance FROM %s WHERE personId = '%s'""" % (table, personIdU)
				cursor.execute(sql1)
				result = cursor.fetchall()
				balance = result[0][0]
				lcd.lcd_clear()
				correct_auth()
				lcd.lcd_display_string(resultN+"?", 1)
				respond = app.yesNoBox("Confirm?","Are you "+resultN+"?")
				if respond == False:
					open_deposit(btn)
				if respond == True:
					app.setLabelBg("Identify_Authentication_user","green")
					lcd.lcd_clear()
					lcd.lcd_display_string("Hi!", 1)
					lcd.lcd_display_string(resultN, 2)
					time.sleep(1.2)
					lcd.lcd_clear()
					lcd.lcd_display_string("Please wait...", 1)
					app.infoBox("Message",stucoPermission)
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
							warning_reco()
						elif str(len(faces)) != '0':
							cv2.imwrite( "/home/pi/Desktop/FacePython/admin.jpg",image)
							correct()					
							img_url = "/home/pi/Desktop/FacePython/admin.jpg"
							person_group_id = 'pas'
							CreateFaceId = CF.face.detect("/home/pi/Desktop/FacePython/admin.jpg")
							if CreateFaceId == []:
								app.errorBox("Error", errorRecognizeAdmin)
								open_deposit(btn)
							if CreateFaceId != []:
								faceId = (CreateFaceId[0]["faceId"])
								identify = CF.face.identify([faceId] , person_group_id, max_candidates_return=1, threshold = 0.7 )
								candidates = (identify[0]["candidates"])
								if candidates == []:
									app.errorBox("Error", errorRecognizeAdmin) 
									open_deposit(btn)
								if candidates != []:  
									personId = (candidates[0]["personId"])
									confidence = (candidates[0]["confidence"])
									if confidence < 0.6:
										app.errorBox("Error", errorRecognizeAdmin) 
										open_deposit(btn)
									if confidence >= 0.6:
										getName = CF.person.get(person_group_id, personId)
										sql2 = """SELECT Admin, First_Name, Last_Name FROM %s WHERE personId = '%s'""" % (table, personId)
										cursor.execute(sql2)
										result1 = cursor.fetchall()
										AdminFirstName = result1[0][1]
										AdminLastName = result1[0][2]
										AdminName = AdminFirstName + " " +AdminLastName
										tf = result1[0][0]
										 
										if tf == 1:
											lcd.lcd_clear()
											lcd.lcd_display_string("How much do you", 1)
											lcd.lcd_display_string("want to deposit?", 2)
											app.setLabelBg("Identify_Authentication_sell","green")
											app.infoBox("Message","Hello! Admin "+ AdminName) 
											app.setLabel("buyer_deposit","Buyer: ")
											app.setLabel("buyer_depost_enter",resultN)
											app.setLabel("account_balance_deposit","Account Balance:")
											app.setLabel("account_balance_deposit_enter",balance)
												
										else:
											warning()
											app.errorBox("Error","You do not have the permission to access!!")
											open_deposit(btn)
																												
				else:
					warning()
					app.errorBox("Error","Error! Please contact any Stuco members for further information!")
					open_deposit(btn)	

def submit_deposit_check(btn):
	item = app.getEntry("Deposit_Amount_entry")
	balance = app.getLabel("account_balance_deposit_enter")
	item = int(item)
	balance = int(balance)
	if item < 0:
		app.errorBox("Error","Error! Deposit cannot be negative!")
	else:
		totalbalanceitem = balance + item
		totalbalanceitem = str(totalbalanceitem)
		item = str(item)
		lcd.lcd_clear()
		lcd.lcd_display_string("Deposit $" + item+"?", 1)
		lcd.lcd_display_string("After:$" + totalbalanceitem, 2)
		result_ans = app.yesNoBox("Confirm","Hi, "+resultN+"! You will have "+totalbalanceitem+" after the deposit! Please Confirm!")
		balance = str(balance)
		if result_ans == True:
			submit_deposit_amount(btn)

def submit_deposit_amount(btn):
	item = app.getEntry("Deposit_Amount_entry")
	if item < 0:
		app.errorBox("Error","Error! Deposit cannot be negative!")
		open_deposit(btn)
	else:
		sql3 = """SELECT Balance, Bonus_Points_Total, Bonus_Points_Current FROM %s WHERE personId = '%s' """ % (table, personIdU)
		cursor.execute(sql3)
		result3 = cursor.fetchall()
		balanceB = result3[0][0]
		total_bonus = result3[0][1]
		current_bonus = result3[0][2]
		
		item = int(item)
		balanceB = int(balanceB)
		balance = balanceB + item
		total_bonus = total_bonus + item
		current_bonus = current_bonus + item
		
		sql4 = """UPDATE %s SET Balance = '%s' WHERE personId = '%s'""" % (table, balance, personIdU)
		cursor.execute(sql4)
		sql09 = """UPDATE %s SET Bonus_Points_Current = '%s' WHERE personId = '%s'""" % (table, current_bonus, personIdU)
		cursor.execute(sql09)
		sql099 = """UPDATE %s SET Bonus_Points_Total = '%s' WHERE personId = '%s'""" % (table, total_bonus, personIdU)
		cursor.execute(sql099)
		
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
		current_bonus = str(current_bonus)	
		correct_update()
		lcd.lcd_clear()
		lcd.lcd_display_string("Thank you!", 1)
		time.sleep(1)
		lcd.lcd_clear()
		lcd.lcd_display_string("You now have", 1)
		lcd.lcd_display_string(balanceA, 2)
		time.sleep(2)
		lcd.lcd_clear()
		lcd.lcd_display_string(current_bonus, 1)
		lcd.lcd_display_string("bouns point(s)", 2)
		time.sleep(2)
		lcd.lcd_clear()
		lcd.lcd_display_string("in your account!", 1)
		app.infoBox("Message","Thank You! "+ UN +"! You have "+ balanceA +" in your account! You now have "+current_bonus+" bonus point(s)!")
		db.commit()
	
		
		email = str(email)
		UN = str(UN)
		item = str(item)
		strSubject = "PAS Stuco - Deposit"
		strContent = "Hi, "+UN+", You have deposited $ "+item+". Your account balance is now "+ balanceA+". You now have "+current_bonus+" bonus point(s)! \nOn "+date
		sendGmailSmtp('stucopas@gmail.com','sciencefair',email,strSubject,strContent)
		sendGmailSmtp('stucopas@gmail.com','sciencefair',"stucopas@gmail.com",strSubject,strContent)
		ending = True
		open_deposit(btn)

"""-----------------------Deposit_Code-----------------------"""
app.addToolbar("Deposit",open_deposit,findIcon=True)

app.go()
