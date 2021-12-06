import sys, os, glob, re


#mihpsafiledir = "params/Output/"
mihpsafiledir = "."
#Combined 15-49	18.1	0.33	15.2	0.5	13.4	0.332	11.5
#Male	15-49	14.5	0.46	12.3	0.4154	10.7	0.412	8.6
#Female	15-49	21.1	0.35	17.7	0.4463	15.9	0.385	14.8

survey_prevM = [14.5,12.3,10.7,8.6]
survey_prevF = [21.1,17.7,15.9,14.8]

se_M = [0.46,0.4154,0.412,0.5]
se_F = [0.35,0.4463,0.385,0.5]

t_survey = [2005,2010,2015,2020]

TARGET_WIDTH = 4

def get_MIHPSA_indices(mihpsa_filename):
    mihpsa_file = open(mihpsa_filename,"r")
    header = mihpsa_file.readlines()[0].rstrip().split(",")
    mihpsa_file.close()

    i_NpopM15_49 = header.index('NPop_15to49_male')
    i_NpopF15_49 = header.index('NPop_15to49_female')
    i_PosM15_49 =  header.index('NPos_15to49_male')
    i_PosF15_49 =  header.index('NPos_15to49_female')

    return [i_NpopM15_49,i_NpopF15_49,i_PosM15_49,i_PosF15_49]



# Opens a file and returns the output (excluding the first line, which is assumed to be a header) as a list, where each element is a line of the file.
def read_data(filename):
    infile = open(filename, "r")
    data_raw = infile.read().rstrip().splitlines()
    infile.close()
    
    # First line is a header:
    return data_raw[1:]


def check_target_fit(prevalence_M,prevalence_F,TARGET_WIDTH):
    

    #survey_prevM = [14.5,12.3,10.7,8.6]
    #survey_prevF = [21.1,17.7,15.9,14.8]

    #se_M = [0.46,0.4154,0.412,0.5]
    #se_F = [0.35,0.4463,0.385,0.5]
    max_distance_from_target = 0
    for (i,year) in enumerate(t_survey):
        distance_from_target_M = abs(100*prevalence_M[year] - survey_prevM[i])/(1.96*se_M[i])
        distance_from_target_F = abs(100*prevalence_F[year] - survey_prevF[i])/(1.96*se_F[i])
        max_distance_from_target = max(max_distance_from_target,distance_from_target_M,distance_from_target_F)

    return max_distance_from_target

# For a given fit, make the string corresponding to it:
def make_summary_fit(f, dist):
    run_tag = f.split("_Run")[1].replace("_0.csv","")
    dir_tag = f.split("_Rand")[1].split("_")[0]
    return dir_tag + "_0 "+run_tag+" "+str(dist)

def get_results_dirs(root_dir):
    possible_results_dirs = [x[0] for x in os.walk(root_dir)]

    # Now check that these are of the form "..../RESULTSX":
    checked_dirs = []
    pattern = re.compile("^(RESULTS[1-9]*[0-9]*)")
    for dir in possible_results_dirs:
        string_to_check = dir.split("/")[-1]
        if pattern.match(string_to_check):
            checked_dirs += [dir]
    checked_dirs.sort()
    return checked_dirs


def target_fit_dir(mihpsarootdir):

    outstring = ""
    
    mihpsa_resultsdirs = get_results_dirs(mihpsarootdir)
    
    for mihpsafiledir in mihpsa_resultsdirs:
        mihpsafiles = glob.glob(mihpsafiledir + "/Output/MIHPSA_output_CL*.csv")
        [i_NpopM15_49,i_NpopF15_49,i_PosM15_49,i_PosF15_49] = get_MIHPSA_indices(mihpsafiles[0])

    

    
        # Process each of the MIHPSA output files:
        for n,f in enumerate(mihpsafiles):

            outputs_prevalence_M15_49 = {}
            outputs_prevalence_F15_49 = {}

            # Read the data from a single file (header is not used)
            run_data = read_data(f)
        

            for i,line in enumerate(run_data):

                [year,NpopM15_49,NpopF15_49,PosM15_49,PosF15_49] = [int(line.split(",")[index]) for index in [0,i_NpopM15_49,i_NpopF15_49,i_PosM15_49,i_PosF15_49]]
                if(year in t_survey):
            
                    outputs_prevalence_M15_49[year] = PosM15_49/(1.0*NpopM15_49)
                    outputs_prevalence_F15_49[year] = PosF15_49/(1.0*NpopF15_49)




                
            d = check_target_fit(outputs_prevalence_M15_49,outputs_prevalence_F15_49,TARGET_WIDTH)
            if (d<2):
                outstring += make_summary_fit(f,d)+"\n"

    return outstring
                        

                        

    

resultsdir = "RESULTS/"
fit_data = target_fit_dir(resultsdir)
outfile = open("targetfits_MIHPSA.txt","w")
outfile.write(fit_data)
outfile.close()
