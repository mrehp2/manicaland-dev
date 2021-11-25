#############################################################################
# CODE DESCRIPTION, PURPOSE AND HOW TO RUN
# (WHEN YOU HAVE THE REQUIREMENTS LISTED BELOW):
#
# This script takes data from the UNPD WPP projections.
# It generates $COUNTRYMortalityMen_WPP$YEAR.csv, $COUNTRYMortalityMen_WPP$YEAR.csv,  and $COUNTRYFertility_WPP$YEAR.csv
# where $COUNTRY is the country (e.g. Zimbabwe) and $YEAR is the year of WPP data used.
# $COUNTRY and $YEAR are set below. (note: the "$" here is just to clarify that they are variables - in the code here they are "COUNTRY" and "YEAR").
# Modify "COUNTRY" and "YEAR" variables below to change the country and UNPD WPP version used.
#
# Call code via:
# python read_UNPD_mortality_data.py 2019 Zimbabwe
#
#############################################################################
# REQUIREMENTS TO RUN THE CODE:
# You need to download 4 data files from UNPD:
# From https://population.un.org/wpp/Download/Standard/Population/
# The two population indicators "Quinquennial Population by Five-Year Age Groups - Male/Female". In 2017 the files are called:
# WPP2017_POP_F07_2_POPULATION_BY_AGE_MALE.xlsx
# WPP2017_POP_F07_3_POPULATION_BY_AGE_FEMALE.xlsx

# From https://population.un.org/wpp/Download/Standard/Mortality/
# "Number of male/female deaths by five-year age groups."
# In 2017 the files are called:
# WPP2017_MORT_F04_2_DEATHS_BY_AGE_MALE.xlsx
# WPP2017_MORT_F04_3_DEATHS_BY_AGE_FEMALE.xlsx




# Additional requirements: python package 'openpyxl':
# Uses packages 'openpyxl' and 'pandas' to read in xlsx files.
# To install make sure you have pip:
# (if you don't, then install via) sudo apt install python-pip
# Then install openpyxl and pandas:
# pip install openpyxl pandas

#############################################################################


#############################################################################
# Code validation:
# checked against file ~/Dropbox/PoPART/IBM\ Model\ Background/Demographic\ data/SouthAfricaMortalityMen.csv+SouthAfricaMortalityWomen.csv for South Africa UNPD WPP 2015 estimates (and similarly Zambia outputs in the same folder) - outputs match to about 9d.p. (for some reason the validation file numbers are all rounded to around 9d.p. only - hence the tiny mismatch).
#############################################################################


# Library functions:
import openpyxl, pandas
import sys,os,glob


# This is the year of the UNPD WPP projections we are using - currently using WPP2019 projections.
YEAR = int(sys.argv[1])
COUNTRY = sys.argv[2]
### Change these to use different UNPD files and/or different country.
#COUNTRY = "South Africa"
COUNTRY = "Zimbabwe"

#Store this info to pass to Sweave:
mortality_info_file = open("mortality.info","w")
mortality_info_file.write(str(YEAR)+","+COUNTRY+"\n")
mortality_info_file.close()

# By default we keep the UNPD medium variant for future estimates:
projection_type = "MEDIUM VARIANT"


print("***USING UNPD WPP",YEAR,projection_type," projections***")




# This is the list of sheets we want to pull out. Note that Excel stores things like whitespace after the names so we will create a copy of this list that includes this whitespace below:
list_of_sheets = ["ESTIMATES"] + [projection_type]


### Names of the WPP files. In 2015 and 2017 these are the formats of the filenames:
# Number of deaths in a 5 year period:
Mortality_male_filename = "WPP"+str(YEAR)+"_MORT_F04_2_DEATHS_BY_AGE_MALE"
Mortality_female_filename = "WPP"+str(YEAR)+"_MORT_F04_3_DEATHS_BY_AGE_FEMALE"

# Population by 5 year age group:
NPop_male_filename = "WPP"+str(YEAR)+"_POP_F07_2_POPULATION_BY_AGE_MALE"
NPop_female_filename = "WPP"+str(YEAR)+"_POP_F07_3_POPULATION_BY_AGE_FEMALE"



############################################
### Utility functions:
############################################


######### Functions which relate to file operations (finding files, copying files) : ####################

# Given a file called "foo" looks for possible excel extensions.
# Code is needed because UNPD saved 2015 as .XLS and 2017 as .xlsx.
def find_correct_filename(filename_without_extension):
    possible_files = glob.glob(os.getcwd()+"/"+filename_without_extension+".[xX]*")

    if len(possible_files)>1:
        print("Too many possible files:",possible_files)
        sys.exit(1)
    else:
        return possible_files[0]


# We expect the header to be 5 year age groups, with last one "X+":
# This function checks that header has the correct format. It also
# returns the array index corresponding to the group 80+
def check_mortality_header(header,f):

    n_age_groups = len(header)
    for i in range(n_age_groups-1):
        min_age = 5*i
        max_age = min_age+4
        if min_age==80:
            i_max = i
        age_range = str(min_age)+"-"+str(max_age)
        if not(age_range==header[i]):
            print("Error: header for file ",f," not of the expected format in check_mortality_header(). Exiting",age_range,header[i])
            sys.exit(1)
            
    # Now check oldest age group:
    age_range = str(5*(n_age_groups-1))+"+"
    if not(age_range==header[n_age_groups-1]):
        print("Error: header for file ",f," not of the expected format. Exiting",age_range,header[n_age_groups-1])
        sys.exit(1)


    try:
        return i_max
    except:
        print("ERROR: in check_mortality_header() i_max is not defined. Exitng.")
        sys.exit(1)



# This function checks that header has the correct format.
# We expect the header to be 0-4, 5-9,.... 75-79, 80+, 80-84, 85-89,...95-99, 100+.
# Note that there are two ways data are presented - either as 80+ or as 80-84,85-89...100+.
# We want to get both i_80plus and i_100plus (the column index for 80+ and 100+).
# Unlike check_mortality header here we construct what the header should look like, and compare it to the existing one.
def check_NPop_header(header,f):
    if "80+" in header:
        n_age_groups = len(header)-2
    else:
        n_age_groups = len(header)-1
    i = 0

    
    
    header_to_compare = []
    while 1:
        
        if i==n_age_groups:
            break
        
        min_age = 5*i
        max_age = min_age+4
        if min_age==80:
            i_max = i
        age_range = str(min_age)+"-"+str(max_age)

        if min_age==80:
            
            if "80+" in header:
                header_to_compare += ["80+"]                
                i_80plus = i
                i_80to84 = i+1
            else:
                # Set to something random and negative.
                i_80plus = -1000
                i_80to84 = i
                

        header_to_compare += [age_range]
        i = i+1

    header_to_compare += ["100+"]

    
    if not(header_to_compare==header):
        print("Error: NPop header for file ",f," not of the xpected format. Exiting.\nComparison header=",header_to_compare,"\nOriginal:",header)
        sys.exit(1)

        
    try:
        # i_80plus is the index for the "80+" column.
        # i_80to84 is the index for the 80-84 column
        return [i_80plus,i_80to84]
    except:
        print("ERROR: in check_NPop_header() i_max is not defined. Exitng.")
        sys.exit(1)




        
# Given two dictionaries containing data from the past and future respectively (where the dictionary keys are the time periods), combine them to form a single dictionary:
def combine_times_time_periods(past_data,future_data):
    MIN_YEAR = 1950
    MAX_YEAR = 2100

    past_years = past_data.keys()
    future_years = future_data.keys()

    combined_dictionary = {}
    
    for t_start in range(MIN_YEAR,MAX_YEAR,5):
        t_end = t_start+5
        t_range = str(t_start)+"-"+str(t_end)
        if t_range in past_years:
            combined_dictionary[t_range] = past_data[t_range]
        else:
            combined_dictionary[t_range] = future_data[t_range]        

    return combined_dictionary


# Given two dictionaries containing data from the past and future respectively (where the dictionary keys are the years), combine them to form a single dictionary:
def combine_times_years(past_data,future_data):
    MIN_YEAR = 1950
    MAX_YEAR = 2100

    past_years = past_data.keys()
    future_years = future_data.keys()

    combined_dictionary = {}

    # Offset MAX_YEAR by 1 so upper limit of list is MAX_YEAR.
    for year in range(MIN_YEAR,MAX_YEAR+1,5):
        if year in past_years:
            combined_dictionary[year] = past_data[year]
        else:
            combined_dictionary[year] = future_data[year]        

    return combined_dictionary


# Given a list of sheet names (where the formatting may not match Excel's exactly in terms of whitespace etc) and the name of the xlsx file, pull out the named sheets and return this (as an array) and the list of sheet names 
def pull_out_sheets(infilename,list_of_sheets):

    book = openpyxl.load_workbook(infilename, data_only=True)
    
    sheets_to_keep = {}
    

    for sheet in book:
        formatted_sheet_name = sheet.title.rstrip().upper()
        if formatted_sheet_name in list_of_sheets:
            sheets_to_keep[formatted_sheet_name] = sheet
            
    return sheets_to_keep


def combine_upper_age_groups(line,i_max):
    upper_age_groups_to_combine = line[i_max:]
    combined_upper_age_gps_total = sum(upper_age_groups_to_combine)
    # combine the first i_max-1 groups with the combined upper age group:
    combined_data = line[:i_max] + [combined_upper_age_gps_total]
    return combined_data


def combine_upper_age_groups_NPop(line,i_80plus,i_80to84,i_data_start):
    if (i_80plus>=0):
        try:
            NPop_80plus = float(line[i_80plus])
        except:
            # if line[i_80plus] is '...' then we need to sum over 80-84, 85-89,...100+
            NPop_80plus = sum(line[i_80to84:])
        combined_data = line[i_data_start:i_80plus] + [NPop_80plus]
            
    # Future projections don't have an 80+ group
    else:
            
        combined_data = line[i_data_start:i_80to84] + [sum(line[i_80to84:])]

    return combined_data


# Given a mortality worksheet, pulls out the mortality data for the given COUNTRY, combining the highest age groups (so making a single 80+ group e.g. 80+ instead of 80-95, 85-90, 90-95, 95+).
def extract_country_data_mortality(sheet,COUNTRY,f):
    mortality_data = {}
    
    for i, line in enumerate(sheet.values):

        line = list(line)
        # 17th row is the header. Check this is what we think it is as a way fo verifying the file.
        if i==16:
            try:
                i_data_start = line.index("0-4")
            except:
                # If this happens, then UNPD has changed the format of their file again.
                print("Unexpected format of Excel file",f," in extract_country_data_mortality()- please check that line 16 contains the header information",line)

            header = line[i_data_start:]
            # Make sure that this is of the correct format. If it is, then give the index corresponding to the age group 80+ (when combining data)
            i_max = check_mortality_header(header,f)


        # Look for the country name - this is a data row.
        if COUNTRY in line:
            # (i_data_start-1)th column is the year range e.g. 1950-55:
            time_range = line[i_data_start-1]
            # (i_data_start)th column onwards is the mortality data in each age group.
            # UNPD presents both estimates to present and future projections in age groups 0-4, 5-9, ... 90-94, 95+
            mortality_data_this_time_period = line[i_data_start:]
            # Combine the highest age groups (80+)
            mortality_data[time_range] = combine_upper_age_groups(mortality_data_this_time_period,i_max)


    return mortality_data



# Given a pop size worksheet, pulls out the population size data for the given country, combining the highest age groups (so making a single 80+ group e.g. 80+ instead of 80-95, 85-90, 90-95, 95-100, 100+).
def extract_country_data_NPop(sheet,COUNTRY,f):
    NPop_data = {}
    
    for i, line in enumerate(sheet.values):

        line = list(line)

        # 17th row is the header. Check this is what we think it is as a way fo verifying the file.
        if i==16:
            try:
                i_data_start = line.index("0-4")

            except:
                # If this happens, then UNPD has changed the format of their file again.
                print("Error: Unexpected format of Excel file",f," in extract_country_data_NPop() - please check that line 16 contains the header information",line)
                sys.exit(1)
                
            header = line[i_data_start:]
            # Make sure that this is of the correct format. If it is, then give the indices corresponding to the age groups 80+ and 80-84 (when combining data)
            [i_80plus,i_80to84] = check_NPop_header(header,f)

            # Need to adjust as we previously removed the first i_data_start columns:
            i_80plus = i_80plus + i_data_start
            i_80to84 = i_80to84 + i_data_start


        # Look for the country name - this is a data row.
        if COUNTRY in line:
            NPop_data_this_year = line
            # (i_data_start-1)th column is the year e.g. 1955:
            year = line[i_data_start-1]

            # UNPD presents both estimates to present and future projections in age groups 0-4, 5-9, etc. from 7th column onwards:

            # Combine the age 80+ age groups if needed (or use the 80+ if not):
            NPop_data[year] = combine_upper_age_groups_NPop(NPop_data_this_year,i_80plus,i_80to84,i_data_start)
            #print "year = ",year,"80+ pop = ",NPop_data[year][-1]


    return NPop_data


# Given a data file of the form 1950=x, 1955=y ... etc, create a data file of the form 1950-55 = (x+y)/2 etc.
def interpolate_data(original_data):
    MIN_YEAR = 1950
    MAX_YEAR = 2100

    interpolated_data = {}
    
    for t_start in range(MIN_YEAR,MAX_YEAR,5):
        t_end = t_start+5
        t_range = str(t_start)+"-"+str(t_end)

        interpolated_data[t_range] = []

        n_data = len(original_data[t_start])
        if len(original_data[t_end])!=n_data:
            print("Error: interpolate_data() length of lines for years ",t_start," and ",t_end," do not match. Exiting.")
            sys.exit(1)
        
        for i in range(n_data):
            start_data = original_data[t_start][i]
            end_data = original_data[t_end][i]
            interpolated_data[t_range] += [0.5*(start_data+end_data)]


    return interpolated_data

def get_mortality_data(mortality_worksheets,COUNTRY,Mortality_filename,list_of_sheets):
    # Pull out data from "ESTIMATES" sheet (i.e. until present time):
    country_data_mortality_to_present = extract_country_data_mortality(mortality_worksheets[list_of_sheets[0]],COUNTRY,Mortality_filename)


    # Pull out data from "MEDIUM VARIANT" sheet (i.e. present time to 2100):
    country_data_mortality_future_projection = extract_country_data_mortality(mortality_worksheets[list_of_sheets[1]],COUNTRY,Mortality_filename)

    # Now stick the two time periods together:
    country_data_mortality = combine_times_time_periods(country_data_mortality_to_present,country_data_mortality_future_projection)

    return country_data_mortality
    
def get_NPop_data(NPop_worksheets,COUNTRY,NPop_filename,list_of_sheets):
    country_data_NPop_to_present = extract_country_data_NPop(NPop_worksheets[list_of_sheets[0]],COUNTRY,NPop_filename)

    country_data_NPop_future_projection = extract_country_data_NPop(NPop_worksheets[list_of_sheets[1]],COUNTRY,NPop_filename)

    country_data_NPop = combine_times_years(country_data_NPop_to_present,country_data_NPop_future_projection)

    # Population data needs to be converted from point estimates every 5 years (e.g. 1950, 1955,...) to an average over a 5 year range (e.g. 1950-55).
    # To do this we just take the average of the 1950 and 1955 values.
    country_data_NPop_time_range = interpolate_data(country_data_NPop)

    return country_data_NPop_time_range

def calculate_mortality_rate(Ndeaths,Npeople):
    # UNPD gives number of deaths over 5 year period.
    return (Ndeaths/Npeople)/5.0
    
# Take number of deaths over 5 year period, and number of people, and create
# a mortality rate
def calculate_annual_mortality_rates(Ndeaths,Npeople):
    MIN_YEAR = 1950
    MAX_YEAR = 2100

    mortality_rate = {}

    Nagegroups = len(Ndeaths["1950-1955"])
    
    for t_start in range(MIN_YEAR,MAX_YEAR,5):
        t_end = t_start+5
        t_range = str(t_start)+"-"+str(t_end)

        if not(Nagegroups==len(Ndeaths[t_range]) and Nagegroups==len(Ndeaths[t_range])):
            print("Error in calculate_annual_mortality_rates(): different lengths for the number of deaths and number of people. Exiting")
            sys.exit(1)

        mortality_rate[t_range] = []
        for i in range(Nagegroups):
            mortality_rate[t_range] += [calculate_mortality_rate(Ndeaths[t_range][i],Npeople[t_range][i])]

    return mortality_rate



def output_mortality_range(mortality_rate,outfilename):
    MIN_YEAR = 1950
    MAX_YEAR = 2100

    # This is the header for the output file:
    outstring = "Period,0-4,5-9,10-14,15-19,20-24,25-29,30-34,35-39,40-44,45-49,50-54,55-59,60-64,65-69,70-74,75-79,80+\n"



    for t_start in range(MIN_YEAR,MAX_YEAR,5):
        t_end = t_start+5
        t_range = str(t_start)+"-"+str(t_end)
        mortality_rate_string = ",".join([str(x) for x in mortality_rate[t_range]])
        outstring += t_range+","+mortality_rate_string+"\n"

    outfile = open(outfilename,"w")
    outfile.write(outstring)
    outfile.close()
    #print outstring

    
    
####################################################
### MAIN CODE:
####################################################
            
# Add the correct extension (e.g. ".xlsx" to the files:
Mortality_male_filename = find_correct_filename(Mortality_male_filename)
Mortality_female_filename = find_correct_filename(Mortality_female_filename)
NPop_male_filename = find_correct_filename(NPop_male_filename)
NPop_female_filename = find_correct_filename(NPop_female_filename)
            


male_mortality_worksheets = pull_out_sheets(Mortality_male_filename,list_of_sheets)
female_mortality_worksheets = pull_out_sheets(Mortality_female_filename,list_of_sheets)
male_NPop_worksheets = pull_out_sheets(NPop_male_filename,list_of_sheets)
female_NPop_worksheets = pull_out_sheets(NPop_female_filename,list_of_sheets)





country_data_male_mortality = get_mortality_data(male_mortality_worksheets,COUNTRY,Mortality_male_filename,list_of_sheets)
#print country_data_male_mortality["1990-1995"]

country_data_female_mortality = get_mortality_data(female_mortality_worksheets,COUNTRY,Mortality_female_filename,list_of_sheets)
#print country_data_female_mortality["1990-1995"]


country_data_male_NPop_time_range = get_NPop_data(male_NPop_worksheets,COUNTRY,NPop_male_filename,list_of_sheets)

country_data_female_NPop_time_range = get_NPop_data(female_NPop_worksheets,COUNTRY,NPop_female_filename,list_of_sheets)



male_annual_mortality_rate = calculate_annual_mortality_rates(country_data_male_mortality,country_data_male_NPop_time_range)

female_annual_mortality_rate = calculate_annual_mortality_rates(country_data_female_mortality,country_data_female_NPop_time_range)

# Save filename with country name, but removing any spaces (e.g. SouthAfrica)
country_for_filename = COUNTRY.replace(" ","")

output_mortality_range(male_annual_mortality_rate,country_for_filename+"MortalityMen_WPP"+str(YEAR)+".csv")
output_mortality_range(female_annual_mortality_rate,country_for_filename+"MortalityWomen_WPP"+str(YEAR)+".csv")



#print country_data_female_NPop_time_range["2095-2100"]


#print country_data_male_mortality["2025-2030"]



###########################################################
            #list_of_sheets_in_excel[formatted_sheet_name] = sheet.name

            #print list_of_sheets_in_excel

#for formatted_sheet_name in list_of_sheets_in_excel:
    
    
#working_sheet = book.sheet_by_name(list_of_sheets_in_excel[0])



# Locate header for data, and get indices for country+data:
#for i in range(working_sheet.nrows):
#    print working_sheet.row_values(i)

####Not needed any more:
# country_data_male_NPop_to_present = extract_country_data_NPop(male_NPop_worksheets[list_of_sheets[0]],country,NPop_male_filename,max_age_group)

# country_data_male_NPop_future_projection = extract_country_data_NPop(male_NPop_worksheets[list_of_sheets[1]],country,NPop_male_filename,max_age_group)

# country_data_male_NPop = combine_times_years(country_data_male_NPop_to_present,country_data_male_NPop_future_projection)

# country_data_male_NPop_time_range = interpolate_data(country_data_male_NPop)


# Pull out male data from "ESTIMATES" sheet (i.e. until present time)
#country_data_male_mortality_to_present = extract_country_data_mortality(male_mortality_worksheets[list_of_sheets[0]],country,Mortality_male_filename,max_age_group)
# Pull out male data from "MEDIUM VARIANT" sheet (i.e. present time to 2100)
#country_data_male_mortality_future_projection = extract_country_data_mortality(male_mortality_worksheets[list_of_sheets[1]],country,Mortality_male_filename,max_age_group)

#country_data_male_mortality = combine_times_time_periods(country_data_male_mortality_to_present,country_data_male_mortality_future_projection)

