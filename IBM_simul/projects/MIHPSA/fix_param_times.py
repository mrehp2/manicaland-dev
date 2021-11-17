import sys

timesfile = open("params/param_processed_patch0_times.csv","r")
timesdata = timesfile.readlines()
timesfile.close()

date_to_change = "2030.0"
new_date = "2042.0" # 2042 so have output for MIHPSA covering 2041.5.

# Check that 2030.0 appears in the file:
if not("".join(timesdata).find(date_to_change)):
    sys.exit(1)

outstring = timesdata[0]
for line in timesdata[1:]:
    splitline = line.split(" ")
    try:
        i_check = splitline.index(date_to_change)
    except:
        print("Current end_time=",splitline[3]," is not 2030.0. Please re-run with new date_to_change if needed. Exiting")
    if not(i_check==3):
        print("Error - the end_time should have index 3. Please check that the end_time in the original file is 2030.0")
        sys.exit(1)

    outstring += line.replace(date_to_change,new_date)
outstring = outstring.rstrip()
print(outstring)

print("Updating params/param_processed_patch0_times.csv")
timesfile = open("params/param_processed_patch0_times.csv","w")
timesfile.write(outstring)
timesfile.close()
