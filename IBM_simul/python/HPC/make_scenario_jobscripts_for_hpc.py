
import os,sys,re
NOT_CF = 0
IS_CF = 1

ARM_A_COMMUNITIES = [2,5,8,10]
ARM_B_COMMUNITIES = [1,6,9,11]
ARM_C_COMMUNITIES = [3,4,7,12]


# Make the job name that is passed to the queue scheduler (ie SGE, etc).
def get_job_name(community_number,scenario):
    if community_number<=12:
        job_name = "zam"+str(community_number)
    else:
        job_name = "sa"+str(community_number)
    if community_number in ARM_B_COMMUNITIES:
        job_name += "b"

    job_name = job_name + scenario.split("_")[0]
    return job_name


# Given a community number, get the corresponding control community number. 
def get_control_community(community_number):

    if community_number in ARM_A_COMMUNITIES:
        i = ARM_A_COMMUNITIES.index(community_number)
    elif community_number in ARM_B_COMMUNITIES:
        i = ARM_B_COMMUNITIES.index(community_number)
    else:
        print "Error: community number must lie in range",str(min(ARM_A_COMMUNITIES+ARM_B_COMMUNITIES))+"-"+str(max(ARM_A_COMMUNITIES+ARM_B_COMMUNITIES))+". Exiting"
        sys.exit(1)
    control_community_number = ARM_C_COMMUNITIES[i]

    return control_community_number


# Either get the community number from the directory the code is being run from, or else get it from a command line argument.
# If neither are possible, print an error message and exit.
def get_community_number(args):
    p = re.compile('SCENARIOS_COMMUNITY[0-9]+')
    thisdir = os.getcwd().split("/")[-2]
    print thisdir
    if p.match(thisdir):
        community_number = int(thisdir.replace("SCENARIOS_COMMUNITY",""))
    elif len(args)==2:
        community_number = int(args[1])
    else:
        print "Error: Need to pass community number as argument. Exiting"
        sys.exit(1)
    return community_number




def update_job_script(template_jobsubmission_script,job_name,community,input_dir,control_community,s,is_counterfactual):
    this_job_submission_script = template_jobsubmission_script.replace("X_JOB_NAME",job_name)
    this_job_submission_script = this_job_submission_script.replace("X_COMMUNITY_NUMBER",str(community))
    this_job_submission_script = this_job_submission_script.replace("X_INPUT_DIRECTORY",'"'+input_dir+'"')
    this_job_submission_script = this_job_submission_script.replace("X_CONTROL_NUMBER",str(control_community))
    this_job_submission_script = this_job_submission_script.replace("X_SCENARIO",'"'+s+'"')
    if not(is_counterfactual):
        this_job_submission_script = this_job_submission_script.replace("X_OUTDIR",'"'+s+'"')
    else:
        this_job_submission_script = this_job_submission_script.replace("X_OUTDIR",'"'+'CF'+'"')
    return this_job_submission_script


#################################################################
##### Functions which make the job script for the counterfactual
#################################################################
# Function takes the line which is the call for the executable and updates it to switch on the counterfactual.
# ibm_code_call = "./popart-simul.exe . $NRUNS 0 1 Output $offset $pc_offset"
# Counterfactual call will be : "./popart-simul.exe . $NRUNS 1 1 Output $offset $pc_offset"
def deconstruct_code_call_line(call):
    split_call = call.split() # split by whitespace
    if (not(len(split_call)==8) or not(split_call[4]=="1") or not(split_call[3]=="0")):
        print "ERROR: call to popart-simul.exe has changed. Need to update make_scenario_jobscripts_for_hpc.py to reflect this"
    cf_call = " ".join(split_call[0:3])+" 1 "+ " ".join(split_call[4:])
    return cf_call


def replace_ibm_call_with_counterfactual(template_jobsubmission_script):
    # Change this if you ever change the name of the executable:
    ibm_code_call = "./popart-simul.exe"

    counterfactual_job_submission_script = ""
    template_job_submission_script_by_line = template_jobsubmission_script.splitlines()

    for line in template_job_submission_script_by_line:
        if line[:len(ibm_code_call)]==ibm_code_call:
            # Modify line to make this a CF call:
            updated_line = deconstruct_code_call_line(line) 
            counterfactual_job_submission_script += updated_line + "\n"
        else:
            # Keep line unchanged
            counterfactual_job_submission_script += line +"\n"
    return counterfactual_job_submission_script



#################################################################
#################################################################


####################################################################################
#### Main code:
####################################################################################


community = get_community_number(sys.argv)
control_community = get_control_community(community)

print community,control_community

TEMPLATE_FILENAME = "job_template_scenarios.txt"
TEMPLATE_JOBSUBMISSION_FILE = open(TEMPLATE_FILENAME,"r")
template_jobsubmission_script = TEMPLATE_JOBSUBMISSION_FILE.read()
TEMPLATE_JOBSUBMISSION_FILE.close()

SCENARIO_JOBSUBMISSION_FILE_ROOTFILENAME = "job"

#SCENARIOS_TO_RUN = ["Central_Chips_centralARTlinkage_centralVMMC","Central_Chips_centralARTlinkage_optimVMMC","Central_Chips_centralARTlinkage_pessimVMMC","Central_Chips_optimARTlinkage_centralVMMC","Central_Chips_optimARTlinkage_optimVMMC","Central_Chips_optimARTlinkage_pessimVMMC","Central_Chips_pessimARTlinkage_centralVMMC","Central_Chips_pessimARTlinkage_optimVMMC","Central_Chips_pessimARTlinkage_pessimVMMC","Optim_Chips_centralARTlinkage_centralVMMC","Optim_Chips_centralARTlinkage_optimVMMC","Optim_Chips_centralARTlinkage_pessimVMMC","Optim_Chips_optimARTlinkage_centralVMMC","Optim_Chips_optimARTlinkage_optimVMMC","Optim_Chips_optimARTlinkage_pessimVMMC","Optim_Chips_pessimARTlinkage_centralVMMC","Optim_Chips_pessimARTlinkage_optimVMMC","Optim_Chips_pessimARTlinkage_pessimVMMC","Pessim_Chips_centralARTlinkage_centralVMMC","Pessim_Chips_centralARTlinkage_optimVMMC","Pessim_Chips_centralARTlinkage_pessimVMMC","Pessim_Chips_optimARTlinkage_centralVMMC","Pessim_Chips_optimARTlinkage_optimVMMC","Pessim_Chips_optimARTlinkage_pessimVMMC","Pessim_Chips_pessimARTlinkage_centralVMMC","Pessim_Chips_pessimARTlinkage_optimVMMC","Pessim_Chips_pessimARTlinkage_pessimVMMC"]


SCENARIOS_TO_RUN = ["Central_Chips_centralARTlinkage_centralVMMC","Optim_Chips_optimARTlinkage_optimVMMC","Pessim_Chips_pessimARTlinkage_pessimVMMC"]


print "Check that popart-ibm.exe file is in directory with correct flags for printing."


SCRIPTS_TO_RUN = []
# This script should run in a directory called something like JOB_SCRIPTS_SCENARIOS, 
# so we take its parent directory as the input directory
input_dir = "/".join(os.getcwd().split("/")[:-1])+"/"





for s in SCENARIOS_TO_RUN:
    this_job_submission_script = template_jobsubmission_script.replace("INPUTDIRECTORY",s)

    job_name = get_job_name(community,s)
    this_job_submission_script = update_job_script(this_job_submission_script,job_name,community,input_dir,control_community,s,NOT_CF)

    THISSCRIPTNAME = SCENARIO_JOBSUBMISSION_FILE_ROOTFILENAME+s+".sh"
    outfile = open(THISSCRIPTNAME,"w")
    outfile.write(this_job_submission_script)
    outfile.close()
    SCRIPTS_TO_RUN += [THISSCRIPTNAME]
    

print "Run the following: (ie copy and paste in command line)"

for script in SCRIPTS_TO_RUN:
    print "qsub "+script


# Now make counterfactual:
cf_script = replace_ibm_call_with_counterfactual(template_jobsubmission_script)

cf_job_name = get_job_name(community,"cf")
cf_script = update_job_script(cf_script,cf_job_name,community,input_dir,control_community,SCENARIOS_TO_RUN[0],IS_CF)

results_dir = "SCENARIOS_COMMUNITY$community/RESULTS/$directory"
results_dir_cf = "SCENARIOS_COMMUNITY$community/RESULTS/CF"


cf_script = cf_script.replace(results_dir,results_dir_cf)


cf_filename = "job_cf.sh"
outfile = open(cf_filename,"w")
outfile.write(cf_script)
outfile.close()

print "qsub "+cf_filename
