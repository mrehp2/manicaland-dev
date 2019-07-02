#!/usr/bin/env python3
"""
make_params_folder_files.py takes data from different sources (outputs of analyses of PC/CHiPs raw
data done in R; other prior values/ranges specified in a bunch of text files) and creates the 
param_*.txt files needed by `make_ibm_parameter_sample.py`.

Usage: python make_params_folder_files.py [basedir] [community_numbers] [HPC_SYSTEMS]

basedir : dir
    base directory (e.g. ~/popart-ibm-code/popart-code/IBM_simul/)

community_numbers : int
    This can be any number of integers.  If you are using 2 patches then you only need to pass the
    community number of patch 0. Patch 1 is automatically the arm C community in the same triplet as
    patch 0. Patch 0 can be arm C (in which case both patches are parameterised using the data from
    the same arm C community).  If using >2 patches then you need to enter in each one separately.
    This code does NOT assume that any of the >2 patches are arm C.  Finally if you want to have 2
    patches but both are e.g. arm A (instead of patch 1 being arm C) you can just pass both 
    community numbers as arguments (e.g. python make_params_folder_files.py 2 2).  

HPC_SYSTEMS : str
    The final argument can be one of ["ICHPC","RESCOMP"] which designates if the IBM is to be run on
    an HPC system (ICHPC is at Imperial; RESCOMP is at Oxford).  
"""

import glob, sys, os, filecmp, shutil
from datetime import datetime
from os.path import join
import random,copy

import utilities as utils

# Two python files in the same folder as this file: 
# both contain CHiPs visit-specific functions only.
from make_future_pc_schedule import make_future_pc_visit_schedule
from make_future_chips_visit_data import make_future_chips_visit_data


def get_country(this_community):
    """
    Get the country corresponding to the PopART trial community. 
    
    Communities 1-12 are Zambia, 13-21 are South Africa.
    """
    if this_community <= 12:
        country = "ZAMBIA"
    else:
        country = "SOUTHAFRICA"
        
    return country


def get_country_sentencecase(this_country):
    """
    Changes capitalization of countryname string from capitals to SentenceCase.  
    """
    if this_country=="ZAMBIA":
        return "Zambia"
    elif this_country=="SOUTHAFRICA":
        return "SouthAfrica"
    else:
        utils.handle_error("Error: unknown country name "+this_country+" in get_country_sentencecase(). Exiting.")


def read_community_arm_data(params_basedir):
    """
    Extract data on which community number is in which arm (A,B,C) and return as a dictionary.  
    
    Input data are stored within csv file "community_dictionary_withtrialarm.csv" listing cluster, 
    community name, community number, and arm.  This file is typically stored with the RAW_PRIORS
    folder.  
    
    
    Parameters
    ----------
    params_basedir : str
        Base directory where parameter file (`community_dictionary_withtrialarm.csv`) is stored.  
    
    
    Returns
    -------
    community_arm_data : dict
        Dictionary with keys as community number and values as the arm type (str)
    """
    
    SEP = ","

    # this is an excel csv file containing each community number, name and arm (ie A,B,C)
    try:
        input_file = join(params_basedir, "community_dictionary_withtrialarm.csv")
        community_dictionary_file = open(input_file,"r")
        community_data = community_dictionary_file.read().rstrip().splitlines()
        community_dictionary_file.close()
    except:
        utils.handle_error("Error: file community_dictionary_withtrialarm.csv not found in "+
            "read_community_arm_data(). Exiting.")
    
    header = community_data[0].split(SEP) 
    community_number_col = header.index("Cluster")
    community_arm_col = header.index("Arm")

    # This stores the dictionary translating from community number to arm.
    community_arm_data = {}

    # Now go through all lines except header and pull out community number and arm:
    for line in community_data[1:]:
        data = line.split(SEP)
        arm = data[community_arm_col]
        community_number = int(data[community_number_col])
        community_arm_data[community_number] = arm
    
    return community_arm_data


def get_triplet(this_community):
    """
    Given community number (int or str) return list of all communities in the same triplet (int)
    
    
    Parameters
    ----------
    this_community : int
        Community number of interest
    
    
    Returns
    -------
    this_triplet : list of int
        The 3 community numbers forming the triplet in which `this_community` belongs.  Community 
        numbers 1-3 are triplet 1, 4-6 are triplet 2, ..., 19-21 are triplet 7. 
    
    
    Example
    -------
    # Find the community numbers in the same triplet as community 5
    get_triplet(5)
    >> [4, 5, 6]
    
    # Return triplet for every community
    [get_triplet(i) for i in range(1, 22)]
    """
    triplet_number = (int(this_community) + 2)//3
    this_triplet = [3*triplet_number - 2, 3*triplet_number - 1, 3*triplet_number]
    return this_triplet


def get_control_community_number(intervention_community, community_arm_data):
    """
    Given community number, return the corresponding arm C (control) community number.  
    
    Generally used for finding the community number of a control arm corresponding to a given 
    intervention community.  
    
    
    Parameters
    ----------
    intervention_community : int
        Community number of the intervention community of interest
    
    community_arm_data : dict
        Dictionary (generally output from `read_community_arm_data()`) with keys as community 
        numbers (i.e. 1-21) and values and trial arm designation (i.e. 'A', 'B', 'C').  
    
    
    Returns
    -------
    c : int
        Community number of control arm within the same triplet as `intervention_community`
    
    
    Example
    -------
    get_control_community_number(5)
    >> 4
    # Therefore community 4 is the control arm (arm C) for the triplet that community 5 is in. 
    """
    
    this_triplet = get_triplet(intervention_community)
    
    for c in this_triplet:
        if community_arm_data[c]=="C":
            return c


######### Functions which relate to checking the format of a string (e.g. is it a number?) :

def is_number(s):
    """
    Check if input string is a number or not. 
    Returns 1 if it is a number, and 0 otherwise.
    """
    try:
        float(s)
        return 1
    except ValueError:
        return 0


def is_range(newp):
    """
    Check if input string is a range (ie of the form "a-b", where a and b are numbers) or not. 
    
    Returns 1 if it is a range, and 0 otherwise.
    
    
    Parameters
    ----------
    newp : str
        Input string
    
    
    Returns
    -------
    (int)
        1 if input string is a range of the form "a-b", 0 otherwise
    
    
    Example
    -------
    is_range("9-10")
    >> 1
    
    is_range("9 - 10")
    >> 1
    
    is_range("0.5-0.75")
    >> 1
    
    is_range("a-b")
    >> 0
    """
    
    try:
        x = newp.split("-")
        if len(x)!=2:
            return 0 # Should have exactly two numbers (lower limit and upper limit)
        for i in x:
            if is_number(i)==0:
                return 0 # If not a number, no need to check any other things in x.
    except: # newp is something other than a string.
        return 0
    return 1


def checkvalue(paramtocheck):
    """
    Check that what we read in from the param*.txt file is an allowed input.  
    
    If it is a single thing then it can be a number, a range, or one of the text strings listed 
    below.  This function is used on the `paramvaluelist` that's output after processing a line with
    `parse_line()`.
    
    
    Parameters
    ----------
    paramtocheck : list
        Parameter value stored within a list (of variable length).  The elements of the list are
        usually strings of an int/float or they may be a keyword: one of RANDOMSEED, BY_COUNTRY, 
        BY_COMMUNITY, FROM_CHIPS_R_ANALYSIS, FROM_R_PARTNERSHIP_ANALYSIS_OF_PC0, FROM_CHIPS_FILE, 
    
    
    Returns
    -------
    list or int
        A list of `[1, keyword_or_param]` will be returned if the parameter was recognised, 
        otherwise 0 is returned.  The argument `keyword_or_param` is either one of the above 
        keywords or "Number", "Range", "Multiple numbers and/or ranges" for input parameter strings
        that are respectively numbers (int/float), a range (i.e. '[a-b]'), or a longer list of ints
        or floats (i.e. ['1.2', '6.3', '0.3']).  
    
    
    Example
    -------
    line = "eff_circ_vmmc 0.6  //  Cori 2013 Table S7"
    [paramname, paramvaluelist, comment] = utils.parse_line(line)
    paramvaluelist
    >> ['0.6']
    checkvalue(paramvaluelist)
    >> [1, 'Number']
    
    line = "ran_seed_run RANDOMSEED //  We need to stick a random integer here."
    [paramname, paramvaluelist, comment] = utils.parse_line(line)
    paramvaluelist
    >> ['RANDOMSEED']
    checkvalue(paramvaluelist)
    >> [1, 'Random seed']
    
    line = "time_gt500_to_500_spvl0 [4.56-6.37] // Cori AIDS 2015"
    [paramname, paramvaluelist, comment] = utils.parse_line(line)
    paramvaluelist
    >> ['[4.56-6.37]']
    checkvalue(paramvaluelist)
    >> [1, 'Range']
    
    line = "p_age_m_1j 0.81 0.6 2.2 0 0 0 0 //  Made up numbers"
    [paramname, paramvaluelist, comment] = utils.parse_line(line)
    paramvaluelist
    >> ['0.81', '0.6', '2.2', '0', '0', '0', '0']
    checkvalue(paramvaluelist)
    >> [1, 'Multiple numbers and/or ranges']
    """
    
    if len(paramtocheck)==1:
        p = paramtocheck[0]
        if (p == "RANDOMSEED"):
            return [1, "Random seed"]
        if (p == "BY_COUNTRY"):
            return [1, "BY_COUNTRY"]
        if (p == "BY_COMMUNITY"):
            return [1, "BY_COMMUNITY"]
        if (p == "FROM_CHIPS_R_ANALYSIS"):
            return [1, "FROM_CHIPS_R_ANALYSIS"]
        if (p == "FROM_R_PARTNERSHIP_ANALYSIS_OF_PC0"):
            return [1, "FROM_R_PARTNERSHIP_ANALYSIS_OF_PC0"]
        if (p == "FROM_CHIPS_FILE"):
            return [1, "FROM_CHIPS_FILE"]
        if is_number(p):
            return [1, "Number"]
        if (p[0] == "[" and p[-1] == "]"):
            a = is_range(p[1:-1])
            if a == 1:
                return [1, "Range"]
            else:
                return 0
    else: # Otherwise it is a longer list, so check each element of the list is a number or a range.
        p = paramtocheck[:]
        for i in p:
            # So p is hopefully either a string of numbers or a mix of numbers and ranges [a-b] e.g. 1 2 [3-4]
            if (is_number(i) == 0):
                try:
                    if (is_range(i[1:-1]) == 1):
                        continue
                except: # If we get here than i is not a number or of the form [a-b] so error:
                    utils.handle_error("Error - unknown type for "+p+"\nExiting.") # Note that we don't reach the return now - but maybe remove this later on once we know it is always OK.
                return 0 # If not a number or range, no need to check any other things in x.

        return [1,"Multiple numbers and/or ranges"]

    # The above should have handled any possibility. So if we get here print an error message and exit:
    utils.handle_error(" ".join(paramtocheck)+" unknown type")
    return 0 # Not needed - the handle_error above will kill the program.


######### Functions which relate to file operations (finding files, copying files) :


def check_single_file_and_return_name(file_path_to_try, errormessage):
    """
    Check for [a single] file of the form in the string `file_path_to_try`, return file name
    
    
    Parameters
    ----------
    file_path_to_try : str
        Path to a file; can be a filename, or can include wildcards '*'.  
    errormessage : str
        Error message to print if there are more than one file of the form `file_path_to_try`.  
    
    
    Returns
    -------
    Multiple options
        If >1 file of this type then print `errormessage`, if 0 files of this type then return -1, 
        if exactly 1 type of this file then return the filename (including full path).  
    
    
    Example
    -------
    
    check_single_file_and_return_name("/bin/ls", "This won't be printed ... ")
    >> '/bin/ls'
    
    check_single_file_and_return_name("/bin/l*", "Too many files!")
    # will exit
    
    check_single_file_and_return_name("/bin/non_existent", "Won't be printed ... ")
    >> -1
    """
    possible_files = glob.glob(file_path_to_try)
    if len(possible_files) > 1:
        utils.handle_error(errormessage + "\nExiting")
    if len(possible_files) == 1:
        return possible_files[0] # Return just the filename.
    else:
        return -1 # Signal that no file exists.


def check_whether_data_file_up_to_date(data_filename, source_filename_list, print_warning_only):
    """
    Checks if file `data_filename` is newer than files in list `source_filename_list`
    
    If `data_filename` is newer than all files in `source_filename_list`, return 1, otherwise return
    list of all files newer than `data_filename`.  Time is measured by time at which files were last
    modified on the current system.  
    
    
    Parameters
    ----------
    data_filename : str
        Filename of interest
    source_filename_list : list
        List of filenames to check modification time against `data_filename`.
    print_warning_only : int
        Should only a warning be printed (0)?  Otherwise an error is thrown (1).  No warning or
        error thrown with a value of -1.  
    
    
    Returns
    -------
    files_updated_out_of_sync : list
        List of filenames in `source_filename_list` that 
    
    
    Example
    -------
    import os, time
    all_files = os.listdir('./')
    open("temp_1st", 'w').close(); time.sleep(1)
    open("temp_2nd", 'w').close(); time.sleep(1)
    open("temp_3rd", 'w').close()
    check_whether_data_file_up_to_date("temp_3rd", all_files, True)
    >> 1
    
    check_whether_data_file_up_to_date("temp_1st", all_files, True)
    >> Warning: temp_2nd is more recent than temp_1st.
    >> temp_2nd was modified at 2017-08-15 12:26:51
    >> temp_1st was modified at 2017-08-15 12:26:50
    >> 
    >> Warning: temp_3rd is more recent than temp_1st.
    >> temp_3rd was modified at 2017-08-15 12:26:52
    >> temp_1st was modified at 2017-08-15 12:26:50
    >> 
    >>  ['temp_2nd', 'temp_3rd']
    """
    files_updated_out_of_sync = []

    if not(os.path.isfile(data_filename)): # First check file exists:
            utils.handle_error("Error: file " + data_filename + 
                " does not exist when calling check_whether_data_file_up_to_date(). Exiting.")
    data_file_timeupdated = os.path.getmtime(data_filename)
    
    for f in source_filename_list:
        if not(os.path.isfile(f)):
            utils.handle_error("Error: file " + f + 
                " does not exist when calling check_whether_data_file_up_to_date checking file " +
                data_filename + " Exiting.")
            
        source_file_timeupdated = os.path.getmtime(f)
        if (data_file_timeupdated < source_file_timeupdated):
            files_updated_out_of_sync += [f]
            if print_warning_only == 1:
                
                print("Warning: " + f.split("/")[-1] + " is more recent than " + 
                    data_filename.split("/")[-1] + ".\n" + 
                    f + " was modified at " + 
                    datetime.fromtimestamp(source_file_timeupdated).strftime('%Y-%m-%d %H:%M:%S') + 
                    "\n" + 
                    data_filename + " was modified at " + 
                    datetime.fromtimestamp(data_file_timeupdated).strftime('%Y-%m-%d %H:%M:%S') + 
                    "\n")
            elif print_warning_only == 0:
                utils.handle_error("Error: " + f + " is more recent that " + data_filename+".\n" + 
                f + " was modified at " + 
                datetime.fromtimestamp(source_file_timeupdated).strftime('%Y-%m-%d %H:%M:%S') + 
                "\n" + data_filename + " was modified at " + 
                datetime.fromtimestamp(data_file_timeupdated).strftime('%Y-%m-%d %H:%M:%S') + 
                "\nExiting.")
            elif print_warning_only == -1:
                pass
    
    # if files_updated_out_of_sync is an empty list then not(files_updated_out_of_sync) is true.
    if not(files_updated_out_of_sync):
        return 1
    else:
        return files_updated_out_of_sync


def copy_file_checking_if_exists(original_data_filename, outfilename):
    """
    Check if file `outfilename` exists, otherwise replace it.  
    
    If not, copies the file `original_data_filename` to `outfilename`.
    If it does exist it checks if the files are identical (NB under certain circumstances 
    filecmp.cmp() may not always work but not expecting problems here).
    If they are identical, do nothing else.
    if they aren't identical ask if we should overwrite.  
    
    
    Parameters
    ----------
    original_data_filename : str
        
    outfilename : str
        
        
    Returns
    -------
    Nothing, copies files
    
    Example
    -------
    
    
    """
    # If the outfilename output file exists first check if they are the same.
    if os.path.isfile(outfilename):
        # If files not the same then check if we want to overwrite:
        if not(filecmp.cmp(original_data_filename, outfilename)):
            response = raw_input(original_data_filename + " and " + outfilename + 
                " are not identical. Overwrite " + outfilename + " (y/n) ?").lower()
            
            # Keep asking until response is one of "y" and "n":
            while not(response in ["y","n"]):
                response = raw_input("Please enter y/n only: ").lower()
                
            if response=="y":
                print("Overwriting " + outfilename)
                shutil.copyfile(original_data_filename, outfilename)
                return 
            else:
                print("Not overwriting " + outfilename + ". Please check this is OK.")
                return
        else:
            return
    # if the file does not already exist then copy it:
    else:
        try:
            shutil.copyfile(original_data_filename,outfilename)
        except:
            outputfiledir = "/".join(outfilename.split("/")[:-1])
            utils.handle_error("Error: trying to copy " + original_data_filename + " to " + outfilename + 
            ".\nCheck if input file " + original_data_filename + " and output folder " + 
            outputfiledir + " exist.\nExiting")
        return


def copy_chips_file_removing_whitespace_and_store_start_end_times(original_data_filename, outfilename):
    """
    Copies specified file (overwriting existing file), removes trailing whitespace in copied file.
    
    This is needed for the CHiPs files because Anne's R script adds extra whitespace at the end but
    the IBM is set up to count lines (but not to check if they are blank) so this causes the IBM to 
    stop.  Function can write to a list of files (not just one).  
    Function also pulls out the start and end times of
    """
    # check the input file exists:
    if os.path.isfile(original_data_filename):
        infile = open(original_data_filename,"r")
        data = infile.read().rstrip()
        start_time = data.splitlines()[1].split()[0]
        end_time = data.splitlines()[-1].split()[0]
        infile.close()
    else:
        utils.handle_error("Error: Cannot find file " + original_data_filename + ". Exiting")
    outfile = open(outfilename,"w")
    outfile.write(data)
    outfile.close()
    
    return [start_time, end_time]


###############################################################################################
########### Now functions that load up specific data (ie things used to generate param ranges):
###############################################################################################


def read_country_data(country, country_params_dir):
    """
    Read country data for a given community, return dictionary with keys as parameter names.
    
    
    Parameters
    ----------
    country : str
        
    country_params_dir : str
        Directory 
    
    
    Returns
    -------
    country_data : dict
        Dictionary with keys as ... and values as ... 
    
    
    Example
    -------
    country_params_dir = read_country_data("ZAMBIA", country_params_dir)
    >>
    """
    
    # This will store the country data (the keys for this dictionary are the parameter names).
    country_data = {}
    
    filename = join(country_params_dir, "param_by_country_" + country + ".txt")
    linedata = utils.parse_file(filename)
    
    # Go through the file line-by-line:
    for l in linedata:
        
        [paramname, paramvaluelist, comment] = utils.parse_line(l)
        
        # Convert list to a string with each element separated by a space.
        country_data[paramname] = ' '.join(paramvaluelist)
        country_data[paramname] = utils.add_comment(country_data[paramname], comment)
    
    return country_data


def get_community_level_files(community_param_dir):
    """
    Find all files of the form `param*.txt` in community dir return them as a list.
    
    Note: could use os.path.basename() here instead of str.replace().
    
    
    Parameters
    ----------
    community_param_dir : str
        Directory of data ... 
    
    
    Returns
    -------
    list_of_files_without_dirs : list (of strs)
    
    
    Example
    -------
    
    
    """
    list_of_files_including_dirs = glob.glob(join(community_param_dir, "param*.txt"))
    list_of_files_without_dirs = [x.replace(community_param_dir,"") for x in list_of_files_including_dirs]
    return list_of_files_without_dirs


def read_community_data(files_by_community, community_param_dir):
    """
    Read in the community-level data.
    
    
    Parameters
    ----------
    files_by_community : 
        
    community_param_dir : str
        
    
    
    
    Returns
    -------
    community_data : dict
    
    
    Example
    -------
    
    read_community_data(files_by_community, community_param_dir)
    
    """
    
    # This will store the community data (the keys for this dictionary are the parameter names).
    community_data = {}
    
    for f in files_by_community:
        
        linedata = utils.parse_file(community_param_dir+f)
        # Go through the file line-by-line:
        for l in linedata:
            # Pull out the parameter name, the value (or range etc) and any comments on that line.
            [paramname, paramvaluelist, comment] = utils.parse_line(l)
            
            # Convert list to str where each list element is separated by a space.
            community_data[paramname] = ' '.join(paramvaluelist)
            community_data[paramname] = utils.add_comment(community_data[paramname], comment)
        
    return community_data


# Read in the time to ART data for people who test HIV+ with CHiPs. This is based on Anne's analysis of CHiPs data (where we record when someone is first recorded HIV+ by CHiPs and then the time from first visit to starting ART). The R script which generates the data we use here is in ~/Dropbox/PoPART/Data\:Stats/CHiPs\ data/R/CodeForSurvivalAnalysis.R
# This function reads in the output for a given community/round that was created by Anne's script and creates a dictionary storing the required outputs.
# At present we fit a biphasic exponential (each person has a probability p_fast that they have time to starting ART from exponential with mean time t_fast, otherwise they are exponenial with mean t_slow. This corresponds to having a population with 'fast' and 'slow' progressors that seems to fit the data well.
# Because R1 ChiPs was a learning experience we found (with Sian) that the rate of ART initiation improved over time; we therefore split R1 into 6 "Quarters", so 6*3=18 parameters. R2 onwards are by round (so 3 parameters per round).
def read_time_to_art_params(country, round, time_to_art_dir):
    """
    
    
    Parameters
    ----------
    country : str
        Country of interest ('Zambia' or 'SouthAfrica')
    round : int
        CHiPs round number of interest
    time_to_art_dir : str
        Directory
    
    Returns
    -------
    
    Example
    -------
    
    """
    # Convert the country to sentencecase (ie first character upper case, rest lower case).
    country_sentencecase = get_country_sentencecase(country)
    # Hack so that file names for SA will find the correct files
    if country_sentencecase == "SouthAfrica":
        country_sentencecase = "SA"
    
    # Open the data file. Note that at present (Jan 2017) we only have the analysis for Zambia:

    # The following is a fix for a couple of issues. Firstly we have multiple rounds, but data only for a subset (so we first check if the correct data file exists for the given round, then if not we use the data file from the previous round). Secondly CHiPs R1 had different rates every 3 months so we fit separate parameters to each "quarter" - and the filename is "TwoExpFitsByQuarter_Zambia.txt", while for later rounds it is TwoExpFits_Zambia.txt.
    # But basically this reads in the data from the appropriate place.
    r = round
    while (r > 0):
        art_dir = join(time_to_art_dir, "Round" + str(r), "TimeToARTInitiation")
        file_pattern = "TwoExpFits*" + country_sentencecase + ".txt"
        
        err_msg = "Ambiguous choices for time to ART parameters for round " + str(r) + \
            "\nPlease ensure only one file of the form TwoExpFits*.txt in the appropriate dir."
        
        possible_filename = check_single_file_and_return_name(join(art_dir, file_pattern), err_msg)
        if not(possible_filename == -1):
            # Give it a meaningful name now we have found the right filename.
            time_to_art_filename = possible_filename 
            break
        r = r - 1
    
    # Just get the actual filename without the file path:
    filename_no_dir = time_to_art_filename.split("/")[-1]
    
    # Again we need a fix for the fact that R1 has different rates every 3 months:
    if (filename_no_dir == "TwoExpFits_" + country_sentencecase + ".txt"):
        datatype = "ByRound"
    elif (filename_no_dir == "TwoExpFitsByQuarter_" + country_sentencecase + ".txt"):
        datatype = "ByQuarter"
    else:
        utils.handle_error("Unknown file type for time to ART parameters " + filename_no_dir + 
            ".\nOnly possibilities allowed are TwoExpFits_" + country_sentencecase + ".txt" + 
            " and TwoExpFitsByQuarter_"+country_sentencecase+".txt\nExiting.")
    
    # Now read in the data:
    infile = open(time_to_art_filename,"r")
    time_to_art_unprocesseddata = infile.read().rstrip().split("\n")
    infile.close()
    
    # Use the first row of the file to find out what each column means:
    header = time_to_art_unprocesseddata[0].split()
    
    # Data is modelled as a biphasic exponential - so there is a probability that someone is a fast
    # initiator (if not they are a slow initiator) and a fast and slow rate for initiation.
    # Gets central estimate for proportion of individuals who are fast initiators on ART.
    
    # The "+2" is because the first 2 columns (quarter, year) don't have headers.
    
    if datatype == "ByRound":
        # Files with the same parameters for the whole year don't have the "Q1" etc columns.
        n_initial_columns = 1
    elif datatype == "ByQuarter":
        # Files with different parameters each "quarter" have a column giving the quarter e.g. "Q1"
        n_initial_columns = 2
    
    # Get the correct column numbers for each of the data we want. 
    # Right now we ignore the CIs for each data but can easily modify to get this:
    column_PropFastInitiators = header.index("PropFastInitiators") + n_initial_columns
    column_dailyRatehigh = header.index("dailyRate1") + n_initial_columns
    column_dailyRatelow = header.index("dailyRate2") + n_initial_columns
    
    # Stores for the processed outputs
    proportions_string = ""
    t_high_string = ""
    t_low_string = ""
    
    # Count the number of time periods that we split the round into to get params.
    n_time_periods = len(time_to_art_unprocesseddata[1:])
    
    use_dp = 1
    
    for line in time_to_art_unprocesseddata[1:]:
        # Now extract the data (note that at this point these are string variables, not floats:
        [p_fast,gamma_high,gamma_low] = [line.split()[column_PropFastInitiators],line.split()[column_dailyRatehigh],line.split()[column_dailyRatelow]]
        
        if (use_dp==0): # Output full output from the text file that R used.
            t_high_string += str((1.0/float(gamma_high))/365.0)+ " " # Convert from daily rate to time to start ART, and then convert back to string.
            t_low_string  += str((1.0/float(gamma_low))/365.0) + " " # Convert from daily rate to time to start ART.
            proportions_string += p_fast+" " # p_fast was always a string so no need to convert variable type.
        else:           # Earlier versions only used n dp
            t_high_string += "{0:.9f}".format((1.0/float(gamma_high))/365.0)+ " " # Convert from daily rate to time to start ART, and then convert back to string.
            t_low_string  += "{0:.9f}".format((1.0/float(gamma_low))/365.0) + " " # Convert from daily rate to time to start ART.
            proportions_string += "{0:.9f}".format(float(p_fast))+" " # p_fast was a string so need to convert to float and back to string.

    # 'blurb' is the comment printed after the end of the data.
    if (r==round):
        blurb = "// Based on ZAMBIA analyses of data for round "+str(round)+": see file /Dropbox/PoPART/Data:Stats/CHiPs data/Round"+str(round)+"/TimeToARTInitiation/"+filename_no_dir
    else:
        blurb = "// assuming same as round"+str(r)+" for now"

    proportions_string += blurb + "\n" 
    t_high_string += blurb + "\n"
    t_low_string += blurb + "\n"




    # Now return a dictionary containing all the necessary data:
    return {"p_start_art_popart_round"+str(round)+"_mean_fast":proportions_string,"t_start_art_popart_round"+str(round)+"_mean_fast":t_high_string,"t_start_art_popart_round"+str(round)+"_mean_slow":t_low_string,"n_time_periods_round"+str(round):n_time_periods}


def read_partnership_data(country, pc0_partnership_dir):
    """
    This function reads in the data generated from the raw PC data by a knitr document written by 
    Anne:
    ~/Dropbox/PoPART/Data\:Stats/PC\ Data\ Downloads/15-12-2016_PC0_NEWFINAL/R/partnerships/ExtractPartnershipParamFromPC0.Rnw
    
    
    Parameters
    ----------
    country : str
        Country of interest
    pc0_partnership_dir : str
        Directory housing PC0 partnership data
    
    
    Returns
    -------
    partnership_data : dict
        Dictionary of partnership data
    
    """
    # Determine whether check_whether_data_file_up_to_date() prints warning (if 1) or exits (if 0).
    print_warning_only = -1
    
    # This will store the partnership data (the keys for this dictionary are the parameter names).
    partnership_data = {}
    
    infilename = join(pc0_partnership_dir, "R", "partnerships")
    if country == "ZAMBIA":
        infilename = join(infilename, "param_partnerships_fromPC0_Za.txt")
    elif country == "SOUTHAFRICA":
        infilename = join(infilename, "param_partnerships_fromPC0_SA.txt")
    else:
        utils.handle_error("Error: Unknown country " + country + "\nExiting.")
    
    pc0_source_files = [
        join(pc0_partnership_dir, "R", "DataCleaning", "Read_PC0_final_data.R"),
        join(pc0_partnership_dir, "R", "DataCleaning", "PC0.yml"),
        join(pc0_partnership_dir, "R", "DataCleaning", "PC0_partner.yml"),
        join(pc0_partnership_dir, "R", "DataCleaning", "RenameColMergedPC0.yml"),
        join(pc0_partnership_dir, "R", "DataCleaning", "recipes.yml"),
        join(pc0_partnership_dir, "RawData", "PC0.csv"),
        join(pc0_partnership_dir, "RawData", "PC0_partner.csv"),
        join(pc0_partnership_dir, "MergedAndCleanData", "Recoded_PC0_merged_dat.rds"), 
        join(pc0_partnership_dir, "MergedAndCleanData", "Recoded_PC0_merged_dat.rds"), 
        join(pc0_partnership_dir, "R","partnerships", "ExtractPartnershipParamFromPC0.Rnw")]
    
    #check = check_whether_data_file_up_to_date(infilename, pc0_source_files, print_warning_only)
    linedata = utils.parse_file(infilename)
    for l in linedata:
        
        # Pull out the parameter name, the value (or range etc) and any comments on that line.
        [paramname,paramvaluelist,comment] = utils.parse_line(l)
        
        # Check data type is OK
        [isok,typeofinput] = checkvalue(paramvaluelist)
        if isok:
            # This takes the list and converts it to a string where each list element is separated
            # by a space.
            partnership_data[paramname] = ' '.join(paramvaluelist)
            partnership_data[paramname] = utils.add_comment(partnership_data[paramname],comment)
        else:
            utils.handle_error("Error in read_partnership_data() for line " + l + "\nExiting\n")
        
    return partnership_data


####################################################################################################
# Generate specific files (either using known data or copying files directly.
# Files we generate here are param_patchinfo.txt, 
####################################################################################################


def extract_timestep_from_ibm_code(ibm_code_dir):
    """
    Read in directly from the IBM C source code what the timestep used is.
    
    Parameters
    ----------
    ibm_code_dir : str
    
    """
    try:
        constants_file = open(join(ibm_code_dir, "constants.h"),"r")
    except:
        utils.handle_error("Error: Cannot find IBM source code file constants.h in extract_timestep_from_ibm_code(). Exiting")
    constants_text = constants_file.read()
    constants_file.close()
    i = constants_text.index("#define N_TIME_STEP_PER_YEAR")
    timestep_line = constants_text[i:].splitlines()[0]
    n_timesteps_per_year_string = timestep_line.split("/*")[0].split()[-1]
    try:
        n_timesteps_per_year = int(n_timesteps_per_year_string)
    except:
        utils.handle_error("Error: n_timesteps_per_year has to be an integer. When reading from constants.h file it was found to be "+n_timesteps_per_year_string)
    if not(n_timesteps_per_year==48):
        print("WARNING: NUMBER OF TIMESTEPS READ FROM constants.h IBM SOURCE FILE IS NOT 48. PLEASE CHECK")
    return n_timesteps_per_year
    

# Pulls out the times that the round started and finished from the CHiPs data file.
def format_raw_chips_times(chips_round_start_raw, chips_round_end_raw, ibm_code_dir):
    
    NTIMESTEPSPERYEAR = extract_timestep_from_ibm_code(ibm_code_dir)
    chips_end_round_finished = float(chips_round_end_raw) + 1.0/NTIMESTEPSPERYEAR
    return [chips_round_start_raw,chips_end_round_finished]


def copy_chips_visit_schedule(this_community, this_patch, chips_data_root_dir, output_dir,
        ibm_code_dir):
    """
    Copies the Chips R1-4 datasets that Anne makes (using the script ReadChipsDataExtract.R from 
    Dropbox/PoPART/Data:Stats/CHiPs data/R/) into the correct directory (renaming them and removing
    trailing whitespace that would break the IBM).
    
    
    Parameters
    ----------
    this_community
    this_patch
    chips_data_root_dir
    output_dir
    ibm_code_dir
    scenario :str 
        Scenario of interest.  Default "Central_Chips".  
    
    Returns
    -------
    list of the form [chips_round_start_times, chips_round_end_times, chips_timings]
    
    chips_round_start_times
    chips_round_end_times
    chips_timings
    """
    chipsdatafiles = {}
    chips_round_start_times = {}
    chips_round_end_times = {}
    
    if (community_arm_data[this_community]=="C"):
        utils.handle_error("Can't call copy_chips_visit_schedule for arm C community. Exiting")
    
    for r in range(1, NCHIPSROUNDS + 1):
        chips_scenario_root = join(chips_data_root_dir, "Round"+str(r), "TimeOfChipsVisits")
        
        chipsfile = "Chips_schedule_by_age_and_gender_round" + str(r) + \
            "_community" + str(this_community) + ".txt"
        
        chipsdatafiles[r] = join(chips_scenario_root, chipsfile)
    
    chips_timings = {}
    for r in range(1, NCHIPSROUNDS + 1):
        
        chips_outfilename = join(output_dir, \
            "param_processed_patch" + str(this_patch) + "_chipsuptake_round" + str(r) + ".csv")
        
        # Copy the file chipsdatafiles[r] to everything in the file chips_outfilename, and from
        # that file also get the start and end times of the round.
        
        [chips_round_start_raw, chips_round_end_raw] = \
            copy_chips_file_removing_whitespace_and_store_start_end_times(chipsdatafiles[r],
                chips_outfilename)
        
        [chips_round_start_times[r], chips_round_end_times[r]] =\
            format_raw_chips_times(chips_round_start_raw,
                chips_round_end_raw, ibm_code_dir)
        
        chips_timings["CHIPS_YEAR"+str(r)+"_START"] = chips_round_start_times[r]
        chips_timings["CHIPS_YEAR"+str(r)+"_END"] = chips_round_end_times[r]
    
    return [chips_round_start_times, chips_round_end_times, chips_timings]


def copy_pc_visit_schedule(this_community,patch_number,input_dir,output_dir):
    """
    Copies the PC0 visit schedule from the relevant data directory. This PC0 schedule file is 
    created by the file GeneratePC0schedule.R  (I think?)  Anne wrote that 
    pulls the times people were visited direct from the PC0 csv dataset.
    """
    infilename = join(input_dir, "PC0_schedule_by_HIV_status_age_and_gender_community"+str(this_community)+".csv")
    outfilename = join(output_dir, "param_processed_patch"+str(patch_number)+"_PC0_community"+str(this_community)+".csv")
    
    copy_file_checking_if_exists(infilename, outfilename)
    make_future_pc_visit_schedule(PCRANDOMSEED, outfilename, this_community, patch_number, 
        output_dir, NPCROUNDS)


def copy_fertility_file(country, input_dir, output_dir):
    """
    Copy the fertility data file from the source directory input_dir
    
    Parameters
    ----------
    country : str
    input_dir : str
    output_dir : str
    
    Returns
    -------
    Nothing, copies files
    """
    # Convert the country to sentencecase (ie first character upper case, rest lower case).
    country_sentencecase = get_country_sentencecase(country)
    
    # This is the file we are copying:
    fertility_data_file = join(input_dir, country_sentencecase + "Fertility.csv")
    
    # This is what we are copying to
    fertility_outfilename = join(output_dir, "param_fertility.txt")
    
    copy_file_checking_if_exists(fertility_data_file, fertility_outfilename)


def copy_mortality_file(country, mortality_sweave_code_dir, mortality_unpd_data_dir, output_dir):
    """
    Copies the mortality file generated using Mike's script EstimatingRatesFromUNPD.Rnw
    (which analyses a csv downloaded from UNPD).
    
    Parameters
    ----------
    country : str
    mortality_sweave_code_dir : str
    mortality_unpd_data_dir : str
    output_dir : str
    
    Returns
    -------
    
    """
    # Convert the country to sentencecase (ie first character upper case, rest lower case).
    country_sentencecase = get_country_sentencecase(country)

    # This is where the file we are copying is (and the sweave file that made it):
    # mortality_sweave_code_dir =
    # "SOURCED_FROM_LITERATURE/Analysing_UNPD_estimates_demographic_params/"
    # This is the file we are copying:
    mortality_data_file = join(mortality_sweave_code_dir, country_sentencecase + "_mortalityByAgeCoefficients.txt")
    
    # determines whether check_whether_data_file_up_to_date() prints warning (if 1) or exits (if 0).
    print_warning_only = -1
    
    # We check if any of the above have been modified more recently than the resulting data file:
    data_file_depends_on = [
        join(mortality_sweave_code_dir, "EstimatingRatesFromUNPD.Rnw"),
        join(mortality_unpd_data_dir, "SouthAfricaMortalityMen.csv"),
        join(mortality_unpd_data_dir, "SouthAfricaMortalityWomen.csv"),
        join(mortality_unpd_data_dir, "ZambiaMortalityMen.csv"),
        join(mortality_unpd_data_dir, "ZambiaMortalityWomen.csv"),
        join(mortality_unpd_data_dir, "SouthAfricaFertility.csv"),
        join(mortality_unpd_data_dir, "ZambiaFertility.csv")]
    
    check = check_whether_data_file_up_to_date(mortality_data_file,data_file_depends_on,print_warning_only)
    if (not(check==1) and print_warning_only==0):
        print(check + " is more recent that " + mortality_data_file + 
            ". Running sweave to generate file")
        utils.run_sweave("EstimatingRatesFromUNPD.Rnw",mortality_sweave_code_dir)
    else:
        if VERBOSE_OUTPUT == 1:
            print(mortality_data_file + " up to date")
    
    # This is what we are copying to
    mortality_outfilename = join(output_dir, "param_mortality.txt")
    
    copy_file_checking_if_exists(mortality_data_file,mortality_outfilename)


def write_patchinfo(communities, output_dir, community_arm_data):
    """
    Generate the file `param_patchinfo.txt` using the list of communities and the data 
    we pulled from file `community_dictionary_withtrialarm.csv` using `read_community_arm_data()`.
    
    
    Parameters
    ----------
    communities : 
    output_dir : str
    community_arm_data : dict
    
    
    Returns
    -------
    Nothing, writes the file `param_patchinfo.txt` to the directory `output_dir`.
    
    
    Example
    -------
    
    
    """
    
    # Dictionary to convert from A/B/C to 1/2/0 (as used in IBM: 0=ARM C, 1=ARM A, 2=ARM B)
    arm_numbers = {"A":"1", "B":"2", "C":"0"}
    
    patchinfo_cluster_text = "cluster_number ("
    patchinfo_arm_text = "trial_arm ("
    for c in communities:
        community_arm = community_arm_data[c]
        community_arm_number = arm_numbers[community_arm]
        patchinfo_cluster_text += str(c)+","
        patchinfo_arm_text += community_arm_number+","
    
    # Remove the trailing commas from each line
    patchinfo_cluster_text = patchinfo_cluster_text.rstrip(",")
    patchinfo_arm_text = patchinfo_arm_text.rstrip(",")
    
    # Now add extra info at end of each line
    patchinfo_cluster_text += ") // Cluster 1 is arm B, cluster 2 is arm A.\n"
    patchinfo_arm_text += ")     // 0=ARM C, 1=ARM A, 2=ARM B"
    
    outfile = open(join(output_dir, "param_patchinfo.txt"),"w")
    outfile.write(patchinfo_cluster_text + patchinfo_arm_text)
    
    outfile.close()



####################################################################################################
######### Only needed for running on HPC (ie if GETHPCFILES==1)
####################################################################################################


def check_future_art_file(input_dir):
    """
    """
    art_filename = "start_art_popart_round34.csv"
    
    art_infile = input_dir + "start_art_popart_round34.csv"
    #art_outfile = output_dir + "start_art_popart_round34.csv"
    #outputdir = "HPC/RESCOMP/MAKE_SCENARIOS_GOODFITS/"

    data_file_depends_on = [input_dir+"CodeForSurvivalAnalysis.R"]

    # Whether check_whether_data_file_up_to_date() prints warning (if 1) or exits (if 0).
    # or prints to warning (-1)
    print_warning_only = -1
    check = check_whether_data_file_up_to_date(art_infile,data_file_depends_on,print_warning_only)
    if (not(check==1) and print_warning_only==0):
        print(check+" is more recent that "+art_infile+". Exiting\n")
        sys.exit(1)
    else:
        if VERBOSE_OUTPUT==1:
            print(art_infile+" up to date")


####################################################################################################
######### Main code: ###############################################################################

# If this script is run from the command line, the following code will run automatically:
if __name__=="__main__":
    NCHIPSROUNDS = 3
    NPCROUNDS = 4
    CHIPSDATAROUNDS = 3
    
    # Used in generating PC12-36 visit schedule to add a small amount of randomness 
    # (not necessary I think but a simple way to implement)
    PCRANDOMSEED = 20
    
    COMMAND_LINE_ARGS = sys.argv[:]
    if len(COMMAND_LINE_ARGS)<=2:
        utils.handle_error("Need to pass community number when calling "+__file__+". Exiting")
    
    initial_dir = COMMAND_LINE_ARGS[1]
    # Check directory exists. If so then move to that directory:
    utils.check_directory_exists(initial_dir)
    os.chdir(initial_dir)
    
    # Now work out if we're running this to generate a tar archive for HPC or not:
    HPC_SYSTEMS = ["ICHPC","RESCOMP"]
    if COMMAND_LINE_ARGS[-1] in ["LAPTOP"]+HPC_SYSTEMS:
        # Get extra files needed for HPC run if needed:
        if COMMAND_LINE_ARGS[-1] in HPC_SYSTEMS:
            GETHPCFILES = 1
            HPC_SYSTEM=COMMAND_LINE_ARGS[-1]
        else:
            GETHPCFILES = 0
        COMMAND_LINE_ARGS = COMMAND_LINE_ARGS[:-1]
        #print COMMAND_LINE_ARGS
    
    else: # default - don't get HPC files.
        GETHPCFILES = 0
    
    try:
        all_communities = [int(x) for x in COMMAND_LINE_ARGS[2:]]
    except:
        utils.handle_error("All arguments passed to make_params_folder_file.py must be integers. Exiting")
    for x in all_communities:
        if (x<1 or x>21):
            utils.handle_error("All arguments passed to "+__file__+" must be in the range 1-21. Exiting")
    
    VERBOSE_OUTPUT = 0 # print out extra information.
    
    ########################################################################################
    ########### Folders used by the code:
    ########################################################################################
    
    # When opening a file python can't apparently use '~' directly. But os.path.expanduser('~')
    # gives the expanded path (e.g. /home/me).
    homedir = os.path.expanduser('~')
    
    # This is the directory containing all the input stuff we need to generate the parameters:
    params_basedir = join(".", "data","RAW_PRIORS")
    
    # This contains the subfolders of the input community-level parameters:
    params_community_basedir = join(params_basedir, "PARAM_SOURCES")
    
    # We read in the IBM code at one point to check specific things.
    # make_params_folder_files.py now lives in the same directory as the IBM code. 
    ibm_code_dir = join(".", "src")
    
    # template_dir contains a list of all the files that *SHOULD* be created. 
    # Used as a check that everything is made as it should be.
    template_dir = join(params_basedir, "TEMPLATE")
    
    # This is where we store the file containing the parameters that vary by country 
    # (ie differ between Zambia and South Africa but not between communities in the same country).
    country_params_dir = join(params_basedir, "PARAM_SOURCES")
    
    # This is where we write to. Always make the directory take the name of the patch 0 community
    output_dir = join(".", "data", "GENERATED_PRIORS", "PARAMS_COMMUNITY"+str(all_communities[0]))
    
    # Mortality and fertility data is based on UNPD estimates (with mortality estimates removing
    # HIV mortality by fitting a curve to times outside of main impact of HIV epidemic based on
    # analysis from Sweave file - see IBM model documetation for full explanation).
    fertility_data_dir = join(homedir,"Dropbox","PoPART","IBM Model Background","Demographic data")
    mortality_unpd_data_dir = fertility_data_dir
    
    mortality_sweave_code_dir = join(params_basedir, "SOURCED_FROM_LITERATURE",
        "Analysing_UNPD_estimates_demographic_params")
    
    ####### Analysis of ChiPs data:
    # Determines parameters for time to start ART. Data is stored in subdirectories by round.
    time_to_art_dir = join(homedir, "Dropbox","PoPART", "Data:Stats", "CHiPs data")
    
    # Determines parameters for time when people are visited by CHiPs.  Data is stored in
    # subdirectories by round.
    time_of_chips_visits_dir = join(homedir, "Dropbox","PoPART", "Data:Stats", "CHiPs data")
    
    # Analysis of PC0 partnership data:
    pc0_partnership_dir = join(homedir, "Dropbox", "PoPART", "Data:Stats", "PC Data Downloads", 
        "15-12-2016_PC0_NEWFINAL")
    # Analysis of PC0 visit schedule (when PC participants are seen by by PC interviewer):
    pc0_visit_schedule_dir = join(homedir, "Dropbox","PoPART","Data:Stats","PC Data Downloads",
        "15-12-2016_PC0_NEWFINAL","R","PC0schedules")
    
    utils.check_directory_exists(params_basedir)
    utils.check_directory_exists(ibm_code_dir)
    utils.check_directory_exists(template_dir)
    utils.check_directory_exists(fertility_data_dir)
    utils.check_directory_exists(mortality_sweave_code_dir)
    utils.check_directory_exists(mortality_unpd_data_dir)
    utils.check_directory_exists(time_to_art_dir)
    utils.check_directory_exists(time_of_chips_visits_dir)
    utils.check_directory_exists(pc0_partnership_dir)
    utils.check_directory_exists(pc0_visit_schedule_dir)
    utils.check_directory_exists_and_create(output_dir)
    
    # Here we generate the list of files which will eventually be copied:
    # all param files need to be named like this for now.
    template_files = glob.glob(join(template_dir, "param*.txt"))
    
    # For now we keep these in template_dir but may remove.
    exceptions = ["param_mortality.txt", "param_fertility.txt", "param_patchinfo.txt"]
    for e in exceptions:
        try:
            template_files.remove(join(template_dir, e))
        except:
            utils.handle_error("Warning - file " + e + " not in " + template_dir + "." +
            "For now exiting - maybe change code later on?")
    
    # Now set up patch info:
    # Firstly look up which arm each of the 21 communities belongs to:
    community_arm_data = read_community_arm_data(params_basedir)
    
    if len(all_communities)==1:
        MAKE_SIMULATED_CONTROL=1 # We use the same parameters as in the community given in "community_arm_data" for the control. Only difference is in param_patchinfo.txt where we pretend that it is the control arm number.
        armc_community_number = get_control_community_number(all_communities[0],community_arm_data)
        all_communities += [armc_community_number]
    else:
        MAKE_SIMULATED_CONTROL=0 

    # Create the file param_patchinfo.txt:
    write_patchinfo(all_communities,output_dir,community_arm_data)

    # Now we generate all the necessary files for each patch:
    for patch_number in range(len(all_communities)):
        if(MAKE_SIMULATED_CONTROL == 1):
            # We use inputs from the patch 0 community (so identical parameters)
            input_community = all_communities[0]
            
            # But use the visit schedule from current community (so there can be some difference)
            pc_schedule_community = all_communities[patch_number]
        else:
            input_community = all_communities[patch_number]
            pc_schedule_community = all_communities[patch_number]
        
        country = get_country(input_community)
        
        copy_pc_visit_schedule(pc_schedule_community, patch_number, \
            pc0_visit_schedule_dir, output_dir)
        
        # This is where we store the community parameters and the fitting_data_processed.txt file.
        community_param_dir = join(params_community_basedir, 
            "PARAM_BY_COMMUNITY_" + str(input_community))
        
        utils.check_directory_exists(community_param_dir)
        
        # Now copy the fitting data file. This isn't used for much in the IBM - mainly it ensures that we are between 0 and about 45% HIV prevalence at the start of CHiPs 
        # which is quite a weak constraint. This file (and the corresponding code in the IBM) might be removed at some point (can also be used to implement target fitting).
        # Note that we only need one file (so use the one from the first patch (ie patch=0):
        if patch_number == 0:
            copy_file_checking_if_exists(\
                join(community_param_dir, "fitting_data_processed.txt"),\
                join(output_dir, "fitting_data_processed.txt")\
                )
        
        # Generate/copy special files:
        copy_fertility_file(country, fertility_data_dir, output_dir)
        copy_mortality_file(country, mortality_sweave_code_dir, mortality_unpd_data_dir, output_dir)
        
        # These relate to when people are visited by CHiPs. copy_chips_visit_schedule() uses
        # analysis from Anne's knitr 
        # to get this from the raw CHiPS line data Sian provides.
        # These files also give us the start/end times of the CHiPs round that we need for
        # param_times.txt
        if community_arm_data[input_community] in ['A', 'B']:
            [chips_round_start_times, chips_round_end_times, chips_timings] =\
                copy_chips_visit_schedule(input_community, patch_number, \
                time_of_chips_visits_dir, output_dir, ibm_code_dir)
        else:
            
            # If this is an arm C community, then the CHiPs schedule from arm A in the same triplet
            triplet = get_triplet(input_community)
            
            for t in triplet:
                if community_arm_data[t] == 'A':
                    arm_a_community = t
            
            [chips_round_start_times, chips_round_end_times, chips_timings] =\
                copy_chips_visit_schedule(arm_a_community, patch_number, \
                time_of_chips_visits_dir, output_dir, ibm_code_dir)
        
        # Given the CHiPS visit schedule from R1-R3 copied in copy_chips_visit_schedule(),
        # extrapolate to post-trial CHiPs visits under the assumption that PopART-style testing
        # is adopted everywhere post-trial.
        make_future_chips_visit_data(output_dir, patch_number, round_to_extrapolate_from = 3)
        
        # Read in the country-level data:
        country_level_data = read_country_data(country, country_params_dir)

        # First get a list of the files that are in the community-level directory:
        files_by_community = get_community_level_files(community_param_dir)

        # Read in the community-level data:
        community_level_data = read_community_data(files_by_community, community_param_dir)

        # Read in the output of the knitr analysis of PC0 data:
        partnership_data = read_partnership_data(country, pc0_partnership_dir)

        # Now read in "time to starting ART after CHiPs visit" parameters. The files we read in are generated by an R script that carries out an analysis of the raw CHiPs line data (the R script is from Anne, the raw data provided by Sian).
        time_to_art_params = {}
        # We want to work out how many time periods are in each round. Right now it is 6 1 1 1 (ie 6 periods in R1, then one period in each other round) but do this to keep flexibility.
        n_time_periods_art_popart_per_round_string = ""
        for chips_rounds in range(1, NCHIPSROUNDS + 1):
            
            new_time_to_art_params = read_time_to_art_params(country, chips_rounds,time_to_art_dir) # Temporary store for this round's data.
            n_time_periods_art_popart_per_round_string += \
                str(new_time_to_art_params["n_time_periods_round"+str(chips_rounds)])+ " "
            # Now add new round data into existing data.
            time_to_art_params = utils.merge_two_dicts(time_to_art_params, new_time_to_art_params)
   
        # Make a dictionary which just contains n_time_periods_art_popart_per_round, and add it to
        # time_to_art_params
        time_to_art_params = utils.merge_two_dicts(time_to_art_params,
            {"n_time_periods_art_popart_per_round":n_time_periods_art_popart_per_round_string})
        
        # This will store the text going in each output file f:
        output_file_strings = {}
        
        # Now go through each of the template files in turn.
        for f in template_files:
            linedata = utils.parse_file(f) # Pull out the data from f.
            
            if country == "SOUTHAFRICA":
                if "times" in f:
                    linedata.append('DHSROUND4 BY_COUNTRY')
                
            output_file_strings[f] = "" # This will store the new file output.
            for l in linedata:
                # Pull out parameter name, the value (or range etc) and any comments on that line
                [paramname, paramvaluelist, comment] = utils.parse_line(l)
                
                [isok, typeofinput] = checkvalue(paramvaluelist)
                if isok:
                    if typeofinput == "BY_COUNTRY":
                        output_file_strings[f] += paramname + " " +\
                            country_level_data[paramname].rstrip() + "\n"
                        
                        # Now we tick off this variable by removing it from the dictionary. At the
                        # end we check the dictionary is empty  so we did use everything we were
                        # supposed to.
                        if country_level_data.pop(paramname, None) == None:
                            utils.handle_error("Error - key " + paramname + " not found. Exiting.")
                    
                    elif typeofinput == "BY_COMMUNITY":
                        # This just checks that the file really should be there.
                        if not(f.replace(template_dir,"") in files_by_community):
                            utils.handle_error("Error: " + f + \
                                " not supposed to contain data by community. Exiting.")
                        
                        output_file_strings[f] += paramname + " " +\
                            community_level_data[paramname].rstrip() + "\n"
                        # Now we tick off this variable by removing it from the dictionary. At the
                        # end we check the dictionary is empty  so we did use everything we were
                        # supposed to.
                        if community_level_data.pop(paramname,None) == None:
                            utils.handle_error("Error - key" + paramname + "not found. Exiting")
                        
                    elif typeofinput == "FROM_CHIPS_R_ANALYSIS":
                        output_file_strings[f] += paramname + " " +\
                            time_to_art_params[paramname].rstrip() + "\n"
                    
                    elif typeofinput == "FROM_CHIPS_FILE":
                        output_file_strings[f] += paramname + " " + \
                            str(chips_timings[paramname]) + "\n"
                    
                    elif typeofinput == "FROM_R_PARTNERSHIP_ANALYSIS_OF_PC0":
                        output_file_strings[f] += paramname + " " + \
                            partnership_data[paramname].rstrip() + "\n"
                    
                    elif typeofinput in \
                        ["Number", "Range", "Random seed", "Multiple numbers and/or ranges"]:
                        
                        # This takes the list and converts it to a string where each list element
                        # is separated by a space.
                        paramvalue  = ' '.join(paramvaluelist)
                        output_file_strings[f] += utils.remove_extra_whitespace(
                            paramname + " " + paramvalue)
                        
                        output_file_strings[f] = \
                            utils.add_comment(output_file_strings[f], comment) + "\n"
                    else:
                        utils.handle_error("Error: not dealing with " + typeofinput + \
                            " at present.  Exiting.\n")
        
        for f in template_files:
            output_filename = f.replace(template_dir, output_dir)
            output_file = open(output_filename, "w")
            output_file.write(output_file_strings[f])
            output_file.close()
        
        # Now check that we did remove everything from the country list (so that all the files
        # match up).
        if not(country_level_data == {}):
            utils.handle_error("Error - country_level_data=" + country_level_data + \
                " should be empty. Variables do not match. Exiting")
        
    # ###########################################################################################
    # ############# Now stuff if we run on HPC:
    # ###########################################################################################
    #
    # # The file start_art_popart_round34.csv is in this directory giving values for time to start
    # # ART for rounds 3/4:
    # future_time_to_art_dir = join(homedir, "Dropbox", "PoPART", "Data:Stats", "CHiPs data", "R")
    #
    # if GETHPCFILES==1:
    #     print("\n\nNow HPC stuff:")
    #     #art_output_dir = "HPC/RESCOMP/MAKE_SCENARIOS_GOODFITS/"
    #     #copy_future_art_file(future_time_to_art_dir,art_output_dir)
    #     check_future_art_file(future_time_to_art_dir)
