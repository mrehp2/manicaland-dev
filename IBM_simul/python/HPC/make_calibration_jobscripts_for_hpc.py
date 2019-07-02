
import os,sys



TEMPLATE_FILENAME = "job_template_calibrate.txt"
TEMPLATE_JOBSUBMISSION_FILE = open(TEMPLATE_FILENAME,"r")
template_jobsubmission_script = TEMPLATE_JOBSUBMISSION_FILE.read()
TEMPLATE_JOBSUBMISSION_FILE.close()


TEMPLATE_RUN_R_FILENAME = "job_template_run_R_calibration.txt"
TEMPLATE_RUN_R_JOBSUBMISSION_FILE = open(TEMPLATE_RUN_R_FILENAME,"r")
template_run_r_script = TEMPLATE_RUN_R_JOBSUBMISSION_FILE.read()
TEMPLATE_RUN_R_JOBSUBMISSION_FILE.close()


# Make the correct work directory based on the current directory. Note that "well" has a much larger quota than my home directory.
def make_well_directory():
    cwd = os.getcwd().lstrip("/").split("/")
    # Remove the last element of the list if needed:
    if cwd[-1] in ["JOB_SCRIPTS","CODE","JOB_SCRIPTS_CALIBRATE"]:
        cwd.pop()
    if (cwd[0] in ["gpfs0","gpfs1","gpfs2"] and cwd[1]=="well" and cwd[2]=="fraser" and cwd[3]=="users"):
        currentuser = cwd[4]
        remainingdirs = cwd[5:]
        well_dir = "/well/fraser/users/"+currentuser+"/"
        for d in remainingdirs:
            well_dir = well_dir + d + "/"
            if not os.path.exists(well_dir):
                os.mkdir(well_dir)
        return well_dir
    else:
        print "Unknown directory structure",cwd,". Exiting"
        sys.exit(1)



# based on the current working directory, check *****
def get_runtype():
    cwd = os.getcwd().split("/")
    if cwd[-1] in ["JOB_SCRIPTS","CODE","JOB_SCRIPTS_CALIBRATE"]:
        dir = cwd[-2]
    else:
        dir = cwd[-1]
    if dir.lower().find("highacute")>=0:
        runtype = "highacute"
    elif dir.lower().find("lowacute")>=0:
        runtype = "lowacute"    
    elif dir.lower().find("lowcontamination")>=0:
        runtype = "lowcontam"   
    elif dir.lower().find("earlier_epidemic")>=0:
        runtype = "earlier"   
    elif dir.lower().find("later_epidemic")>=0:
        runtype = "later"   
    elif dir.lower().find("higher_seed")>=0:
        runtype = "high_seed"   
    elif dir.lower().find("higher_max_partners")>=0:
        runtype = "high_part"   
    elif dir.lower().find("homogeneous_by_age")>=0:
        runtype = "hom_age"   
    elif dir.lower().find("homogeneous_by_gender")>=0:
        runtype = "hom_gender"   
    elif dir.lower().find("low_test_sensitivity")>=0:
        runtype = "low_test_sens"   
    elif dir.lower().find("pessimisticart")>=0:
        runtype = "pess"    
    else:
        print "Unknown run type"
        runtype = "x"
    return runtype


ARM_A_COMMUNITIES = [2,5,8,10]
ARM_B_COMMUNITIES = [1,6,9,11]
ALL_COMMUNITIES = ARM_A_COMMUNITIES + ARM_B_COMMUNITIES

SCRIPTS_TO_RUN = []

# Make directories if needed:
working_dir = make_well_directory()


for community in ALL_COMMUNITIES:

    if not(os.system("python ../check_calibration.py "+str(community))==0):
        print "***Error for community",community,". Exiting***"
        sys.exit(1)

    if community<=12:
        job_name = "zam"+str(community)
    else:
        job_name = "sa"+str(community)
    if community in ARM_B_COMMUNITIES:
        job_name += "b"

    job_name = job_name + "_" + get_runtype()

    this_job_submission_script = template_jobsubmission_script.replace("X_JOB_NAME",job_name)
    this_job_submission_script = this_job_submission_script.replace("X_COMMUNITY_NUMBER",str(community))
    this_job_submission_script = this_job_submission_script.replace("X_WORKING_DIRECTORY",'"'+working_dir+'"')



    THISSCRIPTNAME = job_name + ".sh"


    outfile = open(THISSCRIPTNAME,"w")
    outfile.write(this_job_submission_script)
    outfile.close()
    SCRIPTS_TO_RUN += [THISSCRIPTNAME]


    # This generates the scripts that run Calibration.R and generate_posterior_params.py
    this_run_r_script = template_run_r_script.replace("X_JOB_NAME",job_name)
    this_run_r_script = this_run_r_script.replace("X_COMMUNITY_NUMBER",str(community))
    THISSCRIPTNAME = "run_r_"+job_name + ".sh"
    outfile = open(THISSCRIPTNAME,"w")
    outfile.write(this_run_r_script)
    outfile.close()


print "Run the following: (ie copy and paste in command line)"

for script in SCRIPTS_TO_RUN:
    print "qsub "+script


