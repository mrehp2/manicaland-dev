import glob,sys,os
import shutil   # For copying files

#CALIBRATION_TYPE="MIHPSA"
#CALIBRATION_TYPE="R7"
CALIBRATION_TYPE="R1-7"
#CALIBRATION_TYPE="R67"
#CALIBRATION_TYPE="TARGETMIHPSA"
#CALIBRATION_TYPE="LIKELIHOOD" # Uses likelihood_fit_Manicaland.py to get 10 highest likelihood runs (grouped into 15-24F, 25-54F, 15-29M, 30-54M outcomes)
#CALIBRATION_TYPE="TARGETPICK" # Uses pick_target_fits_Manicaland.py to target-fit to some outcomes
#CALIBRATION_TYPE="DISTANCE"
dir_root = "RESULTS/"

if(CALIBRATION_TYPE=="MIHPSA"):
    output_dir = "./IMPACT_MIHPSAFIT/params/"
    goodfits_file = "goodfits_mihpsa.txt"
    offset = 0
elif(CALIBRATION_TYPE=="TARGETMIHPSA"):
    output_dir = "./IMPACT_TARGETMIHPSA/params/"
    goodfits_file = "targetfits_MIHPSA.txt"
    offset = 0
elif(CALIBRATION_TYPE=="R7"):
    output_dir = "./IMPACT_R7/params/"
    goodfits_file = "goodfits7.txt"
    offset = 1
elif(CALIBRATION_TYPE=="R67"):
    output_dir = "./IMPACT_R67/params/"
    goodfits_file = "goodfits67.txt"
    offset = 1
elif(CALIBRATION_TYPE=="R1-7"): # Rounds 1-7
    output_dir = "./IMPACT_R1R7/params/"
    goodfits_file = "goodfits1234567.txt"
    offset = 1
elif(CALIBRATION_TYPE=="LIKELIHOOD"): 
    output_dir = "./IMPACT_LIKELIHOOD/params/"
    goodfits_file = "likelihood_Manicaland.txt"
    offset = 0
elif(CALIBRATION_TYPE=="TARGETPICK"):
    output_dir = "./IMPACT_TARGETPICK/params/"
    goodfits_file = "goodfits_targetpick.txt"
    offset = 0
elif(CALIBRATION_TYPE=="DISTANCE"):
    output_dir = "./IMPACT_DISTANCE/params/"
    goodfits_file = "distance_Manicaland.txt"
    offset = 0
else:
    print "Error: unknown calibration_type. Exiting"
    sys.exit(1)
    

if(not(os.path.isdir(output_dir))):
    try:
        os.makedirs(output_dir)
    except:
        print "Error - need to make directory ",output_dir
        sys.exit()

        
likelihood_fits_file = open(dir_root+"/"+goodfits_file,"r")
likelihood_fits_data = likelihood_fits_file.read().splitlines()
likelihood_fits_file.close()

# [Directory number, run number]
run_dir_numbers = [[x.split()[0].replace("_0",""),x.split()[1]] for x in likelihood_fits_data]

#directories = [ for x in likelihood_fits_data]


# This will store the output for each param.csv file.
# The keys are the filenames
output_string = {}


# run_dir is a pair of numbers - the directory (run_dir[0]) and the run number (run_dir[1]):
for run_dir in run_dir_numbers:
    param_dir = dir_root+"/RESULTS"+run_dir[0]+"/"

    lhc_file_list = glob.glob(param_dir+"param_processed_*.csv")

    full_file_list = glob.glob(param_dir+"*.*")

    # Files that also need to be copied:
    remaining_file_list = list(set(full_file_list)-set(lhc_file_list))

    # These files also need to be copied (but due to names we add/remove them from the lists by hand):
    exception_files = [param_dir+"param_processed_patch0_fertility.csv",param_dir+"param_processed_patch0_mortality.csv",param_dir+"param_processed_patch0_mtct.csv"]

    remaining_file_list += exception_files
    for f in exception_files:
        lhc_file_list.remove(f)

    
    
    # Copy these files (if this is the first one in the list):
    if (run_dir==run_dir_numbers[0]):
        for f in remaining_file_list:
            f_name = f.split("/")[-1]
    
            #print output_dir+f_name
            shutil.copy(f,output_dir+f_name)


    # Now pull the lines from each
    for f in lhc_file_list:
        infile = open(f,"r")
        params = infile.read().splitlines()
        infile.close()

        # This is the filename (i.e. removing directory)
        f_name = f.split("/")[-1]

        # Add header if this is the first one in the list:
        if (run_dir==run_dir_numbers[0]):
            output_string[f_name] = params[0]+"\n"
    
        #output_string[f_name] += params[int(run_dir[1])+1]+"\n" # Previous version.
        output_string[f_name] += params[int(run_dir[1])+offset]+"\n"

#print output_string

for f_name in output_string.keys():
    print output_dir+f_name
    outfile = open(output_dir+f_name,"w")
    outfile.write(output_string[f_name])
    outfile.close()



outfile = open(output_dir+"python_seed.txt","w")
outfile.write("1\n")
outfile.close()
    
#dictionary_file = open("impact_evaluation/parameters/dictionary_params_to_file_"+COUNTY+".csv","w")
#dictionary_file.write(dictionary_params_to_file)
#dictionary_file.close()
