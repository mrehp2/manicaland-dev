import sys

# Code takes in a list of R variables (e.g. from names(r1data)) and outputs them as an R list "c(a,b,...)" - so easy to create a data cut.

# File we are reading from:
infilename = "varlist.txt"

outfile = "varlist_as_list.txt"

infile = open(infilename,"r")
vars_unformatted = infile.read().rstrip().splitlines()

# Takes a line containing one or more vars, and outputs them as a string:
def split_line(l):
    # Each variable is in quotation marks.
    # The even numbered entries in the list varlist are the actual variable names:
    varlist_messy = l.split('"')
    varlist = varlist_messy[1:len(varlist_messy):2]
    string_varlist = '","'.join(varlist)
    return [string_varlist,len(varlist)]

outstring = "c("

n_vars = 0
for vline in vars_unformatted:
    a = vline.lstrip()[0]
    if not(a=="["):
        print "Error: ",vline," does not start with a '['"
        sys.exit(1)
    vline_nonumber = vline.split("]")[1]

    [vars_line,n] = split_line(vline_nonumber)


    n_vars += n
    outstring += '"'+vars_line+'",'

outstring = outstring.rstrip(",")
outstring += ")\n"
print outstring

print n_vars
