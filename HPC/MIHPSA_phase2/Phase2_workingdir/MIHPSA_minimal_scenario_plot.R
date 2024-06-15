## Code compares minimal with essential scenario:

rm(list=ls())
library(ggplot2)
library(RColorBrewer)
library(dplyr)

essential_dir <- "results_statusquo/Output"
minimal_dir <- "results_minimal/Output"
##minimal_dir <- "results_minimal_plusCUPP//Output"
nruns <- 10

years.to.plot <- seq(2020,2050)

read_outputs <- function(filedir,nruns)
{


    outputs <- list()



    for(i in 1:nruns){
        inputfilename <- paste0(filedir,"/MIHPSA_output_CL05_Zim_patch0_Rand1_Run",as.character(i),"_0.csv")
        outputs[[(i)]] <- read.csv(inputfilename,header=T,sep=",")

    }


    return(outputs)
    
}

get_HIVpositivity_rate <- function(list.essential,list.minimal,nruns, years){
    # generate_extra_outputs(essential.outputs,minimal.outputs,nruns, seq(2022,2024))

    extra.tests.cumulative <- (list.essential[[1]]$N_HIVtests_15to24F - list.minimal[[1]]$N_HIVtests_15to24F)[which(list.essential[[1]]$Year %in% years)]
    extra.diagnoses.cumulative <- (list.essential[[1]]$N_newHIVdiagnoses_15to24F - list.minimal[[1]]$N_newHIVdiagnoses_15to24F)[which(list.essential[[1]]$Year %in% years)]

    extra.tests <- extra.tests.cumulative[2:length(extra.tests.cumulative)] - extra.tests.cumulative[1:(length(extra.tests.cumulative)-1)]
    extra.diagnoses <- extra.diagnoses.cumulative[2:length(extra.diagnoses.cumulative)] - extra.diagnoses.cumulative[1:(length(extra.diagnoses.cumulative)-1)]

    positivity <- data.frame(t=years[2:length(years)],rate=extra.diagnoses/extra.tests,run="1")
    


    for (i in 2:nruns){
        extra.tests.cumulative <- (list.essential[[i]]$N_HIVtests_15to24F - list.minimal[[i]]$N_HIVtests_15to24F)[which(list.essential[[i]]$Year %in% years)]
        extra.diagnoses.cumulative <- (list.essential[[i]]$N_newHIVdiagnoses_15to24F - list.minimal[[i]]$N_newHIVdiagnoses_15to24F)[which(list.essential[[i]]$Year %in% years)]
        
        extra.tests <- extra.tests.cumulative[2:length(extra.tests.cumulative)] - extra.tests.cumulative[1:(length(extra.tests.cumulative)-1)]
        extra.diagnoses <- extra.diagnoses.cumulative[2:length(extra.diagnoses.cumulative)] - extra.diagnoses.cumulative[1:(length(extra.diagnoses.cumulative)-1)]

        positivity.temp <- data.frame(t=years[2:length(years)],rate=extra.diagnoses/extra.tests,run=as.character(i))

        positivity <- rbind(positivity,positivity.temp) 
    }
    return(positivity)

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



plot.change.minimal.essential <- function(list.numerator,list.denominator,i.col,years.to.plot,expected.value.ll,expected.value.ul,nruns,y.title,main.title){

    
    plot.df <- data.frame(t=years.to.plot,outcome=list.numerator[[1]][list.numerator[[1]]$Year %in% years.to.plot,i.col]/list.denominator[[1]][list.denominator[[1]]$Year %in% years.to.plot,i.col], run=1)

    for (i in 2:nruns){
        temp.df <- data.frame(t=years.to.plot,outcome=list.numerator[[i]][list.numerator[[i]]$Year %in% years.to.plot,i.col]/list.denominator[[i]][list.denominator[[i]]$Year %in% years.to.plot,i.col], run=i)
        plot.df <- rbind(plot.df,temp.df) 
    }

    plot.df$run <- as.character(plot.df$run)

    p <- ggplot() + geom_line(data=plot.df, aes(x=t, y=outcome, color=run)) +
        geom_vline(xintercept=2023, linetype="dotted", color = "black") +
        geom_hline(yintercept=expected.value.ll, linetype="dashed", color = "red") +
        geom_hline(yintercept=expected.value.ul, linetype="dashed", color = "red") +
        ggtitle(main.title) + labs(x="", y=y.title)
    
    return(p)
    #return(plot.df)

}

essential.outputs <- read_outputs(essential_dir,nruns)
minimal.outputs <- read_outputs(minimal_dir,nruns)

#df <- generate_extra_outputs(essential.outputs,minimal.outputs,nruns, seq(2022,2024))



positivity.rate.SBCC <- get_HIVpositivity_rate(essential.outputs,minimal.outputs,nruns, seq(2022,2030))
mean(positivity.rate.SBCC[positivity.rate.SBCC$t %in% 2023,]$rate)
## 0.78%



####################
## Add in condom non-use measures:
for(i in 1:nruns){
    essential.outputs[[i]]$prop.nocond.LT <- 1.0-essential.outputs[[i]]$prop_longtermpartnership_condomuse
    essential.outputs[[i]]$prop.nocond.nonreg <- 1.0-essential.outputs[[i]]$prop_nonregpartnership_condomuse
    essential.outputs[[i]]$prop.nocond.concurrent <- 1.0-essential.outputs[[i]]$prop_concurrentpartnership_condomuse
    minimal.outputs[[i]]$prop.nocond.LT <- 1.0-minimal.outputs[[i]]$prop_longtermpartnership_condomuse
    minimal.outputs[[i]]$prop.nocond.nonreg <- 1.0-minimal.outputs[[i]]$prop_nonregpartnership_condomuse
    minimal.outputs[[i]]$prop.nocond.concurrent <- 1.0-minimal.outputs[[i]]$prop_concurrentpartnership_condomuse

}



######################################
## Get column indices:

col.names <- colnames(essential.outputs[[1]])

i.nconcurrentpartnerships15to49 <- which(col.names=="n_concurrent_partnerships_15to49")
i.nmultiplepartnerships15to49 <- which(col.names=="n_multiple_partnerships_lastyear_15to49")

i.propcond_longterm <- which(col.names=="prop_longtermpartnership_condomuse")
i.propcond_nonreg <- which(col.names=="prop_nonregpartnership_condomuse")

i.propcond_concurrent <- which(col.names=="prop_concurrentpartnership_condomuse")


i.nhivtests.15to24F <- which(col.names=="N_HIVtests_15to24F")

i.npop.15to24F <- which(col.names=="NPop_15to24_female")

i.prop.nocond_longterm <- which(col.names=="prop.nocond.LT")
i.prop.nocond_nonreg <- which(col.names=="prop.nocond.nonreg")
i.prop.nocond_concurrent <- which(col.names=="prop.nocond.concurrent")


#x <- plot.change.minimal.essential(essential.outputs,minimal.outputs,i.nconcurrentpartnerships15to49,years.to.plot,(1-0.07),nruns)

pdf(paste0(minimal_dir,"/vs_statusquo_concurrentpartnerships.pdf"))
plot.change.minimal.essential(minimal.outputs,essential.outputs,i.nconcurrentpartnerships15to49,years.to.plot,1/(1.0-0.06),1/(1.0-0.0),nruns,"Proportion change in partnerships (compared to essential scenario)","Number of concurrent partnerships")
dev.off()

pdf(paste0(minimal_dir,"/vs_statusquo_multiplepartnerships.pdf"))
plot.change.minimal.essential(minimal.outputs,essential.outputs,i.nmultiplepartnerships15to49,years.to.plot,1/(1.0-0.06),1/(1.0-0.0),nruns,"Proportion change in partnerships (compared to essential scenario)","Number of  multiple partnerships")
dev.off()


pdf(paste0(minimal_dir,"/vs_statusquo_condom_nonuse_LTP.pdf"))
plot.change.minimal.essential(minimal.outputs,essential.outputs,i.prop.nocond_longterm,years.to.plot,1/(1.0-0.17),1/(1.0-0.17),nruns,"Proportion change in partnerships (compared to essential scenario)","Condom not used in long-term partnerships")
dev.off()

pdf(paste0(minimal_dir,"/vs_statusquo_condom_nonuse_nonreg.pdf"))
plot.change.minimal.essential(minimal.outputs,essential.outputs,i.prop.nocond_nonreg,years.to.plot,1/(1.0-0.20),1/(1.0-0.03),nruns,"Proportion change in partnerships (compared to essential scenario)","Condom not used in non-regular partnerships")
dev.off()


pdf(paste0(minimal_dir,"/vs_statusquo_condom_nouse_concurrent.pdf"))
plot.change.minimal.essential(minimal.outputs,essential.outputs,i.prop.nocond_concurrent,years.to.plot,1/(1.0-0.20),1/(1.0-0.03),nruns,"Proportion change in partnerships (compared to essential scenario)","Condom not used in concurrent partnerships")
dev.off()


## Can't use this as it's cumulative tests:
#plot.change.minimal.essential(essential.outputs,minimal.outputs,i.nhivtests.15to24F,years.to.plot,1.0/(1.0-0.11*0.17),1.0/(1.0-0.03*0.17),nruns,"Proportion change in HIV tests per year (compared to essential scenario)","HIV testing in 15-24 year old women")





essential.tests <- convert_cumulative_to_annual_output(essential.outputs, i.nhivtests.15to24F, nruns)
minimal.tests <- convert_cumulative_to_annual_output(minimal.outputs, i.nhivtests.15to24F, nruns)

essential.tests$comparison <- minimal.tests$annual.output/essential.tests$annual.output
essential.tests <- essential.tests[essential.tests$t %in% years.to.plot,]

pdf(paste0(minimal_dir,"/vs_statusquo_HIVtests15to24F.pdf"))
ggplot() + geom_line(data=essential.tests, aes(x=t, y=comparison, color=run)) +
        geom_vline(xintercept=2023, linetype="dotted", color = "black") +
        geom_hline(yintercept=(1.0-0.053), linetype="dashed", color = "red") +
        geom_hline(yintercept=(1.0-0.053), linetype="dashed", color = "red") +
        ggtitle("HIV testing in 15-24 year old women") + labs(x="", y="Proportion change in HIV tests per year (compared to essential scenario)")
dev.off()

i.2021 <- which(essential.outputs[[1]]$Year==2021)
IBM.pop.size.2021 <- c()
for(i in 1:nruns){
    IBM.pop.size.2021 <- c(IBM.pop.size.2021,essential.outputs[[i]]$Npop_15plus_male[i.2021] + essential.outputs[[i]]$Npop_15plus_female[i.2021])
}

## 15+ population in 2021:
real.pop.size.2021 <- 8773997.323
pop.scale <- real.pop.size.2021/IBM.pop.size.2021
essential.tests$rescaled.tests <- -1
for(i in 1:nruns){
    essential.tests$rescaled.tests[essential.tests$run %in% i] <- essential.tests$annual.output[essential.tests$run %in% i]*pop.scale[i]
}

minimal.tests$rescaled.tests <- -1
for(i in 1:nruns){
    minimal.tests$rescaled.tests[minimal.tests$run %in% i] <- minimal.tests$annual.output[minimal.tests$run %in% i]*pop.scale[i]
}
minimal.tests <- minimal.tests[minimal.tests$t %in% seq(2020,2050),]

combined.tests <- cbind(essential.tests[,c(1,3,5)],minimal.tests[,4])
colnames(combined.tests)[4] <- "rescaled.tests.minimal"

median.tests <- combined.tests %>% group_by(t) %>%
       summarise(median.essential=median(rescaled.tests), median.minimal=median(rescaled.tests.minimal),median.diff=median(rescaled.tests-rescaled.tests.minimal))

pdf(paste0(minimal_dir,"/vs_statusquo_NumberHIVtests15to24F.pdf"))
ggplot(data=median.tests, aes(x=t, y=median.essential)) +
    geom_line() + 
    geom_line(aes(y=median.minimal),linetype="dotted") +
        ggtitle("Median annual number of HIV tests 15-24F") + labs(x="", y="Number of tests") 
dev.off()

median.tests$median.essential - median.tests$median.minimal




##############################################################
## HIV incidence:
##############################################################

## i.newinf.1524M <- which(col.names=="N_newHIVinfections_15to24_male")
## i.newinf.2549M <- which(col.names=="N_newHIVinfections_25to49_male")
## i.newinf.1524F <- which(col.names=="N_newHIVinfections_15to24_female")
## i.newinf.2549F <- which(col.names=="N_newHIVinfections_25to49_female")

## i.npop.1549M <- which(col.names=="NPop_15to49_male")
## i.npop.1549F <- which(col.names=="NPop_15to49_female")

## i.npos.1549M <- which(col.names=="NPos_15to49_male")
## i.npos.1549F <- which(col.names=="NPos_15to49_female")


for (i in 1:nruns){

    essential.outputs[[i]]$cumulative.newcases <- essential.outputs[[i]]$N_newHIVinfections_15to24_male+essential.outputs[[i]]$N_newHIVinfections_15to24_female + essential.outputs[[i]]$N_newHIVinfections_25to49_male+essential.outputs[[i]]$N_newHIVinfections_25to49_female
    essential.outputs[[i]]$newcases <- c(0,essential.outputs[[i]]$cumulative.newcases[2:length(essential.outputs[[i]]$cumulative.newcases)]-essential.outputs[[i]]$cumulative.newcases[1:(length(essential.outputs[[i]]$cumulative.newcases)-1)])    
    essential.outputs[[i]]$incidence <- 100*(essential.outputs[[i]]$newcases) / (essential.outputs[[i]]$NPop_15to49_male + essential.outputs[[i]]$NPop_15to49_female - essential.outputs[[i]]$NPos_15to49_male - essential.outputs[[i]]$NPos_15to49_female)


    minimal.outputs[[i]]$cumulative.newcases <- minimal.outputs[[i]]$N_newHIVinfections_15to24_male+minimal.outputs[[i]]$N_newHIVinfections_15to24_female + minimal.outputs[[i]]$N_newHIVinfections_25to49_male+minimal.outputs[[i]]$N_newHIVinfections_25to49_female
    minimal.outputs[[i]]$newcases <- c(0,minimal.outputs[[i]]$cumulative.newcases[2:length(minimal.outputs[[i]]$cumulative.newcases)]-minimal.outputs[[i]]$cumulative.newcases[1:(length(minimal.outputs[[i]]$cumulative.newcases)-1)])    
    minimal.outputs[[i]]$incidence <- 100*(minimal.outputs[[i]]$newcases) / (minimal.outputs[[i]]$NPop_15to49_male + minimal.outputs[[i]]$NPop_15to49_female - minimal.outputs[[i]]$NPos_15to49_male - minimal.outputs[[i]]$NPos_15to49_female)
    
}

i.incidence.15to49 <- which(colnames(essential.outputs[[1]])=="incidence")

incidence.df <- data.frame(t=years.to.plot,outcome.essential=essential.outputs[[1]][essential.outputs[[1]]$Year %in% years.to.plot,i.incidence.15to49], run="1", outcome.minimal=minimal.outputs[[1]][minimal.outputs[[1]]$Year %in% years.to.plot,i.incidence.15to49])

for (i in 2:nruns){
    temp.df <- data.frame(t=years.to.plot,outcome.essential=essential.outputs[[i]][essential.outputs[[i]]$Year %in% years.to.plot,i.incidence.15to49], run=as.character(i), outcome.minimal=minimal.outputs[[i]][minimal.outputs[[i]]$Year %in% years.to.plot,i.incidence.15to49])
    incidence.df <- rbind(incidence.df,temp.df) 
}

pdf(paste0(minimal_dir,"/vs_statusquo_HIVincidence_byrun.pdf"))
ggplot(data=incidence.df, aes(x=t, y=outcome.essential, group=run, color=run)) +
    geom_line() + 
    geom_line(aes(y=outcome.minimal),linetype="dotted") +
    ggtitle("HIV incidence 15-49 year olds (by run)") + labs(x="", y="HIV incidence per 100 py")
dev.off()


pdf(paste0(minimal_dir,"/vs_statusquo_HIVincidence_median.pdf"))
median.incidence.df <- incidence.df %>% group_by(t) %>%
       summarise(median.essential=median(outcome.essential), median.minimal=median(outcome.minimal))
ggplot(data=median.incidence.df, aes(x=t, y=median.essential)) +
    geom_line() + 
    geom_line(aes(y=median.minimal),linetype="dotted") +
        ggtitle("Median HIV incidence 15-49 year olds") + labs(x="", y="HIV incidence per 100 py") +
    ylim(0,1)
dev.off()















