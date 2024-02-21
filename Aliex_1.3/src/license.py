import os, sys
import hashlib
import jwt
import time
import datetime
def getMachine_addr():
	os_type = sys.platform.lower()
	if "win" in os_type:
		command = "wmic bios get serialnumber"
	elif "linux" in os_type:
		command = "hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid"
	elif "darwin" in os_type:
		command = "ioreg -l | grep IOPlatformSerialNumber"
	return os.popen(command).read().replace("\n","").replace("	","").replace(" ","")

def life_time_token(str_time):
	year_contract = int(str_time[0:4])
	month_contract = int(str_time[5:7])
	day_contract = int(str_time[8:10])


	now = time.time()
	dt = datetime.datetime.fromtimestamp(now)
	date_now = str(dt)

	year_now = int(date_now[0:4])	
	month_now = int(date_now[5:7])
	day_now = int(date_now[8:10])
	
	if year_contract > year_now:
		return "yes"
	elif year_contract == year_now:
		if month_contract > month_now:
			return "yes"
		elif month_contract == month_now:
			if day_contract >= day_now:
				return 'yes'
			else:
				return 'no'		

def check_activation(token):

	token_state = True
	key='tlkwjdqhd'
	# machinenumber = 'KEHOWR'
	# payload={"time":"2023-01-23","machinenumber":machinenumber }
	try:
		decoded = jwt.decode(token, options={"verify_signature": False}) # works in PyJWT >= v2.0
	except jwt.exceptions.DecodeError:
		token_state = False

	if token_state == True:
		machine_number = getMachine_addr()
		machine_number = machine_number[12:len(machine_number)]
		life_time_token(decoded['time'])
		if(decoded['machinenumber'] == machine_number):
			if(life_time_token(decoded['time']) == 'yes'):
				json = {"time":decoded['time'], "machinenumber":decoded['machinenumber']}
				newtoken = jwt.encode(json, key)
				if newtoken == token:
					return 'yes'
			else:
				return "notime"
		else:
			return 'incorrect'		
