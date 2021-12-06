# Script to move files from e.g. run1 to run2.

# Used when I am generating dummy data for calibration and need 2 or more RESULTS directories

import os
import shutil
import glob

csvfiles = glob.glob("*.csv")


oldrun=1
newrun=2

oldrunname = "Rand"+str(oldrun)
newrunname = "Rand"+str(newrun)

for oldfilename in csvfiles:
    if oldfilename.find(oldrunname)>=0:
        newfilename = oldfilename.replace(oldrunname,newrunname)
        print oldfilename,newfilename
        os.rename(oldfilename, newfilename)
