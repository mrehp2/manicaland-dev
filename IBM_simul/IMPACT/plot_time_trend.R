


rm(list=ls())
require(plotrix)
require(RColorBrewer)

# These aren't used:
## i.year <- 1
## i.prevalence <- 2
## i.incidence <- 3

## i.totalpop <- 10
## i.npopm <- 12
## i.npopf <- 14
## i.prop.lowrisk <- 45
## i.prop.medrisk <- 46
## i.prop.highrisk <- 47

## i.npop.pos.m <- 11
## i.npop.pos.f <- 13
## i.prev.lowrisk <- 48
## i.prev.medrisk <- 49
## i.prev.highrisk <- 50

## i.prop.hivposonart <- 8
## i.n.needART.m <- 25
## i.n.needART.f <- 27
## i.n.onART.m <- 24
## i.n.onART.f <- 26
## ###i.frac.needART.onART.m <- 20
## ###i.frac.needART.onART.f <- 21
## i.prop.m.circ <- 28
## i.n.womenwaitingPrEP <- 30
## i.n.womenonPrEP.adherent.under25 <- 31
## i.n.womenonPrEP.adherent.25plus <- 32
## i.n.womenonPrEP.semiadherent.under25 <- 33
## i.n.womenonPrEP.semiadherent.25plus <- 34
## i.n.mtct.transmissions <- 15
## i.n.mtct.deaths <- 16
## i.n.mtct.alive.agefourteen <- 17
## i.frac.mtct.alive.onART.agefourteen <- 18
## i.ndied <- 40
## #
## i.n.diedfromhiv <- 38

## i.n.hsv2.m <- 42
## i.n.hsv2.f <- 43
## i.incidence.hsv2 <- 41
## i.n.hivtests <- 19
## #
## i.n.acute.infections <- 36






make.annualoutput.filenames <- function(n.reps,rootdir,scenario){
    if(scenario==0){
        file.tag <- ""
    }else if (scenario==1){
        file.tag <- "_NOBARRIER"
    }else if (scenario==2){
        file.tag <- "_NOPREPBARRIER"
    }else if (scenario==3){
        file.tag <- "_NOVMMCBARRIER"
    }else if (scenario==4){
        file.tag <- "_NOCONDBARRIER"
    }
    
    file.names <- rep("",n.reps)
    for (i in 1:n.reps)
    {
        file.names[i] <- paste0(rootdir,"/Annual_outputs_CL05_Zim_patch0_Rand1_Run",as.character(i),"_0",file.tag,".csv")
    }
    return(file.names)
}





calculate.annual.number.from.cumulative <- function(cumulative.var)
{
    n.timepoints <- length(cumulative.var)
    cumulative.last.year <- c(0,cumulative.var[1:n.timepoints-1])
    annual.number <- cumulative.var - cumulative.last.year
    return(annual.number)

}


## get.annual.output.model.data <- function(model.filename)
## {
##     stored.data.thisrun <- list()
##     annual.output.data.thisrun <- read.csv(model.filename,header=T)

##     stored.data.thisrun[[i.year]] <- annual.output.data.thisrun$Year

##     stored.data.thisrun[[i.prevalence]] <- annual.output.data.thisrun$Prevalence
##     stored.data.thisrun[[i.incidence]] <- annual.output.data.thisrun$Incidence
##     stored.data.thisrun[[i.totalpop]] <- annual.output.data.thisrun$TotalPopulation
##     stored.data.thisrun[[i.npopm]] <- annual.output.data.thisrun$PopulationM
##     stored.data.thisrun[[i.npopf]] <- annual.output.data.thisrun$PopulationF
##     stored.data.thisrun[[i.prop.lowrisk]] <- annual.output.data.thisrun$Prop_riskLow
##     stored.data.thisrun[[i.prop.medrisk]] <- annual.output.data.thisrun$Prop_riskMed
##     stored.data.thisrun[[i.prop.highrisk]] <- annual.output.data.thisrun$Prop_riskHigh

##     stored.data.thisrun[[i.npop.pos.m]] <- annual.output.data.thisrun$NumberPositiveM
##     stored.data.thisrun[[i.npop.pos.f]] <- annual.output.data.thisrun$NumberPositiveF
    
##     stored.data.thisrun[[i.prev.lowrisk]] <- annual.output.data.thisrun$Prevalence_riskLow
##     stored.data.thisrun[[i.prev.medrisk]] <- annual.output.data.thisrun$Prevalence_riskMed
##     stored.data.thisrun[[i.prev.highrisk]] <- annual.output.data.thisrun$Prevalence_riskHigh


##     stored.data.thisrun[[i.prop.hivposonart]] <- annual.output.data.thisrun$PropHIVPosONART
##     stored.data.thisrun[[i.n.needART.m]] <- annual.output.data.thisrun$NNeedARTM
##     stored.data.thisrun[[i.n.needART.f]] <- annual.output.data.thisrun$NNeedARTM
##     stored.data.thisrun[[i.n.onART.m]] <- annual.output.data.thisrun$NOnARTM
##     stored.data.thisrun[[i.n.onART.f]] <- annual.output.data.thisrun$NOnARTF
##     stored.data.thisrun[[i.frac.needART.onART.m]] <- annual.output.data.thisrun$NOnARTM/annual.output.data.thisrun$NNeedARTM
##     stored.data.thisrun[[i.frac.needART.onART.f]] <- annual.output.data.thisrun$NOnARTF/annual.output.data.thisrun$NNeedARTF


##     stored.data.thisrun[[i.prop.m.circ]] <- annual.output.data.thisrun$PropMenCirc
##     stored.data.thisrun[[i.n.womenwaitingPrEP]] <- annual.output.data.thisrun$N_women_waiting_PrEP
##     stored.data.thisrun[[i.n.womenonPrEP.adherent]] <- annual.output.data.thisrun$N_women_on_PrEP_adherent
##     stored.data.thisrun[[i.n.womenonPrEP.semiadherent]] <- annual.output.data.thisrun$N_women_on_PrEP_semiadherent

##     stored.data.thisrun[[i.n.mtct.transmissions]] <- annual.output.data.thisrun$N_mother_to_child_transmissions
##     stored.data.thisrun[[i.n.mtct.deaths]] <- annual.output.data.thisrun$N_mother_to_child_transmissions_deaths
##     stored.data.thisrun[[i.n.mtct.alive.agefourteen]] <- annual.output.data.thisrun$N_mother_to_child_transmissions_alive_age14
##     stored.data.thisrun[[i.frac.mtct.alive.onART.agefourteen]] <- annual.output.data.thisrun$N_mother_to_child_transmissions_alive_age14 / annual.output.data.thisrun$N_mother_to_child_transmissions_alive_onARTage14


##     # Turn cumulative number of people died into annual total:
##     stored.data.thisrun[[i.ndied]] <- calculate.annual.number.from.cumulative(annual.output.data.thisrun$N_dead)
##     # Fraction of deaths in a year that are from HIV (numerator excludes people who were HIV+ but died for other reasons):
##     stored.data.thisrun[[i.frac.diedfromhiv]] <- calculate.annual.number.from.cumulative(annual.output.data.thisrun$NDied_from_HIV) / stored.data.thisrun[[i.ndied]]

    
##     stored.data.thisrun[[i.n.hsv2.m]] <- annual.output.data.thisrun$nprevalent_hsv2_m
##     stored.data.thisrun[[i.n.hsv2.f]] <- annual.output.data.thisrun$nprevalent_hsv2_f
    
##     stored.data.thisrun[[i.incidence.hsv2]] <- annual.output.data.thisrun$annual_incident_hsv2
    
	
##     stored.data.thisrun[[i.n.hivtests]] <- annual.output.data.thisrun$NHIVTestedThisYear
##     stored.data.thisrun[[i.frac.acute.infections]] <- annual.output.data.thisrun$NewCasesThisYearFromAcute / annual.output.data.thisrun$NewCasesThisYear

##     return(stored.data.thisrun)

    
## }



get.annual.output.model.data <- function(model.filename)
{
    annual.output.data.thisrun <- read.csv(model.filename,header=T)

    year <- annual.output.data.thisrun$Year

    prevalence <- annual.output.data.thisrun$Prevalence
    incidence <- annual.output.data.thisrun$Incidence
    totalpop <- annual.output.data.thisrun$TotalPopulation
    npopm <- annual.output.data.thisrun$PopulationM
    npopf <- annual.output.data.thisrun$PopulationF
    prop.lowrisk <- annual.output.data.thisrun$Prop_riskLow
    prop.medrisk <- annual.output.data.thisrun$Prop_riskMed
    prop.highrisk <- annual.output.data.thisrun$Prop_riskHigh

    npop.pos.m <- annual.output.data.thisrun$NumberPositiveM
    npop.pos.f <- annual.output.data.thisrun$NumberPositiveF
    
    prev.lowrisk <- annual.output.data.thisrun$Prevalence_riskLow
    prev.medrisk <- annual.output.data.thisrun$Prevalence_riskMed
    prev.highrisk <- annual.output.data.thisrun$Prevalence_riskHigh


    prop.hivposonart <- annual.output.data.thisrun$PropHIVPosONART
    n.needART.m <- annual.output.data.thisrun$NNeedARTM
    n.needART.f <- annual.output.data.thisrun$NNeedARTM
    n.onART.m <- annual.output.data.thisrun$NOnARTM
    n.onART.f <- annual.output.data.thisrun$NOnARTF
    frac.needART.onART.m <- annual.output.data.thisrun$NOnARTM/annual.output.data.thisrun$NNeedARTM
    frac.needART.onART.f <- annual.output.data.thisrun$NOnARTF/annual.output.data.thisrun$NNeedARTF


    prop.m.circ <- annual.output.data.thisrun$PropMenCirc
    n.womenwaitingPrEP <- annual.output.data.thisrun$N_women_waiting_PrEP
    n.womenonPrEP.adherent.under25 <- annual.output.data.thisrun$N_women_on_PrEP_adherent_under25
    n.womenonPrEP.adherent.25plus <- annual.output.data.thisrun$N_women_on_PrEP_adherent_25plus
    n.womenonPrEP.semiadherent.under25 <- annual.output.data.thisrun$N_women_on_PrEP_semiadherent_under25
    n.womenonPrEP.semiadherent.25plus <- annual.output.data.thisrun$N_women_on_PrEP_semiadherent_25plus
    n.menonPrEP.adherent <- annual.output.data.thisrun$N_men_on_PrEP_adherent
    n.menonPrEP.semiadherent <- annual.output.data.thisrun$N_men_on_PrEP_semiadherent

    n.mtct.transmissions <- annual.output.data.thisrun$N_mother_to_child_transmissions
    n.mtct.deaths <- annual.output.data.thisrun$N_mother_to_child_transmissions_deaths
    n.mtct.alive.agefourteen <- annual.output.data.thisrun$N_mother_to_child_transmissions_alive_age14
    frac.mtct.alive.onART.agefourteen <- annual.output.data.thisrun$N_mother_to_child_transmissions_alive_age14 / annual.output.data.thisrun$N_mother_to_child_transmissions_alive_onARTage14


    # Turn cumulative number of people died into annual total:
    ndied <- calculate.annual.number.from.cumulative(annual.output.data.thisrun$N_dead)
    # Fraction of deaths in a year that are from HIV (numerator excludes people who were HIV+ but died for other reasons):
    frac.diedfromhiv <- calculate.annual.number.from.cumulative(annual.output.data.thisrun$NDied_from_HIV) / ndied

    
    n.hsv2.m <- annual.output.data.thisrun$nprevalent_hsv2_m
    n.hsv2.f <- annual.output.data.thisrun$nprevalent_hsv2_f
    
    incidence.hsv2 <- annual.output.data.thisrun$annual_incident_hsv2
    
	
    n.hivtests <- annual.output.data.thisrun$NHIVTestedThisYear
    frac.acute.infections <- annual.output.data.thisrun$NewCasesThisYearFromAcute / annual.output.data.thisrun$NewCasesThisYear



    outputs <- list(t=year,
    prevalence=prevalence,
    incidence=incidence,
    totalpop=totalpop,
    npopm=npopm,
    npopf=npopf,
    prop.lowrisk=prop.lowrisk,
    prop.medrisk=prop.medrisk,
    prop.highrisk=prop.highrisk,
    npop.pos.m=npop.pos.m,
    npop.pos.f=npop.pos.f,
    prev.lowrisk=prev.lowrisk,
    prev.medrisk=prev.medrisk,
    prev.highrisk=prev.highrisk,
    prop.hivposonart=prop.hivposonart,
    n.needART.m=n.needART.m,
    n.needART.f=n.needART.f,
    n.onART.m=n.onART.m,
    n.onART.f=n.onART.f,
    frac.needART.onART.m=frac.needART.onART.m,
    frac.needART.onART.f=frac.needART.onART.f,
    prop.m.circ=prop.m.circ,
    n.womenwaitingPrEP=n.womenwaitingPrEP,
    n.womenonPrEP.adherent.under25=n.womenonPrEP.adherent.under25,
    n.womenonPrEP.adherent.25plus=n.womenonPrEP.adherent.25plus,
    n.womenonPrEP.semiadherent.under25=n.womenonPrEP.semiadherent.under25,
    n.womenonPrEP.semiadherent.25plus=n.womenonPrEP.semiadherent.25plus,

    n.menonPrEP.adherent=n.menonPrEP.adherent,
    n.menonPrEP.semiadherent=n.menonPrEP.semiadherent,

    n.mtct.transmissions=n.mtct.transmissions,
    n.mtct.deaths=n.mtct.deaths,
    n.mtct.alive.agefourteen=n.mtct.alive.agefourteen,
    frac.mtct.alive.onART.agefourteen,frac.mtct.alive.onART.agefourteen,
    ndied=ndied,
    frac.diedfromhiv=frac.diedfromhiv,
    n.hsv2.m=n.hsv2.m,
    n.hsv2.f=n.hsv2.f,
    incidence.hsv2=incidence.hsv2,
    n.hivtests=n.hivtests,
    frac.acute.infections=frac.acute.infections)



    return(outputs)


    
}




get.data.as.list <- function(list.of.filenames)
{
    nruns <- length(list.of.filenames)

    for (i in seq(nruns))
    {
        model.filename <- list.of.filenames[i]

        annual.output.data.thisrun <- read.csv(model.filename,header=T)
        
        year <- annual.output.data.thisrun$Year
        
        prevalence <- annual.output.data.thisrun$Prevalence
        incidence <- annual.output.data.thisrun$Incidence
        totalpop <- annual.output.data.thisrun$TotalPopulation
        npopm <- annual.output.data.thisrun$PopulationM
        npopf <- annual.output.data.thisrun$PopulationF
        prop.lowrisk <- annual.output.data.thisrun$Prop_riskLow
        prop.medrisk <- annual.output.data.thisrun$Prop_riskMed
        prop.highrisk <- annual.output.data.thisrun$Prop_riskHigh
        
        npop.pos.m <- annual.output.data.thisrun$NumberPositiveM
        npop.pos.f <- annual.output.data.thisrun$NumberPositiveF
        
        prev.lowrisk <- annual.output.data.thisrun$Prevalence_riskLow
        prev.medrisk <- annual.output.data.thisrun$Prevalence_riskMed
        prev.highrisk <- annual.output.data.thisrun$Prevalence_riskHigh
        
        
        prop.hivposonart <- annual.output.data.thisrun$PropHIVPosONART
        n.needART.m <- annual.output.data.thisrun$NNeedARTM
        n.needART.f <- annual.output.data.thisrun$NNeedARTM
        n.onART.m <- annual.output.data.thisrun$NOnARTM
        n.onART.f <- annual.output.data.thisrun$NOnARTF
        frac.needART.onART.m <- annual.output.data.thisrun$NOnARTM/annual.output.data.thisrun$NNeedARTM
        frac.needART.onART.f <- annual.output.data.thisrun$NOnARTF/annual.output.data.thisrun$NNeedARTF
        
        
        prop.m.circ <- annual.output.data.thisrun$PropMenCirc
        n.womenwaitingPrEP <- annual.output.data.thisrun$N_women_waiting_PrEP
        n.womenonPrEP.adherent.under25 <- annual.output.data.thisrun$N_women_on_PrEP_adherent_under25
        n.womenonPrEP.adherent.25plus <- annual.output.data.thisrun$N_women_on_PrEP_adherent_25plus
        n.womenonPrEP.semiadherent.under25 <- annual.output.data.thisrun$N_women_on_PrEP_semiadherent_under25
        n.womenonPrEP.semiadherent.25plus <- annual.output.data.thisrun$N_women_on_PrEP_semiadherent_25plus
        n.menonPrEP.adherent <- annual.output.data.thisrun$N_men_on_PrEP_adherent
        n.menonPrEP.semiadherent <- annual.output.data.thisrun$N_men_on_PrEP_semiadherent

        n.mtct.transmissions <- annual.output.data.thisrun$N_mother_to_child_transmissions
        n.mtct.deaths <- annual.output.data.thisrun$N_mother_to_child_transmissions_deaths
        n.mtct.alive.agefourteen <- annual.output.data.thisrun$N_mother_to_child_transmissions_alive_age14
        frac.mtct.alive.onART.agefourteen <- annual.output.data.thisrun$N_mother_to_child_transmissions_alive_age14 / annual.output.data.thisrun$N_mother_to_child_transmissions_alive_onARTage14

        
        # Turn cumulative number of people died into annual total:
        ndied <- calculate.annual.number.from.cumulative(annual.output.data.thisrun$N_dead)
        # Fraction of deaths in a year that are from HIV (numerator excludes people who were HIV+ but died for other reasons):
        frac.diedfromhiv <- calculate.annual.number.from.cumulative(annual.output.data.thisrun$NDied_from_HIV) / ndied

    
        n.hsv2.m <- annual.output.data.thisrun$nprevalent_hsv2_m
        n.hsv2.f <- annual.output.data.thisrun$nprevalent_hsv2_f
    
        incidence.hsv2 <- annual.output.data.thisrun$annual_incident_hsv2
    
	
        n.hivtests <- annual.output.data.thisrun$NHIVTestedThisYear
        frac.acute.infections <- annual.output.data.thisrun$NewCasesThisYearFromAcute / annual.output.data.thisrun$NewCasesThisYear

        
        
        
        if(i==1){
            t <- annual.output.data.thisrun$Year
        
            prevalence.store <- prevalence
            incidence.store <- incidence
            totalpop.store <- totalpop
            npopm.store <- npopm
            npopf.store <- npopf
            prop.lowrisk.store <- prop.lowrisk
            prop.medrisk.store <- prop.medrisk
            prop.highrisk.store <- prop.highrisk
            
            npop.pos.m.store <- npop.pos.m
            npop.pos.f.store <- npop.pos.f
            
            prev.lowrisk.store <- prev.lowrisk
            prev.medrisk.store <- prev.medrisk
            prev.highrisk.store <- prev.highrisk
            
            
            prop.hivposonart.store <- prop.hivposonart
            n.needART.m.store <- n.needART.m
            n.needART.f.store <- n.needART.f
            n.onART.m.store <- n.onART.m
            n.onART.f.store <- n.onART.f
            frac.needART.onART.m.store <- frac.needART.onART.m
            frac.needART.onART.f.store <- frac.needART.onART.f
        
        
            prop.m.circ.store <- prop.m.circ
            n.womenwaitingPrEP.store <- n.womenwaitingPrEP
            n.womenonPrEP.adherent.under25.store <- n.womenonPrEP.adherent.under25
            n.womenonPrEP.adherent.25plus.store <- n.womenonPrEP.adherent.25plus
            n.womenonPrEP.semiadherent.under25.store <- n.womenonPrEP.semiadherent.under25
            n.womenonPrEP.semiadherent.25plus.store <- n.womenonPrEP.semiadherent.25plus
            n.menonPrEP.adherent.store <- n.menonPrEP.adherent
            n.menonPrEP.semiadherent.store <- n.menonPrEP.semiadherent
            
            n.mtct.transmissions.store <- n.mtct.transmissions
            n.mtct.deaths.store <- n.mtct.deaths
            n.mtct.alive.agefourteen.store <- n.mtct.alive.agefourteen
            frac.mtct.alive.onART.agefourteen.store <- frac.mtct.alive.onART.agefourteen
            ndied.store <- ndied
            frac.diedfromhiv.store <- frac.diedfromhiv
            
    
            n.hsv2.m.store <- n.hsv2.m
            n.hsv2.f.store <- n.hsv2.f
    
            incidence.hsv2.store <- incidence.hsv2
            n.hivtests.store <- n.hivtests
            frac.acute.infections.store <- frac.acute.infections



            

        }else{

            prevalence.store <- cbind(prevalence.store,prevalence)
            incidence.store <- cbind(incidence.store,incidence)
            totalpop.store <- cbind(totalpop.store,totalpop)
            npopm.store <- cbind(npopm.store,npopm)
            npopf.store <- cbind(npopf.store,npopf)
            prop.lowrisk.store <- cbind(prop.lowrisk.store,prop.lowrisk)
            prop.medrisk.store <- cbind(prop.medrisk.store,prop.medrisk)
            prop.highrisk.store <- cbind(prop.highrisk.store,prop.highrisk)
            
            npop.pos.m.store <- cbind(npop.pos.m.store,npop.pos.m)
            npop.pos.f.store <- cbind(npop.pos.f.store,npop.pos.f)
            
            prev.lowrisk.store <- cbind(prev.lowrisk.store,prev.lowrisk)
            prev.medrisk.store <- cbind(prev.medrisk.store,prev.medrisk)
            prev.highrisk.store <- cbind(prev.highrisk.store,prev.highrisk)
            
            
            prop.hivposonart.store <- cbind(prop.hivposonart.store,prop.hivposonart)
            n.needART.m.store <- cbind(n.needART.m.store,n.needART.m)
            n.needART.f.store <- cbind(n.needART.f.store,n.needART.f)
            n.onART.m.store <- cbind(n.onART.m.store,n.onART.m)
            n.onART.f.store <- cbind(n.onART.f.store,n.onART.f)
            frac.needART.onART.m.store <- cbind(frac.needART.onART.m.store,frac.needART.onART.m)
            frac.needART.onART.f.store <- cbind(frac.needART.onART.f.store,frac.needART.onART.f)
        
        
            prop.m.circ.store <- cbind(prop.m.circ.store,prop.m.circ)
            n.womenwaitingPrEP.store <- cbind(n.womenwaitingPrEP.store,n.womenwaitingPrEP)
            n.womenonPrEP.adherent.under25.store <- cbind(n.womenonPrEP.adherent.under25.store,n.womenonPrEP.adherent.under25)
            n.womenonPrEP.adherent.25plus.store <- cbind(n.womenonPrEP.adherent.25plus.store,n.womenonPrEP.adherent.25plus)
            n.womenonPrEP.semiadherent.under25.store <- cbind(n.womenonPrEP.semiadherent.under25.store,n.womenonPrEP.semiadherent.under25)
            n.womenonPrEP.semiadherent.25plus.store <- cbind(n.womenonPrEP.semiadherent.25plus.store,n.womenonPrEP.semiadherent.25plus)
            n.menonPrEP.adherent.store <- cbind(n.menonPrEP.adherent.store,n.menonPrEP.adherent)
            n.menonPrEP.semiadherent.store <- cbind(n.menonPrEP.semiadherent.store,n.menonPrEP.semiadherent)
            
            n.mtct.transmissions.store <- cbind(n.mtct.transmissions.store,n.mtct.transmissions)
            n.mtct.deaths.store <- cbind(n.mtct.deaths.store,n.mtct.deaths)
            n.mtct.alive.agefourteen.store <- cbind(n.mtct.alive.agefourteen.store,n.mtct.alive.agefourteen)
            frac.mtct.alive.onART.agefourteen.store <- cbind(frac.mtct.alive.onART.agefourteen.store,frac.mtct.alive.onART.agefourteen)
            ndied.store <- cbind(ndied.store,ndied)
            frac.diedfromhiv.store <- cbind(frac.diedfromhiv.store,frac.diedfromhiv)
                
            n.hsv2.m.store <- cbind(n.hsv2.m.store,n.hsv2.m)
            n.hsv2.f.store <- cbind(n.hsv2.f.store,n.hsv2.f)
    
            incidence.hsv2.store <- cbind(incidence.hsv2.store,incidence.hsv2)
            n.hivtests.store <- cbind(n.hivtests.store,n.hivtests)
            frac.acute.infections.store <- cbind(frac.acute.infections.store,frac.acute.infections)


        }
    }



    data.store <- list(t=t,
    prevalence.store=prevalence.store,
    incidence.store=incidence.store,
    totalpop.store=totalpop.store,
    npopm.store=npopm.store,
    npopf.store=npopf.store,
    prop.lowrisk.store=prop.lowrisk.store,
    prop.medrisk.store=prop.medrisk.store,
    prop.highrisk.store=prop.highrisk.store,
    npop.pos.m.store=npop.pos.m.store,
    npop.pos.f.store=npop.pos.f.store,
    prev.lowrisk.store=prev.lowrisk.store,
    prev.medrisk.store=prev.medrisk.store,
    prev.highrisk.store=prev.highrisk.store,
    prop.hivposonart.store=prop.hivposonart.store,
    n.needART.m.store=n.needART.m.store,
    n.needART.f.store=n.needART.f.store,
    n.onART.m.store=n.onART.m.store,
    n.onART.f.store=n.onART.f.store,
    frac.needART.onART.m.store=frac.needART.onART.m.store,
    frac.needART.onART.f.store=frac.needART.onART.f.store,
    prop.m.circ.store=prop.m.circ.store,
    n.womenwaitingPrEP.store=n.womenwaitingPrEP.store,
    n.womenonPrEP.adherent.under25.store=n.womenonPrEP.adherent.under25.store,
    n.womenonPrEP.adherent.25plus.store=n.womenonPrEP.adherent.25plus.store,
    n.womenonPrEP.semiadherent.under25.store=n.womenonPrEP.semiadherent.under25.store,
    n.womenonPrEP.semiadherent.25plus.store=n.womenonPrEP.semiadherent.25plus.store,

    n.menonPrEP.adherent.store=n.menonPrEP.adherent.store,
    n.menonPrEP.semiadherent.store=n.menonPrEP.semiadherent.store,

    n.mtct.transmissions.store=n.mtct.transmissions.store,
    n.mtct.deaths.store=n.mtct.deaths.store,
    n.mtct.alive.agefourteen.store=n.mtct.alive.agefourteen.store,
    frac.mtct.alive.onART.agefourteen.store,frac.mtct.alive.onART.agefourteen.store,
    ndied.store=ndied.store,
    frac.diedfromhiv.store=frac.diedfromhiv.store,
    n.hsv2.m.store=n.hsv2.m.store,
    n.hsv2.f.store=n.hsv2.f.store,
    incidence.hsv2.store=incidence.hsv2.store,
    n.hivtests.store=n.hivtests.store,
    frac.acute.infections.store=frac.acute.infections.store)



    return(data.store)
}





plot.polygon <- function(t,ylowerpolygon,yupperpolygon,ymean,ylowerdotted,yupperdotted,polygon.col,lines.col,firstpolygon,x.range,y.range,plot.title,y.axis.label)
{

    alpha.adjust <- 0.3
    #unadjusted.col <- colorRampPalette(c(polygon.cols[1], "black"))(100)[50]
    
    if (firstpolygon==1){
        # Type="n" means don't draw anything:
        plot(t,ymean,type="n",lty=1,lwd=0.5, ,xlab="",ylab=y.axis.label,cex.lab=1.4,cex.axis=1.4,xlim=x.range,ylim = y.range,main=plot.title,cex.main=1.2)
    }
    t.max <- t[length(t)]
    t.min <- t[1]

    polygon(x=c(t,t.max,rev(t),t.min),
        y=c(ylowerpolygon,ylowerpolygon[length(ylowerpolygon)],rev(yupperpolygon),yupperpolygon[1]),col=adjustcolor(polygon.col,alpha.f=alpha.adjust),border=NA)
    lines(t,ymean,lwd=2,,col=lines.col)
    if (!(is.na(ylowerdotted))){
        lines(t,ylowerdotted,lwd=1,lty=3,col=lines.col)
        lines(t,yupperdotted,lwd=1,lty=3,col=lines.col)
    }
    
}


# Multipurpose plot function for different barrier scenarios:
plot.one.scenario <- function(t,baseline.data,lq,uq,x.range,y.range,plot.filename,plot.legend,plot.title,y.axis.label)
{

    if(!is.na(plot.filename)){
        pdf(plot.filename)
    }
    
        
    plot.polygon(t=t,
                 ylowerpolygon=apply(baseline.data,1,quantile,lq),
                 yupperpolygon=apply(baseline.data,1,quantile,uq),
                 ymean=apply(baseline.data,1, median, na.rm = TRUE),
                 ylowerdotted=NA,
                 yupperdotted=NA,
                 polygon.col=polygon.cols[1],lines.col=lines.cols[1],firstpolygon=1,x.range=x.range,y.range=y.range,plot.title=plot.title,y.axis.label=y.axis.label)
    

    ## plot.polygon(t=t.opt,
    ##              ylowerpolygon=apply(optimal.data,1,quantile,lq),
    ##              yupperpolygon=apply(optimal.data,1,quantile,uq),
    ##              ymean=rowMedians(optimal.data),
    ##              ylowerdotted=NA,
    ##              yupperdotted=NA,
    ##              polygon.col=polygon.cols[3],lines.col=lines.cols[3],firstpolygon=0,x.range=x.range,y.range=y.range,plot.title=NA,y.axis.label=NA)

    if(plot.legend==1)
    {
        legend("topleft",col=polygon.cols,legend=c("With barriers"),lty=1,lwd=4,bty="n",cex=1.1)
    }
    
    if(!is.na(plot.filename)){
        dev.off()
    }

}



plot.two.scenarios <- function(t,baseline.data,nobarrier.data,lq,uq,x.range,y.range,plot.filename,plot.legend,plot.title,y.axis.label)
{

    if(!is.na(plot.filename)){
        pdf(plot.filename)
    }
    
        
    plot.polygon(t=t,
                 ylowerpolygon=apply(baseline.data,1,quantile,lq),
                 yupperpolygon=apply(baseline.data,1,quantile,uq),
                 ymean=apply(baseline.data,1, median, na.rm = TRUE),
                 ylowerdotted=NA,
                 yupperdotted=NA,
                 polygon.col=polygon.cols[1],lines.col=lines.cols[1],firstpolygon=1,x.range=x.range,y.range=y.range,plot.title=plot.title,y.axis.label=y.axis.label)
    

    plot.polygon(t=t,
                 ylowerpolygon=apply(nobarrier.data,1,quantile,lq),
                 yupperpolygon=apply(nobarrier.data,1,quantile,uq),
                 ymean=apply(baseline.data,1, median, na.rm = TRUE),
                 ylowerdotted=NA,
                 yupperdotted=NA,
                 polygon.col=polygon.cols[2],lines.col=lines.cols[2],firstpolygon=0,x.range=x.range,y.range=y.range,plot.title=NA,y.axis.label=NA)
    
    ## plot.polygon(t=t.opt,
    ##              ylowerpolygon=apply(optimal.data,1,quantile,lq),
    ##              yupperpolygon=apply(optimal.data,1,quantile,uq),
    ##              ymean=rowMedians(optimal.data),
    ##              ylowerdotted=NA,
    ##              yupperdotted=NA,
    ##              polygon.col=polygon.cols[3],lines.col=lines.cols[3],firstpolygon=0,x.range=x.range,y.range=y.range,plot.title=NA,y.axis.label=NA)

    if(plot.legend==1)
    {
        legend("topleft",col=polygon.cols,legend=c("With barriers","No barrier scenario"),lty=1,lwd=4,bty="n",cex=1.1)
    }
    
    if(!is.na(plot.filename)){
        dev.off()
    }

}



# Multipurpose plot function for different barrier scenarios:
plot.four.scenarios <- function(t,baseline.data,scenario2.data,scenario3.data,scenario4.data,lq,uq,x.range,y.range,plot.filename,plot.legend,plot.title,y.axis.label)
{

    if(!is.na(plot.filename)){
        pdf(plot.filename)
    }
    
        
    plot.polygon(t=t,
                 ylowerpolygon=apply(baseline.data,1,quantile,lq),
                 yupperpolygon=apply(baseline.data,1,quantile,uq),
                 ymean=apply(baseline.data,1, median, na.rm = TRUE),
                 ylowerdotted=NA,
                 yupperdotted=NA,
                 polygon.col=polygon.cols[1],lines.col=lines.cols[1],firstpolygon=1,x.range=x.range,y.range=y.range,plot.title=plot.title,y.axis.label=y.axis.label)
    

    plot.polygon(t=t,
                 ylowerpolygon=apply(scenario2.data,1,quantile,lq),
                 yupperpolygon=apply(scenario2.data,1,quantile,uq),
                 ymean=apply(scenario2.data,1, median, na.rm = TRUE),
                 ylowerdotted=NA,
                 yupperdotted=NA,
                 polygon.col=polygon.cols[2],lines.col=lines.cols[2],firstpolygon=0,x.range=x.range,y.range=y.range,plot.title=NA,y.axis.label=NA)


    plot.polygon(t=t,
                 ylowerpolygon=apply(scenario3.data,1,quantile,lq),
                 yupperpolygon=apply(scenario3.data,1,quantile,uq),
                 ymean=apply(scenario3.data,1, median, na.rm = TRUE),
                 ylowerdotted=NA,
                 yupperdotted=NA,
                 polygon.col=polygon.cols[3],lines.col=lines.cols[3],firstpolygon=0,x.range=x.range,y.range=y.range,plot.title=NA,y.axis.label=NA)
    
    plot.polygon(t=t,
                 ylowerpolygon=apply(scenario4.data,1,quantile,lq),
                 yupperpolygon=apply(scenario4.data,1,quantile,uq),
                 ymean=apply(scenario4.data,1, median, na.rm = TRUE),
                 ylowerdotted=NA,
                 yupperdotted=NA,
                 polygon.col=polygon.cols[4],lines.col=lines.cols[4],firstpolygon=0,x.range=x.range,y.range=y.range,plot.title=NA,y.axis.label=NA)
    

    if(plot.legend==1)
    {
        legend("topleft",col=polygon.cols,legend=c("With barriers","No motivation barrier","No access barrier","No effective use barrier"),lty=1,lwd=4,bty="n",cex=1.1)
    }
    
    if(!is.na(plot.filename)){
        dev.off()
    }

}





##################################################

# Number of fitted runs used:
n.runs <- 10


# last 0 that this is the baseline cascade scenario:
annualoutput.filenames <- make.annualoutput.filenames(n.runs,"./IMPACT/params/Output",0)

annualoutput.filenames.scenario2 <- make.annualoutput.filenames(n.runs,"./IMPACT/params/Output",3)
annualoutput.filenames.scenario3 <- make.annualoutput.filenames(n.runs,"./IMPACT/params/Output",2)
annualoutput.filenames.scenario4 <- make.annualoutput.filenames(n.runs,"./IMPACT/params/Output",1)


all.data <- get.data.as.list(annualoutput.filenames)
#data.run1 <- get.annual.output.model.data(annualoutput.filenames[1])
all.data.scenario2 <- get.data.as.list(annualoutput.filenames.scenario2)
all.data.scenario3 <- get.data.as.list(annualoutput.filenames.scenario3)
all.data.scenario4 <- get.data.as.list(annualoutput.filenames.scenario4)







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



#plot.scenarios <- function(t,baseline.data,nobarrier.data,lq,uq,x.range,y.range,plot.filename,plot.legend,plot.title,y.axis.label)



polygon.cols<- c(brewer.pal(n = 11, name = "RdYlBu")[8], brewer.pal(n = 9, name = "Reds")[3], brewer.pal(n = 9, name = "Greens")[3], brewer.pal(n = 11, name = "BrBG")[4], brewer.pal(n = 11, name = "PuOr")[5])
lines.cols<- c(brewer.pal(n = 11, name = "RdYlBu")[10], brewer.pal(n = 9, name = "Reds")[7], brewer.pal(n = 9, name = "Greens")[7], brewer.pal(n = 11, name = "BrBG")[2], brewer.pal(n = 11, name = "PuOr")[7])


# These are the CIs we use for the shaded plot regions:
lq <- 0.1
uq <- 0.9

t.range <- c(2020,2030)

#plot.scenarios(all.data$t,100*all.data$prevalence.store, all.data$prevalence.store,lq,uq,t.range,c(0.02,40),plot.filename="prevalence.pdf",plot.legend=1,plot.title="Overall prevalence","Prevalence (%)")






plot.four.scenarios(all.data$t,100*all.data$prevalence.store, 100*all.data.scenario2$prevalence.store, 100*all.data.scenario3$prevalence.store, 100*all.data.scenario4$prevalence.store,lq,uq,t.range,c(0,20),plot.filename=NA,plot.legend=1,plot.title="Overall prevalence","Prevalence (%)")



plot.one.scenario(all.data$t,100*all.data$incidence.store,lq,uq,c(2000,2040),c(0,3),plot.filename="incidence_trends_withbarriers.pdf",plot.legend=0,plot.title="Overall incidence (with barriers)","Incidence (%)")

plot.one.scenario(all.data$t,100*all.data$prevalence.store,lq,uq,c(2000,2040),c(0,20),plot.filename="prevalence_trends_withbarriers.pdf",plot.legend=0,plot.title="Overall prevalence (with barriers)","Prevalence (%)")


plot.four.scenarios(all.data$t,100*all.data$incidence.store, 100*all.data.scenario2$incidence.store, 100*all.data.scenario3$incidence.store, 100*all.data.scenario4$incidence.store,lq,uq,t.range,c(0,1.5),plot.filename="incidence_trends_scenarioplot.pdf",plot.legend=1,plot.title="Overall incidence","Incidence (%)")

plot.four.scenarios(all.data$t,100*all.data$prevalence.store, 100*all.data.scenario2$prevalence.store, 100*all.data.scenario3$prevalence.store, 100*all.data.scenario4$prevalence.store,lq,uq,t.range,c(0,20),plot.filename="prevalence_trends_scenarioplot.pdf",plot.legend=1,plot.title="Overall prevalence","Prevalence (%)")



