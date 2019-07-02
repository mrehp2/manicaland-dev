
import os,sys,re


ARM_A_COMMUNITIES = [2,5,8,10]
ARM_B_COMMUNITIES = [1,6,9,11]
ARM_C_COMMUNITIES = [3,4,7,12]


# Make the job name that is passed to the queue scheduler (ie SGE, etc).
def get_job_name(community_number):
    job_name = "g" # stands for goodfits.
    if community_number<=12:
        job_name += "zam"+str(community_number)
    else:
        job_name += "sa"+str(community_number)
    if community_number in ARM_B_COMMUNITIES:
        job_name += "b"

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

# based on the current working directory, check *****
def get_runtype():
    cwd = os.getcwd().split("/")
    if cwd[-1] in ["JOB_SCRIPTS","CODE","JOB_SCRIPTS_GOODFITS"]:
        dir = cwd[-2]
    else:
        dir = cwd[-1]
    if dir.lower().find("highacute")>=0:
        runtype = "highacute"
    elif dir.lower().find("lowacute")>=0:
        runtype = "lowacute"    
    elif dir.lower().find("pessimisticart")>=0:
        runtype = "pess"    
    else:
        print "Unknown run type"
        runtype = "x"
    return runtype


####################################################################################
#### Main code:
####################################################################################


TEMPLATE_FILENAME = "job_template_goodfits.txt"
TEMPLATE_JOBSUBMISSION_FILE = open(TEMPLATE_FILENAME,"r")
template_jobsubmission_script = TEMPLATE_JOBSUBMISSION_FILE.read()
TEMPLATE_JOBSUBMISSION_FILE.close()

GOODFITS_JOBSUBMISSION_FILE_ROOTFILENAME = "job"


# This script should run in a directory called something like JOB_SCRIPTS_GOODFITS, 
# so we take its parent directory as the input directory
input_dir = "/".join(os.getcwd().split("/")[:-1])+"/"

SCRIPTS_TO_RUN = []

runtype = get_runtype()

print "Check that popart-ibm.exe file is in directory with correct flags for printing."

for community in ARM_A_COMMUNITIES+ARM_B_COMMUNITIES:

    control_community = get_control_community(community)

    #print community,control_community

    job_name = get_job_name(community)

    this_job_submission_script = template_jobsubmission_script.replace("X_JOB_NAME",job_name+runtype)
    this_job_submission_script = this_job_submission_script.replace("X_COMMUNITY_NUMBER",str(community))
    this_job_submission_script = this_job_submission_script.replace("X_CONTROL_NUMBER",str(control_community))
    this_job_submission_script = this_job_submission_script.replace("X_GOODFITS_DIR",'"'+input_dir+'"')

    THISSCRIPTNAME = job_name+".sh"
    outfile = open(THISSCRIPTNAME,"w")
    outfile.write(this_job_submission_script)
    outfile.close()
    SCRIPTS_TO_RUN += [THISSCRIPTNAME]


print "Run the following: (ie copy and paste in command line)"

for script in SCRIPTS_TO_RUN:
    print "qsub "+script

