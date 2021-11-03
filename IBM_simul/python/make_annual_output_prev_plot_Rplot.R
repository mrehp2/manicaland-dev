#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

MAX.N <- 70 # Maximum number of runs to show on one graph.

# test if there is at least one argument: if not, return an error
if (length(args)<2) {
  stop("The following arguments must be supplied (input file, output file).n", call.=FALSE)
}

infilename <- args[1]
print(infilename)
outputfilename <- args[2]
print(outputfilename)

#infilename <- "/home/mike/MANICALAND/manicaland-dev/IBM_simul/results/RESULTS/Output/Summary_annual_output_prevalence.csv"    

data = read.csv(infilename,header=F,sep=",")

pdf(outputfilename)
ncols <- dim(data)[2]
if(ncols<=MAX.N+2){
    plot.indices <- seq(3,ncols)
}else{
    plot.indices <- sample(seq(3,ncols),MAX.N,replace=F)
}

plot(data[,1],100*data[,2],type="l",ylab="HIV prevalence (%)",xlab="",ylim=c(0,50))
for(i in plot.indices){
    lines(data[,1],100*data[,i])
}
dev.off()
