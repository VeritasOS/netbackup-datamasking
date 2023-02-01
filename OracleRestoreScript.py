import sys
import os
import subprocess as sp
import time
import datetime

def Recovery(Output_file,mountpath,PARAMcmd):
	catalog = "catalog start with {0} noprompt;\n".format(mountpath)
	catalog = bytes(catalog,encoding='utf-8')	
	
	process=sp.Popen('$ORACLE_HOME/bin/rman target /',stdin=sp.PIPE,env=os.environ.copy(),stderr = sp.PIPE, stdout=Output_file,shell=True)

	process.stdin.write(b"shutdown immediate;\n")
	process.stdin.flush()

	process.stdin.write(b"startup mount;\n")
	process.stdin.flush()

	process.stdin.write(catalog)
	process.stdin.flush()

	process.stdin.write(b"restore database;\n")
	process.stdin.flush()

	process.stdin.write(b"run{\n")
	process.stdin.write(b"allocate channel ch00 type SBT_TAPE\n")
	process.stdin.write(PARAMcmd)
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

def check_nbu_dir():
	cmd = "[ -d /usr/openv/netbackup ]"
	p1 = sp.Popen(cmd,stdin=sp.PIPE,env=os.environ.copy(),stderr = sp.PIPE, stdout=sp.PIPE,shell=True)
	p1.wait()
	
	if p1.returncode == 0:
		print ("Netbackup Exists")
		PARAMcmd =bytes( "PARMS='SBT_LIBRARY=/usr/openv/netbackup/bin/libobk.so64';\n",encoding='utf-8')
		return PARAMcmd, True

	else:
		print ("Netbackup doesnt Exist on this Machine")

	return None, False
