# To do:
# need to make likelihood capable of dealing with LL=0 situations (k=0, n=0, p=0).
# also make likelihood group by age (e.g. calculate over 5 year age groups - may help with the zeros).

import glob, sys, os, re, math
#import itemgetter # use to find max N log likelihoods from dict.

def read_calibration_file(infilename):
    infile = open(infilename,"r")
    calibration_data_strings = infile.read().rstrip().splitlines()
    #header = [calibration_data_strings[0].rstrip(",").split(",")]
    calibration_data = []
    for line in calibration_data_strings[1:]:
        split_line = line.rstrip(",").split(",")
        calibration_data += [[int(x) for x in split_line]]
    return calibration_data


def get_calibration_results_dirs(calibration_root_dir):
    possible_calibration_results_dirs = [x[0] for x in os.walk(calibration_root_dir)]
    # Now check that these are of the form "..../RESULTSX":
    checked_dirs = []
    pattern = re.compile("^(RESULTS[1-9]*[0-9]*)")
    for dir in possible_calibration_results_dirs:
        string_to_check = dir.split("/")[-1]
        if pattern.match(string_to_check):
            checked_dirs += [dir]
    checked_dirs.sort()
    return checked_dirs


def decompose(file_name):
    cluster_no = file_name.split("CL")[1].split("_")[0]
    country = file_name.split("_")[3].split("_")[0]
    patchno = file_name.split("_patch")[1].split("_")[0]
    rand = file_name.split("_Rand")[1].split("_")[0]
    if ("PCseed" in file_name):
        pcseed = file_name.split("_PCseed")[1].split("_")[0]
    else:
        pcseed = -1
    randseed = file_name.split("_")[-1].rstrip(".csv")

    return [cluster_no,country,patchno,rand, pcseed,randseed]


    
def check_calibration_files_consistent(dir_list):
    print "in check_calibration_files_consistent dir_list=",dir_list
    checked_files = []
    for i in range(len(dir_list)):
        potential_calibration_files = glob.glob(dir_list[i]+"/Output/Calibration*.csv")
        if potential_calibration_files==[]:
            potential_calibration_files = glob.glob(dir_list[i]+"/Calibration*.csv")
        for j in range(len(potential_calibration_files)):
            # Get the filename:
            f_name = potential_calibration_files[j].split("/")[-1]

            if (i==0 and j==0):
                # Check that the first filename is consistent with all the other filenames:
                [community,country,patchno,rand,pcseed,randseed] = decompose(f_name)
            else:
                # if there is no "PCseed": 
                if pcseed==-1:
                    pattern = re.compile("Calibration_output_CL"+community+"_"+country+"__patch"+patchno+"_Rand[1-9]+[0-9]*_[0-9]+.csv")

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


    

def test_condition(a,f,n,r,g,denominator):
    if (a in range(40,45) and f.split("/")[-2]=="RESULTS2" and n==2 and r=="R1" and g=="M" and denominator=="Ntot"):
        return 1
    elif (a in range(20,25) and f.split("/")[-2]=="RESULTS2" and n==10 and r=="R2" and g=="F" and denominator=="Npos"):
        return 1
    elif (a in range(65,70) and f.split("/")[-2]=="RESULTS2" and n==39 and r=="R2" and g=="F" and denominator=="Naware"):
        return 1
    else:
        return 0


def convert_sorted_to_dictionary(sorted_list):
    output_dictionary = {}

    # sorted_list is of the form: [(('10_PCseed0_0', 0), -1185011.544119031), (('10_PCseed0_0', 31), -1185180.2019216502)]
    for entry in sorted_list:
        output_dictionary[entry[0]] = entry[1]
    return output_dictionary
        
    
########################################################
###     Functions using IBM calibration files:      ####
########################################################


def get_calibration_filenames_and_check_headers(calibration_root_dir):
    # Ensure that the directory ends in "/":
    calibration_root_dir = add_slash(calibration_root_dir)
    print "Dir=",calibration_root_dir
    # Get all the sub-directories where the Calibration*.csv files are:
    calibration_results_dirs = get_calibration_results_dirs(calibration_root_dir)

    # Find the files in those sub-directories, and check that they are all named the right way e.g. Calibration_output_CL05_Zim_V2.0_patch0_Rand1_PCseed0_0.csv 
    check_calibration_files_consistent(calibration_results_dirs)
    [calibration_files,community] = check_calibration_files_consistent(calibration_results_dirs)

    # Number of files
    nfiles = len(calibration_files)
    print "Number of IBM calibration files to read = ",nfiles
    # Now read in the header from each file:

    header = [[] for i in range(nfiles)]
    for i in range(nfiles):
        f = calibration_files[i]
        thisfile = open(f)
        header[i] = [thisfile.readline().rstrip("\n").rstrip(",").split(",")]

        thisfile.close()
        

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
    return [community,header[0][0],calibration_files,full_header_string]



# For survey data split things like "M25" or "F46" to be gender+age:
def split_survey_datatype(instring):
    m = re.match("^([MF])([0-9]+)",instring)
    gender = m.group(1)
    age = int(m.group(2))
    return [gender,age]
    




# For IBM calibration file:
def unpack_header(header):

    if (not(header[0]=="SampleNumber") or not(header[1]=="RepNumber") or not(header[2]=="RunNumber") or not(header[3]=="RandomSeed")):
        print "error in header for IBM calibration file: first 4 entries should be SampleNumber, RepNumber, RunNumber, RandomSeed. Exiting\n",header
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


##################################################
###  Get best fits from a single file:         ###
##################################################

#def get_cohort_likelihood(survey_data,model_data, age_groupings, N_BESTFITS):
def get_cohort_likelihood_bestfits_fromonerun(model_calibration_filename,  model_header,survey_data, survey_header, N_BESTFITS):
#def structure_ibm_data(model_data_array, header):

    model_data = read_calibration_file(model_calibration_filename)
    nruns = len(model_data)

    filekey = model_calibration_filename.split("_Rand")[1].rstrip(".csv")
    #filekey = model_calibration_filename
#####HERE

    [ibm_datatypes,lookup_table] = unpack_header(model_header)
    model_surveytypes = ibm_datatypes.keys()

    survey_data_surveytypes = survey_data.keys()

    if not(set(survey_data_surveytypes) <= set(model_surveytypes)):
        print "Error:Some survey data surveytypes not included in model surveytypes. Exiting"
        sys.exit(1)

    
    # Store log-likelihoods:
    log_likelihood_by_round = {}
    for n in range(nruns):
        log_likelihood_by_round[(filekey,n)] = 0

    # For each indicator, look up the denominator:
    numerator_denominator = {"Npos":"Ntot", "Naware":"Npos", "NonART":"Naware"}
    possible_numerators = numerator_denominator.keys()

            

    for n in range(nruns):        # Go through the runs in a single Calibration.csv file.                 
        for s in survey_data_surveytypes:     # Look for different types of survey (DHS, CHiPs, cohort).
            rounds = survey_data[s].keys()
            for r in rounds:      # Rounds of the given survey type:
                survey_numerators = list(set(possible_numerators).intersection(set(survey_data[s][r].keys())))

                for t in survey_numerators:   # Outcomes (prevalence, 90-90-90 etc collected in the survey).
                    denominator = numerator_denominator[t]

                    genders = survey_data[s][r][t].keys()
                    for g in genders:
                        minage = max(min(survey_data[s][r][t][g]),15)
                        if not(minage%5==0):
                            minage = minage + (5-minage%5)
                        maxage = max(survey_data[s][r][t][g])-5
                        if not(maxage%5==0):
                            maxage = maxage - maxage%5
                        ages = range(minage,maxage,5)
                        #    if not(set(survey_rounds) <= set(model_data_rounds)):
                        #        print "Error: IBM model data does not have the same rounds as the survey data"
                        #    if not(set(numerators) <= set(model_data_datatypes)):
                        #        print "Error: IBM model data contains indicators not given in get_cohort_likelihood(). Need to extend numerator_denominator"
                            
                        model_k = 0
                        model_N = 0
                        survey_k = 0
                        survey_N = 0
                        for age_gp_start in ages:

                            dataname_numerator_start = s+r.replace("R","Round")+t+g+str(age_gp_start)
                            dataname_denominator_start = s+r.replace("R","Round")+denominator+g+str(age_gp_start)
                            i_numerator_start = lookup_table[dataname_numerator_start]
                            i_denominator_start = lookup_table[dataname_denominator_start]
                            for a in range(5):
                                #print filekey,n,i_numerator_start+a,a,age_gp_start
                                model_k += model_data[n][i_numerator_start+a]
                                model_N += model_data[n][i_denominator_start+a]

                                survey_k += survey_data[s][r][t][g][a+age_gp_start]
                                survey_N += survey_data[s][r][denominator][g][a+age_gp_start]
                            log_likelihood_by_round[(filekey,n)] += calculate_log_likelihood(survey_k,survey_N,model_k,model_N)



                                

    res = sorted( log_likelihood_by_round.items(), key=lambda pair: pair[1], reverse=True )[:N_BESTFITS]
    best_fits_likelihoods = convert_sorted_to_dictionary(res)
    print best_fits_likelihoods
    
    best_fits_data = {}
    for data_key in best_fits_likelihoods.keys():
        n = data_key[1]
        best_fits_data[data_key] = ",".join([str(x) for x in model_data[n]])
    return [best_fits_likelihoods,best_fits_data]
        

# Given k observed 'heads' out of N trials, calculate the associated log-likelihood (log to base e):
def calculate_log_likelihood(survey_k, survey_N, model_k, model_N):

    # Make a table of factorials here:
    log_factorials = []
    # Ramunajan's approximation is good to 10^-10 when N=50, so cap the exact calculation at 100:
    for i in range(101):
        log_factorials += [math.log(math.factorial(i))]
        
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


    try:
        log_likelihood = log_factorials[survey_k] + survey_k*math.log(model_p)+(survey_N-survey_k)*math.log(1-model_p)-log_factorials[survey_N] - log_factorials[survey_N-survey_k]
        #log_likelihood = math.log(math.factorial(survey_k)) + survey_k*math.log(model_p)+(survey_N-survey_k)*math.log(1-model_p)-math.log(math.factorial(survey_N)) - math.log(math.factorial(survey_N-survey_k))
    except:
        #print "XXX",model_k,model_N,model_p,survey_k,survey_N
        #print Ramunajan_approximation(survey_k)
        #print survey_k*math.log(model_p)
        #print (survey_N-survey_k)*math.log(1-model_p)
        #print Ramunajan_approximation(survey_N)
        #print Ramunajan_approximation(survey_N-survey_k)
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

#from guppy import hpy

#h = hpy() 

calibration_root_dir = "/home/mike/MANICALAND/manicaland-dev/IBM_simul/results_2021_05_09/"
#calibration_root_dir = "/home/mike/MANICALAND/manicaland-dev/IBM_simul/results2/"

[community, ibm_data_header, all_model_calibration_filenames, full_header_string] = get_calibration_filenames_and_check_headers(calibration_root_dir)

#[community, ibm_data_header, model_data_array,full_header_string] = read_ibm_calibration_files(calibration_root_dir)
print "Finished reading in IBM calibration files. Community=",community


#chips_survey_data_dir = "/home/mike/Dropbox (SPH Imperial College)/PoPART/Data:Stats/CHiPs data/"
survey_data = {}
rounds = [6]
# For each type of data (cohort, DHS, CHiPS) etc we call read_survey_files:
[survey_data_header,survey_data["Cohort"]] = read_survey_files(rounds)

N_BEST_RUNS_TO_GET = 10

# We get the N_BEST_RUNS_TO_GET best fits from each file, then put all of those fits together and choose the N_BEST_RUNS_TO_GET best ones.
# Approach is scalable memory-wise provided that N_BEST_RUNS_TO_GET is not close to 1000.

all_best_N_runs = {}
all_best_N_runs_data = {}
for f in all_model_calibration_filenames:
    [this_run_bestfits_likelihood,this_run_bestfits_data] = get_cohort_likelihood_bestfits_fromonerun(f,  ibm_data_header,survey_data, survey_data_header, N_BEST_RUNS_TO_GET)
    #print "Finished for ",f
    print this_run_bestfits_likelihood

    all_best_N_runs.update(this_run_bestfits_likelihood)
    all_best_N_runs_data.update(this_run_bestfits_data)
#print "All runs=",all_best_N_runs
#print "Finiahed calculating likelihoods"

for run in all_best_N_runs.keys():
    print "run=",run,"likelihood=",all_best_N_runs[run]

overall_best_runs_list = sorted(all_best_N_runs.items(), key=lambda pair: pair[1], reverse=True )[:N_BEST_RUNS_TO_GET]
overall_best_runs = convert_sorted_to_dictionary(overall_best_runs_list)
print overall_best_runs

best_model_calibration_filename = calibration_root_dir+"Calibration_data_bestfits.csv"
best_model_likelihood_filename = calibration_root_dir+"goodfits.txt"

best_model_calibration_file = open(best_model_calibration_filename,"w")
best_model_likelihood_file = open(best_model_likelihood_filename,"w")

best_model_calibration_data = full_header_string+"\n"
best_model_likelihood_output = ""

# Create file listing the files, lines and likelihoods of the best files:
for run in overall_best_runs.keys():
    run_filename = run[0]
    run_line = str(run[1])
    likelihood = str(overall_best_runs[run])
    best_model_likelihood_output += run_filename+" "+run_line+" "+likelihood+"\n"

    #best_model_calibration_data += ",".join([str(x) for x in model_data_array[i[0][0]][i[0][1]]])+"\n"
    best_model_calibration_data += all_best_N_runs_data[run]+"\n"

best_model_calibration_file.write(best_model_calibration_data)
best_model_likelihood_file.write(best_model_likelihood_output)

best_model_calibration_file.close()
best_model_likelihood_file.close()


#print h.heap()

# Call R to plot stuff:
#os.system("Rscript plot_by_age_gender.R")
