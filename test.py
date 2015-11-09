'''test.py
    This file is a unit testing module used in development purposes for validating changes made to the application backend.'''

import backend

def truthCheck(ret):
	if ret == True:
		return 'OK!'
	else:
		return 'Fail!'

print('Email uniqueness checker... ' + truthCheck(backend.emailAlreadyInUse('aleksey.bilogur@baruchmail.cuny.edu')))
# Need a testing method for the below.
# print(backend.addNewUser('ab', 'something', []))