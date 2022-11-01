import sys
import os
import subprocess as sp
import time
import datetime

def Recovery(Output_file):

	process=sp.Popen('/u01/app/oracle/product/19.0.0/dbhome_1/bin/rman target /',stdin=sp.PIPE,env=os.environ.copy(),stderr = sp.PIPE, stdout=Output_file,shell=True)

	process.stdin.write(b"shutdown immediate;\n")
	process.stdin.flush()

	process.stdin.write(b"startup mount;\n")
	process.stdin.flush()

	process.stdin.write(b"catalog start with '/home/oracle/oracle_backed_up1' noprompt;\n")
	process.stdin.flush()

	process.stdin.write(b"restore database;\n")
	process.stdin.flush()

	process.stdin.write(b"run{\n")
	process.stdin.write(b"allocate channel ch00 type SBT_TAPE\n")
	process.stdin.write(b"PARMS='SBT_LIBRARY=/usr/openv/netbackup/bin/libobk.so64';\n")
	process.stdin.write(b"recover database;\n")
	process.stdin.write(b"release channel ch00;\n")
	process.stdin.write(b"}\n") 
	process.stdin.flush() 


	process.stdin.write(b"alter database open;\n")
	process.stdin.flush()

	process.stdin.write(b"exit\n")
	process.stdin.flush() 	
	
	process.wait()
	result = process.communicate() 
	if result !=0:
		return False 
	else:
		return True 
def main():


	rmanCMD = '/u01/app/oracle/product/19.0.0/dbhome_1/bin/rman target /'
	FILENAME="Recovery_DB" + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '_') + ".output"
	Output_file=open(FILENAME, "w")
	print ("Starting Oracle Recovery...")
	Flag = Recovery(Output_file) 
	if Flag:
		print ("Recovery Operations Done")
	else:
		print ("Check Logs for Error")


if __name__ == "__main__":
        main()


