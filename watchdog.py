"""Realizați un script care să monitorizeze starea unui proces și să îl repornească dacă execuția
acestuia s-a oprit. Se poate configura intervalul de timp la care să fie verificată starea
procesului, cât și locația fișierului de log. Se va scrie în log orice modificare a stării procesului(dead / alive). ex: watchdog.py bitcoin_miner.exe 60 watchdog.log"""
import sys,time,os,subprocess

try:
	PROCESS_NAME=sys.argv[1]#the process that will be monitorized
	TIME=sys.argv[2]#in seconds
	LOGFILE=sys.argv[3]#the logfile that will be created and will write in it
except:#the default values, if user will not input anything
	PROCESS_NAME="Core Temp.exe"
	TIME="3"
	LOGFILE="watchdog.log"

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
#start process in windows


print(executeApp())
#parsarea outputului pentru a reusi sa luam PID-ul noului proces



