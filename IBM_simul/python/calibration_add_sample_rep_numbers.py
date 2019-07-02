#!/usr/bin/env python3
"""
Script to add rep/sample numbers to the calibration files.  

This script opens the calibration files output from the IBM (after it has run) and adds ID numbers 
for both parameter samples and simulation repeats, which designate the number of simulations that
have been performed for each parameter sample.  These (nsamples and nreps) are given as input args
to this script.  


Usage:
    python calibration_add_sample_rep_numbers.py [outdir] [nsamples] [nreps]


Command-line arguments:

outdir: dir
    Directory where the files output from the IBM are stored.
nsamples: int
    Number of samples used in the output IBM simulations.  
nreps : int
    Number of simulations performed for each parameter sample.  


Note: This script does not currently work when running on the rescomp cluster.  
"""

import sys, os
from os.path import join
import utilities as utils

if __name__ == "__main__":
    
    # Parse arguments
    output_dir = sys.argv[1]
    nsamples = int(sys.argv[2])
    nreps = int(sys.argv[3])
    
    #os.chdir(output_dir)
    output_files = os.listdir(output_dir)
    calibration_files = [o for o in output_files if "Calibration" in o]
    
    for f in calibration_files:
        lines = utils.parse_file(join(output_dir, f))
        
        # Append first two columns as IDs for sample number and simulation rep number
        for i, l in enumerate(lines):
            if i == 0:
                new_header_line = "SampleNumber,RepNumber,"+l
                lines[0] = new_header_line
            else:
                sample_number = ((i - 1)//nreps)
                rep_number = (i - 1) - sample_number*nreps
                new_line = str(sample_number) + "," + str(rep_number) + "," + l
                lines[i] = new_line
        
        # Save the file again
        outfilename = join(output_dir, f)
        outfile = open(outfilename,"w")
        outfile.write('\n'.join(lines))
        outfile.close()
