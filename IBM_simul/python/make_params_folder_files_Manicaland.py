#!/usr/bin/env python3
"""
make_params_folder_files_Manicaland.py takes data from different sources (outputs of analyses of survey or intervention data done in R; other prior values/ranges specified in a bunch of text files) and creates the param_*.txt files needed by `make_ibm_parameter_sample.py`.

Usage: python make_params_folder_files_Manicaland.py [basedir] [site_no] [HPC_SYSTEMS]

basedir : dir
    base directory (e.g. ~/MANICALAND/manicaland-dev/IBM_simul/)

site_no : int
    Refers to a Manicaland site 0='all R7 sites combined'; (2,3,5,7,8,9,14,15)= sites.

HPC_SYSTEMS : str
    The final argument can be one of ["ICHPC","RESCOMP"] which designates if the IBM is to be run on
    an HPC system (ICHPC is at Imperial; RESCOMP is at Oxford).  
"""

import glob, sys, os, filecmp, shutil
from datetime import datetime,date
from os.path import join
import random,copy
import openpyxl   # For reading Excel files.

import utilities as utils



def get_country(this_community):
    """
    For PopART this code returned Zambia/South Africa depending on community number.
    For Manicaland it's always Zimbabwe.
    Keep in case I want to customise.    
    """
    # if this_community <= 12:
    #     country = "ZAMBIA"
    # else:
    #     country = "SOUTHAFRICA"

    country = "ZIMBABWE"

    return country


def get_country_sentencecase(this_country):
    """
    Changes capitalization of countryname string from capitals to SentenceCase.  
    """
    if this_country=="ZAMBIA":
        return "Zambia"
    elif this_country=="SOUTHAFRICA":
        return "SouthAfrica"
    elif this_country=="ZIMBABWE":
        return "Zimbabwe"
    else:
        utils.handle_error("Error: unknown country name "+this_country+" in get_country_sentencecase(). Exiting.")




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
        BY_COMMUNITY, FROM_CHIPS_R_ANALYSIS, FROM_R_PARTNERSHIP_ANALYSIS, FROM_CHIPS_FILE, 
    
    
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
        if (p == "FROM_CHIPS_R_ANALYSIS"):   # Specific to PopART
            return [1, "FROM_CHIPS_R_ANALYSIS"]
        if (p == "FROM_R_PARTNERSHIP_ANALYSIS"):  # Specific to PopART
            return [1, "FROM_R_PARTNERSHIP_ANALYSIS"]
        if (p == "FROM_CHIPS_FILE"):         # Specific to PopART
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


# Function not currently used - but could be useful.
# This function was originally called copy_chips_file_removing_whitespace_and_store_start_end_times(). It copies a file (overwriting any existing file) removing trailing whitespace in the original file.
# Originally used because Anne's R script added extra whitespace at the end, but the IBM counts lines (including blank ones) so it caused issues.
# For CHiPs files we also pulled the start and end times of the round, and returned them.
def copy_chips_file_removing_whitespace_and_store_start_end_times(original_data_filename, outfilename):
    # check the input file exists:
    if os.path.isfile(original_data_filename):
        infile = open(original_data_filename,"r")
        data = infile.read().rstrip()
        # For CHiPs files we also pulled the start and end times of the round, and returned them.
        #start_time = data.splitlines()[1].split()[0]
        #end_time = data.splitlines()[-1].split()[0]
        infile.close()
    else:
        utils.handle_error("Error: Cannot find file " + original_data_filename + ". Exiting")
    outfile = open(outfilename,"w")
    outfile.write(data)
    outfile.close()
    # Only used for CHiPs.
    #return [start_time, end_time]


##### For reading in Excel file that I made to store Spectrum MTCT output:

# Given a single sheet name and the name of the xlsx file, pull out the named sheet and return as an array:
def pull_out_sheet(infilename,sheet_to_get):

    book = openpyxl.load_workbook(infilename, data_only=True)
    sheet_to_keep = {}

    for sheet in book:
        formatted_sheet_name = sheet.title.rstrip().upper()
        if formatted_sheet_name==sheet_to_get:
            return sheet.values

    print("Error: sheet",sheet_to_get," not found. Exiting.")
    sys.exit(1)

    

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




def read_partnership_data(country, partnership_analysis_dir):
    print("Country=",country)
    """
    For PopART function reads in the data generated from the raw PC data by a knitr document written by  Anne:
    ~/Dropbox/PoPART/Data\:Stats/PC\ Data\ Downloads/15-12-2016_PC0_NEWFINAL/R/partnerships/ExtractPartnershipParamFromPC0.Rnw

    """

    popart_basedir = join(homedir, "Dropbox", "PoPART", "Data:Stats", "PC Data Downloads", "15-12-2016_PC0_NEWFINAL")

    """

    Parameters
    ----------
    country : str
        Country of interest
    partnership_analysis_dir : str
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

    

    if country == "ZAMBIA":
        infilename = join(popart_basedir, "R", "partnerships", "param_partnerships_fromPC0_Za.txt")
    elif country == "SOUTHAFRICA":
        infilename = join(popart_basedir, "R", "partnerships", "param_partnerships_fromPC0_SA.txt")
    elif country == "ZIMBABWE":
        infilename = join(partnership_analysis_dir, "param_partnerships_from_R_Zim.txt")
    else:
        utils.handle_error("Error: Unknown country " + country + "\nExiting.")

    
    if country in ["ZAMBIA","SOUTHAFRICA"]:
        partnership_analysis_source_files = [
            join(popart_basedir, "R", "DataCleaning", "Read_PC0_final_data.R"),
            join(popart_basedir, "R", "DataCleaning", "PC0.yml"),
            join(popart_basedir, "R", "DataCleaning", "PC0_partner.yml"),
            join(popart_basedir, "R", "DataCleaning", "RenameColMergedPC0.yml"),
            join(popart_basedir, "R", "DataCleaning", "recipes.yml"),
            join(popart_basedir, "RawData", "PC0.csv"),
            join(popart_basedir, "RawData", "PC0_partner.csv"),
            join(popart_basedir, "MergedAndCleanData", "Recoded_PC0_merged_dat.rds"), 
            join(popart_basedir, "MergedAndCleanData", "Recoded_PC0_merged_dat.rds"), 
            join(popart_basedir, "R","partnerships", "ExtractPartnershipParamFromPC0.Rnw")]
        
        #check = check_whether_data_file_up_to_date(infilename, partnership_analysis_source_files, print_warning_only)
    elif country=="ZIMBABWE":
        partnership_analysis_source_files = [join(partnership_analysis_dir, "Partnership_parameterization_Manicaland_20-11-2019.R")]        
        check = check_whether_data_file_up_to_date(infilename, partnership_analysis_source_files, print_warning_only)



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




# Given a mtct worksheet, pulls out the data, and save it as a PopART-IBM param file called mtct_param_filename:
def make_mtct_params(sheet,mtct_param_filename):

    outstring = ""
    passed_header = 0 
    years = []
    for i, line in enumerate(sheet):
        line = list(line)
        
        if (passed_header>0):
            outstring += " ".join([str(x) for x in line])+"\n"
            years += [line[0]]
        else:
            # If some elements aren't numbers then this is probably the header.
            if not(all(isinstance(item,float) for item in line)):
                passed_header=1

    # Add the first and last year as the first line of the file:
    outstring = str(min(years))+" "+str(max(years))+"\n"+outstring
    
    outfile = open(mtct_param_filename,"w")
    outfile.write(outstring)
    outfile.close()






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
    

def get_most_recent_WPP_year(WPP_filename):

    WPP_files = glob.glob(WPP_filename)

    years_stored_in_folder = []
    
    for f in WPP_files:
        # Get the filename:
        this_filename = f.split("/")[-1]
        # Find the year of publication (files of the form WPP20XX_..."
        first_part_of_filename = this_filename.split("_")[0]

        if ((len(first_part_of_filename)!=7) or (first_part_of_filename[0:3])!="WPP"):
            print("Error for UNPD WPP file ",this_filename,". Filename not in expected format",first_part_of_filename)
            sys.exit(1)


        try:
            years_stored_in_folder += [int(first_part_of_filename[3:])]
        except:
            print("Error for UNPD WPP file ",f,". Filename not in expected format")
            sys.exit(1)

    # Now pick the most recent year:
    most_recent_year = max(years_stored_in_folder)

    # From datetime module - check if the most recent WPP year is within 2 years of current year.
    current_year = date.today().year
    if (most_recent_year+2<current_year):
        print("Warning: newer UNPD WPP projections may exist than ",most_recent_year)
        
    return most_recent_year



# Function looks for the most recent year where we have all the required UNPD WPP datafiles, and checks that this is a recent dataset (<3 years old).
def get_current_IBM_fertility_datafile(input_dir, country_sentencecase):
    

    # This gets the year of the most recent WPP file in the directory:
    most_recent_year = get_most_recent_WPP_year(input_dir+"/WPP*_FERT_F07_AGE_SPECIFIC_FERTILITY.xlsx")


    most_recent_WPP_file = input_dir+"/WPP"+str(most_recent_year)+"_FERT_F07_AGE_SPECIFIC_FERTILITY.xlsx"
    
    most_recent_fertility_file = input_dir+"/"+country_sentencecase+"Fertility_WPP"+str(most_recent_year)+".csv"
    # Check that this file exists:
    if not(os.path.isfile(most_recent_fertility_file)): 
            utils.handle_error("Error: file " + most_recent_fertility_file + 
                " does not exist  when calling get_current_IBM_fertility_datafile(). Exiting.")


    # determines whether check_whether_data_file_up_to_date() prints warning (if 1) or exits (if 0).
    print_warning_only = -1

    data_file_depends_on = [most_recent_WPP_file,
        join(input_dir+"/read_UNPD_fertility_data.py")]
    
    check = check_whether_data_file_up_to_date(most_recent_fertility_file,data_file_depends_on,print_warning_only)
    if (not(check==1) and print_warning_only==0):
        print(check + " is more recent that " + most_recent_WPP_file + 
            ". Running python to generate file")
        os.system("python read_UNPD_fertility_data.py "+str(most_recent_year)+" "+country_sentencecase)
    else:
        if VERBOSE_OUTPUT == 1:
            print(most_recent_fertility_file + " up to date")

    return most_recent_fertility_file



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
    
    # Find the fertility file we are copying.
    # Note that UNPD publishes updated datasets every 2 years, so this bit of code finds the most up-to-date file and makes sure it is within <=3 years.
    #template_files = glob.glob(join(template_dir, "param*.txt"))
    fertility_data_file = get_current_IBM_fertility_datafile(input_dir, country_sentencecase)
    
    # This is what we are copying to
    #print "Copying ",fertility_data_file
    fertility_outfilename = join(output_dir, "param_fertility.txt")

    copy_file_checking_if_exists(fertility_data_file, fertility_outfilename)


# Function looks for the most recent year where we have all the required UNPD WPP datafiles, and checks that this is a recent dataset (<3 years old).
def get_current_UNPD_mortality_datafile_year(input_dir, country_sentencecase):
    
    WPP_pop_size_file_men = input_dir+"/WPP*_POP_F07_2_POPULATION_BY_AGE_MALE.xlsx"
    WPP_pop_size_file_women = input_dir+"/WPP*_POP_F07_3_POPULATION_BY_AGE_FEMALE.xlsx"
    WPP_mortality_file_men = input_dir+"/WPP*_MORT_F04_2_DEATHS_BY_AGE_MALE.xlsx"
    WPP_mortality_file_women = input_dir+"/WPP*_MORT_F04_3_DEATHS_BY_AGE_FEMALE.xlsx"
 
    # This gets the year of the most recent WPP file in the directory:
    most_recent_year_Npop_M = get_most_recent_WPP_year(WPP_pop_size_file_men)
    most_recent_year_Npop_F = get_most_recent_WPP_year(WPP_pop_size_file_women)
    most_recent_year_mort_M = get_most_recent_WPP_year(WPP_mortality_file_men)
    most_recent_year_mort_F = get_most_recent_WPP_year(WPP_mortality_file_women)

    if not(most_recent_year_Npop_M==most_recent_year_Npop_F==most_recent_year_mort_M==most_recent_year_mort_F):
        print("Error: One or more missing WPP files - not all have the same date. Exiting\n")
        sys.exit(1)
    else: # All are the same.
        most_recent_year = most_recent_year_mort_F


    return most_recent_year

    
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

    most_recent_year = get_current_UNPD_mortality_datafile_year(mortality_unpd_data_dir, country_sentencecase)


    latest_WPP_pop_size_file_men = mortality_unpd_data_dir+"/WPP"+str(most_recent_year)+"_POP_F07_2_POPULATION_BY_AGE_MALE.xlsx"
    latest_WPP_pop_size_file_women = mortality_unpd_data_dir+"/WPP"+str(most_recent_year)+"_POP_F07_3_POPULATION_BY_AGE_FEMALE.xlsx"
    latest_WPP_mortality_file_men = mortality_unpd_data_dir+"/WPP"+str(most_recent_year)+"_MORT_F04_2_DEATHS_BY_AGE_MALE.xlsx"
    latest_WPP_mortality_file_women = mortality_unpd_data_dir+"/WPP"+str(most_recent_year)+"_MORT_F04_3_DEATHS_BY_AGE_FEMALE.xlsx"

    
    # determines whether check_whether_data_file_up_to_date() prints warning (if 1) or exits (if 0).
    print_warning_only = -1

    data_file_depends_on = [latest_WPP_pop_size_file_men,
                            latest_WPP_pop_size_file_women,
                            latest_WPP_mortality_file_men,
                            latest_WPP_mortality_file_women,
                            join(mortality_unpd_data_dir+"/EstimatingRatesFromUNPDv2.Rnw"),
                            join(mortality_unpd_data_dir+"/read_UNPD_mortality_data.py")]
    
    check = check_whether_data_file_up_to_date(mortality_data_file,data_file_depends_on,print_warning_only)
    if (not(check==1) and print_warning_only==0):
        print(check + " is more recent than"+mortality_data_file+". Running python to generate file")
        os.system("python read_UNPD_mortality_data.py "+str(most_recent_year)+" "+country)
        utils.run_sweave("EstimatingRatesFromUNPD.Rnw",mortality_sweave_code_dir)
    else:
        if VERBOSE_OUTPUT == 1:
            print("Mortality file"+most_recent_mortality_file+" up to date")

    
    
    # This is what we are copying to
    mortality_outfilename = join(output_dir, "param_mortality.txt")
    #print "Copying file",mortality_data_file," to ",mortality_outfilename
    copy_file_checking_if_exists(mortality_data_file,mortality_outfilename)




def write_patchinfo(communities, output_dir, setting, community_arm_data={}):
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

    # For PopART only: Dictionary to convert from A/B/C to 1/2/0 (as used in IBM: 0=ARM C, 1=ARM A, 2=ARM B)

    patchinfo_cluster_text = "cluster_number ("
    
    if setting in ["Zambia","SouthAfrica"]:
        arm_numbers = {"A":"1", "B":"2", "C":"0"}
        patchinfo_arm_text = "trial_arm ("
    else:
        patchinfo_arm_text = ""

    for c in communities:
        patchinfo_cluster_text += str(c)+","
        if setting in ["Zambia","SouthAfrica"]:
            community_arm = community_arm_data[c]
            community_arm_number = arm_numbers[community_arm]
            patchinfo_arm_text += community_arm_number+","
    
    # Remove the trailing commas from each line
    patchinfo_cluster_text = patchinfo_cluster_text.rstrip(",")
    if setting in ["Zambia","SouthAfrica"]:
        patchinfo_arm_text = patchinfo_arm_text.rstrip(",")
    
    # Now add extra info at end of each line
    patchinfo_cluster_text += ") \n"
    if setting in ["Zambia","SouthAfrica"]:
        patchinfo_arm_text += ")     // 0=ARM C, 1=ARM A, 2=ARM B"
    
    outfile = open(join(output_dir, "param_patchinfo.txt"),"w")
    outfile.write(patchinfo_cluster_text + patchinfo_arm_text)
    
    outfile.close()
    



####################################################################################################
######### Main code: ###############################################################################

# If this script is run from the command line, the following code will run automatically:
if __name__=="__main__":
    
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
        print("Error for community number.",site_no)
        utils.handle_error("All arguments passed to make_params_folder_file_Manicaland.py must be integers. Exiting")

    for x in all_communities:
        if not(x in [0,2,3,5,7,8,9,14,15]):
            utils.handle_error("Community number passed to "+__file__+" must be in the set {0,2,3,5,7,8,9,14,15}. Exiting")
    
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
    # make_params_folder_files_Manicaland.py now lives in the same directory as the IBM code. 
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
    fertility_data_dir = join(homedir,"manicaland-dev","Parameterization","Demographics")
    mortality_unpd_data_dir = fertility_data_dir
    
    mortality_sweave_code_dir = join(homedir,"manicaland-dev","Parameterization","Demographics")


    # Analysis of Manicaland partnership data:
    partnership_analysis_dir = join(homedir, "manicaland-dev", "Parameterization")

    
    utils.check_directory_exists(params_basedir)
    utils.check_directory_exists(ibm_code_dir)
    utils.check_directory_exists(template_dir)
    utils.check_directory_exists(fertility_data_dir)
    utils.check_directory_exists(mortality_sweave_code_dir)
    utils.check_directory_exists(mortality_unpd_data_dir)
    utils.check_directory_exists_and_create(output_dir)
    
    # Here we generate the list of files which will eventually be copied:
    # all param files need to be named like this for now.
    template_files = glob.glob(join(template_dir, "param*.txt"))

    # For now we keep these in template_dir but may remove.
    exceptions = ["param_mortality.txt", "param_fertility.txt"]
    for e in exceptions:
        try:
            template_files.remove(join(template_dir, e))
        except:
            utils.handle_error("Warning - file " + e + " not in " + template_dir + "." +
            "For now exiting - maybe change code later on?")
    
    
    country = get_country(all_communities[0])
        

    # Create the file param_patchinfo.txt:
    write_patchinfo(all_communities,output_dir,"Zimbabwe")
    
    # This is where we store the community parameters and the fitting_data_processed.txt file.
    site_no = all_communities[0]
    
    if (site_no==0):  # "0" means 'all Manicaland communities.
        community_param_dir = join(params_community_basedir,"PARAM_ALL_COMMUNITIES")
    else:
        community_param_dir = join(params_community_basedir,"PARAM_BY_COMMUNITY_" + str(site_no))
        
    utils.check_directory_exists(community_param_dir)

    # Now copy the fitting data file. This isn't used for much in the IBM - mainly it ensures that we are between 0 and about 45% HIV prevalence at the start of CHiPs 
    # which is quite a weak constraint. This file (and the corresponding code in the IBM) might be removed at some point (can also be used to implement target fitting).
    # Note that we only need one file (so use the one from the first patch (ie patch=0):

    copy_file_checking_if_exists(join(community_param_dir, "fitting_data_processed.txt"),join(output_dir, "fitting_data_processed.txt"))
        
    # Generate/copy special files:

    copy_fertility_file(country, fertility_data_dir, output_dir)
    copy_mortality_file(country, mortality_sweave_code_dir, mortality_unpd_data_dir, output_dir)

    mtct_file = "../Parameterization/Spectrum_Manicaland_2019_MTCT.xlsx"
    # This is the sheet we want to pull out from the Excel file: 
    mtct_sheet_needed = "FOR IBM"

    # Extract the worksheet:
    mtct_worksheets = pull_out_sheet(mtct_file,mtct_sheet_needed)

    # Now process it and save it in the format needed by the IBM:
    mtct_params = make_mtct_params(mtct_worksheets,join(output_dir,"param_mtct.txt"))




        
    # Read in the country-level data:
    country_level_data = read_country_data(country, country_params_dir)

    # First get a list of the files that are in the community-level directory:
    files_by_community = get_community_level_files(community_param_dir)

    # Read in the community-level data:
    community_level_data = read_community_data(files_by_community, community_param_dir)

    # Read in the output of the knitr analysis of PC0 data:
    partnership_data = read_partnership_data(country, partnership_analysis_dir)


    # This will store the text going in each output file f:
    output_file_strings = {}
        
    # Now go through each of the template files in turn.
    for f in template_files:
        linedata = utils.parse_file(f) # Pull out the data from f.
            
        if country == "SOUTHAFRICA":
            if "times" in f:
                linedata.append('DHSROUND4 BY_COUNTRY')
                
        output_file_strings[f] = "" # This will store the new file output.

        #print "Processing",f
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
                        
                elif typeofinput == "FROM_R_PARTNERSHIP_ANALYSIS":
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
                    print("For file ",f)
                    utils.handle_error("Error: not dealing with " + typeofinput + \
                                       " at present.  Exiting.\n")
        
    for f in template_files:
        output_filename = f.replace(template_dir, output_dir)
        #print "Writing to",output_filename
        output_file = open(output_filename, "w")
        output_file.write(output_file_strings[f])
        output_file.close()
        
    # Now check that we did remove everything from the country list (so that all the files
    # match up).
    if not(country_level_data == {}):
        print("ERROR*** - country_level_data=",country_level_data)
        sys.exit(1)

    if not(community_level_data == {}):
        print("ERROR*** - community_level_data=",community_level_data)
        sys.exit(1)

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
