import subprocess
import time
import os
import signal
import sys
from sys import version_info

print "Homology batch script. Runs 'chomp-cubical' on each file in the input folder outputs to file with name of first file.\n"

py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2

if len(sys.argv) < 3:

	if py3:
		in_folder = input("Input folder for txt files?")
		if not os.path.exists(in_folder):
			in_folder = input("That folder doesn't exist. Input folder? (e.g. 'plots'): ")
		out_file = input("Output filename?: ")
	  
	else:
		in_folder = raw_input("Input folder? (e.g. 'plots or 'files/imgs'): ")
		if not os.path.exists(in_folder):
			in_folder = raw_input("That folder doesn't exist. Input folder? (e.g. 'plots'): ")
		out_file = raw_input("Output filename?: ")

else:
	in_folder = sys.argv[1]
	out_file = sys.argv[2]

files = os.listdir(in_folder)
if '.DS_Store' in files:
	files.remove('.DS_Store')

files = sorted(files) # make sure the list is sorted!

resultsName = out_file + ".csv"

if os.path.isfile(resultsName):
	resultsName = resultsName[ :-4] + "_1.csv" # remove .csv and add _1.csv
	
subprocess.call(["touch",resultsName])

count = 1

print "Analyzing homology...\n"

resultsFile = open(resultsName, 'r+')
resultsFile.write('name-step,betti-0,betti-1,betti-2 \n')

for file in files:
	p = subprocess.Popen(["chomp-cubical","./"+in_folder+"/"+file], stdout=subprocess.PIPE)
	output, err = p.communicate()
	# want to print csv: STEP,b0,b1,b2
	# where STEP is the time step e.g. 004 or 326 (3 digits, out of 500 steps, could be more)
	# chomp-cubical gives e.g. 'Betti Numbers: 5 16 0'
	bettis = output.split()[-3: ] # gets ['5', '16', '0']
	bettisStr = bettis[0]+','+bettis[1]+','+bettis[2]
	# file is the input filename, e.g. 'theta-491.png.txt'
	tStep = file.split('.')[0] # 'theta-491'
	sys.stdout.write("\r Processing " + str(count) + " of " + str(len(files)) + " | " + tStep + ': ' + bettisStr)
	sys.stdout.flush()
	count += 1
	resultsFile.write(tStep + ',' + bettisStr + '\n')

resultsFile.write('\n')
resultsFile.close()
sys.stdout.write("\n")
print "Results saved in " + resultsName
