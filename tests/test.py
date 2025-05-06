import os 
import procwrap

path = os.path.dirname(os.path.abspath(__file__)) 
file = open(path + "/sample_test1.in")
user_inputs = file.readlines()
file.close()

proc = procwrap.Observer([path + "/sample.exe"], user_inputs)
proc.start()
print("STDOUT:", proc.stdout)

proc.save(path + "/output.txt")