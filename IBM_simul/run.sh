#!/bin/bash

seed=10
nsamples=2
nreps=1
verbose=0
community=5

# Calculate the overall number of simulations to perform (nreps * nsamples)
nruns=`expr $nsamples \* $nreps`
# Store current directory so easy to get back there:
currentdir=$PWD
ibmdir="./src/"
# This is where we will get the params from:
inputdirectory="./data/GENERATED_PRIORS/PARAMS_COMMUNITY$community/"
# This is where the output of make_params_folder_files_Manicaland.py is:
outputdirectory="./data/SAMPLED_PARAMETERS/PARAMS_COMMUNITY$community/"

# Make directory if it does not exist:
mkdir -p $outputdirectory/Output

# Remove any param_processed_patch* files. Note that these will be re-generated by
# make_params_folder_files.py and make_ibm_parameter_sample.py, so it is *important* that this rm
# command occurs BEFORE either of those 
# scripts are called.
rm -f $outputdirectory/param_processed_patch*.csv
rm -f $inputdirectory/param_processed_patch*.csv

# Take the RAW_PRIORS parameter ranges and convert them into things that can be read by make_ibm_parameter_sample.py.
# This code also copies files from output of R scripts.
python python/make_params_folder_files_Manicaland.py $currentdir $community LAPTOP

# Make the parameter files used by the IBM:
python python/make_ibm_parameter_sample_Manicaland.py $inputdirectory $outputdirectory $seed $nsamples $nreps $verbose

# Is this a counterfactual or not?

# If not counterfactual:
if [ -z "$1" ]; then 
    # Put any counterfactual files safe in temporary folder (the 2>/dev/null should prevent 
    # an error message if no such file exists):
    cd $outputdirectory
    mkdir -p Output/temp
    mv Output/*CF*.csv Output/temp 2>/dev/null
    
    # Remove old non-counterfactual output files:
    rm -f Output/*.csv 
    
    # Put any counterfactual files back and remove the temporary folder:
    mv Output/temp/*CF*.csv Output/ 2>/dev/null
    rmdir Output/temp

    # Go back to the original directory:
    cd $currentdir

    #echo "NOT COUNTERFACTUAL"
    echo "********RUNNING IBM**********"
    
    $ibmdir/popart-simul.exe $outputdirectory $nruns

    # Now go and generate ART output files 
    # e.g. ART_distribution_CL05_Za_A_V1.2_patch0_Rand10_Run2_0.csv and
    # ART_transition_dist_CL04_Za_C_V1.2_patch1_Rand10_Run1_0.csv
    
    python python/generate_art_distribution_files.py $outputdirectory/Output

# Else is a counterfactual:
else
    if [ "$1" = "CF" ]; then
        # Remove old counterfactual output files:
        rm -f Output/*CF*.csv
        
        #echo "COUNTERFACTUAL"
        echo "********RUNNING IBM COUNTERFACTUAL**********"
        $ibmdir/popart-simul.exe $outputdirectory $nruns 1
    
        # Generate ART output files 
        # e.g. ART_distribution_CL05_Za_A_V1.2_patch0_Rand10_Run2_0.csv and
        # ART_transition_dist_CL04_Za_C_V1.2_patch1_Rand10_Run1_0.csv
        python python/generate_art_distribution_files.py $outputdirectory/Output
    
    else
        echo "Unknown option"
        #./popart-simul.exe $directory $nruns
    fi
fi

# Post-process the calibration files to include sample and rep numbers in the csv files
python python/calibration_add_sample_rep_numbers.py $outputdirectory/Output $nsamples $nreps
