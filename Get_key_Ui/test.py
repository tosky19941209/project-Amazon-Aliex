import os, sys
import hashlib
import datetime
import hashlib
import time
import hmac
hash_key = 'tlkwjdqhd'

def hash_message_with_key(message, key):
    # Combine the message and key
    message_with_key = message + key

    # Create a new hash object using SHA-256 algorithm
    hash_object = hashlib.sha256(message_with_key.encode())

    # Get the hexadecimal representation of the hash
    hashed_message = hash_object.hexdigest()

    return hashed_message

# def check_activation(token):
# 	serialnumber = getMachine_addr()
# 	serial_number = serialnumber[12:len(serialnumber)]
# 	machine_number = hash_message_with_key(serial_number, hash_key)
# 	if (token == machine_number):
# 		return "yes"
# 	else:
# 		return "no"



# now = time.time()
# dt = datetime.datetime.fromtimestamp(now)
# date_str = str(dt)
date_str = '2024-03-12'

machine_number_input = 'YEKSHOW'
serial_number = hash_message_with_key(machine_number_input + date_str, hash_key)
print(serial_number)