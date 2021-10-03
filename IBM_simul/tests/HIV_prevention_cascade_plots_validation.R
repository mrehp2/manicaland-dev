


# Function makes sure that the number of people for each cascade output is correct (where possible checking by age group, otherwise checking for consistency against Annual_outputs*.csv).
data.checks <- function(run,intervention.prep,intervention.VMMC,intervention.cond)
{

    if(intervention.prep==0 & intervention.VMMC==0 & intervention.cond==0)
    {
        tail.string <- ""
    }else
    {
            tail.string <- paste0("PrEP",as.character(intervention.prep),"_VMMC",as.character(intervention.VMMC),"_cond",as.character(intervention.cond))
    }

    #resultsdir <- "../data/SAMPLED_PARAMETERS/PARAMS_COMMUNITY5/Output/"
    resultsdir <- "../results/RESULTS/Output/"
    
    data <- read.csv(paste0(resultsdir,"HIVpreventioncascade_CL05_Zim_patch0_Rand1_Run",as.character(run),"_0",tail.string,".csv"),header=T,sep=",")
    validation.data <- read.csv(paste0(resultsdir,"Annual_outputs_CL05_Zim_patch0_Rand1_Run",as.character(run),"_0",tail.string,".csv"),header=T,sep=",")

    Nmen.validation <- validation.data$PopulationM
    Nwomen.validation <- validation.data$PopulationF
    
    PrEP.check.Nmen.lt15 <- data$PrEP_M.15.NoPrEP. + data$PrEP_M.15.WaitPrEP. + data$PrEP_M.15.OnPrEPSemi. + data$PrEP_M.15.OnPrEPAdh.

    PrEP.check.Nmen.1529 <- data$PrEP_M15.29.NoPrEP. + data$PrEP_M15.29.WaitPrEP. + data$PrEP_M15.29.OnPrEPSemi. + data$PrEP_M15.29.OnPrEPAdh.

    PrEP.check.Nmen.3054 <- data$PrEP_M30.54.NoPrEP. + data$PrEP_M30.54.WaitPrEP. + data$PrEP_M30.54.OnPrEPSemi. + data$PrEP_M30.54.OnPrEPAdh.

    PrEP.check.Nmen.55plus <- data$PrEP_M55..NoPrEP. + data$PrEP_M55..WaitPrEP. + data$PrEP_M55..OnPrEPSemi. + data$PrEP_M55..OnPrEPAdh. 

    PrEP.check.Nmen.neversex <- data$PrEP_Mneversex.NoPrEP. + data$PrEP_Mneversex.WaitPrEP. + data$PrEP_Mneversex.OnPrEPSemi. + data$PrEP_Mneversex.OnPrEPAdh.

    PrEP.check.Nmen <- data$PrEP_M.15.NoPrEP. + data$PrEP_M.15.WaitPrEP. + data$PrEP_M.15.OnPrEPSemi. + data$PrEP_M.15.OnPrEPAdh. + data$PrEP_M15.29.NoPrEP. + data$PrEP_M15.29.WaitPrEP. + data$PrEP_M15.29.OnPrEPSemi. + data$PrEP_M15.29.OnPrEPAdh. + data$PrEP_M30.54.NoPrEP. + data$PrEP_M30.54.WaitPrEP. + data$PrEP_M30.54.OnPrEPSemi. + data$PrEP_M30.54.OnPrEPAdh. + data$PrEP_M55..NoPrEP. + data$PrEP_M55..WaitPrEP. + data$PrEP_M55..OnPrEPSemi. + data$PrEP_M55..OnPrEPAdh. + data$PrEP_Mneversex.NoPrEP. + data$PrEP_Mneversex.WaitPrEP. + data$PrEP_Mneversex.OnPrEPSemi. + data$PrEP_Mneversex.OnPrEPAdh.


    PrEP.check.Nwomen.lt15 <- data$PrEP_F.15.NoPrEP. + data$PrEP_F.15.WaitPrEP. + data$PrEP_F.15.OnPrEPSemi. + data$PrEP_F.15.OnPrEPAdh. 

    PrEP.check.Nwomen.1524 <- data$PrEP_F15.24.NoPrEP. + data$PrEP_F15.24.WaitPrEP. + data$PrEP_F15.24.OnPrEPSemi. + data$PrEP_F15.24.OnPrEPAdh.

    PrEP.check.Nwomen.2554 <- data$PrEP_F25.54.NoPrEP. + data$PrEP_F25.54.WaitPrEP. + data$PrEP_F25.54.OnPrEPSemi. + data$PrEP_F25.54.OnPrEPAdh.

    PrEP.check.Nwomen.55plus <- data$PrEP_F55..NoPrEP. + data$PrEP_F55..WaitPrEP. + data$PrEP_F55..OnPrEPSemi. + data$PrEP_F55..OnPrEPAdh.

    PrEP.check.Nwomen.neversex <- data$PrEP_Fneversex.NoPrEP. + data$PrEP_Fneversex.WaitPrEP. + data$PrEP_Fneversex.OnPrEPSemi. + data$PrEP_Fneversex.OnPrEPAdh.


    prep.should.be.zero.men <- data$PrEP_M.15.WaitPrEP. + data$PrEP_M.15.OnPrEPSemi. + data$PrEP_M.15.OnPrEPAdh.data$PrEP_M55..WaitPrEP. + data$PrEP_M55..OnPrEPSemi. + data$PrEP_M55..OnPrEPAdh.  + data$PrEP_Mneversex.WaitPrEP. + data$PrEP_Mneversex.OnPrEPSemi. + data$PrEP_Mneversex.OnPrEPAdh.    
    
    prep.should.be.zero.women <-  + data$PrEP_F.15.WaitPrEP. + data$PrEP_F.15.OnPrEPSemi. + data$PrEP_F.15.OnPrEPAdh.  + data$PrEP_F55..WaitPrEP. + data$PrEP_F55..OnPrEPSemi. + data$PrEP_F55..OnPrEPAdh. +  + data$PrEP_Fneversex.WaitPrEP. + data$PrEP_Fneversex.OnPrEPSemi. + data$PrEP_Fneversex.OnPrEPAdh.
    
    # Overall PrEP:
    PrEP.check.Nwomen <- PrEP.check.Nwomen.lt15 +  PrEP.check.Nwomen.1524 + PrEP.check.Nwomen.2554 + PrEP.check.Nwomen.55plus + PrEP.check.Nwomen.neversex


    # VMMC:
    VMMC.check.lt15 <- data$VMMC_.15.uncirc. + data$VMMC_.15.waitVMMC. + data$VMMC_.15.VMMC. + data$VMMC_.15.VMMCheal. + data$VMMC_.15.TMC.

    VMMC.check.1529 <- data$VMMC_15.29.uncirc. + data$VMMC_15.29.waitVMMC. + data$VMMC_15.29.VMMC. + data$VMMC_15.29.VMMCheal. + data$VMMC_15.29.TMC.

    VMMC.check.3054 <- data$VMMC_30.54.uncirc. + data$VMMC_30.54.waitVMMC. + data$VMMC_30.54.VMMC. + data$VMMC_30.54.VMMCheal. + data$VMMC_30.54.TMC.

    VMMC.check.55plus <- data$VMMC_55..uncirc. + data$VMMC_55..waitVMMC. + data$VMMC_55..VMMC. + data$VMMC_55..VMMCheal. + data$VMMC_55..TMC.

    VMMC.check.neversex <- data$VMMC_neversex.uncirc. + data$VMMC_neversex.VMMCheal. + data$VMMC_neversex.waitVMMC. +  data$VMMC_neversex.TMC. + data$VMMC_neversex.VMMC.     

    AlwaysCondLT.check.Men.lt30 <- data$Npeople_AlwaysCondLT_M.30.n. + data$Npeople_AlwaysCondLT_M.30.y. + data$Npeople_NocurrentLT_M.30

    AlwaysCondLT.check.Men.30plus <- data$Npeople_AlwaysCondLT_M30..n. + data$Npeople_AlwaysCondLT_M30..y. + data$Npeople_NocurrentLT_M30.


    AlwaysCondLT.check.Women.lt25 <- data$Npeople_AlwaysCondLT_F.25.n. + data$Npeople_AlwaysCondLT_F.25.y. + data$Npeople_NocurrentLT_F.25

    AlwaysCondLT.check.Women.25plus <- data$Npeople_AlwaysCondLT_F25..n. + data$Npeople_AlwaysCondLT_F25..y. + data$Npeople_NocurrentLT_F25.
    AlwaysCondLT.check.Women <- AlwaysCondLT.check.Women.lt25 + AlwaysCondLT.check.Women.25plus

    AlwaysCondCasual.check.Men.lt30 <- data$Npeople_AlwaysCondCasual_M.30.n. + data$Npeople_AlwaysCondCasual_M.30.y. + data$Npeople_NocurrentCasual_M.30

    AlwaysCondCasual.check.Men.30plus <- data$Npeople_AlwaysCondCasual_M30..n. + data$Npeople_AlwaysCondCasual_M30..y. + data$Npeople_NocurrentCasual_M30.


    AlwaysCondCasual.check.Women.lt25 <- data$Npeople_AlwaysCondCasual_F.25.n. + data$Npeople_AlwaysCondCasual_F.25.y. + data$Npeople_NocurrentCasual_F.25

    AlwaysCondCasual.check.Women.25plus <- data$Npeople_AlwaysCondCasual_F25..n. + data$Npeople_AlwaysCondCasual_F25..y. + data$Npeople_NocurrentCasual_F25.
    AlwaysCondCasual.check.Women <- AlwaysCondCasual.check.Women.lt25 + AlwaysCondCasual.check.Women.25plus


    if(!(identical(Nmen.validation,PrEP.check.Nmen))){print("Error: PrEP Nmen does not match")}
    if(!(identical(Nwomen.validation,PrEP.check.Nwomen))){print("Error: PrEP Nwomen does not match")}

    if(!(identical(VMMC.check.lt15,PrEP.check.Nmen.lt15))){print("Error: VMMC and PrEP Nmen <15 does not match")}
    if(!(identical(VMMC.check.1529,PrEP.check.Nmen.1529))){print("Error: VMMC and PrEP Nmen 15-29 does not match")}
    if(!(identical(VMMC.check.3054,PrEP.check.Nmen.3054))){print("Error: VMMC and PrEP Nmen 30-54 does not match")}
    if(!(identical(VMMC.check.55plus,PrEP.check.Nmen.55plus))){print("Error: VMMC and PrEP Nmen 55+ does not match")}
    if(!(identical(VMMC.check.neversex,PrEP.check.Nmen.neversex))){print("Error: VMMC and PrEP Nmen neversex does not match")}    
    
    if(!all(prep.should.be.zero.men==0)){print("Error: some population of men that should not be eligible for PrEP are receiving it")}
    if(!all(prep.should.be.zero.women==0)){print("Error: some population of women that should not be eligible for PrEP are receiving it")}

    
    if(!(identical(Nwomen.validation,AlwaysCondLT.check.Women))){print("Error: always cond LT Women does not match")}
   


    if(!(identical(AlwaysCondCasual.check.Men.lt30,AlwaysCondLT.check.Men.lt30))){print("Error: Always cond casual Nmen <30 does not match always cond LT Nmen <30")}
    if(!(identical(AlwaysCondCasual.check.Men.30plus,AlwaysCondLT.check.Men.30plus))){print("Error: Always cond casual Nmen 30+ does not match always cond LT Nmen 30+")}
    if(!(identical(AlwaysCondCasual.check.Women.lt25,AlwaysCondLT.check.Women.lt25))){print("Error: Always cond casual Nwomen <25 does not match always cond LT Nwomen <25")}
    if(!(identical(AlwaysCondCasual.check.Women.25plus,AlwaysCondLT.check.Women.25plus))){print("Error: Always cond casual Nwomen 25+ does not match always cond LT Nwomen 25+")}
    if(!(identical(Nwomen.validation,AlwaysCondLT.check.Women))){print("Error: always cond LT Women does not match")}
    

    
    # Check people aren't starting PrEP when aged <15: 
    if(!all(data$PrEP_M.15.WaitPrEP. + data$PrEP_M.15.OnPrEPSemi. + data$PrEP_M.15.OnPrEPAdh. + data$PrEP_F.15.WaitPrEP. + data$PrEP_F.15.OnPrEPSemi. + data$PrEP_F.15.OnPrEPAdh.==0)){print("Error - some people are starting PrEP when under 15")}

}

