

'''Declaring some Global Variable'''
import sys

MESSAGE = "Message"
ERROR = "Error"
STATUS = "Status"
UPDATE_MESSAGE = "Record updated"
INSERT_MESSAGE = "Record inserted"
OPERATION = "Operation"
INFO = "info ================= "
ERROR_MSG = "error ================= "
SUCESS = "Request sucessfully completed"
CODE = "Error code"
ACTION = "Action"
LINE_NO = "Line_no"
SALES = "sales"
PURCHASES = "purchases"

def generateId(key,value):
    n = value # will be the last id from table
    str = key # will be the Preceding Word
    id = str+f'{n:05}'
    print("Generated id : ",id)
    return  id

def printLineNo():
    return str(format(sys.exc_info()[-1].tb_lineno))


def isnull(variable):
    if not variable or variable == '':
        return True
    else:
        return False

def whoami(request):
    username = request.user.username
    userid = request.user.id

    print("username :", username)
    print("id :", userid)
    return 0

def printCreate(module):
    return print(module," : created ")

def printUpdated(module):
    return print(module," : updated ")

def printDeleted(module):
    return print(module," : deleted ")




import random
import string

def get_random_alphaNumeric_string(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))


print(get_random_alphaNumeric_string())