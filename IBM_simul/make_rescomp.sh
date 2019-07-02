#!/bin/bash
# 
# Script to processes input parameter files ready for running the IBM on rescomp.  
# This shell script calls a couple of Python scripts, once for each community, to 
# generate the desired input files for the IBM (files of the form param_processed*.csv)

# Arguments
seed=10                     # Seed used by the Python scripts
nruns=1                     # Number of runs to generate using the Latin Hypercube sampling
verbose=1                   # print verbose output?
rescompdir="calibration_unblinding_params"    # name of the folder in which to save these files


# Remove the output directory if it already exists
rm -rf $rescompdir
mkdir -p $rescompdir

# Store current directory so easy to get back there:
currentdir=$PWD

# Define the array of communities for which to generate parameter values
declare -a communities=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21)
echo "Generating parameter files for ${#communities[@]} PopART communities"

for community in ${communities[@]}
do 
    # Define the input and output directories for each community
    inputdir="data/GENERATED_PRIORS/PARAMS_COMMUNITY${community}"
    outputdir="${rescompdir}/PARAMS_COMMUNITY${community}"
    mkdir -p $outputdir
    
    # Remove all files from input and output directories
    rm -r $inputdir/*.*
    
    # Take the RAW_PRIORS parameter ranges, convert to files that can be read by the IBM
    # This code also copies files from output of R scripts.
    python python/make_params_folder_files.py $currentdir $community RESCOMP
    
    # Create param_processed*.csv files from the template text files
    python python/make_ibm_parameter_sample.py $inputdir $outputdir $seed $nruns $verbose
done

# Make a tar archive file:
echo "***CREATING TARFILE:***"
tar -czf $rescompdir.tar.gz $rescompdir
