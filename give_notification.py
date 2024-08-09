from functions import *


Input1 = input("Send to? ")
Input2 = input("Head? ")
Input3 = input("Body? ") 
Input4 = input("Important? ")
Input5 = input("Image? ")

openDataFiles()
id, output, success = sendNotification(Input1, Input2, Input3, bool(Input4.lower()), Input5)
print(output)