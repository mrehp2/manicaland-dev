#!/usr/bin/env python3
"""
Functions process post-trial CHiPs coverage files

Previous comment: Code based on file print_dummy_chips_data_scenarios.py used in DSMB Oct 2016.
"""
import sys, os
from os.path import join
import utilities as utils

def read_chips_infile(round_to_extrapolate_from, infiledir):
    """
    Read CHiPs data from which we are extrapolating (ie from round_to_extrapolate_from)
    """
    # Read in the data we will use to extrapolate
    infile = "param_processed_patch0_chipsuptake_round" + str(round_to_extrapolate_from) + ".csv"
    
    extrapolation_file = open(join(infiledir, infile), "r")
    extrapolation_data = extrapolation_file.read().rstrip().split("\n")
    extrapolation_file.close()
    return extrapolation_data


def create_output_string(annual_coverage_for_extrapolation,
    numberoftimesteps_in_extrapolation_round, user_defined_future_coverage, OPTION,
    NTIMESTEPS_POSTTRIAL, genders, ages, header = None):
    """
    Create the extrapolated CHiPs visit coverage and store in the string `outstring`
    output depends upon input argument `OPTION`
    
    Create a long string to be written to file as a space-delimited CHiPs coverage file.  
    The string will have a header line (time year t_step prop_hiv_status_known3MM18 ...
    prop_hiv_status_known3MM80 prop_hiv_status_known3MF18 ... prop_hiv_status_known_3MF80) 
    followed by a line for each time step of the post-trial round.  
    
    Each line, for each time step will show the year (in decimal year), year (int), time step 
    within the year (int), followed by the proportion of each age/sex group that is visited in 
    that time step in the post-trial round (for all age/sex combinations listed in `genders` and 
    `ages` arguments).  
    
    Arguments
    ---------
    annual_coverage_for_extrapolation : dict (with floats as values of dict entries)
        The cumulative CHiPs coverage
    numberoftimesteps_in_extrapolation_round : int
        Number of time steps in the round from which the post-trial round coverage is extrapolated
    user_defined_future_coverage : float
        A user-defined value of coverage to use in the post-trial round
    OPTION : int
        An option that denotes how post-trial round coverage is calculated.  Can take the following
        values: 1) 
    NTIMESTEPS_POSTTRIAL : int
        Number of timesteps in the post-trial rounds
    genders : list
        list of genders
    ages : list
        List of age groups
    header : str
        The header to use for the post-trial round coverage file
    
    Returns
    -------
    outstring : str
        Output string of the CHiPs coverage file for the post-trial round (read to be written to 
        file)
    """
    
    # First attach the header line to the output string
    if header is None:
        outstring = "Random header\n"
    else: 
        outstring = header + "\n"
    
    # Delimiter used in the output file
    SEP = " "
    
    # Loop through all timesteps (rows of the output file)
    # then loop through the 
    for t in range(NTIMESTEPS_POSTTRIAL):
        outstring += str(t*1.0) + SEP + "1" + SEP + str(t) + SEP
        for g in genders:
            for a in ages:
                if(OPTION == 1):
                    
                    x = annual_coverage_for_extrapolation[g][a]
                    y = numberoftimesteps_in_extrapolation_round
                    outstring += str(x/y) + SEP
                    
                elif(OPTION == 2):
                    
                    x = annual_coverage_for_extrapolation[g][a]
                    y = NTIMESTEPS_POSTTRIAL
                    outstring += str(x/y) + SEP
                    
                elif(OPTION == 3):
                    
                    x = user_defined_future_coverage
                    y = numberoftimesteps_in_extrapolation_round
                    outstring += str(x/y) + SEP
                    
        outstring += "\n"
    return outstring


def get_chips_round_timing(end_of_popart, immediate_start_of_post_popart_rounds,
    NTIMESTEPS_PER_CALENDAR_YEAR, DURATION_POSTTRIAL_CHIPS_ROUNDS):
    """
    Calculate the start/end of the future round and the number of timesteps
    
    
    """
    # Use this if future CHiPs rounds (ie post-trial) are to start IMMEDIATELY AFTER PopART:
    if(immediate_start_of_post_popart_rounds == 1): 
        # If we want to start post-popart CHiPs straight after PopART (ie 1 timestep after):
        CHIPSSTART_FUTUREROUND  = end_of_popart + 1.0/NTIMESTEPS_PER_CALENDAR_YEAR
    else:
        # Else, start at the beginning of the following year.
        CHIPSSTART_FUTUREROUND  = int(end_of_popart) + 1
    
    # This is the time when the post-popart first 'round' ends.
    CHIPSEND_FUTUREROUND  = CHIPSSTART_FUTUREROUND + DURATION_POSTTRIAL_CHIPS_ROUNDS
    # The corresponding duration of the post-trial 'round'
    NTIMESTEPS_POSTTRIAL = int(round(DURATION_POSTTRIAL_CHIPS_ROUNDS*NTIMESTEPS_PER_CALENDAR_YEAR))
    
    return [CHIPSSTART_FUTUREROUND,CHIPSEND_FUTUREROUND,NTIMESTEPS_POSTTRIAL]


def make_dictionary_ages_to_column_number(ages, genders):
    """
    Return a dictionary to translate between age/gender and column number
    
    Iterate through items g in the iterable `genders`, then through items a in the iterable `ages`
    and increment a counter, saving dict[g][a] as the counter.  
    
    Arguments
    ---------
    age : list
        Age groups of interest
    genders : list
        Genders of interest
    
    Returns
    -------
    indice : dict
        Dictionary translating age/gender to column number (if counting M18, M19, ... F18, F19, etc
    
    Example
    -------
    
    ages = [18, 19, 20]
    genders = ["M", "F"]
    make_dictionary_ages_to_column_number(ages, genders)
    
    >> {'F': {18: 3, 19: 4, 20: 5}, 'M': {18: 0, 19: 1, 20: 2}}
    """
    indices = {}
    counter = 0
    for g in genders:
        indices[g] = {}
        for a in ages:
            indices[g][a] = counter
            counter = counter + 1
    return indices


def analyse_extrapolation_data(ages, genders, extrapolation_data, IMPROVEMENTINPOSTTRIAL, indices):
    """
    Store the extrapolation data (store split by gender and by age/gender combined)
    
    """
    annual_coverage_for_extrapolation = {}
    numberoftimesteps_in_extrapolation_round = 0
    # Set up the store giving zaro values:
    annual_coverage_for_extrapolation = {}
    for g in genders:
        annual_coverage_for_extrapolation[g] = {}
        for a in ages:
            annual_coverage_for_extrapolation[g][a] = 0

    # Now go line-by-line through the data file we use for extrapolation. The first line is a header so skip it.
    for line in extrapolation_data[1:]:
        # Data is split by spaces. First 3 columns are times. Remove first 3 columns and convert rest from string to int:
        line_data = [float(x) for x in line.split(" ")[3:]]
        numberoftimesteps_in_extrapolation_round = numberoftimesteps_in_extrapolation_round + 1
        for g in genders:
            for a in ages:
                annual_coverage_for_extrapolation[g][a] = annual_coverage_for_extrapolation[g][a] + line_data[indices[g][a]]
    

    # Now scale by IMPROVEMENTINPOSTTRIAL:
    for g in genders:
        for a in ages:
            annual_coverage_for_extrapolation[g][a] = \
                annual_coverage_for_extrapolation[g][a] * IMPROVEMENTINPOSTTRIAL 

    return [annual_coverage_for_extrapolation, numberoftimesteps_in_extrapolation_round]


def make_future_chips_visit_data(output_dir, patch_number,
    round_to_extrapolate_from = 3):
    """
    output_dir : 
    
    patch_number
    
    round_to_extrapolate_from : int
        CHiPs round from which to use coverage when calculating coverage for the post-trial rounds
    """
    NTIMESTEPS_PER_CALENDAR_YEAR = 48
    
    # This says whether the post-PopART CHiPs rounds :
    # - start immediately after PopART (immediate_start_of_post_popart_rounds = 1)
    #  - or whether they start at the beginning of the following year (immediate_start_of_post_popart_rounds = 0):
    immediate_start_of_post_popart_rounds = 0
    
    # Duration of future 'CHiPs' rounds after end of trial
    DURATION_POSTTRIAL_CHIPS_ROUNDS = 1.0
    
    # Factor by which post-trial ChiPs can be better than extrapolation round. 
    # IMPROVEMENTINPOSTTRIAL=1.0 means 'stays the same as in the extrapolation round'.
    IMPROVEMENTINPOSTTRIAL = 1.0
    
    #try:
    #    COMMUNITY = sys.argv[1]
    #    DIRECTORY = sys.argv[2]
    #except:
    #    print "Error: make_future_chips_visit_data.py requires 2 arguments: the community and the directory we are using." 

    # OPTION is a switch whether we use:
    # 1 the timesteply rate (i.e. we see the same % of the population each week as the average per-timestep from round listed in `round_to_extrapolate_from`)
    # 2 the previous round coverage level
    # 3 a user-defined coverage (note that this is the same for all age groups and genders).
    OPTION = 1
    if not(OPTION in [1,2,3]):
        print("OPTION needs to be in {1,2,3}. Exiting\n")
        sys.exit(1)
    
    ##################################################################
    # To change what extrapolation data we use, alter these vars below:
    ##################################################################
    
    # This is the user-defined coverage (used in option 3 only):
    user_defined_future_coverage = [0.566, 0.566]
    
    # This just sets up what the data looks like (how it's divided by age/sex):
    ages = [str(a) for a in range(18, 80)] + ["80+"]
    genders = ["M", "F"]
    
    extrapolation_data = read_chips_infile(round_to_extrapolate_from, output_dir)
    
    # Pull out the header of the previous CHiPs round to use in the post-trial round file
    header = extrapolation_data[0]
    
    end_of_popart = float(extrapolation_data[-1].split()[0])
    
    [CHIPSSTART_FUTUREROUND,CHIPSEND_FUTUREROUND,NTIMESTEPS_POSTTRIAL] = \
        get_chips_round_timing(end_of_popart, 
            immediate_start_of_post_popart_rounds,
            NTIMESTEPS_PER_CALENDAR_YEAR,
            DURATION_POSTTRIAL_CHIPS_ROUNDS)
    
    indices = make_dictionary_ages_to_column_number(ages, genders)
    
    [annual_coverage_for_extrapolation,numberoftimesteps_in_extrapolation_round] = \
        analyse_extrapolation_data(ages, genders, extrapolation_data, \
            IMPROVEMENTINPOSTTRIAL, indices)
    
    outstring = create_output_string(annual_coverage_for_extrapolation, 
        numberoftimesteps_in_extrapolation_round, 
        user_defined_future_coverage, OPTION, 
        NTIMESTEPS_POSTTRIAL, genders, ages, header)
    
    utils.write_file(output_dir + "/" + "param_processed_patch" + \
        str(patch_number) + "_chipsuptake_roundposttrial.csv", outstring)
