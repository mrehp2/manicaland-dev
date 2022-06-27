# Outline: File reads in the extended annual outputs file (currently called MIHPSA_outputs*.csv) and HIV prevention cascade files (HIVpreventioncascade_CL05_Zim_*.csv) from all Output/ directories listed in allfiledir, and makes two summary files for each directory.
# These output files are used by plot_cascade_impact.R to plot trends over time (incidence, use of prevention tools).

# The two output files are as follows:
# 1. MANICALAND_project_outputs_stage1*.csv contains summaries (median, 2.5 and 97.5 percentiles) of the key outputs (prevalence, incidence, ART coverage, etc. See read_manicaland_files_and_make_summary_file() for a full list of outputs.
# 2. HIVpreventioncascade*.csv contains summaries  (median, 2.5 and 97.5 percentiles) of the proportion of each priority population who are using each prevention tool.

# This file is a (highly) modified version of get_mihpsa_project_outputs_vX.py.


# Note that this file also does the following:
# scales populations to match the overall size of the adult populati on in Manicaland in 2012 (specified in "Manicaland_population_scale_adult").

import glob, sys, os, math
import numpy

USE_STDEV = 0 # Print mean +/- 1.645*s.d. or not in make_mean_CI() (in addition to median, 2.5 and 97.5 percentiles)


# Need to scale the IBM population to the total population of Zimbabwe. Right now we use the 2021 index:
Manicaland_population_scale_adult_year = 2012 # Zimbabwe census
Manicaland_population_scale_adult =  978747 # Table 6.9b C:\Users\mpickles\Dropbox (SPH Imperial College)\Covid_19\Parameters\Demographics\Zimbabwe2012_census_National_Report.pdf. Total pop (inc children) is 1752698, so 44.2% are children <15 (compared to national average of 41%).
#Manicaland_population_scale_child = 1752698 - 978747


# Population of men 15-49 (WPP 2019 - see Zimbabwe_WPP_pop_for_ART.xlsx).
#N_VMMC = [2918543,2945782,2975741,3003943,3034779,3067700,3102525,3139667,31763#70,3221509,3273850,3330609]


# Opens a file and returns the output (excluding the first line, which is assumed to be a header) as a list, where each element is a line of the file.
def read_data(filename):
    infile = open(filename, "r")
    data_raw = infile.read().rstrip().splitlines()
    infile.close()
    
    # First line is a header:
    return data_raw[1:]





def read_Manicaland_header(mihpsa_filename):
    mihpsa_file = open(mihpsa_filename,"r")
    header = mihpsa_file.readlines()[0].rstrip().split(",")
    mihpsa_file.close()

    i_NpopM15_49 = header.index('NPop_15to49_male')
    i_NpopF15_49 = header.index('NPop_15to49_female')

    # Note that I use "49" in the variable name b
    i_NpopM_younger = header.index('NPop_15to29_male')
    i_NpopM_older = header.index('NPop_30to54_male')
    i_NpopF_younger = header.index('NPop_15to24_female')
    i_NpopF_older = header.index('NPop_25to54_female')

    i_PosM15_49 =  header.index('NPos_15to49_male')
    i_PosF15_49 =  header.index('NPos_15to49_female')

    i_PosM_younger = header.index('NPos_15to29_male')
    i_PosM_older = header.index('NPos_30to54_male')
    i_PosF_younger = header.index('NPos_15to24_female')
    i_PosF_older = header.index('NPos_25to54_female')

    i_artM15plus = header.index('NonART_15plus_male')
    i_artF15plus = header.index('NonART_15plus_female')

    i_NpopM15plus = header.index('Npop_15plus_male')
    i_NpopF15plus = header.index('Npop_15plus_female')
    #i_Npop_child = header.index('Npop_children_under15')
    

    i_NposM15plus = header.index('Npos_15plus_male')
    i_NposF15plus = header.index('Npos_15plus_female')
    i_NawareM15plus = header.index('Naware_15plus_male')
    i_NawareF15plus = header.index('Naware_15plus_female')
    i_NonARTM15plus = header.index('NonART_15plus_male')
    i_NonARTF15plus = header.index('NonART_15plus_female')
    i_N_VSM15plus = header.index('N_VS_15plus_male')
    i_N_VSF15plus = header.index('N_VS_15plus_female')
    
    i_N_newHIVinfections_15to24_male = header.index('N_newHIVinfections_15to24_male')
    i_N_newHIVinfections_25to49_male = header.index('N_newHIVinfections_25to49_male')
    i_N_newHIVinfections_15to24_female = header.index('N_newHIVinfections_15to24_female')
    i_N_newHIVinfections_25to49_female = header.index('N_newHIVinfections_25to49_female')
    i_N_newHIVdiagnoses_15plus = header.index('N_newHIVdiagnoses_15plus')

    i_VMMC_op = header.index('N_VMMC_cumulative_15_49') # Cumulative # of VMMCs carried out in 15-49
    
    i_circ = header.index('Ncirc_15to49') # This is (cumulative) men circumcised either VMMC or TMC aged 15-49.

    
    return [i_NpopM15_49,i_NpopF15_49,i_NpopM_younger,i_NpopF_younger,i_NpopM_older,i_NpopF_older,i_PosM15_49,i_PosF15_49,i_PosM_younger,i_PosF_younger,i_PosM_older,i_PosF_older,i_artM15plus,i_artF15plus,i_NpopM15plus,i_NpopF15plus,i_circ,i_NposM15plus,i_NposF15plus,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_newHIVinfections_15to24_male,i_N_newHIVinfections_25to49_male,i_N_newHIVinfections_15to24_female,i_N_newHIVinfections_25to49_female,i_N_newHIVdiagnoses_15plus,i_VMMC_op]



def read_HIVpreventioncascade_files(HIVpreventioncascade_filedir,outfilename,file_tag):
    # If this is 1 then we include 'no partner of type X' in the numerator and denominator of the condom use measure.
    INCLUDE_NO_PARTNER=0
    ERR=1e-12
    
    HIVpreventioncascadefiles = glob.glob(HIVpreventioncascade_filedir + "/HIVpreventioncascade_CL*"+file_tag)
    print(file_tag,HIVpreventioncascadefiles)


    outputs_prop_PrEP_M_younger = {}
    outputs_prop_PrEP_M_older = {}
    outputs_prop_PrEP_M15_54 = {}
    outputs_prop_PrEP_F_younger = {}
    outputs_prop_PrEP_F_older = {}
    outputs_prop_PrEP_F15_54 = {}
    outputs_prop_VMMC_M_younger = {}
    outputs_prop_VMMC_M_older = {}
    outputs_prop_VMMC_15_54 = {}
    
    outputs_prop_M_15_29_LTpartnerships_cond_lastact = {}
    outputs_prop_M_15_29_LT_cond_always = {}
    outputs_prop_M_30_54_LTpartnerships_cond_lastact = {}
    outputs_prop_M_30_54_LT_cond_always = {}

    outputs_prop_F_15_24_LTpartnerships_cond_lastact = {}
    outputs_prop_F_15_24_LT_cond_always = {}
    outputs_prop_F_25_54_LTpartnerships_cond_lastact = {}
    outputs_prop_F_25_54_LT_cond_always = {}
    
    outputs_prop_M_15_29_Casualpartnerships_cond_lastact = {}
    outputs_prop_M_15_29_Casual_cond_always = {}
    outputs_prop_M_30_54_Casualpartnerships_cond_lastact = {}
    outputs_prop_M_30_54_Casual_cond_always = {}

    outputs_prop_F_15_24_Casualpartnerships_cond_lastact = {}
    outputs_prop_F_15_24_Casual_cond_always = {}
    outputs_prop_F_25_54_Casualpartnerships_cond_lastact = {}
    outputs_prop_F_25_54_Casual_cond_always = {}
    
    
    # Process each of the HIVpreventioncascade output files:
    for n,f in enumerate(HIVpreventioncascadefiles):

        # Read the data from a single file (header is not returned)
        run_data = read_data(f)
        

        for i,line in enumerate(run_data):

            linedata = [int(x) for x in line.split(",")]
            year = linedata[0]
            if(year>=1990):
                
            
            
                if(n==0):
                    
                    i_temp = 4
                    outputs_prop_PrEP_M_younger[year] = [(linedata[i_temp+3]+linedata[i_temp+4])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+ERR)]
                    outputs_prop_PrEP_M15_54[year] = [(linedata[i_temp+3]+linedata[i_temp+4]+linedata[i_temp+7]+linedata[i_temp+8])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+linedata[i_temp+5]+linedata[i_temp+6]+linedata[i_temp+7]+linedata[i_temp+8]+ERR)]

                    i_temp += 4
                    outputs_prop_PrEP_M_older[year] = [(linedata[i_temp+3]+linedata[i_temp+4])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+ERR)]

                    i_temp += 12 # Skip 55+M and <15F
                    outputs_prop_PrEP_F_younger[year] = [(linedata[i_temp+3]+linedata[i_temp+4])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+ERR)]
                    
                    outputs_prop_PrEP_F15_54[year] =  [(linedata[i_temp+3]+linedata[i_temp+4]+linedata[i_temp+7]+linedata[i_temp+8])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+linedata[i_temp+5]+linedata[i_temp+6]+linedata[i_temp+7]+linedata[i_temp+8]+ERR)]

                    i_temp += 4
                    outputs_prop_PrEP_F_older[year] = [(linedata[i_temp+3]+linedata[i_temp+4])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+ERR)]

                    i_temp += 21 # Skip 55+F, neversexM/F and <15M VMMC (which is *5* long)
                    outputs_prop_VMMC_M_younger[year] = [(linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+linedata[i_temp+5]+ERR)]

                    outputs_prop_VMMC_15_54[year] = [(linedata[i_temp+3]+linedata[i_temp+8])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+linedata[i_temp+5]+linedata[i_temp+6]+linedata[i_temp+7]+linedata[i_temp+8]+linedata[i_temp+9]+linedata[i_temp+10]+ERR)]
                    i_temp += 5
                    outputs_prop_VMMC_M_older[year] = [(linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+linedata[i_temp+5]+ERR)]
                
                    i_temp += 15 # Skip 55+ and neversex.

                    # Proportion of partnerships of 15-29 year old men where a condom was used in last act.
                    outputs_prop_M_15_29_LTpartnerships_cond_lastact[year] = [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]
                    i_temp += 2 

                    # Proportion of 15-29 year old men who currently use a condom with all their partners (count "no current partners" as yes):
                    outputs_prop_M_15_29_LT_cond_always[year] = [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                    
                    i_temp += 3
                    outputs_prop_M_15_29_Casualpartnerships_cond_lastact[year] = [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]

                    i_temp += 2 
                    outputs_prop_M_15_29_Casual_cond_always[year] = [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                    
                    i_temp += 3

                    outputs_prop_M_30_54_LTpartnerships_cond_lastact[year] = [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]
                    i_temp += 2 

                    outputs_prop_M_30_54_LT_cond_always[year] = [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                    
                    i_temp += 3
                    outputs_prop_M_30_54_Casualpartnerships_cond_lastact[year] = [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]

                    i_temp += 2 
                    outputs_prop_M_30_54_Casual_cond_always[year] = [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                    
                    i_temp += 3



                    outputs_prop_F_15_24_LTpartnerships_cond_lastact[year] = [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]
                    i_temp += 2 

                    outputs_prop_F_15_24_LT_cond_always[year] = [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                    
                    i_temp += 3
                    outputs_prop_F_15_24_Casualpartnerships_cond_lastact[year] = [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]

                    i_temp += 2 
                    outputs_prop_F_15_24_Casual_cond_always[year] = [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                    
                    i_temp += 3

                    outputs_prop_F_25_54_LTpartnerships_cond_lastact[year] = [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]
                    i_temp += 2 

                    outputs_prop_F_25_54_LT_cond_always[year] = [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                    
                    i_temp += 3
                    outputs_prop_F_25_54_Casualpartnerships_cond_lastact[year] = [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]

                    i_temp += 2 
                    outputs_prop_F_25_54_Casual_cond_always[year] = [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                ##############################
                
                else:
                    
                    i_temp = 4
                    outputs_prop_PrEP_M_younger[year] += [(linedata[i_temp+3]+linedata[i_temp+4])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+ERR)]
                    outputs_prop_PrEP_M15_54[year] += [(linedata[i_temp+3]+linedata[i_temp+4]+linedata[i_temp+7]+linedata[i_temp+8])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+linedata[i_temp+5]+linedata[i_temp+6]+linedata[i_temp+7]+linedata[i_temp+8]+ERR)]


                    i_temp += 4
                    outputs_prop_PrEP_M_older[year] += [(linedata[i_temp+3]+linedata[i_temp+4])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+ERR)]

                    i_temp += 12 # Skip 55+M and <15F
                    outputs_prop_PrEP_F_younger[year] += [(linedata[i_temp+3]+linedata[i_temp+4])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+ERR)]
                    
                    outputs_prop_PrEP_F15_54[year] +=  [(linedata[i_temp+3]+linedata[i_temp+4]+linedata[i_temp+7]+linedata[i_temp+8])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+linedata[i_temp+5]+linedata[i_temp+6]+linedata[i_temp+7]+linedata[i_temp+8]+ERR)]

                    i_temp += 4
                    outputs_prop_PrEP_F_older[year] += [(linedata[i_temp+3]+linedata[i_temp+4])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+ERR)]

                    i_temp += 21 # Skip 55+F, neversexM/F and <15M VMMC (which is *5* long)
                    outputs_prop_VMMC_M_younger[year] += [(linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+linedata[i_temp+5]+ERR)]

                    outputs_prop_VMMC_15_54[year] += [(linedata[i_temp+3]+linedata[i_temp+8])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+linedata[i_temp+5]+linedata[i_temp+6]+linedata[i_temp+7]+linedata[i_temp+8]+linedata[i_temp+9]+linedata[i_temp+10]+ERR)]
                    i_temp += 5
                    outputs_prop_VMMC_M_older[year] += [(linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+linedata[i_temp+3]+linedata[i_temp+4]+linedata[i_temp+5]+ERR)]
                
                    i_temp += 15 # Skip 55+ and neversex.

                    # Proportion of partnerships of 15-29 year old men where a condom was used in last act.
                    outputs_prop_M_15_29_LTpartnerships_cond_lastact[year] += [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]
                    i_temp += 2 

                    # Proportion of 15-29 year old men who currently use a condom with all their partners (count "no current partners" as yes):
                    outputs_prop_M_15_29_LT_cond_always[year] += [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                    
                    i_temp += 3
                    outputs_prop_M_15_29_Casualpartnerships_cond_lastact[year] += [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]

                    i_temp += 2 
                    outputs_prop_M_15_29_Casual_cond_always[year] += [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                    
                    i_temp += 3
                    

                    outputs_prop_M_30_54_LTpartnerships_cond_lastact[year] += [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]
                    i_temp += 2 

                    outputs_prop_M_30_54_LT_cond_always[year] += [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                    
                    i_temp += 3
                    outputs_prop_M_30_54_Casualpartnerships_cond_lastact[year] += [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]

                    i_temp += 2 
                    outputs_prop_M_30_54_Casual_cond_always[year] += [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                    
                    i_temp += 3


###
                    outputs_prop_F_15_24_LTpartnerships_cond_lastact[year] += [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]
                    i_temp += 2 

                    outputs_prop_F_15_24_LT_cond_always[year] += [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                    
                    i_temp += 3
                    outputs_prop_F_15_24_Casualpartnerships_cond_lastact[year] += [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]

                    i_temp += 2 
                    outputs_prop_F_15_24_Casual_cond_always[year] += [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                    
                    i_temp += 3

####
                    outputs_prop_F_25_54_LTpartnerships_cond_lastact[year] += [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]
                    i_temp += 2 

                    outputs_prop_F_25_54_LT_cond_always[year] += [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]
                    
                    i_temp += 3
                    outputs_prop_F_25_54_Casualpartnerships_cond_lastact[year] += [linedata[i_temp+2]/(linedata[i_temp+1]+linedata[i_temp+2]+ERR)]

                    i_temp += 2 
                    outputs_prop_F_25_54_Casual_cond_always[year] += [(linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3])/(linedata[i_temp+1]+linedata[i_temp+2]+INCLUDE_NO_PARTNER*linedata[i_temp+3]+ERR)]


                    

    outputs_to_store = {"prop_PrEP_M15_29":outputs_prop_PrEP_M_younger,
                        "prop_PrEP_M15_54":outputs_prop_PrEP_M15_54,
                        "prop_PrEP_M30_54":outputs_prop_PrEP_M_older,
                        "prop_PrEP_F15_24":outputs_prop_PrEP_F_younger,
                        "prop_PrEP_F15_54":outputs_prop_PrEP_F15_54,
                        "prop_PrEP_F25_54":outputs_prop_PrEP_F_older,
                        "prop_VMMC_M15_29":outputs_prop_VMMC_M_younger,
                        "prop_VMMC_15_54":outputs_prop_VMMC_15_54,
                        "prop_VMMC_M30_54":outputs_prop_VMMC_M_older,
                        "prop_M_15_29_LTpartnerships_cond_lastact":outputs_prop_M_15_29_LTpartnerships_cond_lastact,
                        "prop_M_15_29_LT_cond_always":outputs_prop_M_15_29_LT_cond_always,
                        "prop_M_15_29_Casualpartnerships_cond_lastact":outputs_prop_M_15_29_Casualpartnerships_cond_lastact,
                        "prop_M_15_29_Casual_cond_always":outputs_prop_M_15_29_Casual_cond_always,
                        "prop_M_30_54_LTpartnerships_cond_lastact":outputs_prop_M_30_54_LTpartnerships_cond_lastact,
                        "prop_M_30_54_LT_cond_always":outputs_prop_M_30_54_LT_cond_always,
                        "prop_M_30_54_Casualpartnerships_cond_lastact":outputs_prop_M_30_54_Casualpartnerships_cond_lastact,
                        "prop_M_30_54_Casual_cond_always":outputs_prop_M_30_54_Casual_cond_always,
                        "prop_F_15_24_LTpartnerships_cond_lastact":outputs_prop_F_15_24_LTpartnerships_cond_lastact,
                        "prop_F_15_24_LT_cond_always":outputs_prop_F_15_24_LT_cond_always,
                        "prop_F_15_24_Casualpartnerships_cond_lastact":outputs_prop_F_15_24_Casualpartnerships_cond_lastact,
                        "prop_F_15_24_Casual_cond_always":outputs_prop_F_15_24_Casual_cond_always,
                        "prop_F_25_54_LTpartnerships_cond_lastact":outputs_prop_F_25_54_LTpartnerships_cond_lastact,
                        "prop_F_25_54_LT_cond_always":outputs_prop_F_25_54_LT_cond_always,
                        "prop_F_25_54_Casualpartnerships_cond_lastact":outputs_prop_F_25_54_Casualpartnerships_cond_lastact,
                        "prop_F_25_54_Casual_cond_always":outputs_prop_F_25_54_Casual_cond_always
    }

                        
    



    list_of_outputs = ["prop_PrEP_M15_29","prop_PrEP_M15_54","prop_PrEP_M30_54","prop_PrEP_F15_24","prop_PrEP_F15_54","prop_PrEP_F25_54","prop_VMMC_M15_29","prop_VMMC_15_54","prop_VMMC_M30_54","prop_M_15_29_LTpartnerships_cond_lastact","prop_M_15_29_LT_cond_always","prop_M_15_29_Casualpartnerships_cond_lastact","prop_M_15_29_Casual_cond_always","prop_M_30_54_LTpartnerships_cond_lastact","prop_M_30_54_LT_cond_always","prop_M_30_54_Casualpartnerships_cond_lastact","prop_M_30_54_Casual_cond_always","prop_F_15_24_LTpartnerships_cond_lastact","prop_F_15_24_LT_cond_always","prop_F_15_24_Casualpartnerships_cond_lastact","prop_F_15_24_Casual_cond_always","prop_F_25_54_LTpartnerships_cond_lastact","prop_F_25_54_LT_cond_always","prop_F_25_54_Casualpartnerships_cond_lastact","prop_F_25_54_Casual_cond_always"]

    print(outfilename)
    make_mean_CI(outputs_to_store,list_of_outputs,outfilename)
    






# For each run we need to generate the 
def get_pop_scale(manicaland_model_data,i_NpopM15_49,i_NpopM15plus,i_NpopF15plus):

    for line in manicaland_model_data:
        year = int(line.split(",")[0])
        if(year==Manicaland_population_scale_adult_year):
            line_data = line.split(",")
            
            pop_tot_adult = int(line_data[i_NpopM15plus]) + int(line_data[i_NpopF15plus])
            #pop_child = int(line_data[i_Npop_child])
            scale_tot_adult = Manicaland_population_scale_adult / (1.0*pop_tot_adult)

            # Entire population:L
            #scale_pop = (Manicaland_population_scale_adult+Manicaland_population_scale_child) / (1.0*(pop_tot_adult+pop_child))
            

            #print("Scales: ",scale_tot_adult)
            break

    #return [scale_pop, scale_pop, scale_pop, scale_pop]
    return scale_tot_adult


def write_output(outputs,outfile):
    outstring = ""
    years_saved = sorted(outputs)
    #years_saved = outputs.keys()
    #years_saved.sort()
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
    #years = output1.keys()
    #years.sort()
    outputs_summed = {}
    #outputs_summed[years[0]] = [0]*len(output1[years[0]])
    for y in range(len(years)):
        outputs_summed[years[y]] = [output1[years[y]][i]+output2[years[y]][i] for i in range(len(output1[years[y]]))]

    return outputs_summed



def sum_three_outputs(output1,output2,output3):
    years = sorted(output1)
    #years = output1.keys()
    #years.sort()
    outputs_summed = {}
    #outputs_summed[years[0]] = [0]*len(output1[years[0]])
    for y in range(len(years)):
        outputs_summed[years[y]] = [output1[years[y]][i]+output2[years[y]][i]+output3[years[y]][i] for i in range(len(output1[years[y]]))]

    return outputs_summed
    

def calculate_incidence(N_newinfections,Npop,Npos):
    years = sorted(N_newinfections)
    #years = N_newinfections.keys()
    #years.sort()
    incidence = {}
    #incidence[years[0]] = [0]*len(N_newinfections[years[0]])
    for y in range(len(years)):
        incidence[years[y]] = [N_newinfections[years[y]][i] / (Npop[years[y]][i] - Npos[years[y]][i]) for i in range(len(N_newinfections[years[y]]))]
    return incidence

def get_quotient(output1,output2,ERR):
    years = sorted(output1)
    #years = output1.keys()
    #years.sort()
    outputs_quotient = {}
    outputs_quotient[years[0]] = [0]*len(output1[years[0]])
    for y in range(1,len(years)):
        outputs_quotient[years[y]] = [output1[years[y]][i]/(1.0*output2[years[y]][i]+ERR) for i in range(len(output1[years[y]]))]

    return outputs_quotient


def generate_output_from_one_var(output):
    SEP=","    
    outstr = ""
    for y in range(1990,2041):
        outstr += str(y)+SEP+SEP.join([str(x) for x in output[y]])+"\n"
    return outstr


def make_mean_CI(outputs_dict,output_names,outfilename):
    SEP=","
    output_string = "Year"+SEP +SEP.join(["Median_"+x+SEP+"LL_"+x+SEP+"UL_"+x for x in output_names]).rstrip(SEP)+"\n"

    for y in range(1990,2041):
        output_string += str(y) + SEP
        for outputname in output_names:
            output_string += str(numpy.median(outputs_dict[outputname][y])) + SEP + str(numpy.percentile(outputs_dict[outputname][y],5)) + SEP +str(numpy.percentile(outputs_dict[outputname][y],95)) + SEP
        output_string = output_string.rstrip(SEP)
        output_string += "\n"

    outfile = open(outfilename,"w")
    outfile.write(output_string)
    outfile.close()

# This one is the transpose (years are cols, outcomes are rows):
def make_mean_CI_old(outputs_dict,output_names):

    output_string = "OutcomeMeasure "+" ".join([str(x) for x in range(1990,2041)])+"\n"
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

        

        output_string += outputname + "_"
        output_string += "Median " + " ".join([str(x) for x in median_output]) +  "\n"
        #output_string += "Mean " + " ".join([str(x) for x in mean_output]) +  "\n"
        output_string += outputname + "_"
        output_string += "LL "+" ".join([str(x) for x in ll_output]) +  "\n"
        output_string += outputname + "_"
        output_string += "UL "+" ".join([str(x) for x in ul_output]) +  "\n"
        if(USE_STDEV==1):
            output_string += outputname + "_"
            output_string += "STD_LL "+" ".join([str(x) for x in ll_stdev]) +  "\n"
            output_string += outputname + "_"
            output_string += "STD_UL "+" ".join([str(x) for x in ul_stdev]) +  "\n"
        #output_string += "\n"

    outfile = open("MANICALAND_project_outputs_stage1.csv","w")
    outfile.write(output_string)
    outfile.close()

        

def read_manicaland_files_and_make_summary_file(manicalandfiledir,outfilename,file_tag):

    ERR=1e-12
    
    manicalandfiles = glob.glob(manicalandfiledir + "/MIHPSA_output_CL*"+file_tag)

    [i_NpopM15_49,i_NpopF15_49,i_NpopM_younger,i_NpopF_younger,i_NpopM_older,i_NpopF_older,i_PosM15_49,i_PosF15_49,i_PosM_younger,i_PosF_younger,i_PosM_older,i_PosF_older,i_artM15plus,i_artF15plus,i_NpopM15plus,i_NpopF15plus,i_circ,i_NposM15plus,i_NposF15plus,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_newHIVinfections_15to24_male,i_N_newHIVinfections_25to49_male,i_N_newHIVinfections_15to24_female,i_N_newHIVinfections_25to49_female,i_N_newHIVdiagnoses_15plus,i_VMMC_op] = read_Manicaland_header(manicalandfiles[0])

    
    #prevalence_M_by_year = []
    #prevalence_F_by_year = []
    outputs_prevalence_M15_49 = {}
    outputs_prevalence_M_younger = {}
    outputs_prevalence_M_older = {}
    outputs_prevalence_F15_49 = {}
    outputs_prevalence_F_younger = {}
    outputs_prevalence_F_older = {}
    outputs_prevalence_overall15_49 = {}
    
    outputs_Npop_M15_49 = {}
    outputs_Npop_F15_49 = {}

    outputs_Npop_M_younger = {}
    outputs_Npop_M_older = {}

    outputs_Npop_F_younger = {}
    outputs_Npop_F_older = {}

    outputs_Npop15_49 = {}

    outputs_Npop_15plus = {}
    outputs_Npop_M15plus = {}
    outputs_Npop_F15plus = {}

    outputs_Npos_M15_49 = {}
    outputs_Npos_F15_49 = {}

    outputs_Npos_M_younger = {}
    outputs_Npos_M_older = {}
    outputs_Npos_F_younger = {}
    outputs_Npos_F_older = {}


    outputs_Npos_M15plus = {}
    outputs_Npos_F15plus = {}


    outputs_Npos15_49 = {}

    
    outputs_N_ART_M15plus = {}
    outputs_N_ART_F15plus = {}

    # UNAIDS definition of ART coverage: Percentage of people living with HIV currently receiving ART among the estimated number of adults and children living with HIV
    outputs_ARTcoverage_M15plus = {}
    outputs_ARTcoverage_F15plus = {}

    outputs_DiagOnART_M15plus = {}
    outputs_DiagOnART_F15plus = {}
    

    outputs_prop_diagnosed_M15plus = {}
    outputs_prop_diagnosed_F15plus = {}

    outputs_VMMC_cumulative15_49 = {}
    
    outputs_Ncirc_15_49 = {} # Number of 15-49 year old men who are currently circumcised.

    outputs_propcirc_15_49 = {} # Number of 15-49 year old men who are currently circumcised.
    
    outputs_prop_VS_adult15plus = {}


    outputs_Ncumulativecases_M15_49 = {}
    outputs_Ncumulativecases_M_younger = {}
    outputs_Ncumulativecases_M_older = {}
    outputs_Ncumulativecases_F15_49 = {}
    outputs_Ncumulativecases_F_younger = {}
    outputs_Ncumulativecases_F_older = {}
    
    
    # Process each of the Manicaland output files:
    for n,f in enumerate(manicalandfiles):

        # Read the data from a single file (header is not used)
        run_data = read_data(f)
        
        scale_tot_adult = get_pop_scale(run_data,i_NpopM15_49,i_NpopM15plus,i_NpopF15plus)


        for i,line in enumerate(run_data):

            [year,NpopM15_49,NpopF15_49,NpopM_younger,NpopF_younger,NpopM_older,NpopF_older,PosM15_49,PosF15_49,PosM_younger,PosF_younger,PosM_older,PosF_older,artM15plus,artF15plus,NpopM15plus,NpopF15plus,Ncirc_15_49,NposM15plus,NposF15plus,NawareM15plus,NawareF15plus,NonARTM15plus,NonARTF15plus,N_VSM15plus,N_VSF15plus,N_newHIVinfections_15to24_male,N_newHIVinfections_25to49_male,N_newHIVinfections_15to24_female,N_newHIVinfections_25to49_female,N_newHIVdiagnoses_15plus,N_VMMC_op_cumulative] = [int(line.split(",")[index]) for index in [0,i_NpopM15_49,i_NpopF15_49,i_NpopM_younger,i_NpopF_younger,i_NpopM_older,i_NpopF_older,i_PosM15_49,i_PosF15_49,i_PosM_younger,i_PosF_younger,i_PosM_older,i_PosF_older,i_artM15plus,i_artF15plus,i_NpopM15plus,i_NpopF15plus,i_circ,i_NposM15plus,i_NposF15plus,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_newHIVinfections_15to24_male,i_N_newHIVinfections_25to49_male,i_N_newHIVinfections_15to24_female,i_N_newHIVinfections_25to49_female,i_N_newHIVdiagnoses_15plus,i_VMMC_op]]
            if(n==0):


    # UNAIDS definition of ART coverage: Percentage of people living with HIV currently receiving ART among the estimated number of adults and children living with HIV

                outputs_prevalence_M15_49[year] = [PosM15_49/(1.0*NpopM15_49)]

                outputs_prevalence_M_younger[year] = [PosM_younger/(1.0*NpopM_younger)]
                outputs_prevalence_M_older[year] = [PosM_older/(1.0*NpopM_older)]

                outputs_prevalence_F15_49[year] = [PosF15_49/(1.0*NpopF15_49)]

                outputs_prevalence_F_younger[year] = [PosF_younger/(1.0*NpopF_younger)]
                outputs_prevalence_F_older[year] = [PosF_older/(1.0*NpopF_older)]

                outputs_prevalence_overall15_49[year] = [(PosM15_49+PosF15_49)/(1.0*(NpopM15_49+NpopF15_49))]

                
                outputs_N_ART_M15plus[year] = [artM15plus*scale_tot_adult]
                outputs_N_ART_F15plus[year] = [artF15plus*scale_tot_adult]

                outputs_Npop_M15_49[year] = [NpopM15_49*scale_tot_adult]
                outputs_Npop_F15_49[year] = [NpopF15_49*scale_tot_adult]
                outputs_Npop15_49[year] = [(NpopM15_49+NpopF15_49)*scale_tot_adult]

                outputs_Npop_M_younger[year] = [NpopM_younger*scale_tot_adult]
                outputs_Npop_M_older[year] = [NpopM_older*scale_tot_adult]
                outputs_Npop_F_younger[year] = [NpopF_younger*scale_tot_adult]
                outputs_Npop_F_older[year] = [NpopF_older*scale_tot_adult]


                outputs_Npop_15plus[year] = [(NpopM15plus+NpopF15plus)*scale_tot_adult]
                outputs_Npop_M15plus[year] = [NpopM15plus*scale_tot_adult]
                outputs_Npop_F15plus[year] = [NpopF15plus*scale_tot_adult]

                
                outputs_Npos_M15_49[year] = [PosM15_49*scale_tot_adult]
                outputs_Npos_F15_49[year] = [PosF15_49*scale_tot_adult]
                outputs_Npos15_49[year] = [(PosM15_49+PosF15_49)*scale_tot_adult]

                outputs_Npos_M_younger[year] = [PosM_younger*scale_tot_adult]
                outputs_Npos_M_older[year] = [PosM_older*scale_tot_adult]
                outputs_Npos_F_younger[year] = [PosF_younger*scale_tot_adult]
                outputs_Npos_F_older[year] = [PosF_older*scale_tot_adult]
                
                outputs_Npos_M15plus[year] = [NposM15plus*scale_tot_adult]
                outputs_Npos_F15plus[year] = [NposF15plus*scale_tot_adult]
                
                outputs_ARTcoverage_M15plus[year] = [artM15plus/(1.0*NposM15plus+ERR)]

                outputs_ARTcoverage_F15plus[year] = [artF15plus/(1.0*NposF15plus+ERR)]
                

                outputs_DiagOnART_M15plus[year] = [artM15plus/(1.0*NawareM15plus+ERR)]

                outputs_DiagOnART_F15plus[year] = [artF15plus/(1.0*NawareF15plus+ERR)]
                
                
                outputs_Ncirc_15_49[year] = [Ncirc_15_49*scale_tot_adult]
                outputs_propcirc_15_49[year] = [Ncirc_15_49/(1.0*NpopM15_49)]

                outputs_prop_diagnosed_M15plus[year] = [NawareM15plus/(1.0*NposM15plus+ERR)]

                outputs_prop_diagnosed_F15plus[year] = [NawareF15plus/(1.0*NposF15plus+ERR)]


                outputs_prop_VS_adult15plus[year] = [(N_VSM15plus+N_VSF15plus)/(1.0*(artM15plus+artF15plus+ERR))]





                ##############################


                outputs_Ncumulativecases_M_younger[year] = [N_newHIVinfections_15to24_male*scale_tot_adult]
                outputs_Ncumulativecases_M_older[year] = [N_newHIVinfections_25to49_male*scale_tot_adult]

                outputs_Ncumulativecases_F_younger[year] = [N_newHIVinfections_15to24_female*scale_tot_adult]
                outputs_Ncumulativecases_F_older[year] = [N_newHIVinfections_25to49_female*scale_tot_adult]

                outputs_Ncumulativecases_M15_49[year] = [(N_newHIVinfections_15to24_male+N_newHIVinfections_25to49_male)*scale_tot_adult]
                outputs_Ncumulativecases_F15_49[year] = [(N_newHIVinfections_15to24_female+N_newHIVinfections_25to49_female)*scale_tot_adult]
                

                #outputs_cumulativetotaldeaths_M20_59[year] = [N_deaths_20_59_male*scale_tot_adult]
                #outputs_cumulativetotaldeaths_F20_59[year] = [N_deaths_20_59_female*scale_tot_adult]
                #outputs_cumulativeNtests_M15plus[year] = [N_HIVtests_15plus_male*scale_tot_adult]
                #outputs_cumulativeNtests_F15plus[year] = [N_HIVtests_15plus_female*scale_tot_adult]
                #outputs_cumulativeNdiagnoses[year] = [N_newHIVdiagnoses_15plus*scale_tot_adult]

                outputs_VMMC_cumulative15_49[year] = [N_VMMC_op_cumulative*scale_tot_adult]

                
            else:
                outputs_Npop_M15_49[year] += [NpopM15_49*scale_tot_adult]
                outputs_Npop_F15_49[year] += [NpopF15_49*scale_tot_adult]
                outputs_Npop_M_younger[year] += [NpopM_younger*scale_tot_adult]
                outputs_Npop_M_older[year] += [NpopM_older*scale_tot_adult]
                outputs_Npop_F_younger[year] += [NpopF_younger*scale_tot_adult]
                outputs_Npop_F_older[year] += [NpopF_older*scale_tot_adult]

                outputs_Npop15_49[year] += [(NpopM15_49+NpopF15_49)*scale_tot_adult]
                outputs_Npop_15plus[year] += [(NpopM15plus+NpopF15plus)*scale_tot_adult]
                outputs_Npop_M15plus[year] += [NpopM15plus*scale_tot_adult]
                outputs_Npop_F15plus[year] += [NpopF15plus*scale_tot_adult]
                
                
                outputs_Npos_M15_49[year] += [PosM15_49*scale_tot_adult]
                outputs_Npos_F15_49[year] += [PosF15_49*scale_tot_adult]
                outputs_Npos15_49[year] += [(PosM15_49+PosF15_49)*scale_tot_adult]

                outputs_Npos_M_younger[year] += [PosM_younger*scale_tot_adult]
                outputs_Npos_M_older[year] += [PosM_older*scale_tot_adult]
                outputs_Npos_F_younger[year] += [PosF_younger*scale_tot_adult]
                outputs_Npos_F_older[year] += [PosF_older*scale_tot_adult]
                
                outputs_Npos_M15plus[year] += [NposM15plus*scale_tot_adult]
                outputs_Npos_F15plus[year] += [NposF15plus*scale_tot_adult]
                
                
                outputs_prevalence_M15_49[year] += [PosM15_49/(1.0*NpopM15_49)]
                outputs_prevalence_M_younger[year] += [PosM_younger/(1.0*NpopM_younger)]
                outputs_prevalence_M_older[year] += [PosM_older/(1.0*NpopM_older)]

                outputs_prevalence_F15_49[year] += [PosF15_49/(1.0*NpopF15_49)]
                outputs_prevalence_F_younger[year] += [PosF_younger/(1.0*NpopF_younger)]
                outputs_prevalence_F_older[year] += [PosF_older/(1.0*NpopF_older)]

                outputs_prevalence_overall15_49[year] += [(PosM15_49+PosF15_49)/(1.0*(NpopM15_49+NpopF15_49))]

                
                outputs_N_ART_M15plus[year] += [artM15plus*scale_tot_adult]
                outputs_N_ART_F15plus[year] += [artF15plus*scale_tot_adult]

                outputs_ARTcoverage_M15plus[year] += [artM15plus/(1.0*NposM15plus+ERR)]
                outputs_ARTcoverage_F15plus[year] += [artF15plus/(1.0*NposF15plus+ERR)]
                outputs_DiagOnART_M15plus[year] += [artM15plus/(1.0*NawareM15plus+ERR)]

                outputs_DiagOnART_F15plus[year] += [artF15plus/(1.0*NawareF15plus+ERR)]

                
                outputs_Ncirc_15_49[year] += [Ncirc_15_49*scale_tot_adult] 
                outputs_propcirc_15_49[year] += [Ncirc_15_49/(1.0*NpopM15_49)]

                outputs_prop_diagnosed_M15plus[year] += [NawareM15plus/(1.0*NposM15plus+ERR)]
                outputs_prop_diagnosed_F15plus[year] += [NawareF15plus/(1.0*NposF15plus+ERR)]


                outputs_prop_VS_adult15plus[year] += [(N_VSM15plus+N_VSF15plus)/(1.0*(artM15plus+artF15plus+ERR))]
                
                ### Flow measures:
                ##############################

                outputs_Ncumulativecases_M_younger[year] += [N_newHIVinfections_15to24_male*scale_tot_adult]
                outputs_Ncumulativecases_M_older[year] += [N_newHIVinfections_25to49_male*scale_tot_adult]
                outputs_Ncumulativecases_M15_49[year] += [(N_newHIVinfections_15to24_male+N_newHIVinfections_25to49_male)*scale_tot_adult]
                
                outputs_Ncumulativecases_F_younger[year] += [N_newHIVinfections_15to24_female*scale_tot_adult]
                outputs_Ncumulativecases_F_older[year] += [N_newHIVinfections_25to49_female*scale_tot_adult]
                outputs_Ncumulativecases_F15_49[year] += [(N_newHIVinfections_15to24_female+N_newHIVinfections_25to49_female)*scale_tot_adult]
                


                #outputs_cumulativeAIDSdeaths_M15plus[year] += [N_AIDSdeaths_15plus_male*scale_tot_adult]
                #outputs_cumulativeAIDSdeaths_F15plus[year] += [N_AIDSdeaths_15plus_female*scale_tot_adult]

                #outputs_cumulativetotaldeaths_M20_59[year] += [N_deaths_20_59_male*scale_tot_adult]
                #outputs_cumulativetotaldeaths_F20_59[year] += [N_deaths_20_59_female*scale_tot_adult]
                #outputs_cumulativeNtests_M15plus[year] += [N_HIVtests_15plus_male*scale_tot_adult]
                #outputs_cumulativeNtests_F15plus[year] += [N_HIVtests_15plus_female*scale_tot_adult]
                #outputs_cumulativeNdiagnoses[year] += [N_newHIVdiagnoses_15plus*scale_tot_adult]

                outputs_VMMC_cumulative15_49[year] += [N_VMMC_op_cumulative*scale_tot_adult]





    ##################################################################
    # Now make annual outputs from cumulative ones:
    ##################################################################

    outputs_Nincidentcases_M15_49 = get_annual_from_cumulative(outputs_Ncumulativecases_M15_49)
    outputs_Nincidentcases_M_younger = get_annual_from_cumulative(outputs_Ncumulativecases_M_younger)
    outputs_Nincidentcases_M_older = get_annual_from_cumulative(outputs_Ncumulativecases_M_older)
    outputs_Nincidentcases_F15_49 = get_annual_from_cumulative(outputs_Ncumulativecases_F15_49)
    outputs_Nincidentcases_F_younger = get_annual_from_cumulative(outputs_Ncumulativecases_F_younger)
    outputs_Nincidentcases_F_older = get_annual_from_cumulative(outputs_Ncumulativecases_F_older)
    
    outputs_Nincidentcases_adult15_49 = sum_two_outputs(outputs_Nincidentcases_M15_49,outputs_Nincidentcases_F15_49)

    outputs_incidence_M15_49 = calculate_incidence(outputs_Nincidentcases_M15_49,outputs_Npop_M15_49,outputs_Npos_M15_49)
    outputs_incidence_F15_49 = calculate_incidence(outputs_Nincidentcases_F15_49,outputs_Npop_F15_49,outputs_Npos_F15_49)
    outputs_incidence_M_younger = calculate_incidence(outputs_Nincidentcases_M_younger,outputs_Npop_M_younger,outputs_Npos_M_younger)
    outputs_incidence_M_older = calculate_incidence(outputs_Nincidentcases_M_older,outputs_Npop_M_older,outputs_Npos_M_older)
    outputs_incidence_F_younger = calculate_incidence(outputs_Nincidentcases_F_younger,outputs_Npop_F_younger,outputs_Npos_F_younger)
    outputs_incidence_F_older = calculate_incidence(outputs_Nincidentcases_F_older,outputs_Npop_F_older,outputs_Npos_F_older)

    outputs_incidence_adult15_49 = calculate_incidence(outputs_Nincidentcases_adult15_49,outputs_Npop15_49,outputs_Npos15_49)


    

                
    #outputs_totaldeaths_M20_59 = get_annual_from_cumulative(outputs_cumulativetotaldeaths_M20_59)
    #outputs_totaldeaths_F20_59 = get_annual_from_cumulative(outputs_cumulativetotaldeaths_F20_59)
    #outputs_totaldeaths_adult20_59 = sum_two_outputs(outputs_totaldeaths_M20_59,outputs_totaldeaths_F20_59)

    #outputs_Ntests_M15plus = get_annual_from_cumulative(outputs_cumulativeNtests_M15plus)
    #outputs_Ntests_F15plus = get_annual_from_cumulative(outputs_cumulativeNtests_F15plus)
    #outputs_annualNdiagnoses = get_annual_from_cumulative(outputs_cumulativeNdiagnoses)


    outputs_VMMC_annual15_49 = get_annual_from_cumulative(outputs_VMMC_cumulative15_49)
    


    ## Now make annual number of VMMC:
    #outputs_circ=get_annual_from_cumulative(outputs_circ_cumulative15_49)

    outdir = "checks/"
    if(not(os.path.isdir(outdir))):
        try:
            os.makedirs(outdir)
        except:
            print("Error - need to make directory ",outdir)
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
    



                

    outputs_to_store = {"Npop15_49":outputs_Npop15_49,
                        "Npop_15plus":outputs_Npop_15plus,
                        "Npop_M15plus":outputs_Npop_M15plus,
                        "Npop_F15plus":outputs_Npop_F15plus,
                        "PrevalenceM15_49":outputs_prevalence_M15_49,
                        "PrevalenceF15_49":outputs_prevalence_F15_49,
                        "PrevalenceAll15_49":outputs_prevalence_overall15_49,
                        "N_ART_M_15plus":outputs_N_ART_M15plus,
                        "N_ART_F_15plus":outputs_N_ART_F15plus,
                        "ARTcoverage_M_15plus":outputs_ARTcoverage_M15plus,
                        "ARTcoverage_F_15plus":outputs_ARTcoverage_F15plus,
                        "Diagnosed_onART_M_15plus":outputs_DiagOnART_M15plus,
                        "Diagnosed_onART_F_15plus":outputs_DiagOnART_F15plus,
                        "N_VMMC_annual_15_49":outputs_VMMC_annual15_49,
                        "N_circ_15_49":outputs_Ncirc_15_49,
                        "prop_circ_15_49":outputs_propcirc_15_49,
                        "PropDiagnosed_M15plus":outputs_prop_diagnosed_M15plus,
                        "PropDiagnosed_F15plus":outputs_prop_diagnosed_F15plus,
                        "PropAdultVS":outputs_prop_VS_adult15plus,
                
                        "New_cases_M15_49":outputs_Nincidentcases_M15_49,
                        "New_cases_M15_29":outputs_Nincidentcases_M_younger,
                        "New_cases_M30_54":outputs_Nincidentcases_M_older,
                        "New_cases_F15_49":outputs_Nincidentcases_F15_49,
                        "New_cases_F15_24":outputs_Nincidentcases_F_younger,
                        "New_cases_F25_54":outputs_Nincidentcases_F_older,
                        "New_cases_total15_49":outputs_Nincidentcases_adult15_49,
                        "IncidenceM15_49":outputs_incidence_M15_49,
                        "IncidenceF15_49":outputs_incidence_F15_49,
                        "Incidencetotal15_49":outputs_incidence_adult15_49,
                        "Npos_M15plus":outputs_Npos_M15plus,
                        "Npos_F15plus":outputs_Npos_F15plus,
                        "PrevalenceM15_29":outputs_prevalence_M_younger,
                        "PrevalenceM30_54":outputs_prevalence_M_older,
                        "PrevalenceF15_24":outputs_prevalence_F_younger,
                        "PrevalenceF25_54":outputs_prevalence_F_older,
                        "IncidenceM15_29":outputs_incidence_M_younger,
                        "IncidenceM30_54":outputs_incidence_M_older,
                        "IncidenceF15_24":outputs_incidence_F_younger,
                        "IncidenceF25_54":outputs_incidence_F_older,
                        "Npop_M15_29":outputs_Npop_M_younger,
                        "Npop_M30_54":outputs_Npop_M_older,
                        "Npop_F15_24":outputs_Npop_F_younger,
                        "Npop_F25_54":outputs_Npop_F_older

                        
    }

                        
    


                        

    list_of_outputs = ["PrevalenceM15_49","PrevalenceF15_49","PrevalenceAll15_49","ARTcoverage_M_15plus","ARTcoverage_F_15plus","N_ART_M_15plus","N_ART_F_15plus","prop_circ_15_49","N_VMMC_annual_15_49",
                       "PropDiagnosed_M15plus","PropDiagnosed_F15plus","PropAdultVS","Npop_15plus","Npop_M15plus","Npop_F15plus","Npop15_49","Diagnosed_onART_M_15plus","Diagnosed_onART_F_15plus",
                       "New_cases_M15_49","New_cases_F15_49","New_cases_total15_49","IncidenceM15_49","IncidenceF15_49","Incidencetotal15_49",
                       "Npos_M15plus","Npos_F15plus","PrevalenceM15_29","PrevalenceF15_24","PrevalenceM30_54","PrevalenceF25_54",
                       "IncidenceM15_29","IncidenceF15_24","IncidenceM30_54","IncidenceF25_54",
                       "New_cases_M15_29","New_cases_F15_24","New_cases_M30_54","New_cases_F25_54"
    ]
                        

    #,"Prevalence_child"

    make_mean_CI(outputs_to_store,list_of_outputs,outfilename)
    

    


    
##################################
# Main code:
##################################

#manicalandfiledir = "params/Output/"
#manicalandfiledir = "param_cond_M15_29_remove_barriers/Output/"

PrEPinterventionparamdirs = glob.glob("param_PrEP_[MF]*")
VMMCinterventionparamdirs = glob.glob("param_VMMC_[MF]*")
Condinterventionparamdirs = glob.glob("param_cond_[MF]*")

AllPopinterventionparamdirs = glob.glob("param_*_all_priority_pops_*")

interventionparamdirs = PrEPinterventionparamdirs +  VMMCinterventionparamdirs +Condinterventionparamdirs + AllPopinterventionparamdirs


# Create summary files for each directory in alldirs:
alldirs = [d +"/Output/" for d in interventionparamdirs] + ["params/Output/"]


# This is where the summary files are stored - make the directory if it doesn't already exist:
outputdir="Summary_files_for_plotting/"
if not os.path.exists(outputdir):
    os.makedirs(outputdir)

# Now loop through alldirs, generating the summary files:    
for manicalandfiledir in alldirs:

    # Sort out how the files are named:
    if(manicalandfiledir=="params/Output/"):
        intervention_tag="_baseline"
        file_tag = "_0.csv"    
    else:
        intervention_tag=manicalandfiledir.split("/")[0].replace("param_","")
        if(intervention_tag[0:4]=="cond" and intervention_tag[-11:]=="allbarriers"):
            file_tag = "_0PrEP1_VMMC1_cond0.csv"
        elif(intervention_tag[0:4]=="cond" and intervention_tag[-11:]!="allbarriers"):
            file_tag = "_0PrEP1_VMMC1_cond1.csv"
        elif(intervention_tag[0:9]=="All_tools" and intervention_tag[-11:]!="allbarriers"):
            file_tag = "_0PrEP1_VMMC1_cond1.csv"
        elif(intervention_tag[0:4]!="cond"):
            file_tag = "_0PrEP1_VMMC1_cond0.csv"

    # For checking if needed:
    print("Hey",manicalandfiledir,intervention_tag,file_tag)


    read_HIVpreventioncascade_files(manicalandfiledir,outputdir+"HIVpreventioncascade"+intervention_tag+".csv",file_tag)

# This function looks in manicalandfiledir for all the MIHPSA_Output*.csv files and makes an output file for the Manicaland project.
    read_manicaland_files_and_make_summary_file(manicalandfiledir,outputdir+"MANICALAND_project_outputs_stage1"+intervention_tag+".csv",file_tag)
