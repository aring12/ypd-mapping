#!/usr/bin/python3
import os, glob

path = "/Users/Adin/Desktop/ypd mapping/YPD Crime Logs/2015/"
supp_files = glob.glob(os.path.join(path, "*p.pdf")) + glob.glob(os.path.join(path, "*p.PDF")) + glob.glob(os.path.join(path, "*p_A.PDF")) + glob.glob(os.path.join(path, "*p_A.pdf"))
a_files = glob.glob(os.path.join(path, "*a.pdf")) + glob.glob(os.path.join(path, "*a.PDF")) + glob.glob(os.path.join(path, "*A.pdf")) + glob.glob(os.path.join(path, "*A.PDF"))
b_files = glob.glob(os.path.join(path, "*b.pdf")) + glob.glob(os.path.join(path, "*b.PDF")) + glob.glob(os.path.join(path, "*B.pdf")) + glob.glob(os.path.join(path, "*B.PDF"))

# remove supps:
for f in supp_files:
	os.remove(f)

# remove old files and replace with updated
for f in a_files:
	name = str(f)
	l = len(name)
	front = name[:l-5]
	back = name[l-4:]
	new_name = front + back
	try:
		os.remove(new_name)
	except FileNotFoundError:
		print("no original{}".format(new_name))
	os.rename(name, new_name)

# remove old files and replace with updated in case of multiple updates
for f in b_files:
	name = str(f)
	l = len(name)
	front = name[:l-5]
	back = name[l-4:]
	new_name = front + back
	try:
		os.remove(new_name)
	except FileNotFoundError:
		print("no original{}".format(new_name))
	os.rename(name, new_name)