# Script to take a 'baseline' set of runs, and generate modified param_processed_patch0_barriers.csv parameter sets (one per directory)
# and then generate a bash script to run all the parameter sets in their given directories.
# Script used for Manicaland HIV prevention cascade NIH call, Jan 2022.
# "Baseline" parameter files to be read from directory "params"
# and written to directories "params_VMMC_M_15_29_remove_barriers" etc.


import os, sys, glob
from numpy import prod
from os import path
from shutil import copyfile
import xlrd



# Read in Louisa's Excel file, and pull out the non-conditional cascade probabilities (which are then stored - so that individual cascade probabilites can be modified to calculate a probability of using prevention tool X):
def read_cascade_excel_file(methods):
    cascade_param_file = ("/home/mike/Dropbox (SPH Imperial College)/Manicaland/Cascades/cascade_model_parameters.xlsx")
 
    wb = xlrd.open_workbook(cascade_param_file)
    sheet = wb.sheet_by_index(0)

    


    cascade_data = {}

    for i in range(3,sheet.nrows):
        rowdata = sheet.row_values(i, start_colx=0, end_colx=None)
        tool = rowdata[0].encode("ascii").rstrip()
        if(tool in methods):
            s = rowdata[2].encode("ascii")
            # Ignore the never sex group here:
            if not(s=="Never had sex"):
                gender = rowdata[1].encode("ascii").replace("Female","F").replace("Male","M").rstrip()
                age_gp = s.lstrip().replace("Ever had sex ","").replace("-","_")
                pop =  gender + age_gp
                
                [p_motivation,p_access,p_effuse] = [rowdata[4]/(1.0*rowdata[3]),rowdata[7]/(1.0*rowdata[4]),rowdata[10]/(1.0*rowdata[7])]
                if not(tool in cascade_data.keys()):
                    cascade_data[tool] = {}
            
                cascade_data[tool][pop] = [p_motivation,p_access,p_effuse]
    
    return cascade_data





# Runs a set of checks to make sure everything is as expected when the code first starts:
def check_expected_file_structure(intervention_param_files):
    if not os.path.exists("params"):
        print("Error - directory params not found. Exiting")
        sys.exit(1)

    for f in intervention_param_files:
        if not(os.path.isfile("params/"+f)):
            print("Error - file "+f+" not found in params/")
            sys.exit(1)
        

def get_list_of_param_files_excluding_intervention_files(intervention_files):
    txt_files = glob.glob("params/*.txt")
    csv_files = [x for x in glob.glob("params/*.csv") if x.split("/")[-1] not in intervention_files]
    filenames_list = [x.split("/")[-1] for x in txt_files + csv_files]
    return filenames_list
    
                
# Makes destination_dir and then copies all the parameter files (apart from param_barriers.csv - which makes up the list intervention_param_files):
def copy_non_intervention_files(intervention_param_files,destination_dir):

    # Looks up all the *.txt and *.csv files in the directory "params", apart from those in intervention_param_files.
    files_to_copy = get_list_of_param_files_excluding_intervention_files(intervention_param_files)
    #print(intervention_param_files)
    #print(files_to_copy)

    # Make the directory:
    os.mkdir(destination_dir)
    
    # Copy all the other files:
    for f in files_to_copy:
        try:
            copyfile("params/"+f, destination_dir+f)
        except:
            print("Error occurred while copying",f,"to ",destination_dir)
            sys.exit(1)



############################################################
# Main code:
############################################################

prevention_methods = ["Male condoms","PrEP","VMMC"]

dictionary_tool_paramnames = {"PrEP":"p_use_PrEP_","VMMC":"p_use_VMMC_","Male condoms":"p_use_cond_casual_"}
dictionary_agegroups = {'M15_29':"M_young", 'M30_54':"M_old", 'F15_24':"F_young", 'F25_54':"F_old"}


# For each tool: motivation, access, effective use:
# Condoms - motivation is up to 63%, make 90% (similar to Avahan FSW)
#           availability - up to 98% availabity already, so make 100%;
#           effective use  - currently up to 70%, negotiation and knowledge of how to use are issues . Assume can make 90% (again Avahan-ish).
#
# VMMC - motivation is 55% - barriers due to being unaware of VMMC, perceived consequences (pain/infection) and social consequences. Assme 90% upper limit (similar to TMC levels in parts of SSA). 
#        availability is 90% already, so make 100%.
#        effective use - issues around disapproval of partners and others. Assume 90% upper limit (similar to TMC levels).

# PrEP - Motivation 30%, based on SEARCH trial (Koss Lancet HIV 2020) where overall 27% of participants started PrEP given no access barriers. ECHO trial (Donnell Lancet HIV 2021) found 26% started PrEP (again, assume no access barriers). Note that for SEARCH 45% of individuals with self-identified HIV risk started PrEP (so could be an alternative upper bound).
#       - access - highest in data is 84%. Assume can be up to 100%.
#       - effective use - forgets pills, partner disapproval. Assume can be 90%.

intervention_barrier_levels = {"Male condoms":[0.9, 1.0, 0.9],"PrEP":[0.3,1.0,0.9],"VMMC":[0.9,1.0,0.9]}


# This contains the pre-existing parameters:
baseline_dir = "params/"

# Read in Louisa's prevention cascade probabilities:
cascade_data = read_cascade_excel_file(prevention_methods)


# We will read in the 'baseline' cascade barriers file into baseline_data from this file:
intervention_param_file = "param_processed_patch0_barriers.csv"

# Check that the file structure is as expected:
check_expected_file_structure([intervention_param_file])

# Now load the prevention cascade probabilities:
infile = open(baseline_dir+intervention_param_file,"r")
d = infile.readlines()
baseline_data = [line.rstrip().split(" ") for line in d]
header = baseline_data[0]




print("Check VMMC multiplier for conversion to annual VMMC rate")

##############################################################################
# Generate parameter sets where we remove barriers in *all* priority populations
# The "All_tools" tool means change all of PrEP+VMMC+condom use.

pops = {"VMMC":['M15_29', 'M30_54'],"PrEP":['M15_29', 'M30_54', 'F15_24', 'F25_54'],"Male condoms":['M15_29', 'M30_54', 'F15_24', 'F25_54']}

# Go through all tools, populations and intervention scenarios ("barriers"):
for tool in prevention_methods+["All_tools"]:

    # The "1" means intervene in this barrier. The barriers are
    for barriers in ["increase_motivation","increase_access","increase_effuse","remove_barriers"]:
        if tool=="Male condoms":
            # Remove the "male" from male condom:
            tool_filenametag = "cond"
        else:
            tool_filenametag = tool



        # This will store the new_param_value for the given tool(s) and all priority populations
        new_param_values = {}
        list_i_to_change = {}
        if(tool=="All_tools"):
            new_param_values = {x:{} for x in prevention_methods}
            list_i_to_change = {x:{} for x in prevention_methods}
            tool_list = prevention_methods[:]
        else:
            new_param_values[tool] = {}
            list_i_to_change[tool] = {}
            tool_list = [tool]
            print("Tool_list=",tool_list)
            print("Tool=",tool)
            
        for a_tool in tool_list:
            for population in pops[a_tool]:


            # These are the names of the column in the baseline param_processed_patch0_barriers.csv that we will modify (i_to_change is then the column number):
                paramfile_column_name = dictionary_tool_paramnames[a_tool]+dictionary_agegroups[population]+"_intervention"
                list_i_to_change[a_tool][population] = header.index(paramfile_column_name)
                print("List of col nos to change",list_i_to_change)
                    
                # Calculate the probability of the given population using the given tool for this "barrier" scenario:
                if(barriers=="increase_motivation"):
                    new_param_values[a_tool][population] = intervention_barrier_levels[a_tool][0]*cascade_data[a_tool][population][1]*cascade_data[a_tool][population][2]
                elif(barriers=="increase_access"):
                    new_param_values[a_tool][population] = cascade_data[a_tool][population][0]*intervention_barrier_levels[a_tool][1]*cascade_data[a_tool][population][2]
                elif(barriers=="increase_effuse"):
                    new_param_values[a_tool][population] = cascade_data[a_tool][population][0]*cascade_data[a_tool][population][1]*intervention_barrier_levels[a_tool][2]
                elif(barriers=="remove_barriers"):
                    new_param_values[a_tool][population] = prod(intervention_barrier_levels[a_tool])
                else:
                    new_param_values[a_tool][population] = -1 # Dummy value - this would break popart-ibm.exe if encountered, so acts as a check that we never reach this value.

                if(a_tool=="VMMC"):
                    # Multiply by 0.20524131132744 to convert from a cumulative % circumcised to an annual %. The value is obtained in C:\Users\mpickles\Dropbox (SPH Imperial College)\Manicaland\Model\VMMC\Model_VMMC_uptake_FINAL.xlsx - it is the % of VMMC operations from 2013-2019 (from DHIS-2 data) that occurred in 2019. Assume that this same multiplier holds now.
                    new_param_values[a_tool][population] = new_param_values[a_tool][population]*0.20524131132744
        
        
        # This is the header for the updated param_processed_patch0_barriers.csv file:
        new_dataset = " ".join(baseline_data[0])+"\n"
            
        # Now swap in the new probability for each parameter set (i.e. line in the file):
        for line in baseline_data[1:]:
            updated_line = line[:]
            if(not(barriers=="allbarriers")):
                for a_tool in tool_list:
                    for population in pops[a_tool]:
                        i_to_change = list_i_to_change[a_tool][population]
                        updated_line[i_to_change] = str(new_param_values[a_tool][population])

            new_dataset += " ".join(updated_line)+"\n"
                
            
        param_outputdir = "param_"+tool_filenametag+"_all_priority_pops_"+barriers+"/"
        print(param_outputdir)

        if (os.path.isdir(param_outputdir)):
            print("Dir ",param_outputdir,"already exists. Exiting")
            sys.exit(1)


        # Copies the other param_*.csv files to the directory dir_to_check (having first made that directory):
        copy_non_intervention_files([intervention_param_file],param_outputdir)                
        # Now write the altered prevention cascade csv file:
        outfile = open(param_outputdir+intervention_param_file,"w")
        outfile.write(new_dataset)
        outfile.close()
            



#############################################################################
# Generate scenarios for "Motivation+access" for all priority populations and tools:

pops = {"VMMC":['M15_29', 'M30_54'],"PrEP":['M15_29', 'M30_54', 'F15_24', 'F25_54'],"Male condoms":['M15_29', 'M30_54', 'F15_24', 'F25_54']}

# Go through all tools, populations and intervention scenarios ("barriers"):
for tool in prevention_methods+["All_tools"]:

    # The "1" means intervene in this barrier. The barriers are
    barriers = "increase_motivation_access"
    if tool=="Male condoms":
        # Remove the "male" from male condom:
        tool_filenametag = "cond"
    else:
        tool_filenametag = tool



    # This will store the new_param_value for the given tool(s) and all priority populations
    new_param_values = {}
    list_i_to_change = {}
    if(tool=="All_tools"):
        new_param_values = {x:{} for x in prevention_methods}
        list_i_to_change = {x:{} for x in prevention_methods}
        tool_list = prevention_methods[:]
    else:
        new_param_values[tool] = {}
        list_i_to_change[tool] = {}
        tool_list = [tool]
        print("Tool_list=",tool_list)
        print("Tool=",tool)
            
    for a_tool in tool_list:
        for population in pops[a_tool]:


        # These are the names of the column in the baseline param_processed_patch0_barriers.csv that we will modify (i_to_change is then the column number):
            paramfile_column_name = dictionary_tool_paramnames[a_tool]+dictionary_agegroups[population]+"_intervention"
            list_i_to_change[a_tool][population] = header.index(paramfile_column_name)
            print("List of col nos to change",list_i_to_change)
                    
            # Calculate the probability of the given population using the given tool for this "barrier" scenario:
            new_param_values[a_tool][population] = intervention_barrier_levels[a_tool][0]*intervention_barrier_levels[a_tool][1]*cascade_data[a_tool][population][2]

            if(a_tool=="VMMC"):
                # Multiply by 0.20524131132744 to convert from a cumulative % circumcised to an annual %. The value is obtained in C:\Users\mpickles\Dropbox (SPH Imperial College)\Manicaland\Model\VMMC\Model_VMMC_uptake_FINAL.xlsx - it is the % of VMMC operations from 2013-2019 (from DHIS-2 data) that occurred in 2019. Assume that this same multiplier holds now.
                new_param_values[a_tool][population] = new_param_values[a_tool][population]*0.20524131132744
        
        
    # This is the header for the updated param_processed_patch0_barriers.csv file:
    new_dataset = " ".join(baseline_data[0])+"\n"
            
    # Now swap in the new probability for each parameter set (i.e. line in the file):
    for line in baseline_data[1:]:
        updated_line = line[:]
        for a_tool in tool_list:
            for population in pops[a_tool]:
                i_to_change = list_i_to_change[a_tool][population]
                updated_line[i_to_change] = str(new_param_values[a_tool][population])

        new_dataset += " ".join(updated_line)+"\n"
                
            
    param_outputdir = "param_"+tool_filenametag+"_all_priority_pops_"+barriers+"/"
    print(param_outputdir)

    if (os.path.isdir(param_outputdir)):
        print("Dir ",param_outputdir,"already exists. Exiting")
        sys.exit(1)


    # Copies the other param_*.csv files to the directory dir_to_check (having first made that directory):
    copy_non_intervention_files([intervention_param_file],param_outputdir)                
    # Now write the altered prevention cascade csv file:
    outfile = open(param_outputdir+intervention_param_file,"w")
    outfile.write(new_dataset)
    outfile.close()
            



#############################################################################
# Go through all tools, populations and intervention scenarios ("barriers"):
for tool in prevention_methods:
    if(tool=="VMMC"):
        pops = ['M15_29', 'M30_54']
    else:
        pops = ['M15_29', 'M30_54', 'F15_24', 'F25_54']

    for population in pops:
        # The "1" means intervene in this barrier. The barriers are
        for barriers in ["allbarriers","increase_motivation","increase_access","increase_effuse","remove_barriers"]:
            if tool=="Male condoms":
                # Remove the "male" from male condom:
                tool_filenametag = "cond"
            else:
                tool_filenametag = tool

            # This is the name of the column in the baseline param_processed_patch0_barriers.csv that we will modify (i_to_change is then the column number):
            paramfile_column_name = dictionary_tool_paramnames[tool]+dictionary_agegroups[population]+"_intervention"
            i_to_change = header.index(paramfile_column_name)

            # Calculate the probability of the given population using the given tool for this "barrier" scenario:
            if(barriers=="increase_motivation"):
                new_param_value = intervention_barrier_levels[tool][0]*cascade_data[tool][population][1]*cascade_data[tool][population][2]
            elif(barriers=="increase_access"):
                new_param_value = cascade_data[tool][population][0]*intervention_barrier_levels[tool][1]*cascade_data[tool][population][2]
            elif(barriers=="increase_effuse"):
                new_param_value = cascade_data[tool][population][0]*cascade_data[tool][population][1]*intervention_barrier_levels[tool][2]
            elif(barriers=="remove_barriers"):
                new_param_value = prod(intervention_barrier_levels[tool])
            else:
                new_param_value = -1 # Dummy value - this would break popart-ibm.exe if encountered, so acts as a check that we never reach this value.

            if(tool=="VMMC"):
                # Multiply by 0.20524131132744 to convert from a cumulative % circumcised to an annual %. The value is obtained in C:\Users\mpickles\Dropbox (SPH Imperial College)\Manicaland\Model\VMMC\Model_VMMC_uptake_FINAL.xlsx - it is the % of VMMC operations from 2013-2019 (from DHIS-2 data) that occurred in 2019. Assume that this same multiplier holds now.
                new_param_value = new_param_value*0.20524131132744
            # This is the header for the updated param_processed_patch0_barriers.csv file:
            new_dataset = " ".join(baseline_data[0])+"\n"

            # Now swap in the new probability for each parameter set (i.e. line in the file):
            for line in baseline_data[1:]:
                updated_line = line[:]
                if(not(barriers=="allbarriers")):
                    updated_line[i_to_change] = str(new_param_value)

                new_dataset += " ".join(updated_line)+"\n"
                
            
            param_outputdir = "param_"+tool_filenametag+"_"+population+"_"+barriers+"/"
            print(param_outputdir)

            if (os.path.isdir(param_outputdir)):
                print("Dir ",param_outputdir,"already exists. Exiting")
                sys.exit(1)


            # Copies the other param_*.csv files to the directory dir_to_check (having first made that directory):
            copy_non_intervention_files([intervention_param_file],param_outputdir)                
            # Now write the altered prevention cascade csv file:
            outfile = open(param_outputdir+intervention_param_file,"w")
            outfile.write(new_dataset)
            outfile.close()
            

######################################################
# Now make a shell script to run everything:
######################################################



intervention_script = ''' #!/bin/bash

seed=$1
nsamples=10 # chaneg for different nruns
nreps=1
verbose=0
community=5

# Calculate the overall number of simulations to perform (nreps * nsamples)
nruns=`expr $nsamples \* $nreps`
# Store current directory so easy to get back there:
currentdir=$PWD
ibmdir="./"

echo "********RUNNING IBM**********"

'''


    



for tool in prevention_methods:
    if(tool=="VMMC"):
        pops = ['M15_29', 'M30_54']
    else:
        pops = ['M15_29', 'M30_54', 'F15_24', 'F25_54']

    for population in pops:
        # The "1" means intervene in this barrier. The barriers are
        for barriers in ["allbarriers","increase_motivation","increase_access","increase_effuse","remove_barriers"]:
            if tool=="Male condoms":
                print("Male condoms")
                # Remove the "male" from male condom:
                tool_filenametag = "cond"
                if barriers=="allbarriers":
                    popart_ibm_intervention_flag="110"
                else:
                    popart_ibm_intervention_flag="111"
            else:
                tool_filenametag = tool
                popart_ibm_intervention_flag="110"

            
            param_outputdir = "param_"+tool_filenametag+"_"+population+"_"+barriers+"/"
            

            intervention_script += 'outputdirectory="./'+param_outputdir+'"\n'
            intervention_script += 'mkdir -p $outputdirectory/Output\n'
            
            intervention_script += '$ibmdir/popart-simul.exe $outputdirectory $nruns '+popart_ibm_intervention_flag+'\n'


# Special runs:
for barriers in ["increase_motivation","increase_access","increase_effuse","remove_barriers"]:

    intervention_script += 'outputdirectory="./param_PrEP_all_priority_pops_'+barriers+'/"\n'
    intervention_script += 'mkdir -p $outputdirectory/Output\n'
    intervention_script += '$ibmdir/popart-simul.exe $outputdirectory $nruns 110\n'

    intervention_script += 'outputdirectory="./param_VMMC_all_priority_pops_'+barriers+'/"\n'
    intervention_script += 'mkdir -p $outputdirectory/Output\n'
    intervention_script += '$ibmdir/popart-simul.exe $outputdirectory $nruns 110\n'

    intervention_script += 'outputdirectory="./param_cond_all_priority_pops_'+barriers+'/"\n'
    intervention_script += 'mkdir -p $outputdirectory/Output\n'
    intervention_script += '$ibmdir/popart-simul.exe $outputdirectory $nruns 111\n'

    intervention_script += 'outputdirectory="./param_All_tools_all_priority_pops_'+barriers+'/"\n'
    intervention_script += 'mkdir -p $outputdirectory/Output\n'
    intervention_script += '$ibmdir/popart-simul.exe $outputdirectory $nruns 111\n'

for tool in prevention_methods+["All_tools"]:
    intervention_script += 'outputdirectory="./param_'+tool+'_all_priority_pops_increase_motivation_access/"\n'
    intervention_script += 'mkdir -p $outputdirectory/Output\n'
    intervention_script += '$ibmdir/popart-simul.exe $outputdirectory $nruns 110\n'
            
bash_script_file = open("run_all_scenarios.sh","w")
bash_script_file.write(intervention_script)
bash_script_file.close()
