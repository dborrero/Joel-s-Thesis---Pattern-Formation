# numfix.py

import os
import subprocess
from sys import argv

folder = argv[1]

files = os.listdir(folder)

if '.DS_Store' in files:
	files.remove('.DS_Store')

for file in files:
	step = file.split('-')[1].split('.')[0] #gets just the digits
	if len(step) == 3:
		step = '0' + step
		newname = file.split('-')[0]+'-'+step+'.'+file.split('.')[1]
		subprocess.Popen(['mv', folder+'/'+file, folder+'/'+newname])
