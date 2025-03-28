import glob, sys, os, math
import numpy
import pandas # for Excel
import collections  # Used to check for duplicates


## Use as flag to create outputs:
MIHPSA_SCENARIO = 99

## 1 - Essential scenario
## 2 - Essential + PrEP scenario
## 3 - Phase 2 status quo scenario
## 4 - Phase 2 minimal scenario
## 5 - Phase 2 minimal plus CUPP scenario
## 6 - Phase 2 minimal plus SBCC scenario
## 7 - Phase 2 minimal + PrEP scenario


## To get from 1990 to 2040, need to use 2041.
MIHPSA_TIMEPERIOD = 2073

USE_STDEV = 0 # Print mean +/- 1.645*s.d. or not in make_mean_CI()


survey_N_art = [1000*x for x in [7712.514,7822.167,7936.191,8044.421,8172.255,8316.685,8471.238,8633.707,8773.997323]]   # Aged 15+. See C:\Users\mpickles\Dropbox (SPH Imperial College)\projects\MIHPSA_Zimabwe2021\Zimbabwe_WPP_pop_for_ART.xlsx. Based on WPP 2019, with extrapolation for 2021. Note that WPP is in thousands (so multiply by 1000).
year_ART = range(2013,2022) # Specified in MIHPSA file sent by Valentina. Note "All ART totals are reported at the end of each year." - so take 2013.0 etc.

survey_N_art_children = [1000*x for x in [5637.864,5764.543,5878.451,5985.917,6064.344,6122.127,6174.235,6229.22,6318.618]]

# Need to scale the IBM population to the total population of Zimbabwe. Right now we use the 2021 index:
MIHPSA_population_scale_adult_year = 2021
MIHPSA_population_scale_adult = survey_N_art[year_ART.index(MIHPSA_population_scale_adult_year)]
print("MIHPSA adult population aged 15+ in 2021 is ",MIHPSA_population_scale_adult)

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
    i_N_newHIVdiagnoses_15plus_male = header.index('N_newHIVdiagnoses_15plus_male')
    i_N_newHIVdiagnoses_15plus_female = header.index('N_newHIVdiagnoses_15plus_female')

    i_VMMC_op = header.index('N_VMMC_cumulative_15_49') # Cumulative # of VMMCs carried out in 15-49
    
    i_circ = header.index('Ncirc_15to49') # This is (cumulative) men circumcised either VMMC or TMC aged 15-49.
    i_N_ARTinitiations_15plus = header.index('N_ARTinitiations_15plus')
    i_N_ARTreinitiations_15plus = header.index('N_ARTreinitiations_15plus')

    
    i_N_ARTexperienced_bysex_15plus_male = header.index('N_ARTexperienced_bysex_15plus_male')
    i_N_ARTexperienced_bysex_15plus_female = header.index('N_ARTexperienced_bysex_15plus_female')
    i_N_ARTexperienced_bysex_younger_male = header.index('N_ARTexperienced_bysex_younger_male')
    i_N_ARTexperienced_bysex_younger_female = header.index('N_ARTexperienced_bysex_younger_female')
    i_N_ARTexperienced_bysex_older_male = header.index('N_ARTexperienced_bysex_older_male')
    i_N_ARTexperienced_bysex_older_female = header.index('N_ARTexperienced_bysex_older_female')
    i_n_women_at_elevatedrisk_15to24 = header.index('n_women_at_elevatedrisk_15to24')
    
    i_n_women_at_elevatedrisk_andonoralPrEP_15to24 = header.index('n_women_at_elevatedrisk_andonoralPrEP_15to24')
    i_N_VS_bysex_younger_male = header.index('N_VS_bysex_younger_male')
    i_N_VS_bysex_younger_female = header.index('N_VS_bysex_younger_female')
    i_N_VS_bysex_older_male = header.index('N_VS_bysex_older_male')
    i_N_VS_bysex_older_female = header.index('N_VS_bysex_older_female')
    i_N_newHIVinfections_15plus_male = header.index('N_newHIVinfections_15plus_male')
    i_N_newHIVinfections_15plus_female = header.index('N_newHIVinfections_15plus_female')
    i_N_newbirths = header.index('N_newbirths')
    i_N_newbirths_HIVpos = header.index('N_newbirths_HIVpos')
    i_N_deaths_15plus_male = header.index('N_deaths_15plus_male')
    i_N_deaths_15plus_female = header.index('N_deaths_15plus_female')
    i_YLL_15plus_male = header.index('YLL_15plus_male')
    i_YLL_15plus_female = header.index('YLL_15plus_female')
    i_YLL_children_under15 = header.index('YLL_children_under15')
    i_YLL_15plus_male_discounted = header.index('YLL_15plus_male_discounted')
    i_YLL_15plus_female_discounted = header.index('YLL_15plus_female_discounted')
    i_YLL_children_under15_discounted = header.index('YLL_children_under15_discounted')


    i_n_women_used_oralPrEP_lastQ_15to24 = header.index('n_women_used_oralPrEP_lastQ_15to24')
    i_n_women_active_oralPrEP_lastQ_15to24 = header.index('n_women_active_oralPrEP_lastQ_15to24')
    i_n_women_ever_oralPrEP_15to24 = header.index('n_women_ever_oralPrEP_15to24')
    i_n_women_used_dapivirinering_lastQ_15to24 = header.index('n_women_used_dapivirinering_lastQ_15to24')
    i_n_women_active_dapivirinering_lastQ_15to24 = header.index('n_women_active_dapivirinering_lastQ_15to24')
    i_n_women_used_injectablePrEP_lastQ_15to24 = header.index('n_women_used_injectablePrEP_lastQ_15to24')
    i_n_women_active_injectablePrEP_lastQ_15to24 = header.index('n_women_active_injectablePrEP_lastQ_15to24')
    i_n_women_used_oralPrEP_lastQ_15plus_sdpartner = header.index('n_women_used_oralPrEP_lastQ_15plus_sdpartner')
    i_n_women_active_oralPrEP_lastQ_15plus_sdpartner = header.index('n_women_active_oralPrEP_lastQ_15plus_sdpartner')
    i_n_women_used_dapivirinering_lastQ_15plus_sdpartner = header.index('n_women_used_dapivirinering_lastQ_15plus_sdpartner')
    i_n_women_active_dapivirinering_lastQ_15plus_sdpartner = header.index('n_women_active_dapivirinering_lastQ_15plus_sdpartner')
    i_n_women_used_injectablePrEP_lastQ_15plus_sdpartner = header.index('n_women_used_injectablePrEP_lastQ_15plus_sdpartner')
    i_n_women_active_injectablePrEP_lastQ_15plus_sdpartner = header.index('n_women_active_injectablePrEP_lastQ_15plus_sdpartner')

    i_N_firsttime_oralPrEPinitiations_15to24F = header.index('N_firsttime_oralPrEPinitiations_15to24F')
    
    i_n_notonART_byCD4_15plus_gt500 = header.index('n_notonART_byCD4_15plus[0]')
    i_n_notonART_byCD4_15plus_350_500 = header.index('n_notonART_byCD4_15plus[1]')
    i_n_notonART_byCD4_15plus_200_350 = header.index('n_notonART_byCD4_15plus[2]')
    i_n_notonART_byCD4_15plus_lt200 = header.index('n_notonART_byCD4_15plus[3]')
    i_N_HIVneg_in_SD_partnership_M15plus = header.index('N_HIVneg_in_SD_partnership_M15plus')
    i_N_HIVneg_in_SD_partnership_F15plus = header.index('N_HIVneg_in_SD_partnership_F15plus')
    i_N_HIVneg_in_SD_partnership_noART_M15plus = header.index('N_HIVneg_in_SD_partnership_noART_M15plus')
    i_N_HIVneg_in_SD_partnership_noART_F15plus = header.index('N_HIVneg_in_SD_partnership_noART_F15plus')
    i_n_eversex_M15plus = header.index('n_eversex_M15plus')
    i_n_eversex_F15plus = header.index('n_eversex_F15plus')
    i_n_usedcondomlastact_M15plus = header.index('n_usedcondomlastact_M15plus')
    i_n_usedcondomlastact_F15plus = header.index('n_usedcondomlastact_F15plus')
    i_nonART_M15_24 = header.index('nonART_M15_24')
    i_nonART_F15_24 = header.index('nonART_F15_24')
    i_naware_M15_24 = header.index('naware_M15_24')
    i_naware_F15_24 = header.index('naware_F15_24')

    i_N_newHIVdiagnoses_15to24F = header.index('N_newHIVdiagnoses_15to24F')
    i_N_HIVtests_15to24F = header.index('N_HIVtests_15to24F')
    


    
    return [i_NpopM15_49,i_NpopF15_49,i_NpopM15_24,i_NpopF15_24,i_NpopM25_49,i_NpopF25_49,i_PosM15_49,i_PosF15_49,i_PosM15_24,i_PosF15_24,i_PosM25_49,i_PosF25_49,i_art_child,i_NpopM15plus,i_NpopF15plus,i_Npop_child,i_circ,i_NposM15plus,i_NposF15plus,i_Npos_child,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_women_sexuallyactive_15to24,i_N_women_usecondomlastact_15to24,i_N_deaths_20_59_male,i_N_deaths_20_59_female,i_N_AIDSdeaths_15plus_male,i_N_AIDSdeaths_15plus_female,i_N_AIDSdeaths_children_under15,i_N_HIVtests_15plus_male,i_N_HIVtests_15plus_female,i_N_newHIVinfections_15to24_male,i_N_newHIVinfections_25to49_male,i_N_newHIVinfections_15to24_female,i_N_newHIVinfections_25to49_female,i_N_newHIVdiagnoses_15plus_male,i_N_newHIVdiagnoses_15plus_female,i_VMMC_op,i_N_ARTinitiations_15plus,i_N_ARTreinitiations_15plus,i_N_ARTexperienced_bysex_15plus_male,i_N_ARTexperienced_bysex_15plus_female,i_N_ARTexperienced_bysex_younger_male,i_N_ARTexperienced_bysex_younger_female,i_N_ARTexperienced_bysex_older_male,i_N_ARTexperienced_bysex_older_female,i_n_women_at_elevatedrisk_15to24,i_n_women_at_elevatedrisk_andonoralPrEP_15to24,i_N_VS_bysex_younger_male,i_N_VS_bysex_younger_female,i_N_VS_bysex_older_male,i_N_VS_bysex_older_female,i_N_newHIVinfections_15plus_male,i_N_newHIVinfections_15plus_female,i_N_newbirths,i_N_newbirths_HIVpos,i_N_deaths_15plus_male,i_N_deaths_15plus_female,i_YLL_15plus_male,i_YLL_15plus_female,i_YLL_children_under15,i_YLL_15plus_male_discounted,i_YLL_15plus_female_discounted,i_YLL_children_under15_discounted,i_n_notonART_byCD4_15plus_gt500,i_n_notonART_byCD4_15plus_350_500,i_n_notonART_byCD4_15plus_200_350,i_n_notonART_byCD4_15plus_lt200,i_N_HIVneg_in_SD_partnership_M15plus,i_N_HIVneg_in_SD_partnership_F15plus,i_N_HIVneg_in_SD_partnership_noART_M15plus,i_N_HIVneg_in_SD_partnership_noART_F15plus,i_n_eversex_M15plus,i_n_eversex_F15plus,i_n_usedcondomlastact_M15plus,i_n_usedcondomlastact_F15plus,i_nonART_M15_24,i_nonART_F15_24,i_naware_M15_24,i_naware_F15_24,i_n_women_used_oralPrEP_lastQ_15to24,i_n_women_active_oralPrEP_lastQ_15to24,i_n_women_ever_oralPrEP_15to24,i_n_women_used_dapivirinering_lastQ_15to24,i_n_women_active_dapivirinering_lastQ_15to24,i_n_women_used_injectablePrEP_lastQ_15to24,i_n_women_active_injectablePrEP_lastQ_15to24,i_n_women_used_oralPrEP_lastQ_15plus_sdpartner,i_n_women_active_oralPrEP_lastQ_15plus_sdpartner,i_n_women_used_dapivirinering_lastQ_15plus_sdpartner,i_n_women_active_dapivirinering_lastQ_15plus_sdpartner,i_n_women_used_injectablePrEP_lastQ_15plus_sdpartner,i_n_women_active_injectablePrEP_lastQ_15plus_sdpartner,i_N_firsttime_oralPrEPinitiations_15to24F,i_N_newHIVdiagnoses_15to24F,i_N_HIVtests_15to24F]

    

    


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
            print(f"Scales: {scale_VMMC} {scale_tot_adult} {scale_child} {scale_pop}")
            break

    #return [scale_pop, scale_pop, scale_pop, scale_pop]
    return [scale_VMMC, scale_tot_adult, scale_child, scale_pop]


def write_output(outputs,outfile):
    outstring = ""
    years_saved = sorted(outputs)

    for year in years_saved:
        outstring += str(year)+","
        for run_output in outputs[year]:
            outstring += str(run_output)+","
        outstring = outstring.rstrip(",") +"\n"
        

    outfile = open(outfile,"w")
    outfile.write(outstring)
    outfile.close()

def get_annual_from_cumulative(outputs_cumulative):
    years = sorted(outputs_cumulative)
    outputs = {}
    #outputs[years[0]] = outputs_cumulative[years[0]][:]
    #outputs[years[0]] = [0]*len(outputs_cumulative[years[0]])
    for y in range(len(years)-1):
        # The cumulative outputs start at 1990.5.
        # We want the first annual output to be for 1990.5-1991.5.
        outputs[years[y]] = [outputs_cumulative[years[y+1]][i] - outputs_cumulative[years[y]][i] for i in range(len(outputs_cumulative[years[y]]))]

    return outputs

def sum_two_outputs(output1,output2):
    years = sorted(output1)

    outputs_summed = {}
    #outputs_summed[years[0]] = [0]*len(output1[years[0]])
    for y in range(len(years)):
        outputs_summed[years[y]] = [output1[years[y]][i]+output2[years[y]][i] for i in range(len(output1[years[y]]))]

    return outputs_summed



def sum_three_outputs(output1,output2,output3):
    years = sorted(output1)
    outputs_summed = {}
    #outputs_summed[years[0]] = [0]*len(output1[years[0]])
    for y in range(len(years)):
        outputs_summed[years[y]] = [output1[years[y]][i]+output2[years[y]][i]+output3[years[y]][i] for i in range(len(output1[years[y]]))]

    return outputs_summed
    

def calculate_incidence(N_newinfections,Npop,Npos):
    years = sorted(N_newinfections)

    incidence = {}
    #incidence[years[0]] = [0]*len(N_newinfections[years[0]])
    for y in range(len(years)):
        #print y, len(N_newinfections[years[y]]),len(Npop),len(Npos)
        incidence[years[y]] = [100*N_newinfections[years[y]][i] / (Npop[years[y]][i] - Npos[years[y]][i]) for i in range(len(N_newinfections[years[y]]))]
    return incidence

def get_quotient(output1,output2,ERR):
    years = sorted(output1)

    outputs_quotient = {}
    outputs_quotient[years[0]] = [0]*len(output1[years[0]])
    for y in range(1,len(years)):
        outputs_quotient[years[y]] = [output1[years[y]][i]/(1.0*output2[years[y]][i]+ERR) for i in range(len(output1[years[y]]))]

    return outputs_quotient

def get_quarterly_from_annual(output):
    years = sorted(output)

    outputs_quarterly = {}
    outputs_quarterly[years[0]] = [0]*len(output[years[0]])
    for y in range(1,len(years)):
        outputs_quarterly[years[y]] = [output[years[y]][i]/4.0 for i in range(len(output[years[y]]))]

    return outputs_quarterly



def generate_output_from_one_var(output):
    outstr = ""
    for y in range(1990,MIHPSA_TIMEPERIOD):
        #print(y,output[y])
        outstr += str(y)+" "+" ".join([str(x) for x in output[y]])+"\n"
    return outstr


def make_mean_CI(outputs_dict,output_names,output_file):

    output_string = "Outcome Measure "+" ".join([str(x) for x in range(1990,MIHPSA_TIMEPERIOD)])+"\n"
    for outputname in output_names:
        #print(outputname)
        mean_output = []
        median_output = []
        ll_output = []
        ul_output = []
        ll_stdev = []
        ul_stdev = []
        for y in range(1990,MIHPSA_TIMEPERIOD):
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

        
    outfile = open(output_file,"w")
    #outfile = open("MIHPSA_project_outputs_phase2.csv","w")
    outfile.write(output_string)
    outfile.close()

def make_mean_CI_andstore(outputs_dict):

    output_median_CI_dict = {}
    
    for outputname in outputs_dict.keys():
        #print(outputname)
        mean_output = []
        median_output = []
        ll_output = []
        ul_output = []
        ll_stdev = []
        ul_stdev = []
        for y in range(1990,MIHPSA_TIMEPERIOD):
            mean_output += [numpy.mean(outputs_dict[outputname][y])]
            median_output += [numpy.median(outputs_dict[outputname][y])]
            ll_output += [numpy.percentile(outputs_dict[outputname][y],5)]
            ul_output += [numpy.percentile(outputs_dict[outputname][y],95)]
            ll_stdev += [numpy.mean(outputs_dict[outputname][y]) - 1.645* numpy.std(outputs_dict[outputname][y])]
            ul_stdev += [numpy.mean(outputs_dict[outputname][y]) + 1.645* numpy.std(outputs_dict[outputname][y])]

        output_median_CI_dict[outputname] = {"Median":median_output, "LL":ll_output, "UL":ul_output}


        


    return(output_median_CI_dict)

        

def read_mihpsa_files_and_make_summary_file(mihpsafiledir):

    ERR=1e-12
    
    mihpsafiles = glob.glob(mihpsafiledir + "/MIHPSA_output_CL*.csv")
    print(f"{mihpsafiles}")

    #[i_NpopM15_49,i_NpopF15_49,i_PosM15_49,i_PosF15_49,i_artM15plus,i_artF15plus,i_art_child,i_NpopM15plus,i_NpopF15plus,i_Npop_child,i_circ,i_NposM15plus,i_NposF15plus,i_Npos_child,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_women_sexuallyactive_15to24,i_N_women_usecondomlastact_15to24,i_N_deaths_20_59_male,i_N_deaths_20_59_female,i_N_AIDSdeaths_15plus_male,i_N_AIDSdeaths_15plus_female,i_N_AIDSdeaths_children_under15,i_N_HIVtests_15plus_male,i_N_HIVtests_15plus_female,i_N_newHIVinfections_15to49_male,i_N_newHIVinfections_15to49_female,i_N_newHIVdiagnoses_15plus]

    [i_NpopM15_49,i_NpopF15_49,i_NpopM15_24,i_NpopF15_24,i_NpopM25_49,i_NpopF25_49,i_PosM15_49,i_PosF15_49,i_PosM15_24,i_PosF15_24,i_PosM25_49,i_PosF25_49,i_art_child,i_NpopM15plus,i_NpopF15plus,i_Npop_child,i_circ,i_NposM15plus,i_NposF15plus,i_Npos_child,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_women_sexuallyactive_15to24,i_N_women_usecondomlastact_15to24,i_N_deaths_20_59_male,i_N_deaths_20_59_female,i_N_AIDSdeaths_15plus_male,i_N_AIDSdeaths_15plus_female,i_N_AIDSdeaths_children_under15,i_N_HIVtests_15plus_male,i_N_HIVtests_15plus_female,i_N_newHIVinfections_15to24_male,i_N_newHIVinfections_25to49_male,i_N_newHIVinfections_15to24_female,i_N_newHIVinfections_25to49_female,i_N_newHIVdiagnoses_15plus_male,i_N_newHIVdiagnoses_15plus_female,i_VMMC_op,i_N_ARTinitiations_15plus,i_N_ARTreinitiations_15plus,i_N_ARTexperienced_bysex_15plus_male,i_N_ARTexperienced_bysex_15plus_female,i_N_ARTexperienced_bysex_younger_male,i_N_ARTexperienced_bysex_younger_female,i_N_ARTexperienced_bysex_older_male,i_N_ARTexperienced_bysex_older_female,i_n_women_at_elevatedrisk_15to24,i_n_women_at_elevatedrisk_andonoralPrEP_15to24,i_N_VS_bysex_younger_male,i_N_VS_bysex_younger_female,i_N_VS_bysex_older_male,i_N_VS_bysex_older_female,i_N_newHIVinfections_15plus_male,i_N_newHIVinfections_15plus_female,i_N_newbirths,i_N_newbirths_HIVpos,i_N_deaths_15plus_male,i_N_deaths_15plus_female,i_YLL_15plus_male,i_YLL_15plus_female,i_YLL_children_under15,i_YLL_15plus_male_discounted,i_YLL_15plus_female_discounted,i_YLL_children_under15_discounted,i_n_notonART_byCD4_15plus_gt500,i_n_notonART_byCD4_15plus_350_500,i_n_notonART_byCD4_15plus_200_350,i_n_notonART_byCD4_15plus_lt200,i_N_HIVneg_in_SD_partnership_M15plus,i_N_HIVneg_in_SD_partnership_F15plus,i_N_HIVneg_in_SD_partnership_noART_M15plus,i_N_HIVneg_in_SD_partnership_noART_F15plus,i_n_eversex_M15plus,i_n_eversex_F15plus,i_n_usedcondomlastact_M15plus,i_n_usedcondomlastact_F15plus,i_nonART_M15_24,i_nonART_F15_24,i_naware_M15_24,i_naware_F15_24,i_n_women_used_oralPrEP_lastQ_15to24,i_n_women_active_oralPrEP_lastQ_15to24,i_n_women_ever_oralPrEP_15to24,i_n_women_used_dapivirinering_lastQ_15to24,i_n_women_active_dapivirinering_lastQ_15to24,i_n_women_used_injectablePrEP_lastQ_15to24,i_n_women_active_injectablePrEP_lastQ_15to24,i_n_women_used_oralPrEP_lastQ_15plus_sdpartner,i_n_women_active_oralPrEP_lastQ_15plus_sdpartner,i_n_women_used_dapivirinering_lastQ_15plus_sdpartner,i_n_women_active_dapivirinering_lastQ_15plus_sdpartner,i_n_women_used_injectablePrEP_lastQ_15plus_sdpartner,i_n_women_active_injectablePrEP_lastQ_15plus_sdpartner,i_N_firsttime_oralPrEPinitiations_15to24F,i_N_newHIVdiagnoses_15to24F,i_N_HIVtests_15to24F] = read_MIHPSA_header(mihpsafiles[0])

    
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
    outputs_ARTcoverage_F15_24 = {}
    outputs_ARTcoverage_15_24 = {}


    outputs_DiagOnART_M15plus = {}
    outputs_DiagOnART_F15plus = {}
    outputs_DiagOnART_F15_24 = {}
    outputs_DiagOnART_15_24 = {}
    outputs_DiagOnART_15plus = {}


    outputs_prop_diagnosed_M15plus = {}
    outputs_prop_diagnosed_F15plus = {}
    outputs_prop_diagnosed_child = {}
    outputs_prop_diagnosed_15plus = {}

    outputs_prop_diagnosed_M15_24 = {}
    outputs_prop_diagnosed_F15_24 = {}

    outputs_VMMC_cumulative15_49 = {}
    
    outputs_Ncirc_15_49 = {} # Number of 15-49 year old men who are currently circumcised.

    outputs_propcirc_15_49 = {} # Number of 15-49 year old men who are currently circumcised.
    
    outputs_prop_F15_24_sex_active_usedcondomlasttime = {}

    outputs_prop_VS_adult15plus = {}
    outputs_prop_VS_adult15_24 = {} ## Added MIHPSA phase 2


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


    ## Added phase 2 (stores of cumulative totals to generate annual flows):
    outputs_cumulativetotaldeaths_M15plus = {}
    outputs_cumulativetotaldeaths_F15plus = {}
    outputs_cumulativeYLL_15plus = {}
    outputs_cumulativeYLL_child = {}
    outputs_cumulativeYLL_15plus_discounted = {}
    outputs_cumulativeYLL_child_discounted = {}

    
    outputs_cumulativeNtests_M15plus = {}
    outputs_cumulativeNtests_F15plus = {}
    outputs_cumulativeNtests_15to24F = {}
    outputs_cumulativeNdiagnoses = {}
    outputs_cumulativeNdiagnoses_M15plus = {}
    outputs_cumulativeNdiagnoses_F15plus = {}
    outputs_cumulativeNdiagnoses_15to24F = {}


    
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

    ## Added MIHPSA phase 2:
    outputs_totaldeaths_M15plus = {}
    outputs_totaldeaths_F15plus = {}

    
    outputs_Ntests_M15plus = {}
    outputs_Ntests_F15plus = {}
    outputs_Ntests_adult15plus = {}

    outputs_proportion_tests_pos_15plus = {}

    ## Added MIHPSA phase 2:
    outputs_prop_ARTexperienced_M15plus = {}
    outputs_prop_ARTexperienced_F15plus = {}
    outputs_prop_ARTexperienced_15_24 = {}
    outputs_prop_ARTexperienced_15plus = {}

    ## Added MIHPSA phase 2:
    outputs_N_women_at_elevatedrisk_15to24 = {}
    outputs_prop_women_at_elevatedrisk_andonPrEP_15to24 = {}
    outputs_N_women_at_elevatedrisk_andonPrEP_15to24 = {}

    outputs_Ncumulativecases_M15plus = {}
    outputs_Ncumulativecases_F15plus = {}
    outputs_cumulative_newbirths = {}
    outputs_cumulative_newbirths_HIVpos = {}


    outputs_n_notonART_byCD4_15plus_gt500 = {}
    outputs_n_notonART_byCD4_15plus_350_500 = {}
    outputs_n_notonART_byCD4_15plus_200_350 = {}
    outputs_n_notonART_byCD4_15plus_50_200 = {}
    outputs_n_notonART_byCD4_15plus_lt50 = {}
    outputs_N_HIVneg_in_SD_partnership_15plus = {}
    outputs_N_HIVneg_in_SD_partnership_F15plus = {}
    outputs_N_HIVneg_in_SD_partnership_noART_F15plus = {}
    outputs_N_HIVneg_in_SD_partnership_noART_15plus = {}
    outputs_n_eversex_M15plus = {}
    outputs_n_eversex_F15plus = {}
    outputs_prop_eversex_M15plus = {}
    outputs_prop_eversex_F15plus = {}
    outputs_prop_eversex_F15_24 = {}
    outputs_prop_usedcondomlastact_M15plus = {}
    outputs_prop_usedcondomlastact_F15plus = {}
    outputs_nonART_M15_24 = {}
    outputs_nonART_F15_24 = {}
    outputs_nonART_15_24 = {}
    outputs_naware_M15_24 = {}
    outputs_naware_F15_24 = {}


    outputs_N_women_used_oralPrEP_lastQ_15to24 = {}
    outputs_N_women_active_oralPrEP_lastQ_15to24 = {} 
    outputs_N_women_ever_oralPrEP_15to24 = {}
    outputs_N_women_used_dapivirinering_lastQ_15to24 = {} 
    outputs_N_women_active_dapivirinering_lastQ_15to24 = {} 
    outputs_N_women_used_injectablePrEP_lastQ_15to24 = {} 
    outputs_N_women_active_injectablePrEP_lastQ_15to24 = {} 
    outputs_N_women_used_oralPrEP_lastQ_15plus_sdpartner = {} 
    outputs_N_women_active_oralPrEP_lastQ_15plus_sdpartner = {} 
    outputs_N_women_used_dapivirinering_lastQ_15plus_sdpartner = {} 
    outputs_N_women_active_dapivirinering_lastQ_15plus_sdpartner = {} 
    outputs_N_women_used_injectablePrEP_lastQ_15plus_sdpartner = {} 
    outputs_N_women_active_injectablePrEP_lastQ_15plus_sdpartner = {} 
    outputs_cumulativeN_firsttime_oralPrEPinitiations_15to24F = {} 

    outputs_cumulativeNARTinitiations_15plus = {}
    outputs_cumulativeNARTreinitiations_15plus = {}

    
    
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

            # print(i)
            # print(line)
            # ls = line.split(",")
            # for index in [0,i_NpopM15_49,i_NpopF15_49,i_NpopM15_24,i_NpopF15_24,i_NpopM25_49,i_NpopF25_49,i_PosM15_49,i_PosF15_49,i_PosM15_24,i_PosF15_24,i_PosM25_49,i_PosF25_49,i_art_child,i_NpopM15plus,i_NpopF15plus,i_Npop_child,i_circ,i_NposM15plus,i_NposF15plus,i_Npos_child,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_women_sexuallyactive_15to24,i_N_women_usecondomlastact_15to24,i_N_deaths_20_59_male,i_N_deaths_20_59_female,i_N_AIDSdeaths_15plus_male,i_N_AIDSdeaths_15plus_female,i_N_AIDSdeaths_children_under15,i_N_HIVtests_15plus_male,i_N_HIVtests_15plus_female,i_N_newHIVinfections_15to24_male,i_N_newHIVinfections_25to49_male,i_N_newHIVinfections_15to24_female,i_N_newHIVinfections_25to49_female,i_N_newHIVdiagnoses_15plus_male,i_N_newHIVdiagnoses_15plus_female,i_VMMC_op,i_N_ARTexperienced_bysex_15plus_male,i_N_ARTexperienced_bysex_15plus_female,i_N_ARTexperienced_bysex_younger_male,i_N_ARTexperienced_bysex_younger_female,i_N_ARTexperienced_bysex_older_male,i_N_ARTexperienced_bysex_older_female,i_n_women_at_elevatedrisk_15to24,i_n_women_at_elevatedrisk_andonoralPrEP_15to24,i_N_VS_bysex_younger_male,i_N_VS_bysex_younger_female,i_N_VS_bysex_older_male,i_N_VS_bysex_older_female,i_N_newHIVinfections_15plus_male,i_N_newHIVinfections_15plus_female,i_N_newbirths,i_N_newbirths_HIVpos,i_N_deaths_15plus_male,i_N_deaths_15plus_female,i_YLL_15plus_male,i_YLL_15plus_female,i_YLL_children_under15]:
            #     print(ls[index])

            [year,NpopM15_49,NpopF15_49,NpopM15_24,NpopF15_24,NpopM25_49,NpopF25_49,PosM15_49,PosF15_49,PosM15_24,PosF15_24,PosM25_49,PosF25_49,art_child,NpopM15plus,NpopF15plus,Npop_child,Ncirc_15_49,NposM15plus,NposF15plus,Npos_child,NawareM15plus,NawareF15plus,NonARTM15plus,NonARTF15plus,N_VSM15plus,N_VSF15plus,N_women_sexuallyactive_15to24,N_women_usecondomlastact_15to24,N_deaths_20_59_male,N_deaths_20_59_female,N_AIDSdeaths_15plus_male,N_AIDSdeaths_15plus_female,N_AIDSdeaths_children_under15,N_HIVtests_15plus_male,N_HIVtests_15plus_female,N_newHIVinfections_15to24_male,N_newHIVinfections_25to49_male,N_newHIVinfections_15to24_female,N_newHIVinfections_25to49_female,N_newHIVdiagnoses_15plus_male,N_newHIVdiagnoses_15plus_female,N_VMMC_op_cumulative,N_ARTinitiations_15plus,N_ARTreinitiations_15plus,N_ARTexperienced_bysex_15plus_male,N_ARTexperienced_bysex_15plus_female,N_ARTexperienced_bysex_younger_male,N_ARTexperienced_bysex_younger_female,N_ARTexperienced_bysex_older_male,N_ARTexperienced_bysex_older_female,n_women_at_elevatedrisk_15to24,n_women_at_elevatedrisk_andonoralPrEP_15to24,N_VS_bysex_younger_male,N_VS_bysex_younger_female,N_VS_bysex_older_male,N_VS_bysex_older_female,N_newHIVinfections_15plus_male,N_newHIVinfections_15plus_female,N_newbirths,N_newbirths_HIVpos,N_deaths_15plus_male,N_deaths_15plus_female] = [int(line.split(",")[index]) for index in [0,i_NpopM15_49,i_NpopF15_49,i_NpopM15_24,i_NpopF15_24,i_NpopM25_49,i_NpopF25_49,i_PosM15_49,i_PosF15_49,i_PosM15_24,i_PosF15_24,i_PosM25_49,i_PosF25_49,i_art_child,i_NpopM15plus,i_NpopF15plus,i_Npop_child,i_circ,i_NposM15plus,i_NposF15plus,i_Npos_child,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_women_sexuallyactive_15to24,i_N_women_usecondomlastact_15to24,i_N_deaths_20_59_male,i_N_deaths_20_59_female,i_N_AIDSdeaths_15plus_male,i_N_AIDSdeaths_15plus_female,i_N_AIDSdeaths_children_under15,i_N_HIVtests_15plus_male,i_N_HIVtests_15plus_female,i_N_newHIVinfections_15to24_male,i_N_newHIVinfections_25to49_male,i_N_newHIVinfections_15to24_female,i_N_newHIVinfections_25to49_female,i_N_newHIVdiagnoses_15plus_male,i_N_newHIVdiagnoses_15plus_female,i_VMMC_op,i_N_ARTinitiations_15plus,i_N_ARTreinitiations_15plus,i_N_ARTexperienced_bysex_15plus_male,i_N_ARTexperienced_bysex_15plus_female,i_N_ARTexperienced_bysex_younger_male,i_N_ARTexperienced_bysex_younger_female,i_N_ARTexperienced_bysex_older_male,i_N_ARTexperienced_bysex_older_female,i_n_women_at_elevatedrisk_15to24,i_n_women_at_elevatedrisk_andonoralPrEP_15to24,i_N_VS_bysex_younger_male,i_N_VS_bysex_younger_female,i_N_VS_bysex_older_male,i_N_VS_bysex_older_female,i_N_newHIVinfections_15plus_male,i_N_newHIVinfections_15plus_female,i_N_newbirths,i_N_newbirths_HIVpos,i_N_deaths_15plus_male,i_N_deaths_15plus_female]]
            #print(year)

            [YLL_15plus_male,YLL_15plus_female,YLL_children_under15,YLL_15plus_male_discounted,YLL_15plus_female_discounted,YLL_children_under15_discounted,n_notonART_byCD4_15plus_gt500,n_notonART_byCD4_15plus_350_500,n_notonART_byCD4_15plus_200_350,n_notonART_byCD4_15plus_lt200,N_HIVneg_in_SD_partnership_M15plus,N_HIVneg_in_SD_partnership_F15plus,N_HIVneg_in_SD_partnership_noART_M15plus,N_HIVneg_in_SD_partnership_noART_F15plus,n_eversex_M15plus,n_eversex_F15plus,n_usedcondomlastact_M15plus,n_usedcondomlastact_F15plus,nonART_M15_24,nonART_F15_24,NawareM15_24,NawareF15_24,n_women_used_oralPrEP_lastQ_15to24,n_women_active_oralPrEP_lastQ_15to24,n_women_ever_oralPrEP_15to24,n_women_used_dapivirinering_lastQ_15to24,n_women_active_dapivirinering_lastQ_15to24,n_women_used_injectablePrEP_lastQ_15to24,n_women_active_injectablePrEP_lastQ_15to24,n_women_used_oralPrEP_lastQ_15plus_sdpartner,n_women_active_oralPrEP_lastQ_15plus_sdpartner,n_women_used_dapivirinering_lastQ_15plus_sdpartner,n_women_active_dapivirinering_lastQ_15plus_sdpartner,n_women_used_injectablePrEP_lastQ_15plus_sdpartner,n_women_active_injectablePrEP_lastQ_15plus_sdpartner,N_firsttime_oralPrEPinitiations_15to24F,N_newHIVdiagnoses_15to24F,N_HIVtests_15to24F] = [float(line.split(",")[index]) for index in [i_YLL_15plus_male,i_YLL_15plus_female,i_YLL_children_under15,i_YLL_15plus_male_discounted,i_YLL_15plus_female_discounted,i_YLL_children_under15_discounted,i_n_notonART_byCD4_15plus_gt500,i_n_notonART_byCD4_15plus_350_500,i_n_notonART_byCD4_15plus_200_350,i_n_notonART_byCD4_15plus_lt200,i_N_HIVneg_in_SD_partnership_M15plus,i_N_HIVneg_in_SD_partnership_F15plus,i_N_HIVneg_in_SD_partnership_noART_M15plus,i_N_HIVneg_in_SD_partnership_noART_F15plus,i_n_eversex_M15plus,i_n_eversex_F15plus,i_n_usedcondomlastact_M15plus,i_n_usedcondomlastact_F15plus,i_nonART_M15_24,i_nonART_F15_24,i_naware_M15_24,i_naware_F15_24,i_n_women_used_oralPrEP_lastQ_15to24,i_n_women_active_oralPrEP_lastQ_15to24,i_n_women_ever_oralPrEP_15to24,i_n_women_used_dapivirinering_lastQ_15to24,i_n_women_active_dapivirinering_lastQ_15to24,i_n_women_used_injectablePrEP_lastQ_15to24,i_n_women_active_injectablePrEP_lastQ_15to24,i_n_women_used_oralPrEP_lastQ_15plus_sdpartner,i_n_women_active_oralPrEP_lastQ_15plus_sdpartner,i_n_women_used_dapivirinering_lastQ_15plus_sdpartner,i_n_women_active_dapivirinering_lastQ_15plus_sdpartner,i_n_women_used_injectablePrEP_lastQ_15plus_sdpartner,i_n_women_active_injectablePrEP_lastQ_15plus_sdpartner,i_N_firsttime_oralPrEPinitiations_15to24F,i_N_newHIVdiagnoses_15to24F,i_N_HIVtests_15to24F]]

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
                
                outputs_N_ART_M15plus[year] = [NonARTM15plus*scale_tot_adult]
                outputs_N_ART_F15plus[year] = [NonARTF15plus*scale_tot_adult]
                outputs_N_ART_child[year] = [art_child*scale_child]
                outputs_N_ART_total[year] = [(NonARTM15plus+NonARTF15plus)*scale_tot_adult + art_child*scale_child]

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
                
                outputs_ARTcoverage_M15plus[year] = [NonARTM15plus/(1.0*NposM15plus+ERR)]

                outputs_ARTcoverage_F15plus[year] = [NonARTF15plus/(1.0*NposF15plus+ERR)]
                
                outputs_ARTcoverage_child[year] = [art_child/(1.0*Npos_child+ERR)]
                outputs_ARTcoverage_total[year] = [(NonARTM15plus+NonARTF15plus+art_child)/(1.0*(NposM15plus+NposF15plus+Npos_child+ERR))]
                outputs_ARTcoverage_F15_24[year] = [nonART_F15_24/(1.0*PosF15_24+ERR)]
                outputs_ARTcoverage_15_24[year]  = [(nonART_M15_24+nonART_F15_24)/(1.0*(PosM15_24+PosF15_24)+ERR)]


                outputs_DiagOnART_M15plus[year] = [NonARTM15plus/(1.0*NawareM15plus+ERR)]

                outputs_DiagOnART_F15plus[year] = [NonARTF15plus/(1.0*NawareF15plus+ERR)]
                outputs_DiagOnART_F15_24[year] = [nonART_F15_24/(1.0*NawareF15_24+ERR)]
                outputs_DiagOnART_15_24[year]  = [(nonART_M15_24+nonART_F15_24)/(1.0*(NawareM15_24+NawareF15_24)+ERR)]
                outputs_DiagOnART_15plus[year] = [(NonARTM15plus+NonARTF15plus)/(1.0*(NawareM15plus+NawareF15plus)+ERR)]
                
                
                #outputs_circ_cumulative15_49[year] = [circ*scale_VMMC] # This is circumicsion. As TMC is rare (and constant over time) the difference in cumulative cirucmcision per year should be roughly VMMC.
                outputs_Ncirc_15_49[year] = [Ncirc_15_49*scale_VMMC]
                outputs_propcirc_15_49[year] = [Ncirc_15_49/(1.0*NpopM15_49)]

                outputs_prop_diagnosed_M15plus[year] = [NawareM15plus/(1.0*NposM15plus+ERR)]

                outputs_prop_diagnosed_F15plus[year] = [NawareF15plus/(1.0*NposF15plus+ERR)]
                outputs_prop_diagnosed_M15_24[year] = [NawareM15_24/(1.0*PosM15_24+ERR)]
                outputs_prop_diagnosed_F15_24[year] = [NawareF15_24/(1.0*PosF15_24+ERR)]
                #outputs_prop_diagnosed_child = {}
                outputs_prop_diagnosed_15plus[year] = [(NawareM15plus+NawareF15plus)/(1.0*(NposM15plus+NposF15plus)+ERR)]
                outputs_prop_F15_24_sex_active_usedcondomlasttime[year] = [N_women_usecondomlastact_15to24/(1.0*N_women_sexuallyactive_15to24)]

                outputs_prop_VS_adult15plus[year] = [(N_VSM15plus+N_VSF15plus)/(1.0*(NonARTM15plus+NonARTF15plus+ERR))]



                ##############################
                ## Added phase 2 stocks:
                ##############################

                outputs_prop_VS_adult15_24[year] = [(N_VS_bysex_younger_male+N_VS_bysex_younger_female)/(1.0*(NonARTM15plus+NonARTF15plus+ERR))]

                outputs_prop_ARTexperienced_M15plus[year] = [NonARTM15plus/(1.0*N_ARTexperienced_bysex_15plus_male+ERR)]
                outputs_prop_ARTexperienced_F15plus[year] = [NonARTF15plus/(1.0*N_ARTexperienced_bysex_15plus_female+ERR)]
                outputs_prop_ARTexperienced_15_24[year] = [(nonART_M15_24+nonART_F15_24)/(1.0*(N_ARTexperienced_bysex_younger_male+N_ARTexperienced_bysex_younger_female+ERR))]
                outputs_prop_ARTexperienced_15plus[year] = [(NonARTM15plus+NonARTF15plus)/(1.0*(N_ARTexperienced_bysex_15plus_male+N_ARTexperienced_bysex_15plus_female+ERR))]

                outputs_N_women_at_elevatedrisk_15to24[year] = [n_women_at_elevatedrisk_15to24*scale_tot_adult]
                outputs_prop_women_at_elevatedrisk_andonPrEP_15to24[year] = [n_women_at_elevatedrisk_andonoralPrEP_15to24/(1.0*n_women_at_elevatedrisk_15to24)]
                outputs_N_women_at_elevatedrisk_andonPrEP_15to24[year] = [n_women_at_elevatedrisk_andonoralPrEP_15to24*scale_tot_adult]


                outputs_n_notonART_byCD4_15plus_gt500[year] = [n_notonART_byCD4_15plus_gt500*scale_tot_adult]
                outputs_n_notonART_byCD4_15plus_350_500[year] = [n_notonART_byCD4_15plus_350_500*scale_tot_adult]
                outputs_n_notonART_byCD4_15plus_200_350[year] = [n_notonART_byCD4_15plus_200_350*scale_tot_adult]
                outputs_n_notonART_byCD4_15plus_50_200[year] = [n_notonART_byCD4_15plus_lt200*0.75*scale_tot_adult]
                outputs_n_notonART_byCD4_15plus_lt50[year] = [n_notonART_byCD4_15plus_lt200*0.25*scale_tot_adult]
                outputs_N_HIVneg_in_SD_partnership_15plus[year] = [(N_HIVneg_in_SD_partnership_M15plus+N_HIVneg_in_SD_partnership_F15plus)*scale_tot_adult]
                outputs_N_HIVneg_in_SD_partnership_F15plus[year] = [N_HIVneg_in_SD_partnership_F15plus*scale_tot_adult]
                outputs_N_HIVneg_in_SD_partnership_noART_15plus[year] = [(N_HIVneg_in_SD_partnership_noART_M15plus+N_HIVneg_in_SD_partnership_noART_F15plus)*scale_tot_adult]
                outputs_N_HIVneg_in_SD_partnership_noART_F15plus[year] = [N_HIVneg_in_SD_partnership_noART_F15plus*scale_tot_adult]
                outputs_prop_eversex_M15plus[year] = [n_eversex_M15plus/(1.0*NpopM15plus)]
                outputs_prop_eversex_F15plus[year] = [n_eversex_F15plus/(1.0*NpopM15plus)]
                outputs_prop_eversex_F15_24[year] = [N_women_sexuallyactive_15to24/(1.0*NpopF15_24)]
                outputs_prop_usedcondomlastact_M15plus[year] = [n_usedcondomlastact_M15plus/(1.0*n_eversex_M15plus)]
                outputs_prop_usedcondomlastact_F15plus[year] = [n_usedcondomlastact_F15plus/(1.0*n_eversex_F15plus)]
                outputs_nonART_M15_24[year] = [nonART_M15_24*scale_tot_adult]
                outputs_nonART_F15_24[year] = [nonART_F15_24*scale_tot_adult]
                outputs_nonART_15_24[year]  = [(nonART_M15_24+nonART_F15_24)*scale_tot_adult]
                outputs_naware_M15_24[year] = [NawareM15_24*scale_tot_adult]
                outputs_naware_F15_24[year] = [NawareF15_24*scale_tot_adult]


                outputs_N_women_used_oralPrEP_lastQ_15to24[year] = [n_women_used_oralPrEP_lastQ_15to24*scale_tot_adult]
                outputs_N_women_active_oralPrEP_lastQ_15to24[year] = [n_women_active_oralPrEP_lastQ_15to24*scale_tot_adult]
                outputs_N_women_ever_oralPrEP_15to24[year] = [n_women_ever_oralPrEP_15to24*scale_tot_adult]
                outputs_N_women_used_dapivirinering_lastQ_15to24[year] = [n_women_used_dapivirinering_lastQ_15to24*scale_tot_adult]
                outputs_N_women_active_dapivirinering_lastQ_15to24[year] = [n_women_active_dapivirinering_lastQ_15to24*scale_tot_adult]
                outputs_N_women_used_injectablePrEP_lastQ_15to24[year] = [n_women_used_injectablePrEP_lastQ_15to24*scale_tot_adult]
                outputs_N_women_active_injectablePrEP_lastQ_15to24[year] = [n_women_active_injectablePrEP_lastQ_15to24*scale_tot_adult]
                outputs_N_women_used_oralPrEP_lastQ_15plus_sdpartner[year] = [n_women_used_oralPrEP_lastQ_15plus_sdpartner*scale_tot_adult]
                outputs_N_women_active_oralPrEP_lastQ_15plus_sdpartner[year] = [n_women_active_oralPrEP_lastQ_15plus_sdpartner*scale_tot_adult]
                outputs_N_women_used_dapivirinering_lastQ_15plus_sdpartner[year] = [n_women_used_dapivirinering_lastQ_15plus_sdpartner*scale_tot_adult]
                outputs_N_women_active_dapivirinering_lastQ_15plus_sdpartner[year] = [n_women_active_dapivirinering_lastQ_15plus_sdpartner*scale_tot_adult]
                outputs_N_women_used_injectablePrEP_lastQ_15plus_sdpartner[year] = [n_women_used_injectablePrEP_lastQ_15plus_sdpartner*scale_tot_adult]
                outputs_N_women_active_injectablePrEP_lastQ_15plus_sdpartner[year] = [n_women_active_injectablePrEP_lastQ_15plus_sdpartner*scale_tot_adult]
                outputs_cumulativeN_firsttime_oralPrEPinitiations_15to24F[year] = [N_firsttime_oralPrEPinitiations_15to24F*scale_tot_adult]


                
                ##############################


                outputs_Ncumulativecases_M15_24[year] = [N_newHIVinfections_15to24_male*scale_tot_adult]
                outputs_Ncumulativecases_M25_49[year] = [N_newHIVinfections_25to49_male*scale_tot_adult]

                outputs_Ncumulativecases_F15_24[year] = [N_newHIVinfections_15to24_female*scale_tot_adult]
                outputs_Ncumulativecases_F25_49[year] = [N_newHIVinfections_25to49_female*scale_tot_adult]

                outputs_Ncumulativecases_M15_49[year] = [(N_newHIVinfections_15to24_male+N_newHIVinfections_25to49_male)*scale_tot_adult]
                outputs_Ncumulativecases_F15_49[year] = [(N_newHIVinfections_15to24_female+N_newHIVinfections_25to49_female)*scale_tot_adult]

                ## Added phase 2:
                outputs_Ncumulativecases_M15plus[year] = [N_newHIVinfections_15plus_male*scale_tot_adult]
                outputs_Ncumulativecases_F15plus[year] = [N_newHIVinfections_15plus_female*scale_tot_adult]

                
                outputs_cumulativeAIDSdeaths_M15plus[year] = [N_AIDSdeaths_15plus_male*scale_tot_adult]
                outputs_cumulativeAIDSdeaths_F15plus[year] = [N_AIDSdeaths_15plus_female*scale_tot_adult]
                outputs_cumulativeAIDSdeaths_child[year] = [N_AIDSdeaths_children_under15*scale_child]
                outputs_cumulativetotaldeaths_M20_59[year] = [N_deaths_20_59_male*scale_tot_adult]
                outputs_cumulativetotaldeaths_F20_59[year] = [N_deaths_20_59_female*scale_tot_adult]


                ## Added phase 2:
                outputs_cumulativetotaldeaths_M15plus[year] = [N_deaths_15plus_male*scale_tot_adult]
                outputs_cumulativetotaldeaths_F15plus[year] = [N_deaths_15plus_female*scale_tot_adult]
                outputs_cumulativeYLL_15plus[year] = [(YLL_15plus_male+YLL_15plus_female)*scale_tot_adult]
                
                outputs_cumulativeYLL_child[year] = [YLL_children_under15*scale_child]
                
                outputs_cumulativeYLL_15plus_discounted[year] = [(YLL_15plus_male_discounted+YLL_15plus_female_discounted)*scale_tot_adult]
                
                outputs_cumulativeYLL_child_discounted[year] = [YLL_children_under15_discounted*scale_child]
                
                outputs_cumulativeNtests_M15plus[year] = [N_HIVtests_15plus_male*scale_tot_adult]
                outputs_cumulativeNtests_F15plus[year] = [N_HIVtests_15plus_female*scale_tot_adult]
                outputs_cumulativeNdiagnoses[year] = [(N_newHIVdiagnoses_15plus_male+N_newHIVdiagnoses_15plus_female)*scale_tot_adult]
                outputs_cumulativeNdiagnoses_M15plus[year] = [N_newHIVdiagnoses_15plus_male*scale_tot_adult]
                outputs_cumulativeNdiagnoses_F15plus[year] = [N_newHIVdiagnoses_15plus_female*scale_tot_adult]
                outputs_cumulativeNdiagnoses_15to24F[year] = [N_newHIVdiagnoses_15to24F*scale_tot_adult]

                outputs_VMMC_cumulative15_49[year] = [N_VMMC_op_cumulative*scale_VMMC]
                outputs_cumulativeNtests_15to24F[year] = [N_HIVtests_15to24F*scale_tot_adult]
                outputs_cumulativeNARTinitiations_15plus[year] = [N_ARTinitiations_15plus*scale_tot_adult]
                outputs_cumulativeNARTreinitiations_15plus[year] = [N_ARTreinitiations_15plus*scale_tot_adult]


                ##############################
                ## Added phase 2 flows:
                ##############################
                outputs_cumulative_newbirths[year] = [N_newbirths*scale_child]
                outputs_cumulative_newbirths_HIVpos[year] = [N_newbirths_HIVpos*scale_child]
                
                
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


                
                outputs_N_ART_M15plus[year] += [NonARTM15plus*scale_tot_adult]
                outputs_N_ART_F15plus[year] += [NonARTF15plus*scale_tot_adult]
                outputs_N_ART_child[year] += [art_child*scale_child]
                outputs_N_ART_total[year] += [(NonARTM15plus+NonARTF15plus)*scale_tot_adult + art_child*scale_child]

                outputs_ARTcoverage_M15plus[year] += [NonARTM15plus/(1.0*NposM15plus+ERR)]
                outputs_ARTcoverage_F15plus[year] += [NonARTF15plus/(1.0*NposF15plus+ERR)]
                outputs_ARTcoverage_child[year] += [art_child/(1.0*Npos_child)]
                outputs_ARTcoverage_total[year] += [(NonARTM15plus+NonARTF15plus+art_child)/(1.0*(NposM15plus+NposF15plus+Npos_child))]
                outputs_ARTcoverage_F15_24[year] += [nonART_F15_24/(1.0*PosF15_24+ERR)]
                outputs_ARTcoverage_15_24[year]  += [(nonART_M15_24+nonART_F15_24)/(1.0*(PosM15_24+PosF15_24)+ERR)]

                outputs_DiagOnART_M15plus[year] += [NonARTM15plus/(1.0*NawareM15plus+ERR)]

                outputs_DiagOnART_F15plus[year] += [NonARTF15plus/(1.0*NawareF15plus+ERR)]

                outputs_DiagOnART_F15_24[year] += [nonART_F15_24/(1.0*NawareF15_24+ERR)]
                outputs_DiagOnART_15_24[year]  += [(nonART_M15_24+nonART_F15_24)/(1.0*(NawareM15_24+NawareF15_24)+ERR)]
                outputs_DiagOnART_15plus[year] += [(NonARTM15plus+NonARTF15plus)/(1.0*(NawareM15plus+NawareF15plus)+ERR)]
                
                outputs_Ncirc_15_49[year] += [Ncirc_15_49*scale_VMMC] 
                outputs_propcirc_15_49[year] += [Ncirc_15_49/(1.0*NpopM15_49)]

                outputs_prop_diagnosed_M15plus[year] += [NawareM15plus/(1.0*NposM15plus+ERR)]
                outputs_prop_diagnosed_F15plus[year] += [NawareF15plus/(1.0*NposF15plus+ERR)]
                outputs_prop_diagnosed_M15_24[year] += [NawareM15_24/(1.0*PosM15_24+ERR)]
                outputs_prop_diagnosed_F15_24[year] += [NawareF15_24/(1.0*PosF15_24+ERR)]
                outputs_prop_diagnosed_15plus[year] += [(NawareM15plus+NawareF15plus)/(1.0*(NposM15plus+NposF15plus)+ERR)]

                outputs_prop_F15_24_sex_active_usedcondomlasttime[year] += [N_women_usecondomlastact_15to24/(1.0*N_women_sexuallyactive_15to24)]

                outputs_prop_VS_adult15plus[year] += [(N_VSM15plus+N_VSF15plus)/(1.0*(NonARTM15plus+NonARTF15plus+ERR))]


                
                ##############################
                ## Added phase 2 stocks:
                ##############################

                outputs_prop_VS_adult15_24[year] += [(N_VS_bysex_younger_male+N_VS_bysex_younger_female)/(1.0*(NonARTM15plus+NonARTF15plus+ERR))]

                outputs_prop_ARTexperienced_M15plus[year] += [NonARTM15plus/(1.0*N_ARTexperienced_bysex_15plus_male+ERR)]
                outputs_prop_ARTexperienced_F15plus[year] += [NonARTF15plus/(1.0*N_ARTexperienced_bysex_15plus_female+ERR)]
                outputs_prop_ARTexperienced_15_24[year] += [(nonART_M15_24+nonART_F15_24)/(1.0*(N_ARTexperienced_bysex_younger_male+N_ARTexperienced_bysex_younger_female+ERR))]
                outputs_prop_ARTexperienced_15plus[year] += [(NonARTM15plus+NonARTF15plus)/(1.0*(N_ARTexperienced_bysex_15plus_male+N_ARTexperienced_bysex_15plus_female+ERR))]


                outputs_N_women_at_elevatedrisk_15to24[year] += [n_women_at_elevatedrisk_15to24*scale_tot_adult]
                outputs_prop_women_at_elevatedrisk_andonPrEP_15to24[year] += [n_women_at_elevatedrisk_andonoralPrEP_15to24/(1.0*n_women_at_elevatedrisk_15to24)]
                outputs_N_women_at_elevatedrisk_andonPrEP_15to24[year] += [n_women_at_elevatedrisk_andonoralPrEP_15to24*scale_tot_adult]

                outputs_n_notonART_byCD4_15plus_gt500[year] += [n_notonART_byCD4_15plus_gt500*scale_tot_adult]
                outputs_n_notonART_byCD4_15plus_350_500[year] += [n_notonART_byCD4_15plus_350_500*scale_tot_adult]
                outputs_n_notonART_byCD4_15plus_200_350[year] += [n_notonART_byCD4_15plus_200_350*scale_tot_adult]
                outputs_n_notonART_byCD4_15plus_50_200[year] += [n_notonART_byCD4_15plus_lt200*0.75*scale_tot_adult]
                outputs_n_notonART_byCD4_15plus_lt50[year] += [n_notonART_byCD4_15plus_lt200*0.25*scale_tot_adult]
                outputs_N_HIVneg_in_SD_partnership_15plus[year] += [(N_HIVneg_in_SD_partnership_M15plus+N_HIVneg_in_SD_partnership_F15plus)*scale_tot_adult]
                outputs_N_HIVneg_in_SD_partnership_F15plus[year] += [N_HIVneg_in_SD_partnership_F15plus*scale_tot_adult]
                outputs_N_HIVneg_in_SD_partnership_noART_15plus[year] += [(N_HIVneg_in_SD_partnership_noART_M15plus+N_HIVneg_in_SD_partnership_noART_F15plus)*scale_tot_adult]
                outputs_N_HIVneg_in_SD_partnership_noART_F15plus[year] += [N_HIVneg_in_SD_partnership_noART_F15plus*scale_tot_adult]
                outputs_prop_eversex_M15plus[year] += [n_eversex_M15plus/(1.0*NpopM15plus)]
                outputs_prop_eversex_F15plus[year] += [n_eversex_F15plus/(1.0*NpopF15plus)]
                outputs_prop_eversex_F15_24[year] += [N_women_sexuallyactive_15to24/(1.0*NpopF15_24)]
                outputs_prop_usedcondomlastact_M15plus[year] += [n_usedcondomlastact_M15plus/(1.0*n_eversex_M15plus)]
                outputs_prop_usedcondomlastact_F15plus[year] += [n_usedcondomlastact_F15plus/(1.0*n_eversex_F15plus)]
                outputs_nonART_M15_24[year] += [nonART_M15_24*scale_tot_adult]
                outputs_nonART_F15_24[year] += [nonART_F15_24*scale_tot_adult]
                outputs_nonART_15_24[year] += [(nonART_M15_24+nonART_F15_24)*scale_tot_adult]
                outputs_naware_M15_24[year] += [NawareM15_24*scale_tot_adult]
                outputs_naware_F15_24[year] += [NawareF15_24*scale_tot_adult]


                outputs_N_women_used_oralPrEP_lastQ_15to24[year] += [n_women_used_oralPrEP_lastQ_15to24*scale_tot_adult]
                outputs_N_women_active_oralPrEP_lastQ_15to24[year] += [n_women_active_oralPrEP_lastQ_15to24*scale_tot_adult]
                outputs_N_women_ever_oralPrEP_15to24[year] += [n_women_ever_oralPrEP_15to24*scale_tot_adult]
                outputs_N_women_used_dapivirinering_lastQ_15to24[year] += [n_women_used_dapivirinering_lastQ_15to24*scale_tot_adult]
                outputs_N_women_active_dapivirinering_lastQ_15to24[year] += [n_women_active_dapivirinering_lastQ_15to24*scale_tot_adult]
                outputs_N_women_used_injectablePrEP_lastQ_15to24[year] += [n_women_used_injectablePrEP_lastQ_15to24*scale_tot_adult]
                outputs_N_women_active_injectablePrEP_lastQ_15to24[year] += [n_women_active_injectablePrEP_lastQ_15to24*scale_tot_adult]
                outputs_N_women_used_oralPrEP_lastQ_15plus_sdpartner[year] += [n_women_used_oralPrEP_lastQ_15plus_sdpartner*scale_tot_adult]
                outputs_N_women_active_oralPrEP_lastQ_15plus_sdpartner[year] += [n_women_active_oralPrEP_lastQ_15plus_sdpartner*scale_tot_adult]
                outputs_N_women_used_dapivirinering_lastQ_15plus_sdpartner[year] += [n_women_used_dapivirinering_lastQ_15plus_sdpartner*scale_tot_adult]
                outputs_N_women_active_dapivirinering_lastQ_15plus_sdpartner[year] += [n_women_active_dapivirinering_lastQ_15plus_sdpartner*scale_tot_adult]
                outputs_N_women_used_injectablePrEP_lastQ_15plus_sdpartner[year] += [n_women_used_injectablePrEP_lastQ_15plus_sdpartner*scale_tot_adult]
                outputs_N_women_active_injectablePrEP_lastQ_15plus_sdpartner[year] += [n_women_active_injectablePrEP_lastQ_15plus_sdpartner*scale_tot_adult]
                outputs_cumulativeN_firsttime_oralPrEPinitiations_15to24F[year] += [N_firsttime_oralPrEPinitiations_15to24F*scale_tot_adult]
                
                ### Flow measures:
                ##############################

                outputs_Ncumulativecases_M15_24[year] += [N_newHIVinfections_15to24_male*scale_tot_adult]
                outputs_Ncumulativecases_M25_49[year] += [N_newHIVinfections_25to49_male*scale_tot_adult]
                outputs_Ncumulativecases_M15_49[year] += [(N_newHIVinfections_15to24_male+N_newHIVinfections_25to49_male)*scale_tot_adult]
                
                outputs_Ncumulativecases_F15_24[year] += [N_newHIVinfections_15to24_female*scale_tot_adult]
                outputs_Ncumulativecases_F25_49[year] += [N_newHIVinfections_25to49_female*scale_tot_adult]
                outputs_Ncumulativecases_F15_49[year] += [(N_newHIVinfections_15to24_female+N_newHIVinfections_25to49_female)*scale_tot_adult]

                ## Added phase 2:
                outputs_Ncumulativecases_M15plus[year] += [N_newHIVinfections_15plus_male*scale_tot_adult]
                outputs_Ncumulativecases_F15plus[year] += [N_newHIVinfections_15plus_female*scale_tot_adult]


                outputs_cumulativeAIDSdeaths_M15plus[year] += [N_AIDSdeaths_15plus_male*scale_tot_adult]
                outputs_cumulativeAIDSdeaths_F15plus[year] += [N_AIDSdeaths_15plus_female*scale_tot_adult]
                outputs_cumulativeAIDSdeaths_child[year] += [N_AIDSdeaths_children_under15*scale_child]
                outputs_cumulativetotaldeaths_M20_59[year] += [N_deaths_20_59_male*scale_tot_adult]
                outputs_cumulativetotaldeaths_F20_59[year] += [N_deaths_20_59_female*scale_tot_adult]

                ## Added phase 2:
                outputs_cumulativetotaldeaths_M15plus[year] += [N_deaths_15plus_male*scale_tot_adult]
                outputs_cumulativetotaldeaths_F15plus[year] += [N_deaths_15plus_female*scale_tot_adult]
                outputs_cumulativeYLL_15plus[year] += [(YLL_15plus_male+YLL_15plus_female)*scale_tot_adult]
                outputs_cumulativeYLL_child[year] += [YLL_children_under15*scale_child]
                outputs_cumulativeYLL_15plus_discounted[year] += [(YLL_15plus_male_discounted+YLL_15plus_female_discounted)*scale_tot_adult]
                
                outputs_cumulativeYLL_child_discounted[year] += [YLL_children_under15_discounted*scale_child]
                
                outputs_cumulativeNtests_M15plus[year] += [N_HIVtests_15plus_male*scale_tot_adult]
                outputs_cumulativeNtests_F15plus[year] += [N_HIVtests_15plus_female*scale_tot_adult]
                outputs_cumulativeNdiagnoses[year] += [(N_newHIVdiagnoses_15plus_male+N_newHIVdiagnoses_15plus_female)*scale_tot_adult]
                outputs_cumulativeNdiagnoses_M15plus[year] += [N_newHIVdiagnoses_15plus_male*scale_tot_adult]
                outputs_cumulativeNdiagnoses_F15plus[year] += [N_newHIVdiagnoses_15plus_female*scale_tot_adult]
                outputs_cumulativeNdiagnoses_15to24F[year] += [N_newHIVdiagnoses_15to24F*scale_tot_adult]

                outputs_VMMC_cumulative15_49[year] += [N_VMMC_op_cumulative*scale_VMMC]
                outputs_cumulativeNtests_15to24F[year] += [N_HIVtests_15to24F*scale_tot_adult]

                outputs_cumulativeNARTinitiations_15plus[year] += [N_ARTinitiations_15plus*scale_tot_adult]
                outputs_cumulativeNARTreinitiations_15plus[year] += [N_ARTreinitiations_15plus*scale_tot_adult]

                ##############################
                ## Added phase 2 flows:
                ##############################
                outputs_cumulative_newbirths[year] += [N_newbirths*scale_child]
                outputs_cumulative_newbirths_HIVpos[year] += [N_newbirths_HIVpos*scale_child]




    ##################################################################
    # Now make annual outputs from cumulative ones:
    ##################################################################

    outputs_Nincidentcases_M15_49 = get_annual_from_cumulative(outputs_Ncumulativecases_M15_49)
    outputs_Nincidentcases_M15_24 = get_annual_from_cumulative(outputs_Ncumulativecases_M15_24)
    outputs_Nincidentcases_M25_49 = get_annual_from_cumulative(outputs_Ncumulativecases_M25_49)
    outputs_Nincidentcases_F15_49 = get_annual_from_cumulative(outputs_Ncumulativecases_F15_49)
    outputs_Nincidentcases_F15_24 = get_annual_from_cumulative(outputs_Ncumulativecases_F15_24)
    outputs_Nincidentcases_F25_49 = get_annual_from_cumulative(outputs_Ncumulativecases_F25_49)

    ## Added phase 2:
    outputs_Nincidentcases_M15plus = get_annual_from_cumulative(outputs_Ncumulativecases_M15plus)
    outputs_Nincidentcases_F15plus = get_annual_from_cumulative(outputs_Ncumulativecases_F15plus)
    

    
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


    
    ## Added phase 2:
    outputs_totaldeaths_M15plus = get_annual_from_cumulative(outputs_cumulativetotaldeaths_M15plus)
    outputs_totaldeaths_F15plus = get_annual_from_cumulative(outputs_cumulativetotaldeaths_F15plus)
    outputs_YLL_15plus = get_annual_from_cumulative(outputs_cumulativeYLL_15plus)
    outputs_YLL_child = get_annual_from_cumulative(outputs_cumulativeYLL_child)

    outputs_YLL_15plus_discounted = get_annual_from_cumulative(outputs_cumulativeYLL_15plus_discounted)
    outputs_YLL_child_discounted = get_annual_from_cumulative(outputs_cumulativeYLL_child_discounted)

    

    outputs_Ntests_M15plus = get_annual_from_cumulative(outputs_cumulativeNtests_M15plus)
    outputs_Ntests_F15plus = get_annual_from_cumulative(outputs_cumulativeNtests_F15plus)
    outputs_Ntests_adult15plus = sum_two_outputs(outputs_Ntests_M15plus,outputs_Ntests_F15plus)
    outputs_Ntests_15to24F = get_annual_from_cumulative(outputs_cumulativeNtests_15to24F)
    outputs_annualNdiagnoses = get_annual_from_cumulative(outputs_cumulativeNdiagnoses)
    outputs_annualNdiagnoses_M15plus = get_annual_from_cumulative(outputs_cumulativeNdiagnoses_M15plus)
    outputs_annualNdiagnoses_F15plus = get_annual_from_cumulative(outputs_cumulativeNdiagnoses_F15plus)
    outputs_annualNdiagnoses_15to24F = get_annual_from_cumulative(outputs_cumulativeNdiagnoses_15to24F)

    outputs_annualNARTinitiations_15plus = get_annual_from_cumulative(outputs_cumulativeNARTinitiations_15plus)
    outputs_annualNARTreinitiations_15plus = get_annual_from_cumulative(outputs_cumulativeNARTreinitiations_15plus)


    outputs_VMMC_annual15_49 = get_annual_from_cumulative(outputs_VMMC_cumulative15_49)
    
    outputs_Ntests_adult15plus = sum_two_outputs(outputs_Ntests_M15plus,outputs_Ntests_F15plus)

    outputs_proportion_tests_pos_15plus = get_quotient(outputs_annualNdiagnoses,outputs_Ntests_adult15plus,ERR)
    outputs_proportion_tests_pos_M15plus = get_quotient(outputs_annualNdiagnoses_M15plus,outputs_Ntests_M15plus,ERR)
    outputs_proportion_tests_pos_F15plus = get_quotient(outputs_annualNdiagnoses_F15plus,outputs_Ntests_M15plus,ERR)

    outputs_proportion_tests_pos_15to24F = get_quotient(outputs_annualNdiagnoses_15to24F,outputs_Ntests_15to24F,ERR)

    outputs_annual_N_firsttime_oralPrEPinitiations_15to24F = get_annual_from_cumulative(outputs_cumulativeN_firsttime_oralPrEPinitiations_15to24F)
    outputs_quarterly_N_firsttime_oralPrEPinitiations_15to24F = get_quarterly_from_annual(outputs_annual_N_firsttime_oralPrEPinitiations_15to24F)


    ##############################
    ## Added phase 2 flows:
    ##############################
    outputs_newbirths = get_annual_from_cumulative(outputs_cumulative_newbirths)
    outputs_newbirths_HIVpos = get_annual_from_cumulative(outputs_cumulative_newbirths_HIVpos)
    
    ## Now make annual number of VMMC:
    #outputs_circ=get_annual_from_cumulative(outputs_circ_cumulative15_49)

    outdir = "checks/"
    if(not(os.path.isdir(outdir))):
        try:
            os.makedirs(outdir)
        except:
            print(f"Error - need to make directory {outdir}")
            sys.exit()


    # I have validated these by hand against MIHPSA_output_CL05_Zim_patch0_Rand1_Run3_0.csv (this run is column H in each of the csv's below)
    validate=0
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
                        "ARTcoverage_F_15_24":outputs_ARTcoverage_F15_24,
                        "ARTcoverage_15_24":outputs_ARTcoverage_15_24,
                        "Diagnosed_onART_M_15plus":outputs_DiagOnART_M15plus,
                        "Diagnosed_onART_F_15plus":outputs_DiagOnART_F15plus,
                        "Diagnosed_onART_F_15_24":outputs_DiagOnART_F15_24,
                        "Diagnosed_onART_15_24":outputs_DiagOnART_15_24,
                        "Diagnosed_onART_15plus":outputs_DiagOnART_15plus,


                        "N_VMMC_annual_15_49":outputs_VMMC_annual15_49,
                        "N_circ_15_49":outputs_Ncirc_15_49,
                        "prop_circ_15_49":outputs_propcirc_15_49,
                        "PropDiagnosed_M15plus":outputs_prop_diagnosed_M15plus,
                        "PropDiagnosed_F15plus":outputs_prop_diagnosed_F15plus,
                        "PropDiagnosed_M15_24":outputs_prop_diagnosed_M15_24,
                        "PropDiagnosed_F15_24":outputs_prop_diagnosed_F15_24,
                        "PropDiagnosed_15plus":outputs_prop_diagnosed_15plus,
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
                        "Ntests_total15plus":outputs_Ntests_adult15plus,
                        "Ntests_adult15plus":outputs_Ntests_adult15plus,
                        "Prop_tests_pos_15plus":outputs_proportion_tests_pos_15plus,
                        "Prop_tests_pos_M15plus":outputs_proportion_tests_pos_M15plus,
                        "Prop_tests_pos_F15plus":outputs_proportion_tests_pos_F15plus,
                        "Prop_tests_pos_15to24F":outputs_proportion_tests_pos_15to24F,
                        "Npos_M15plus":outputs_Npos_M15plus,
                        "Npos_F15plus":outputs_Npos_F15plus,
                        "Npos_M15_24":outputs_Npos_M15_24,
                        "Npos_F15_24":outputs_Npos_F15_24,
                        "Npos_M25_49":outputs_Npos_M25_49,
                        "Npos_F25_49":outputs_Npos_F25_49,
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
                        "Npop_F25_49":outputs_Npop_F25_49,
                        "prop_ARTexperienced_M15plus":outputs_prop_ARTexperienced_M15plus,
                        "prop_ARTexperienced_F15plus":outputs_prop_ARTexperienced_F15plus,
                        "prop_ARTexperienced_15_24":outputs_prop_ARTexperienced_15_24,
                        "prop_ARTexperienced_15plus":outputs_prop_ARTexperienced_15plus,
                        "N_women_at_elevatedrisk_15to24":outputs_N_women_at_elevatedrisk_15to24,
                        "prop_women_at_elevatedrisk_andonPrEP_15to24":outputs_prop_women_at_elevatedrisk_andonPrEP_15to24,
                        "N_women_at_elevatedrisk_andonPrEP_15to24":outputs_N_women_at_elevatedrisk_andonPrEP_15to24,
                        "prop_VS_adult15_24":outputs_prop_VS_adult15_24,
                        "Nincidentcases_M15plus":outputs_Nincidentcases_M15plus,
                        "Nincidentcases_F15plus":outputs_Nincidentcases_F15plus,
                        "newbirths":outputs_newbirths,
                        "newbirths_HIVpos":outputs_newbirths_HIVpos,
                        "totaldeaths_M15plus":outputs_totaldeaths_M15plus,
                        "totaldeaths_F15plus":outputs_totaldeaths_F15plus,
                        "YLL_15plus":outputs_YLL_15plus,
                        "YLL_child":outputs_YLL_child,
                        "YLL_15plus_discounted":outputs_YLL_15plus_discounted,
                        "YLL_child_discounted":outputs_YLL_child_discounted,
                        "n_notonART_byCD4_15plus_gt500":outputs_n_notonART_byCD4_15plus_gt500,
                        "n_notonART_byCD4_15plus_350_500":outputs_n_notonART_byCD4_15plus_350_500,
                        "n_notonART_byCD4_15plus_200_350":outputs_n_notonART_byCD4_15plus_200_350,
                        "n_notonART_byCD4_15plus_50_200":outputs_n_notonART_byCD4_15plus_50_200,
                        "n_notonART_byCD4_15plus_lt50":outputs_n_notonART_byCD4_15plus_lt50,
                        "N_HIVneg_in_SD_partnership_15plus":outputs_N_HIVneg_in_SD_partnership_15plus,
                        "N_HIVneg_in_SD_partnership_F15plus":outputs_N_HIVneg_in_SD_partnership_F15plus,
                        "N_HIVneg_in_SD_partnership_noART_15plus":outputs_N_HIVneg_in_SD_partnership_noART_15plus,
                        "N_HIVneg_in_SD_partnership_noART_F15plus":outputs_N_HIVneg_in_SD_partnership_noART_F15plus,
                        "prop_eversex_M15plus":outputs_prop_eversex_M15plus,
                        "prop_eversex_F15plus":outputs_prop_eversex_F15plus,
                        "prop_eversex_F15_24":outputs_prop_eversex_F15_24,
                        "prop_usedcondomlastact_M15plus":outputs_prop_usedcondomlastact_M15plus,
                        "prop_usedcondomlastact_F15plus":outputs_prop_usedcondomlastact_F15plus,
                        "nonART_M15_24":outputs_nonART_M15_24,
                        "nonART_F15_24":outputs_nonART_F15_24,
                        "nonART_15_24":outputs_nonART_15_24,
                        "naware_M15_24":outputs_naware_M15_24,
                        "naware_F15_24":outputs_naware_F15_24,

                        "N_women_used_oralPrEP_lastQ_15to24":outputs_N_women_used_oralPrEP_lastQ_15to24,
                        "N_women_active_oralPrEP_lastQ_15to24":outputs_N_women_active_oralPrEP_lastQ_15to24,
                        "N_women_ever_oralPrEP_15to24":outputs_N_women_ever_oralPrEP_15to24,
                        "N_women_used_dapivirinering_lastQ_15to24":outputs_N_women_used_dapivirinering_lastQ_15to24,
                        "N_women_active_dapivirinering_lastQ_15to24":outputs_N_women_active_dapivirinering_lastQ_15to24,
                        "N_women_used_injectablePrEP_lastQ_15to24":outputs_N_women_used_injectablePrEP_lastQ_15to24,
                        "N_women_active_injectablePrEP_lastQ_15to24":outputs_N_women_active_injectablePrEP_lastQ_15to24,
                        "N_women_used_oralPrEP_lastQ_15plus_sdpartner":outputs_N_women_used_oralPrEP_lastQ_15plus_sdpartner,
                        "N_women_active_oralPrEP_lastQ_15plus_sdpartner":outputs_N_women_active_oralPrEP_lastQ_15plus_sdpartner,
                        "N_women_used_dapivirinering_lastQ_15plus_sdpartner":outputs_N_women_used_dapivirinering_lastQ_15plus_sdpartner,
                        "N_women_active_dapivirinering_lastQ_15plus_sdpartner":outputs_N_women_active_dapivirinering_lastQ_15plus_sdpartner,
                        "N_women_used_injectablePrEP_lastQ_15plus_sdpartner":outputs_N_women_used_injectablePrEP_lastQ_15plus_sdpartner,
                        "N_women_active_injectablePrEP_lastQ_15plus_sdpartner":outputs_N_women_active_injectablePrEP_lastQ_15plus_sdpartner,
                        "N_firsttime_oralPrEPinitiations_lastQ_15to24F":outputs_quarterly_N_firsttime_oralPrEPinitiations_15to24F,
                        "N_annualNARTinitiations_15plus":outputs_annualNARTinitiations_15plus,
                        "N_annualNARTreinitiations_15plus":outputs_annualNARTreinitiations_15plus
    }





    ##Removed in phase 2:
    #"Npop15_49","Npop_total","Npos_total","totaldeaths_M20_59","totaldeaths_F20_59","totaldeaths_adult20_59","Ntests_M15plus","Ntests_F15plus","Ntests_adult15plus",

    # list_of_outputs = ["PrevalenceM15_49","PrevalenceF15_49","PrevalenceAll15_49","PrevalenceF15_24",
    #                    "Npop_M15plus","Npop_F15plus","Npop_15plus","Npop_child",
    #                    "Npop_M15_24","Npop_F15_24","Npop_M25_49","Npop_F25_49",
    #                    "N_HIVneg_in_SD_partnership_15plus",
    #                    "N_HIVneg_in_SD_partnership_noART_15plus",
    #                    "N_HIVneg_in_SD_partnership_F15plus",
    #                    "N_HIVneg_in_SD_partnership_noART_F15plus",
    #                    "Npos_M15plus","Npos_F15plus","Npos_child",
    #                    "Npos_M15_24","Npos_F15_24","Npos_M25_49","Npos_F25_49",
    #                     "n_notonART_byCD4_15plus_gt500","n_notonART_byCD4_15plus_350_500","n_notonART_byCD4_15plus_200_350","n_notonART_byCD4_15plus_50_200","n_notonART_byCD4_15plus_lt50",
    #                    "PropDiagnosed_15plus","PropDiagnosed_M15plus","PropDiagnosed_F15plus",
    #                    "PropDiagnosed_M15_24","PropDiagnosed_F15_24",
    #                    "prop_eversex_M15plus","prop_eversex_F15plus","prop_eversex_F15_24",
    #                    "prop_usedcondomlastact_M15plus","prop_usedcondomlastact_F15plus","PropF15_24_condlasttime",
    #                    "N_women_at_elevatedrisk_15to24","prop_women_at_elevatedrisk_andonPrEP_15to24",
    #                    "prop_circ_15_49",
    #                    "N_ART_M_15plus","N_ART_F_15plus","nonART_15_24","N_ART_total","N_ART_child",
    #                    "Diagnosed_onART_M_15plus","Diagnosed_onART_F_15plus",
    #                    "Diagnosed_onART_F_15_24","Diagnosed_onART_15_24","Diagnosed_onART_15plus",

    #                    "ARTcoverage_M_15plus","ARTcoverage_F_15plus",
    #                    "ARTcoverage_F_15_24","ARTcoverage_15_24",
    #                    "ARTcoverage_total","ARTcoverage_child",
    #                    "prop_ARTexperienced_M15plus","prop_ARTexperienced_F15plus","prop_ARTexperienced_15_24","prop_ARTexperienced_15plus",
    #                    "PropAdultVS","prop_VS_adult15_24",

    #                    ## Flows:
    #                    "newbirths","newbirths_HIVpos",
    #                    "IncidenceM15_49","IncidenceF15_49","Incidencetotal15_49","IncidenceF15_24",
    #                    "Nincidentcases_M15plus","Nincidentcases_F15plus",
    #                    "New_cases_M15_49","New_cases_F15_49","New_cases_total15_49",
    #                    "New_cases_M15_24","New_cases_F15_24","New_cases_M25_49","New_cases_F25_49", 
    #                    "AIDSdeaths_M15plus","AIDSdeaths_F15plus","AIDSdeaths_total","AIDSdeaths_child",
    #                    "totaldeaths_M15plus","totaldeaths_F15plus",
    #                    "YLL_15plus","YLL_child",

    #                     "Prop_tests_pos_15plus","Prop_tests_pos_M15plus","Prop_tests_pos_F15plus",
                       
    #                    "N_VMMC_annual_15_49",
                       
    #                    "N_women_at_elevatedrisk_andonPrEP_15to24"
    # ]
                        

    #,"Prevalence_child"
    #print(outputs_to_store["prop_ARTexperienced_M15plus"])
    #print(outputs_to_store["New_cases_F25_49"])

    outputs_summary_stats = make_mean_CI_andstore(outputs_to_store)
    return(outputs_summary_stats)



## Function takes the stock or flow "dictionaries" in Vale's Excel spreadsheet and pulls out the following:
## var_outputs: a python dictionary of Vale's variable name (hereby denoted valevarname) and the outputs required (either "All"=Median+95% CrI or "Mean"=Median only.
## ordered_var_list: a list of valevarname in the order they appear.
def function_get_clean_varlist_and_outputs(varlist):
    i=0
    var_outputs = {}
    ordered_var_list = []
    nvar=len(varlist)
    while(i<nvar):
        if(varlist[i][-2:]=="_M"):
            if(i<(nvar-2)):
                if((varlist[i+1][-5:]=="_95LL") and (varlist[i+2][-5:]=="_95UL")):
                    ordered_var_list += [varlist[i]]
                    #print(varlist[i])
                    var_outputs[varlist[i]]="All"
                    i = i+3
                    # Next one is another mean:
                elif(varlist[i+1][-2:]=="_M"):
                    ordered_var_list += [varlist[i]]                
                    #print(varlist[i])
                    var_outputs[varlist[i]]="Median"
                    i = i+1
                elif((varlist[i+1][-4:]=="_95L") and (varlist[i+2][-5:]=="_95UL")):
                    ordered_var_list += [varlist[i]]                
                    #print(varlist[i])
                    var_outputs[varlist[i]]="All"
                    i = i+3
                elif((varlist[i+1]=="NHIV_FSW1599_LL") and (varlist[i+2]=="NHIV_FSW1599_UL")):
                    ordered_var_list += [varlist[i]]
                    #print(varlist[i])
                    var_outputs[varlist[i]]="All"
                    i = i+3
                else:
                    print("Error - variables don't fit format. Exiting\n")
                    print(varlist[i],varlist[i+1],varlist[i+2])
                    sys.exit(1)
            elif(i<nvar):
                if(varlist[i][-2:]=="_M"):
                    ordered_var_list += [varlist[i]]
                    #print(varlist[i])
                    var_outputs[varlist[i]]="Median"
                    i = i+1
                else:
                    print("Help1!")
                    print(i,nvar)
                    print(varlist[i+1])
                    sys.exit(1)
                    
            else:
                print("Help2!")
                print(i,nvar)
                print(varlist[i])
                sys.exit(1)
        elif(varlist[i].rstrip()=="We refer to the number of test episode not number of test kits"):
            i = i+1
        else:
            print("Help3!")
            print(i,nvar)
            print(varlist[i]+"X")
            sys.exit(1)
                    

    return [var_outputs, ordered_var_list]

    
####################################################################
## Dictionaries:
####################################################################

## Flow variables (e.g. incidence):
## Convert between Vale's and my variables.
## "X" means I don't have it as an output right now.
flow_variable_dictionary = {"NAlive_Fbirth1599_M":"X",
"NHIV_Fbirth1599_M":"X",
"NAlive_FbirthBF1599_M":"X",
"NHIV_FbirthBF1599_M":"X",
"NAlive_FpregEverBirth1524_M":"X",
"NHIV_FpregEverBirth1524_M":"X",
"NAlive_A01_M":"newbirths",
"NAlive_HIVPOSmum_A01_M":"X",
"NHIV_HIVPOSmum_A01_M":"newbirths_HIVpos",
"HIVIncid_M1549_M":"IncidenceM15_49",
"HIVIncid_F1549_M":"IncidenceF15_49",
"HIVIncid_A1549_M":"Incidencetotal15_49",
"HIVIncid_F1524_M":"IncidenceF15_24",
"HIVIncid_FSW1599_M":"X",
"HIVIncid_SDCA1599_M":"X", ## Incidence in 15+ with HIV+ partner.
"HIVIncid_SDCF1599_M":"X",
"HIVIncid_MSM1599_M":"X",
"HIVIncid_pregbfF1549_M":"X",
"HIVIncid_occA1599_M":"X",
"HIVIncid_gbvF1599_M":"X",
"NHIVInf_M1599_M":"Nincidentcases_M15plus",
"NHIVInf_F1599_M":"Nincidentcases_F15plus",
"NHIVInf_A014_M":"X",
"NHIVInf_M1549_M":"New_cases_M15_49",
"NHIVInf_F1549_M":"New_cases_F15_49",
"NHIVInf_A1549_M":"New_cases_total15_49",
"NHIVInf_M1524_M":"New_cases_M15_24",
"NHIVInf_F1524_M":"New_cases_F15_24",
"NHIVInf_M2549_M":"New_cases_M25_49",
"NHIVInf_F2549_M":"New_cases_F25_49",
"AIDSDeaths_M1599_M":"AIDSdeaths_M15plus",
"AIDSDeaths_F1599_M":"AIDSdeaths_F15plus",
"AIDSDeaths_A1599_M":"AIDSdeaths_total",
"AIDSDeaths_A014_M":"X",  ## In future use AIDSdeaths_child
"TOTDeaths_M1599_M":"totaldeaths_M15plus",
"TOTDeaths_F1599_M":"totaldeaths_F15plus",
"TOTDeaths_A014_M":"X",
"YLL_AgeGenLifeExpect_A1599_M":"YLL_15plus",
"YLL_AgeGenLifeExpect_A014_M":"X",
"YLL_AgeGenLifeExpect_3Disc_A1599_M":"YLL_15plus_discounted",
"YLL_AgeGenLifeExpect_3Disc_A014_M":"X",
"Ntested_ANCPD_F1599_M":"X",
"Ntests_ANCPD_F1599_M":"X",
"Ntested_A06m_M":"X",
"Ntested_EndBF_Inf_M":"X",
"NHIVST_PD_M1599_M":"X",
"NHIVST_PD_F1599_M":"X",
"NHIVST_SDNP_M1599_M":"X",
"NHIVST_SDNP_F1599_M":"X",
"NHIVST_SDPARTNER_M1599_M":"X",
"NHIVST_SDPARTNER_F1599_M":"X",
"Ntests_FACSYMPT_M1599_M":"X",
"Ntests_FACSYMPT_F1599_M":"X",
"Ntests_FACNOSYMPT_M1599_M":"X",
"Ntests_FACNOSYMPT_F1599_M":"X",
"Ntests_FAC_A014_M":"X",
"Ntests_IndexFAC_M1599_M":"X",
"Ntests_IndexFAC_F1599_M":"X",
"Ntests_RecInf_M1599_M":"X",
"Ntests_RecInf_F1599_M":"X",
"Ntests_COM_M1599_M":"X",
"Ntests_COM_F1599_M":"X",
"Ntested_FSWprog_FSW1599_M":"X",
"Ntests_FSW1599_M":"X",
"Ntested_MSMprog_MSM1599_M":"X",
"Ntests_MSM1599_M":"X",
"Ntested_TGprog_TG1599_M":"X",
"Ntests_TG1599_M":"X",
"TOTTests_M1599_M":"Ntests_M15plus",
"TOTTests_F1599_M":"Ntests_F15plus",
"TOTTests_A1599_M":"Ntests_total15plus",
"TOTTests_A014_M":"X",
"TOTHIVST_M1599_M":"X",
"TOTHIVST_F1599_M":"X",
"TOTHIVST_A014_M":"X",
"NPosTests_ANCPD_F1599_M":"X",
"NPostTest_A06m_M":"X",
"NPosTests_EndBF_Inf_M":"X",
"NPosConfHIVST_PD_M1599_M":"X",
"NPosConfHIVST_PD_F1599_M":"X",
"NPosConfHIVST_SDNP_M1599_M":"X",
"NPosConfHIVST_SDNP_F1599_M":"X",
"NPosConfHIVST_SDPARTNER_M1599_M":"X",
"NPosConfHIVST_SDPARTNER_F1599_M":"X",
"NPosTests_FAC_M1599_M":"X",
"NPosTests_FAC_F1599_M":"X",
"NPosTests_FAC_A014_M":"X",
"NPosTests_IndexFAC_M1599_M":"X",
"NPosTests_IndexFAC_F1599_M":"X",
"NPosTests_RecInf_M1599_M":"X",
"NPosTests_RecInf_F1599_M":"X",
"NPosTests_COM_M1599_M":"X",
"NPosTests_COM_F1599_M":"X",
"NPosTests_FSWprog_FSW1599_M":"X",
"NPosTests_FSW1599_M":"X",
"NPosTests_MSMprog_MSM1599_M":"X",
"NPosTests_MSM1599_M":"X",
"NPosTests_Tgprog_TG1599Tested_M":"X",
"NPosTests_TG1599_M":"X",
"TOTPosTests_M1599_M":"X",
"TOTPosTests_F1599_M":"X",
"TOTPosTests_A014_M":"X",
"TOTPosConfHIVST_M1599_M":"X",
"TOTPosConfHIVST_F1599_M":"X",
"PosRate_M1599_M":"Prop_tests_pos_M15plus",
"PosRate_F1599_M":"Prop_tests_pos_F15plus",
"PosRate_A1599_M":"Prop_tests_pos_15plus",
"PosRate_F1524_M":"Prop_tests_pos_15to24F",  ## Just added
"PosRate_FSW1599_M":"X",
"PosRate_MSM1529_M":"X",
"NDREAMS_F1524_M":"X",
"NDREAMSEver_F1524_M":"X",
"NDREAMS_NEGF1524_M":"X",
"NDREAMSEver_NEGF1524_M":"X",
"NFSWprog_FSW1599_M":"X",
"NFSWprogEver_FSW1599_M":"X",
"NMSMprog_MSM1599_M":"X",
"NMSMprogEver_MSM1599_M":"X",
"NSBCC_A1599_M":"X",
"NUEU_A1599_M":"X",
"NCUPP_A1599_M":"X",
"NCondoms_A1599_M":"X",
"NGPMHC_DiagM1599_M":"X",
"NGPMHC_M1599_M":"X",
"NVMMC_M1549_M":"N_VMMC_annual_15_49",
"NTDFPrEPinit_F1524_M":"N_firsttime_oralPrEPinitiations_lastQ_15to24F",
"NTDFPrEP_F1524_M":"N_women_used_oralPrEP_lastQ_15to24",
"NTDFPrEPCT_F1524_M":"N_women_active_oralPrEP_lastQ_15to24", 
"NTDFPrEPEver_F1524_M":"N_women_ever_oralPrEP_15to24",
"NTDFPrEPinit_FSW1599_M":"X",
"NTDFPrEP_FSW1599_M":"X",
"NTDFPrEPCT_FSW1599_M":"X",
"NTDFPrEPEver_FSW1599_M":"X",
"NTDFPrEPinit_SDCA1599_M":"X",
"NTDFPrEP_SDCA1599_M":"X",
"NTDFPrEPCT_SDCA1599_M":"X",
"NTDFPrEPEver_SDCA1599_M":"X",
"NTDFPrEPinit_MSM1599_M":"X",
"NTDFPrEP_MSM1599_M":"X",
"NTDFPrEPCT_MSM1599_M":"X",
"NTDFPrEPEver_MSM1599_M":"X",
"NTDFPrEPinit_pregbfF1549_M":"X",
"NTDFPrEP_pregbfF1549_M":"X",
"NTDFPrEPCT_pregbfF1549_M":"X",
"NTDFPrEPEver_pregbfF1549_M":"X",
"NDPVPrEPinit_F1524_M":"X",
"NDPVPrEP_F1524_M":"N_women_used_dapivirinering_lastQ_15to24",
"NDPVPrEPCT_F1524_M":"N_women_active_dapivirinering_lastQ_15to24",
"NDPVPrEPEver_F1524_M":"X",
"NDPVPrEPinit_FSW1599_M":"X",
"NDPVPrEP_FSW1599_M":"X",
"NDPVPrEPCT_FSW1599_M":"X",
"NDPVPrEPEver_FSW1599_M":"X",
"NDPVPrEPinit_SDCF1599_M":"X",
"NDPVPrEP_SDCF1599_M":"X",
"NDPVPrEPCT_SDCF1599_M":"X",
"NDPVPrEPEver_SDCF1599_M":"X",
"NDPVPrEPinit_pregbfF1549_M":"X",
"NDPVPrEP_pregbfF1549_M":"X",
"NDPVPrEPCT_pregbfF1549_M":"X",
"NDPVPrEPEver_pregbfF1549_M":"X",                            
"NCABPrEPinit_F1524_M":"X",
"NCABPrEP_F1524_M":"N_women_used_injectablePrEP_lastQ_15to24",
"NCABPrEPCT_F1524_M":"N_women_active_injectablePrEP_lastQ_15to24",
"NCABPrEPEver_F1524_M":"X",
"NCABPrEPinit_FSW1599_M":"X",
"NCABPrEP_FSW1599_M":"X",
"NCABPrEPCT_FSW1599_M":"X",
"NCABPrEPEver_FSW1599_M":"X",
"NCABPrEPinit_SDCA1599_M":"X",
"NCABPrEP_SDCA1599_M":"X",
"NCABPrEPCT_SDCA1599_M":"X",
"NCABPrEPEver_SDCA1599_M":"X",
"NCABPrEPinit_MSM1599_M":"X",
"NCABPrEP_MSM1599_M":"X",
"NCABPrEPCT_MSM1599_M":"X",
"NCABPrEPEver_MSM1599_M":"X",
"NCABPrEPinit_pregbfF1549_M":"X",
"NCABPrEP_pregbfF1549_M":"X",
"NCABPrEPCT_pregbfF1549_M":"X",
"NCABPrEPEver_pregbfF1549_M":"X",
"NPEPocc_A1599_M":"X",
"NPEPoccEver_A1599_M":"X",
"NPEPgbv_F1599_M":"X",
"NPEPgbvEver_F1599_M":"X",
"NPMTCT_FbirthHIV1599_M":"X",
"NARTinit_A1599_M":"N_annualNARTinitiations_15plus",   ## Just addded
"NARTreinit_A1599_M":"N_annualNARTreinitiations_15plus",
"NTreatFail_A1599_M":"X",
"N_A1599_CD4_M":"X",
"NCD4_A1599_M":"X",
"NMCD4lt350_A1599_M":"X",
"NMCD4lt200_A1599_M":"X",
"N_CTX_A1599_M":"X",
"N_CTX_A014_M":"X",
"NAHD_A1599_M":"X",
"NIdentAHD_A1599_M":"X",
"NScreenCM_A1599AHD_M":"X",
"NScreenCM_A014_M":"X",
"NScreenTB_A1599AHD_M":"X",
"NScreenTB_A014_M":"X",
"NPrevTreatCrypt_A1599_M":"X",
"NPrevTreatCrypt_A014_M":"X",
"NTreatCrypt_A1599_M":"X",
"NTreatCrypt_A014_M":"X",
"NTreatTB_A1599_M":"X",
"NTreatTB_A014_M":"X",
"NAIDS_A1599_M":"X",
"NTreatAIDS_A1599_M":"X",
"NVLtested_A1599_M":"X",
"NVLtested_A014_M":"X",
"NVL_A1599_M":"X",
"NVL_A014_M":"X",
"N_A1599_POCCD4_M":"X",
"NPOCCD4_A1599_M":"X",
"N_A1599_POCVL_M":"X",
"N_A014_POCVL_M":"X",
"NPOCVL_A1599_M":"X",
"NPOCVL_A014_M":"X",
"NCRF_A1599_M":"X",
"NCATS_HIVPOSA1524_M":"X",
"NCATS_HIVNEGA1524_M":"X",
"NERC_HIVPOSA1524_M":"X",
"NERC_HIVNEGA1524_M":"X",
"NYMM_HIVPOSFpregEverBirth1524_M":"X",
"NMVLgt1000_A1599_M":"X",
"NMVLgt1000Ever_A1599_M":"X",
"N_ADHCVIR_MVLgt1000EverA1599_M":"X",
"N_ADHCADO_A1524_M":"X"}


## Outputs that are stored and calculated here in python, but not outputted:
# "N_women_used_oralPrEP_lastQ_15plus_sdpartner"
# "N_women_active_oralPrEP_lastQ_15plus_sdpartner"
# "N_women_used_dapivirinering_lastQ_15plus_sdpartner"
# "N_women_active_dapivirinering_lastQ_15plus_sdpartner"
# "N_women_used_injectablePrEP_lastQ_15plus_sdpartner"
# "N_women_active_injectablePrEP_lastQ_15plus_sdpartner"


##Stocks:
stock_variable_dictionary = {"HIVprev_M1549_M":"PrevalenceM15_49",
"HIVprev_F1549_M":"PrevalenceF15_49",
"HIVprev_A1549_M":"PrevalenceAll15_49",
"HIVprev_pregF1549_M":"X",
"HIVprev_F1524_M":"PrevalenceF15_24",
"HIVprev_FSW1599_M":"X",
"HIVprev_MSM1599_M":"X",
"HIVprev_TG1599_M":"X",
"NAlive_M1599_M":"Npop_M15plus",
"NAlive_F1599_M":"Npop_F15plus",
"NAlive_A014_M":"Npop_child",
"NAlive_M1524_M":"Npop_M15_24",
"NAlive_F1524_M":"Npop_F15_24",
"NAlive_M2549_M":"Npop_M25_49",
"NAlive_F2549_M":"Npop_F25_49",
"NAlive_FSW1599_M":"X",
"NAlive_MSM1599_M":"X",
"NAlive_TG1599_M":"X",
"Nalive_NEGInSDA1599_M":"N_HIVneg_in_SD_partnership_15plus",
"Nalive_NEGInSDNotOnARTA1599_M":"N_HIVneg_in_SD_partnership_noART_15plus",
"Nalive_NEGInSDF1599_M":"N_HIVneg_in_SD_partnership_F15plus",
"Nalive_NEGInSDNotOnARTF1599_M":"N_HIVneg_in_SD_partnership_noART_F15plus",
"NHIV_M1599_M":"Npos_M15plus",
"NHIV_F1599_M":"Npos_F15plus",
"NHIV_A014_M":"Npos_child",
"NHIV_M1524_M":"Npos_M15_24",
"NHIV_F1524_M":"Npos_F15_24",
"NHIV_M2549_M":"Npos_M25_49",
"NHIV_F2549_M":"Npos_F25_49",
"NHIV_FSW1599_M":"X",
"NHIV_MSM1599_M":"X",
"NHIV_TG1599_M":"X",
"NHIV_A1599_NoART_CD4500pl_M":"n_notonART_byCD4_15plus_gt500",
"NHIV_A1599_NoART_CD4350499_M":"n_notonART_byCD4_15plus_350_500",
"NHIV_A1599_NoART_CD4200349_M":"n_notonART_byCD4_15plus_200_350",
"NHIV_A1599_NoART_CD450199_M":"n_notonART_byCD4_15plus_50_200",
"NHIV_A1599_NoART_CD4050_M":"n_notonART_byCD4_15plus_lt50",
"NHIV_A014_NoART_CD4500pl_M":"X",
"NHIV_A014_NoART_CD4350499_M":"X",
"NHIV_A014_NoART_CD4200349_M":"X",
"NHIV_A014_NoART_CD450199_M":"X",
"NHIV_A014_NoART_CD4050_M":"X",
"NHIV_A1599_Asympt_Undiag_M":"X",
"NHIV_A1599_Asympt_Diag_NoART_M":"X",
"NHIV_A1599_Asympt_Diag_ART_M":"X",
"NHIV_A1599_Sympt_NOAIDS_M":"X",
"NHIV_A1599_Sympt_AIDS_M":"X",
"NHIV_A014_Asympt_Undiag_M":"X",
"NHIV_A014_Asympt_Diag_NoART_M":"X",
"NHIV_A014_Asympt_Diag_ART_M":"X",
"NHIV_A014_Sympt_NOAIDS_M":"X",
"NHIV_A014_Sympt_AIDS_M":"X",
"P_DIAG_A1599_M":"PropDiagnosed_15plus",
"P_DIAG_M1599_M":"PropDiagnosed_M15plus",
"P_DIAG_F1599_M":"PropDiagnosed_F15plus",
"P_DIAG_A014_M":"X",
"P_DIAG_M1524_M":"PropDiagnosed_M15_24",
"P_DIAG_F1524_M":"PropDiagnosed_F15_24",
"P_DIAG_FSW1599_M":"X",
"P_DIAG_MSM1599_M":"X",
"P_EVERSEX_M1599_M":"prop_eversex_M15plus",
"P_EVERSEX_F1599_M":"prop_eversex_F15plus",
"P_EVERSEX_F1524_M":"prop_eversex_F15_24",
"P_EVERSEX_MSM1599_M":"X",
"P_CONDOMLAST_M1599_M":"prop_usedcondomlastact_M15plus",
"P_CONDOMLAST_F1599_M":"prop_usedcondomlastact_F15plus",
"P_CONDOMLAST_F1524_M":"PropF15_24_condlasttime",
"P_CONDOMLAST_FSW1599_M":"X",
"P_CONDOMLAST_MSM1599_M":"X",
"P_CLS3m_M1599_M":"X",
"P_CLS3m_F1599_M":"X",
"P_CLS3m_F1524_M":"X",
"P_CLS3m_FSW_M":"X",
"P_CLS3m_MSM_M":"X",
"P_STI_FSW1599_M":"X",
"P_STI_MSM1599_M":"X",
"NAlive_ElevRiskF1524_M":"N_women_at_elevatedrisk_15to24",
"P_TDFPrEP_ElevRiskF1524_M":"prop_women_at_elevatedrisk_andonPrEP_15to24",
"NAlive_FPregBirthBF1599_M":"X",
"P_TDFPrEP_FPregBirthBF1599_M":"X",
"P_DPVPrEP_ElevRiskF1524_M":"X",
"P_DPVPrEP_FPregBirthBF1599_M":"X",
"P_CABPrEP_ElevRiskF1524_M":"X",
"P_CABPrEP_FPregBirthBF1599_M":"X",
"CIRC_PREV_M1549_M":"prop_circ_15_49",
"NOnART_M1599_M":"N_ART_M_15plus",
"NOnART_F1599_M":"N_ART_F_15plus",
"NOnART_A1524_M":"nonART_15_24",
"NOnART_A1599_M":"N_ART_total",
"NOnART_A014_M":"N_ART_child", 
"P_onART_DiagM1599_M":"Diagnosed_onART_M_15plus",
"P_onART_DiagF1599_M":"Diagnosed_onART_F_15plus",
"P_onART_DiagF1524_M":"Diagnosed_onART_F_15_24",
"P_onART_DiagA1524_M":"Diagnosed_onART_15_24",
"P_onART_DiagA1599_M":"Diagnosed_onART_15plus",
"P_onART_DiagA014_M":"X",
"P_onART_DiagFSW1599_M":"X",
"P_onART_DiagMSM1599_M":"X",
"P_onART_Diag12mAHDA1599_M":"X",
"P_onART_Diag12mNOAHDA1599_M":"X",
"P_onART_Diag12mAHDA014_M":"X",
"P_onART_Diag12mNOAHDA014_M":"X",
"P_onART_Diag12mAHDA1524_M":"X",
"P_onART_Diag12mNOAHDA1524_M":"X",
"P_onART_HIVM1599_M":"ARTcoverage_M_15plus",
"P_onART_HIVF1599_M":"ARTcoverage_F_15plus",
"P_onART_HIVF1524_M":"ARTcoverage_F_15_24",
"P_onART_HIVA1524_M":"ARTcoverage_15_24",
"P_onART_HIVA1599_M":"ARTcoverage_total",
"P_onART_HIVA014_M":"X", ## ARTcoverage_child
"P_onART_HIVFSW1599_M":"X",
"P_onART_HIVMSM1599_M":"X",
"P_onART_ExpM1599_M":"prop_ARTexperienced_M15plus",   ## To check.
"P_onART_ExpF1599_M":"prop_ARTexperienced_F15plus",
"P_onART_ExpA1524_M":"prop_ARTexperienced_15_24",
"P_onART_ExpA1599_M":"prop_ARTexperienced_15plus",
"P_onART_ExpA014_M":"X",
"P_onART_ExpFSW1599_M":"X",
"P_onART_ExpMSM1599_M":"X",
"P_onART_ExpFpregEverBirth1524_M":"X",
"P_VLS_onARTA1599_M":"PropAdultVS",
"P_VLS_onARTA1524_M":"prop_VS_adult15_24",
"P_VLS_onARTA014_M":"X",
"P_VLS_onARTpregEverBirthF1524_M":"X",
"P_VLS_onARTMVLgt1000EverA1599_M":"X"}

    
##################################
# Main code:
##################################

## Load up Vale's latest template and get the variables needed (plus the order they're in):
infile = "/home/mike/Dropbox (SPH Imperial College)/projects/MIHPSA_Zimabwe2021/Phase2/Output template MIHPSAZimP2_20230706.xlsx"
flows = pandas.read_excel(infile, sheet_name="Dictionary FLOW")
flows = flows.dropna(subset=['Variable name'])
flow_names = flows['Variable name'].values.tolist()
#print(flow_names)
#print(len(flow_names))

stocks = pandas.read_excel(infile, sheet_name="Dictionary STOCK ")
stocks = stocks.dropna(subset=['Variable name'])
stock_names = stocks['Variable name'].values.tolist()

## Load up the valevarnames:
[flowname_dict,flow_varlist] = function_get_clean_varlist_and_outputs(flow_names)
[stockname_dict,stock_varlist] = function_get_clean_varlist_and_outputs(stock_names)

## Check for duplicates:
a = stockname_dict.keys()
stock_duplicates = [item for item, count in collections.Counter(a).items() if count > 1]
if(stock_duplicates!=[]):
    print("Duplicates in stock:")
    print(stock_duplicates)
a = flowname_dict.keys()
flow_duplicates = [item for item, count in collections.Counter(a).items() if count > 1]
if(len(flow_duplicates)>0):
    print("Duplicates in flow:")
    print(flow_duplicates)



# PRINTVARS = 0
# if(PRINTVARS==1):
#     print("Flow variables (e.g. incidence):")
#     for i in flowname_dict.keys():
#         print(i)

#     print("Stock variables (e.g. prevalence):")
#     for i in stockname_dict.keys():
#         print(i)

if(set(stock_variable_dictionary.keys())==set(stock_varlist)):
    print("Stocks match")
else:
    print("Mismatch in stocks")
    print("In my dictionary but not in Excel file:")
    print(list(set(stock_variable_dictionary.keys())-set(stock_varlist)))
    print("In Excel file but not in my dictionary:")
    print(list(set(stock_varlist) - set(stock_variable_dictionary.keys())))
    #print(stock_varlist)
    
if(set(flow_variable_dictionary.keys())==set(flow_varlist)):
    print("Flows match")
else:
    print("Mismatch in flows")
    print("In my dictionary but not in Excel file:")
    print(list(set(flow_variable_dictionary.keys())-set(flow_varlist)))
    print("In Excel file but not in my dictionary:")
    print(list(set(flow_varlist) - set(flow_variable_dictionary.keys())))
    #print(flow_varlist)





if(MIHPSA_SCENARIO==1):
    print("Essential scenario")
    mihpsafiledir = "params_essential/Output/"
    ##output_file = "MIHPSA_project_outputs_phase2_essential.csv"
    output_file_flows = "MIHPSA_project_outputs_phase2_essential_flows.csv"
    output_file_stocks = "MIHPSA_project_outputs_phase2_essential_stocks.csv"
elif(MIHPSA_SCENARIO==2):
    print("Essential + PrEP scenario")
    mihpsafiledir = "params_essential_plus_PrEP/Output/"
    ##output_file = "MIHPSA_project_outputs_phase2_essentialplusPrEP.csv"
    output_file_flows = "MIHPSA_project_outputs_phase2_essentialplusPrEP_flows.csv"
    output_file_stocks = "MIHPSA_project_outputs_phase2_essentialplusPrEP_stocks.csv"
elif(MIHPSA_SCENARIO==3):
    print("Phase 2 status quo scenario")
    mihpsafiledir = "results_statusquo/Output/"
    output_file_flows = "MIHPSA_project_outputs_phase2_statusquo_flows.csv"
    output_file_stocks = "MIHPSA_project_outputs_phase2_statusquo_stocks.csv"
elif(MIHPSA_SCENARIO==4):
    print("Phase 2 minimal scenario")
    mihpsafiledir = "results_minimal/Output/"
    output_file_flows = "MIHPSA_project_outputs_phase2_minimal_flows.csv"
    output_file_stocks = "MIHPSA_project_outputs_phase2_minimal_stocks.csv"
elif(MIHPSA_SCENARIO==5):
    print("Phase 2 minimal plus CUPP scenario")
    mihpsafiledir = "results_minimal_plusCUPP/Output/"
    output_file_flows = "MIHPSA_project_outputs_phase2_minimalplusCUPP_flows.csv"
    output_file_stocks = "MIHPSA_project_outputs_phase2_minimalplusCUPP_stocks.csv"
elif(MIHPSA_SCENARIO==6):
    print("Phase 2 minimal plus SBCC scenario")
    mihpsafiledir = "results_minimal_plusSBCC/Output/"
    output_file_flows = "MIHPSA_project_outputs_phase2_minimalplusSBCC_flows.csv"
    output_file_stocks = "MIHPSA_project_outputs_phase2_minimalplusSBCC_stocks.csv"
elif(MIHPSA_SCENARIO==7):
    print("Phase 2 minimal + PrEP scenario")
    mihpsafiledir = "results_minimal_plusPrEP/Output/"
    output_file_flows = "MIHPSA_project_outputs_phase2_minimalplusPrEP_flows.csv"
    output_file_stocks = "MIHPSA_project_outputs_phase2_minimalplusPrEP_stocks.csv"
elif(MIHPSA_SCENARIO==99):
    print("Phase 2 minimal + PrEP scenario")
    mihpsafiledir = "params_testing24aug2024/Output/"
    output_file_flows = "TESTING_FLOWS.csv"
    output_file_stocks = "TESTING_STOCKS.csv"
    
    #mihpsafiledir = "params/testing_output/"





# This function looks in mihpsafiledir for all the MIHPSA_Output*.csv files and makes an output file for the MIHPSA project.
# Saves these as 
outputs_summary_stats = read_mihpsa_files_and_make_summary_file(mihpsafiledir)

outstring_flow = "t,"
for valevarname in flow_varlist:
    stats_needed = flowname_dict[valevarname]
    if(stats_needed=="All"):
        outstring_flow += valevarname+","+valevarname.rsplit("_M", 1)[0]+"_95LL,"+valevarname.rsplit("_M", 1)[0]+"_95UL,"
    else:
        outstring_flow += valevarname+","
outstring_flow.rstrip(",")
outstring_flow += "\n"


outstring_stock = "t,"
for valevarname in stock_varlist:
    stats_needed = stockname_dict[valevarname]
    if(stats_needed=="All"):
        outstring_stock += valevarname+","+valevarname.rsplit("_M", 1)[0]+"_95LL,"+valevarname.rsplit("_M", 1)[0]+"_95UL,"
    else:
        outstring_stock += valevarname+","
outstring_stock.rstrip(",")
outstring_stock += "\n"


#for y in range(1990,MIHPSA_TIMEPERIOD):
for y in range(2022,(MIHPSA_TIMEPERIOD-1)):
    # Time index in list of outputs
    i = y-1990
    outstring_flow += str(y)+"-"+str(y+1)+","
    for valevarname in flow_varlist:
        ibm_varname = flow_variable_dictionary[valevarname]
        stats_needed = flowname_dict[valevarname]
        ##print(y,valevarname, ibm_varname, stats_needed)
        # Skip if "X" - means not outputted by IBM:
        if(ibm_varname=="X"):
            if(stats_needed=="All"):
                outstring_flow += ",,,"
            else:
                outstring_flow += ","
        else:
            stats_needed = flowname_dict[valevarname]
            outstring_flow += str(outputs_summary_stats[ibm_varname]["Median"][i])+","
            if(stats_needed=="All"):
                outstring_flow += str(outputs_summary_stats[ibm_varname]["LL"][i])+","
                outstring_flow += str(outputs_summary_stats[ibm_varname]["UL"][i])+","
    outstring_flow.rstrip(",")
    outstring_flow += "\n"

## Stocks start in 2023:
for y in range(2023,MIHPSA_TIMEPERIOD):
    # Time index in list of outputs
    i = y-1990
    outstring_stock += str(y)+","
    for valevarname in stock_varlist:
        ibm_varname = stock_variable_dictionary[valevarname]
        stats_needed = stockname_dict[valevarname]
        ##print(y,valevarname, ibm_varname, stats_needed)
        # Skip if "X" - means not outputted by IBM:
        if(ibm_varname=="X"):
            if(stats_needed=="All"):
                outstring_stock += ",,,"
            else:
                outstring_stock += ","
        else:
            stats_needed = stockname_dict[valevarname]
            outstring_stock += str(outputs_summary_stats[ibm_varname]["Median"][i])+","
            if(stats_needed=="All"):
                outstring_stock += str(outputs_summary_stats[ibm_varname]["LL"][i])+","
                outstring_stock += str(outputs_summary_stats[ibm_varname]["UL"][i])+","
    outstring_stock.rstrip(",")
    outstring_stock += "\n"

    ####
    # outstring_stock += str(y)+","
    # for valevarname in stock_varlist[0:2]:
    #     ibm_varname = stock_variable_dictionary[valevarname]
    #     # Skip if "X" - means not outputted by IBM:
    #     if not(ibm_varname=="X"):
    #         stats_needed = stockname_dict[valevarname]
    #         outstring_stock += str(outputs_summary_stats[ibm_varname]["Median"][i])+","
    #         if(stats_needed=="All"):
    #             outstring_stock += str(outputs_summary_stats[ibm_varname]["LL"][i])+","
    #             outstring_stock += str(outputs_summary_stats[ibm_varname]["UL"][i])+","
    # outstring_stock.rstrip(",")
    # outstring_stock += "\n"
     


#print(outputs_summary_stats[flow_variable_dictionary["HIVIncid_M1549_M"]]["Median"])
flow_outfile = open(output_file_flows,"w")
flow_outfile.write(outstring_flow)
flow_outfile.close()

stock_outfile = open(output_file_stocks,"w")
stock_outfile.write(outstring_stock)
stock_outfile.close()

##print(outstring_flow)
