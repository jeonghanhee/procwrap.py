# procwrap.py
This is a library that uses subprocess to automatically capture the complete output.

### Examples include.
```py
import os 
import procwrap

path = os.path.dirname(os.path.abspath(__file__)) 
file = open(path + "/sample_test1.in") # this is input file.
user_inputs = file.readlines() # The type is a list, and each element must end with a "\n".
file.close()

proc = procwrap.Observer([path + "/sample.exe"], user_inputs) # test
proc.start() # essential!!
print("STDOUT:", proc.stdout) # print stdout.

proc.save(path + "/output.txt") # save to a file :)
```

### How do I install it?
Since it's not an official library, it needs to be installed in development mode. XD
<br />
Please type the command exactly as shown below!

In project: 
```shell
pip install -e .
```
<br/>
Download to Github:
```shell
pip install git+https://github.com/jeonghanhee/procwrap.py.git
```
<br/>
Then you'll be able to use it!
