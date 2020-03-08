# To do:
# need to make likelihood capable of dealing with LL=0 situations (k=0, n=0, p=0).
# also make likelihood group by age (e.g. calculate over 5 year age groups - may help with the zeros).

import glob, sys, os, re, math
#import itemgetter # use to find max N log likelihoods from dict.

def read_calibration_file(infilename):
    infile = open(infilename,"r")
    calibration_data_strings = infile.read().rstrip().splitlines()
    header = [calibration_data_strings[0].rstrip(",").split(",")]
    calibration_data = []
    for line in calibration_data_strings[1:]:
        split_line = line.rstrip(",").split(",")
        calibration_data += [[int(x) for x in split_line]]
    return [header,calibration_data]


def get_calibration_results_dirs(calibration_root_dir):
    possible_calibration_results_dirs = [x[0] for x in os.walk(calibration_root_dir)]
    # Now check that these are of the form "..../RESULTSX":
    checked_dirs = []
    pattern = re.compile("^(RESULTS[1-9]+[0-9]*)")
    for dir in possible_calibration_results_dirs:
        string_to_check = dir.split("/")[-1]
        if pattern.match(string_to_check):
            checked_dirs += [dir]
    checked_dirs.sort()
    return checked_dirs


def decompose(file_name):
    cluster_no = file_name.split("CL")[1].split("_")[0]
    country = file_name.split("_")[3].split("_")[0]
    version = file_name.split("_")[4].split("_")[0].lstrip("V")
    patchno = file_name.split("_patch")[1].split("_")[0]
    rand = file_name.split("_Rand")[1].split("_")[0]
    if ("PCseed" in file_name):
        pcseed = file_name.split("_PCseed")[1].split("_")[0]
    else:
        pcseed = -1
    randseed = file_name.split("_")[-1].rstrip(".csv")

    return [cluster_no,country,version,patchno,rand, pcseed,randseed]


    
def check_calibration_files_consistent(dir_list):
    #print "in check_calibration_files_consistent dir_list=",dir_list
    checked_files = []
    for i in range(len(dir_list)):
        potential_calibration_files = glob.glob(dir_list[i]+"/Calibration*.csv")
        for j in range(len(potential_calibration_files)):
            # Get the filename:
            f_name = potential_calibration_files[j].split("/")[-1]
            if (i==0 and j==0):
                # Check that the first filename is consistent with all the other filenames:
                [community,country,version,patchno,rand,pcseed,randseed] = decompose(f_name)
            else:
                # if there is no "PCseed": 
                if pcseed==-1:
                    pattern = re.compile("Calibration_output_CL"+community+"_"+country+"_V"+version+"_patch"+patchno+"_Rand[1-9]+[0-9]*_[0-9]+.csv")
                    if not(pattern.match(f_name)):
                        print "Error: filename",f_name," does not match expected format with no pcseed"
                        sys.exit(1)
                else:
                    pattern = re.compile("Calibration_output_CL"+community+"_"+country+"_V"+version+"_patch"+patchno+"_Rand[1-9]+[0-9]*_PCseed"+pcseed+"_[0-9]+.csv")
                    if not(pattern.match(f_name)):
                        print "Error: filename",f_name," does not match expected format with no pcseed"
                        sys.exit(1)
            checked_files += [potential_calibration_files[j]]       
            #print "Checked that ",f_name," is OK"

    return [checked_files,community]


def add_slash(directory):
    if directory[-1]=="/":
        return directory
    else:
        return directory+"/"


def make_age_grouping_dictionary(min_age,max_age, width):
    # Use integer division:
    offset = min_age/width   # This is the 0 group.
    age_grouping_dictionary = {}
    for a in range(min_age,max_age+1):
        age_grouping_dictionary[a] = a/width - offset
    return age_grouping_dictionary
    

def test_condition(a,f,n,r,g,denominator):
    if (a in range(40,45) and f.split("/")[-2]=="RESULTS2" and n==2 and r=="R1" and g=="M" and denominator=="Ntot"):
        return 1
    elif (a in range(20,25) and f.split("/")[-2]=="RESULTS2" and n==10 and r=="R2" and g=="F" and denominator=="Npos"):
        return 1
    elif (a in range(65,70) and f.split("/")[-2]=="RESULTS2" and n==39 and r=="R2" and g=="F" and denominator=="Naware"):
        return 1
    else:
        return 0
        

#################################################
###      Read in IBM calibration files:      ####
#################################################

def read_ibm_calibration_files(calibration_root_dir):
    # Ensure that the directory ends in "/":
    calibration_root_dir = add_slash(calibration_root_dir)

    # Get all the sub-directories where the Calibration*.csv files are:
    calibration_results_dirs = get_calibration_results_dirs(calibration_root_dir)
    # Print where we're getting results from:
    print calibration_results_dirs
    # Find the files in those sub-directories, and check that they are all named the right way e.g. Calibration_output_CL05_Zim_V2.0_patch0_Rand1_PCseed0_0.csv 
    [calibration_files,community] = check_calibration_files_consistent(calibration_results_dirs)

    # Number of files
    nfiles = len(calibration_files)
    print "Number of IBM calibration files to read = ",nfiles
    # Now read in the data and header from each file:
    calibration_data = {}
    for f in calibration_files:
        calibration_data[f] =[]

    
    header = [[] for i in range(nfiles)]
    for i in range(nfiles):
        [header[i],calibration_data[calibration_files[i]]] = read_calibration_file(calibration_files[i])

    # Check that all the headers match:
    for i in range(1,nfiles):
        if header[0]!=header[i]:
            print "Error: header files do not match for files", calibration_files[0], calibration_files[i]
            sys.exit(1)

    # Here we get the header, so we can write it to make the calibration file header for the best N runs.
    full_header = []
    for i in header:
        full_header += i
    full_header_string = ",".join(full_header[0])
    return [community,header[0][0],calibration_data,full_header_string]

# For survey data split things like "M25" or "F46" to be gender+age:
def split_survey_datatype(instring):
    m = re.match("^([MF])([0-9]+)",instring)
    gender = m.group(1)
    age = int(m.group(2))
    return [gender,age]
    

# For IBM calibration file:
def unpack_header(header):
    if (not(header[0]=="SampleNumber") or not(header[1]=="RepNumber") or not(header[2]=="RunNumber") or not(header[3]=="RandomSeed")):
        print "error in header for IBM calibration file: first 4 entries should be SampleNumber, RepNumber, RunNumber, RandomSeed. Exiting\n"
        sys.exit(1)

    surveytypes = {}
    rounds = []
    datatypes = []
    age = []

    # We will use this to get the column number from the variable name:
    lookup_table = {}
    header_offset = 0

    # First 4 columns aren't variables:
    for i in range(4,len(header)):
        h = header[i]

        lookup_table[h] = i
                     
        #m = re.match("^([a-Z]+)Round([0-9])(?:Ntot|Npos)([MF])([0-9]+)", h)
        m = re.match("^([a-zA-Z]+)Round([0-9])([a-zA-Z]+)([MF])([0-9]+)", h)
        thissurveytype = m.group(1)
        if not(thissurveytype in surveytypes.keys()):
            surveytypes[thissurveytype] = {}
        
        round = "R"+m.group(2)
        if not(round in surveytypes[thissurveytype].keys()):
            surveytypes[thissurveytype][round] = {}
        
        thisdatatype = m.group(3)
        if not(thisdatatype in surveytypes[thissurveytype][round].keys()):
            surveytypes[thissurveytype][round][thisdatatype] = {}
        gender = m.group(4)
        if not(gender in surveytypes[thissurveytype][round][thisdatatype].keys()):
            surveytypes[thissurveytype][round][thisdatatype][gender] = {}
            surveytypes[thissurveytype][round][thisdatatype][gender]["All_ages"] = []
        surveytypes[thissurveytype][round][thisdatatype][gender]["All_ages"] += [int(m.group(5))]


    for survey in surveytypes.keys():
        for round in surveytypes[survey].keys():
            for datatype in surveytypes[survey][round].keys():
                for gender in surveytypes[survey][round][datatype].keys():

                    surveytypes[survey][round][datatype][gender]["minage"] = min(surveytypes[survey][round][datatype][gender]["All_ages"])
                    surveytypes[survey][round][datatype][gender]["maxage"] = max(surveytypes[survey][round][datatype][gender]["All_ages"])

                    # Remove this as it's not needed: 
                    del surveytypes[survey][round][datatype][gender]["All_ages"]
    return [surveytypes,lookup_table]




def structure_ibm_data(model_data_array, header):
    [ibm_datatypes,lookup_table] = unpack_header(header)
    surveytypes = ibm_datatypes.keys()
    ibm_data_structure = {}
    #print model_data_array

    # We make the storage dictionary here, so we can have it arranged by survey type etc:

    for s in surveytypes:     # Look for different types of survey (DHS, CHiPs, cohort).
        ibm_data_structure[s] = {}
        for f in model_data_array.keys(): # Go through each Calibration.csv file:
            ibm_data_structure[s][f] = []
            nruns = len(model_data_array[f])
            # Create an array of (blank) dictionaries - each element of the array is a run from a calibration file.
            for n in range(nruns):
                ibm_data_structure[s][f] += [{}]

            #Now fill the array of dictionaries.
            for n in range(nruns):        # Go through the runs in a single Calibration.csv file.                 
                rounds = ibm_datatypes[s].keys()
                for r in rounds:      # Rounds of the given survey type:
                    ibm_data_structure[s][f][n][r] = {}                
                    datatypes = ibm_datatypes[s][r].keys()
                    for t in datatypes:   # Outcomes (prevalence, 90-90-90 etc collected in the survey).
                        ibm_data_structure[s][f][n][r][t] = {}
                        genders = ibm_datatypes[s][r][t].keys()
                        for g in genders:
                            ibm_data_structure[s][f][n][r][t][g] = {}
                            # We do ages when we enter data into the structure.

    
    # Now we put the data from each Calibration file into ibm_data_structure:
    for f in model_data_array.keys(): # Go through each Calibration.csv file:
        nruns = len(model_data_array[f])
        for n in range(nruns):        # Go through the runs in a single Calibration.csv file.
            for s in surveytypes:     # Look for different types of survey (DHS, CHiPs, cohort).
                rounds = ibm_datatypes[s].keys()
                for r in rounds:      # Rounds of the given survey type:
                    datatypes = ibm_datatypes[s][r].keys()
                    for t in datatypes:   # Outcomes (prevalence, 90-90-90 etc collected in the survey).
                        genders = ibm_datatypes[s][r][t].keys()
                        for g in genders:
                            ages = range(ibm_datatypes[s][r][t][g]['minage'],ibm_datatypes[s][r][t][g]['maxage']+1)
                            for a in ages:
                                dataname = s+r.replace("R","Round")+t+g+str(a)
                                i = lookup_table[dataname]
                                ibm_data_structure[s][f][n][r][t][g][a] = model_data_array[f][n][i]

    return ibm_data_structure
#for surevytype in :
#        print surveytype,": rounds ",
#    for r in ibm_datatypes[surveytype].keys():
#        for t in ibm_datatypes[surveytype][r].keys():
#            print ibm_datatypes[surveytype][r][t].keys()

    
###########################################################################
# Read in data files from CHiPs or Manicaland:                            #
# Code reads in ONLY ONE TYPE OF DATA (e.g. CHIPS, COHORT, DHS)           #
# so need to call multiple times if working with different types of data. #
###########################################################################
def read_survey_files(rounds):

    # When opening a file python can't apparently use '~' directly. But os.path.expanduser('~')
    # gives the expanded path (e.g. /home/me).
    homedir = os.path.expanduser('~')
    survey_data_dir = homedir+"/Dropbox (SPH Imperial College)/Manicaland/Model/"
    # These need to match the IBM outputs.
    dictionary_survey_to_IBMoutput = {"All": "Ntot", "HIV+":"Npos", "AwareOfStatus":"Naware", "OnART":"NonART"}


    survey_data_store = {}
    for r in rounds:
        this_round = "R"+str(r)
            
    for r in rounds:
        thisround = "R"+str(r)

        # Make dictionary to store data for this round:
        survey_data_store[thisround] = {}
        for d in dictionary_survey_to_IBMoutput:
            datatype = dictionary_survey_to_IBMoutput[d]
            survey_data_store[thisround][datatype] = {}
            for g in ["M","F"]:
                survey_data_store[thisround][datatype][g] = {}


        
        print "***PLACEHOLDER HERE***"

        survey_data_filename = survey_data_dir+"CalibrationData/Manicalandr"+str(r)+"_calibration_data.txt"
        #survey_data_filename = survey_data_dir + "Round1/TimeOfChipsVisits/cascade_by_gender_age_table_n_round1_community1.txt"

        survey_file = open(survey_data_filename)
        survey_data = survey_file.read().rstrip().splitlines()
        header = survey_data[0].split(" ")
        for line in survey_data[1:]:
            linedata = line.split(" ")
            datatype = dictionary_survey_to_IBMoutput[linedata[0]]

            #survey_data_store[datatype] = [int(x) for x in linedata[1:]]
            for i in range(1,len(linedata)):
                # Header is 1 index off linedata:
                [gender,age] = split_survey_datatype(header[i-1])
                survey_data_store[thisround][datatype][gender][age] = int(linedata[i])
            
    return [header,survey_data_store]


def get_cohort_likelihood(survey_data,model_data, age_groupings, N_BESTFITS):
    survey_rounds = survey_data.keys()

    model_data_files = model_data.keys()
    model_data_runs = len(model_data[model_data_files[0]])
    
    model_data_rounds_dict = model_data[model_data_files[0]][0]
    model_data_rounds = model_data_rounds_dict.keys()

    model_data_datatypes_dict = model_data_rounds_dict[model_data_rounds[0]]
    model_data_datatypes = model_data_datatypes_dict.keys()
    
    model_data_genders_dict = model_data_datatypes_dict[model_data_datatypes[0]]
    model_data_genders = model_data_genders_dict.keys()

    model_data_age_dict = model_data_genders_dict[model_data_genders[0]]
    model_data_age = model_data_age_dict.keys()

    age_group_indices = []
    for k in age_groupings.keys():
        if not(age_groupings[k] in age_group_indices):
            age_group_indices += [age_groupings[k]]
    print age_group_indices
    model_k = []
    model_N = []
    survey_k = []
    survey_N = []

    for age_gp_index in age_group_indices:
        model_k += [0]
        model_N += [0]
        survey_k += [0]
        survey_N += [0]

    print model_data_rounds
    print model_data_datatypes
    print model_data_genders
    print model_data_age
    
    print survey_rounds
    # Check that survey_rounds is a subset of model_data_rounds:
    if not(set(survey_rounds) <= set(model_data_rounds)):
        print "Error: IBM model data does not have the same rounds as the survey data"
        sys.exit(1)
        
    # For each indicator, look up the denominator:
    numerator_denominator = {"Npos":"Ntot", "Naware":"Npos", "NonART":"Naware"}
    numerators = numerator_denominator.keys()
    
    if not(set(numerator_denominator.keys()) <= set(model_data_datatypes)):
        print "Error: IBM model data contains indicators not given in get_cohort_likelihood(). Need to extend numerator_denominator"
        sys.exit(1)
        
    # Store log-likelihoods:
    log_likelihood_by_round = {}
    for f in model_data_files:
        for n in range(model_data_runs):
            log_likelihood_by_round[(f,n)] = 0

    #print model_data["/home/mike/MANICALAND/manicaland-dev/IBM_simul/results2/RESULTS2/Calibration_output_CL05_Zim_V2.0_patch0_Rand10_PCseed0_0.csv"][1]["R1"]["Ntot"]["F"]
                
    # IBM data store format is ibm_data_structure[s][f][n][r][t][g][a].
    for f in model_data_files:
        for n in range(model_data_runs):
            for r in survey_rounds:
                # Loop through survey types:
                for numerator in numerators:
                    denominator = numerator_denominator[numerator]
                    #for t in  model_data_datatypes:
                    for g in model_data_genders:
                        for age_gp_index in age_group_indices:
                            model_k[age_gp_index] = 0
                            model_N[age_gp_index] = 0
                            survey_k[age_gp_index] = 0
                            survey_N[age_gp_index] = 0
                        sum = 0
                        for a in model_data_age:
                            age_gp_index = age_groupings[a]
                            model_k[age_gp_index] += model_data[f][n][r][numerator][g][a]
                            model_N[age_gp_index] += model_data[f][n][r][denominator][g][a]
                            survey_k[age_gp_index] += survey_data[r][numerator][g][a]
                            survey_N[age_gp_index] += survey_data[r][denominator][g][a]
                            if test_condition(a,f,n,r,g,denominator):
                                sum += model_data[f][n][r][denominator][g][a]
                                #print n,r,g,denominator,sum,age_gp_index,model_data[f][n][r][denominator][g][a]
                       # print sum#print model_k[age_gp_index],model_N[age_gp_index]
                                
                        #
                                                
                        for age_gp_index in age_group_indices:
                            #print "PP",g,age_gp_index, numerator,denominator
                            log_likelihood_by_round[(f,n)] += calculate_log_likelihood(survey_k[age_gp_index],survey_N[age_gp_index],model_k[age_gp_index],model_N[age_gp_index])

    #Print for debugging - checked that sorting works OK.
    #for f in model_data_files:
    #    for n in range(model_data_runs):
    #        print f.split("/")[-2:-1],n,log_likelihood_by_round[(f,n)]

    # Needs python3!
    #res = dict(sorted(log_likelihood_by_round.items(), key = itemgetter(1), reverse = True)[:10])

    res = sorted( log_likelihood_by_round.items(), key=lambda pair: pair[1], reverse=True )[:N_BESTFITS]
    return res
        

# Given k observed 'heads' out of N trials, calculate the associated log-likelihood (log to base e):
def calculate_log_likelihood(survey_k, survey_N, model_k, model_N):

    # If denominator is zero, then ignore this:
    if ((model_N==0) or (survey_N==0)):
        return 0

    model_p = model_k/float(model_N)
    if (model_k==0):
        if (survey_k==0):
            return 0
        else:
            model_p=(model_k+0.5)/float(model_N)

    if (model_k==model_N):
        if (survey_k==survey_N):
            return 0
        else:
            model_p = (model_k-0.5)/float(model_N)

    #print model_k,model_N,model_p,survey_k,survey_N
    try:
        log_likelihood = math.log(math.factorial(survey_k)) + survey_k*math.log(model_p)+(survey_N-survey_k)*math.log(1-model_p)-math.log(math.factorial(survey_N)) - math.log(math.factorial(survey_N-survey_k))
    except:
        print "XXX",model_k,model_N,model_p,survey_k,survey_N
        print Ramunajan_approximation(survey_k)
        print survey_k*math.log(model_p)
        print (survey_N-survey_k)*math.log(1-model_p)
        print Ramunajan_approximation(survey_N)
        print Ramunajan_approximation(survey_N-survey_k)
        log_likelihood = Ramunajan_approximation(survey_k) + survey_k*math.log(model_p)+(survey_N-survey_k)*math.log(1-model_p) -Ramunajan_approximation(survey_N) - Ramunajan_approximation(survey_N-survey_k)
        # Use math.log10() for log_10.

    return log_likelihood

# Approximate ln(N!) using Stirling:
def stirling_approximation(N):
    return N*math.log(N) - N + 0.5*math.log(2*math.pi * N)
# So much more awesome than Stirling: e.g. for N=100, difference between Stirling and true value is ~O(0.001), but for Ramunajan it's O(10^-10).
def Ramunajan_approximation(N):
    return N*math.log(N) - N + math.log(N*(1+4*N*(1+2*N)))/6.0 + 0.5*math.log(math.pi)


#################################################
###      Main code:      ####
#################################################

calibration_root_dir = "/home/mike/MANICALAND/manicaland-dev/IBM_simul/results_new/"
[community, header, model_data_array,full_header_string] = read_ibm_calibration_files(calibration_root_dir)



# Find out what the IBM is storing - we will compare this against survey data later:
ibm_datatypes = unpack_header(header)
ibm_model_data_structured = structure_ibm_data(model_data_array,  header)






#chips_survey_data_dir = "/home/mike/Dropbox (SPH Imperial College)/PoPART/Data:Stats/CHiPs data/"


survey_data = {}
rounds = [6]
# For each type of data (cohort, DHS, CHiPS) etc we call read_survey_files:
[header,survey_data["Cohort"]] = read_survey_files(rounds)
#print survey_data

#print ibm_model_data_structured

# Make 5 year age groups 10-14, 15-19, 20-24 etc up to 75-79.
age_groupings = make_age_grouping_dictionary(10,79, 10)

# Last argument is number of best fits to get.
likelihood_cohort = get_cohort_likelihood(survey_data["Cohort"],ibm_model_data_structured["Cohort"], age_groupings, 10)


best_model_calibration_filename = "Calibration_data_bestfits.csv"
best_model_likelihood_filename = "goodfits.txt"

best_model_calibration_file = open(best_model_calibration_filename,"w")
best_model_likelihood_file = open(best_model_likelihood_filename,"w")

best_model_calibration_data = full_header_string+"\n"
best_model_likelihood_output = ""

# Create file listing the files, lines and likelihoods of the best files:
for i in likelihood_cohort:
    best_model_likelihood_output += i[0][0]+" "+str(i[0][1])+" "+str(i[1])+"\n"

    best_model_calibration_data += ",".join([str(x) for x in model_data_array[i[0][0]][i[0][1]]])+"\n"

best_model_calibration_file.write(best_model_calibration_data)
best_model_likelihood_file.write(best_model_likelihood_output)

best_model_calibration_file.close()
best_model_likelihood_file.close()



# Call R to plot stuff:
os.system("Rscript plot_by_age_gender.R")
