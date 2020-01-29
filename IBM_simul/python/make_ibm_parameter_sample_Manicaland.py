#!/usr/bin/env python3

COUNTRY="Zimbabwe"

"""
Generate a sample from a Latin Hypercube given parameters defined by a range and output for IBM.

Usage: python make_ibm_parameter_sample.py [indir] [outdir] [ran_seed] [nsample] [nrep] [VERBOSE]

This script does several things:
1) imports parameter values from several text files;
2) checks which parameters in these files are defined on a range of the form `[min,max]`
    (as opposed to being a fixed value);
3) uses a Latin Hypercube to uniformly sample the multidimensional space that spans the combined
    range defined by those varying parameters;
4) outputs parameter text files in a format required as input to the individual-based model.

Parameter files that this script will look for in `indir` are the following:

param_patchinfo.txt
param_init.txt
param_demographics.txt
param_times.txt
param_HIV.txt
param_HSV2.txt
param_cascade.txt
param_popart.txt
param_partnerships.txt
param_PrEP_background.txt
param_PrEP_intervention.txt
Command-line arguments
----------------------
indir
    Directory where script can find the text files of input parameters(i.e. `param_*.txt` files).
    Typically usage names this directory of the form `.../GENERATED_PRIORS/PARAMS_COMMUNTIY5/`,
    for instance.
outdir
    Directory for output of parameter files that have been generated from the Latin Hypercube.
    Default directory if not specified is `infiledir`.  Typical usage names a directory ending
    with `.../SAMPLED_PARAMETERS/PARAMS_COMMUNITY5/`, for example.
ran_seed : int
    Random seed to use.  Set before sampling the Latin Hypercube; set using
    `random.seed(ran_seed)`.  Default value is 1.
nsample : int
    Number of samples (parameter coordinates) to draw from the Latin Hypercube.  Default value is
    the environment variable `DEFAULTSAMPLE = 1000`.
nrep : int
    Number of repeated simulations for each sample of the parameter space using a different random
    seed for the IBM.  
VERBOSE: 0, 1
    Should extra helpful print statements be generated (1 = Yes).  Default value is 0 = No.

This file is part of the PopART IBM.

The PopART IBM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The PopART IBM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with the PopART IBM.  If not, see <http://www.gnu.org/licenses/>.
"""

import os, sys, random, string, glob
import shutil # for file copying etc.x
from os.path import join, basename # for adjusting path names in a platform-independent manner

import utilities as utils


###########################################################################
###########################################################################


def parse_command_line_arguments(args):
    """
    Parse command-line arguments passed when program is called.
    
    Command-line arguments should be of the form:
        python make_ibm_parameter_sample.py INFILEDIR OUTFILEDIR RANDOMSEED NSAMPLE NREP VERBOSE
    
    Only the first argument is necessary - everything else has default values.
    
    
    Parameters
    ----------
    args : list
        A list of command-line arguments as in sys.argv.  
    
    
    Returns
    -------
    [infiledir, outfiledir, ran_seed, nsample, nrep, VERBOSE]; list
        
    
    
    Example
    -------
    
    
    """
    # Make sure that the parameter folder is passed as an argument:
    try:
        infiledir = args[0]
    except:
        utils.handle_error("Error: make_ibm_parameter_sample.py requires the parameter folder to be included first.")
    # Make sure that the directory path ends in a "/":
    if not(infiledir[-1]=="/"):
        infiledir += "/"
    
    # This gets the output folder (ie where we write the files that the IBM will read in).
    if len(args)>1:
        outfiledir = args[1]
    else: # Default is that we write to the same directory we get the parameter ranges from:
        outfiledir = infiledir
    # Make sure that the directory path ends in a "/":
    if not(outfiledir[-1]=="/"):
        outfiledir += "/"
    
    # Set random seed - either pass as argument or use default value:
    if len(args)>2:
        ran_seed = int(args[2])
    else:
        ran_seed = 1 # Default value.
    # Seed should not exceed 10^10 (otherwise could have read-in issues when reading in the string
    # in C as the string is assumed to be a dozen characters at most including the string
    # terminator \0.
    MAXSEED = int(1e10)
    if(ran_seed>MAXSEED):
        ran_seed = ran_seed % MAXSEED
    
    if len(args)>3:
        nsample = int(args[3]) # Sets the size of the latin hypercube part of the sample.
                               # note - total sample size = nsample*(number of scenarios)
    else:
        nsample = DEFAULTSAMPLE  # Default (currently 1000 samples)
    
    if len(args)>4:
        nrep = int(args[4]) # Number of repeat simulations per parameter set
    else:
        nrep = DEFAULTNREP  # Default (currently 1 rep)
    
    if len(args)>5:
        VERBOSE = int(args[5]) # 1 means print stuff, 0 means don't
    else:
        VERBOSE = 0 # Default value - don't print stuff
    
    return [infiledir,outfiledir,ran_seed,nsample,nrep,VERBOSE]


########################################################
# Functions using the file patam_patchinfo.txt:
########################################################

def get_npatches(infiledir):
    """
    Read file `param_patchinfo.txt` and return number of patches in simulation.  
    
    Number of patches in the simulation is defined by how many numbers are within parentheses,
    separated by commas, in the line starting with `cluster_number` in the file 
    `param_patchinfo.txt`.  This line will typically look like: 
    
    `cluster_number (5,4) // Additional comments`
    
    
    Parameters
    ---------
    infiledir : str
        String of path to the directory containing the file `param_patchinfo.txt`.  This is 
        typically the `outputdir` as used in `make_params_folder_files.py`.  Generally named 
        something like "./GENERATED_PRIORS/PARAMS_COMMUNITY5/"
    
    
    Returns
    -------
    NPATCHES : int
        number of patches in the simulation
    """
    patchinfofile = open(join(infiledir, "param_patchinfo.txt"))
    patchinfo = patchinfofile.read().rstrip().split("\n")
    patchinfofile.close()
    for line in patchinfo:
        varname = line.split()[0]
        if varname == "cluster_number":
            patch_clusters = line.split()[1]
            NPATCHES = len(patch_clusters.split(","))

    return NPATCHES


def parse_patch_info(line, NPATCHES):
    """
    Split up a line from `param_patchinfo.txt` file into the correct format
    
    
    Parameters
    ----------
    line : str
        String specifying a line from the file `param_patchinfo.txt`
    NPATCHES : int
        Number of patches in the model
    
    
    Returns
    -------
    patchinfo_output : 
    
    
    Example
    -------
    """

    # Store the line output (with placeholders for variables which need LHC or grid sampling):
    patchinfo_output = ""

    line = remove_whitespaceandcomments(line)

    # Split line by spaces.  First word is name of the var so slice to keep only the ones after.
    words = line.split(" ")
    
    # Remove trailing and leading whitespace (e.g. tabs) from each word:
    words = [w.rstrip() for w in words]
    words = [w.lstrip() for w in words]
    words = words[1:]
    n_words = len(words)
    
    if n_words>1:
        utils.handle_error("Too many things on one line of param_patch_info.txt - exiting!")
    else:
        patch_info_line = words[0]
    
    # Parentheses (round brackets) mean that this is different for different patches:
    if (patch_info_line[0]=="("):
        patch_objects = split_patch_data(patch_info_line,line,NPATCHES)
        for p in range(NPATCHES):
            patchinfo_output += patch_objects[p]+" "
    else:
        param = get_param_number(patch_info_line,line)
        for p in range(NPATCHES):
            patchinfo_output += str(param)+ " "
    
    return patchinfo_output


def write_patch_info(patch_info_file, infiledir, outfiledir, NPATCHES):
    """
    Take the info from the param_patch_info.txt file and write it in the correct format for the IBM
    in the file param_processed_patch_info.txt file.
    
    
    Parameters
    ----------
    patch_info_file : str
        
    infiledir : str
        Input directory
    outfiledir : str
        Output directory
    NPATCHES : int
        Number of patches in the model
    
    
    Returns
    -------
    Nothing is returned; a file is written.  
    
    Example
    -------
    
    
    """
    patch_info_output = ""
    infile = open(join(infiledir, patch_info_file),"r")
    # Read in the file (this is read in initially as a single string including line breaks), then
    # strip off the last line break, then split the remaining text by line break into a list called
    # text_list. Each line of the original file is then an element in the list at this point.
    text_list = infile.read().rstrip().split("\n")
    for line in text_list:
        patch_info_output += parse_patch_info(line, NPATCHES) + "\n"
    infile.close()
    
    # Remove trailing newline characters
    patch_info_output = patch_info_output.rstrip()

    patch_info_outfilename = patch_info_file.replace("param", "param_processed")
    outfile = open(join(outfiledir, patch_info_outfilename), "w")
    outfile.write(patch_info_output)
    outfile.close()


########################################################
# Functions using the file param_patchinfo.txt:
########################################################


def split_patch_data(word, line, NPATCHES):
    """
    Takes an object (`word`) which varies by patch - ie something enclosed in parentheses and where 
    the input for each patch is separated by a comma.  The object "line" is used for debugging.
    Function splits up the word and returns the split object as a list.
    
    Parameters
    ----------
    word : str
    line : str
    NPATCHES : int
    
    Returns
    -------
    
    Notes
    -----
    That it does not convert the objects in the list to floats.
    
    
    Example
    -------
    
    """
    
    if (word[-1] != ")"):
        utils.handle_error("Error: Format of file is not correct - do not include spaces between " + 
            "parentheses\nError is for parameter " + line.split(" ")[0] + "\nExiting.")
            
    patch_objects = word[1:-1].split(",")
    
    if (len(patch_objects) != NPATCHES):
        utils.handle_error("Number of patches = " + NPATCHES + "\nNumber of objects in the following " + 
            "line is not equal to the number of patches" + line.split(" ")[0] + "\nExiting.")
    return patch_objects


def get_lhc_sample_range(word, line):
    """
    Convert string specifying a parameter range into a list of two floats defining that range.
    
    Given a Latin hypercube range as a string ("word") check it is in the right format.
    If it is convert it to a list [x,y] where x and y are floats, and return that list.
    The object "line" is used for debugging.
    Latin hypercube ranges are two numbers separated by a comma and surrounded by square brackets.
    
    
    Parameters
    ----------
    word : str
        String specifying the parameter range (for instance "[0.0-1.2]").  
    line : str
        File line from which the `word` string has been extracted (for debugging purposes)
    
    
    Returns
    -------
    lhc_sample_range : list
        List of parameter range specified as floats (converted from `word`).  
    
    
    Example
    -------
    word = "[0.0-1.2]"
    get_lhc_sample_range(word, "")
    >> [0.0, 1.2]
    
    # Can handle spaces in `word`
    word = "[0.0 - 1.2]"
    get_lhc_sample_range(word, "")
    >> [0.0, 1.2]
    """
    # Make sure that the "word" is in the right format - [a,b] - where a and b are numbers:
    if (word[-1] != "]"):
        utils.handle_error("Format of file is not correct - do not include spaces between square " + 
            "brackets.\nError is for parameter" + line.split(" ")[0] + "\nExiting.")
    
    param_range = word[1:-1].split("-")
    
    if len(param_range) != 2:
        utils.handle_error("Format of file is not correct - objects between square brackets are to be" + 
            " Latin hypercube sampled. They should be of the format e.g. [0.1-0.9] with only " + 
            "one dash.\nError is for parameter" + line.split(" ")[0] + "\nExiting")
    
    # Convert the range from strings to floats. Print an error if not possible.
    try:
        lhc_sample_range = [float(param_range[0]), float(param_range[1])]
    except:
        utils.handle_error("Format of file is not correct - objects between square brackets are to be " + 
            "Latin hypercube sampled. They should be of the format e.g. [0.1-0.9].\nError is for" + 
            " parameter" + line.split(" ")[0] + "\nExiting")
    
    # Now make sure a < b
    if lhc_sample_range[0] >= lhc_sample_range[1]:
        utils.handle_error("Format of file is not correct - objects between square brackets are to be " + 
            "Latin hypercube sampled. They should be of the format e.g. [0.1-0.9] with the second" +
            " number strictly greater than the first.\nError is for parameter" + 
            line.split(" ")[0] + "\nExiting.")
    
    return lhc_sample_range


def get_scenarios(word, line):
    """
    Given a set of scenarios as a string ("word") check it is in the right format.
    If it is convert it to a list "scenarios" [s_1,s_2,...] where s_i are floats, and return that 
    list.  The object "line" is used for debugging.  Scenarios are a set of numbers separated by 
    commas and surrounded by curly brackets.
    
    
    Parameters
    ----------
    word : 
    
    line : str
    
    
    Returns
    -------
    scenarios : 
    
    
    Example
    -------
    
    """
    if (word[-1] != "}"):
        utils.handle_error("Format of file is not correct - do not include spaces between curly brackets"+
            word + "\nError is for parameter" + line.split(" ")[0] + "\nExiting.")
    
    scenarios_text = word[1:-1].split(";")
    if len(scenarios_text)<2:
        utils.handle_error("Error: Format of file is not correct - objects between curly brackets are " +
            "scenarios. We need >1 scenario.\nError is for parameter" + line.split(" ")[0] + 
            "\nExiting.")
    try:
        scenarios = [float(s) for s in scenarios_text]
    except:
        utils.handle_error("Error: Format of file is not correct - objects between curly brackets are" + 
            " scenarios. Each item separated by a semicolon should be a number.\n" + 
            "Error is for parameter" + line.split(" ")[0] + "Listed scenarios are:" + 
            scenarios_text + "\nExiting.")
    
    return scenarios


def get_param_number(word,line):
    try:
        param = float(word)
    except:
        utils.handle_error("Unknown format on line"+line+"\nExiting.")
    return param


def parse_line(line, i_lhc_sampling_vars, NPATCHES):
    """
    Format a single line from a parameter file.  
    
    Parameters
    ----------
    line : str
        String which is a line from a parameter file
    i_lhc_sampling_vars : 
    
    NPATCHES : int
        Number of patches in the model
    
    """
    # Store the line output (with placeholders for variables which need LHC or grid sampling):
    line_output = [[]]
    for p in range(NPATCHES-1):
        line_output.append([])
    

    # This will store the min+max of the variables which need lhc sampling. The order which they
    # turn up in the source file is preserved so that when we latin hypercube sample them it is
    # easy to replace the correct variable with the corresponding placeholder in line_output.
    lhc_sampling_vars = []
    # This will store all the scenarios - if we have a variable which we want to take the values
    # 1,2,3 for example then the line in the param file will be "this_param_name SCENARIO 1 2 3". 
    scenario_vars =[]
    i_scenario_vars = 0

    line = remove_whitespaceandcomments(line)

    # split line by spaces. First word is name of the var so slice to keep only the ones after.
    words = line.split(" ")
    header_temp = words[0]
    # Remove trailing and leading whitespace (e.g. tabs) from each word:
    words = [w.rstrip() for w in words]
    words = [w.lstrip() for w in words]
    words = words[1:]
    n_words = len(words)
    header = ""
    for i in range(n_words):
        if n_words>1:
            header += header_temp + "_"+str(i+1)+" "
        else:
            header += header_temp + " "
    # Now check if this is a Latin hypercube sampled variable - this will be indicated by "LHC" in
    # the second column followed by 2 numbers which are the min+max values of the variable to be
    # sampled.  At present we are assuming uniform dists on each var - can change fairly easily.
    
    if (words[0].upper()=="RANDOMSEED"): # Use upper to ensure that using upper case.
        if (n_words>1):
            utils.handle_error("Only allowed comments in the line specifying RANDOMSEED.")
        for p in range(NPATCHES):
            line_output[p] += [["RANDOMSEED"]]
        # Nothing else allowed so return.
        return [line_output,lhc_sampling_vars,scenario_vars,i_lhc_sampling_vars,words[0] + " "]

    # Otherwise go through the line word-by-word (can have >1 parameter on a given line):
    for i in range(n_words):
        # Parentheses (round brackets) mean that this is different for different patches:
        if (words[i][0]=="("):
            patch_objects = split_patch_data(words[i],line,NPATCHES)
            for p in range(NPATCHES):
                # if the first element of a given patch object is a square bracket then we carry
                # out a LHC sample for that patch. 
                if (patch_objects[p][0]=="["):
                    lhc_sample_range = get_lhc_sample_range(patch_objects[p],line)
                    # We store the min and max for each variable 
                    lhc_sampling_vars += [lhc_sample_range]
                    # Add a placeholder in line_output so easy to replace later on:
                    line_output[p] += [["LHC",i_lhc_sampling_vars]]
                    i_lhc_sampling_vars = i_lhc_sampling_vars + 1

                elif (patch_objects[p][0]=="{"):
                    scenarios = get_scenarios(patch_objects[p],line)
                    scenario_vars += scenarios                    
                    line_output[p] += [["SCENARIO",i_scenario_vars]]
                    i_scenario_vars = i_scenario_vars + 1
                # Only other possibility - a number (which is the same for all patches, and the
                # same for all runs):
                else:
                    param = get_param_number(patch_objects[p],line)
                    line_output[p] += [["CONSTANT",param]]

        # Square brackets indicate that this is an LHC-sampled variable - should be of the form
        # [a-b] where the prior range of the variable is a to b. For now assume uniform - can make
        # non-uniform by adapting code here e.g. [a-b,exponential].
        elif (words[i][0]=="["):
            lhc_sample_range = get_lhc_sample_range(words[i],line)
            # We store the min and max for each variable 
            lhc_sampling_vars += [lhc_sample_range]
            # Add a placeholder in line_output so easy to replace later on:
            for p in range(NPATCHES):
                line_output[p] += [["LHC",i_lhc_sampling_vars]]
            i_lhc_sampling_vars = i_lhc_sampling_vars + 1
        # Curly brackets indicate that this is a variable with different scenarios - should be of
        # the form {p;q;r}. We would run 3 sets of scenarios (ie for each LHC we run with this
        # variable taking values p,q,r) for this example. Can have an arbitrary number of
        # scenarios, but increases number of runs hugely so use with caution.
        elif (words[i][0]=="{"):
            scenarios = get_scenarios(words[i],line)
            scenario_vars += scenarios
            for p in range(NPATCHES):
                line_output[p] = [["SCENARIO",i_scenario_vars]]
            i_scenario_vars = i_scenario_vars + 1
        # Only other possibility - a number (which is the same for all patches, and the same for all runs):
        else:
            param = get_param_number(words[i],line)
            for p in range(NPATCHES):
                line_output[p] += [["CONSTANT",param]]


    return [line_output,lhc_sampling_vars,scenario_vars,i_lhc_sampling_vars,header]


def make_sampleframe(varlist,nsample):
    """
    Split min/max of variables into evenly spaced list and return associated stepsizes. 
    
    Splits the min/max of each element in `varlist` into `nsample` values, returning this list of 
    evenly spaced numbers and also the stepsize for each such variable.  Can be used for grid or 
    Latin hypercube sampling.  
    
    
    Parameters
    ----------
    varlist : list of lists (dimension `len(nvars)` x 2)
        Each subelement of `varlist` has two elements: the min and max of variable in question, it
        is within this range that we split into `nsample` values.  
    
    nsample : int
        Number of samples to generate from the Latin Hypercube (the number of evenly spaced values
        to generate between the min/max of each variable).  
    
    
    Returns
    -------
    List of two values: [thissampleframe, stored_stepsizes]
    
    thissampleframe : list of lists (dimension `len(varlist)` x `nsample`)
        Each element is a list of evenly spaced numbers over the interval specified from
        `varlist[i][0]` to `varlist[i][1]`.  Note that for numpy users, this is the same as:
        >>> import numpy as np
        >>> thissampleframe = [list(np.linspace(v[0], v[1], nsample)) for v in varlist]
    
    stored_stepsizes : list (same length as `varlist`)
        The list of step sizes used to construct the evenly spaced numbers in `thissampleframe`.  
        Calculated as `float(varlist[i][1] - varlist[i][0])/(nsample - 1)`.  
    
    
    Examples
    --------
    >>> x = [[0, 1.0], [-3.0, -2.0], [0.91, 1.21]]
    >>> nsample = 5
    >>> [thissampleframe,stored_stepsizes] = make_sampleframe(x, nsample)
    """
    thissampleframe = []
    stored_stepsizes = []
    for v in varlist:
        # Assume for each variable that we have the [min,max]:
        minv = min(v)
        maxv = max(v)
        if (not(minv==v[0]) or not(maxv==v[1])):
            utils.handle_error("ERROR:varlist in wrong form. Exiting.")

        if (nsample>1):
            # Use float to make sure that do NOT use integer division. The -1 ensures that the
            # biggest value in the LHC is maxv
            stepsize = float(maxv - minv)/(nsample-1)

            # Generate a set of nsample points from minv to maxv equally spaced:
            # Note thissampleframe is a list of lists (each sublist is nsample points for a given
            # variable v (in the same order as varlist).
            thissampleframe += [[minv + x*stepsize for x in range(0,nsample)]]
        else:
            # Use float to make sure that do NOT use integer division. The -1 ensures that the
            # biggest value in the LHC is maxv
            stepsize = float(maxv - minv)

            # Generate a single point half-way inbetween:
            # Note thissampleframe is a list of lists (each sublist is nssample=1 points for a
            # given variable v (in the same order as varlist).
            thissampleframe += [[float(maxv+minv)/2.0]]

        
        # Store the stepsize (so we can use it in make_lhc)
        stored_stepsizes += [stepsize]


    return [thissampleframe,stored_stepsizes]


def make_lhc(lhc_sampleframe,lhc_stepsize,nsample):
    """
    Generate a Latin Hypercube (LHC) sample of size `nsample` from a multivariate grid defined by
    `lhc_sampleframe`.
    
    Loops through the possible values of each variable (in `lhc_sampleframe`), chooses one value at
    random (without replacement), adds this value to a list of coordinates and repeats `nsample`
    times.  The number of variables/dimensions of the multivariate grid is `len(lhc_sampleframe)`.  
    
    Note: the original `lhc_sampleframe` object is modified by this function.  Perhaps a copy of
    this list should be made within this function to avoid this behaviour.  Otherwise, the use of 
    list.remove() could be replaced.  
    
    
    Parameters
    ----------
    lhc_sampleframe : list of lists
        Each element is a list of evenly spaced numbers over the interval of interest of each 
        variable.  
    lhc_stepsize : list
        Step sizes for each variable, defining the multidimensional grid that the LHC samples from.
        *Does not* currently need this as the ranges passed in `lhc_sampleframe` contain this info.
    nsample : int
        Number of samples to draw from the LHC.  
    
    
    Returns
    -------
    lhc : list (dimension nvar x `nsample`)
        List of coordinates in the multidimensional space sampled using LHC sampling.  
    
    
    Examples
    --------
    
    >>> lhc_sampleframe = [[1, 2, 3], [0.25, 0.5, 0.75], [1970, 1975, 1980], [1.2, 1.3, 1.4]]
    >>> lhc_stepsize = None     # Not needed
    >>> nsample = 3
    >>> make_lhc(lhc_sampleframe,lhc_stepsize,nsample)
    """
    nvars = len(lhc_sampleframe)
    if nvars==0:
        return -1
    lhc = []
    for i in range(nsample):
        coord = [] # This will store the "coordinates" of a single point in the LHC sample - ie the
        # value of each variable within that sample.
        for j in range(nvars):
            temp = random.choice(lhc_sampleframe[j])
            coord += [temp]
            # This ensures we choose each point without replacement - ie generate a LHC:
            lhc_sampleframe[j].remove(temp)
        lhc.append(coord)
    # Each element of lhc is a point in the latin hypercube (ie a single sample of params)
    return lhc


def merge_lhc_constants_scenarios(data_from_file_and_patch, lhc, scenarios, nsample, C_RANDOM_SEED):
    """
    Here we want to merge the lhc and text output. text_output is a single string we will repeat 
    nsample times, coming from a single param file.
    In each copy we use a different element of lhc (ie a different set of LHC coordinates) to 
    replace the "LHC" placeholders within text_output.  This creates nsample different parameter 
    sets, where most parameters are kept constant apart from the LHC ones.  Note that if there are 
    no LHC variables in this file then the output will be nsample copies of the same line.
    """
    n_params = len(data_from_file_and_patch)

    outstring = ""
    for n in range(nsample):
        for i in range(n_params):
            if (data_from_file_and_patch[i][0]=="CONSTANT"):
                outstring += str(data_from_file_and_patch[i][1])+" "
            elif (data_from_file_and_patch[i][0]=="LHC"):
                outstring += str(lhc[n][data_from_file_and_patch[i][1]])+" "
            elif (data_from_file_and_patch[i][0].strip() == "RANDOMSEED"):
                outstring += C_RANDOM_SEED[n] + " "
            elif (data_from_file_and_patch[i][0]=="SCENARIO"):
                print("Not currently implementing scenarios properly!!!")
                outstring += str(scenarios[data_from_file_and_patch[i][1]][0])+" "
            else:
                utils.handle_error("Error: not understood!!!" + 
                    str(data_from_file_and_patch[i]) + "\nExiting.")
        # Remove trailing space from line for neatness:
        outstring.rstrip()
        outstring += "\n"

    return outstring


def merge_lhc_constants_scenarios_with_reps(data_from_file_and_patch, lhc, scenarios, nsample, 
        nrep, C_RANDOM_SEED):
    """
    """
    n_params = len(data_from_file_and_patch)

    outstring = ""
    ran_seed_counter = 0
    for n in range(nsample):
        for r in range(nrep):
            for i in range(n_params):
                if (data_from_file_and_patch[i][0]=="CONSTANT"):
                    outstring += str(data_from_file_and_patch[i][1])+" "
                elif (data_from_file_and_patch[i][0]=="LHC"):
                    outstring += str(lhc[n][data_from_file_and_patch[i][1]])+" "
                elif (data_from_file_and_patch[i][0].strip()=="RANDOMSEED"):
                    outstring += C_RANDOM_SEED[ran_seed_counter] + " "
                    ran_seed_counter += 1
                elif (data_from_file_and_patch[i][0]=="SCENARIO"):
                    print("Not currently implementing scenarios properly!!!")
                    outstring += str(scenarios[data_from_file_and_patch[i][1]][0])+" "
                else:
                    utils.handle_error("Error: not understood!!!" + 
                        str(data_from_file_and_patch[i]) + "\nExiting.")
            
            # Remove trailing space from line for neatness:
            outstring.rstrip()
            outstring += "\n"
            
    return outstring


def add_scenarios(scenario_vars,dict_outstring,cumulative_n_vars_with_scenarios_per_file,filename_list):
    # Check we don't have too many scenarios:
    n_scenarios = 1
    for s in scenario_vars:
        n_scenarios = n_scenarios * len(s)
    
    if (n_scenarios*nsample)>50000:
        utils.handle_error("Too many scenarios/too big latin hypercube sample). Exiting.")
    
    for s in scenario_vars:
        DONE_SCENARIO = 0
        for f in filename_list:
            # Check if there is at least one instance of the word SCENARIO, and we have not already\
            # carried out the scenario:
            if (dict_outstring[f].count("SCENARIO")>0 and DONE_SCENARIO==0):
                DONE_SCENARIO = 1
                temp_file_output = ""
                dict_outstring_temp_splitbyline = dict_outstring[f].rstrip().split("\n")
                for scenario in s:
                    for line in dict_outstring_temp_splitbyline:
                        # Make a copy of dict_outstring_temp_splitbyline where the first instance
                        # of the word SCENARIO is replaced, and add this to temp_file_output
                        temp_file_output = temp_file_output + line.replace("SCENARIO",scenario,1) + "\n"
                dict_outstring[f] = temp_file_output
            else:
                dict_outstring_temp = ""
                # We copy the line(s) in dict_outstring len(
                for scenario in s:
                    dict_outstring_temp += dict_outstring[f]

                dict_outstring[f] = dict_outstring_temp


def remove_whitespaceandcomments(line):
    """
    Removes text following double-slash (C comment), remove trailing whitespace in resultant string.
    
    For an input string, `line`, the following is performed:
        1) any text following a double-slash is removed
        2) any white space in truncated line (after removing double slash) is removed
        3) double spaces and tabs converted to single space
    
    This is so that in the original params.txt files we can include comments about the parameters.
    
    
    Parameters
    ----------
    line : str
        Input string, typically from a parameter input text file.  
    
    
    Returns
    -------
    line : str
        Input string with removed 
    
    
    Example
    -------
    line = "PARAMETER_NAME      [0,1]  // This is a parameter that has a range from 0 to 1."
    remove_whitespaceandcomments(line)
    >> 'PARAMETER_NAME [0,1]'
    """
    # Anything after a double slash is treated as a comment (ie C-like behaviour):
    line = line.split("//")[0].rstrip()

    # Remove any trailing whitespace at the end of the line:
    line = line.rstrip()
    
    # Replace commas by spaces (only needed if a csv file)
    # line = line.replace(","," ")
    
    # Replace tabs by spaces 
    line = line.replace("\t"," ")
    
    # Remove any double spaces (ie replace them with single spaces until there are no more).
    while (line.find("  ")>-1):
        line = line.replace("  "," ")
    return line


def process_fertility_file(infiledir, outfiledir, NPATCHES):
    """
    Convert the UNPD fertility files to space-delimited files.  
    
    This function loads files entitled "param_fertility.txt" which are data from the UNPD, removes
    the first row and column of the files (headers), replaces carriage returns (^M) with newlines, 
    and change commas to spaces.  A file for each patch is saved (patch numbering starts from 0) so
    that output files are of the form "param_processed_patch0_fertility.csv", 
    "param_processed_patch1_fertility.csv", etc.
    
    UNPD numbers are fertility per 1000 women in that age group PER 5 YEARS, we normalise to per 
    woman per year rates.  Output files use spaces/newlines instead of commas/carriage returns.
    
    
    Parameters
    ----------
    infiledir : str
        Input directory; where to find "param_fertility.txt" files.  
    outfiledir : str
        Output directory; where to write param_processed_patch*_fertility.csv" files
    NPATCHES : int
        Number of patches for which to generate parameter files for.  
    
    Returns
    -------
    Nothing is returned; fertility files are written to file.  
    
    Example
    -------
    process_fertility_file("./data/RAW_PRIORS/TEMPLATE/", "../../Desktop/", 2)
    
    Note: this function saves the files with a .csv extension but they're really space-delimited
    files.  This should be changed in the future so that file extension and type are consistent.  
    """

    fertilityinfile = open(join(infiledir, "param_fertility.txt"),"r")
    fertilitydata = fertilityinfile.read().rstrip()
    fertilityinfile.close()
    
    fertility_outstring = ""

    # Split text by Excel carriage return ^M (this is dependent upon the version of Python)
    if (sys.version_info[0] == 3): # python 3
        fertilitydatabyline = fertilitydata.split("\n")
    elif (sys.version_info[0] == 2): # python 2
        fertilitydatabyline = fertilitydata.splitlines()

    for line in fertilitydatabyline[1:]:                # First line is a header to ignore it.
        # Split line into an array, by commas, keep all except first column (which is a heading)
        datainaline = line.split(",")[1:]
        
        # Normalise to per-woman per year fertility (and convert to string)
        datainaline_numeric_normalised = [float(x)/1000.0 for x in datainaline]
        datainaline_string_normalised = [str(x) for x in datainaline_numeric_normalised]
        
        # Make string from the array, with spaces between each array element.
        processedline = " ".join(datainaline_string_normalised)
        fertility_outstring += processedline+"\n"
    
    # Write a fertility file for each patch
    for p in range(NPATCHES):
        outfilename = "param_processed_patch" + str(p) + "_fertility.txt"
        outfilename = outfilename.replace("txt","csv")
        outfile = open(join(outfiledir, outfilename),"w")
        outfile.write(fertility_outstring)
        outfile.close()




def copy_existing_processed_files(infiledir, outfiledir, NPATCHES):
    """
    Copy all files of the form `param_processed*.*` files (and some special files) to output directory.
    
    
    This function copies all files of the form "param_processed*.*" in the directory `infiledir` to
    the folder `outfiledir`.  This function first checks that any files in `infiledir` of the form
    "param*.txt" are not already in `outfiledir` but in the form "param_processed_patch*.csv".  
    
    For example the file param_processed_patch0_chipsuptake_round1.csv is actually copied (by 
    make_params_folder_files.py) directly from a file generated by Anne's script. BUT we don't want
    to copy every param_processed*.csv file as many of these are generated by this script 
    (ie make_ibm_parameter_sample.py) - although we could do this and it wouldn't matter 
    much. So here we copy every file that doesn't have a corresponding param*.txt file.
    
    The algorithm is:
        LIST 1: Look in `infiledir` for files named "param*.txt". Convert these names into 
        corresponding sampled files would look like (ie string replace operations on filenames).
        
        LIST 2: Look for files named "param_processed*.*" in `infiledir`.  
    
    Compare LIST 1 and LIST 2, only copy those in LIST 2 that don't have a corresp. file in LIST 1.
    
    
    Note: comparison of files could be performed succinctly with a Python set().  
    
    Parameters
    ----------
    infiledir : str
        Input directory of parameter files (i.e. `GENERATED_PRIORS` folder).  
    
    outfiledir :str
        Output directory (to which files will be copied).  
    
    NPATCHES : int
        Number of patches in the model.  
    
    Returns
    -------
    Nothing returned; this function copies files.  
    """
    
    # No need to copy if the two folders are the same 
    # (note that shutil.copy gives an error if the infile and outfile are the same).
    if (infiledir == outfiledir):
        print("Directories the same")
        return
    
    # Get list of the original (ie prior range) files (these are of the form param_stuff.txt):
    list_of_original_param_files_including_dirs = glob.glob(join(infiledir, "param*.txt"))
    list_of_original_param_files_without_dirs = {}
    
    for p in range(NPATCHES):
        # Remove directory in pathname
        base = [basename(x) for x in list_of_original_param_files_including_dirs]
        
        # Switch `param_` to `param_processed_patch*`
        base_proc = [x.replace("param_","param_processed_patch"+str(p)+"_") for x in base]
        
        # Switch from a suffix of ".txt" to ".csv"
        base_proc_csv = [x.replace(".txt",".csv") for x in base_proc]
        
        # Store in dict
        list_of_original_param_files_without_dirs[p] = base_proc_csv
    
    # List the processed (ie sampled files) already in the input directory
    list_of_processed_param_files_including_dirs = glob.glob(join(infiledir, "param_processed*.*"))
    
    # Remove the full directory path
    list_of_files_to_copy = [basename(x) for x in list_of_processed_param_files_including_dirs]
    
    # Only copy files which aren't generated from the prior range files (GENERATED_PRIORS folder). 
    # So remove files that have filenames (after conversion) like those of the prior range files.
    for p in range(NPATCHES):
        list_of_files_to_copy = [item for item in list_of_files_to_copy if item not in list_of_original_param_files_without_dirs[p]]
    
    # There are files which don't have the standard format (e.g. param_patchinfo.txt, which becomes
    # param_processed_patchinfo.txt after formatting as there is only one patchinfo file for all
    # the patches). So remove that file and any others like it (add to the list
    # special_files_to_remove if there are any more to add).
    special_files_to_remove = ["param_processed_patchinfo.txt"]
    list_of_files_to_copy = [item for item in list_of_files_to_copy if item not in special_files_to_remove]
    
    # There are also files which aren't of the form param_processed*.csv that need to be copied
    # (e.g. fitting_data_processedtxt)
    special_files_to_add = ["fitting_data_processed.txt"]
    list_of_files_to_copy = list_of_files_to_copy + special_files_to_add
    
    # Finally copy the files that need to be copied:
    for f in list_of_files_to_copy:
        try:
            shutil.copyfile(join(infiledir, f), join(outfiledir, f))
        except:
            print("Warning: file ",f," not found.")


####################################################################################################
####################################################################################################
################################################## Main code #######################################
####################################################################################################
####################################################################################################

# If this file is being run as a script, then do the following:
if __name__=="__main__":

    # BIGNUMBER is just some large number (currently 2**31-1) which is less than the maximum that
    # the system can store (ie sys.maxint). 2**31 is >1 billion so should be OK.
    # Note that this needed to be changed for windows (probably as 32 bit compiler) as otherwise
    # some seeds were negative.
    
    BIGNUMBER = 2**31-1
    DEFAULTSAMPLE  = 1000 # Default number of parameter sets sampled.
    DEFAULTNREP = 1 # Default number of simulations per parameter set
    
    patch_info_file = "param_patchinfo.txt"

    
    filename_list = ["param_init.txt", "param_demographics.txt", "param_times.txt", 
                     "param_HIV.txt", "param_HSV2.txt", "param_cascade.txt", "param_partnerships.txt", "param_PrEP_background.txt", "param_PrEP_intervention.txt"]

    if COUNTRY in ["Zambia","SouthAfrica"]:
        filename_list+= ["param_popart.txt"]
        patch_info_file = "param_patchinfo.txt"

        
    # sys.argv[0] is the filename so just pass the remaining command line arguments.
    processed_args = parse_command_line_arguments(sys.argv[1:])
    [infiledir, outfiledir, ran_seed, nsample, nrep, VERBOSE] = processed_args
    
    utils.check_directory_exists(infiledir)
    utils.check_directory_exists(outfiledir)

    if COUNTRY=="Zimbabwe":
        NPATCHES=1
    elif COUNTRY in ["Zambia","SouthAfrica"]:
        NPATCHES = get_npatches(infiledir)
    
    if not(outfiledir==infiledir):
        utils.check_directory_exists(outfiledir)
        copy_existing_processed_files(infiledir, outfiledir, NPATCHES)
    
    # Verbose output if VERBOSE==1:
    if VERBOSE==1:
        print("Nsample=", nsample)
        print("Nrep=", nrep)
        print("ran_seed=", ran_seed)
    
    # Set the seed for the random number generator to ensure get the same output for the same seed.
    random.seed(ran_seed)
    
    ################################################################################################
    ####### Now can call other parts of code:
    ################################################################################################
    
    # Make an array consisting of nsample random numebrs to be used as seeds for the IBM
    # (ie within the C code).
    C_RANDOM_SEED = [str(random.randint(0,BIGNUMBER)) for i in range(nsample * nrep)]
    
    # We store this in the output folder so we know what seed made this sample.
    randomseedfile = open(join(outfiledir, "python_seed.txt"),"w")
    randomseedfile.write(str(ran_seed))
    randomseedfile.close()
    
    ################################################################################################
    ##########################################  Main code ##########################################
    ################################################################################################
    
    # generates a file containing the key patch info data:
    #if COUNTRY in ["Zambia","SouthAfrica"]:
    write_patch_info(patch_info_file,infiledir,outfiledir,NPATCHES)
    
    # Each element of this list is itself a list (array) containing the values of one variable 
    # ie [x_min, x_min+stepsize, x_min+2*stepsize...x_max] where stepsize = (x_max-x_min)/nsample.
    # This list will be a single list from ALL patches (so we simultaneously sample from each
    # patch).
    lhc_sampling_vars_all = []
    # This list will count the number of variables to be sampled using LHC per file. Note that it
    # is a list (not a dictionary) but we use the same ordering as the list filename_list.
    cumulative_n_lhc_vars_per_file = [0]
    cumulative_n_lhc_vars = 0
    # Now the same for the scenarios:
    cumulative_n_vars_with_scenarios_per_file = [0]
    cumulative_n_vars_with_scenarios = 0
    
    # This will store the header for each file:
    header_all = {}
    for f in filename_list:
        header_all[f] = ""
    
    # This will store the scenarios we need for each variable (for some variables v we may want to
    # run the code with e.g. v=2, v=5, v=10. This will allow us to run multiple scenarios (ie
    # duplicate all non-scenario variables for each combination of scenario variables). Note that
    # the total number of scenarios cannot be too big (otherwise slow to run IBM!)
    scenario_vars = []
    temp_store_output = {}
    
    # Index for each variable in the LHC sample:
    i_lhc_sampling_vars = 0
    
    # Here we go through each input file in turn:
    for f_i, f in enumerate(filename_list):
        if not(os.path.isfile(join(infiledir, f))): # First check file exists:
            utils.handle_error("Error: file "+f+" does not exist. Exiting.")
        
        # Read in the file (this is read in initially as a single string including line breaks),
        # then strip off the last line break, then split the remaining text by line break into a
        # list called text_list. Each line of the original file is then an element in the list at
        # this point.
        infile = open(join(infiledir, f),"r")
        text_list = infile.read().rstrip().split("\n")
        infile.close()
        
        # Each element temp_store_output[f] stores the output from that param file in the format
        # temp_store_output[f][p] = [["CONSTANT",3.7],["LHC",21], ["SCENARIO",5]]. For "CONSTANT"
        # the value of the variable is given. For "LHC" and "SCENARIO" the position of the variable
        # in the corresponding LHC/SCENARIO array is given.
        temp_store_output[f] = {}
        for p in range(NPATCHES):
            temp_store_output[f][p] = []
        
        # Go through each element of the list (`line` takes values text_list[0], text_list[1], etc.)
        for line in text_list:
            if line != "":
                [line_output, line_lhc_sampling_vars, line_scenario_vars, i_lhc_sampling_vars, header] = parse_line(line, i_lhc_sampling_vars, NPATCHES)
                header_all[f] += header
                
                for p in range(NPATCHES):
                    temp_store_output[f][p] += line_output[p]
                
                # Check if the list is non-empty:
                if line_lhc_sampling_vars:
                    lhc_sampling_vars_all += line_lhc_sampling_vars
                    cumulative_n_lhc_vars = cumulative_n_lhc_vars + 1
                
                if line_scenario_vars:
                    scenario_vars += [line_scenario_vars]
                    cumulative_n_vars_with_scenarios = cumulative_n_vars_with_scenarios + 1
        
        cumulative_n_lhc_vars_per_file += [cumulative_n_lhc_vars]
        cumulative_n_vars_with_scenarios_per_file += [cumulative_n_vars_with_scenarios]
    
    [lhc_sampleframe, lhc_stepsize] = make_sampleframe(lhc_sampling_vars_all, nsample)
    lhc = make_lhc(lhc_sampleframe, lhc_stepsize, nsample)
    
    # Create a dictionary for saving the output string for each file.
    dict_outstring = {}
    for f_i, f in enumerate(filename_list):
        dict_outstring[f] = {}
        for p in range(NPATCHES):
            # Note that I've set up cumulative_n_lhc_vars_per_file[] so that the f_i to f_i+1 th
            # elements are the number of latin hypercube vars for that given variable.
            dict_outstring[f][p] = merge_lhc_constants_scenarios_with_reps(temp_store_output[f][p], 
                lhc, scenario_vars, nsample, nrep, C_RANDOM_SEED)
    
    # Counter for the number of parameters
    n_params = 0
    
    # Write param_processed_patch*.csv files
    for f in filename_list:
        for p in range(NPATCHES):
            # Update the filename; it starts with 'param_processed_patch' and ends in 'csv'
            outfilename = f.replace("param", "param_processed_patch"+str(p))
            outfilename = outfilename.replace("txt","csv")
            
            # Write parameter file to disk
            outfile = open(join(outfiledir, outfilename),"w")
            outfile.write(header_all[f]+"\n"+dict_outstring[f][p])
            outfile.close()
            
            # Update the count of the cumulative number of parameters
            n_params += len(dict_outstring[f][p].split("\n")[0].rstrip().split(" "))
            
            if (VERBOSE==1):
                print("Processed parameter input files generated:",n_params,"parameters")
    
    # Copy fertility, mortality and mtct parameter files
    filetags = ["param_mortality.txt","param_mtct.txt"]
    process_fertility_file(infiledir, outfiledir, NPATCHES)
    for f in filetags:
        for p in range(NPATCHES):
            outfilename = f.replace("param", "param_processed_patch" + str(p))
            outfilename = outfilename.replace("txt", "csv")
            try:
                shutil.copy(join(infiledir, f), join(outfiledir, outfilename))
            # eg. src and dest are the same file
            except shutil.Error as e:
                print('Error: %s' % e)
            # eg. source or destination doesn't exist
            except IOError as e:
                print('Error: %s' % e.strerror)
