
CARRY_OUT_DIRECT_COMPARISON = 0 # Set to 1 to compare .c, .h files to a given template directory

# Python script to make sure that the C and data files on the HPC are OK.

# Compares C code to template, and checks that the constants.h constants are OK (i.e. we only generate Annual_outputs and Calibration).

# To do: Check the job.sh script.

import difflib,glob,re,sys

# These contain the original ("template") code, and the new one:
template_directory = "src/"
directory_to_check = "../src_check/"



def check_file(filename1,filename2):

    with open(filename1,'r') as hosts0:
        with open(filename2,'r') as hosts1:
            diff = difflib.unified_diff(hosts0.readlines(), hosts1.readlines(), fromfile='hosts0', tofile='hosts1', lineterm='', n=0)
            lines = list(diff)[2:]
            added = [line[1:] for line in lines if line[0] == '+']
            removed = [line[1:] for line in lines if line[0] == '-']

    if(added):
        print 'additions in ',filename1.split('/')[-1],':'
        for line in added:
            print line

    if(removed):
        print 'removals in ',filename1.split('/')[-1],':'
        for line in removed:
            print line


def get_files_to_check(template_dir):
    template_files = [x.split("/")[-1] for x in glob.glob(template_dir+"/*.[ch]")]
    return template_files


# These lines check each .c/.h file against the ones in the 'template_directory':
if(CARRY_OUT_DIRECT_COMPARISON==1):
    list_of_files = get_files_to_check(template_directory)
    for f in list_of_files:
        check_file(template_directory+f,directory_to_check+f)


    

def check_constants_file(filedir):
    infile = open(filedir+"/constants.h","r")

    constants_file = infile.read()
    infile.close()

    constants_should_be_zero = ["SIMPLE_PARTNERSHIP_CHECK","SWEEP_THROUGH_TO_CHECK_LISTS","SWEEP_THROUGH_TO_CHECK_N_PARTNERS_OUTSIDE_AND_N_HIVPOS_PARTNERS_AND_N_HIVPOS_PARTNERS_OUTSIDE","DEBUG_PARTNERSHIP_DURATION","CHECK_AGE_LIST","DEBUG_HIV_PREVENTION_CASCADES","WRITE_ANNUAL_PARTNERSHIPS_OUTPUTS","WRITE_HIVSURVIVAL_OUTPUT","WRITE_NEW_MALE_CIRCUMCISION_STATUS","VERBOSE_OUTPUT","CHECK_POPULATION_SIZE_CONSISTENCY","PRINT_HIV_PREVENTION_CASCADE_INFO","PRINT_DEBUG_DEMOGRAPHICS","WRITE_DEBUG_DEMOGRAPHICS_NBIRTHS_NEWADULTS_DEATHS","WRITE_DEBUG_DEMOGRAPHICS_AGE_DISTRIBUTION_ONEYEARINCKIDS","WRITE_DEBUG_DEMOGRAPHICS_LIFE_EXPECTANCY","PRINT_DEBUG_INPUT","WRITE_DEBUG_INITIAL_SPVL_DISTRIBUTION","WRITE_DEBUG_CD4_AFTER_SEROCONVERSION","WRITE_DEBUG_HIV_DURATION","WRITE_DEBUG_HIV_DURATION_KM","WRITE_DEBUG_HIV_STATES","WRITE_DEBUG_ART_STATE","WRITE_ART_STATUS_BY_AGE_SEX","WRITE_DEBUG_CHIPS_STATES","TIMESTEP_AGE","WRITE_PHYLOGENETICS_OUTPUT","WRITE_PARTNERSHIP_NETWORK_SNAPSHOT","WRITE_PARTNERS_OUTSIDE_COMMUNITY","WRITE_HAZARDS","WRITE_PARTNERSHIPS_AT_PC0","CHECKPARAMS","WRITE_EVERYTIMESTEP"]
    n_vars_needed = len(constants_should_be_zero)
    n_vars_found = 0

    for c in constants_should_be_zero:
        matchstr = "#define\s+"+c+"\s[01]"
        x = re.search(matchstr, constants_file)
        if(not(x)):
            print "Huh - can't find",c
            sys.exit(1)
        else:
            #print "Found:",constants_file[x.start():].splitlines()[0]
            if(x.group().split(" ")[-1]!="0"):
                print "***Error - constant",c," not set to zero***"
                sys.exit(1)
            n_vars_found += 1
        
        # for l in constants_file:
        #     matchstr = "#define\s+"+c+"\s[01]"
        #     x = re.search(matchstr, l)
        #     if(x):
        #         #print l[x.start():]
        #         if(x.group().split(" ")[-1]!="0"):
        #             print "***Error - constant",c," not set to zero***"





    constants_should_be_one = []
    n_vars_needed += len(constants_should_be_one)
    for c in constants_should_be_one:
        matchstr = "#define\s+"+c+"\s[01]"
        x = re.search(matchstr, constants_file)
        if(not(x)):
            print "Huh - can't find",c
            sys.exit(1)
        else:
            #print "Found:",constants_file[x.start():].splitlines()[0]
            if(x.group().split(" ")[-1]!="1"):
                print "***Error - constant",c," not set to one***"
                sys.exit(1)
            n_vars_found += 1
        




    
    # Now special ones:
    special_vars = ["WRITE_DHS_CALIBRATION","WRITE_COST_EFFECTIVENESS_OUTPUT"]
    n_vars_needed += len(special_vars)
    
    for c in special_vars:
        matchstr = "#define\s+"+c+"\s[01]"
        # Make sure the string is present somewhere:
        x = re.search(matchstr, constants_file)
        if(not(x)):
            print "Huh - can't find",c
            sys.exit(1)
        else:
            #print "Found:",constants_file[x.start():].splitlines()[0]
            if(x.group().split(" ")[-1]!="0"):
                print "Please check - constant",c," not set to zero. Is this correct?"
                print constants_file[x.start():].splitlines()[0]
                print
            n_vars_found += 1



        # for l in constants_file:        
        #     x = re.search(matchstr, l)
        #     if(x):
        #         #print l[x.start():]
        #         if(x.group().split(" ")[-1]!="0"):
        #             print "Please check - constant",c," not set to zero. Is this correct?"
    


    matchstr = "#define\s+FOLLOW_INDIVIDUAL\s[-]{0,1}[1-9]+[0-9]*"
    n_vars_needed += 1
    x = re.search(matchstr, constants_file)
    if(not(x)):
        print "Huh - can't find FOLLOW_INDIVIDUAL"
    #print "Found",constants_file[x.start():].splitlines()[0]
    if(x.group().split(" ")[-1]!="-1"):
        print "Please check - FOLLOW_INDIVIDUAL is not set to -1. Is this correct?"
    n_vars_found += 1

    if(n_vars_found!=n_vars_needed):
        print "***ERROR - didn't find some variables",n_vars_found,n_vars_needed
    
    
check_constants_file("src")
#" 0 /* Write DHS outputs to Calibration*.csv files. */
# -1

# 0 /*  Generates a new file cost_effectiveness_$.csv */
    

def check_param_values_expected(param_filename,expected_values):
    param_file = open("data/GENERATED_PRIORS/PARAMS_COMMUNITY5/"+param_filename)
    param = param_file.readlines()
    param_file.close()
    v =expected_values.keys()
    # Go through the file line-by-line:
    for l in param:
        thisvar = l.split()[0]
        if thisvar in v:
            if(l.split()[1]!=expected_values[thisvar]):
                print "Unexpected value in",param_filename,"for:",thisvar,l.split()[1],expected_values[thisvar]
            else:
                print thisvar," is OK"


print "\nChecking parameter files:"

expected_values_times = {"start_time_hiv":"1960", "start_time_simul":"1900","end_time_simul":"2030"}
check_param_values_expected("param_times.txt",expected_values_times)


expected_values_init = {"initial_adult_population_size":"750"}
check_param_values_expected("param_init.txt",expected_values_init)

print "\nChecking job script number of runs and array size"
infile=open("job_Manicaland.sh","r")
jobfile = infile.readlines()
infile.close()
for l in jobfile:
    if l[:7]=="#PBS -J":
        reps=l.split()[2]
        print "Number of array reps=",reps
    elif l[:9]=="nsamples=":
        nsamples = l[9:].split()[0]
        if(int(nsamples)<500):
            print "***WARNING - number of samples is ",nsamples
        else:
            print "Number of samples=",nsamples
