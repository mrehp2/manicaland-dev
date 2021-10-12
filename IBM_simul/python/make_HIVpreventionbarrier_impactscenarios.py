# Given a set of calibrated runs with files param_processed_patchP_barriers.csv, create corresponding impact parameter files (i.e. reduction_non_use_intervention set to different values).
# Impact parameter files to be read from directory "params"
# and written to directories "params_intervention20" etc (20 would represent a 20% effective intervention).


import os, sys, glob
from os import path
from shutil import copyfile

param_name = "reduction_non_use_intervention"
patches = [0] # Specify the patches here.
intervention_param_files = ["param_processed_patch"+str(p)+"_barriers.csv" for p in patches]
intervention_baseline_value = 0.1 # This is what the value of the variable shoudl be beforehand.
intervention_effectiveness_values = [0.2,0.3,0.4]


# Runs a set of checks to make sure everything is as expected when the code first starts:
def check_expected_file_structure(intervention_param_files,intervention_effectiveness_values):
    if not os.path.exists("params"):
        print "Error - directory params not found. Exiting"
        sys.exit(1)

    for f in intervention_param_files:
        if not(os.path.isfile("params/"+f)):
            print "Error - file "+f+" not found in params/"
            sys.exit(1)
        
    for i in intervention_effectiveness_values:
            if os.path.exists("params"+str(int(100*i))):
                print "Error: directory params"+str(int(100*i))+"/ already exists. Exiting"
                sys.exit(1)


def get_list_of_param_files_excluding_intervention_files(intervention_files):
    txt_files = glob.glob("params/*.txt")
    csv_files = [x for x in glob.glob("params/*.csv") if x.split("/")[-1] not in intervention_files]
    filenames_list = [x.split("/")[-1] for x in txt_files + csv_files]
    return filenames_list
    
                


def copy_non_intervention_files(intervention_param_files,intervention_effectiveness_values):

    files_to_copy = get_list_of_param_files_excluding_intervention_files(intervention_param_files)

    print files_to_copy


    # Copy all the other files:
    for i in intervention_effectiveness_values:
        destination_dir = "params"+str(int(100*i))+"/"
        os.mkdir(destination_dir)
        for f in files_to_copy:
            try:
                copyfile("params/"+f, destination_dir+f)
            except:
                print "Error occurred while copying",f,"to ",destination_dir
                sys.exit(1)


check_expected_file_structure(intervention_param_files,intervention_effectiveness_values)
                
copy_non_intervention_files(intervention_param_files,intervention_effectiveness_values)                

# Now load the
intervention_files_data = {}
for f in intervention_param_files:
    
    infile = open("params/"+f,"r")
    original_data = infile.readlines()
    infile.close()
    i_param = original_data[0].split().index(param_name)
    template_data = original_data[0]
    for line in original_data[1:]:
        modified_line = line.split()[:]
        if not(modified_line[i_param]==str(intervention_baseline_value)):
            print "Error - mismatch between value of intervention in baseline file and expected value"
            sys.exit(1)
        modified_line[i_param] = "ZZZ"
        modified_line = ' '.join(modified_line)
        template_data += modified_line + "\n"
    print template_data
    
    # template_data is now a string that is identical to the original one, except that ZZZ now replaces the original intervention parameter.

    for i in intervention_effectiveness_values:
        destination_dir = "params"+str(int(100*i))+"/"
        modified_data = template_data.replace("ZZZ",str(i))
        outfile = open(destination_dir + f, "w")
        outfile.write(modified_data)
        outfile.close()
        

