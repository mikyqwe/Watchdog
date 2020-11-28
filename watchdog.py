"""Realizați un script care să monitorizeze starea unui proces și să îl repornească dacă execuția
acestuia s-a oprit. Se poate configura intervalul de timp la care să fie verificată starea
procesului, cât și locația fișierului de log. Se va scrie în log orice modificare a stării procesului(dead / alive). ex: watchdog.py bitcoin_miner.exe 60 watchdog.log"""
import sys,time,os,subprocess,logging

try:
	PROCESS_NAME=sys.argv[1]#the process that will be monitorized
	TIME=sys.argv[2]#in seconds
	LOGFILE=sys.argv[3]#the logfile that will be created and will write in it
except:#the default values, if user's input will not be good.
	PROCESS_NAME="Core Temp.exe"
	TIME="3"
	LOGFILE="watchdog.log"

def configLogger():
	os.remove(LOGFILE)
	date_strftime_format = "%d-%b-%y %H:%M:%S"
	logging.basicConfig(filename=LOGFILE, level=logging.INFO,format='%(asctime)s:%(message)s',datefmt=date_strftime_format)
configLogger()

def getPID(s):
	"""This function will get the pid of the app we just opened given a string with the specific format of windows cmd's 'tasklist'."""
	while " " in s:#stergem toate spatiile din text (pot fi spatii multiple)
		s=s.replace(' ','')
	s=s.split("PID:")#facem un split dupa PID: pentru ca fiecare element a lui b sa inceapa cu PID-ul procesului
	pidWanted=s[-1]
	pidWanted=pidWanted.split("SessionName")
	return pidWanted[0][0:len(pidWanted[0])-4]

def executeApp():
	"""This function will execute the app we want and will return its PID"""
	command='start "" "'+PROCESS_NAME+'"' #command to start the process_name in windows cmd
	subprocess.run(command,shell=True)
	command='tasklist /fi "IMAGENAME eq '+PROCESS_NAME+'" /fo list'
	return getPID(str(subprocess.run(command,shell=True,capture_output=True)))

def alive(PID):
	"""This function will check wether a process is alive or not by its PID."""
	command='tasklist /fi "PID eq '+PID+'" /fo list'
	cmd_output=subprocess.run(command,shell=True,capture_output=True)
	count=str(cmd_output).count(str(PID))#in cmd_output we will have the whole output that is something like: 'For the PID: X we have found the next matches: PID:X name: y...'=>X=2 if there are matches, if there are not matches the output will be: 'For the PID: X we have found the next matches:'-> 1 match
	if count==2:#so now we will see if X=2 or X=1, to see if the process alive or not
		return True
	else:
		return False

PID=executeApp()#we execute the app for the first time
logging.info(' {} first started with the PID: {}'.format(PROCESS_NAME,PID))
while True:
	time.sleep(int(TIME))
	if alive(PID) == False:
		logging.info(' {} with the PID: {} is not alive anymore. Soon it will start back.'.format(PROCESS_NAME,PID))
		PID=executeApp()
		logging.info(' {} came back from the dead. The new PID is: {}'.format(PROCESS_NAME,PID))

#




