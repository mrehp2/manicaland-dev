#

import glob, sys, os, math
import numpy

USE_STDEV = 0 # Print mean +/- 1.645*s.d. or not in make_mean_CI()


survey_N_art = [1000*x for x in [7712.514,7822.167,7936.191,8044.421,8172.255,8316.685,8471.238,8633.707,8773.997323]]   # Aged 15+. See C:\Users\mpickles\Dropbox (SPH Imperial College)\projects\MIHPSA_Zimabwe2021\Zimbabwe_WPP_pop_for_ART.xlsx. Based on WPP 2019, with extrapolation for 2021. Note that WPP is in thousands (so multiply by 1000).
year_ART = range(2013,2022) # Specified in MIHPSA file sent by Valentina. Note "All ART totals are reported at the end of each year." - so take 2013.0 etc.

survey_N_art_children = [1000*x for x in [5637.864,5764.543,5878.451,5985.917,6064.344,6122.127,6174.235,6229.22,6318.618]]

# Need to scale the IBM population to the total population of Zimbabwe. Right now we use the 2021 index:
MIHPSA_population_scale_adult_year = 2021
MIHPSA_population_scale_adult = survey_N_art[year_ART.index(MIHPSA_population_scale_adult_year)]
MIHPSA_population_scale_child = survey_N_art_children[year_ART.index(MIHPSA_population_scale_adult_year)]



# Population of men 15-49 (WPP 2019 - see Zimbabwe_WPP_pop_for_ART.xlsx).
N_VMMC = [2918543,2945782,2975741,3003943,3034779,3067700,3102525,3139667,3176370,3221509,3273850,3330609]
year_VMMC = range(2008,2020)
MIHPSA_population_scale_for_VMMC_year = 2019
# Scale for men only:
MIHPSA_population_scale_for_VMMC = N_VMMC[year_VMMC.index(MIHPSA_population_scale_for_VMMC_year)]




# Opens a file and returns the output (excluding the first line, which is assumed to be a header) as a list, where each element is a line of the file.
def read_data(filename):
    infile = open(filename, "r")
    data_raw = infile.read().rstrip().splitlines()
    infile.close()
    
    # First line is a header:
    return data_raw[1:]





def read_MIHPSA_header(mihpsa_filename):
    mihpsa_file = open(mihpsa_filename,"r")
    header = mihpsa_file.readlines()[0].rstrip().split(",")
    mihpsa_file.close()

    i_NpopM15_49 = header.index('NPop_15to49_male')
    i_NpopF15_49 = header.index('NPop_15to49_female')

    i_NpopM15_24 = header.index('NPop_15to24_male')
    i_NpopM25_49 = header.index('NPop_25to49_male')
    i_NpopF15_24 = header.index('NPop_15to24_female')
    i_NpopF25_49 = header.index('NPop_25to49_female')

    i_PosM15_49 =  header.index('NPos_15to49_male')
    i_PosF15_49 =  header.index('NPos_15to49_female')

    i_PosM15_24 = header.index('NPos_15to24_male')
    i_PosM25_49 = header.index('NPos_25to49_male')
    i_PosF15_24 = header.index('NPos_15to24_female')
    i_PosF25_49 = header.index('NPos_25to49_female')

    i_artM15plus = header.index('NonART_15plus_male')
    i_artF15plus = header.index('NonART_15plus_female')

    i_NpopM15plus = header.index('Npop_15plus_male')
    i_NpopF15plus = header.index('Npop_15plus_female')
    i_Npop_child = header.index('Npop_children_under15')
    
    i_art_child = header.index('Naware_children_under15')

    i_NposM15plus = header.index('Npos_15plus_male')
    i_NposF15plus = header.index('Npos_15plus_female')
    i_Npos_child = header.index('Npos_children_under15')
    i_NawareM15plus = header.index('Naware_15plus_male')
    i_NawareF15plus = header.index('Naware_15plus_female')
    i_NonARTM15plus = header.index('NonART_15plus_male')
    i_NonARTF15plus = header.index('NonART_15plus_female')
    i_N_VSM15plus = header.index('N_VS_15plus_male')
    i_N_VSF15plus = header.index('N_VS_15plus_female')
    
    i_N_women_sexuallyactive_15to24 = header.index('N_women_sexuallyactive_15to24')
    i_N_women_usecondomlastact_15to24 = header.index('N_women_usecondomlastact_15to24')


    i_N_deaths_20_59_male = header.index('N_deaths_20_59_male')
    i_N_deaths_20_59_female = header.index('N_deaths_20_59_female')
    i_N_AIDSdeaths_15plus_male = header.index('N_AIDSdeaths_15plus_male')
    i_N_AIDSdeaths_15plus_female = header.index('N_AIDSdeaths_15plus_female')
    i_N_AIDSdeaths_children_under15 = header.index('N_AIDSdeaths_children_under15')
    i_N_HIVtests_15plus_male = header.index('N_HIVtests_15plus_male')
    i_N_HIVtests_15plus_female = header.index('N_HIVtests_15plus_female')
    i_N_newHIVinfections_15to24_male = header.index('N_newHIVinfections_15to24_male')
    i_N_newHIVinfections_25to49_male = header.index('N_newHIVinfections_25to49_male')
    i_N_newHIVinfections_15to24_female = header.index('N_newHIVinfections_15to24_female')
    i_N_newHIVinfections_25to49_female = header.index('N_newHIVinfections_25to49_female')
    i_N_newHIVdiagnoses_15plus = header.index('N_newHIVdiagnoses_15plus')

    
    i_circ = header.index('Ncirc_15to49') # This is (cumulative) men circumcised either VMMC or TMC aged 15-49.

    
    return [i_NpopM15_49,i_NpopF15_49,i_NpopM15_24,i_NpopF15_24,i_NpopM25_49,i_NpopF25_49,i_PosM15_49,i_PosF15_49,i_PosM15_24,i_PosF15_24,i_PosM25_49,i_PosF25_49,i_artM15plus,i_artF15plus,i_art_child,i_NpopM15plus,i_NpopF15plus,i_Npop_child,i_circ,i_NposM15plus,i_NposF15plus,i_Npos_child,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_women_sexuallyactive_15to24,i_N_women_usecondomlastact_15to24,i_N_deaths_20_59_male,i_N_deaths_20_59_female,i_N_AIDSdeaths_15plus_male,i_N_AIDSdeaths_15plus_female,i_N_AIDSdeaths_children_under15,i_N_HIVtests_15plus_male,i_N_HIVtests_15plus_female,i_N_newHIVinfections_15to24_male,i_N_newHIVinfections_25to49_male,i_N_newHIVinfections_15to24_female,i_N_newHIVinfections_25to49_female,i_N_newHIVdiagnoses_15plus]

    


# For each run we need to generate the 
def get_pop_scale(mihpsa_model_data,i_NpopM15_49,i_NpopM15plus,i_NpopF15plus,i_Npop_child):

    for line in mihpsa_model_data:
        year = int(line.split(",")[0])
        if(year==MIHPSA_population_scale_adult_year):
            line_data = line.split(",")
            
            pop_tot_adult = int(line_data[i_NpopM15plus]) + int(line_data[i_NpopF15plus])
            pop_child = int(line_data[i_Npop_child])
            scale_tot_adult = MIHPSA_population_scale_adult / (1.0*pop_tot_adult)
            scale_child = MIHPSA_population_scale_child / (1.0*pop_child)

            # Entire population:L
            scale_pop = (MIHPSA_population_scale_adult+MIHPSA_population_scale_child) / (1.0*(pop_tot_adult+pop_child))
            
        elif(year==MIHPSA_population_scale_for_VMMC_year):
            line_data = line.split(",")
            
            pop_M_VMMC = int(line_data[i_NpopM15_49])

            scale_VMMC = MIHPSA_population_scale_for_VMMC / (1.0*pop_M_VMMC)

        if(year>=max(MIHPSA_population_scale_adult_year,MIHPSA_population_scale_for_VMMC_year)):
            print "Scales: ",scale_VMMC,scale_tot_adult,scale_child,scale_pop
            break

    #return [scale_pop, scale_pop, scale_pop, scale_pop]
    return [scale_VMMC, scale_tot_adult, scale_child, scale_pop]


def write_output(outputs,outfile):
    outstring = ""
    years_saved = outputs.keys()
    years_saved.sort()
    for year in years_saved:
        outstring += str(year)+","
        for run_output in outputs[year]:
            outstring += str(run_output)+","
        outstring = outstring.rstrip(",") +"\n"
        

    #print outstring
    outfile = open(outfile,"w")
    outfile.write(outstring)
    outfile.close()

def get_annual_from_cumulative(outputs_cumulative):
    years = outputs_cumulative.keys()
    years.sort()
    outputs = {}
    #outputs[years[0]] = outputs_cumulative[years[0]][:]
    #outputs[years[0]] = [0]*len(outputs_cumulative[years[0]])
    for y in range(len(years)-1):
        # The cumulative outputs start at 1990.5.
        # We want the first annual output to be for 1990.5-1991.5.
        outputs[years[y]] = [outputs_cumulative[years[y+1]][i] - outputs_cumulative[years[y]][i] for i in range(len(outputs_cumulative[years[y]]))]

    return outputs

def sum_two_outputs(output1,output2):
    years = output1.keys()
    years.sort()
    outputs_summed = {}
    #outputs_summed[years[0]] = [0]*len(output1[years[0]])
    for y in range(len(years)):
        outputs_summed[years[y]] = [output1[years[y]][i]+output2[years[y]][i] for i in range(len(output1[years[y]]))]

    return outputs_summed



def sum_three_outputs(output1,output2,output3):
    years = output1.keys()
    years.sort()
    outputs_summed = {}
    #outputs_summed[years[0]] = [0]*len(output1[years[0]])
    for y in range(len(years)):
        outputs_summed[years[y]] = [output1[years[y]][i]+output2[years[y]][i]+output3[years[y]][i] for i in range(len(output1[years[y]]))]

    return outputs_summed
    

def calculate_incidence(N_newinfections,Npop,Npos):
    years = N_newinfections.keys()
    years.sort()
    incidence = {}
    #incidence[years[0]] = [0]*len(N_newinfections[years[0]])
    for y in range(len(years)):
        #print y, len(N_newinfections[years[y]]),len(Npop),len(Npos)
        incidence[years[y]] = [N_newinfections[years[y]][i] / (Npop[years[y]][i] - Npos[years[y]][i]) for i in range(len(N_newinfections[years[y]]))]
    return incidence

def get_quotient(output1,output2,ERR):
    years = output1.keys()
    years.sort()
    outputs_quotient = {}
    outputs_quotient[years[0]] = [0]*len(output1[years[0]])
    for y in range(1,len(years)):
        outputs_quotient[years[y]] = [output1[years[y]][i]/(1.0*output2[years[y]][i]+ERR) for i in range(len(output1[years[y]]))]

    return outputs_quotient


def generate_output_from_one_var(output):
    outstr = ""
    for y in range(1990,2041):
        outstr += str(y)+" "+" ".join([str(x) for x in output[y]])+"\n"
    return outstr


def make_mean_CI(outputs_dict,output_names):

    output_string = "Outcome Measure "+" ".join([str(x) for x in range(1990,2041)])+"\n"
    for outputname in output_names:
        mean_output = []
        median_output = []
        ll_output = []
        ul_output = []
        ll_stdev = []
        ul_stdev = []
        for y in range(1990,2041):
            mean_output += [numpy.mean(outputs_dict[outputname][y])]
            median_output += [numpy.median(outputs_dict[outputname][y])]
            ll_output += [numpy.percentile(outputs_dict[outputname][y],5)]
            ul_output += [numpy.percentile(outputs_dict[outputname][y],95)]
            ll_stdev += [numpy.mean(outputs_dict[outputname][y]) - 1.645* numpy.std(outputs_dict[outputname][y])]
            ul_stdev += [numpy.mean(outputs_dict[outputname][y]) + 1.645* numpy.std(outputs_dict[outputname][y])]

        

        output_string += outputname + " "
        output_string += "Median " + " ".join([str(x) for x in median_output]) +  "\n"
        #output_string += "Mean " + " ".join([str(x) for x in mean_output]) +  "\n"
        output_string += " LL "+" ".join([str(x) for x in ll_output]) +  "\n"
        output_string += " UL "+" ".join([str(x) for x in ul_output]) +  "\n"
        if(USE_STDEV==1):
            output_string += " STD_LL "+" ".join([str(x) for x in ll_stdev]) +  "\n"
            output_string += " STD_UL "+" ".join([str(x) for x in ul_stdev]) +  "\n"
        #output_string += "\n"

    outfile = open("MIHPSA_project_outputs_stage1.csv","w")
    outfile.write(output_string)
    outfile.close()

        

def read_mihpsa_files_and_make_summary_file(mihpsafiledir):

    ERR=1e-12
    
    mihpsafiles = glob.glob(mihpsafiledir + "/MIHPSA_output_CL*.csv")
    print mihpsafiles

    #[i_NpopM15_49,i_NpopF15_49,i_PosM15_49,i_PosF15_49,i_artM15plus,i_artF15plus,i_art_child,i_NpopM15plus,i_NpopF15plus,i_Npop_child,i_circ,i_NposM15plus,i_NposF15plus,i_Npos_child,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_women_sexuallyactive_15to24,i_N_women_usecondomlastact_15to24,i_N_deaths_20_59_male,i_N_deaths_20_59_female,i_N_AIDSdeaths_15plus_male,i_N_AIDSdeaths_15plus_female,i_N_AIDSdeaths_children_under15,i_N_HIVtests_15plus_male,i_N_HIVtests_15plus_female,i_N_newHIVinfections_15to49_male,i_N_newHIVinfections_15to49_female,i_N_newHIVdiagnoses_15plus]

    [i_NpopM15_49,i_NpopF15_49,i_NpopM15_24,i_NpopF15_24,i_NpopM25_49,i_NpopF25_49,i_PosM15_49,i_PosF15_49,i_PosM15_24,i_PosF15_24,i_PosM25_49,i_PosF25_49,i_artM15plus,i_artF15plus,i_art_child,i_NpopM15plus,i_NpopF15plus,i_Npop_child,i_circ,i_NposM15plus,i_NposF15plus,i_Npos_child,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_women_sexuallyactive_15to24,i_N_women_usecondomlastact_15to24,i_N_deaths_20_59_male,i_N_deaths_20_59_female,i_N_AIDSdeaths_15plus_male,i_N_AIDSdeaths_15plus_female,i_N_AIDSdeaths_children_under15,i_N_HIVtests_15plus_male,i_N_HIVtests_15plus_female,i_N_newHIVinfections_15to24_male,i_N_newHIVinfections_25to49_male,i_N_newHIVinfections_15to24_female,i_N_newHIVinfections_25to49_female,i_N_newHIVdiagnoses_15plus] = read_MIHPSA_header(mihpsafiles[0])

    
    #prevalence_M_by_year = []
    #prevalence_F_by_year = []
    outputs_prevalence_M15_49 = {}
    outputs_prevalence_M15_24 = {}
    outputs_prevalence_M25_49 = {}
    outputs_prevalence_F15_49 = {}
    outputs_prevalence_F15_24 = {}
    outputs_prevalence_F25_49 = {}
    outputs_prevalence_overall15_49 = {}
    outputs_prevalence_child = {}
    
    outputs_Npop_M15_49 = {}
    outputs_Npop_F15_49 = {}

    outputs_Npop_M15_24 = {}
    outputs_Npop_M25_49 = {}

    outputs_Npop_F15_24 = {}
    outputs_Npop_F25_49 = {}

    outputs_Npop15_49 = {}

    outputs_Npop_15plus = {}
    outputs_Npop_M15plus = {}
    outputs_Npop_F15plus = {}
    outputs_Npop_child = {}
    outputs_Npop_total = {}

    outputs_Npos_M15_49 = {}
    outputs_Npos_F15_49 = {}

    outputs_Npos_M15_24 = {}
    outputs_Npos_M25_49 = {}
    outputs_Npos_F15_24 = {}
    outputs_Npos_F25_49 = {}


    outputs_Npos_M15plus = {}
    outputs_Npos_F15plus = {}
    outputs_Npos_child = {}
    outputs_Npos_total = {}


    outputs_Npos15_49 = {}

    
    outputs_N_ART_M15plus = {}
    outputs_N_ART_F15plus = {}
    outputs_N_ART_child = {}
    outputs_N_ART_total = {}
    # UNAIDS definition of ART coverage: Percentage of people living with HIV currently receiving ART among the estimated number of adults and children living with HIV
    outputs_ARTcoverage_M15plus = {}
    outputs_ARTcoverage_F15plus = {}
    outputs_ARTcoverage_child = {}
    outputs_ARTcoverage_total = {}

    outputs_DiagOnART_M15plus = {}
    outputs_DiagOnART_F15plus = {}
    

    outputs_prop_diagnosed_M15plus = {}
    outputs_prop_diagnosed_F15plus = {}
    outputs_prop_diagnosed_child = {}
    outputs_prop_diagnosed_overall = {}
    #outputs_circ_cumulative15_49 = {} # This is circumicsion. As TMC is rare (and constant over time) the difference in cumulative cirucmcision per year should be roughly VMMC.
    outputs_Ncirc_15_49 = {} # Number of 15-49 year old men who are currently circumcised.

    outputs_propcirc_15_49 = {} # Number of 15-49 year old men who are currently circumcised.
    
    outputs_prop_F15_24_sex_active_usedcondomlasttime = {}

    outputs_prop_VS_adult15plus = {}


    outputs_Ncumulativecases_M15_49 = {}
    outputs_Ncumulativecases_M15_24 = {}
    outputs_Ncumulativecases_M25_49 = {}
    outputs_Ncumulativecases_F15_49 = {}
    outputs_Ncumulativecases_F15_24 = {}
    outputs_Ncumulativecases_F25_49 = {}
    
    outputs_cumulativeAIDSdeaths_M15plus = {}
    outputs_cumulativeAIDSdeaths_F15plus = {}
    outputs_cumulativeAIDSdeaths_child = {}
    outputs_cumulativetotaldeaths_M20_59 = {}
    outputs_cumulativetotaldeaths_F20_59 = {}
    outputs_cumulativeNtests_M15plus = {}
    outputs_cumulativeNtests_F15plus = {}
    outputs_cumulativeNdiagnoses = {}


    
    #outputs_incidence_M15_49 = {}
    #outputs_incidence_F15_49 = {}
    #outputs_incidence_adult15_49 = {}

    #outputs_Nincidentcases_M15_49 = {}
    #outputs_Nincidentcases_F15_49 = {}
    #outputs_Nincidentcases_adult15_49 = {}

    outputs_AIDSdeaths_M15plus = {}
    outputs_AIDSdeaths_F15plus = {}
    outputs_AIDSdeaths_child = {}
    outputs_AIDSdeaths_total = {}

    outputs_totaldeaths_M20_59 = {}
    outputs_totaldeaths_F20_59 = {}
    outputs_totaldeaths_adult20_59 = {}

    outputs_Ntests_M15plus = {}
    outputs_Ntests_F15plus = {}
    outputs_Ntests_adult15plus = {}

    outputs_proportion_tests_pos_15plus = {}
    
    # Process each of the MIHPSA output files:
    for n,f in enumerate(mihpsafiles):

        # Read the data from a single file (header is not used)
        run_data = read_data(f)
        
        [scale_VMMC, scale_tot_adult, scale_child, scale_pop] = get_pop_scale(run_data,i_NpopM15_49,i_NpopM15plus,i_NpopF15plus,i_Npop_child)

        # Force all the scales to be the same (currently that for all individuals, scale_pop):
        scale_VMMC = scale_pop
        scale_tot_adult = scale_pop
        scale_child = scale_pop


        for i,line in enumerate(run_data):

            [year,NpopM15_49,NpopF15_49,NpopM15_24,NpopF15_24,NpopM25_49,NpopF25_49,PosM15_49,PosF15_49,PosM15_24,PosF15_24,PosM25_49,PosF25_49,artM15plus,artF15plus,art_child,NpopM15plus,NpopF15plus,Npop_child,Ncirc_15_49,NposM15plus,NposF15plus,Npos_child,NawareM15plus,NawareF15plus,NonARTM15plus,NonARTF15plus,N_VSM15plus,N_VSF15plus,N_women_sexuallyactive_15to24,N_women_usecondomlastact_15to24,N_deaths_20_59_male,N_deaths_20_59_female,N_AIDSdeaths_15plus_male,N_AIDSdeaths_15plus_female,N_AIDSdeaths_children_under15,N_HIVtests_15plus_male,N_HIVtests_15plus_female,N_newHIVinfections_15to24_male,N_newHIVinfections_25to49_male,N_newHIVinfections_15to24_female,N_newHIVinfections_25to49_female,N_newHIVdiagnoses_15plus] = [int(line.split(",")[index]) for index in [0,i_NpopM15_49,i_NpopF15_49,i_NpopM15_24,i_NpopF15_24,i_NpopM25_49,i_NpopF25_49,i_PosM15_49,i_PosF15_49,i_PosM15_24,i_PosF15_24,i_PosM25_49,i_PosF25_49,i_artM15plus,i_artF15plus,i_art_child,i_NpopM15plus,i_NpopF15plus,i_Npop_child,i_circ,i_NposM15plus,i_NposF15plus,i_Npos_child,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_women_sexuallyactive_15to24,i_N_women_usecondomlastact_15to24,i_N_deaths_20_59_male,i_N_deaths_20_59_female,i_N_AIDSdeaths_15plus_male,i_N_AIDSdeaths_15plus_female,i_N_AIDSdeaths_children_under15,i_N_HIVtests_15plus_male,i_N_HIVtests_15plus_female,i_N_newHIVinfections_15to24_male,i_N_newHIVinfections_25to49_male,i_N_newHIVinfections_15to24_female,i_N_newHIVinfections_25to49_female,i_N_newHIVdiagnoses_15plus]]
            if(n==0):


    # UNAIDS definition of ART coverage: Percentage of people living with HIV currently receiving ART among the estimated number of adults and children living with HIV

                outputs_prevalence_M15_49[year] = [PosM15_49/(1.0*NpopM15_49)]

                outputs_prevalence_M15_24[year] = [PosM15_24/(1.0*NpopM15_24)]
                outputs_prevalence_M25_49[year] = [PosM25_49/(1.0*NpopM25_49)]

                outputs_prevalence_F15_49[year] = [PosF15_49/(1.0*NpopF15_49)]

                outputs_prevalence_F15_24[year] = [PosF15_24/(1.0*NpopF15_24)]
                outputs_prevalence_F25_49[year] = [PosF25_49/(1.0*NpopF25_49)]

                outputs_prevalence_overall15_49[year] = [(PosM15_49+PosF15_49)/(1.0*(NpopM15_49+NpopF15_49))]

                outputs_prevalence_child[year] = [Npos_child/(1.0*Npop_child)]
                
                outputs_N_ART_M15plus[year] = [artM15plus*scale_tot_adult]
                outputs_N_ART_F15plus[year] = [artF15plus*scale_tot_adult]
                outputs_N_ART_child[year] = [art_child*scale_child]
                outputs_N_ART_total[year] = [(artM15plus+artF15plus)*scale_tot_adult + art_child*scale_child]

                outputs_Npop_M15_49[year] = [NpopM15_49*scale_tot_adult]
                outputs_Npop_F15_49[year] = [NpopF15_49*scale_tot_adult]
                outputs_Npop15_49[year] = [(NpopM15_49+NpopF15_49)*scale_tot_adult]

                outputs_Npop_M15_24[year] = [NpopM15_24*scale_tot_adult]
                outputs_Npop_M25_49[year] = [NpopM25_49*scale_tot_adult]
                outputs_Npop_F15_24[year] = [NpopF15_24*scale_tot_adult]
                outputs_Npop_F25_49[year] = [NpopF25_49*scale_tot_adult]


                outputs_Npop_15plus[year] = [(NpopM15plus+NpopF15plus)*scale_tot_adult]
                outputs_Npop_M15plus[year] = [NpopM15plus*scale_tot_adult]
                outputs_Npop_F15plus[year] = [NpopF15plus*scale_tot_adult]

                outputs_Npop_child[year] = [Npop_child*scale_child]

                outputs_Npop_total[year] = [(NpopM15plus+NpopF15plus)*scale_tot_adult + Npop_child*scale_child]
                
                outputs_Npos_M15_49[year] = [PosM15_49*scale_tot_adult]
                outputs_Npos_F15_49[year] = [PosF15_49*scale_tot_adult]
                outputs_Npos15_49[year] = [(PosM15_49+PosF15_49)*scale_tot_adult]

                outputs_Npos_M15_24[year] = [PosM15_24*scale_tot_adult]
                outputs_Npos_M25_49[year] = [PosM25_49*scale_tot_adult]
                outputs_Npos_F15_24[year] = [PosF15_24*scale_tot_adult]
                outputs_Npos_F25_49[year] = [PosF25_49*scale_tot_adult]
                
                outputs_Npos_M15plus[year] = [NposM15plus*scale_tot_adult]
                outputs_Npos_F15plus[year] = [NposF15plus*scale_tot_adult]
                outputs_Npos_child[year] = [Npos_child*scale_child]
                outputs_Npos_total[year] = [(NposM15plus+NposF15plus)*scale_tot_adult + Npos_child*scale_child]
                
                outputs_ARTcoverage_M15plus[year] = [artM15plus/(1.0*NposM15plus+ERR)]

                outputs_ARTcoverage_F15plus[year] = [artF15plus/(1.0*NposF15plus+ERR)]
                
                outputs_ARTcoverage_child[year] = [art_child/(1.0*Npos_child+ERR)]
                outputs_ARTcoverage_total[year] = [(artM15plus+artF15plus+art_child)/(1.0*(NposM15plus+NposF15plus+Npos_child+ERR))]

                outputs_DiagOnART_M15plus[year] = [artM15plus/(1.0*NawareM15plus+ERR)]

                outputs_DiagOnART_F15plus[year] = [artF15plus/(1.0*NawareF15plus+ERR)]
                
                
                #outputs_circ_cumulative15_49[year] = [circ*scale_VMMC] # This is circumicsion. As TMC is rare (and constant over time) the difference in cumulative cirucmcision per year should be roughly VMMC.
                outputs_Ncirc_15_49[year] = [Ncirc_15_49*scale_VMMC]
                outputs_propcirc_15_49[year] = [Ncirc_15_49/(1.0*NpopM15_49)]

                outputs_prop_diagnosed_M15plus[year] = [NawareM15plus/(1.0*NposM15plus+ERR)]

                outputs_prop_diagnosed_F15plus[year] = [NawareF15plus/(1.0*NposF15plus+ERR)]

                #outputs_prop_diagnosed_child = {}
                #outputs_prop_diagnosed_overall = {}
                outputs_prop_F15_24_sex_active_usedcondomlasttime[year] = [N_women_usecondomlastact_15to24/(1.0*N_women_sexuallyactive_15to24)]

                outputs_prop_VS_adult15plus[year] = [(N_VSM15plus+N_VSF15plus)/(1.0*(artM15plus+artF15plus+ERR))]





                ##############################


                outputs_Ncumulativecases_M15_24[year] = [N_newHIVinfections_15to24_male*scale_tot_adult]
                outputs_Ncumulativecases_M25_49[year] = [N_newHIVinfections_25to49_male*scale_tot_adult]

                outputs_Ncumulativecases_F15_24[year] = [N_newHIVinfections_15to24_female*scale_tot_adult]
                outputs_Ncumulativecases_F25_49[year] = [N_newHIVinfections_25to49_female*scale_tot_adult]

                outputs_Ncumulativecases_M15_49[year] = [(N_newHIVinfections_15to24_male+N_newHIVinfections_25to49_male)*scale_tot_adult]
                outputs_Ncumulativecases_F15_49[year] = [(N_newHIVinfections_15to24_female+N_newHIVinfections_25to49_female)*scale_tot_adult]
                
                outputs_cumulativeAIDSdeaths_M15plus[year] = [N_AIDSdeaths_15plus_male*scale_tot_adult]
                outputs_cumulativeAIDSdeaths_F15plus[year] = [N_AIDSdeaths_15plus_female*scale_tot_adult]
                outputs_cumulativeAIDSdeaths_child[year] = [N_AIDSdeaths_children_under15*scale_child]
                outputs_cumulativetotaldeaths_M20_59[year] = [N_deaths_20_59_male*scale_tot_adult]
                outputs_cumulativetotaldeaths_F20_59[year] = [N_deaths_20_59_female*scale_tot_adult]
                outputs_cumulativeNtests_M15plus[year] = [N_HIVtests_15plus_male*scale_tot_adult]
                outputs_cumulativeNtests_F15plus[year] = [N_HIVtests_15plus_female*scale_tot_adult]
                outputs_cumulativeNdiagnoses[year] = [N_newHIVdiagnoses_15plus*scale_tot_adult]



                
            else:
                outputs_Npop_M15_49[year] += [NpopM15_49*scale_tot_adult]
                outputs_Npop_F15_49[year] += [NpopF15_49*scale_tot_adult]
                outputs_Npop_M15_24[year] += [NpopM15_24*scale_tot_adult]
                outputs_Npop_M25_49[year] += [NpopM25_49*scale_tot_adult]
                outputs_Npop_F15_24[year] += [NpopF15_24*scale_tot_adult]
                outputs_Npop_F25_49[year] += [NpopF25_49*scale_tot_adult]

                outputs_Npop15_49[year] += [(NpopM15_49+NpopF15_49)*scale_tot_adult]
                outputs_Npop_15plus[year] += [(NpopM15plus+NpopF15plus)*scale_tot_adult]
                outputs_Npop_M15plus[year] += [NpopM15plus*scale_tot_adult]
                outputs_Npop_F15plus[year] += [NpopF15plus*scale_tot_adult]
                
                outputs_Npop_child[year] += [Npop_child*scale_child]
                outputs_Npop_total[year] += [(NpopM15plus+NpopF15plus)*scale_tot_adult + Npop_child*scale_child]
                
                outputs_Npos_M15_49[year] += [PosM15_49*scale_tot_adult]
                outputs_Npos_F15_49[year] += [PosF15_49*scale_tot_adult]
                outputs_Npos15_49[year] += [(PosM15_49+PosF15_49)*scale_tot_adult]

                outputs_Npos_M15_24[year] += [PosM15_24*scale_tot_adult]
                outputs_Npos_M25_49[year] += [PosM25_49*scale_tot_adult]
                outputs_Npos_F15_24[year] += [PosF15_24*scale_tot_adult]
                outputs_Npos_F25_49[year] += [PosF25_49*scale_tot_adult]
                
                outputs_Npos_M15plus[year] += [NposM15plus*scale_tot_adult]
                outputs_Npos_F15plus[year] += [NposF15plus*scale_tot_adult]
                outputs_Npos_child[year] += [Npos_child*scale_child]
                outputs_Npos_total[year] += [(NposM15plus+NposF15plus)*scale_tot_adult + Npos_child*scale_child]
                
                
                outputs_prevalence_M15_49[year] += [PosM15_49/(1.0*NpopM15_49)]
                outputs_prevalence_M15_24[year] += [PosM15_24/(1.0*NpopM15_24)]
                outputs_prevalence_M25_49[year] += [PosM25_49/(1.0*NpopM25_49)]

                outputs_prevalence_F15_49[year] += [PosF15_49/(1.0*NpopF15_49)]
                outputs_prevalence_F15_24[year] += [PosF15_24/(1.0*NpopF15_24)]
                outputs_prevalence_F25_49[year] += [PosF25_49/(1.0*NpopF25_49)]

                outputs_prevalence_overall15_49[year] += [(PosM15_49+PosF15_49)/(1.0*(NpopM15_49+NpopF15_49))]

                outputs_prevalence_child[year] += [Npos_child/(1.0*Npop_child)]


                
                outputs_N_ART_M15plus[year] += [artM15plus*scale_tot_adult]
                outputs_N_ART_F15plus[year] += [artF15plus*scale_tot_adult]
                outputs_N_ART_child[year] += [art_child*scale_child]
                outputs_N_ART_total[year] += [(artM15plus+artF15plus)*scale_tot_adult + art_child*scale_child]

                outputs_ARTcoverage_M15plus[year] += [artM15plus/(1.0*NposM15plus+ERR)]
                outputs_ARTcoverage_F15plus[year] += [artF15plus/(1.0*NposF15plus+ERR)]
                outputs_ARTcoverage_child[year] += [art_child/(1.0*Npos_child)]
                outputs_ARTcoverage_total[year] += [(artM15plus+artF15plus+art_child)/(1.0*(NposM15plus+NposF15plus+Npos_child))]

                outputs_DiagOnART_M15plus[year] += [artM15plus/(1.0*NawareM15plus+ERR)]

                outputs_DiagOnART_F15plus[year] += [artF15plus/(1.0*NawareF15plus+ERR)]

                
                outputs_Ncirc_15_49[year] += [Ncirc_15_49*scale_VMMC] 
                outputs_propcirc_15_49[year] += [Ncirc_15_49/(1.0*NpopM15_49)]

                outputs_prop_diagnosed_M15plus[year] += [NawareM15plus/(1.0*NposM15plus+ERR)]
                outputs_prop_diagnosed_F15plus[year] += [NawareF15plus/(1.0*NposF15plus+ERR)]

                outputs_prop_F15_24_sex_active_usedcondomlasttime[year] += [N_women_usecondomlastact_15to24/(1.0*N_women_sexuallyactive_15to24)]

                outputs_prop_VS_adult15plus[year] += [(N_VSM15plus+N_VSF15plus)/(1.0*(artM15plus+artF15plus+ERR))]
                
                ### Flow measures:
                ##############################

                outputs_Ncumulativecases_M15_24[year] += [N_newHIVinfections_15to24_male*scale_tot_adult]
                outputs_Ncumulativecases_M25_49[year] += [N_newHIVinfections_25to49_male*scale_tot_adult]
                outputs_Ncumulativecases_M15_49[year] += [(N_newHIVinfections_15to24_male+N_newHIVinfections_25to49_male)*scale_tot_adult]
                
                outputs_Ncumulativecases_F15_24[year] += [N_newHIVinfections_15to24_female*scale_tot_adult]
                outputs_Ncumulativecases_F25_49[year] += [N_newHIVinfections_25to49_female*scale_tot_adult]
                outputs_Ncumulativecases_F15_49[year] += [(N_newHIVinfections_15to24_female+N_newHIVinfections_25to49_female)*scale_tot_adult]
                


                outputs_cumulativeAIDSdeaths_M15plus[year] += [N_AIDSdeaths_15plus_male*scale_tot_adult]
                outputs_cumulativeAIDSdeaths_F15plus[year] += [N_AIDSdeaths_15plus_female*scale_tot_adult]
                outputs_cumulativeAIDSdeaths_child[year] += [N_AIDSdeaths_children_under15*scale_child]
                outputs_cumulativetotaldeaths_M20_59[year] += [N_deaths_20_59_male*scale_tot_adult]
                outputs_cumulativetotaldeaths_F20_59[year] += [N_deaths_20_59_female*scale_tot_adult]
                outputs_cumulativeNtests_M15plus[year] += [N_HIVtests_15plus_male*scale_tot_adult]
                outputs_cumulativeNtests_F15plus[year] += [N_HIVtests_15plus_female*scale_tot_adult]
                outputs_cumulativeNdiagnoses[year] += [N_newHIVdiagnoses_15plus*scale_tot_adult]






    ##################################################################
    # Now make annual outputs from cumulative ones:
    ##################################################################

    outputs_Nincidentcases_M15_49 = get_annual_from_cumulative(outputs_Ncumulativecases_M15_49)
    outputs_Nincidentcases_M15_24 = get_annual_from_cumulative(outputs_Ncumulativecases_M15_24)
    outputs_Nincidentcases_M25_49 = get_annual_from_cumulative(outputs_Ncumulativecases_M25_49)
    outputs_Nincidentcases_F15_49 = get_annual_from_cumulative(outputs_Ncumulativecases_F15_49)
    outputs_Nincidentcases_F15_24 = get_annual_from_cumulative(outputs_Ncumulativecases_F15_24)
    outputs_Nincidentcases_F25_49 = get_annual_from_cumulative(outputs_Ncumulativecases_F25_49)
    
    outputs_Nincidentcases_adult15_49 = sum_two_outputs(outputs_Nincidentcases_M15_49,outputs_Nincidentcases_F15_49)

    outputs_incidence_M15_49 = calculate_incidence(outputs_Nincidentcases_M15_49,outputs_Npop_M15_49,outputs_Npos_M15_49)
    outputs_incidence_F15_49 = calculate_incidence(outputs_Nincidentcases_F15_49,outputs_Npop_F15_49,outputs_Npos_F15_49)
    outputs_incidence_M15_24 = calculate_incidence(outputs_Nincidentcases_M15_24,outputs_Npop_M15_24,outputs_Npos_M15_24)
    outputs_incidence_M25_49 = calculate_incidence(outputs_Nincidentcases_M25_49,outputs_Npop_M25_49,outputs_Npos_M25_49)
    outputs_incidence_F15_24 = calculate_incidence(outputs_Nincidentcases_F15_24,outputs_Npop_F15_24,outputs_Npos_F15_24)
    outputs_incidence_F25_49 = calculate_incidence(outputs_Nincidentcases_F25_49,outputs_Npop_F25_49,outputs_Npos_F25_49)

    outputs_incidence_adult15_49 = calculate_incidence(outputs_Nincidentcases_adult15_49,outputs_Npop15_49,outputs_Npos15_49)


    
    outputs_AIDSdeaths_M15plus = get_annual_from_cumulative(outputs_cumulativeAIDSdeaths_M15plus)
    outputs_AIDSdeaths_F15plus = get_annual_from_cumulative(outputs_cumulativeAIDSdeaths_F15plus)
    outputs_AIDSdeaths_child = get_annual_from_cumulative(outputs_cumulativeAIDSdeaths_child)
    outputs_AIDSdeaths_total = sum_three_outputs(outputs_AIDSdeaths_M15plus,outputs_AIDSdeaths_F15plus,outputs_AIDSdeaths_child)
                
    outputs_totaldeaths_M20_59 = get_annual_from_cumulative(outputs_cumulativetotaldeaths_M20_59)
    outputs_totaldeaths_F20_59 = get_annual_from_cumulative(outputs_cumulativetotaldeaths_F20_59)
    outputs_totaldeaths_adult20_59 = sum_two_outputs(outputs_totaldeaths_M20_59,outputs_totaldeaths_F20_59)

    outputs_Ntests_M15plus = get_annual_from_cumulative(outputs_cumulativeNtests_M15plus)
    outputs_Ntests_F15plus = get_annual_from_cumulative(outputs_cumulativeNtests_F15plus)
    outputs_annualNdiagnoses = get_annual_from_cumulative(outputs_cumulativeNdiagnoses)

    outputs_Ntests_adult15plus = sum_two_outputs(outputs_Ntests_M15plus,outputs_Ntests_F15plus)

    outputs_proportion_tests_pos_15plus = get_quotient(outputs_annualNdiagnoses,outputs_Ntests_adult15plus,ERR)

    ## Now make annual number of VMMC:
    #outputs_circ=get_annual_from_cumulative(outputs_circ_cumulative15_49)

    outdir = "checks/"
    if(not(os.path.isdir(outdir))):
        try:
            os.makedirs(outdir)
        except:
            print "Error - need to make directory ",outdir
            sys.exit()


    # I have validated these by hand against MIHPSA_output_CL05_Zim_patch0_Rand1_Run3_0.csv (this run is column H in each of the csv's below)
    validate=1
    if(validate==1):
        #outfile = open(outdir+"N_circ.csv","w")
        #outfile.write(generate_output_from_one_var(outputs_circ))
        #outfile.close()
        
        outfile = open(outdir+"Incidence_15_49.csv","w")
        outfile.write(generate_output_from_one_var(outputs_incidence_adult15_49))
        outfile.close()
    

        outfile = open(outdir+"Prop_tests_pos_15plus.csv","w")
        outfile.write(generate_output_from_one_var(outputs_proportion_tests_pos_15plus))
        outfile.close()
    


                

    outputs_to_store = {"Npop15_49":outputs_Npop15_49,
                        "Npop_15plus":outputs_Npop_15plus,
                        "Npop_M15plus":outputs_Npop_M15plus,
                        "Npop_F15plus":outputs_Npop_F15plus,
                        "Npop_child":outputs_Npop_child,
                        "Npop_total":outputs_Npop_total,
                        "PrevalenceM15_49":outputs_prevalence_M15_49,
                        "PrevalenceF15_49":outputs_prevalence_F15_49,
                        "PrevalenceAll15_49":outputs_prevalence_overall15_49,
                        "N_ART_M_15plus":outputs_N_ART_M15plus,
                        "N_ART_F_15plus":outputs_N_ART_F15plus,
                        "N_ART_child":outputs_N_ART_child,
                        "N_ART_total":outputs_N_ART_total,
                        "ARTcoverage_M_15plus":outputs_ARTcoverage_M15plus,
                        "ARTcoverage_F_15plus":outputs_ARTcoverage_F15plus,
                        "ARTcoverage_child":outputs_ARTcoverage_child,
                        "ARTcoverage_total":outputs_ARTcoverage_total,
                        "Diagnosed_onART_M_15plus":outputs_DiagOnART_M15plus,
                        "Diagnosed_onART_F_15plus":outputs_DiagOnART_F15plus,
                        #"VMMCoperations_15plus":outputs_circ,
                        "N_circ_15_49":outputs_Ncirc_15_49,
                        "prop_circ_15_49":outputs_propcirc_15_49,
                        "PropDiagnosed_M15plus":outputs_prop_diagnosed_M15plus,
                        "PropDiagnosed_F15plus":outputs_prop_diagnosed_F15plus,
                        "PropF15_24_condlasttime":outputs_prop_F15_24_sex_active_usedcondomlasttime,
                        "PropAdultVS":outputs_prop_VS_adult15plus,
                
                        "New_cases_M15_49":outputs_Nincidentcases_M15_49,
                        "New_cases_M15_24":outputs_Nincidentcases_M15_24,
                        "New_cases_M25_49":outputs_Nincidentcases_M25_49,
                        "New_cases_F15_49":outputs_Nincidentcases_F15_49,
                        "New_cases_F15_24":outputs_Nincidentcases_F15_24,
                        "New_cases_F25_49":outputs_Nincidentcases_F25_49,
                        "New_cases_total15_49":outputs_Nincidentcases_adult15_49,
                        "IncidenceM15_49":outputs_incidence_M15_49,
                        "IncidenceF15_49":outputs_incidence_F15_49,
                        "Incidencetotal15_49":outputs_incidence_adult15_49,
                        "AIDSdeaths_M15plus":outputs_AIDSdeaths_M15plus,
                        "AIDSdeaths_F15plus":outputs_AIDSdeaths_F15plus,
                        "AIDSdeaths_child":outputs_AIDSdeaths_child,
                        "AIDSdeaths_total":outputs_AIDSdeaths_total,
                        "totaldeaths_M20_59":outputs_totaldeaths_M20_59,
                        "totaldeaths_F20_59":outputs_totaldeaths_F20_59,
                        "totaldeaths_adult20_59":outputs_totaldeaths_adult20_59,
                        "Ntests_M15plus":outputs_Ntests_M15plus,
                        "Ntests_F15plus":outputs_Ntests_F15plus,
                        "Ntests_adult15plus":outputs_Ntests_adult15plus,
                        "Prop_tests_pos_15plus":outputs_proportion_tests_pos_15plus,
                        "Npos_M15plus":outputs_Npos_M15plus,
                        "Npos_F15plus":outputs_Npos_F15plus,
                        "Npos_child":outputs_Npos_child,
                        "Npos_total":outputs_Npos_total,
                        "PrevalenceM15_24":outputs_prevalence_M15_24,
                        "PrevalenceM25_49":outputs_prevalence_M25_49,
                        "PrevalenceF15_24":outputs_prevalence_F15_24,
                        "PrevalenceF25_49":outputs_prevalence_F25_49,
                        "Prevalence_child":outputs_prevalence_child,
                        "IncidenceM15_24":outputs_incidence_M15_24,
                        "IncidenceM25_49":outputs_incidence_M25_49,
                        "IncidenceF15_24":outputs_incidence_F15_24,
                        "IncidenceF25_49":outputs_incidence_F25_49,
                        "Npop_M15_24":outputs_Npop_M15_24,
                        "Npop_M25_49":outputs_Npop_M25_49,
                        "Npop_F15_24":outputs_Npop_F15_24,
                        "Npop_F25_49":outputs_Npop_F25_49

                        
    }

                        
    


                        

    list_of_outputs = ["PrevalenceM15_49","PrevalenceF15_49","PrevalenceAll15_49","ARTcoverage_M_15plus","ARTcoverage_F_15plus","ARTcoverage_child","ARTcoverage_total","N_ART_M_15plus","N_ART_F_15plus","N_ART_child","N_ART_total","prop_circ_15_49",
                       "PropDiagnosed_M15plus","PropDiagnosed_F15plus","PropF15_24_condlasttime","PropAdultVS","Npop_15plus","Npop_M15plus","Npop_F15plus","Npop15_49","Npop_child","Npop_total","Diagnosed_onART_M_15plus","Diagnosed_onART_F_15plus",
                       "New_cases_M15_49","New_cases_F15_49","New_cases_total15_49","IncidenceM15_49","IncidenceF15_49","Incidencetotal15_49","AIDSdeaths_M15plus","AIDSdeaths_F15plus","AIDSdeaths_child","AIDSdeaths_total","totaldeaths_M20_59","totaldeaths_F20_59","totaldeaths_adult20_59","Ntests_M15plus","Ntests_F15plus","Ntests_adult15plus","Prop_tests_pos_15plus",
                       "Npos_M15plus","Npos_F15plus","Npos_child","Npos_total","PrevalenceM15_24","PrevalenceF15_24","PrevalenceM25_49","PrevalenceF25_49",
                       "IncidenceM15_24","IncidenceF15_24","IncidenceM25_49","IncidenceF25_49",
                       "New_cases_M15_24","New_cases_F15_24","New_cases_M25_49","New_cases_F25_49"
    ]
                        

    #,"Prevalence_child"

    make_mean_CI(outputs_to_store,list_of_outputs)    
    

    
    #write_output(outputs_ART_adult,"MIHPSA_ART_adult.csv")
    #write_output(outputs_ART_child,"MIHPSA_ART_child.csv")
    #write_output(outputs_ART_total,"MIHPSA_ART_total.csv")
    #write_output(outputs_circ,"MIHPSA_circ.csv")
        
    #write_output(outputs_prevalence_overall,"MIHPSA_HIV_prev_overall.csv")


    #outfile = open(mihpsafiledir + "/" + calibration_output_filename,"w")
    #outfile.write(outstring)
    #outfile.close()



    
##################################
# Main code:
##################################

mihpsafiledir = "params/Output/"



# This function looks in mihpsafiledir for all the MIHPSA_Output*.csv files and makes an output file for the MIHPSA project.
# Saves these as 
read_mihpsa_files_and_make_summary_file(mihpsafiledir)

