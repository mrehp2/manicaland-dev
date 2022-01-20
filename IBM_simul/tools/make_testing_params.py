# Code that duplicates a single parameter set NRUNS times.
# Use with calibrated parameter sets to to assess how changing parameters can affect output (e.g. for MIHPSA to increase uptake of ART etc).

files = ["param_processed_patch0_barriers.csv","param_processed_patch0_cascade.csv","param_processed_patch0_demographics.csv","param_processed_patch0_HIV.csv","param_processed_patch0_HSV2.csv","param_processed_patch0_init.csv","param_processed_patch0_partnerships.csv","param_processed_patch0_PrEP_background.csv","param_processed_patch0_PrEP_intervention.csv","param_processed_patch0_times.csv"]


NRUNS = 10

def make_testing_file(f,n_test_params):
    infile = open(f,"r")
    data = infile.readlines()
    infile.close()
    
    outstring = data[0]
    for n in range(n_test_params):
        outstring += data[1]
    print outstring
    outfile = open(f,"w")
    outfile.write(outstring)
    outfile.close()

for f in files:
    make_testing_file(f,NRUNS)
