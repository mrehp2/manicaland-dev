import glob,sys,os
import shutil   # For copying files


dir_root = "/home/mike/MANICALAND/manicaland-dev/IBM_simul/results_testOct2021/"

output_dir = "/home/mike/MANICALAND/manicaland-dev/IBM_simul/IMPACT_TEMP/params/"

if(not(os.path.isdir(output_dir))):
    try:
        os.makedirs(output_dir)
    except:
        print "Error - need to make directiry ",output_dir
        sys.exit()

likelihood_fits_file = open(dir_root+"/goodfits.txt","r")
run_numbers = [int(x.split()[1]) for x in likelihood_fits_file.read().splitlines()]
likelihood_fits_file.close()
print run_numbers



param_dir = "/home/mike/MANICALAND/manicaland-dev/IBM_simul/data/SAMPLED_PARAMETERS/PARAMS_COMMUNITY5/"

lhc_file_list = glob.glob(param_dir+"param_processed_*.csv")

full_file_list = glob.glob(param_dir+"*.*")

# Files that also need to be copied:
remaining_file_list = list(set(full_file_list)-set(lhc_file_list))

# These files also need to be copied (but due to names we add/remove them from the lists by hand):
exception_files = [param_dir+"param_processed_patch0_fertility.csv",param_dir+"param_processed_patch0_mortality.csv",param_dir+"param_processed_patch0_mtct.csv"]

remaining_file_list += exception_files
for f in exception_files:
    lhc_file_list.remove(f)

    

# Copy these files:
for f in remaining_file_list:
    f_name = f.split("/")[-1]
    #print output_dir+f_name
    shutil.copy(f,output_dir+f_name)


    
for f in lhc_file_list:
    infile = open(f,"r")
    params = infile.read().splitlines()
    infile.close()

    output_string = params[0]+"\n"
    
    f_name = f.split("/")[-1]
    for n in run_numbers:
        output_string += params[n+1]+"\n"

    #print output_string
    outfile = open(output_dir+f_name,"w")
    outfile.write(output_string)
    outfile.close()

#dictionary_file = open("impact_evaluation/parameters/dictionary_params_to_file_"+COUNTY+".csv","w")
#dictionary_file.write(dictionary_params_to_file)
#dictionary_file.close()
