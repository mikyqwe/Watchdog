"""
Author: Formagiu Michael-Gabriel
This script will be a watchdog(will open it and will make sure it stays up) for an other process.
"""
import sys,time,os,subprocess,logging

def configLogger():
	"""In here I will config how log file's format"""
	if(os.path.exists(LOGFILE)):
		os.remove(LOGFILE)
	date_strftime_format = "%d-%b-%y %H:%M:%S"
	logging.basicConfig(filename=LOGFILE, level=logging.INFO,format='%(asctime)s:%(message)s',datefmt=date_strftime_format)

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

def is_number(s):
	"""This function checks if a string can be a float number."""
	try:
		float(s)
		return True
	except:
		return False

#less arguments than needed
if (len(sys.argv)<4):
	LOGFILE="watchdog.log"
	configLogger()
	logging.info(' {} arguments are not enough. To run the script you need 4 arguments [script name],[app name],[check cooldown],[logfile name].'.format(len(sys.argv)))
	exit()

PROCESS_NAME=sys.argv[1]#the process that will be monitorized
#app not found at given location
if os.path.exists(PROCESS_NAME)==False:
	logging.info(' The app with the name: {} could not be found. The script will stop now.'.format(PROCESS_NAME))
	exit()

TIME=sys.argv[2]#in seconds
#the argument for time is not in seconds, as needed
if is_number(TIME)==False:
	logging.info(' The time given as input: "{}" can not be converted to a number. The script will stop now.'.format(TIME))
	exit()

LOGFILE=sys.argv[3]#the logfile that will be created and will write in it
configLogger()

PID=executeApp()#we execute the app for the first time
logging.info(' {} first started with the PID: {}'.format(PROCESS_NAME,PID))
while True:
	time.sleep(int(TIME))
	if alive(PID) == False:
		logging.info(' {} with the PID: {} is not alive anymore. Soon it will start back.'.format(PROCESS_NAME,PID))
		PID=executeApp()
		logging.info(' {} came back from the dead. The new PID is: {}'.format(PROCESS_NAME,PID))
