# Checks if the return(list(a=a,b=b)) is correctly specified.

checks_ok = 1
count = 0
infile = open("a","r")
data = infile.read().split(",")
infile.close()

for line in data:
    l = line.lstrip().rstrip()
    vars = l.split("=")
    count = count +1
    if (not(vars[0]==vars[1])):
        print "Error: these don't match",vars
        checks_ok = 0

if (checks_ok==1):
    print "Checked OK - ",count,"lines checked"
        
        

