
import os,sys,glob

from shutil import copyfile

try:
    COMMUNITY = int(sys.argv[1])  # Change for different clusters.                                                        
except:
    print("Syntax error - need to pass community number as an argument.")
    sys.exit(1)


def parse_directory():
    this_dir = os.getcwd().split("/")[-1]
    return this_dir.replace("CALIBRATION","SCENARIOS")

# Based on the current "CALIBRATION" directory this should get the corresponding "SCENARIOS" directory.
scenario_dir = parse_directory()

PARAM_INPUT_DIR = "RESULTS_COMMUNITY"+str(COMMUNITY)+"/"
PARAM_OUTPUT_DIR = "../"+scenario_dir+"/SCENARIOS_COMMUNITY"+str(COMMUNITY)+"/BASELINE_CALIBRATED_PARAMS"+str(COMMUNITY)+"/"
if not os.path.exists(PARAM_OUTPUT_DIR):
    os.makedirs(PARAM_OUTPUT_DIR)


if (COMMUNITY in [1,2]):
    CONTROL = 3
elif (COMMUNITY in [5,6]):
    CONTROL = 4
elif (COMMUNITY in [8,9]):
    CONTROL = 7
elif (COMMUNITY in [10,11]):
    CONTROL = 12
elif (COMMUNITY in [13,14]):
    CONTROL = 15
elif (COMMUNITY in [16,18]):
    CONTROL = 17
elif (COMMUNITY in [19,20]):
    CONTROL = 21
else:
    print("Unknown community. Exiting\n")
    sys.exit(1)

COMMUNITY_INCLUDINGCONTROL = [COMMUNITY,CONTROL]


specialfiles = ["param_processed_patchinfo.txt","param_processed_patch0_fertility.csv","param_processed_patch0_mortality.csv","param_processed_patch1_fertility.csv","param_processed_patch1_mortality.csv","param_processed_patch0_chipsuptake_round1.csv","param_processed_patch0_chipsuptake_round2.csv","param_processed_patch0_chipsuptake_round3.csv","param_processed_patch0_chipsuptake_round4.csv","param_processed_patch0_chipsuptake_roundposttrial.csv","param_processed_patch1_chipsuptake_round1.csv","param_processed_patch1_chipsuptake_round2.csv","param_processed_patch1_chipsuptake_round3.csv","param_processed_patch1_chipsuptake_round4.csv","param_processed_patch1_chipsuptake_roundposttrial.csv","fitting_data_processed.txt"]


PC_files = ["param_processed_patch"+str(p)+"_PC"+r+"_community"+str(COMMUNITY_INCLUDINGCONTROL[p])+".csv" for p in [0,1] for r in ["0","1","2","3"]]

specialfiles = specialfiles+PC_files

# Copy special (ie always the same) files:
def copy_special_files(input_dir,output_dir,specialfiles):
    for f in specialfiles:
        copyfile(input_dir+"/"+f,output_dir+"/"+f)

def make_special_python_seed(output_dir,seed):
    python_file = output_dir+"python_seed.txt"
    python_fileptr = open(python_file,"w")
    python_fileptr.write(seed+"\n")
    python_fileptr.close()

def pull_lines_from_file(original_file,lines_needed):
    f_ptr = open(original_file,"r")
    data = f_ptr.read().split("\n")
    f_ptr.close()

    # First row is always the header.
    header = data[0]+"\n"
    data_kept = ""
    for i in lines_needed:
        data_kept += data[i]+"\n"

    return [header,data_kept]



def get_files_needed(template_dir,special_files):


    all_files = glob.glob(template_dir+"/param*patch*.csv")
    all_files = [f.replace(template_dir+"/","") for f in all_files]

    files_needed = [x for x in all_files if x not in special_files]


    return files_needed








########################################################################
######## Get stuff from GoodFits.txt file:
########################################################################

ANNE_SEP = " " # What Anne uses as delimiter in her .txt files
if (COMMUNITY<10):
    COMMUNITYNAME = "0"+str(COMMUNITY)
else:
    COMMUNITYNAME = str(COMMUNITY)

GOODFITFILE = PARAM_INPUT_DIR+"/GoodFits_CL"+COMMUNITYNAME+".txt"


GOODFITSFILE = open(GOODFITFILE,"r")
goodfitsdata = GOODFITSFILE.read().rstrip().split("\n")
GOODFITSFILE.close()


runs_to_get = {}
for goodfitsline in goodfitsdata[1:]:
    goodfitsdata = goodfitsline.split(ANNE_SEP)
    seed = int(goodfitsdata[1])
    run_no = int(goodfitsdata[2])
    #print seed,run_no
    # Add if already there, else make a new one:                                                                        
    if (seed in runs_to_get.keys()):
        runs_to_get[seed] += [run_no]
    else:
        runs_to_get[seed] = [run_no]


seeds_used = runs_to_get.keys()


########################################################################
######## Get stuff from GoodFits.txt file:
########################################################################


files_needed = get_files_needed(PARAM_INPUT_DIR+"RESULTS"+str(seeds_used[0]),specialfiles)
copy_special_files(PARAM_INPUT_DIR+"RESULTS"+str(seeds_used[0]),PARAM_OUTPUT_DIR,specialfiles)

# Python seed '9999' means impact files - makes it easier for Anne's R knitr/code
make_special_python_seed(PARAM_OUTPUT_DIR,"9999")

print(files_needed)


for f in files_needed:
    output_file = PARAM_OUTPUT_DIR+f
    print(output_file)
    data_kept = ""
    for s in seeds_used:
        this_input_file = PARAM_INPUT_DIR+"RESULTS"+str(s)+"/"+f
        [header,data] = pull_lines_from_file(this_input_file,runs_to_get[s])
        if data_kept=="":
            data_kept += header
        data_kept += data

            
        
    outfile_ptr = open(output_file,"w")
    outfile_ptr.write(data_kept)
    outfile_ptr.close()
        
