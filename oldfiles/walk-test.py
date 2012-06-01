import os
import sys
import re

print sys.argv, len(sys.argv)

cur = os.getcwd() if len(sys.argv)<2 else sys.argv[1]

def pat_serach(str):
#    print str, " : " , sys.argv[2]
    return re.search(sys.argv[2],str)

match = (lambda str: True) if len(sys.argv) < 3 else (lambda str: pat_serach(str))


print 'starting at ' + cur + ' ...'

for tup in os.walk(cur):
    dir, dirs, files = tup
    print dir
    for d in dirs[:]:
        #print "search(",os.path.join(dir,d), ",", sys.argv[2] , ")"
        if not match(os.path.join(dir,d)):
 #           print "not match"
            dirs.remove(d)
            
