import sys

if(len(sys.argv)==1):
    print("Error - need to pass argument rounds or MIHPSA e.g. 1234567. Exiting\n")
    sys.exit(1)

if(sys.argv[1]=="MIHPSA"):
    impactfilename = "params/Calibration_mihpsa.csv"
    results_filename = "../RESULTS/Calibration_mihpsa.csv"
else:
    
    impactfilename = "params/Calibration_data_bestfits"+sys.argv[1]+".csv"
    results_filename = "../RESULTS/Calibration_data_bestfits"+sys.argv[1]+".csv"


impactfile = open(impactfilename,"r")
impactdata = impactfile.readlines()
impactfile.close()

results_file = open(results_filename,"r")
results_data = results_file.readlines()
results_file.close()

stripped_results_data = [",".join(l.split(",")[4:]) for l in results_data]
stripped_impactdata = [",".join(l.split(",")[2:]) for l in impactdata]


for line in stripped_results_data:
    try:
        stripped_impactdata.remove(line)
    except:
        print("Cannot find line",line)
        sys.exit(1)

if not(stripped_impactdata==[]):
    print("Error - two files do not match")
else:
    print("Files match OK")
