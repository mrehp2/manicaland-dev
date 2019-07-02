import random,copy,sys
from os.path import join

# Create the header for the output files. This isn't essential but helps readability:
def make_header(MINAGE,MAXAGE):
    header = "time year t_step " 
    # The header includes lots of terms along the lines of n_enrolled_in_PC0_with_HIV_test_HIVnegM18 n_enrolled_in_PC0_with_HIV_test_HIVnegM19 ...n_enrolled_in_PC0_with_HIV_test_HIVnegM44 n_enrolled_in_PC0_with_HIV_test_HIVnegF18... so use the following to make it:
    # (note that in python range(a,b) goes from a..(b-1) so we make MAXAGE 45 instead of 44).
    header += " ".join(["n_enrolled_in_PC0_with_HIV_test_HIVnegM"+str(i) for i in range(MINAGE,MAXAGE)])+" "+" ".join(["n_enrolled_in_PC0_with_HIV_test_HIVnegF"+str(i) for i in range(MINAGE,MAXAGE)]) + " "
    header += " ".join(["n_enrolled_in_PC0_with_HIV_test_HIVposAwareM"+str(i) for i in range(MINAGE,MAXAGE)])+" "+" ".join(["n_enrolled_in_PC0_with_HIV_test_HIVposAwareF"+str(i) for i in range(MINAGE,MAXAGE)]) + " "
    header += " ".join(["n_enrolled_in_PC0_with_HIV_test_HIVposUnawareM"+str(i) for i in range(MINAGE,MAXAGE)])+" "+" ".join(["n_enrolled_in_PC0_with_HIV_test_HIVposUnawareF"+str(i) for i in range(MINAGE,MAXAGE)]) + "\n"
    return header


# Read in the existing PC0 visit schedule data:
def read_pc0_data(pc0file):
    firstrounddatafile = open(pc0file,"r")
    firstrounddata_str = [x.split(" ")[3:] for x in firstrounddatafile.read().rstrip().split("\n")[1:]]
    firstrounddatafile.close()

    # Stoee the data in this array.
    firstrounddata = []
    for i in firstrounddata_str:
        firstrounddata += [[int(x) for x in i]]
    pc0_duration = len(firstrounddata_str)

    return [firstrounddata,pc0_duration]



# We assume R1 is ALWAYS longer than future rounds (because R1 was a learning experience in the trial, and there were lots of issues with e.g. EDC tablets). 
# The assumption we make for round i_round (i_round>0) is the following:
# Define  d_0=pc_duration[0], and PC[i_round] is duration d_i=pc_duration[i_round] (these are the number of timesteps in the PC rounds).
# We start by counting the number of people seen in each timestep t for t>d_i in PC0 - these are the 'extras'.
# We then copy the visit schedule from timestep 0 to d_i from R1 to the current round (note that at present we have not included the 'extras').
# Finally we add the 'extras' in between time 0 and d_i (this process is described below) - to make sure that in the current round we have seen everyone (we assume here that folloow-up is 100%).
def count_extras(firstrounddata,pc_duration,i_round):

    n_groups = len(firstrounddata[0]) # Number of subdivisions of data (e.g. by age, gender, HIV status/awareness)

    # This will store the number of 'extra' people:
    extras = []
    for i in range(n_groups):
        extras += [0]

    # Now go through the PC0 visit data to count the "extra" people in round i_round (people visited a time pc_duration[i_round] or later after the start of the PC0 round).
    for line in firstrounddata[pc_duration[i_round]:]:
        for i in range(len(line)):
            extras[i] += line[i]
    # Return the extras in this round. Note that the 'extras' may differ in each round if the lenght of that round is different.
    return extras


def make_pc_round_timing_variables(this_community, NROUNDS):
    """
    Set up the start, end, and length of each PC round
    
    Notes
    -----
    E-mail from Alicia Young, 8 Sept 2016:
    
    PC12 started in July 2015 in SA and August 2015 in Zambia, and ended June 30, 2016 in both 
    countries.  First timestep in July 2015 is timestep 24. First timestep in August 2015 is 
    timestep 28 t=0.583333. 30 June 2016 is timestep 23.8, so round to timestep 24 = 0.5. So 
    duration in Zambia is 44 timesteps, 48 timesteps in SA.  PC24 has just started (around 15th 
    August) in SA and is set to start around September 20th  in Zambia.
    Sept 20 = 263/365 days=34.586 timesteps, so call it 35 timesteps=0.729167
    15 august is 227/365 days=29.9 timesteps, so call it 30 timesteps=0.625
    I believe PC24 is set to end in May or June 2017, and PC36 will commence in July or August 2017,
    and I am not sure of the PC36 end date.  End of May is 19.9 timesteps so call it 
    20 timesteps = 0.41667. First timestep in July is timestep 24=0.5.  PC round 1 is PC12, 
    PC round 2 is PC24, PC round 3 is PC36. PC0 dates are in the PC enrolment file.  
    
    
    Parameters
    ----------
    this_community : int
        Community for which the PC rounds are wanted
    NROUNDS : int
        Number of PC rounds of interest
    
    
    Returns
    -------
    list of the form [pc_start, pc_end, pc_duration]
    
    pc_start : list
        Starting date of PC rounds, in decimal years.  Start date of PC0 is not generated here so 
        first element is always zero.
    pc_end : list
        End date of PC rounds, in decimal years.  End date of PC0 is not generated here so first 
        element is always zero.
    pc_duration : list
        Duration of each of the PC rounds.  Duration of PC0 is not generated here so first element 
        is always zero.  
    
    
    Example
    -------
    # Output start, end, and duration of all four PC rounds for community 4
    make_pc_round_timing_variables(4, 4)
    >>[[0, 2015.58333, 2016.729167, 2017.5], 
    >> [0, 2016.5, 2017.41667, 2018.5], 
    >> [0, 44, 33, 48]]
    
    # Output start, end, and duration of first three PC rounds for community 19
    make_pc_round_timing_variables(19, 3)
    >> [[0, 2015.5, 2016.625, 2017.5], 
    >> [0, 2016.5, 2017.41667, 2018.5], 
    >> [0, 48, 38]]
    """
    if (this_community <=12):
        PC_ROUND1_START = 2015.58333  
        PC_ROUND1_END = 2016.5
        PC_ROUND2_START =  2016.729167
        PC_ROUND2_END = 2017.41667
        PC_ROUND3_START = 2017.5 
        PC_ROUND3_END = 2018.5
    else: # South Africa
        PC_ROUND1_START = 2015.5
        PC_ROUND1_END = 2016.5
        PC_ROUND2_START =  2016.625
        PC_ROUND2_END = 2017.41667
        PC_ROUND3_START = 2017.5 
        PC_ROUND3_END = 2018.5
    
    # Note that we're not generating the PC0 data so no need for PC0 dates here. 
    # We get the pc0 duration later directly from the PC0 data file.
    pc_start = [0, PC_ROUND1_START, PC_ROUND2_START, PC_ROUND3_START]
    pc_end = [0, PC_ROUND1_END, PC_ROUND2_END, PC_ROUND3_END]
    
    pc_duration = []
    
    # Assign dummy values for now:
    for round in range(NROUNDS):
        pc_duration += [0]
    
    for i_round in range(1,NROUNDS):
        pc_duration[i_round] = int((pc_end[i_round] - pc_start[i_round])*48)
    
    return [pc_start, pc_end, pc_duration]


def reschedule_extras_visits(extras, firstrounddata, pc_duration, 
        i_round, future_visit_data_i_round):
    
    n_groups = len(firstrounddata[0]) # Number of subdivisions of data (e.g. by age, gender, HIV status/awareness)

    for i in range(n_groups):
        while (extras[i]>=pc_duration[i_round]):
            for j in range(pc_duration[i_round]):
                future_visit_data_i_round[j][i] += 1        # Add an extra visit for each timestep.
            extras[i] = extras[i] - pc_duration[i_round]

        # For the remaining extras, schedule them randomly in time 0-(pc_duration[i_round]-1) (and schedule a maximum of 1 additionalvisit per timestep).
        indices_to_add_to = random.sample(range(pc_duration[i_round]),extras[i])
        for j in indices_to_add_to:
            future_visit_data_i_round[j][i] += 1            # Add an extra visit for each chosen timestep.
    return future_visit_data_i_round


#################################################################################
################################ MAIN FUNCTION ##################################
#################################################################################

def make_future_pc_visit_schedule(RANDOMSEED, pc0file, this_community, 
        patch_number, output_dir, NROUNDS):
    # Sets the seed for when we assign the 'extras' randomly.
    random.seed(RANDOMSEED)
    
    MINAGE = 18
    MAXAGE = 45     # As stated when defining header variable below, note that in python range(a,b) goes from a..(b-1) so we make MAXAGE 45 instead of 44
    
    # We input the PC12-PC36 (i_round=1,2,3) start and end dates based on e-mails from SCHARP. We DON'T have the PC12-36 data until the end of the trial.
    [pc_start,pc_end,pc_duration] = make_pc_round_timing_variables(this_community,NROUNDS)

    # Get PC0 data from data file produced by Anne.
    [firstrounddata,pc_duration[0]] = read_pc0_data(pc0file)


    # Make sure no future round is shorter than R1 (only matters for community 6) - this is needed because of the algorithm we use (but can probably be modified though.
    for i_round in range(1,NROUNDS):
        while pc_duration[i_round]>pc_duration[0]:
            print("Shortening round ",i_round," by 1 timestep in community",this_community)
            pc_duration[i_round] = pc_duration[i_round]-1
            pc_end[i_round] = pc_end[i_round] - 1/48.0


    # futuredata is a dictionary made up of lists of future data (with dictionary keys 1,...NROUNDS).
    futuredata = {}
    for i_round in range(1,NROUNDS):
        # We first assume that the future rounds look like the current round. We will later adjust for the fact that the future rounds may be shorter.
        futuredata[i_round] =  copy.deepcopy(firstrounddata[0:pc_duration[i_round]])

        # Work out how many 'extra' people need to have a visit rescheduled:
        extras = count_extras(firstrounddata,pc_duration,i_round)


        # If there are >= people in group i to be added than there are timesteps in the current round, then firstly schedule one visit per timestep (ie schedule pc_duration[i_round] visits. 
        # The remaining number of people to visit is extras[i]-pc_duration[i_round] - set this to be the new value for extras[i]. Repeat until extras[i] is less than the number of timesteps.
        updated_visit_data = reschedule_extras_visits(extras,firstrounddata,pc_duration,i_round,futuredata[i_round])
        futuredata[i_round] = copy.deepcopy(updated_visit_data)


    # Make a header for the output file (we use the same header for each file).
    header = make_header(MINAGE,MAXAGE)
    


    for i_round in range(1,NROUNDS):
        # Outstring will contain all the information in the file for this round. We start by putting the header and then add the rest after.
        outstring = header

        pc_start_discrete_year = int(pc_start[i_round])
        pc_start_timestep = int((pc_start[i_round] - pc_start_discrete_year)*48)
        for t in range(pc_duration[i_round]):
            tstep_now = t+pc_start_timestep
            year_now = pc_start_discrete_year
            while(tstep_now>=48):
                year_now = year_now + 1
                tstep_now = tstep_now-48
            
            outstring += str(pc_start[i_round]+t/48.0) + " " + str(year_now) + " " + str(tstep_now) + " " + " ".join([str(x) for x in futuredata[i_round][t]])+"\n"
        
        outfilename = join(output_dir, "param_processed_patch" + str(patch_number) + 
            "_PC" + str(i_round) + "_community" + str(this_community) + ".csv")
        
        outfile = open(outfilename,"w")
        outfile.write(outstring)
        outfile.close()


#for p in range(1):
#    make_future_pc_visit_schedule(20,"/Users/mike/Dropbox/PoPART/Data:Stats/PC Data Downloads/15-12-2016_PC0_NEWFINAL/R/PC0schedules/PC0_schedule_by_HIV_status_age_and_gender_community5.csv",5,p,"TEMPLATE/OUTPUT_TESTING/",4)
