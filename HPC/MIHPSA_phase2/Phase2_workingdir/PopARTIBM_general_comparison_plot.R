### Code compares output between two directories of key outputs over time:

## For MIHPSA code compares e.g. minimal with essential scenario:


rm(list=ls())
library(ggplot2)
library(RColorBrewer)
library(dplyr)
library(rlang)

baseline.data.dir <- "results_statusquo/Output"
##comparator.dir <- "results_minimal/Output"
comparator.dir <- "params/Output"
nruns <- 2
years.to.plot <- seq(2020,2050)



default.barplot.cols <- c("#f1595f","#599ad3","#f9a65a","#9e66ab","#cd7058","#d77fb3")
comparison.cols <- c('Baseline'=default.barplot.cols[1], 'Intervention'=default.barplot.cols[2])
barplot.cols.grey <- brewer.pal(4,"Greys")
plot.alpha.baseline <- 0.3
plot.alpha.intervention <- 0.3


convert_cumulative_to_annual_output <- function(df, col.name, new.colname){
    i.col <- which(colnames(df)==col.name)
    new.colname <- paste0(col.name,"_annualised")
    nyears <- length(df$Year)
    df[,new.colname] <- c(0,df[(2:nyears),i.col] - df[1:(nyears-1),i.col])
    return(df)
}


## For each output that I want to be annual, make the annualised version:
make_all_cumulative_outputs_annual <- function(df){
    df <- convert_cumulative_to_annual_output(df,"N_HIVtests_15plus_female","N_HIVtests_15plus_female_annual")
    df <- convert_cumulative_to_annual_output(df,"N_HIVtests_15plus_male","N_HIVtests_15plus_male_annual")
    df <- convert_cumulative_to_annual_output(df,"N_newHIVdiagnoses_15to24F","N_newHIVdiagnoses_15to24F_annual")
    
    return(df)
}


## Read the MIHPSA_output files in a given directory. Returns a dataframe where one column is run number.
read_outputs <- function(filedir,nruns)
{
    outputs <- data.frame()
    for(i in 1:nruns){
        inputfilename <- paste0(filedir,"/MIHPSA_output_CL05_Zim_patch0_Rand1_Run",as.character(i),"_0.csv")
        this.output <- read.csv(inputfilename,header=T,sep=",")

        ## Here we add extra variables as needed:
        this.output$run <- i
        ## Convert from cumulative to annual totals:
        this.output <- make_all_cumulative_outputs_annual(this.output)


    

        
        outputs <- rbind(outputs,this.output)
    }


    ## Add in condom non-use measures:
    outputs$prop.nocond.LT <- 1.0-outputs$prop_longtermpartnership_condomuse
    outputs$prop.nocond.nonreg <- 1.0-outputs$prop_nonregpartnership_condomuse
    outputs$prop.nocond.concurrent <- 1.0-outputs$prop_concurrentpartnership_condomuse
        
    
    return(outputs)
}


####################################################################
## Extra code:
## get_HIVpositivity_rate <- function(list.essential,list.minimal,nruns, years){
##     # generate_extra_outputs(essential.outputs,minimal.outputs,nruns, seq(2022,2024))

##     extra.tests.cumulative <- (list.essential[[1]]$N_HIVtests_15to24F - list.minimal[[1]]$N_HIVtests_15to24F)[which(list.essential[[1]]$Year %in% years)]
##     extra.diagnoses.cumulative <- (list.essential[[1]]$N_newHIVdiagnoses_15to24F - list.minimal[[1]]$N_newHIVdiagnoses_15to24F)[which(list.essential[[1]]$Year %in% years)]

##     extra.tests <- extra.tests.cumulative[2:length(extra.tests.cumulative)] - extra.tests.cumulative[1:(length(extra.tests.cumulative)-1)]
##     extra.diagnoses <- extra.diagnoses.cumulative[2:length(extra.diagnoses.cumulative)] - extra.diagnoses.cumulative[1:(length(extra.diagnoses.cumulative)-1)]

##     positivity <- data.frame(t=years[2:length(years)],rate=extra.diagnoses/extra.tests,run="1")
    


##     for (i in 2:nruns){
##         extra.tests.cumulative <- (list.essential[[i]]$N_HIVtests_15to24F - list.minimal[[i]]$N_HIVtests_15to24F)[which(list.essential[[i]]$Year %in% years)]
##         extra.diagnoses.cumulative <- (list.essential[[i]]$N_newHIVdiagnoses_15to24F - list.minimal[[i]]$N_newHIVdiagnoses_15to24F)[which(list.essential[[i]]$Year %in% years)]
        
##         extra.tests <- extra.tests.cumulative[2:length(extra.tests.cumulative)] - extra.tests.cumulative[1:(length(extra.tests.cumulative)-1)]
##         extra.diagnoses <- extra.diagnoses.cumulative[2:length(extra.diagnoses.cumulative)] - extra.diagnoses.cumulative[1:(length(extra.diagnoses.cumulative)-1)]

##         positivity.temp <- data.frame(t=years[2:length(years)],rate=extra.diagnoses/extra.tests,run=as.character(i))

##         positivity <- rbind(positivity,positivity.temp) 
##     }
##     return(positivity)

## }


get_HIVpositivity_rate_new <- function(df.essential,df.minimal,nruns, years){
    # generate_extra_outputs(essential.outputs,minimal.outputs,nruns, seq(2022,2024))

    extra.tests.cumulative <- (df.essential[[1]]$N_HIVtests_15to24F - df.minimal[[1]]$N_HIVtests_15to24F)[which(df.essential[[1]]$Year %in% years)]
    extra.diagnoses.cumulative <- (df.essential[[1]]$N_newHIVdiagnoses_15to24F - df.minimal[[1]]$N_newHIVdiagnoses_15to24F)[which(df.essential[[1]]$Year %in% years)]

    extra.tests <- extra.tests.cumulative[2:length(extra.tests.cumulative)] - extra.tests.cumulative[1:(length(extra.tests.cumulative)-1)]
    extra.diagnoses <- extra.diagnoses.cumulative[2:length(extra.diagnoses.cumulative)] - extra.diagnoses.cumulative[1:(length(extra.diagnoses.cumulative)-1)]

    positivity <- data.frame(t=years[2:length(years)],rate=extra.diagnoses/extra.tests,run="1")
    


    for (i in 2:nruns){
        extra.tests.cumulative <- (df.essential[[i]]$N_HIVtests_15to24F - df.minimal[[i]]$N_HIVtests_15to24F)[which(df.essential[[i]]$Year %in% years)]
        extra.diagnoses.cumulative <- (df.essential[[i]]$N_newHIVdiagnoses_15to24F - df.minimal[[i]]$N_newHIVdiagnoses_15to24F)[which(df.essential[[i]]$Year %in% years)]
        
        extra.tests <- extra.tests.cumulative[2:length(extra.tests.cumulative)] - extra.tests.cumulative[1:(length(extra.tests.cumulative)-1)]
        extra.diagnoses <- extra.diagnoses.cumulative[2:length(extra.diagnoses.cumulative)] - extra.diagnoses.cumulative[1:(length(extra.diagnoses.cumulative)-1)]

        positivity.temp <- data.frame(t=years[2:length(years)],rate=extra.diagnoses/extra.tests,run=as.character(i))

        positivity <- rbind(positivity,positivity.temp) 
    }
    return(positivity)

}








## plot.change.minimal.essential <- function(list.numerator,list.denominator,i.col,years.to.plot,expected.value.ll,expected.value.ul,nruns,y.title,main.title){

    
##     plot.df <- data.frame(t=years.to.plot,outcome=list.numerator[[1]][list.numerator[[1]]$Year %in% years.to.plot,i.col]/list.denominator[[1]][list.denominator[[1]]$Year %in% years.to.plot,i.col], run=1)

##     for (i in 2:nruns){
##         temp.df <- data.frame(t=years.to.plot,outcome=list.numerator[[i]][list.numerator[[i]]$Year %in% years.to.plot,i.col]/list.denominator[[i]][list.denominator[[i]]$Year %in% years.to.plot,i.col], run=i)
##         plot.df <- rbind(plot.df,temp.df) 
##     }

##     plot.df$run <- as.character(plot.df$run)

##     p <- ggplot() + geom_line(data=plot.df, aes(x=t, y=outcome, color=run)) +
##         geom_vline(xintercept=2023, linetype="dotted", color = "black") +
##         geom_hline(yintercept=expected.value.ll, linetype="dashed", color = "red") +
##         geom_hline(yintercept=expected.value.ul, linetype="dashed", color = "red") +
##         ggtitle(main.title) + labs(x="", y=y.title)
    
##     return(p)
##     #return(plot.df)

## }

baseline.outputs <- read_outputs(baseline.data.dir,nruns)
comparator.outputs <- read_outputs(comparator.dir,nruns)

#df <- generate_extra_outputs(essential.outputs,minimal.outputs,nruns, seq(2022,2024))



##positivity.rate.SBCC <- get_HIVpositivity_rate(essential.outputs,minimal.outputs,nruns, seq(2022,2030))
mean(positivity.rate.SBCC[positivity.rate.SBCC$t %in% 2023,]$rate)
## 0.78%




## Create median, min and max dataframe for plot of variable "var.name"
## See https://rlang.r-lib.org/reference/args_data_masking.html for how I use data masking:
generate.summary.plot.df <- function(df,var.name)
{
    plot.df <- df  %>% group_by(Year) %>% summarise(Median=median(.data[[var.name]]),ll=min(.data[[var.name]]),ul=max(.data[[var.name]]))
    return(plot.df)
}


plot.timetrend.ribbon <- function(plot.df, plot.df.comparator,y.label,x.limits=c(NA,NA),y.limits=c(NA,NA))
{

    p <- ggplot() +
        geom_line(data=plot.df, aes(x=Year, y=100*Median, color="Baseline"), size=1, show.legend=FALSE) +
        geom_line(data=plot.df, aes(x=Year, y=100*ll, color="Baseline"), size=1, linetype="dashed", show.legend=FALSE) +
        geom_line(data=plot.df, aes(x=Year, y=100*ul, color="Baseline"), size=1, linetype="dashed", show.legend=FALSE) +
        geom_ribbon(data=plot.df, 
                    aes(x=Year, ymin=100*ll,ymax=100*ul, fill="Baseline"), alpha=plot.alpha.baseline) +
        ##facet_wrap(~pop) +
        ylab(y.label) +
        theme(axis.title.x = element_blank(),
              axis.text = element_text(size = 12),
              axis.title = element_text(size = 14),
              strip.text.x = element_text(size = 16),
              legend.position = "bottom",
              legend.title = element_blank(),
              legend.text = element_text(size = 12)) +
        ## geom_errorbar(data=validation.data.df,aes(x=t,ymin=100*ll,ymax=100*ul),color="blue") +
        ## geom_point(data=validation.data.df,aes(x=t,y=100*prevalence),color="blue") +
        ## geom_errorbar(data=calibration.data.df,aes(x=t,ymin=100*ll,ymax=100*ul),color="black",width=2, size=1) +
        ## geom_point(data=calibration.data.df,aes(x=t,y=100*prevalence),color="black", size=2)+
        ## Add in the intervention:
        geom_line(data=plot.df.comparator, aes(x=Year, y=100*Median, color="Intervention"), size=1, show.legend=FALSE) +
        geom_line(data=plot.df.comparator, aes(x=Year, y=100*ll, color="Intervention"), size=1, linetype="dashed", show.legend=FALSE) +
        geom_line(data=plot.df.comparator, aes(x=Year, y=100*ul, color="Intervention"), size=1, linetype="dashed", show.legend=FALSE) +
        geom_ribbon(data=plot.df.comparator, 
                    aes(x=Year, ymin=100*ll,ymax=100*ul, fill="Intervention"), alpha=plot.alpha.intervention)
    if(!is.na(x.limits[1])){
        p <- p + xlim(x.limits[1],x.limits[2])
    }
    if(!is.na(y.limits[1])){
        p <- p + ylim(y.limits[1],y.limits[2])
    }
    ##scale_fill_identity(name = 'the fill', guide = 'legend', values=comparison.cols, labels=c("Base","Int"))
    ##theme(panel.spacing = unit(0.8, "cm"))
    return(p)

}


##########################################################################################
##########################################################################################
## Main code:
##########################################################################################
##########################################################################################


plot.df <- generate.summary.plot.df(baseline.outputs,"N_HIVtests_15plus_female_annualised")
plot.df.comparator <- generate.summary.plot.df(comparator.outputs,"N_HIVtests_15plus_female_annualised")
pdf("N_HIVtests_15plusF_minimal_statusquo.pdf")
plot.timetrend.ribbon(plot.df, plot.df.comparator,"Number of HIV tests per year (15+ female)",x.limits=c(NA,NA),y.limits=c(NA,NA))
dev.off()


plot.df <- generate.summary.plot.df(baseline.outputs,"N_HIVtests_15plus_male_annualised")
plot.df.comparator <- generate.summary.plot.df(comparator.outputs,"N_HIVtests_15plus_male_annualised")
pdf("N_HIVtests_15plusM_minimal_statusquo.pdf")
plot.timetrend.ribbon(plot.df, plot.df.comparator,"Number of HIV tests per year (15+ male)",x.limits=c(NA,NA),y.limits=c(NA,NA))
dev.off()






##df <- baseline.outputs

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

pdf(paste0(comparator.dir,"/vs_statusquo_concurrentpartnerships.pdf"))
plot.change.minimal.essential(minimal.outputs,essential.outputs,i.nconcurrentpartnerships15to49,years.to.plot,1/(1.0-0.06),1/(1.0-0.0),nruns,"Proportion change in partnerships (compared to essential scenario)","Number of concurrent partnerships")
dev.off()
