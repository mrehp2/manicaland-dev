# Given a bunch of files of the form MIHPSA_output_CL05_Zim_patch0_Rand1_RunX_0.csv, make a single calibration file for the MIHPSA project.


import glob, sys, os, math

# HIV prevalence in 2005, 2010-11 and 2015-16 - this is DHS data

#Combined	15-49	18.1	0.33	15.2	0.5	13.4	0.332	11.5
#Male	15-49	14.5	0.46	12.3	0.4154	10.7	0.412	8.6
#Female	15-49	21.1	0.35	17.7	0.4463	15.9	0.385	14.8

# 2005 DHS Data collection took place over a seven-month period, from August 2005 to February 2006 (report p7). So take it to be 15 November 2005. (31+28+31+30+31+30+31+31+30+31+15)/365.0=0.873972602739726 ~ 0.874.
# 2010 DHS survey p7: "Data collection took place over a six-month period, from 29 September 2010 through late March 2011." - so pretty much 1 Jan 2011.
# 2015 DHS p5: "Data collection took place over a 6-month period from July 6 to December 20, 2015." - so 167 days. (31+28+31+30+31+30+6+(167/2.0))/365.0 = 0.7410958904109589 ~ 0.741.
t_DHS_r1 = 2005.874
t_DHS_r2 = 2011.0
t_DHS_r3 = 2015.741

t_DHS = [t_DHS_r1,t_DHS_r2,t_DHS_r3]

survey_k_m = [848,769,785]
survey_N_m = [5848,6250,7475]
survey_k_f = [1466,1294,1447]
survey_N_f = [6947,7313,8667]

survey_k_art = [565675,665199,787980,879271,975667,1119909,1150079,1146532,1184901]

survey_N_art = [1000*x for x in [13350.378,13586.71,13814.642,14030.338,14236.599,14438.812,14645.473,14862.927,15092.56406]]   # See C:\Users\mpickles\Dropbox (SPH Imperial College)\projects\MIHPSA_Zimabwe2021\Zimbabwe_WPP_pop_for_ART.xlsx. Based on WPP 2019, with extrapolation for 2021. Note that WPP is in thousands (so multiply by 1000).

year_ART = range(2013,2022) # Specified in MIHPSA file sent by Valentina. Note "All ART totals are reported at the end of each year." - so take 2013.0 etc.

def interpolate(data_year1,data_year2,t):
    year = int(t)
    f = t - year

    interpolated_data = []
    
    for i in range(len(data_year1)):
        interpolated_data += [(1-f)*data_year1[i] + f*data_year2[i]]
    return interpolated_data


# Opens a file and returns the output (excluding the first line, which is assumed to be a header) as a list, where each element is a line of the file.
def read_data(filename):
    infile = open(filename, "r")
    data_raw = infile.read().rstrip().splitlines()
    infile.close()
    
    # First line is a header:
    return data_raw[1:]



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



def read_MIHPSA_header(mihpsa_filename):
    mihpsa_file = open(mihpsa_filename,"r")
    header = mihpsa_file.readlines()[0].rstrip().split(",")
    mihpsa_file.close()

    i_NpopM = header.index('NPop_15to49_male')
    i_NpopF = header.index('NPop_15to49_female')

    i_PosM =  header.index('NPos_15to49_male')
    i_PosF =  header.index('NPos_15to49_female')

    i_artM = header.index('NonART_15plus_male')
    i_artF = header.index('NonART_15plus_female')

    i_NpopM15plus = header.index('Npop_15plus_male')
    i_NpopF15plus = header.index('Npop_15plus_female')
    i_Npop_child = header.index('Npop_children_under15')
    
    i_art_child = header.index('Naware_children_under15')
    
    
    return [i_NpopM,i_NpopF,i_PosM,i_PosF,i_artM,i_artF,i_art_child,i_NpopM15plus,i_NpopF15plus,i_Npop_child]


def make_output_header(year_prev,ART_times):

    header = "Filename,"
    
    for year in range(1990,2030):

        if(year in year_prev):
            header += "Prev_m"+str(year) + "," + "Prev_f"+str(year)+ ","
                
        # Now ART:
        if(year in ART_times):
            header += "Model_Nart" + str(year-1)+ "-" + str(year)+"," + "Model_Ntotal"+ str(year-1)+ "-" + str(year)+ ","
                
    header += "Log_likelihood\n"
    return header

    

def read_mihpsa_files_and_calibrate(mihpsafiledir,t_prev,ART_times,calibration_output_filename):

    year_prev = [int(y) for y in t_prev]
    mihpsafiles = glob.glob(mihpsafiledir + "/MIHPSA_output_CL*.csv")


    [i_NpopM,i_NpopF,i_PosM,i_PosF,i_artM,i_artF,i_art_child,i_NpopM15plus,i_NpopF15plus,i_Npop_child] = read_MIHPSA_header(mihpsafiles[0])

    prevalence_M_by_year = []
    prevalence_F_by_year = []


    # Store log-likelihoods (use dictionary comprehension):
    log_likelihood = {el:0 for el in mihpsafiles}

    outstring = make_output_header(year_prev,ART_times)
    
    # Process each of the MIHPSA files
    for f in mihpsafiles:

        outstring += f+","
        # Read the data from a single file (header is not used)
        mihpsa_run_data = read_data(f)
        for i, line in enumerate(mihpsa_run_data):
            year_data = line.split(",")
            year = int(year_data[0])

            if(year in year_prev):
                next_year_data = mihpsa_run_data[i+1].split(",")
                i_survey = year_prev.index(year)
                t = t_prev[i_survey]

                
                data_y1 = [float(year_data[i_NpopM]),float(year_data[i_PosM]),
                float(year_data[i_NpopF]),float(year_data[i_PosF]),
                int(year_data[i_PosM])/float(year_data[i_NpopM]),
                int(year_data[i_PosF])/float(year_data[i_NpopF])]

                data_y2 = [float(next_year_data[i_NpopM]),float(next_year_data[i_PosM]),
                float(next_year_data[i_NpopF]),float(next_year_data[i_PosF]),
                int(next_year_data[i_PosM])/float(next_year_data[i_NpopM]),
                int(next_year_data[i_PosF])/float(next_year_data[i_NpopF])]

                
                [model_N_m, model_k_m, model_N_f, model_k_f, prev_m, prev_f] = interpolate(data_y1,data_y2,t)


                log_likelihood[f] += calculate_log_likelihood(survey_k_m[i_survey],survey_N_m[i_survey],model_k_m,model_N_m) + calculate_log_likelihood(survey_k_f[i_survey],survey_N_f[i_survey],model_k_f,model_N_f)

                outstring += str(prev_m) + "," + str(prev_f)+ ","
                
                #outstring += str(model_N_m) + "," + str(model_k_m) + "," + str(model_N_f) + "," + str(model_k_f) + "," + str(prev_m) + "," + str(prev_f)+ ","



            # Now ART:
            if(year in ART_times):
                i_survey_art = ART_times.index(year)

                model_Nart = int(year_data[i_artM]) + int(year_data[i_artF]) + int(year_data[i_art_child])
                model_Ntotal = int(year_data[i_NpopM15plus]) + int(year_data[i_NpopF15plus]) + int(year_data[i_Npop_child])

                #print survey_k_art[i_survey_art],survey_N_art[i_survey_art],model_Nart,model_Ntotal,survey_k_art[i_survey_art]/survey_N_art[i_survey_art],float(model_Nart)/model_Ntotal
                
                log_likelihood[f] += calculate_log_likelihood(survey_k_art[i_survey_art],survey_N_art[i_survey_art],model_Nart,model_Ntotal)
                
                outstring += str(model_Nart) + "," + str(model_Ntotal)+ ","
                
        outstring += str(log_likelihood[f])+"\n"


    outfile = open(mihpsafiledir + "/" + calibration_output_filename,"w")
    outfile.write(outstring)
    outfile.close()
#log_likelihood[(filekey,n)] += calculate_log_likelihood(survey_k,survey_N,model_k,model_N)


    
##################################
# Main code:
##################################

mihpsafiledir = sys.argv[1]



# This function looks in mihpsafiledir for all the MIHPSA_Output*.csv files and calculates the likelihood for each (using DHS and ART).
# Saves these as 
read_mihpsa_files_and_calibrate(mihpsafiledir,t_DHS,year_ART,"Calibration_MIHPSA.csv")

