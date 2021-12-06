

import glob



directory = "../results/RESULTS/Output/"


annual_output_files = glob.glob(directory+"Annual_outputs*.csv")



outputs = {}

variable_names = ["PropMenCirc"]
years = [2002,2004,2007,2010,2013,2019]

for v in variable_names:
    outputs[v] = {}
    for y in years:
        outputs[v][y] = []

    
indices = []



for i_f in range(len(annual_output_files)):
    f = open(annual_output_files[i_f],"r")
    data = f.readlines()
    f.close()
    
    if(i_f==0):
        header = data[0].split(",")
        #print header
        for v in variable_names:
            i = header.index(v)
            indices += [i]
    year0 = int(data[1].split(",")[0])
    for y in years:
        i_line = y - year0 + 1 # The 1 is the header.

        for n in range(len(variable_names)):
            i = indices[n]
            outputs[variable_names[n]][y] += [data[i_line].split(",")[i]]

file_output = ""
            
for v in variable_names:
    for y in years:
        file_output += v+","+str(y)+","
        file_output +=  ",".join(outputs[v][y])
        file_output += "\n"
print file_output
        
