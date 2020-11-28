"""Realizați un script care să monitorizeze starea unui proces și să îl repornească dacă execuția
acestuia s-a oprit. Se poate configura intervalul de timp la care să fie verificată starea
procesului, cât și locația fișierului de log. Se va scrie în log orice modificare a stării procesului(dead / alive). ex: watchdog.py bitcoin_miner.exe 60 watchdog.log"""
import sys,time


try:
	PROCESS_NAME=sys.argv[1]#the process that will be monitorized
	TIME=sys.argv[2]#in seconds
	LOG_FILENAME=sys.argv[3]#the logfile that will be created and will write in it
except:#the default values, if user will not input anything
	PROCESS_NAME="metin2client.exe"
	TIME="3"
	LOG_FILENAME="watchdog.log"

#while True:
#	#DO WORK
#	sleep(TIME)

