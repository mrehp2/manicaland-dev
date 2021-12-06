#!/bin/bash

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
# This is where we will get the params from. $outputdirectory/Output is where the results are written.
outputdirectory="./params/"

mkdir -p $outputdirectory/Output


echo "********RUNNING IBM**********"
    
$ibmdir/popart-simul.exe $outputdirectory $nruns 000

# Now go and generate ART output files 
# e.g. ART_distribution_CL05_Za_A_V1.2_patch0_Rand10_Run2_0.csv and
# ART_transition_dist_CL04_Za_C_V1.2_patch1_Rand10_Run1_0.csv
    
python ../../python/generate_art_distribution_files.py $outputdirectory/Output


# Post-process the calibration files to include sample and rep numbers in the csv files
#python ../python/calibration_add_sample_rep_numbers.py $outputdirectory/Output $nsamples $nreps
