import sys, re, os, glob

# Uses Calibration_MIHPSA.csv outputs from a bunch of runs to find the best one.

results_rootdir = "RESULTS/"



def get_results_dirs(results_root_dir):
    possible_results_dirs = [x[0] for x in os.walk(results_root_dir)]
    # Now check that these are of the form "..../RESULTSX":
    checked_dirs = []
    pattern = re.compile("^(RESULTS[1-9]*[0-9]*)")
    for dir in possible_results_dirs:
        string_to_check = dir.split("/")[-1]
        if pattern.match(string_to_check):
            checked_dirs += [dir]
    checked_dirs.sort()
    return checked_dirs




def get_header_indices(infile):
    mihpsa_header_tempfile = open(infile,"r")
    mihpsa_header = mihpsa_header_tempfile.readlines()[0].split(",")
    mihpsa_header_tempfile.close()
    i_filename = mihpsa_header.index("Filename")
    i_loglikelihood = mihpsa_header.index("Log_likelihood\n")
    return [i_filename,i_loglikelihood]


files = []
likelihoods = []

resultsdirs = get_results_dirs(results_rootdir)

[i_filename,i_loglikelihood] = get_header_indices(resultsdirs[0]+"/Output/Calibration_MIHPSA.csv")



for dir in resultsdirs:
    mihpsa_calibration_file = open(dir+"/Output/Calibration_MIHPSA.csv","r")
    mihpha_run_data = mihpsa_calibration_file.readlines()[1:]
    for line in mihpha_run_data:
        splitline = line.split(",")
        likelihoods += [float(splitline[i_loglikelihood])]
        files += [splitline[i_filename]]



n = 10
top_n =  sorted(range(len(likelihoods)), key=lambda x: likelihoods[x])[-n:]


outstring = ""
for (n,i) in enumerate(top_n):
    i_rep = files[i].split("_")[-1].split(".csv")[0]
    i_seed = files[i].split("Rand")[-1].split("_")[0]
    i_run = str(int(files[i].split("Run")[-1].split("_")[0]))
    outstring +=  i_seed+"_"+i_rep+" "+i_run+" "+str(likelihoods[i]) +"\n"


    print "Opening "+results_rootdir+"RESULTS"+str(i_seed)
    calibration_file = open(results_rootdir+"RESULTS"+str(i_seed)+"/Output/Calibration_output_CL05_Zim_patch0_Rand"+str(i_seed)+"_0.csv","r")
    calibration_file_data = calibration_file.readlines()

    # Add header:
    if(n==0):
        calibration_string = calibration_file_data[0]
    
    calibration_string += calibration_file_data[int(i_run)]
    calibration_file.close()



outfile = open(results_rootdir+"/goodfits_mihpsa.txt","w")
outfile.write(outstring)
outfile.close()

outfile_calibration = open(results_rootdir+"/Calibration_mihpsa.csv","w")
outfile_calibration.write(calibration_string)
outfile_calibration.close()

print [files[i] for i in top_n]


