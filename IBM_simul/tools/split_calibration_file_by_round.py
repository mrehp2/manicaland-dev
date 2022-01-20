# Code does 2 things:
# 1. splits the Calibration.csv file into files by round (so can read a single one in OpenOffice).
# 2. Takes a single round (currently R7 - chosen on line 128: "calculate_cascade("params/Round7_Calibration.csv")")
#     and prints certain cascade outputs (currently lines 120-124 using calls to print_prop()).
#     for certain age groups (defined on line 67 - "age_groups = [[15,19],[20,24],[40,44]]")


import sys


def readfile(infilename):
    infile = open(infilename,"r")
    alldata = infile.read().splitlines()
    infile.close()

    return(alldata)

def get_round_data(i_round_start,i_round_end,i_runnumber,header,data):
    outstring = "RunNumber,"+",".join(header[i_round_start:i_round_end+1])+"\n"
    for unsplitline in data:
        line = unsplitline.split(",")
        outstring += line[i_runnumber] + "," + ",".join(line[i_round_start:i_round_end+1])+"\n"
    return outstring


def make_individual_round_calibration_files(rawheader,fulldata):
    header = rawheader.split(",")
    RunNumber = header.index("RunNumber")

    roundstart = [header.index(i_name) for i_name in ["CohortRound"+str(i)+"NtotM13" for i in range(1,8)]]

    for (r,i_round) in enumerate(roundstart):
        outfilename = "params/Round"+str(r+1)+"_Calibration.csv"
        if(r<len(roundstart)-1):
            i_round_end = roundstart[r+1]-1
        else:
            i_round_end = len(header)
            
        rounddata = get_round_data(i_round,i_round_end,RunNumber,header,fulldata)
        
        outfile = open(outfilename,"w")
        outfile.write(rounddata)
        outfile.close()

def print_prop(denom,num,run_list,age_groups):
    outstring = "Run,"
    for (i,a) in enumerate(age_groups):
        outstring += "-".join([str(x) for x in a])+","
    outstring += "\n"
    for r in run_list:
        outstring += str(r)+","
        for (i,a) in enumerate(age_groups):
            outstring += "{:.4f}".format(num[r][i]/(denom[r][i]*1.0))+","
            #outstring += str(num[r][i]/(denom[r][i]*1.0))+","
        outstring += "\n"
    print outstring
    

# Given a single round file, generate cascade for set age groups:
def calculate_cascade(infilename):
    # params/Round7_Calibration.csv
    round = infilename.replace("params/Round","").replace("_Calibration.csv","")

    calibration_file = open(infilename,"r")
    calibration_data = calibration_file.readlines()
    calibration_header = calibration_data[0].split(",")

    age_groups = [[15,19],[20,24],[40,44]]
    i_NM = []
    i_posM = []
    i_awareM = []
    i_artM = []
    i_NF = []
    i_posF = []
    i_awareF = []
    i_artF = []
    
    for g in age_groups:
        i_NM += [[calibration_header.index("CohortRound"+round+"NtotM"+str(age)) for age in g]]
        i_posM += [[calibration_header.index("CohortRound"+round+"NposM"+str(age)) for age in g]]
        i_awareM += [[calibration_header.index("CohortRound"+round+"NawareM"+str(age)) for age in g]]
        i_artM += [[calibration_header.index("CohortRound"+round+"NonARTM"+str(age)) for age in g]]
        i_NF += [[calibration_header.index("CohortRound"+round+"NtotF"+str(age)) for age in g]]
        i_posF += [[calibration_header.index("CohortRound"+round+"NposF"+str(age)) for age in g]]
        i_awareF += [[calibration_header.index("CohortRound"+round+"NawareF"+str(age)) for age in g]]
        i_artF += [[calibration_header.index("CohortRound"+round+"NonARTF"+str(age)) for age in g]]
    i_run = calibration_header.index("RunNumber")
    
    age_group_outputs_NM = {}
    age_group_outputs_posM = {}
    age_group_outputs_awareM = {}
    age_group_outputs_artM = {}
    age_group_outputs_NF = {}
    age_group_outputs_posF = {}
    age_group_outputs_awareF = {}
    age_group_outputs_artF = {}
    allruns = []
    for unsplitline in calibration_data[1:]:
        line = unsplitline.split(",")
        run = line[i_run]
        allruns += [run]
        age_group_outputs_NM[run] = [0]*len(age_groups)
        age_group_outputs_posM[run] = [0]*len(age_groups)
        age_group_outputs_awareM[run] = [0]*len(age_groups)
        age_group_outputs_artM[run] = [0]*len(age_groups)
        age_group_outputs_NF[run] = [0]*len(age_groups)
        age_group_outputs_posF[run] = [0]*len(age_groups)
        age_group_outputs_awareF[run] = [0]*len(age_groups)
        age_group_outputs_artF[run] = [0]*len(age_groups)
        for (i,g) in enumerate(age_groups):
            age_group_outputs_NM[run][i] = sum([int(x) for x in line[i_NM[i][0]:i_NM[i][1]+1]])
            age_group_outputs_posM[run][i] = sum([int(x) for x in line[i_posM[i][0]:i_posM[i][1]+1]])
            age_group_outputs_awareM[run][i] = sum([int(x) for x in line[i_awareM[i][0]:i_awareM[i][1]+1]])
            age_group_outputs_artM[run][i] = sum([int(x) for x in line[i_artM[i][0]:i_artM[i][1]+1]])
            age_group_outputs_NF[run][i] = sum([int(x) for x in line[i_NF[i][0]:i_NF[i][1]+1]])
            age_group_outputs_posF[run][i] = sum([int(x) for x in line[i_posF[i][0]:i_posF[i][1]+1]])
            age_group_outputs_awareF[run][i] = sum([int(x) for x in line[i_awareF[i][0]:i_awareF[i][1]+1]])
            age_group_outputs_artF[run][i] = sum([int(x) for x in line[i_artF[i][0]:i_artF[i][1]+1]])

    print "HIV prevalence"
    print_prop(age_group_outputs_NM,age_group_outputs_posM,allruns,age_groups)
    print "ART awareness"
    print_prop(age_group_outputs_awareM,age_group_outputs_artM,allruns,age_groups)
####################################
calibration_file = "params/Output/Calibration_output_CL05_Zim_patch0_Rand1_0.csv"
alldata = readfile(calibration_file)
make_individual_round_calibration_files(alldata[0],alldata[1:])

calculate_cascade("params/Round7_Calibration.csv")


#CohortRound1NtotM13

