# Code modifies the end_time_simul parameter in the file paramfile.
# Allows simulation to run for longer.

import sys

date_to_change = "2030.0"
new_date = "2042.0" 


paramfile = "params/param_processed_patch0_times.csv"
timesfile = open(paramfile,"r")
timesdata = timesfile.readlines()
timesfile.close()


# Check that "date_to_change" appears in the file:
if not("".join(timesdata).find(date_to_change)):
    sys.exit(1)

outstring = timesdata[0]

try:
    i_check = timesdata[0].split(" ").index("end_time_simul")
except:
    print("Error - could not find end_time_simul in",paramfile)
    sys.exit(1)


# Check all the times are the same - and either the original or new time:
file_value1 = timesdata[1].split(" ")[i_check]
if not(file_value1 in [date_to_change,new_date]):
    print(f"Error - current value of end_time_simul in file is {file_value1}. Exiting")
    sys.exit(1)

for line in timesdata[1:]:
    splitline = line.split(" ")
    if (splitline[i_check]==file_value1):
        if(splitline[i_check]==date_to_change):
            outstring += line.replace(date_to_change,new_date)
    else:
        print(f"Error - values of end_time_simul in file varies. Please check file. Exiting")
        sys.exit(1)
    


# Only update file if needed:
if (file_value1==date_to_change):
    #outstring = outstring.rstrip()
    #print(outstring)


    print(f"Updating {paramfile}")
    timesfile = open(paramfile,"w")
    timesfile.write(outstring)
    timesfile.close()
