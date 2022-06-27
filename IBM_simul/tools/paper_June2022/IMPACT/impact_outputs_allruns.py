# Adapted from get_mihpsa_project_outputs_vX.py
# Gets Manicaland-specific outputs for a large number of runs..

import glob, sys, os, math
import numpy


# Need to scale the IBM population to the total population of Zimbabwe. Right now we use the 2021 index:
Manicaland_population_scale_adult_year = 2012 # Zimbabwe census
Manicaland_population_scale_adult =  978747 # Table 6.9b C:\Users\mpickles\Dropbox (SPH Imperial College)\Covid_19\Parameters\Demographics\Zimbabwe2012_census_National_Report.pdf. Total pop (inc children) is 1752698, so 44.2% are children <15 (compared to national average of 41%).




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

    i_NpopM15_29 = header.index('NPop_15to29_male')
    i_NpopM30_54 = header.index('NPop_30to54_male')
    i_NpopF15_24 = header.index('NPop_15to24_female')
    i_NpopF25_49 = header.index('NPop_25to54_female')

    i_PosM15_49 =  header.index('NPos_15to49_male')
    i_PosF15_49 =  header.index('NPos_15to49_female')

    i_PosM15_29 = header.index('NPos_15to29_male')
    i_PosM30_54 = header.index('NPos_30to54_male')
    i_PosF15_24 = header.index('NPos_15to24_female')
    i_PosF25_49 = header.index('NPos_25to54_female')

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

    
    return [i_NpopM15_49,i_NpopF15_49,i_NpopM15_29,i_NpopF15_24,i_NpopM30_54,i_NpopF25_49,i_PosM15_49,i_PosF15_49,i_PosM15_29,i_PosF15_24,i_PosM30_54,i_PosF25_49,i_artM15plus,i_artF15plus,i_NpopM15plus,i_NpopF15plus,i_circ,i_NposM15plus,i_NposF15plus,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_newHIVinfections_15to24_male,i_N_newHIVinfections_25to49_male,i_N_newHIVinfections_15to24_female,i_N_newHIVinfections_25to49_female,i_N_newHIVdiagnoses_15plus,i_VMMC_op]






# For each run we need to generate a multiplier to make the population about the same size as Manicaland (we scale to Manicaland_population_scale_adult in the year Manicaland_population_scale_adult_year):
def get_pop_scale(manicaland_model_data,i_NpopM15_49,i_NpopM15plus,i_NpopF15plus):

    for line in manicaland_model_data:
        year = int(line.split(",")[0])
        if(year==Manicaland_population_scale_adult_year):
            line_data = line.split(",")
            
            pop_tot_adult = int(line_data[i_NpopM15plus]) + int(line_data[i_NpopF15plus])
            scale_tot_adult = Manicaland_population_scale_adult / (1.0*pop_tot_adult)
            break

    return scale_tot_adult


def write_output(outputs,outfile):
    outstring = ""
    #years_saved = outputs.keys()
    #years_saved.sort()
    years_saved = sorted(output1)
    
    for year in years_saved:
        outstring += str(year)+","
        for run_output in outputs[year]:
            outstring += str(run_output)+","
        outstring = outstring.rstrip(",") +"\n"
        

    outfile = open(outfile,"w")
    outfile.write(outstring)
    outfile.close()

def get_annual_from_cumulative(outputs_cumulative):
    #years = outputs_cumulative.keys()
    #years.sort()
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
    #years = output1.keys()
    #years.sort()
    years = sorted(output1)
    outputs_summed = {}
    #outputs_summed[years[0]] = [0]*len(output1[years[0]])
    for y in range(len(years)):
        outputs_summed[years[y]] = [output1[years[y]][i]+output2[years[y]][i] for i in range(len(output1[years[y]]))]

    return outputs_summed



def sum_three_outputs(output1,output2,output3):
    #years = output1.keys()
    #years.sort()
    years = sorted(output1)
    outputs_summed = {}
    #outputs_summed[years[0]] = [0]*len(output1[years[0]])
    for y in range(len(years)):
        outputs_summed[years[y]] = [output1[years[y]][i]+output2[years[y]][i]+output3[years[y]][i] for i in range(len(output1[years[y]]))]

    return outputs_summed
    

def calculate_incidence(N_newinfections,Npop,Npos):
    #years_saved = sorted(outputs)
    #years_saved = outputs.keys()
    #years_saved.sort()

    years = sorted(N_newinfections)
    #years.sort()
    incidence = {}
    #incidence[years[0]] = [0]*len(N_newinfections[years[0]])
    for y in range(len(years)):
        #print y, len(N_newinfections[years[y]]),len(Npop),len(Npos)
        incidence[years[y]] = [N_newinfections[years[y]][i] / (Npop[years[y]][i] - Npos[years[y]][i]) for i in range(len(N_newinfections[years[y]]))]
    return incidence

def get_quotient(output1,output2,ERR):
    #years = output1.keys()
    #years.sort()
    years = sorted(output1)
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


        

def read_manicaland_files(manicalandfiledir,file_tag):

    ERR=1e-12
    
    manicalandfiles = glob.glob(manicalandfiledir + "/MIHPSA_output_CL*"+file_tag)
    manicalandfiles.sort()
    if manicalandfiles==[]:
        print(manicalandfiledir + "/MIHPSA_output_CL*"+file_tag)
    
    [i_NpopM15_49,i_NpopF15_49,i_NpopM15_29,i_NpopF15_24,i_NpopM30_54,i_NpopF25_49,i_PosM15_49,i_PosF15_49,i_PosM15_29,i_PosF15_24,i_PosM30_54,i_PosF25_49,i_artM15plus,i_artF15plus,i_NpopM15plus,i_NpopF15plus,i_circ,i_NposM15plus,i_NposF15plus,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_newHIVinfections_15to24_male,i_N_newHIVinfections_25to49_male,i_N_newHIVinfections_15to24_female,i_N_newHIVinfections_25to49_female,i_N_newHIVdiagnoses_15plus,i_VMMC_op] = read_Manicaland_header(manicalandfiles[0])

    
    outputs_prevalence_M15_49 = {}
    outputs_prevalence_M15_29 = {}
    outputs_prevalence_M30_54 = {}
    outputs_prevalence_F15_49 = {}
    outputs_prevalence_F15_24 = {}
    outputs_prevalence_F25_49 = {}
    outputs_prevalence_overall15_49 = {}
    
    outputs_Npop_M15_49 = {}
    outputs_Npop_F15_49 = {}
    outputs_Npop_M15_29 = {}
    outputs_Npop_M30_54 = {}
    outputs_Npop_F15_24 = {}
    outputs_Npop_F25_49 = {}
    outputs_Npop15_49 = {}

    outputs_Npop_15plus = {}
    outputs_Npop_M15plus = {}
    outputs_Npop_F15plus = {}

    outputs_Npos_M15_49 = {}
    outputs_Npos_F15_49 = {}

    outputs_Npos_M15_29 = {}
    outputs_Npos_M30_54 = {}
    outputs_Npos_F15_24 = {}
    outputs_Npos_F25_49 = {}


    outputs_Npos_M15plus = {}
    outputs_Npos_F15plus = {}


    outputs_Npos15_49 = {}


    outputs_Ncumulativecases_M15_49 = {}
    outputs_Ncumulativecases_M15_29 = {}
    outputs_Ncumulativecases_M30_54 = {}
    outputs_Ncumulativecases_F15_49 = {}
    outputs_Ncumulativecases_F15_24 = {}
    outputs_Ncumulativecases_F25_49 = {}
    outputs_Ncumulativecases_adult15_49 = {}
    
    
    # Process each of the Manicaland output files:
    for n,f in enumerate(manicalandfiles):

        # Read the data from a single file (header is not used)
        run_data = read_data(f)
        
        scale_tot_adult = get_pop_scale(run_data,i_NpopM15_49,i_NpopM15plus,i_NpopF15plus)


        for i,line in enumerate(run_data):

            [year,NpopM15_49,NpopF15_49,NpopM15_29,NpopF15_24,NpopM30_54,NpopF25_49,PosM15_49,PosF15_49,PosM15_29,PosF15_24,PosM30_54,PosF25_49,artM15plus,artF15plus,NpopM15plus,NpopF15plus,Ncirc_15_49,NposM15plus,NposF15plus,NawareM15plus,NawareF15plus,NonARTM15plus,NonARTF15plus,N_VSM15plus,N_VSF15plus,N_newHIVinfections_15to24_male,N_newHIVinfections_25to49_male,N_newHIVinfections_15to24_female,N_newHIVinfections_25to49_female,N_newHIVdiagnoses_15plus,N_VMMC_op_cumulative] = [int(line.split(",")[index]) for index in [0,i_NpopM15_49,i_NpopF15_49,i_NpopM15_29,i_NpopF15_24,i_NpopM30_54,i_NpopF25_49,i_PosM15_49,i_PosF15_49,i_PosM15_29,i_PosF15_24,i_PosM30_54,i_PosF25_49,i_artM15plus,i_artF15plus,i_NpopM15plus,i_NpopF15plus,i_circ,i_NposM15plus,i_NposF15plus,i_NawareM15plus,i_NawareF15plus,i_NonARTM15plus,i_NonARTF15plus,i_N_VSM15plus,i_N_VSF15plus,i_N_newHIVinfections_15to24_male,i_N_newHIVinfections_25to49_male,i_N_newHIVinfections_15to24_female,i_N_newHIVinfections_25to49_female,i_N_newHIVdiagnoses_15plus,i_VMMC_op]]
            if(n==0):


    # UNAIDS definition of ART coverage: Percentage of people living with HIV currently receiving ART among the estimated number of adults and children living with HIV
                outputs_prevalence_M15_49[year] = [PosM15_49/(1.0*NpopM15_49)]

                outputs_prevalence_M15_29[year] = [PosM15_29/(1.0*NpopM15_29)]
                outputs_prevalence_M30_54[year] = [PosM30_54/(1.0*NpopM30_54)]

                outputs_prevalence_F15_49[year] = [PosF15_49/(1.0*NpopF15_49)]

                outputs_prevalence_F15_24[year] = [PosF15_24/(1.0*NpopF15_24)]
                outputs_prevalence_F25_49[year] = [PosF25_49/(1.0*NpopF25_49)]

                outputs_prevalence_overall15_49[year] = [(PosM15_49+PosF15_49)/(1.0*(NpopM15_49+NpopF15_49))]

                
                outputs_Npop_M15_49[year] = [NpopM15_49*scale_tot_adult]
                outputs_Npop_F15_49[year] = [NpopF15_49*scale_tot_adult]
                outputs_Npop15_49[year] = [(NpopM15_49+NpopF15_49)*scale_tot_adult]

                outputs_Npop_M15_29[year] = [NpopM15_29*scale_tot_adult]
                outputs_Npop_M30_54[year] = [NpopM30_54*scale_tot_adult]
                outputs_Npop_F15_24[year] = [NpopF15_24*scale_tot_adult]
                outputs_Npop_F25_49[year] = [NpopF25_49*scale_tot_adult]


                outputs_Npop_15plus[year] = [(NpopM15plus+NpopF15plus)*scale_tot_adult]
                outputs_Npop_M15plus[year] = [NpopM15plus*scale_tot_adult]
                outputs_Npop_F15plus[year] = [NpopF15plus*scale_tot_adult]

                
                outputs_Npos_M15_49[year] = [PosM15_49*scale_tot_adult]
                outputs_Npos_F15_49[year] = [PosF15_49*scale_tot_adult]
                outputs_Npos15_49[year] = [(PosM15_49+PosF15_49)*scale_tot_adult]

                outputs_Npos_M15_29[year] = [PosM15_29*scale_tot_adult]
                outputs_Npos_M30_54[year] = [PosM30_54*scale_tot_adult]
                outputs_Npos_F15_24[year] = [PosF15_24*scale_tot_adult]
                outputs_Npos_F25_49[year] = [PosF25_49*scale_tot_adult]
                
                outputs_Npos_M15plus[year] = [NposM15plus*scale_tot_adult]
                outputs_Npos_F15plus[year] = [NposF15plus*scale_tot_adult]
                



                outputs_Ncumulativecases_M15_29[year] = [N_newHIVinfections_15to24_male*scale_tot_adult]
                outputs_Ncumulativecases_M30_54[year] = [N_newHIVinfections_25to49_male*scale_tot_adult]

                outputs_Ncumulativecases_F15_24[year] = [N_newHIVinfections_15to24_female*scale_tot_adult]
                outputs_Ncumulativecases_F25_49[year] = [N_newHIVinfections_25to49_female*scale_tot_adult]

                outputs_Ncumulativecases_M15_49[year] = [(N_newHIVinfections_15to24_male+N_newHIVinfections_25to49_male)*scale_tot_adult]
                outputs_Ncumulativecases_F15_49[year] = [(N_newHIVinfections_15to24_female+N_newHIVinfections_25to49_female)*scale_tot_adult]
                
                outputs_Ncumulativecases_adult15_49[year] = [(N_newHIVinfections_15to24_male+N_newHIVinfections_25to49_male+N_newHIVinfections_15to24_female+N_newHIVinfections_25to49_female)*scale_tot_adult]

                
            else:
                outputs_Npop_M15_49[year] += [NpopM15_49*scale_tot_adult]
                outputs_Npop_F15_49[year] += [NpopF15_49*scale_tot_adult]
                outputs_Npop_M15_29[year] += [NpopM15_29*scale_tot_adult]
                outputs_Npop_M30_54[year] += [NpopM30_54*scale_tot_adult]
                outputs_Npop_F15_24[year] += [NpopF15_24*scale_tot_adult]
                outputs_Npop_F25_49[year] += [NpopF25_49*scale_tot_adult]

                outputs_Npop15_49[year] += [(NpopM15_49+NpopF15_49)*scale_tot_adult]
                outputs_Npop_15plus[year] += [(NpopM15plus+NpopF15plus)*scale_tot_adult]
                outputs_Npop_M15plus[year] += [NpopM15plus*scale_tot_adult]
                outputs_Npop_F15plus[year] += [NpopF15plus*scale_tot_adult]
                
                
                outputs_Npos_M15_49[year] += [PosM15_49*scale_tot_adult]
                outputs_Npos_F15_49[year] += [PosF15_49*scale_tot_adult]
                outputs_Npos15_49[year] += [(PosM15_49+PosF15_49)*scale_tot_adult]

                outputs_Npos_M15_29[year] += [PosM15_29*scale_tot_adult]
                outputs_Npos_M30_54[year] += [PosM30_54*scale_tot_adult]
                outputs_Npos_F15_24[year] += [PosF15_24*scale_tot_adult]
                outputs_Npos_F25_49[year] += [PosF25_49*scale_tot_adult]
                
                outputs_Npos_M15plus[year] += [NposM15plus*scale_tot_adult]
                outputs_Npos_F15plus[year] += [NposF15plus*scale_tot_adult]
                
                
                outputs_prevalence_M15_49[year] += [PosM15_49/(1.0*NpopM15_49)]
                outputs_prevalence_M15_29[year] += [PosM15_29/(1.0*NpopM15_29)]
                outputs_prevalence_M30_54[year] += [PosM30_54/(1.0*NpopM30_54)]

                outputs_prevalence_F15_49[year] += [PosF15_49/(1.0*NpopF15_49)]
                outputs_prevalence_F15_24[year] += [PosF15_24/(1.0*NpopF15_24)]
                outputs_prevalence_F25_49[year] += [PosF25_49/(1.0*NpopF25_49)]

                outputs_prevalence_overall15_49[year] += [(PosM15_49+PosF15_49)/(1.0*(NpopM15_49+NpopF15_49))]

                

                outputs_Ncumulativecases_M15_29[year] += [N_newHIVinfections_15to24_male*scale_tot_adult]
                outputs_Ncumulativecases_M30_54[year] += [N_newHIVinfections_25to49_male*scale_tot_adult]
                outputs_Ncumulativecases_M15_49[year] += [(N_newHIVinfections_15to24_male+N_newHIVinfections_25to49_male)*scale_tot_adult]
                
                outputs_Ncumulativecases_F15_24[year] += [N_newHIVinfections_15to24_female*scale_tot_adult]
                outputs_Ncumulativecases_F25_49[year] += [N_newHIVinfections_25to49_female*scale_tot_adult]
                outputs_Ncumulativecases_F15_49[year] += [(N_newHIVinfections_15to24_female+N_newHIVinfections_25to49_female)*scale_tot_adult]
                
                outputs_Ncumulativecases_adult15_49[year] += [(N_newHIVinfections_15to24_male+N_newHIVinfections_25to49_male+N_newHIVinfections_15to24_female+N_newHIVinfections_25to49_female)*scale_tot_adult]

    ##################################################################
    # Now make annual outputs from cumulative ones:
    ##################################################################

    outputs_Nincidentcases_M15_49 = get_annual_from_cumulative(outputs_Ncumulativecases_M15_49)
    outputs_Nincidentcases_F15_49 = get_annual_from_cumulative(outputs_Ncumulativecases_F15_49)
    outputs_Nincidentcases_adult15_49 = sum_two_outputs(outputs_Nincidentcases_M15_49,outputs_Nincidentcases_F15_49)

    outputs_incidence_adult15_49 = calculate_incidence(outputs_Nincidentcases_adult15_49,outputs_Npop15_49,outputs_Npos15_49)




                
    outputs_to_store = {"Npop15_49":outputs_Npop15_49,
                        "Npop_15plus":outputs_Npop_15plus,
                        "Npop_M15plus":outputs_Npop_M15plus,
                        "Npop_F15plus":outputs_Npop_F15plus,
                        "PrevalenceM15_49":outputs_prevalence_M15_49,
                        "PrevalenceF15_49":outputs_prevalence_F15_49,
                        "PrevalenceAll15_49":outputs_prevalence_overall15_49,
                        "Cumulative_cases_M15_49":outputs_Ncumulativecases_M15_49,
                        "Cumulative_cases_M15_29":outputs_Ncumulativecases_M15_29,
                        "Cumulative_cases_M30_54":outputs_Ncumulativecases_M30_54,
                        "Cumulative_cases_F15_49":outputs_Ncumulativecases_F15_49,
                        "Cumulative_cases_F15_24":outputs_Ncumulativecases_F15_24,
                        "Cumulative_cases_F25_49":outputs_Ncumulativecases_F25_49,
                        "Cumulative_cases_total15_49":outputs_Ncumulativecases_adult15_49,
                        "Npos_M15plus":outputs_Npos_M15plus,
                        "Npos_F15plus":outputs_Npos_F15plus,
                        "PrevalenceM15_29":outputs_prevalence_M15_29,
                        "PrevalenceM30_54":outputs_prevalence_M30_54,
                        "PrevalenceF15_24":outputs_prevalence_F15_24,
                        "PrevalenceF25_49":outputs_prevalence_F25_49,
                        "Npop_M15_29":outputs_Npop_M15_29,
                        "Npop_M30_54":outputs_Npop_M30_54,
                        "Npop_F15_24":outputs_Npop_F15_24,
                        "Npop_F25_49":outputs_Npop_F25_49,
                        "incidence_adult15_49":outputs_incidence_adult15_49

                        
    }

                        
    

    return outputs_to_store
                        

def get_n_infections(dataset,population,year):
    return dataset[population][year]


def get_impact(baseline,intervention,population,timespan):
    baseline_ninfections_2020 = get_n_infections(baseline,population,2020)
    intervention_ninfections_2020 = get_n_infections(intervention,population,2020)
    if not(baseline_ninfections_2020==intervention_ninfections_2020):
        print("Mismatch in ninfections in 2020. Exiting\n")
        sys.exit(1)

    baseline_ninfections_year0 = get_n_infections(baseline,population,2020)
    baseline_ninfections_yearN = get_n_infections(baseline,population,2020+timespan)
    
    intervention_ninfections = get_n_infections(intervention,population,2020+timespan)
        
    infections_averted = []
    prop_infections_averted = []
    baseline_infections = []
    for run in range(len(baseline_ninfections_yearN)):
        Ninfections_thisrun_baseline = baseline_ninfections_yearN[run] - baseline_ninfections_year0[run]
        infections_averted += [baseline_ninfections_yearN[run] - intervention_ninfections[run]]
        prop_infections_averted += [(baseline_ninfections_yearN[run] - intervention_ninfections[run])/(Ninfections_thisrun_baseline*1.0)]

        baseline_infections += [Ninfections_thisrun_baseline]
        
    return [infections_averted,prop_infections_averted,baseline_infections]



####################################################################
# Main code:
####################################################################




PrEPinterventionparamdirs = glob.glob("param_PrEP_[MF]*")
VMMCinterventionparamdirs = glob.glob("param_VMMC_[MF]*")
Condinterventionparamdirs = glob.glob("param_cond_[MF]*")
AllToolsinterventionparamdirs = glob.glob("param_All_tools_[MF]*")

AllPopinterventionparamdirs = glob.glob("param_[APVc]*_all_priority_pops_*")

interventionparamdirs = PrEPinterventionparamdirs +  VMMCinterventionparamdirs +Condinterventionparamdirs + AllToolsinterventionparamdirs + AllPopinterventionparamdirs

#print("Using data from",interventionparamdirs)


# Load the data:

baseline = read_manicaland_files("params/Output/","_0.csv")
#baseline = read_manicaland_files("param_VMMC_M15_29_allbarriers/Output/","_0PrEP1_VMMC1_cond1.csv")

intervention_data = {}

for dir in interventionparamdirs:
    # This function looks in manicalandfiledir for all the MIHPSA_Output*.csv files
    # If not condom intervention, then keep the intervention off (otherwise we redraw condomless partnerships, even if the probability is the same, which means the model outputs won't match the counterfactual). 
    if (dir.find("param_cond")>=0 or dir.find("param_All_tools")>=0):
        print(dir,dir.find("param_cond"))
        if dir.find("allbarriers")>=0: # for counterfactual, still keep cond index 0:
            file_tag = "PrEP1_VMMC1_cond0"
        else:
            file_tag = "PrEP1_VMMC1_cond1"
    else:
        file_tag = "PrEP1_VMMC1_cond0"

    intervention_data[dir] = read_manicaland_files(dir+"/Output/","_0"+file_tag+".csv")


SEP = ","

stored_impact_prop = {}
stored_impact_Ninf = {}   # Reduction in number of infections due to intervention.

timescales = [5,10]
for t in timescales:
    stored_impact_prop[t] = {} 
    stored_impact_Ninf[t] = {} 


    
for pop in ["Cumulative_cases_total15_49"]:
    for timescale in timescales:
        outstring = SEP.join(["Scenario","Timescale","Outcome","Median_Ninf_averted","LL_Ninf_averted","UL_Ninf_averted","Median_propinf_averted","LL_propinf_averted","UL_propinf_averted","Median_Ninf_baseline","LL_Ninf_baseline","UL_Ninf_baseline"])+"\n"
        for dir in interventionparamdirs:
            [infections_averted,prop_infections_averted,number_infections_baseline] = get_impact(baseline,intervention_data[dir],pop,timescale)

            stored_impact_prop[timescale][dir] = numpy.median(prop_infections_averted)
            stored_impact_Ninf[timescale][dir] = numpy.median(infections_averted)
            
            outstring += dir + SEP + str(timescale)+SEP+ pop + SEP
            outstring += str(numpy.median(infections_averted))+SEP+str(numpy.percentile(infections_averted,5))+SEP+str(numpy.percentile(infections_averted,95))+SEP+str(numpy.median(prop_infections_averted))+SEP+str(numpy.percentile(prop_infections_averted,5))+SEP+str(numpy.percentile(prop_infections_averted,95))+SEP
            outstring += str(numpy.median(number_infections_baseline))+SEP+str(numpy.percentile(number_infections_baseline,5))+SEP+str(numpy.percentile(number_infections_baseline,95))
            outstring += "\n"
        outfilename = "IMPACT_"+pop+"_"+str(timescale)+"Year.csv"
        outfile = open(outfilename,"w")
        outfile.write(outstring)
        outfile.close()
        
#print(outstring)
#print(stored_impact_prop)


prevention_methods = ["PrEP","VMMC","cond","All_tools"]
#prevention_methods = ["PrEP"]

dictionary_agegroups = {"PrEP":['M15_29','M30_54','F15_24','F25_54','all_priority_pops'],"VMMC":['M15_29','M30_54','all_priority_pops'],"cond":['M15_29','M30_54','F15_24','F25_54','all_priority_pops'],"All_tools":['all_priority_pops']}

intervention_scenarios = ["allbarriers","increase_motivation","increase_access","increase_effuse","remove_barriers"]
outstring_heatmap_matrix_prop_inf = ""
outstring_heatmap_matrix_Ninf = ""
outstring_heatmap_matrix_incidence = ""

for timescale in [10]:
    for tool in prevention_methods:
        for barrier_removed in intervention_scenarios:
            for pop in dictionary_agegroups[tool]:
                dir = "param_"+tool+"_"+pop+"_"+barrier_removed
                outstring_heatmap_matrix_prop_inf += tool+","+barrier_removed+","+pop+","+str(stored_impact_prop[timescale][dir])+"\n"
                outstring_heatmap_matrix_Ninf += tool+","+barrier_removed+","+pop+","+str(stored_impact_Ninf[timescale][dir])+"\n"
                outstring_heatmap_matrix_incidence += tool+","+barrier_removed+","+pop+","+str(numpy.median(intervention_data[dir]["incidence_adult15_49"][2030]))+"\n"
                #print(dir,stored_impact_prop[timescale][dir])
            #print()
            outstring_heatmap_matrix_prop_inf += "\n"
            outstring_heatmap_matrix_Ninf += "\n"
            outstring_heatmap_matrix_incidence += "\n"
        
heatmap_filename = "prop_infections_heatmap.csv"
heatmap_file = open(heatmap_filename,"w")
heatmap_file.write(outstring_heatmap_matrix_prop_inf)
heatmap_file.close()

heatmap_filename = "N_infections_heatmap.csv"
heatmap_file = open(heatmap_filename,"w")
heatmap_file.write(outstring_heatmap_matrix_Ninf)
heatmap_file.close()



heatmap_filename = "Incidence_heatmap.csv"
heatmap_file = open(heatmap_filename,"w")
heatmap_file.write(outstring_heatmap_matrix_incidence)
heatmap_file.close()


