# Script to pull out specific outputs from a set of annual_output.csv files and plot them in R.

import glob, sys, os

def read_ANNUALOUTPUT_header(annualoutput_filename,headernames):
    annualoutput_file = open(annualoutput_filename,"r")
    header = annualoutput_file.readlines()[0].rstrip().split(",")
    annualoutput_file.close()

    i = [header.index(s) for s in headernames]
    try:
        i = [header.index(s) for s in headernames]
    except:
        print("Error: header not found. Exiting\n")
        sys.exit(1)
    return i

# Opens a file and returns the output (excluding the first line, which is assumed to be a header) as a list, where each element is a line of the file.
def read_data(filename):
    infile = open(filename, "r")
    data_raw = infile.read().rstrip().splitlines()
    infile.close()
    
    # First line is a header:
    return data_raw[1:]



def read_annual_output_files_and_extract_data(annualoutputfiledir,plot_output_filename):


    annualoutputfiles = glob.glob(annualoutputfiledir + "/Annual_outputs_CL*.csv")

    [i_prev] = read_ANNUALOUTPUT_header(annualoutputfiles[0],["Prevalence"])



    outputs = {}
    
    # Process each of the Annual output files
    for n,f in enumerate(annualoutputfiles):

        # Read the data from a single file (header is not used)
        run_data = read_data(f)

        

        for line in run_data:

            [year,prev] = [line.split(",")[index] for index in [0,i_prev]]
            if(n==0):
                outputs[year] = [prev]
            else:
                outputs[year] += [prev]
                
        
    outstring = ""
    years_saved = outputs.keys()
    years_saved.sort()
    for year in years_saved:
        outstring += str(year)+","
        for n in range(len(annualoutputfiles)):
            outstring += str(outputs[year][n])+","
        outstring = outstring.rstrip(",") +"\n"
        

    #print outstring
    outfile = open(annualoutputfiledir + "/"+plot_output_filename,"w")
    outfile.write(outstring)
    outfile.close()



resultsdir = "/home/mike/MANICALAND/manicaland-dev/IBM_simul/results/RESULTS/Output/"

outputfilename = "Summary_annual_output_prevalence.csv"    
read_annual_output_files_and_extract_data(resultsdir,outputfilename)


plotname = "prevalenceplot.pdf"
rcmd_string = "Rscript make_annual_output_prev_plot_Rplot.R "+resultsdir+outputfilename+" "+plotname
print rcmd_string
os.system(rcmd_string)

os.system("evince --fullscreen "+plotname)
