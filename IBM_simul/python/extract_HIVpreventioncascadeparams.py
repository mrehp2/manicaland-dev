import glob, sys, os, filecmp, shutil
from datetime import datetime,date
from os.path import join
import random,copy
import xlrd   # For reading Excel files.

import utilities as utils



def pull_out_sheets(infilename,sheet_to_get):

    book = xlrd.open_workbook(infilename)
    sheet_to_keep = {}

    for sheet in book.sheets():
        print sheet.name.rstrip()
        formatted_sheet_name = sheet.name.rstrip()
        if formatted_sheet_name==sheet_to_get:
            return book.sheet_by_name(sheet.name)

    print "Error: sheet",sheet_to_get," not found. Exiting."
    sys.exit(1)


def make_proportion(ci):
    ci_split = ci.split("-")
    ll=str(float(ci_split[0])/100)
    ul=str(float(ci_split[1])/100)
    return ll+"-"+ul

# Given a mtct worksheet, pulls out the data, and save it as a PopART-IBM param file:
def make_HIVpreventioncascade_params(sheet):


    louisa_header = [u'Prevention method', u'Sex', u'Priority population', u'N', u'Proportion motivated', u'', u'', u'Proportion motivated and access', u'', u'', u'Proportion motivated, access and using', u'', u'']
    

    a = {("Female","Never had sex"):-1,("Female","Ever had sex 15-24"):-1, ("Female","Ever had sex 25-54"):-1}

    saved_data = {"Male condoms":{("Female","Never had sex"):-1,("Female","Ever had sex 15-24"):-1, ("Female","Ever had sex 25-54"):-1, ("Male","Never had sex"):-1,("Male","Ever had sex 15-29"):-1, ("Male","Ever had sex 30-54"):-1},
                  "PrEP":{("Female","Never had sex"):-1,("Female","Ever had sex 15-24"):-1, ("Female","Ever had sex 25-54"):-1, ("Male","Never had sex"):-1,("Male","Ever had sex 15-29"):-1, ("Male","Ever had sex 30-54"):-1},
                  "VMMC":{("Male","Never had sex"):-1,("Male","Ever had sex 15-29"):-1, ("Male","Ever had sex 30-54"):-1}}

    prevention_methods_to_keep = saved_data.keys()
    
    for i in range(sheet.nrows):

        # Go through spreadsheet line by line:
        line = sheet.row_values(i)

        if (line==louisa_header):
            continue
        else:
            # Remove the "n % 95% CI" header line, plus any blank line:
            filtered_line = filter(lambda a: a not in  [u'n',u'%',u'',u'% ',u'95% CI'], line)
            if not(filtered_line==[]):
                prevention_method = line[0].rstrip()
                if prevention_method in prevention_methods_to_keep:
                    sex = line[1].rstrip()
                    group = line[2].rstrip()
                    if (sex,group) in saved_data[prevention_method].keys():
                        if line[-1].rstrip()=="-":
                            saved_data[prevention_method][(sex,group)] =  "0"
                        else:
                            saved_data[prevention_method][(sex,group)] =  make_proportion(line[-1].rstrip())

    print saved_data["VMMC"]
    print
    print "PrEP"
    print saved_data["PrEP"]

    
    outstring = ""
    
    
    #outstring = outstring.rstrip()
    return "A"





    

##############################################################
# Main code:
##############################################################

HIVprevention_cascade_param_file = "~/Dropbox (SPH Imperial College)/Manicaland/Cascades/cascade_model_parameters.xlsx"


# This is the sheet we want to pull out from the worksheet. 
sheet_needed = "Sheet1"

# Extract the worksheet
parameter_worksheets = pull_out_sheets(HIVprevention_cascade_param_file,sheet_needed)


# Now process it and save it in the format needed by the IBM:
params = make_HIVpreventioncascade_params(parameter_worksheets)
print "Finished"
print params


