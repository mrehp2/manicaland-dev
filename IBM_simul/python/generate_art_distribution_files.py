"""
Process output files associated with ART distribution in the population




Usage:
python generate_art_distribution_files.py <inputdir>

Arguments
---------
inputdir
    Directory in which the output files can be found named `DEBUG_ART_population_*.csv`.  

"""

import sys, math, os, shutil, glob


def handle_error(err_messg):
    """
    Error-handling function; If an error occurs, print error message and exit program.
    
    Parameters
    ----------
    err_messg: Message to print to screen before exiting
    """
    print(err_messg)
    sys.exit(1)


def read_data(filename):
    """
    Reads in data from an output file, splits lines, returns header and body separately.  
    
    Parameters
    ----------
    filename: str
        Fill file name of file to read
    
    Returns
    -------
    list [data, header]
    
    data : list of str
        list of the lines of the data, split on newline
    header : str
        the header line of the imported file as a single string
    
    """
    
    infile = open(filename, "r")
    data_raw = infile.read().rstrip().splitlines()
    infile.close()
    
    # First line is a header:
    return [data_raw[1:], data_raw[0]]


def write_data(outstring, headers, filename):
    """
    Write an output string and header file to disk.  
    
    Parameters
    ----------
    outstring : str
        String to write to file
    headers : str
        Header string to write to file
    filename : str
        File name of the output file to write to disk
    
    Returns
    -------
    Nothing; writes data to file
    """
    
    outfile = open(filename, "w")
    outfile.write(headers + "\n")
    outfile.write(outstring + "\n")
    outfile.close()


##########################################################################################
########## Functions for processing ART state data:
##########################################################################################

def tryconvert(x):
    """
    Try to convert x to a float or an int.  
    
    This function is used to avoid saving output as a float if it was intended to be an integer.  
    If the difference between the float and int conversion of x is less than 1e-8 then an integer
    is returned, otherwise a float is returned.  If the input type of x cannot be converted to an 
    int or a float then the original input is returned.  
    
    Arguments
    ---------
    x : str, int, float
        Input value can be a string, integer, or float.  
    
    Returns
    -------
    int(x) if 
    float(x) if 
    
    Example
    -------
    
    >>> type(tryconvert(0.4))
    <type 'float'>
    
    >>> type(tryconvert(1))
    <type 'int'>
    
    >>> type(tryconvert(1.0))
    <type 'int'>
    
    >>> type(tryconvert("1.000000001"))
    <type 'int'>
    
    >>> type(tryconvert("1.0000001"))
    <type 'float'>
    
    >>> type(tryconvert([1.0000001]))
    <type 'list'>
    """
    
    try:
        y = float(x)
        z = int(y)
        if(y - z < 1e-8):
            return z
        else:
            return y
    except:
        return x

def make_quotient_string(t, data):
    """
    
    
    Parameters
    ----------
    t : 
    
    data : 
    
    
    Returns
    -------
    
    
    """
    
    
    data_n = float(sum(data))
    outstring = str(t) + OUTPUT_SEP
    
    for i in range(len(data)):
        if data_n > 0:
            if(i == 0):
                outdata = [float(data[i]) / data_n]
            else:
                # Make this a cumulative proportion:
                outdata += [float(data[i])/data_n + outdata[-1]]
        elif data[i] == 0:
            if(i == 0):
                outdata = [0]
            else:
                outdata += [0]
        else:
            handle_error("Problem: numerator" + str(data[i]) + "denominator" + str(n) + "Exiting\n")
    
    outstring += OUTPUT_SEP.join([str(x) for x in outdata])
    return outstring + "\n"


def get_art_data(data):
    """
    
    
    
    Parameters
    ----------
    data : list
    
    
    Returns
    -------
    A list of ... 
    [state_output_string, transition_output_string, filled_columns_transition_data]
    
    state_output_string : str
    
    transition_output_string : str
    
    filled_columns_transition_data : 
    
    
    """
    
    SETCOLUMNSAUTOMATICALLY = 0 
    state_output_string = ""
    transition_output_string = ""

    previous_year_cumulative_transition_data = [0]

    current_year_cumulative_transition_data = {}
    times = []
    for line in data:
        [t,
        n_hivneg,
        n_hivpos_dontknowstatus,
        n_hivpos_knowposneverart,
        n_hivpos_earlyart,
        n_hivpos_artvs,
        n_hivpos_artvu,
        n_hivpos_dropout,
        n_hivpos_cascadedropout,
        n_artdeath,
        cumulative_n_start_emergency_art_fromuntested,
        cumulative_n_start_emergency_art_fromartnaive,
        cumulative_n_start_emergency_art_fromartdroupout,
        cumulative_n_start_emergency_art_fromcascadedropout,
        cumulative_n_learnhivpos_fromuntested,
        cumulative_n_startART_fromuntested,
        cumulative_n_startART_fromartnaive,
        cumulative_n_startART_fromartdropout,
        cumulative_n_startART_fromcascadedropout,
        cumulative_n_becomeVS_fromearlyart,
        cumulative_n_becomeVS_fromartvu,
        cumulative_n_becomeVU_fromearlyart,
        cumulative_n_becomeVU_fromartvs,
        cumulative_n_ARTdropout_fromearlyart,
        cumulative_n_ARTdropout_fromartvs,
        cumulative_n_ARTdropout_fromartvu,
        cumulative_n_cascadedropout_fromARTnaive,
        n_cascadedropout_fromARTneg,
        cumulative_n_aidsdeaths_fromuntested,
        cumulative_n_aidsdeaths_fromartnaive,
        cumulative_n_aidsdeaths_fromearlyart,
        cumulative_n_aidsdeaths_fromartvs,
        cumulative_n_aidsdeaths_fromartvu,
        cumulative_n_aidsdeaths_fromartdropout,
        cumulative_n_aidsdeaths_fromcascadedropout] = [tryconvert(x) for x in line.split(",")]
        
        
        if(t < MINTIME):
            continue
        
        times += [t]
        # Now split these up. Note that we omit the HIV- here:
        state_output_string += make_quotient_string(t, \
            [n_hivpos_dontknowstatus, n_hivpos_knowposneverart, n_hivpos_earlyart, n_hivpos_artvs,\
            n_hivpos_artvu, n_hivpos_dropout, n_hivpos_cascadedropout, n_artdeath])
        
        # To look at transitions we need to subtract the previous year's cumulative total from the
        # current cumulative total. So first put everything from the current year in one array:
        
        current_year_cumulative_transition_data[t] = [
            cumulative_n_start_emergency_art_fromuntested,
            cumulative_n_start_emergency_art_fromartnaive,
            cumulative_n_start_emergency_art_fromartdroupout,
            cumulative_n_start_emergency_art_fromcascadedropout,
            cumulative_n_learnhivpos_fromuntested,
            cumulative_n_startART_fromuntested,
            cumulative_n_startART_fromartnaive,
            cumulative_n_startART_fromartdropout,
            cumulative_n_startART_fromcascadedropout,
            cumulative_n_becomeVS_fromearlyart,
            cumulative_n_becomeVS_fromartvu,
            cumulative_n_becomeVU_fromearlyart,
            cumulative_n_becomeVU_fromartvs,
            cumulative_n_ARTdropout_fromearlyart,
            cumulative_n_ARTdropout_fromartvs,
            cumulative_n_ARTdropout_fromartvu,
            cumulative_n_cascadedropout_fromARTnaive,
            n_cascadedropout_fromARTneg,
            cumulative_n_aidsdeaths_fromuntested,
            cumulative_n_aidsdeaths_fromartnaive,
            cumulative_n_aidsdeaths_fromearlyart,
            cumulative_n_aidsdeaths_fromartvs,
            cumulative_n_aidsdeaths_fromartvu,
            cumulative_n_aidsdeaths_fromartdropout,
            cumulative_n_aidsdeaths_fromcascadedropout
        ]
    
    # Now try to see which column numbers are always zero - remove these to reduce output:
    if(SETCOLUMNSAUTOMATICALLY == 1): 
        possible_blank_columns = range(len(current_year_cumulative_transition_data[times[0]]))
    
    # Don't use "possible_blank_columns" as problems using array that is being changed 
    # for the range.
        for i in range(len(current_year_cumulative_transition_data[times[0]])):
            for t in times:
                if current_year_cumulative_transition_data[t][i] > 0:
                    possible_blank_columns.remove(i)
                    break
        print(possible_blank_columns)
    else:
        possible_blank_columns = [0, 2, 5, 7, 8, 16, 18, 19, 21, 22, 23, 24]
    
    filled_columns_transition_data = [x for x in range(len(current_year_cumulative_transition_data[times[0]])) if x not in possible_blank_columns]
    
    for t in times:
        current_year_cumulative_transition_data[t] = [current_year_cumulative_transition_data[t][i] for i in filled_columns_transition_data]

        # Make sure that previous_year_cumulative_transition_data array is initialised correctly.
        # In particular, ensure we always set up previous_year_cumulative_transition_data to have
        # the right length:
        if (previous_year_cumulative_transition_data == [0]):
            for i in range(len(current_year_cumulative_transition_data[t]) - 1):
                previous_year_cumulative_transition_data += [0]
        
        # Now calculate differences:
        annual_transition_data = []
        
        for i in range(len(current_year_cumulative_transition_data[t])):
            change = current_year_cumulative_transition_data[t][i] - \
                previous_year_cumulative_transition_data[i]
            
            if(change < 0):
                handle_error("Error: negative change in cumulative total. Exiting.")
            annual_transition_data += [change]

            # Now set the "new" previous year to be the current data:
            previous_year_cumulative_transition_data[i] = \
                current_year_cumulative_transition_data[t][i]
        
        # Make quotients and store in a string:
        transition_output_string += make_quotient_string(t, annual_transition_data)
    
    return [state_output_string, transition_output_string, filled_columns_transition_data]


if __name__ == "__main__":
    
    OUTPUT_SEP = ","
    MINTIME = 1970 # Don't bother with any output before 1970 as no HIV then.
    
    # Import (and process) the command-line arguments
    try:
        artfiledir = sys.argv[1]
    except:
        handle_error("Error: need to pass directory as command-line argument. Exiting.")
    
    if not(os.path.isdir(artfiledir)):
        handle_error("Error: " + artfiledir + " does not exist. Please check code. Exiting.")
    
    # Final all files matching the DEBUG_ART_population prefix
    artfiles = glob.glob(artfiledir + "/DEBUG_ART_population_CL*")
    
    # Process each of the art files
    for f in artfiles:
        
        # Read the ART data from a single file (header is not used)
        [ART_data, ART_header] = read_data(f)
        
        [state_output_string, transition_output_string, filled_columns_transition_data] =\
            get_art_data(ART_data)
        
        root_filename = f.replace("DEBUG_ART_population_", "")
        root_filename = root_filename.replace(".csv", "")
        outfile = f.replace("DEBUG_ART_population", "ART_distribution")
        
        header = "t,n_hivpos_dontknowstatus,n_hivpos_knowposneverart,"+\
            "n_hivpos_earlyart,n_hivpos_artvs,n_hivpos_artvu,n_hivpos_dropout," +\
            "n_hivpos_cascadedropout,n_artdeath"
        
        write_data(state_output_string, header, outfile)
        
        outfile = f.replace("DEBUG_ART_population", "ART_transition_dist")
        
        # Define the new header
        header_to_change  = "cumulative_n_start_emergency_art_fromuntested,"+\
            "cumulative_n_start_emergency_art_fromartnaive,"+\
            "cumulative_n_start_emergency_art_fromartdroupout,"+\
            "cumulative_n_start_emergency_art_fromcascadedropout,"+\
            "cumulative_n_learnhivpos_fromuntested,"+\
            "cumulative_n_startART_fromuntested,"+\
            "cumulative_n_startART_fromartnaive,"+\
            "cumulative_n_startART_fromartdropout,"+\
            "cumulative_n_startART_fromcascadedropout,"+\
            "cumulative_n_becomeVS_fromearlyart,"+\
            "cumulative_n_becomeVS_fromartvu,"+\
            "cumulative_n_becomeVU_fromearlyart,"+\
            "cumulative_n_becomeVU_fromartvs,"+\
            "cumulative_n_ARTdropout_fromearlyart," +\
            "cumulative_n_ARTdropout_fromartvs,"+\
            "cumulative_n_ARTdropout_fromartvu,"+\
            "cumulative_n_cascadedropout_fromARTnaive,"+\
            "n_cascadedropout_fromARTneg,"+\
            "cumulative_n_aidsdeaths_fromuntested,"+\
            "cumulative_n_aidsdeaths_fromartnaive,"+\
            "cumulative_n_aidsdeaths_fromearlyart,"+\
            "cumulative_n_aidsdeaths_fromartvs,"+\
            "cumulative_n_aidsdeaths_fromartvu,"+\
            "cumulative_n_aidsdeaths_fromartdropout,"+\
            "cumulative_n_aidsdeaths_fromcascadedropout"
        
        new_header = header_to_change.replace("cumulative_", "annual_change_")
        
        # Convert into a list (split by commas) and pull out only the elements indexed by filled_columns_transition_data:
        new_header_split = [new_header.split(",")[i] for i in filled_columns_transition_data]
        
        # Now stick the list back together into a string:
        new_header = ",".join(new_header_split)
        write_data(transition_output_string, "t," + new_header, outfile)
