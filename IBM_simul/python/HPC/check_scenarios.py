
# Code to check if everything is set correctly.
import sys,re,os


CLUSTERS = {
1:"(1,3)", 
2:"(2,3)", 
5:"(5,4)", 
6:"(6,4)", 
8:"(8,7)", 
9:"(9,7)", 
10:"(10,12)", 
11:"(11,12)", 
13:"(13,15)", 
14:"(14,15)", 
16:"(16,17)", 
18:"(18,17)", 
19:"(19,21)", 
20:"(20,21)"
}


# Change working directory if called from other directory:
currentdir = os.getcwd().split("/")[-1]
# Move up a directory if needed:
if currentdir in ["JOB_SCRIPTS","CODE","JOB_SCRIPTS_CALIBRATE"]:
    os.chdir("..")
workingdir = os.getcwd()



codedir = "CODE/"

def run_make(codedir):
    os.chdir(codedir) 
    os.system("make clean")
    os.system("make all")
    os.chdir("..") # Move back to the earlier directory.


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
######## Check constants.h:
################################################################

def check_constants(codedir):
    constants_file = open(codedir+"constants.h","r")
    constantstext = constants_file.read()
    constants = remove_whitespace(constantstext).split("\n")
    constants_file.close()


    CHECKCONSTANTS = [["SIMPLE_PARTNERSHIP_CHECK",0],
                      ["SWEEP_THROUGH_TO_CHECK_LISTS",0],
                      ["SWEEP_THROUGH_TO_CHECK_N_PARTNERS_OUTSIDE_AND_N_HIVPOS_PARTNERS_AND_N_HIVPOS_PARTNERS_OUTSIDE",0],
                      ["CHECK_AGE_AND_RISK_ASSORTATIVITY",0],
                      ["DEBUG_PARTNERSHIP_DURATION",0],
                      ["GENERATE_ANNUAL_PARTNERSHIPS_OUTPUTS",1],
                      ["AGE_DISTRIBUTION_CHECK",0],
                      ["PRINT_HIVSURVIVAL_OUTPUT",0],
                      ["VERBOSE_OUTPUT",0], # If this is 1 then the IBM prints a lot of debug info to screen.
                      ["CHECKPARAMS",0], # If 1, runs debugging checks on input parameters to make sure they lie within expected ranges.
                      ["SIMPLE_PARTNERSHIP_CHECK",0], # This and the two below are checks that aren't needed apart from debugging.
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
                      ["DEBUG_ART_STATE",0],
                      ["DEBUG_CHIPS_STATES",1],
                      ["PRINT_ALL_RUNS",1],
                      ["PRINT_EACH_RUN_OUTPUT",1],
                      ["PRINT_EVERYTIMESTEP",1], # Generates Timestep_output csv file.
                      ["PRINT_PHYLOGENETICS_OUTPUT",0],
                      ["PRINT_PARTNERSHIP_NETWORK_SNAPSHOT",0],
                      ["PRINT_PARTNERS_OUTSIDE_COMMUNITY",0],
                      ["STORE_HAZARDS",0],
                      ["PRINT_PARTNERSHIPS_AT_PC0",1],
                      ["FOLLOW_INDIVIDUAL",-1],
                      ["MAX_POP_SIZE",320000],
                      ["RUN_PC",1]]

    CODE_CORRECT = 1

    for varpair in CHECKCONSTANTS:
        value = int(find_line(constants,varpair[0]," ",1,2))
        if (value!=varpair[1]):
            print "Set ",varpair[0]," to be",varpair[1],"in constants.h"
            CODE_CORRECT = 0

    return CODE_CORRECT


def check_whether_exe_up_to_date(dir,codedir):
    import glob,datetime
    # Get a list of all the files which end in .c or .h:
    sourcefiles = glob.glob(codedir+"*.[ch]")


    ibm_exe_filename = codedir+"popart-simul.exe"
    if not(os.path.isfile(ibm_exe_filename)):
        run_make(codedir)
    exe_file_timeupdated = os.path.getmtime(ibm_exe_filename)


    files_updated_out_of_sync = []

    for f in sourcefiles:
        source_file_timeupdated = os.path.getmtime(f)
        if (exe_file_timeupdated<source_file_timeupdated):
            files_updated_out_of_sync += [f]
            print "Warning: "+f.split("/")[-1]+" is more recent that "+ibm_exe_filename.split("/")[-1]+".\nRunning Make to fix."
            # Move to the code directory and run make:
            run_make(codedir)
            exe_file_timeupdated = os.path.getmtime(ibm_exe_filename)

    # if files_updated_out_of_sync is an empty list then not(files_updated_out_of_sync) is true.
    if not(files_updated_out_of_sync):
        return 1
    else:
        return files_updated_out_of_sync




CODE_CORRECT = check_constants(codedir)
if CODE_CORRECT==1:
    check_whether_exe_up_to_date(workingdir,codedir)
else:
    print "Please fix IBM constants.h and rerun check_scenarios.py"
