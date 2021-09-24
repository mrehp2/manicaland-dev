rm(list=ls())

library(RColorBrewer)
library(colorspace) # has darken() function for colours.

# Keep an eye on whether 
# outputs$Npeople_AlwaysCondLT_M.30.y
# or
# outputs$Npeople_AlwaysCondLT_M30..y.
# is the condom use for people aged <30.


# Contains functions to check that the data files are consistent
source("HIV_prevention_cascade_plots_validation.R")


# Run data checks on a run (I pick run 2 randomly - can use others):
# Arguments are: run number, intervention.prep, intervention.VMMC, intervention.cond
data.checks(2,1,1,1)

load.plot.data <- function(resultsdir,run,intervention.prep,intervention.VMMC,intervention.cond)
{
    if(intervention.prep==0 & intervention.VMMC==0 & intervention.cond==0)
    {
        tail.string <- ""
    }else
    {
        tail.string <- paste0("PrEP",as.character(intervention.prep),"_VMMC",as.character(intervention.VMMC),"_cond",as.character(intervention.cond))
    }
    
    data <- read.csv(paste0(resultsdir,"HIVpreventioncascade_CL05_Zim_patch0_Rand1_Run",as.character(run),"_0",tail.string,".csv"),header=T,sep=",")
    return(data)
}







get.data.as.list <- function(resultsdir,nruns, intervention.prep,intervention.VMMC,intervention.cond)
{
    TOLERANCE <- 1e-10 # Constant to avoid dividing by zero NAN
    
    # Add trailing "/" to resultsdir if needed:
    if(!substr(resultsdir,nchar(resultsdir),nchar(resultsdir))=="/"){resultsdir<-paste0(resultsdir,"/")}
    
    for (i in seq(1,nruns))
    {
    
        outputs = load.plot.data(resultsdir,i,intervention.prep,intervention.VMMC,intervention.cond)



        # PrEP outputs (only 15-54 eligible):
        PrEP.M.15.29.denom <- outputs$PrEP_M15.29.NoPrEP. + outputs$PrEP_M15.29.OnPrEPSemi. + outputs$PrEP_M15.29.WaitPrEP. + outputs$PrEP_M15.29.OnPrEPAdh.
        prop.PrEP.M.15.29 <- (outputs$PrEP_M15.29.OnPrEPAdh.+ outputs$PrEP_M15.29.OnPrEPSemi.)/pmax(PrEP.M.15.29.denom,TOLERANCE)
        prop.adhere.PrEP.M.15.29 <- (outputs$PrEP_M15.29.OnPrEPAdh.+TOLERANCE)/(outputs$PrEP_M15.29.OnPrEPAdh.+ outputs$PrEP_M15.29.OnPrEPSemi.+TOLERANCE)

        PrEP.M.30.54.denom <- outputs$PrEP_M30.54.NoPrEP. + outputs$PrEP_M30.54.OnPrEPSemi. + outputs$PrEP_M30.54.WaitPrEP. + outputs$PrEP_M30.54.OnPrEPAdh.
        prop.PrEP.M.30.54 <- (outputs$PrEP_M30.54.OnPrEPAdh.+ outputs$PrEP_M30.54.OnPrEPSemi.)/pmax(PrEP.M.30.54.denom,TOLERANCE)
        prop.adhere.PrEP.M.30.54 <- (outputs$PrEP_M30.54.OnPrEPAdh.+TOLERANCE)/(outputs$PrEP_M30.54.OnPrEPAdh.+ outputs$PrEP_M30.54.OnPrEPSemi.+TOLERANCE)

        PrEP.F.15.24.denom <- outputs$PrEP_F15.24.NoPrEP. + outputs$PrEP_F15.24.OnPrEPSemi. + outputs$PrEP_F15.24.WaitPrEP. + outputs$PrEP_F15.24.OnPrEPAdh.
        prop.PrEP.F.15.24 <- (outputs$PrEP_F15.24.OnPrEPAdh.+ outputs$PrEP_F15.24.OnPrEPSemi.)/pmax(PrEP.F.15.24.denom,TOLERANCE)
        prop.adhere.PrEP.F.15.24 <- (outputs$PrEP_F15.24.OnPrEPAdh.+TOLERANCE)/(outputs$PrEP_F15.24.OnPrEPAdh.+ outputs$PrEP_F15.24.OnPrEPSemi.+TOLERANCE)

        PrEP.F.25.54.denom <- outputs$PrEP_F25.54.NoPrEP. + outputs$PrEP_F25.54.OnPrEPSemi. + outputs$PrEP_F25.54.WaitPrEP. + outputs$PrEP_F25.54.OnPrEPAdh.
        prop.PrEP.F.25.54 <- (outputs$PrEP_F25.54.OnPrEPAdh.+ outputs$PrEP_F25.54.OnPrEPSemi.)/pmax(PrEP.F.25.54.denom,TOLERANCE)
        prop.adhere.PrEP.F.25.54 <- (outputs$PrEP_F25.54.OnPrEPAdh.+TOLERANCE)/(outputs$PrEP_F25.54.OnPrEPAdh.+ outputs$PrEP_F25.54.OnPrEPSemi.+TOLERANCE)



        PrEP.M.denom <- outputs$PrEP_M15.29.NoPrEP. + outputs$PrEP_M15.29.OnPrEPSemi. + outputs$PrEP_M15.29.WaitPrEP. + outputs$PrEP_M15.29.OnPrEPAdh. + outputs$PrEP_M30.54.NoPrEP. + outputs$PrEP_M30.54.OnPrEPSemi. + outputs$PrEP_M30.54.WaitPrEP. + outputs$PrEP_M30.54.OnPrEPAdh.
        prop.PrEP.M <- (outputs$PrEP_M15.29.OnPrEPAdh.+ outputs$PrEP_M15.29.OnPrEPSemi. + outputs$PrEP_M30.54.OnPrEPAdh.+ outputs$PrEP_M30.54.OnPrEPSemi.)/pmax(PrEP.M.denom,TOLERANCE)
        prop.adhere.PrEP.M <- (outputs$PrEP_M15.29.OnPrEPAdh.+outputs$PrEP_M30.54.OnPrEPAdh.+TOLERANCE)/(outputs$PrEP_M15.29.OnPrEPAdh.+ outputs$PrEP_M15.29.OnPrEPSemi. + outputs$PrEP_M30.54.OnPrEPAdh.+ outputs$PrEP_M30.54.OnPrEPSemi. + TOLERANCE)


        PrEP.F.denom <- outputs$PrEP_F15.24.NoPrEP. + outputs$PrEP_F15.24.OnPrEPSemi. + outputs$PrEP_F15.24.WaitPrEP. + outputs$PrEP_F15.24.OnPrEPAdh. + outputs$PrEP_F25.54.NoPrEP. + outputs$PrEP_F25.54.OnPrEPSemi. + outputs$PrEP_F25.54.WaitPrEP. + outputs$PrEP_F25.54.OnPrEPAdh.
        prop.PrEP.F <- (outputs$PrEP_F15.24.OnPrEPAdh.+ outputs$PrEP_F15.24.OnPrEPSemi. + outputs$PrEP_F25.54.OnPrEPAdh.+ outputs$PrEP_F25.54.OnPrEPSemi.)/pmax(PrEP.F.denom,TOLERANCE)
        prop.adhere.PrEP.F <- (outputs$PrEP_F15.24.OnPrEPAdh.+outputs$PrEP_F25.54.OnPrEPAdh.+TOLERANCE)/(outputs$PrEP_F15.24.OnPrEPAdh.+ outputs$PrEP_F15.24.OnPrEPSemi. + outputs$PrEP_F25.54.OnPrEPAdh.+ outputs$PrEP_F25.54.OnPrEPSemi. + TOLERANCE)

        prop.PrEP <- (outputs$PrEP_M15.29.OnPrEPAdh.+ outputs$PrEP_M15.29.OnPrEPSemi. + outputs$PrEP_M30.54.OnPrEPAdh.+ outputs$PrEP_M30.54.OnPrEPSemi. + outputs$PrEP_F15.24.OnPrEPAdh.+ outputs$PrEP_F15.24.OnPrEPSemi. + outputs$PrEP_F25.54.OnPrEPAdh.+ outputs$PrEP_F25.54.OnPrEPSemi.)/pmax(PrEP.M.denom + PrEP.F.denom, TOLERANCE)
        prop.adhere.PrEP <- (outputs$PrEP_M15.29.OnPrEPAdh.+outputs$PrEP_M30.54.OnPrEPAdh. + outputs$PrEP_F15.24.OnPrEPAdh.+outputs$PrEP_F25.54.OnPrEPAdh.+TOLERANCE)/(outputs$PrEP_M15.29.OnPrEPAdh.+ outputs$PrEP_M15.29.OnPrEPSemi. + outputs$PrEP_M30.54.OnPrEPAdh.+ outputs$PrEP_M30.54.OnPrEPSemi. + outputs$PrEP_F15.24.OnPrEPAdh.+ outputs$PrEP_F15.24.OnPrEPSemi. + outputs$PrEP_F25.54.OnPrEPAdh.+ outputs$PrEP_F25.54.OnPrEPSemi. + TOLERANCE)

        
        # VMMC outputs:
        VMMC.lt.15.denom <- outputs$VMMC_.15.uncirc. + outputs$VMMC_.15.waitVMMC. + outputs$VMMC_.15.VMMC. + outputs$VMMC_.15.VMMCheal. + outputs$VMMC_.15.TMC.
        prop.VMMC.lt.15 <- outputs$VMMC_.15.VMMC./pmax(VMMC.lt.15.denom,TOLERANCE)
        prop.TMC.lt.15 <- outputs$VMMC_.15.TMC./pmax(VMMC.lt.15.denom,TOLERANCE)
        prop.circ.lt.15 <- (outputs$VMMC_.15.VMMC. + outputs$VMMC_.15.TMC.)/pmax(VMMC.lt.15.denom,TOLERANCE)

        VMMC.15.29.denom <- outputs$VMMC_15.29.uncirc. + outputs$VMMC_15.29.waitVMMC. + outputs$VMMC_15.29.VMMC. + outputs$VMMC_15.29.VMMCheal. + outputs$VMMC_15.29.TMC.
        prop.VMMC.15.29 <- outputs$VMMC_15.29.VMMC./pmax(VMMC.15.29.denom,TOLERANCE)
        prop.TMC.15.29 <- outputs$VMMC_15.29.TMC./pmax(VMMC.15.29.denom,TOLERANCE)
        prop.circ.15.29 <- (outputs$VMMC_15.29.VMMC. + outputs$VMMC_15.29.TMC.)/pmax(VMMC.15.29.denom,TOLERANCE)

        VMMC.30.54.denom <- outputs$VMMC_30.54.uncirc. + outputs$VMMC_30.54.waitVMMC. + outputs$VMMC_30.54.VMMC. + outputs$VMMC_30.54.VMMCheal. + outputs$VMMC_30.54.TMC.
        prop.VMMC.30.54 <- outputs$VMMC_30.54.VMMC./pmax(VMMC.30.54.denom,TOLERANCE)
        prop.TMC.30.54 <- outputs$VMMC_30.54.TMC./pmax(VMMC.30.54.denom,TOLERANCE)
        prop.circ.30.54 <- (outputs$VMMC_30.54.VMMC. + outputs$VMMC_30.54.TMC.)/pmax(VMMC.30.54.denom,TOLERANCE)
       
        VMMC.55.plus.denom <- outputs$VMMC_55..uncirc. + outputs$VMMC_55..waitVMMC. + outputs$VMMC_55..VMMC. + outputs$VMMC_55..VMMCheal. + outputs$VMMC_55..TMC.
        prop.VMMC.55.plus <- outputs$VMMC_55..VMMC./pmax(VMMC.55.plus.denom,TOLERANCE)
        prop.TMC.55.plus <- outputs$VMMC_55..TMC./pmax(VMMC.55.plus.denom,TOLERANCE)
        prop.circ.55.plus <- (outputs$VMMC_55..VMMC. + outputs$VMMC_55..TMC.)/pmax(VMMC.55.plus.denom,TOLERANCE)

        

        VMMC.denom <- VMMC.lt.15.denom + VMMC.15.29.denom + VMMC.30.54.denom + VMMC.55.plus.denom
        prop.VMMC <- (outputs$VMMC_.15.VMMC. + outputs$VMMC_15.29.VMMC. + outputs$VMMC_30.54.VMMC. + outputs$VMMC_55..VMMC.)/pmax(VMMC.denom,TOLERANCE)
        prop.TMC <- (outputs$VMMC_.15.TMC. + outputs$VMMC_15.29.TMC. + outputs$VMMC_30.54.TMC. + outputs$VMMC_55..TMC.)/pmax(VMMC.denom,TOLERANCE)
        prop.circ <- (outputs$VMMC_.15.VMMC. + outputs$VMMC_15.29.VMMC. + outputs$VMMC_30.54.VMMC. + outputs$VMMC_55..VMMC. + outputs$VMMC_.15.TMC. + outputs$VMMC_15.29.TMC. + outputs$VMMC_30.54.TMC. + outputs$VMMC_55..TMC.)/pmax(VMMC.denom,TOLERANCE)

        

        prop.always.cond.LT.M.lt30 <- outputs$Npeople_AlwaysCondLT_M.30.y. / pmax(outputs$Npeople_AlwaysCondLT_M.30.n. + outputs$Npeople_AlwaysCondLT_M.30.y. , TOLERANCE)
        prop.always.cond.LT.M.30plus <- outputs$Npeople_AlwaysCondLT_M30..y. / pmax(outputs$Npeople_AlwaysCondLT_M30..n. + outputs$Npeople_AlwaysCondLT_M30..y. , TOLERANCE)

        prop.always.cond.LT.F.lt25 <- outputs$Npeople_AlwaysCondLT_F.25.y. / pmax(outputs$Npeople_AlwaysCondLT_F.25.n. + outputs$Npeople_AlwaysCondLT_F.25.y. , TOLERANCE)
        prop.always.cond.LT.F.25plus <- outputs$Npeople_AlwaysCondLT_F25..y. / pmax(outputs$Npeople_AlwaysCondLT_F25..n. + outputs$Npeople_AlwaysCondLT_F25..y. , TOLERANCE)


        prop.always.cond.LT.M <- (outputs$Npeople_AlwaysCondLT_M.30.y.+outputs$Npeople_AlwaysCondLT_M30..y.) / pmax(outputs$Npeople_AlwaysCondLT_M.30.n. + outputs$Npeople_AlwaysCondLT_M.30.y. + outputs$Npeople_AlwaysCondLT_M30..n. + outputs$Npeople_AlwaysCondLT_M30..y. , TOLERANCE)
        prop.always.cond.LT.F <- (outputs$Npeople_AlwaysCondLT_F.25.y. + outputs$Npeople_AlwaysCondLT_F25..y.) / pmax(outputs$Npeople_AlwaysCondLT_F.25.n. + outputs$Npeople_AlwaysCondLT_F.25.y. + outputs$Npeople_AlwaysCondLT_F25..n. + outputs$Npeople_AlwaysCondLT_F25..y., TOLERANCE)        
        prop.always.cond.LT <- (outputs$Npeople_AlwaysCondLT_M.30.y.+outputs$Npeople_AlwaysCondLT_M30..y. + outputs$Npeople_AlwaysCondLT_F.25.y. + outputs$Npeople_AlwaysCondLT_F25..y.) / pmax(outputs$Npeople_AlwaysCondLT_M.30.n. + outputs$Npeople_AlwaysCondLT_M.30.y. + outputs$Npeople_AlwaysCondLT_M30..n. + outputs$Npeople_AlwaysCondLT_M30..y. + outputs$Npeople_AlwaysCondLT_F.25.n. + outputs$Npeople_AlwaysCondLT_F.25.y. + outputs$Npeople_AlwaysCondLT_F25..n. + outputs$Npeople_AlwaysCondLT_F25..y., TOLERANCE)
        
        prop.always.cond.Casual.M.lt30 <- outputs$Npeople_AlwaysCondCasual_M.30.y. / pmax(outputs$Npeople_AlwaysCondCasual_M.30.n. + outputs$Npeople_AlwaysCondCasual_M.30.y. , TOLERANCE)
        prop.always.cond.Casual.M.30plus <- outputs$Npeople_AlwaysCondCasual_M30..y. / pmax(outputs$Npeople_AlwaysCondCasual_M30..n. + outputs$Npeople_AlwaysCondCasual_M30..y. , TOLERANCE)

        prop.always.cond.Casual.F.lt25 <- outputs$Npeople_AlwaysCondCasual_F.25.y. / pmax(outputs$Npeople_AlwaysCondCasual_F.25.n. + outputs$Npeople_AlwaysCondCasual_F.25.y. , TOLERANCE)
        prop.always.cond.Casual.F.25plus <- outputs$Npeople_AlwaysCondCasual_F25..y. / pmax(outputs$Npeople_AlwaysCondCasual_F25..n. + outputs$Npeople_AlwaysCondCasual_F25..y. , TOLERANCE)

        prop.always.cond.Casual.M <- (outputs$Npeople_AlwaysCondCasual_M.30.y.+outputs$Npeople_AlwaysCondCasual_M30..y.) / pmax(outputs$Npeople_AlwaysCondCasual_M.30.n. + outputs$Npeople_AlwaysCondCasual_M.30.y. + outputs$Npeople_AlwaysCondCasual_M30..n. + outputs$Npeople_AlwaysCondCasual_M30..y. , TOLERANCE)
        prop.always.cond.Casual.F <- (outputs$Npeople_AlwaysCondCasual_F.25.y. + outputs$Npeople_AlwaysCondCasual_F25..y.) / pmax(outputs$Npeople_AlwaysCondCasual_F.25.n. + outputs$Npeople_AlwaysCondCasual_F.25.y. + outputs$Npeople_AlwaysCondCasual_F25..n. + outputs$Npeople_AlwaysCondCasual_F25..y., TOLERANCE)        
        prop.always.cond.Casual <- (outputs$Npeople_AlwaysCondCasual_M.30.y.+outputs$Npeople_AlwaysCondCasual_M30..y. + outputs$Npeople_AlwaysCondCasual_F.25.y. + outputs$Npeople_AlwaysCondCasual_F25..y.) / pmax(outputs$Npeople_AlwaysCondCasual_M.30.n. + outputs$Npeople_AlwaysCondCasual_M.30.y. + outputs$Npeople_AlwaysCondCasual_M30..n. + outputs$Npeople_AlwaysCondCasual_M30..y. + outputs$Npeople_AlwaysCondCasual_F.25.n. + outputs$Npeople_AlwaysCondCasual_F.25.y. + outputs$Npeople_AlwaysCondCasual_F25..n. + outputs$Npeople_AlwaysCondCasual_F25..y., TOLERANCE)



        prop.partnerships.use.cond.LT.M.lt30 <- outputs$N_CondLT_M.30.y./pmax(outputs$N_CondLT_M.30.y. + outputs$N_CondLT_M.30.n., TOLERANCE)
        prop.partnerships.use.cond.LT.M.30plus <- outputs$N_CondLT_M30..y./pmax(outputs$N_CondLT_M30..y. + outputs$N_CondLT_M30..n., TOLERANCE)

        prop.partnerships.use.cond.LT.F.lt25 <- outputs$N_CondLT_F.25.y./pmax(outputs$N_CondLT_F.25.y. + outputs$N_CondLT_F.25.n., TOLERANCE)
        prop.partnerships.use.cond.LT.F.25plus <- outputs$N_CondLT_F25..y./pmax(outputs$N_CondLT_F25..y. + outputs$N_CondLT_F25..n., TOLERANCE)
        
        prop.partnerships.use.cond.LT.M <- (outputs$N_CondLT_M.30.y. + outputs$N_CondLT_M30..y.)/pmax(outputs$N_CondLT_M.30.y. + outputs$N_CondLT_M.30.n. + outputs$N_CondLT_M30..y. + outputs$N_CondLT_M30..n., TOLERANCE)

        prop.partnerships.use.cond.LT.F <- (outputs$N_CondLT_F.25.y. + outputs$N_CondLT_F25..y.)/pmax(outputs$N_CondLT_F.25.y. + outputs$N_CondLT_F.25.n. + outputs$N_CondLT_F25..y. + outputs$N_CondLT_F25..n., TOLERANCE)

        prop.partnerships.use.cond.LT <- (outputs$N_CondLT_M.30.y. + outputs$N_CondLT_M30..y. + outputs$N_CondLT_F.25.y. + outputs$N_CondLT_F25..y.)/pmax(outputs$N_CondLT_F.25.y. + outputs$N_CondLT_F.25.n. + outputs$N_CondLT_F25..y. + outputs$N_CondLT_F25..n. + outputs$N_CondLT_M.30.y. + outputs$N_CondLT_M.30.n. + outputs$N_CondLT_M30..y. + outputs$N_CondLT_M30..n., TOLERANCE)

        
        ##

        prop.partnerships.use.cond.Casual.M.lt30 <- outputs$N_CondCasual_M.30.y./pmax(outputs$N_CondCasual_M.30.y. + outputs$N_CondCasual_M.30.n., TOLERANCE)
        prop.partnerships.use.cond.Casual.M.30plus <- outputs$N_CondCasual_M30..y./pmax(outputs$N_CondCasual_M30..y. + outputs$N_CondCasual_M30..n., TOLERANCE)

        prop.partnerships.use.cond.Casual.F.lt25 <- outputs$N_CondCasual_F.25.y./pmax(outputs$N_CondCasual_F.25.y. + outputs$N_CondCasual_F.25.n., TOLERANCE)
        prop.partnerships.use.cond.Casual.F.25plus <- outputs$N_CondCasual_F25..y./pmax(outputs$N_CondCasual_F25..y. + outputs$N_CondCasual_F25..n., TOLERANCE)
        
        prop.partnerships.use.cond.Casual.M <- (outputs$N_CondCasual_M.30.y. + outputs$N_CondCasual_M30..y.)/pmax(outputs$N_CondCasual_M.30.y. + outputs$N_CondCasual_M.30.n. + outputs$N_CondCasual_M30..y. + outputs$N_CondCasual_M30..n., TOLERANCE)

        prop.partnerships.use.cond.Casual.F <- (outputs$N_CondCasual_F.25.y. + outputs$N_CondCasual_F25..y.)/pmax(outputs$N_CondCasual_F.25.y. + outputs$N_CondCasual_F.25.n. + outputs$N_CondCasual_F25..y. + outputs$N_CondCasual_F25..n., TOLERANCE)

        prop.partnerships.use.cond.Casual <- (outputs$N_CondCasual_M.30.y. + outputs$N_CondCasual_M30..y. + outputs$N_CondCasual_F.25.y. + outputs$N_CondCasual_F25..y.)/pmax(outputs$N_CondCasual_F.25.y. + outputs$N_CondCasual_F.25.n. + outputs$N_CondCasual_F25..y. + outputs$N_CondCasual_F25..n. + outputs$N_CondCasual_M.30.y. + outputs$N_CondCasual_M.30.n. + outputs$N_CondCasual_M30..y. + outputs$N_CondCasual_M30..n., TOLERANCE)


        
        if(i==1){
            t = outputs$Time

            prop.PrEP.M.15.29.store <- prop.PrEP.M.15.29
            prop.adhere.PrEP.M.15.29.store <- prop.adhere.PrEP.M.15.29
            prop.PrEP.M.30.54.store <- prop.PrEP.M.30.54
            prop.adhere.PrEP.M.30.54.store <- prop.adhere.PrEP.M.30.54
            prop.PrEP.F.15.24.store <- prop.PrEP.F.15.24
            prop.adhere.PrEP.F.15.24.store <- prop.adhere.PrEP.F.15.24
            prop.PrEP.F.25.54.store <- prop.PrEP.F.25.54
            prop.adhere.PrEP.F.25.54.store <- prop.adhere.PrEP.F.25.54
            prop.PrEP.M.store <- prop.PrEP.M
            prop.adhere.PrEP.M.store <- prop.adhere.PrEP.M
            prop.PrEP.F.store <- prop.PrEP.F
            prop.adhere.PrEP.F.store <- prop.adhere.PrEP.F
            prop.PrEP.store <- prop.PrEP
            prop.adhere.PrEP.store <- prop.adhere.PrEP
            

            
            prop.VMMC.lt.15.store <- prop.VMMC.lt.15
            prop.TMC.lt.15.store <- prop.TMC.lt.15
            prop.circ.lt.15.store <- prop.circ.lt.15
            prop.VMMC.15.29.store <- prop.VMMC.15.29
            prop.TMC.15.29.store <- prop.TMC.15.29
            prop.circ.15.29.store <- prop.circ.15.29
            prop.VMMC.30.54.store <- prop.VMMC.30.54
            prop.TMC.30.54.store <- prop.TMC.30.54
            prop.circ.30.54.store <- prop.circ.30.54
            prop.VMMC.55.plus.store <- prop.VMMC.55.plus
            prop.TMC.55.plus.store <- prop.TMC.55.plus
            prop.circ.55.plus.store <- prop.circ.55.plus


            prop.VMMC.store <- prop.VMMC
            prop.TMC.store <- prop.TMC
            prop.circ.store <- prop.circ



            prop.always.cond.LT.M.lt30.store <- prop.always.cond.LT.M.lt30
            prop.always.cond.LT.M.30plus.store <- prop.always.cond.LT.M.30plus

            prop.always.cond.LT.F.lt25.store <- prop.always.cond.LT.F.lt25
            prop.always.cond.LT.F.25plus.store <- prop.always.cond.LT.F.25plus

            prop.always.cond.LT.M.store <- prop.always.cond.LT.M
            prop.always.cond.LT.F.store <- prop.always.cond.LT.F
            prop.always.cond.LT.store <- prop.always.cond.LT
        
            prop.always.cond.Casual.M.lt30.store <- prop.always.cond.Casual.M.lt30
            prop.always.cond.Casual.M.30plus.store <- prop.always.cond.Casual.M.30plus
            prop.always.cond.Casual.F.lt25.store <- prop.always.cond.Casual.F.lt25
            prop.always.cond.Casual.F.25plus.store <- prop.always.cond.Casual.F.25plus

            prop.always.cond.Casual.M.store <- prop.always.cond.Casual.M
            prop.always.cond.Casual.F.store <- prop.always.cond.Casual.F
            prop.always.cond.Casual.store <- prop.always.cond.Casual
        


###
            prop.partnerships.use.cond.LT.M.lt30.store <- prop.partnerships.use.cond.LT.M.lt30
            prop.partnerships.use.cond.LT.M.30plus.store <- prop.partnerships.use.cond.LT.M.30plus

            prop.partnerships.use.cond.LT.F.lt25.store <- prop.partnerships.use.cond.LT.F.lt25
            prop.partnerships.use.cond.LT.F.25plus.store <- prop.partnerships.use.cond.LT.F.25plus

            prop.partnerships.use.cond.LT.M.store <- prop.partnerships.use.cond.LT.M
            prop.partnerships.use.cond.LT.F.store <- prop.partnerships.use.cond.LT.F
            prop.partnerships.use.cond.LT.store <- prop.partnerships.use.cond.LT
        
            prop.partnerships.use.cond.Casual.M.lt30.store <- prop.partnerships.use.cond.Casual.M.lt30
            prop.partnerships.use.cond.Casual.M.30plus.store <- prop.partnerships.use.cond.Casual.M.30plus
            prop.partnerships.use.cond.Casual.F.lt25.store <- prop.partnerships.use.cond.Casual.F.lt25
            prop.partnerships.use.cond.Casual.F.25plus.store <- prop.partnerships.use.cond.Casual.F.25plus

            prop.partnerships.use.cond.Casual.M.store <- prop.partnerships.use.cond.Casual.M
            prop.partnerships.use.cond.Casual.F.store <- prop.partnerships.use.cond.Casual.F
            prop.partnerships.use.cond.Casual.store <- prop.partnerships.use.cond.Casual

            
        }else{


            prop.PrEP.M.15.29.store <- cbind(prop.PrEP.M.15.29.store,prop.PrEP.M.15.29)
            prop.adhere.PrEP.M.15.29.store <- cbind(prop.adhere.PrEP.M.15.29.store,prop.adhere.PrEP.M.15.29)
            prop.PrEP.M.30.54.store <- cbind(prop.PrEP.M.30.54.store,prop.PrEP.M.30.54)
            prop.adhere.PrEP.M.30.54.store <- cbind(prop.adhere.PrEP.M.30.54.store,prop.adhere.PrEP.M.30.54)
            prop.PrEP.F.15.24.store <- cbind(prop.PrEP.F.15.24.store,prop.PrEP.F.15.24)
            prop.adhere.PrEP.F.15.24.store <- cbind(prop.adhere.PrEP.F.15.24.store,prop.adhere.PrEP.F.15.24)
            prop.PrEP.F.25.54.store <- cbind(prop.PrEP.F.25.54.store,prop.PrEP.F.25.54)
            prop.adhere.PrEP.F.25.54.store <- cbind(prop.adhere.PrEP.F.25.54.store,prop.adhere.PrEP.F.25.54)
            prop.PrEP.M.store <- cbind(prop.PrEP.M.store,prop.PrEP.M)
            prop.adhere.PrEP.M.store <- cbind(prop.adhere.PrEP.M.store,prop.adhere.PrEP.M)
            prop.PrEP.F.store <- cbind(prop.PrEP.F.store,prop.PrEP.F)
            prop.adhere.PrEP.F.store <- cbind(prop.adhere.PrEP.F.store,prop.adhere.PrEP.F)
            prop.PrEP.store <- cbind(prop.PrEP.store,prop.PrEP)
            prop.adhere.PrEP.store <- cbind(prop.adhere.PrEP.store,prop.adhere.PrEP)


            
            prop.VMMC.lt.15.store <- cbind(prop.VMMC.lt.15.store,prop.VMMC.lt.15)
            prop.TMC.lt.15.store <- cbind(prop.TMC.lt.15.store,prop.TMC.lt.15)
            prop.circ.lt.15.store <- cbind(prop.circ.lt.15.store,prop.circ.lt.15)
            prop.VMMC.15.29.store <- cbind(prop.VMMC.15.29.store,prop.VMMC.15.29)
            prop.TMC.15.29.store <- cbind(prop.TMC.15.29.store,prop.TMC.15.29)
            prop.circ.15.29.store <- cbind(prop.circ.15.29.store,prop.circ.15.29)
            prop.VMMC.30.54.store <- cbind(prop.VMMC.30.54.store,prop.VMMC.30.54)
            prop.TMC.30.54.store <- cbind(prop.TMC.30.54.store,prop.TMC.30.54)
            prop.circ.30.54.store <- cbind(prop.circ.30.54.store,prop.circ.30.54)
            prop.VMMC.55.plus.store <- cbind(prop.VMMC.55.plus.store,prop.VMMC.55.plus)
            prop.TMC.55.plus.store <- cbind(prop.TMC.55.plus.store,prop.TMC.55.plus)
            prop.circ.55.plus.store <- cbind(prop.circ.55.plus.store,prop.circ.55.plus)

            prop.VMMC.store <- cbind(prop.VMMC.store,prop.VMMC)
            prop.TMC.store <- cbind(prop.TMC.store,prop.TMC)
            prop.circ.store <- cbind(prop.circ.store,prop.circ)



            prop.always.cond.LT.M.lt30.store <- cbind(prop.always.cond.LT.M.lt30.store,prop.always.cond.LT.M.lt30)
            prop.always.cond.LT.M.30plus.store <- cbind(prop.always.cond.LT.M.30plus.store,prop.always.cond.LT.M.30plus)

            prop.always.cond.LT.F.lt25.store <- cbind(prop.always.cond.LT.F.lt25.store,prop.always.cond.LT.F.lt25)
            prop.always.cond.LT.F.25plus.store <- cbind(prop.always.cond.LT.F.25plus.store,prop.always.cond.LT.F.25plus)

            prop.always.cond.LT.M.store <- cbind(prop.always.cond.LT.M.store,prop.always.cond.LT.M)
            prop.always.cond.LT.F.store <- cbind(prop.always.cond.LT.F.store,prop.always.cond.LT.F)
            prop.always.cond.LT.store <- cbind(prop.always.cond.LT.store,prop.always.cond.LT)
        
            prop.always.cond.Casual.M.lt30.store <- cbind(prop.always.cond.Casual.M.lt30.store,prop.always.cond.Casual.M.lt30)
            prop.always.cond.Casual.M.30plus.store <- cbind(prop.always.cond.Casual.M.30plus.store,prop.always.cond.Casual.M.30plus)
            prop.always.cond.Casual.F.lt25.store <- cbind(prop.always.cond.Casual.F.lt25.store,prop.always.cond.Casual.F.lt25)
            prop.always.cond.Casual.F.25plus.store <- cbind(prop.always.cond.Casual.F.25plus.store,prop.always.cond.Casual.F.25plus)

            prop.always.cond.Casual.M.store <- cbind(prop.always.cond.Casual.M.store,prop.always.cond.Casual.M)
            prop.always.cond.Casual.F.store <- cbind(prop.always.cond.Casual.F.store,prop.always.cond.Casual.F)
            prop.always.cond.Casual.store <- cbind(prop.always.cond.Casual.store,prop.always.cond.Casual)


                                        # Now % of partnerships where condom is used:
            prop.partnerships.use.cond.LT.M.lt30.store <- cbind(prop.partnerships.use.cond.LT.M.lt30.store,prop.partnerships.use.cond.LT.M.lt30)
            prop.partnerships.use.cond.LT.M.30plus.store <- cbind(prop.partnerships.use.cond.LT.M.30plus.store,prop.partnerships.use.cond.LT.M.30plus)

            prop.partnerships.use.cond.LT.F.lt25.store <- cbind(prop.partnerships.use.cond.LT.F.lt25.store,prop.partnerships.use.cond.LT.F.lt25)
            prop.partnerships.use.cond.LT.F.25plus.store <- cbind(prop.partnerships.use.cond.LT.F.25plus.store,prop.partnerships.use.cond.LT.F.25plus)

            prop.partnerships.use.cond.LT.M.store <- cbind(prop.partnerships.use.cond.LT.M.store,prop.partnerships.use.cond.LT.M)
            prop.partnerships.use.cond.LT.F.store <- cbind(prop.partnerships.use.cond.LT.F.store,prop.partnerships.use.cond.LT.F)
            prop.partnerships.use.cond.LT.store <- cbind(prop.partnerships.use.cond.LT.store,prop.partnerships.use.cond.LT)
        
            prop.partnerships.use.cond.Casual.M.lt30.store <- cbind(prop.partnerships.use.cond.Casual.M.lt30.store,prop.partnerships.use.cond.Casual.M.lt30)
            prop.partnerships.use.cond.Casual.M.30plus.store <- cbind(prop.partnerships.use.cond.Casual.M.30plus.store,prop.partnerships.use.cond.Casual.M.30plus)
            prop.partnerships.use.cond.Casual.F.lt25.store <- cbind(prop.partnerships.use.cond.Casual.F.lt25.store,prop.partnerships.use.cond.Casual.F.lt25)
            prop.partnerships.use.cond.Casual.F.25plus.store <- cbind(prop.partnerships.use.cond.Casual.F.25plus.store,prop.partnerships.use.cond.Casual.F.25plus)

            prop.partnerships.use.cond.Casual.M.store <- cbind(prop.partnerships.use.cond.Casual.M.store,prop.partnerships.use.cond.Casual.M)
            prop.partnerships.use.cond.Casual.F.store <- cbind(prop.partnerships.use.cond.Casual.F.store,prop.partnerships.use.cond.Casual.F)
            prop.partnerships.use.cond.Casual.store <- cbind(prop.partnerships.use.cond.Casual.store,prop.partnerships.use.cond.Casual)
            
        }
            
    }

    # This is a list of lists:
    data.store <- list(t=t,
                       prop.PrEP.M.15.29.store=prop.PrEP.M.15.29.store,
                       prop.adhere.PrEP.M.15.29.store=prop.adhere.PrEP.M.15.29.store,
                       prop.PrEP.M.30.54.store=prop.PrEP.M.30.54.store,
                       prop.adhere.PrEP.M.30.54.store=prop.adhere.PrEP.M.30.54.store,
                       prop.PrEP.F.15.24.store=prop.PrEP.F.15.24.store,
                       prop.adhere.PrEP.F.15.24.store=prop.adhere.PrEP.F.15.24.store,
                       prop.PrEP.F.25.54.store=prop.PrEP.F.25.54.store,
                       prop.adhere.PrEP.F.25.54.store=prop.adhere.PrEP.F.25.54.store,
                       prop.PrEP.M.store=prop.PrEP.M.store,
                       prop.adhere.PrEP.M.store=prop.adhere.PrEP.M.store,
                       prop.PrEP.F.store=prop.PrEP.F.store,
                       prop.adhere.PrEP.F.store=prop.adhere.PrEP.F.store,
                       prop.PrEP.store=prop.PrEP.store,
                       prop.adhere.PrEP.store=prop.adhere.PrEP.store,



                       prop.VMMC.lt.15.store=prop.VMMC.lt.15.store,
                       prop.TMC.lt.15.store=prop.TMC.lt.15.store,
                       prop.circ.lt.15.store=prop.circ.lt.15.store,
                       prop.VMMC.15.29.store=prop.VMMC.15.29.store,
                       prop.TMC.15.29.store=prop.TMC.15.29.store,
                       prop.circ.15.29.store=prop.circ.15.29.store,
                       prop.VMMC.30.54.store=prop.VMMC.30.54.store,
                       prop.TMC.30.54.store=prop.TMC.30.54.store,
                       prop.circ.30.54.store=prop.circ.30.54.store,
                       prop.VMMC.55.plus.store=prop.VMMC.55.plus.store,
                       prop.TMC.55.plus.store=prop.TMC.55.plus.store,
                       prop.circ.55.plus.store=prop.circ.55.plus.store,

                       prop.VMMC.store=prop.VMMC.store,
                       prop.TMC.store=prop.TMC.store,
                       prop.circ.store=prop.circ.store,

                       
                       prop.always.cond.LT.M.lt30.store=prop.always.cond.LT.M.lt30.store,
                       prop.always.cond.LT.M.30plus.store=prop.always.cond.LT.M.30plus.store,
                       prop.always.cond.LT.F.lt25.store=prop.always.cond.LT.F.lt25.store,
                       prop.always.cond.LT.F.25plus.store=prop.always.cond.LT.F.25plus.store,
                       prop.always.cond.LT.M.store=prop.always.cond.LT.M.store,
                       prop.always.cond.LT.F.store=prop.always.cond.LT.F.store,
                       prop.always.cond.LT.store=prop.always.cond.LT.store,
        
                       prop.always.cond.Casual.M.lt30.store=prop.always.cond.Casual.M.lt30.store,
                       prop.always.cond.Casual.M.30plus.store=prop.always.cond.Casual.M.30plus.store,
                       prop.always.cond.Casual.F.lt25.store=prop.always.cond.Casual.F.lt25.store,
                       prop.always.cond.Casual.F.25plus.store=prop.always.cond.Casual.F.25plus.store,
                       prop.always.cond.Casual.M.store=prop.always.cond.Casual.M.store,
                       prop.always.cond.Casual.F.store=prop.always.cond.Casual.F.store,
                       prop.always.cond.Casual.store=prop.always.cond.Casual.store,

                       prop.partnerships.use.cond.LT.M.lt30.store=prop.partnerships.use.cond.LT.M.lt30.store,
                       prop.partnerships.use.cond.LT.M.30plus.store=prop.partnerships.use.cond.LT.M.30plus.store,
                       prop.partnerships.use.cond.LT.F.lt25.store=prop.partnerships.use.cond.LT.F.lt25.store,
                       prop.partnerships.use.cond.LT.F.25plus.store=prop.partnerships.use.cond.LT.F.25plus.store,

                       prop.partnerships.use.cond.LT.M.store=prop.partnerships.use.cond.LT.M.store,
                       prop.partnerships.use.cond.LT.F.store=prop.partnerships.use.cond.LT.F.store,
                       prop.partnerships.use.cond.LT.store=prop.partnerships.use.cond.LT.store,
                       
                       prop.partnerships.use.cond.Casual.M.lt30.store=prop.partnerships.use.cond.Casual.M.lt30.store,
                       prop.partnerships.use.cond.Casual.M.30plus.store=prop.partnerships.use.cond.Casual.M.30plus.store,
                       prop.partnerships.use.cond.Casual.F.lt25.store=prop.partnerships.use.cond.Casual.F.lt25.store,
                       prop.partnerships.use.cond.Casual.F.25plus.store=prop.partnerships.use.cond.Casual.F.25plus.store,

                       prop.partnerships.use.cond.Casual.M.store=prop.partnerships.use.cond.Casual.M.store,
                       prop.partnerships.use.cond.Casual.F.store=prop.partnerships.use.cond.Casual.F.store,
                       prop.partnerships.use.cond.Casual.store=prop.partnerships.use.cond.Casual.store


                       )

    return(data.store)
}




# plot a single polygon (can superimpose on others if firstpolygon==FALSE):
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








single.polygon.plot <- function(t,y.data, polygon.cols, lines.cols, plot.title, y.axis.label, scale.as.percentage=TRUE, x.range, y.range=c(0,100))
{
    if(scale.as.percentage==TRUE){scale.factor<-100}else{scale.factor<-1}
    
    plot.polygon(t=t,
             ylowerpolygon=apply(scale.factor*y.data,1,quantile,lq),
             yupperpolygon=apply(scale.factor*y.data,1,quantile,uq),
             ymean=rowMeans(scale.factor*y.data),
                                        #ylowerdotted=apply(all.data$prop.adhere.PrEP.store,1,quantile,0.025),
             ylowerdotted=NA,
             yupperdotted=NA,
             polygon.col=polygon.cols[1],lines.col=lines.cols[1],firstpolygon=1,x.range=x.range,y.range=y.range,plot.title=plot.title,y.axis.label=y.axis.label)

}



# Plot by age and gender:
four.age.polygon.plot <- function(t,y.data.age1.sex1, y.data.age2.sex1, y.data.age3.sex1, y.data.age4.sex1, y.data.age1.sex2, y.data.age2.sex2, y.data.age3.sex2, y.data.age4.sex2, polygon.cols, lines.cols, plot.title, y.axis.label, scale.as.percentage=TRUE, x.range, y.range=c(0,100))
{
    if(scale.as.percentage==TRUE){scale.factor<-100}else{scale.factor<-1}
    
    plot.polygon(t=t,
             ylowerpolygon=apply(scale.factor*y.data.age1.sex1,1,quantile,lq),
             yupperpolygon=apply(scale.factor*y.data.age1.sex1,1,quantile,uq),
             ymean=rowMeans(scale.factor*y.data.age1.sex1),
                                        #ylowerdotted=apply(all.data$prop.adhere.PrEP.store,1,quantile,0.025),
             ylowerdotted=NA,yupperdotted=NA,
             polygon.col=polygon.cols[1],lines.col=lines.cols[1],firstpolygon=1,x.range=x.range,y.range=y.range,plot.title=plot.title,y.axis.label=y.axis.label)


    if(is.data.frame(y.data.age2.sex1)){
    plot.polygon(t=t,
             ylowerpolygon=apply(scale.factor*y.data.age2.sex1,1,quantile,lq),
             yupperpolygon=apply(scale.factor*y.data.age2.sex1,1,quantile,uq),
             ymean=rowMeans(scale.factor*y.data.age2.sex1),
                                        #ylowerdotted=apply(all.data$prop.adhere.PrEP.store,1,quantile,0.025),
             ylowerdotted=NA,yupperdotted=NA,
             polygon.col=polygon.cols[2],lines.col=lines.cols[2],firstpolygon=0,x.range=x.range,y.range=y.range,plot.title=plot.title,y.axis.label=y.axis.label)
    }
    

    ##
    if(is.data.frame(y.data.age3.sex1)){
    plot.polygon(t=t,
             ylowerpolygon=apply(scale.factor*y.data.age3.sex1,1,quantile,lq),
             yupperpolygon=apply(scale.factor*y.data.age3.sex1,1,quantile,uq),
             ymean=rowMeans(scale.factor*y.data.age3.sex1),
                                        #ylowerdotted=apply(all.data$prop.adhere.PrEP.store,1,quantile,0.025),
             ylowerdotted=NA,yupperdotted=NA,
             polygon.col=polygon.cols[1],lines.col=lines.cols[1],firstpolygon=0,x.range=x.range,y.range=y.range,plot.title=plot.title,y.axis.label=y.axis.label)
    }
    
    if(is.data.frame(y.data.age4.sex1)){
    plot.polygon(t=t,
             ylowerpolygon=apply(scale.factor*y.data.age4.sex1,1,quantile,lq),
             yupperpolygon=apply(scale.factor*y.data.age4.sex1,1,quantile,uq),
             ymean=rowMeans(scale.factor*y.data.age4.sex1),
                                        #ylowerdotted=apply(all.data$prop.adhere.PrEP.store,1,quantile,0.025),
             ylowerdotted=NA,yupperdotted=NA,
             polygon.col=polygon.cols[1],lines.col=lines.cols[1],firstpolygon=0,x.range=x.range,y.range=y.range,plot.title=plot.title,y.axis.label=y.axis.label)
    }
    
    
}





multi.age.sex.polygon.plot <- function(t,y.data.list, polygon.cols, lines.cols, plot.title, y.axis.label, scale.as.percentage=TRUE, x.range, y.range=c(0,100), x.legend, y.legend, plot.legend, legend.title)
{
    if(scale.as.percentage==TRUE){scale.factor<-100}else{scale.factor<-1}
    
    plot.polygon(t=t,
             ylowerpolygon=apply(scale.factor*y.data.list[[1]],1,quantile,lq),
             yupperpolygon=apply(scale.factor*y.data.list[[1]],1,quantile,uq),
             ymean=rowMeans(scale.factor*y.data.list[[1]]),
                                        #ylowerdotted=apply(all.data$prop.adhere.PrEP.store,1,quantile,0.025),
             ylowerdotted=NA,yupperdotted=NA,
             polygon.col=polygon.cols[1],lines.col=lines.cols[1],firstpolygon=1,x.range=x.range,y.range=y.range,plot.title=plot.title,y.axis.label=y.axis.label)


    for(i in seq(2,length(y.data.list))){
        if(!all(is.na(y.data.list[[i]]))){
            plot.polygon(t=t,
                         ylowerpolygon=apply(scale.factor*y.data.list[[i]],1,quantile,lq),
                         yupperpolygon=apply(scale.factor*y.data.list[[i]],1,quantile,uq),
                         ymean=rowMeans(scale.factor*y.data.list[[i]]),
                                        #ylowerdotted=apply(all.data$prop.adhere.PrEP.store,1,quantile,0.025),
                         ylowerdotted=NA,yupperdotted=NA,
                         polygon.col=polygon.cols[i],lines.col=lines.cols[i],firstpolygon=0,x.range=x.range,y.range=y.range,plot.title=plot.title,y.axis.label=y.axis.label)
        }
    }
    legend(x.legend,y.legend,legend=plot.legend,fill=polygon.cols, title=legend.title)
}




# For debugging:
print.last.timepoint.data <- function(data.list){
    i.last <- dim(data.list[[1]])[1]
    for (i in seq(1,length(data.list)))
    {
        print(data.list[[i]][i.last,])
    }
}




################################################################
# Main code:
################################################################


resultsdir <- "../results/RESULTS/Output/"

intervention.prep <- 1
intervention.VMMC <- 1
intervention.cond <- 1


# For testing:
run <- 1
run1.data <- load.plot.data(resultsdir,run,intervention.prep,intervention.VMMC,intervention.cond)

        
all.data <- get.data.as.list(resultsdir,3, intervention.prep,intervention.VMMC,intervention.cond)



############
# For testing:
###############
lq <- 0.1
uq <- 0.9


polygon.cols<- c(brewer.pal(n = 11, name = "RdYlBu")[8], brewer.pal(n = 9, name = "Reds")[3], brewer.pal(n = 9, name = "Greens")[3], brewer.pal(n = 11, name = "BrBG")[4], brewer.pal(n = 11, name = "PuOr")[5])

polygon.cols.male<- brewer.pal(n = 9, name = "Blues")[seq(3,7)]
polygon.cols.female<- brewer.pal(n = 9, name = "Reds")[seq(3,7)]

polygon.cols.mf<- c(polygon.cols.male,polygon.cols.female,"Gray33")



lines.cols<- c(brewer.pal(n = 11, name = "RdYlBu")[10], brewer.pal(n = 9, name = "Reds")[7], brewer.pal(n = 9, name = "Greens")[7], brewer.pal(n = 11, name = "BrBG")[2], brewer.pal(n = 11, name = "PuOr")[7])

#x.range=c(1990,2030)
#y.range=c(0,1)
#y.axis.label="% on PrEP"
#plot.title="A plot"
#single.polygon.plot(all.data$t, all.data$prop.PrEP.store, polygon.cols, lines.cols, plot.title, y.axis.label, scale.as.percentage=TRUE,x.range, y.range=c(0,20))




# Voluntary male medical circumcision:
temp.data.list <- list(all.data$prop.VMMC.lt.15.store, all.data$prop.VMMC.15.29.store, all.data$prop.VMMC.30.54.store, all.data$prop.VMMC.55.plus.store, all.data$prop.VMMC.store)
multi.age.sex.polygon.plot(all.data$t, temp.data.list, polygon.cols, lines.cols, "VMMC coverage by age group", "% of men in age group who have VMMC", scale.as.percentage=TRUE, x.range=c(2000,2030), y.range=c(0,100), x.legend=2001, y.legend=95, plot.legend=c("<15","15-29","30-54","55+","All ages"), legend.title="Age group")


# Traditional male circumcision:
temp.data.list <- list(all.data$prop.TMC.lt.15.store, all.data$prop.TMC.15.29.store, all.data$prop.TMC.30.54.store, all.data$prop.TMC.55.plus.store, all.data$prop.TMC.store)
multi.age.sex.polygon.plot(all.data$t, temp.data.list, polygon.cols, lines.cols, "Traditional circumcision coverage by age group", "% of men in age group who have TMC", scale.as.percentage=TRUE, x.range=c(1990,2030), y.range=c(0,20), x.legend=1995, y.legend=19, plot.legend=c("<15","15-29","30-54","55+","All ages"), legend.title="Age group")


# Any male circumcision:
temp.data.list <- list(all.data$prop.circ.lt.15.store, all.data$prop.circ.15.29.store, all.data$prop.circ.30.54.store, all.data$prop.circ.55.plus.store, all.data$prop.circ.store)
multi.age.sex.polygon.plot(all.data$t, temp.data.list, polygon.cols, lines.cols, "Circumcision by age group", "% of men in age group who are circumcised", scale.as.percentage=TRUE, x.range=c(2000,2030), y.range=c(0,100), x.legend=2001, y.legend=95, plot.legend=c("<15","15-29","30-54","55+","All ages"), legend.title="Age group")



#single.polygon.plot(all.data$t, temp.data.list[[5]], polygon.cols, lines.cols, plot.title, y.axis.label, scale.as.percentage=TRUE,x.range, y.range=c(0,100))


# PrEP:
temp.data.list <- list(all.data$prop.PrEP.M.15.29.store, all.data$prop.PrEP.M.30.54.store, all.data$prop.PrEP.F.15.24.store, all.data$prop.PrEP.F.25.54.store, all.data$prop.PrEP.M.store, all.data$prop.PrEP.F.store, all.data$prop.PrEP.store)

prep.cols <- c(polygon.cols.male[c(2,3)],polygon.cols.female[c(2,3)],polygon.cols.male[5],polygon.cols.female[5],"Black")

multi.age.sex.polygon.plot(all.data$t, temp.data.list, prep.cols, lines.cols=darken(prep.cols, 0.4), "PrEP use by age group", "% who are on PrEP", scale.as.percentage=TRUE, x.range=c(2015,2030), y.range=c(0,40), x.legend=2015.5, y.legend=19.2, plot.legend=c("Male 15-29","Male 30-54","Female 15-24","Female 25-54","Male all ages","Female all ages","All ages"), legend.title="Population")

# PrEP adherence:
temp.data.list <- list(all.data$prop.adhere.PrEP.M.15.29.store, all.data$prop.adhere.PrEP.M.30.54.store, all.data$prop.adhere.PrEP.F.15.24.store, all.data$prop.adhere.PrEP.F.25.54.store, all.data$prop.adhere.PrEP.M.store, all.data$prop.adhere.PrEP.F.store, all.data$prop.adhere.PrEP.store)

multi.age.sex.polygon.plot(all.data$t, temp.data.list, prep.cols, lines.cols=darken(prep.cols, 0.4), "PrEP adherence by age group", "% on PrEP who are adherent", scale.as.percentage=TRUE, x.range=c(2015,2030), y.range=c(0,100), x.legend=2015.5, y.legend=80, plot.legend=c("Male 15-29","Male 30-54","Female 15-24","Female 25-54","Male all ages","Female all ages","All ages"), legend.title="Population")






# Condoms:
cond.cols <- c(polygon.cols.male[c(2,3)],polygon.cols.female[c(2,3)],polygon.cols.male[5],polygon.cols.female[5],"Black")

temp.data.list <- list(all.data$prop.partnerships.use.cond.LT.M.lt30.store, all.data$prop.partnerships.use.cond.LT.M.30plus.store, all.data$prop.partnerships.use.cond.LT.F.lt25.store, all.data$prop.partnerships.use.cond.LT.F.25plus.store, all.data$prop.partnerships.use.cond.LT.M.store, all.data$prop.partnerships.use.cond.LT.F.store, all.data$prop.partnerships.use.cond.LT.store)
multi.age.sex.polygon.plot(all.data$t, temp.data.list, cond.cols, lines.cols=darken(cond.cols, 0.4), "Condom use with long-term partners", "% of partnerships where condom is used", scale.as.percentage=TRUE, x.range=c(1990,2030), y.range=c(0,40), x.legend=1992.5, y.legend=40, plot.legend=c("Male <29","Male 30+","Female <24","Female 25+","Male all ages","Female all ages","All ages"), legend.title="Population")

# Casual condom use:
temp.data.list <- list(all.data$prop.partnerships.use.cond.Casual.M.lt30.store, all.data$prop.partnerships.use.cond.Casual.M.30plus.store, all.data$prop.partnerships.use.cond.Casual.F.lt25.store, all.data$prop.partnerships.use.cond.Casual.F.25plus.store, all.data$prop.partnerships.use.cond.Casual.M.store, all.data$prop.partnerships.use.cond.Casual.F.store, all.data$prop.partnerships.use.cond.Casual.store)
multi.age.sex.polygon.plot(all.data$t, temp.data.list, cond.cols, lines.cols=darken(cond.cols, 0.4), "Condom use with casual partners", "% of partnerships where condom is used", scale.as.percentage=TRUE, x.range=c(1990,2030), y.range=c(0,100), x.legend=1992.5, y.legend=30, plot.legend=c("Male <29","Male 30+","Female <24","Female 25+","Male all ages","Female all ages","All ages"), legend.title="Population")



# Always use with LT partners:
temp.data.list <- list(all.data$prop.always.cond.LT.M.lt30.store, all.data$prop.always.cond.LT.M.30plus.store, all.data$prop.always.cond.LT.F.lt25.store, all.data$prop.always.cond.LT.F.25plus.store, all.data$prop.always.cond.LT.M.store, all.data$prop.always.cond.LT.F.store, all.data$prop.always.cond.LT.store)
multi.age.sex.polygon.plot(all.data$t, temp.data.list, cond.cols, lines.cols=darken(cond.cols, 0.4), "Always use condoms with long-term partners", "% always using condom", scale.as.percentage=TRUE, x.range=c(1990,2030), y.range=c(0,40), x.legend=1992.5, y.legend=30, plot.legend=c("Male <29","Male 30+","Female <24","Female 25+","Male all ages","Female all ages","All ages"), legend.title="Population")

# Always use with Casual partners:
temp.data.list <- list(all.data$prop.always.cond.Casual.M.lt30.store, all.data$prop.always.cond.Casual.M.30plus.store, all.data$prop.always.cond.Casual.F.lt25.store, all.data$prop.always.cond.Casual.F.25plus.store, all.data$prop.always.cond.Casual.M.store, all.data$prop.always.cond.Casual.F.store, all.data$prop.always.cond.Casual.store)
multi.age.sex.polygon.plot(all.data$t, temp.data.list, cond.cols, lines.cols=darken(cond.cols, 0.4), "Always use condoms with casual partners", "% always using condom", scale.as.percentage=TRUE, x.range=c(1990,2030), y.range=c(0,60), x.legend=1992.5, y.legend=30, plot.legend=c("Male <29","Male 30+","Female <24","Female 25+","Male all ages","Female all ages","All ages"), legend.title="Population")

