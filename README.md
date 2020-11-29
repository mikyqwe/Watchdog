## This is a python 3.x project compatible only for Windows.
## To run this you need to have a 3.x version of Python installed. To check that, you have to open your cmd and to run this: 
python --version
## if the output is not Python 3.x you will need to download it: https://www.python.org/downloads/

## Usage:
[This script will take care of a process that you want. It will automatically restart it if the process is closed, and will write everything that he does in a .log file.]
## How to run it:
put the script in the same folder with the app you want to open
open your CMD
cd ...\Watchdog (change directory to the script)
py arg1 arg2 arg3 arg4
[arg1= watchdog.py]
[arg2=monitorized app's location.]  **You need "" if the app has spaces in its name**
[arg3=time in seconds when the script to check on the app]
[arg4=log file's name]
#example of input:			py watchdog.py bitcoin_miner.exe 60 watchdog.log