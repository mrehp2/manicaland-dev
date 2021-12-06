
# Code checks that sum over age groups for some example outcomes is the same as in the python code.

a = read.csv("../results2/RESULTS2/Calibration_output_CL05_Zim_V2.0_patch0_Rand10_PCseed0_0.csv",header=T)




r <- 2
outcome <- "NonART"
gender <- "F"
age <- 66

get.data <- function(r,outcome,gender,age,row)
{
    n.ages <- 5 # Use 5 year age groups:
    dataname1 <- paste0("CohortRound",as.character(r),outcome,gender,as.character(age))
    
    start.col <- which(colnames(a)==dataname1)
    print(start.col)
    sum.outcomes <- sum(a[row,seq(start.col,start.col+(n.ages-1))])
    print(a[row,seq(start.col,start.col+(n.ages-1))])
    return(sum.outcomes)
}

# IN python row n starts at 0 - so need to add 1 to start at 1.
r=1; outcome="Ntot";gender="M";age="40";row=3
get.data(r,outcome,gender,age,row)

r=2; outcome="Npos";gender="F";age="20";row=11
get.data(r,outcome,gender,age,row)


r=2; outcome="Naware";gender="F";age="65";row=40
get.data(r,outcome,gender,age,row)
