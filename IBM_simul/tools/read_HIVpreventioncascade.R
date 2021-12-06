


data.dir <- "../results_2021_10_01/Output/"


r <- 1
data.file <- paste0(data.dir,"HIVpreventioncascade_CL05_Zim_patch0_Rand1_Run",as.string(r),"_0.csv")

run.data <- read.csv(data.file,header=T)
