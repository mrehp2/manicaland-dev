#############################################################################
# This script takes data from the UNPD WPP projections.
# How to call (from command line):
# python read_UNPD_fertility_data.py
# ****************************DATA REQUIREMENTS:****************************
# You need to download theAge-specific Fertility Rates (ASFR) file from UNPD WPP website:
# https://population.un.org/wpp/Download/Standard/Fertility/
# e.g. WPP2017_FERT_F07_AGE_SPECIFIC_FERTILITY.XLS
# Modify "COUNTRY" and "YEAR" variables below to change the country and UNPD WPP version used.
# Additional requirements: python packae 'xlrd':
# Uses package 'xlrd' to read in xlsx files.
# To install make sure you have pip:
# (if you don't, then install via) sudo apt install python-pip
# Then install xlrd:
# pip install xlrd

#############################################################################



#############################################################################
# Code validation:
# checked against file ~/popart-ibm-code/popart-code/IBM_simul/RAW_PRIORS/TEMPLATE/param_fertility.txt for Zambia UNPD WPP 2015 estimates - outputs match.
#############################################################################

# Library functions:
import xlrd
import sys,os,glob


### Change these to use different UNPD files and/or different country.
#COUNTRY = "South Africa"
COUNTRY = "Zimbabwe"
# This is the year of the UNPD WPP projections we are using - currently using WPP2017 projections.
YEAR = 2017

# By default we keep the UNPD medium variant for future estimates:
projection_type = "MEDIUM VARIANT"


print "***USING UNPD WPP",YEAR,projection_type," projections***"



# This is the list of sheets we want to pull out. Note that Excel stores things like whitespace after the names so we will create a copy of this list that includes this whitespace below:
list_of_sheets = ["ESTIMATES"] + [projection_type]


### Name of the UNPD WPP file:
Fertility_filename = "WPP"+str(YEAR)+"_FERT_F07_AGE_SPECIFIC_FERTILITY"




############################################
### Utility functions:
############################################


######### Functions which relate to file operations (finding files, copying files) : ####################

# Given a file called "foo" looks for possible excel extensions.
# Code is needed because UNPD saved 2015 as .XLS and 2017 as .xlsx.
def find_correct_filename(filename_without_extension):
    possible_files = glob.glob(os.getcwd()+"/"+filename_without_extension+".[xX]*")

    if len(possible_files)>1:
        print "Too many possible files:",possible_files
        sys.exit(1)
    else:
        return possible_files[0]


# We expect the header to be 5 year age groups 15-19,20-24,...45-49.
# This function checks that header has the correct format. 
def check_header(header,f):

    n_age_groups = len(header)


    min_age = 15 # min_age is the lower age in the age range (i.e. 15, 20, 25,...)
    header_to_compare = []
    while 1:
        
        if min_age>45:
            break
        
        max_age = min_age+4

        age_range = str(min_age)+"-"+str(max_age)

        header_to_compare += [age_range]
        min_age = min_age + 5

    
    if not(header_to_compare==header):
        print "Error: header for file ",f," not of the xpected format. Exiting.\nComparison header=",header_to_compare,"\nOriginal:",header
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



# Given a list of sheet names (where the formatting may not match Excel's exactly in terms of whitespace etc) and the name of the xlsx file, pull out the named sheets and return this (as an array) and the list of sheet names 
def pull_out_sheets(infilename,list_of_sheets):

    book = xlrd.open_workbook(infilename)
    
    sheets_to_keep = {}
    

    for sheet in book.sheets():
        formatted_sheet_name = sheet.name.rstrip().upper()
        if formatted_sheet_name in list_of_sheets:
            
            sheets_to_keep[formatted_sheet_name] = book.sheet_by_name(sheet.name)
            
    return sheets_to_keep



# Given a fertility worksheet, pulls out the data for the given COUNTRY
def extract_country_data_fertility(sheet,COUNTRY,f):
    fertility_data = {}
    
    for i in range(sheet.nrows):

        # Go through spreadsheet line by line:
        line = sheet.row_values(i)

        # 17th row is the header. Check this is what we think it is as a way fo verifying the file.
        if i==16:
            header = line[6:]
            # Make sure that the header is of the correct format. 
            i_max = check_header(header,f)


        # Look for the country name - this is a data row.
        if COUNTRY in line:
            # 6th column is the year range e.g. 1950-55:
            time_range = line[5]
            # 7th column onwards is the fertility data in each age group.
            # UNPD presents both estimates to present and future projections in age groups 15-19, 20-24, 45-49.
            fertility_data[time_range] = line[6:]


    return fertility_data




def get_fertility_data(fertility_worksheets,COUNTRY,Fertility_filename,list_of_sheets):
    # Pull out data from "ESTIMATES" sheet (i.e. until present time):
    country_data_fertility_to_present = extract_country_data_fertility(fertility_worksheets[list_of_sheets[0]],COUNTRY,Fertility_filename)


    # Pull out data from "MEDIUM VARIANT" sheet (i.e. present time to 2100):
    country_data_fertility_future_projection = extract_country_data_fertility(fertility_worksheets[list_of_sheets[1]],COUNTRY,Fertility_filename)

    # Now stick the two time periods together:
    country_data_fertility = combine_times_time_periods(country_data_fertility_to_present,country_data_fertility_future_projection)

    return country_data_fertility
    


def output_fertility_range(fertility_data,outfilename):
    MIN_YEAR = 1950
    MAX_YEAR = 2100

    # This is the header for the output file:
    outstring = "Period,15-19,20-24,25-29,30-34,35-39,40-44,45-49\n"



    for t_start in range(MIN_YEAR,MAX_YEAR,5):
        t_end = t_start+5
        t_range = str(t_start)+"-"+str(t_end)
        fertility_data_string = ",".join([str(x) for x in fertility_data[t_range]])
        outstring += t_range+","+fertility_data_string+"\n"

    outfile = open(outfilename,"w")
    outfile.write(outstring)
    outfile.close()
    #print outstring



####################################################
### MAIN CODE:
####################################################
            
# Add the correct extension (e.g. ".xlsx" to the files:
Fertility_filename = find_correct_filename(Fertility_filename)            


# Extract the worksheets (i.e. make an object that contains the data from every worksheet in the Excel file).
fertility_worksheets = pull_out_sheets(Fertility_filename,list_of_sheets)

# Take the object above and parse the relevant data from the worksheets named in list_of_sheets, for COUNTRY.
country_data_fertility = get_fertility_data(fertility_worksheets,COUNTRY,Fertility_filename,list_of_sheets)
#print country_data_fertility["1990-1995"]


# Save filename with country name, but removing any spaces (e.g. SouthAfrica)
country_for_filename = COUNTRY.replace(" ","")

output_fertility_range(country_data_fertility,country_for_filename+"Fertility_WPP"+str(YEAR)+".csv")
