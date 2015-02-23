import subprocess
import time
import os
import signal
import sys
from sys import version_info

print "Batch greyscale conversion. Uses 'chomp-greyscale-to-cubical' to convert all files in a folder.\n"

py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2

if len(sys.argv) < 4:

	if py3:
		in_folder = input("Input folder? (e.g. 'plots' or 'files/imgs'): ")
		if not os.path.exists(in_folder):
			in_folder = input("That folder doesn't exist. Input folder? (e.g. 'plots'): ")
		out_folder = input("Where to output? (e.g. 'out') ")
		threshold = input("Threshold: ")
	  
	else:
		in_folder = raw_input("Input folder? (e.g. 'plots or 'files/imgs'): ")
		if not os.path.exists(in_folder):
			in_folder = raw_input("That folder doesn't exist. Input folder? (e.g. 'plots'): ")
		out_folder = raw_input("Where to output? (e.g. 'out') ")
		threshold = raw_input("Threshold: ")

else:
	in_folder = sys.argv[1]
	threshold = sys.argv[2]
	out_folder = sys.argv[3]

out_folder = out_folder + "_" + threshold # add threshold so i dont forget

if not os.path.exists(out_folder):
    os.makedirs(out_folder)

files = os.listdir(in_folder)
if '.DS_Store' in files:
	files.remove('.DS_Store')

print "Converting to greyscale...\n"
count = 1
for file in files:
	infile = "./"+in_folder+"/"+file
	outfile = "./"+out_folder+"/"+file[ :-4]+".txt" # file[ :-4] removes '.png'

	p = subprocess.call(["chomp-greyscale-to-cubical", infile, threshold, outfile])
	#p.communicate()
	#time.sleep(0.3)
	sys.stdout.write("\r Processing " + str(count) + " of " + str(len(files)) )
	sys.stdout.flush()
	# while not os.path.isfile(outfile):
# 		time.sleep(0.05)
# 	#p.kill()
# 	os.kill(p.pid, signal.SIGINT)
	count += 1
print "Done.\n"