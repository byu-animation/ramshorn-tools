import os
import sys
import glob
import time

'''
script to delete old ifds
takes a parameter specifying the threshold in days
author: Jeremy Oborn
'''

path = '/groups/owned/tmp/ifds/'
check = '*.ifd'
if len(sys.argv) < 2:
	days_old = 7
else:
	days_old = float(sys.argv[1])
delete_threshold = days_old * 24.0 * 60.0 * 60.0
to_glob = os.path.join(path, check);
print "deleting ifds in " + to_glob + " older than " + str(days_old) + " days"
deleted = 0
test = False
if os.path.exists(path):
	ifds = glob.glob(path + '*.ifd')
	now = time.time()
	for ifd in ifds:
		t = os.path.getmtime(ifd)
		c = os.path.getctime(ifd)
		# if not test:
		# 	print ifd
		# 	print "now " + str(now)
		# 	print "file " + str(t)
		# 	print "created " + str(c)
		# 	print "threshold " + str(delete_threshold)
		# 	print "difference " + str(now - t)
		# 	test = True
		if (now - t) > delete_threshold:
			os.remove(ifd)
			deleted = deleted + 1
else:
	print "bad filepath"

print "deleted " + str(deleted) + " ifds"