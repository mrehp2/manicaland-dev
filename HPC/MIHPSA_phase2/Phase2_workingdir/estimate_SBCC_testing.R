

## Code extracts the per-capita HIV testing rate in 15-24 year old women in 2022-23, and compares it to SBCC programme testing (Sista2Sista+DREAMS, MIHPSA Zimbabwe modellers call 21Nov2023_withNotes.pptx)

rm(list=ls())
library(ggplot2)
library(RColorBrewer)

#minimal_dir <- "params_minimal/Output"
#minimal_dir <- "params/Output"
essential_dir <- "params_essential/Output"
#essential_dir <- "params/Output"
nruns <- 10


read_outputs <- function(filedir,nruns)
{


    outputs <- list()



    for(i in 1:nruns){
        inputfilename <- paste0(filedir,"/MIHPSA_output_CL05_Zim_patch0_Rand1_Run",as.character(i),"_0.csv")
        outputs[[(i)]] <- read.csv(inputfilename,header=T,sep=",")

    }


    return(outputs)
    
}



convert_cumulative_to_annual_output <- function(this.list, i.col, nruns){
    # generate_extra_outputs(essential.outputs,minimal.outputs,nruns, seq(2022,2024))

    i.col
    nyears <- length(this.list[[1]]$Year)
    annual.output <- c(0,this.list[[1]][2:nyears,i.col] - this.list[[1]][1:(nyears-1),i.col])

    plot.df <- data.frame(t=this.list[[1]]$Year,annual.output=annual.output,run="1")
    


    for (i in 2:nruns){
        annual.output <- c(0,this.list[[i]][2:nyears,i.col] - this.list[[i]][1:(nyears-1),i.col])

        df.temp <- data.frame(t=this.list[[i]]$Year,annual.output=annual.output,run=as.character(i))
        plot.df <- rbind(plot.df,df.temp) 
    }
    return(plot.df)

}




essential.outputs <- read_outputs(essential_dir,nruns)
##minimal.outputs <- read_outputs(minimal_dir,nruns)




col.names <- colnames(essential.outputs[[1]])



## *Cumulative* HIV tests in 15-24F:
i.nhivtests.15to24F <- which(col.names=="N_HIVtests_15to24F")

i.npop.15to24F <- which(col.names=="NPop_15to24_female")


i.year <- which(essential.outputs[[1]]$Year==2022

##

ntests <- c()
npeople <- c()

for (i in 1:nruns){
    ntests <- c(ntests,(essential.outputs[[i]][i.year,i.nhivtests.15to24F] - essential.outputs[[i]][(i.year-1),i.nhivtests.15to24F]))
    npeople <- c(npeople,(essential.outputs[[i]][i.year,i.npop.15to24F]))
}


## Population size 14-24:
pop.2020.14to24F <- (822+706+ 0.2*958)
pop.2025.14to24F <- (943+787+ 0.2*1094)
pop.2023.14to24F <- (0.6*pop.2025.14to24F + 0.4*pop.2020.14to24F)*1000
pop.2022.14to24F <- (0.4*pop.2025.14to24F + 0.6*pop.2020.14to24F)*1000


##                0-4     5-9     10-14   15-19    20-24  25-29
##Women	2020	  1043	  1101	   958	   822	   706	   602
##Women	2025	  1020	  1029	  1094	   943	   787	


total.tests.14to24F.in2022 <- (ntests/npeople)*pop.2022.14to24F


adjusted.testing.rate <- (9840+22062)/total.tests.14to24F.in2022


(31213+82510)/1800000
