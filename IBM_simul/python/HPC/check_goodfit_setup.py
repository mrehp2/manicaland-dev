# Code to check if everything is set correctly.
import sys,re,os
try:
    COMMUNITY=int(sys.argv[1])
except:
    print "Error: Need to pass community number as an argument. Exiting\n"
    sys.exit(1)
CLUSTERS = {
1:"1 3", 
2:"2 3", 
5:"5 4", 
6:"6 4", 
8:"8 7", 
9:"9 7", 
10:"10 12", 
11:"11 12", 
13:"13 15", 
14:"14 15", 
16:"16 17", 
18:"18 17", 
19:"19 21", 
20:"20 21"
}

if (COMMUNITY<=12):
    COUNTRY="Z"
elif (COMMUNITY<=21):
    COUNTRY="S"
else:
    print "unknown community",COMMUNITY
    sys.exit(1)
# Number of rounds of DHS data in Zambia (3) and SA (4):
NDHSROUNDS_BY_COUNTRY = {"Z":3, "S":4}


paramsdir="SETUP_COMMUNITY"+str(COMMUNITY)+"/Central_Chips_centralARTlinkage_centralVMMC/"
codedir = "CODE/"

def find_line(alllines,name,sep,namecol,outputcol):
    for line in alllines:

        data = line.split(sep)
        if(len(data)>max(namecol,outputcol)):
            if data[namecol]==name:
                return data[outputcol]
    return -1

def remove_whitespace(text):
    re.sub( '\s+', ' ', text ).strip()
    return text

def check_error(v,varname,filename):
    if (v==-1):
        print "Error -",varname," not found in ",filename
        sys.exit(1)



################################################################
######## Check params_patchinfo.txt:
################################################################


param_patchinfo_file = open(paramsdir+"param_processed_patchinfo.txt","r")
params_patchinfo = param_patchinfo_file.read().split("\n")
param_patchinfo_file.close()

community_id = params_patchinfo[0]
#print "A",community_id,"A",CLUSTERS[COMMUNITY],"A"

if (community_id.rstrip()!=CLUSTERS[COMMUNITY].rstrip()):
    print "Set community_id to ",CLUSTERS[COMMUNITY]," in",paramsdir+"params_processed_patchinfo.txt. Currently ",community_id



################################################################
######## Check constants.h:
################################################################

def check_constants(codedir):
    constants_file = open(codedir+"constants.h","r")
    constantstext = constants_file.read()
    constants = remove_whitespace(constantstext).split("\n")
    constants_file.close()


    CHECKCONSTANTS = [["FOLLOW_INDIVIDUAL",-1],
                      ["SIMPLE_PARTNERSHIP_CHECK",0],
                      ["SWEEP_THROUGH_TO_CHECK_LISTS",0],
                      ["SWEEP_THROUGH_TO_CHECK_N_PARTNERS_OUTSIDE_AND_N_HIVPOS_PARTNERS_AND_N_HIVPOS_PARTNERS_OUTSIDE",0],
                      ["CHECK_AGE_AND_RISK_ASSORTATIVITY",0],
                      ["DEBUG_PARTNERSHIP_DURATION",0],
                      ["GENERATE_ANNUAL_PARTNERSHIPS_OUTPUTS",1],
                      ["AGE_DISTRIBUTION_CHECK",0],
                      ["PRINT_HIVSURVIVAL_OUTPUT",0],
                      ["VERBOSE_OUTPUT",0],
                      ["CHECKPARAMS",0],
                      ["PRINT_DEBUG_DEMOGRAPHICS",0],
                      ["DEBUG_DEMOGRAPHICS_NBIRTHS_NEWADULTS_DEATHS",0],
                      ["DEBUG_DEMOGRAPHICS_AGE_DISTRIBUTION_BY_GENDER",0],
                      ["DEBUG_DEMOGRAPHICS_AGE_DISTRIBUTION_ONEYEARINCKIDS",0],
                      ["DEBUG_DEMOGRAPHICS_LIFE_EXPECTANCY",0],
                      ["PRINT_DEBUG_INPUT",0],
                      ["DEBUG_INITIAL_SPVL_DISTRIBUTION",0],
                      ["DEBUG_CD4_AFTER_SEROCONVERSION",0],
                      ["DEBUG_HIV_DURATION",0],
                      ["DEBUG_HIV_DURATION_KM",0],
                      ["DEBUG_HIV_STATES",0],
                      ["DEBUG_ART_STATE",1],
                      ["DEBUG_CHIPS_STATES",1],
                      ["PRINT_ALL_RUNS",1],
                      ["PRINT_EACH_RUN_OUTPUT",1],
                      ["PRINT_EVERYTIMESTEP",0],
                      ["PRINT_PHYLOGENETICS_OUTPUT",0],
                      ["PRINT_PARTNERSHIP_NETWORK_SNAPSHOT",0],
                      ["PRINT_PARTNERS_OUTSIDE_COMMUNITY",0],
                      ["STORE_HAZARDS",0],
                      ["PRINT_PARTNERSHIPS_AT_PC0",1],
                      ["MAX_POP_SIZE",320000],
                      ["RUN_PC",1]]

    for varpair in CHECKCONSTANTS:
        value = int(find_line(constants,varpair[0]," ",1,2))
        if (value!=varpair[1]):
            print "Set ",varpair[0]," to be",varpair[1],"in constants.h"


def check_whether_exe_up_to_date(dir):
    import glob,datetime
    # Get a list of all the files which end in .c or .h:
    sourcefiles = glob.glob("CODE/*.[ch]")
    

    ibm_exe_filename = "CODE/popart-simul.exe"
    exe_file_timeupdated = os.path.getmtime(ibm_exe_filename)
    
    files_updated_out_of_sync = []

    for f in sourcefiles:
        source_file_timeupdated = os.path.getmtime(f)
        if (exe_file_timeupdated<source_file_timeupdated):
            files_updated_out_of_sync += [f]
            print "Error: "+f.split("/")[-1]+" is more recent that "+ibm_exe_filename.split("/")[-1]+".\nPlease run Make"
            sys.exit(1)

    # if files_updated_out_of_sync is an empty list then not(files_updated_out_of_sync) is true.
    if not(files_updated_out_of_sync):
        return 1
    else:
        return files_updated_out_of_sync




check_constants(codedir)
workingdir = os.getcwd()
check_whether_exe_up_to_date(workingdir)

