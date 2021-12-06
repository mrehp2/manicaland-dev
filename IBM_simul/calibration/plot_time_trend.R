


rm(list=ls())
require(plotrix)

i.year <- 1
i.prevalence <- 2
i.incidence <- 3
i.totalpop <- 4
i.npopm <- 5
i.npopf <- 6
i.prop.lowrisk <- 7
i.prop.medrisk <- 8
i.prop.highrisk <- 9

i.npop.pos.m <- 10
i.npop.pos.f <- 11
i.prev.lowrisk <- 12
i.prev.medrisk <- 13
i.prev.highrisk <- 14

i.prop.hivposonart <- 15
i.n.needART.m <- 16
i.n.needART.f <- 17
i.n.onART.m <- 18
i.n.onART.f <- 19
i.frac.needART.onART.m <- 20
i.frac.needART.onART.f <- 21
i.prop.m.circ <- 22
i.n.womenwaitingPrEP <- 23
i.n.womenonPrEP.adherent <- 24
i.n.womenonPrEP.semiadherent <- 25
i.n.mtct.transmissions <- 26
i.n.mtct.deaths <- 27
i.n.mtct.alive.agefourteen <- 28
i.frac.mtct.alive.onART.agefourteen <- 29
i.ndied <- 30
i.frac.diedfromhiv <- 31
i.n.hsv2.m <- 32
i.n.hsv2.f <- 33
i.incidence.hsv2 <- 34
i.n.hivtests <- 35
i.frac.acute.infections <- 36




#i.women.waiting.PrEP <- which(colnames(temp)=="N_women_waiting_PrEP")


calculate.annual.number.from.cumulative <- function(cumulative.var)
{
    n.timepoints <- length(cumulative.var)
    cumulative.last.year <- c(0,cumulative.var[1:n.timepoints-1])
    annual.number <- cumulative.var - cumulative.last.year
    return(annual.number)

}


get.annual.output.model.data <- function(model.filename)
{
    stored.data.thisrun <- list()
    annual.output.data.thisrun <- read.csv(model.filename,header=T)

    stored.data.thisrun[[i.year]] <- annual.output.data.thisrun$Year

    stored.data.thisrun[[i.prevalence]] <- annual.output.data.thisrun$Prevalence
    stored.data.thisrun[[i.incidence]] <- annual.output.data.thisrun$Incidence
    stored.data.thisrun[[i.totalpop]] <- annual.output.data.thisrun$TotalPopulation
    stored.data.thisrun[[i.npopm]] <- annual.output.data.thisrun$PopulationM
    stored.data.thisrun[[i.npopf]] <- annual.output.data.thisrun$PopulationF
    stored.data.thisrun[[i.prop.lowrisk]] <- annual.output.data.thisrun$Prop_riskLow
    stored.data.thisrun[[i.prop.medrisk]] <- annual.output.data.thisrun$Prop_riskMed
    stored.data.thisrun[[i.prop.highrisk]] <- annual.output.data.thisrun$Prop_riskHigh

    stored.data.thisrun[[i.npop.pos.m]] <- annual.output.data.thisrun$NumberPositiveM
    stored.data.thisrun[[i.npop.pos.f]] <- annual.output.data.thisrun$NumberPositiveF
    
    stored.data.thisrun[[i.prev.lowrisk]] <- annual.output.data.thisrun$Prevalence_riskLow
    stored.data.thisrun[[i.prev.medrisk]] <- annual.output.data.thisrun$Prevalence_riskMed
    stored.data.thisrun[[i.prev.highrisk]] <- annual.output.data.thisrun$Prevalence_riskHigh


    stored.data.thisrun[[i.prop.hivposonart]] <- annual.output.data.thisrun$PropHIVPosONART
    stored.data.thisrun[[i.n.needART.m]] <- annual.output.data.thisrun$NNeedARTM
    stored.data.thisrun[[i.n.needART.f]] <- annual.output.data.thisrun$NNeedARTM
    stored.data.thisrun[[i.n.onART.m]] <- annual.output.data.thisrun$NOnARTM
    stored.data.thisrun[[i.n.onART.f]] <- annual.output.data.thisrun$NOnARTF
    stored.data.thisrun[[i.frac.needART.onART.m]] <- annual.output.data.thisrun$NOnARTM/annual.output.data.thisrun$NNeedARTM
    stored.data.thisrun[[i.frac.needART.onART.f]] <- annual.output.data.thisrun$NOnARTF/annual.output.data.thisrun$NNeedARTF


    stored.data.thisrun[[i.prop.m.circ]] <- annual.output.data.thisrun$PropMenCirc
    stored.data.thisrun[[i.n.womenwaitingPrEP]] <- annual.output.data.thisrun$N_women_waiting_PrEP
    stored.data.thisrun[[i.n.womenonPrEP.adherent]] <- annual.output.data.thisrun$N_women_on_PrEP_adherent
    stored.data.thisrun[[i.n.womenonPrEP.semiadherent]] <- annual.output.data.thisrun$N_women_on_PrEP_semiadherent

    stored.data.thisrun[[i.n.mtct.transmissions]] <- annual.output.data.thisrun$N_mother_to_child_transmissions
    stored.data.thisrun[[i.n.mtct.deaths]] <- annual.output.data.thisrun$N_mother_to_child_transmissions_deaths
    stored.data.thisrun[[i.n.mtct.alive.agefourteen]] <- annual.output.data.thisrun$N_mother_to_child_transmissions_alive_age14
    stored.data.thisrun[[i.frac.mtct.alive.onART.agefourteen]] <- annual.output.data.thisrun$N_mother_to_child_transmissions_alive_age14 / annual.output.data.thisrun$N_mother_to_child_transmissions_alive_onARTage14


    # Turn cumulative number of people died into annual total:
    stored.data.thisrun[[i.ndied]] <- calculate.annual.number.from.cumulative(annual.output.data.thisrun$N_dead)
    # Fraction of deaths in a year that are from HIV (numerator excludes people who were HIV+ but died for other reasons):
    stored.data.thisrun[[i.frac.diedfromhiv]] <- calculate.annual.number.from.cumulative(annual.output.data.thisrun$NDied_from_HIV) / stored.data.thisrun[[i.ndied]]

    
    stored.data.thisrun[[i.n.hsv2.m]] <- annual.output.data.thisrun$nprevalent_hsv2_m
    stored.data.thisrun[[i.n.hsv2.f]] <- annual.output.data.thisrun$nprevalent_hsv2_f
    
    stored.data.thisrun[[i.incidence.hsv2]] <- annual.output.data.thisrun$annual_incident_hsv2
    
	
    stored.data.thisrun[[i.n.hivtests]] <- annual.output.data.thisrun$NHIVTestedThisYear
    stored.data.thisrun[[i.frac.acute.infections]] <- annual.output.data.thisrun$NewCasesThisYearFromAcute / annual.output.data.thisrun$NewCasesThisYear

    return(stored.data.thisrun)
    
}

extract.annualoutput.filenames <- function(fitdata,results.rootdir)
{
    n.reps <- dim(fitdata)[1]
    
    file.snippets <- fitdata[,1]
    file.runnumbers <- fitdata[,2]
    # 3rd line is log likelihood - not needed here.
    
    results.dirnumber <- rep(NA,n.reps)
    for (i in 1:n.reps)
    {
        results.dirnumber[i] <- strsplit(as.character(file.snippets[i]),"_")[[1]][1]
    }

    
    # Filenames have the form Annual_outputs_CL05_Zim_V2.0_patch0_Rand1_Run1_PCseed0_0.csv
    # in directories like "results_2020_03_09/RESULTS1/Output/"

    file.names <- rep("",n.reps)
    for (i in 1:n.reps)
    {
        file.names[i] <- paste0(results.rootdir,"/RESULTS",results.dirnumber[i],"/Output/Annual_outputs_CL05_Zim_V2.0_patch0_Rand1_Run",file.snippets[i],".csv")
    }
    return(file.names)
}


fit.data <- read.csv("goodfits.txt",sep=" ",header=F)

annualoutput.filenames <- extract.annualoutput.filenames(fit.data,"/home/mike/MANICALAND/manicaland-dev/IBM_simul/results_2020_03_09/")




data.run1 <- get.annual.output.model.data(annualoutput.filenames[1])







my_rainbow <- c("hotpink","purple","blue","royalblue1","cyan","green","gold","orange2","red","brown","grey","black")
min.age <- 15
max.age <- 79
age.gp.width <- 5

n.age.groups <- (max.age+1-min.age)/age.gp.width

age_groups_lab <- rep("",n.age.groups)
for (i in 1:n.age.groups)
{
    i.age <- (i-1)*age.gp.width + min.age
    age_groups_lab[i] <- paste(as.character(i.age),as.character(i.age+age.gp.width-1),sep="-")
}

#age_groups_lab <- c("15-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79")

col <-  rainbow(length(age_groups_lab))

