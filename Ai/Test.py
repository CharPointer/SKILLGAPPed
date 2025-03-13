import time
import sys

print("hello")

time.sleep(5)

if (sys.argv[1] == "0"):
    raise Exception("Sorry 0") 


if (int(sys.argv[1])%2 == 0):
    raise Exception("Sorry, no numbers below zero") 

print("Bye")