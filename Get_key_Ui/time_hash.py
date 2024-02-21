import jwt
key='super-secret'
machinenumber = 'YLX3ATND'
payload={"time":"2024-01-30","machinenumber":machinenumber }
token = jwt.encode(payload, key)
print (token)
decoded = jwt.decode(token, options={"verify_signature": False}) # works in PyJWT >= v2.0
print (decoded)
print (decoded["time"])