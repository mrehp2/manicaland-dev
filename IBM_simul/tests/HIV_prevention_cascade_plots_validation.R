


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
    
    data <- read.csv(paste0("../results/RESULTS/Output/HIVpreventioncascade_CL05_Zim_patch0_Rand1_Run",as.character(run),"_0",tail.string,".csv"),header=T,sep=",")
    validation.data <- read.csv(paste0("../results/RESULTS/Output/Annual_outputs_CL05_Zim_patch0_Rand1_Run",as.character(run),"_0",tail.string,".csv"),header=T,sep=",")

    Nmen.validation <- validation.data$PopulationM
    Nwomen.validation <- validation.data$PopulationF
    
    PrEP.check.Nmen <- data$PrEP_M.15.NoPrEP. + data$PrEP_M.15.WaitPrEP. + data$PrEP_M.15.OnPrEPSemi. + data$PrEP_M.15.OnPrEPAdh. + data$PrEP_M15.29.NoPrEP. + data$PrEP_M15.29.WaitPrEP. + data$PrEP_M15.29.OnPrEPSemi. + data$PrEP_M15.29.OnPrEPAdh. + data$PrEP_M30.54.NoPrEP. + data$PrEP_M30.54.WaitPrEP. + data$PrEP_M30.54.OnPrEPSemi. + data$PrEP_M30.54.OnPrEPAdh. + data$PrEP_M55..NoPrEP. + data$PrEP_M55..WaitPrEP. + data$PrEP_M55..OnPrEPSemi. + data$PrEP_M55..OnPrEPAdh. + data$PrEP_Mneversex.NoPrEP. + data$PrEP_Mneversex.WaitPrEP. + data$PrEP_Mneversex.OnPrEPSemi. + data$PrEP_Mneversex.OnPrEPAdh.

    PrEP.check.Nwomen <- data$PrEP_F.15.NoPrEP. + data$PrEP_F.15.WaitPrEP. + data$PrEP_F.15.OnPrEPSemi. + data$PrEP_F.15.OnPrEPAdh. + data$PrEP_F15.24.NoPrEP. + data$PrEP_F15.24.WaitPrEP. + data$PrEP_F15.24.OnPrEPSemi. + data$PrEP_F15.24.OnPrEPAdh. + data$PrEP_F25.54.NoPrEP. + data$PrEP_F25.54.WaitPrEP. + data$PrEP_F25.54.OnPrEPSemi. + data$PrEP_F25.54.OnPrEPAdh. + data$PrEP_F55..NoPrEP. + data$PrEP_F55..WaitPrEP. + data$PrEP_F55..OnPrEPSemi. + data$PrEP_F55..OnPrEPAdh. + data$PrEP_Fneversex.NoPrEP. + data$PrEP_Fneversex.WaitPrEP. + data$PrEP_Fneversex.OnPrEPSemi. + data$PrEP_Fneversex.OnPrEPAdh.


    VMMC.check.lt30 <- data$VMMC_.15.uncirc. + data$VMMC_.15.waitVMMC. + data$VMMC_.15.VMMC. + data$VMMC_.15.VMMCheal. + data$VMMC_.15.TMC. + data$VMMC_15.29.uncirc. + data$VMMC_15.29.waitVMMC. + data$VMMC_15.29.VMMC. + data$VMMC_15.29.VMMCheal. + data$VMMC_15.29.TMC.

    VMMC.check.30plus <- data$VMMC_30.54.uncirc. + data$VMMC_30.54.waitVMMC. + data$VMMC_30.54.VMMC. + data$VMMC_30.54.VMMCheal. + data$VMMC_30.54.TMC. + data$VMMC_55..uncirc. + data$VMMC_55..waitVMMC. + data$VMMC_55..VMMC. + data$VMMC_55..VMMCheal. + data$VMMC_55..TMC.


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

    if(!(identical(Nmen.validation,(VMMC.check.lt30+VMMC.check.30plus)))){print("Error: VMMC Nmen does not match")}
    


    if(!(identical(VMMC.check.lt30,AlwaysCondLT.check.Men.lt30))){print("Error: VMMC Nmen <30 does not match always cond LT Nmen <30")}
    if(!(identical(VMMC.check.30plus,AlwaysCondLT.check.Men.30plus))){print("Error: VMMC Nmen 30+ does not match always cond LT Nmen 30+")}
    if(!(identical(Nwomen.validation,AlwaysCondLT.check.Women))){print("Error: always cond LT Women does not match")}
    
    if(!(identical(VMMC.check.lt30,AlwaysCondCasual.check.Men.lt30))){print("Error: VMMC Nmen <30 does not match always cond Casual Nmen <30")}
    if(!(identical(VMMC.check.30plus,AlwaysCondCasual.check.Men.30plus))){print("Error: VMMC Nmen 30+ does not match always cond Casual Nmen 30+")}
    if(!(identical(Nwomen.validation,AlwaysCondCasual.check.Women))){print("Error: always cond Casual Women does not match")}


    # Check people aren't starting PrEP when aged <15: 
    if(!all(data$PrEP_M.15.WaitPrEP. + data$PrEP_M.15.OnPrEPSemi. + data$PrEP_M.15.OnPrEPAdh. + data$PrEP_F.15.WaitPrEP. + data$PrEP_F.15.OnPrEPSemi. + data$PrEP_F.15.OnPrEPAdh.==0)){print("Error - some people are starting PrEP when under 15")}

}

