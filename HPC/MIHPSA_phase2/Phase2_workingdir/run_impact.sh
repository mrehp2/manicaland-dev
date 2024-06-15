#!/bin/bash

seed=$1
#nsamples=2
nsamples=10 # chaneg for different nruns
nreps=1
verbose=0
community=5

# Calculate the overall number of simulations to perform (nreps * nsamples)
nruns=`expr $nsamples \* $nreps`
# Store current directory so easy to get back there:
currentdir=$PWD
ibmdir="./src/"

# This is where the output of make_params_folder_files_Manicaland.py is:
outputdirectory="./params/"

# Make directory if it does not exist:
mkdir -p $outputdirectory/Output

echo "********RUNNING IBM**********"
    
$ibmdir/popart-simul.exe $outputdirectory $nruns


