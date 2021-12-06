

infile_checks = open("a1","r")
checks_data = infile_checks.read().splitlines()

formatted_checks_data = ""
for line in checks_data:
    if line.rstrip()=="":
        continue
    elif line.lstrip()[0]=="#":
        continue
    elif line.find(" <-")>0:
        temp_l = line[line.find(" <-")+len(" <-"):].lstrip()
    else:
        temp_l = line[:]
        
    if(temp_l.find(",run.params")):
        outline = temp_l.split(",run.params")[0]+")) +"
    else:
        outline = temp_l.split(",intervention.params")[0]+")) +"

    formatted_checks_data += outline.replace("check.data(","make.integer(tabulate.data(")+"\n"

outfile = open("a_processed","w")
outfile.write(formatted_checks_data)
outfile.close()



# Now the count.checks file:
infile_counts_checks = open("b","r")
counts_checks_data = infile_counts_checks.read().splitlines()

formatted_counts_checks_data = ""
for line in counts_checks_data:
    if line.rstrip()=="":
        continue
    elif line.lstrip()[0]=="#":
        continue
    elif line.find(" <-")>0:
        temp_l = line[line.find(" <-")+len(" <-"):].lstrip()
    else:
        temp_l = line[:]
    temp_l = temp_l.rstrip()
    if temp_l[-1]==")":
        temp_l +=" +"
    
    formatted_counts_checks_data += temp_l+"\n"

outfile_counts = open("b_processed","w")
outfile_counts.write(formatted_counts_checks_data)
outfile_counts.close()


