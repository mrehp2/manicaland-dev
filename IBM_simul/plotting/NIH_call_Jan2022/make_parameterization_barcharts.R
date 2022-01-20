rm(list=ls())

library(readxl)
library(ggplot2)
#xls_example <- readxl_example("~/")
#read_excel(xlsx_example, sheet = "chickwts")


make.cascade.props <- function(numerators)
{
    prop <- c(as.numeric(numerators[[2]])/as.numeric(numerators[[1]]),
              as.numeric(numerators[[3]])/as.numeric(numerators[[1]]),
              as.numeric(numerators[[4]])/as.numeric(numerators[[1]]))
    return(prop)
}


make.cascade.conditional.props <- function(numerators)
{
    prop <- c(as.numeric(numerators[[2]])/as.numeric(numerators[[1]]),
              as.numeric(numerators[[3]])/as.numeric(numerators[[2]]),
              as.numeric(numerators[[4]])/as.numeric(numerators[[3]]))
    return(prop)
}


# Given an intervention that alters the conditional probability of the i.intervention'th cascade element to value conditional.value.intervention, return the increase in the cascade compared to the original (for plotting as a stacked barchart).
#If you want the actual new cascade ,return new.cascade instead of change.in.cascade.
make.intervention.cascade <- function(i.intervention,conditional.value.intervention,original.cascade)
{
    if(i.intervention==1)
    {
        new.cascade <- c(conditional.value.intervention,(conditional.value.intervention/original.cascade[1])*c(original.cascade[2:3]))
    }else if(i.intervention==2)
    {
        new.cascade <- c(original.cascade[1],conditional.value.intervention*original.cascade[1],(conditional.value.intervention*original.cascade[1]/original.cascade[2])*original.cascade[3])
    }else if(i.intervention==3)
    {
        new.cascade <- c(original.cascade[1:2],(conditional.value.intervention*original.cascade[2]))
    }

    change.in.cascade <- new.cascade - original.cascade
    
    return(change.in.cascade)
}





cascade.data <- read_excel("/home/mike/Dropbox (SPH Imperial College)/Manicaland/Cascades/cascade_model_parameters.xlsx")

# These are the columns containing the n in each cascade step:
i.numerator <- c(4,5,8,11)

# cascade.data[[1]] is the prevention method, cascade.data[[3]] is the priority population age group.
cascade.data[[1]] %in% "Male condoms"

cascade.data[[1]] %in% "PrEP"

vmmc.15.29 <- cascade.data[cascade.data[[1]] %in% "VMMC" & cascade.data[[3]] %in% "Ever had sex 15-29",i.numerator]
vmmc.30.54 <- cascade.data[cascade.data[[1]] %in% "VMMC" & cascade.data[[3]] %in% "Ever had sex 30-54",i.numerator]


prep.M.15.29 <- cascade.data[cascade.data[[1]] %in% "PrEP" & cascade.data[[2]] %in% "Male" & cascade.data[[3]] %in% "Ever had sex 15-29",i.numerator]
prep.M.30.54 <- cascade.data[cascade.data[[1]] %in% "PrEP" & cascade.data[[2]] %in% "Male" & cascade.data[[3]] %in% "Ever had sex 30-54",i.numerator]
prep.F.15.24 <- cascade.data[cascade.data[[1]] %in% "PrEP" & cascade.data[[2]] %in% "Female" & cascade.data[[3]] %in% "Ever had sex 15-24",i.numerator]
prep.F.25.54 <- cascade.data[cascade.data[[1]] %in% "PrEP" & cascade.data[[2]] %in% "Female" & cascade.data[[3]] %in% "Ever had sex 25-54",i.numerator]


cond.M.15.29 <- cascade.data[cascade.data[[1]] %in% "Male condoms" & cascade.data[[2]] %in% "Male" & cascade.data[[3]] %in% "Ever had sex 15-29",i.numerator]
cond.M.30.54 <- cascade.data[cascade.data[[1]] %in% "Male condoms" & cascade.data[[2]] %in% "Male" & cascade.data[[3]] %in% "Ever had sex 30-54",i.numerator]
cond.F.15.24 <- cascade.data[cascade.data[[1]] %in% "Male condoms" & cascade.data[[2]] %in% "Female" & cascade.data[[3]] %in% "Ever had sex 15-24",i.numerator]
cond.F.25.54 <- cascade.data[cascade.data[[1]] %in% "Male condoms" & cascade.data[[2]] %in% "Female" & cascade.data[[3]] %in% "Ever had sex 25-54",i.numerator]


prop.vmmc.15.29 <- make.cascade.props(vmmc.15.29)
prop.vmmc.30.54 <- make.cascade.props(vmmc.30.54)

prop.prep.M.15.29 <- make.cascade.props(prep.M.15.29)
prop.prep.M.30.54 <- make.cascade.props(prep.M.30.54)
prop.prep.F.15.24 <- make.cascade.props(prep.F.15.24)
prop.prep.F.25.54 <- make.cascade.props(prep.F.25.54)

prop.cond.M.15.29 <- make.cascade.props(cond.M.15.29)
prop.cond.M.30.54 <- make.cascade.props(cond.M.30.54)
prop.cond.F.15.24 <- make.cascade.props(cond.F.15.24)
prop.cond.F.25.54 <- make.cascade.props(cond.F.25.54)


change.prop.vmmc.15.29.intervention <- make.intervention.cascade(1,0.9,prop.vmmc.15.29)
change.prop.vmmc.30.54.intervention <- make.intervention.cascade(1,0.9,prop.vmmc.30.54)


change.prop.prep.M.15.29.intervention <- make.intervention.cascade(2,1.0,prop.prep.M.15.29)
change.prop.prep.M.30.54.intervention <- make.intervention.cascade(2,1.0,prop.prep.M.30.54)
change.prop.prep.F.15.24.intervention <- make.intervention.cascade(2,1.0,prop.prep.F.15.24)
change.prop.prep.F.25.54.intervention <- make.intervention.cascade(2,1.0,prop.prep.F.25.54)


change.prop.cond.M.15.29.intervention <- make.intervention.cascade(3,0.9,prop.cond.M.15.29)
change.prop.cond.M.30.54.intervention <- make.intervention.cascade(3,0.9,prop.cond.M.30.54)
change.prop.cond.F.15.24.intervention <- make.intervention.cascade(3,0.9,prop.cond.F.15.24)
change.prop.cond.F.25.54.intervention <- make.intervention.cascade(3,0.9,prop.cond.F.25.54)




age.gp.vmmc <- c(rep("15-29",3),rep("30-54",3),rep("15-29",3),rep("30-54",3)) # 3 for the 3 barriers and then duplicate this for intervention/no intervention.

barrier.vmmc <- factor(c(rep(c("Motivation","Access","Effective use"),4)), levels=c("Motivation","Access","Effective use")) # 4=2*2 for 2 age/sex groups and intervention/no intervention. Use "factor" and "levels" to force the order of the barriers.


uptake.vmmc <- c(prop.vmmc.15.29,prop.vmmc.30.54,
            change.prop.vmmc.15.29.intervention,change.prop.vmmc.30.54.intervention)

# Multiply by 0.20524131132744 to convert from a cumulative % circumcised to an annual %. The value is obtained in C:\Users\mpickles\Dropbox (SPH Imperial College)\Manicaland\Model\VMMC\Model_VMMC_uptake_FINAL.xlsx - it is the % of VMMC operations from 2013-2019 (from DHIS-2 data) that occurred in 2019. Assume that this same multiplier holds now.

VMMC.annual.conversion <- 0.20524131132744
uptake.vmmc.annual <- uptake.vmmc*VMMC.annual.conversion


intervention.vmmc <- c(rep("With barriers",6),rep("Barriers reduced",6))
vmmc.dataframe <- data.frame(age.gp.vmmc,barrier.vmmc,uptake.vmmc,uptake.vmmc.annual,intervention.vmmc)






#########

age.gp.prep.cond <- rep(c(rep("Male 15-29",3),rep("Male 30-54",3),rep("Female 15-24",3),rep("Female 25-54",3)),2) # 3 for the 3 barriers and then duplicate this for intervention/no intervention.

barrier.prep.cond <- factor(c(rep(c("Motivation","Access","Effective use"),8)), levels=c("Motivation","Access","Effective use")) # 8=4*2 for 4 age/sex groups and intervention/no intervention. Use "factor" and "levels" to force the order of the barriers.
intervention.prep.cond <- c(rep("With barriers",12),rep("Barriers reduced",12))

uptake.prep <- c(prop.prep.M.15.29,prop.prep.M.30.54,prop.prep.F.15.24,prop.prep.F.25.54,
            change.prop.prep.M.15.29.intervention,change.prop.prep.M.30.54.intervention,change.prop.prep.F.15.24.intervention,change.prop.prep.F.25.54.intervention)

uptake.cond <- c(prop.cond.M.15.29,prop.cond.M.30.54,prop.cond.F.15.24,prop.cond.F.25.54,
            change.prop.cond.M.15.29.intervention,change.prop.cond.M.30.54.intervention,change.prop.cond.F.15.24.intervention,change.prop.cond.F.25.54.intervention)



vmmc.dataframe <- data.frame(age.gp.vmmc,barrier.vmmc,uptake.vmmc,intervention.vmmc)


prep.dataframe <- data.frame(age.gp.prep.cond,barrier.prep.cond,uptake.prep,intervention.prep.cond)

cond.dataframe <- data.frame(age.gp.prep.cond,barrier.prep.cond,uptake.cond,intervention.prep.cond)



#############################################################################

barplot.cols <- c("#727272","#f1595f","#79c36a","#599ad3","#f9a65a","#9e66ab","#cd7058","#d77fb3")

# VMMC:
pdf("VMMC_prevention_cascade_motivation.pdf",width=10,height=8)
ggplot(vmmc.dataframe, aes(x = barrier.vmmc, y = 100*uptake.vmmc, fill = intervention.vmmc)) + 
    geom_bar(stat = 'identity', position = 'stack') +
    scale_fill_manual(values = barplot.cols[c(3,4)])+
    facet_grid(~age.gp.vmmc) +
    labs(x="VMMC prevention cascade barrier", y="% getting VMMC", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()

# VMMC annual uptake:
pdf("VMMC_prevention_cascade_motivation_annual.pdf",width=10,height=8)
ggplot(vmmc.dataframe, aes(x = barrier.vmmc, y = 100*uptake.vmmc.annual, fill = intervention.vmmc)) + 
    geom_bar(stat = 'identity', position = 'stack') +
    scale_fill_manual(values = barplot.cols[c(3,4)])+
    facet_grid(~age.gp.vmmc) +
    labs(x="VMMC prevention cascade barrier", y="% getting VMMC per year", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()


# PrEP:
pdf("PrEP_prevention_cascade_access.pdf",width=10,height=8)
ggplot(prep.dataframe, aes(x = barrier.prep.cond, y = 100*uptake.prep, fill = intervention.prep.cond)) + 
    geom_bar(stat = 'identity', position = 'stack') +
    scale_fill_manual(values = barplot.cols[c(3,4)])+
    facet_grid(~age.gp.prep.cond) +
    labs(x="PrEP prevention cascade barrier", y="% using PrEP", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()

pdf("Condom_prevention_cascade_motivation.pdf",width=10,height=8)
ggplot(cond.dataframe, aes(x = barrier.prep.cond, y = 100*uptake.cond, fill = intervention.prep.cond)) + 
    geom_bar(stat = 'identity', position = 'stack') +
    scale_fill_manual(values = barplot.cols[c(3,4)])+
    facet_grid(~age.gp.prep.cond) +
    labs(x="Condom prevention cascade barrier", y="% wanting to use condoms", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))

dev.off()





################################
# Baseline plots (note - need to edit out legend by hand).
pdf("VMMC_prevention_cascade_baseline.pdf",width=10,height=8)
ggplot(vmmc.dataframe, aes(x = barrier.vmmc, y = 100*uptake.vmmc, fill = intervention.vmmc)) + 
    geom_bar(stat = 'identity', position = 'stack', alpha=rep(c(1.0,1.0,1.0,0.0,0.0,0.0),2)) +
    scale_fill_manual(values = barplot.cols[c(3,4)])+
    facet_grid(~age.gp.vmmc) +
    labs(x="VMMC prevention cascade barrier", y="% getting VMMC", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()

# Baseline plots (note - need to edit out legend by hand).
pdf("VMMC_prevention_cascade_annual_baseline.pdf",width=10,height=8)
ggplot(vmmc.dataframe, aes(x = barrier.vmmc, y = 100*uptake.vmmc.annual, fill = intervention.vmmc)) + 
    geom_bar(stat = 'identity', position = 'stack', alpha=rep(c(1.0,1.0,1.0,0.0,0.0,0.0),2)) +
    scale_fill_manual(values = barplot.cols[c(3,4)])+
    facet_grid(~age.gp.vmmc) +
    labs(x="VMMC prevention cascade barrier", y="% getting VMMC per year", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()


# PrEP:
pdf("PrEP_prevention_cascade_baseline.pdf",width=10,height=8)
ggplot(prep.dataframe, aes(x = barrier.prep.cond, y = 100*uptake.prep, fill = intervention.prep.cond)) + 
    geom_bar(stat = 'identity', position = 'stack', alpha=rep(c(1.0,1.0,1.0,0.0,0.0,0.0,1.0,1.0,1.0,0.0,0.0,0.0),2)) +
    scale_fill_manual(values = barplot.cols[c(3,4)])+
    facet_grid(~age.gp.prep.cond) +
    labs(x="PrEP prevention cascade barrier", y="% using PrEP", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()

pdf("Condom_prevention_cascade_baseline.pdf",width=10,height=8)
ggplot(cond.dataframe, aes(x = barrier.prep.cond, y = 100*uptake.cond, fill = intervention.prep.cond)) + 
    geom_bar(stat = 'identity', position = 'stack', alpha=rep(c(1.0,1.0,1.0,0.0,0.0,0.0,1.0,1.0,1.0,0.0,0.0,0.0),2)) +
    scale_fill_manual(values = barplot.cols[c(3,4)])+
    facet_grid(~age.gp.prep.cond) +
    labs(x="Condom prevention cascade barrier", y="% wanting to use condoms", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))

dev.off()












#####################################################################
# Special cascade - VMMC interventions for motivation
#                                      + access + eff use sequentially
#####################################################################
change.prop.vmmc.15.29.motivation <- make.intervention.cascade(1,0.9,prop.vmmc.15.29)
change.prop.vmmc.30.54.motivation <- make.intervention.cascade(1,0.9,prop.vmmc.30.54)


change.prop.vmmc.15.29.motivation.access <- make.intervention.cascade(2,1.0,change.prop.vmmc.15.29.motivation+prop.vmmc.15.29)
change.prop.vmmc.15.29.motivation.access.effuse <- make.intervention.cascade(3,0.9,change.prop.vmmc.15.29.motivation+prop.vmmc.15.29+change.prop.vmmc.15.29.motivation.access)
change.prop.vmmc.30.54.motivation.access <- make.intervention.cascade(2,1.0,change.prop.vmmc.30.54.motivation+prop.vmmc.30.54)
change.prop.vmmc.30.54.motivation.access.effuse <- make.intervention.cascade(3,0.9,change.prop.vmmc.30.54.motivation+prop.vmmc.30.54+change.prop.vmmc.30.54.motivation.access)
uptake.vmmc.allsteps <- c(prop.vmmc.15.29,prop.vmmc.30.54,
                          change.prop.vmmc.15.29.motivation,change.prop.vmmc.30.54.motivation,
                          change.prop.vmmc.15.29.motivation.access,change.prop.vmmc.30.54.motivation.access,
                          change.prop.vmmc.15.29.motivation.access.effuse,change.prop.vmmc.30.54.motivation.access.effuse
                          )

uptake.vmmc.allsteps.annual <- VMMC.annual.conversion*uptake.vmmc.allsteps


age.gp.vmmc.allsteps <- c(rep(c(rep("15-29",3),rep("30-54",3)),4)) # 3 for the 3 barriers and then duplicate this for intervention/no intervention.

barrier.vmmc.allsteps <- factor(c(rep(c("Motivation","Access","Effective use"),8)), levels=c("Motivation","Access","Effective use")) # 4=2*2 for 2 age/sex groups and intervention/no intervention. Use "factor" and "levels" to force the order of the barriers.


intervention.vmmc.allsteps <- c(rep("All barriers",6),rep("Increase motivation",6),rep("+Increase access",6),rep("All barriers reduced",6))
intervention.vmmc.allsteps <- factor(intervention.vmmc.allsteps, levels=rev(c("All barriers","Increase motivation","+Increase access","All barriers reduced")))
intervention.vmmc.allsteps.reversed <- factor(intervention.vmmc.allsteps, levels=c("All barriers","Increase motivation","+Increase access","All barriers reduced"))

vmmc.dataframe.allsteps <- data.frame(age.gp.vmmc.allsteps,barrier.vmmc.allsteps,uptake.vmmc.allsteps,uptake.vmmc.allsteps.annual,intervention.vmmc.allsteps,intervention.vmmc.allsteps.reversed)



pdf("VMMC_prevention_cascade_allsteps.pdf",width=10,height=8)

#vmmc.dataframe <- data.frame(age.gp.vmmc,barrier.vmmc,uptake.vmmc,intervention.vmmc)

ggplot(vmmc.dataframe.allsteps, aes(x = barrier.vmmc.allsteps, y = 100*uptake.vmmc.allsteps, fill = intervention.vmmc.allsteps)) + 
    geom_bar(stat = 'identity', position = 'stack') +
    scale_fill_manual(values = barplot.cols[c(1,2,3,4)])+
    #scale_fill_manual(values = c("Increase motivation"=barplot.cols[2],"+Increase access"=barplot.cols[3],"All barriers reduced"=barplot.cols[4],"All barriers"=barplot.cols[1]))+
    facet_grid(~age.gp.vmmc.allsteps) +
    labs(x="VMMC prevention cascade barrier", y="% getting VMMC", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()



# Should be the same as 'baseline'
pdf("VMMC_prevention_cascade_0.pdf",width=10,height=8)
ggplot(vmmc.dataframe.allsteps, aes(x = barrier.vmmc.allsteps, y = 100*uptake.vmmc.allsteps, fill = intervention.vmmc.allsteps)) + 
    geom_bar(stat = 'identity', position = 'stack', alpha=rep(c(1.0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0),2)) +
    scale_fill_manual(values = barplot.cols[c(1,2,3,4)])+
    #scale_fill_manual(values = c("Increase motivation"=barplot.cols[2],"+Increase access"=barplot.cols[3],"All barriers reduced"=barplot.cols[4],"All barriers"=barplot.cols[1]))+
    facet_grid(~age.gp.vmmc.allsteps) +
    labs(x="VMMC prevention cascade barrier", y="% getting VMMC", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()

pdf("VMMC_prevention_cascade_1.pdf",width=10,height=8)
ggplot(vmmc.dataframe.allsteps, aes(x = barrier.vmmc.allsteps, y = 100*uptake.vmmc.allsteps, fill = intervention.vmmc.allsteps)) + 
    geom_bar(stat = 'identity', position = 'stack', alpha=rep(c(1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0),2)) +
    scale_fill_manual(values = barplot.cols[c(1,2,3,4)])+
    #scale_fill_manual(values = c("Increase motivation"=barplot.cols[2],"+Increase access"=barplot.cols[3],"All barriers reduced"=barplot.cols[4],"All barriers"=barplot.cols[1]))+
    facet_grid(~age.gp.vmmc.allsteps) +
    labs(x="VMMC prevention cascade barrier", y="% getting VMMC", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()


pdf("VMMC_prevention_cascade_2.pdf",width=10,height=8)
ggplot(vmmc.dataframe.allsteps, aes(x = barrier.vmmc.allsteps, y = 100*uptake.vmmc.allsteps, fill = intervention.vmmc.allsteps)) + 
    geom_bar(stat = 'identity', position = 'stack', alpha=rep(c(1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0),2)) +
    scale_fill_manual(values = barplot.cols[c(1,2,3,4)])+
    #scale_fill_manual(values = c("Increase motivation"=barplot.cols[2],"+Increase access"=barplot.cols[3],"All barriers reduced"=barplot.cols[4],"All barriers"=barplot.cols[1]))+
    facet_grid(~age.gp.vmmc.allsteps) +
    labs(x="VMMC prevention cascade barrier", y="% getting VMMC", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()


# I can't figure out how to fix the legend order to be the right way around.
# So I will make an identical graph with the wrong bar ordering, but the 
# right legend order, and then copy-and-paste this legend over the original
# in my powerpoint slide :-(
pdf("VMMC_prevention_cascade_allsteps_legendreversed.pdf",width=10,height=8)

#vmmc.dataframe <- data.frame(age.gp.vmmc,barrier.vmmc,uptake.vmmc,intervention.vmmc)

ggplot(vmmc.dataframe.allsteps, aes(x = barrier.vmmc.allsteps, y = 100*uptake.vmmc.allsteps, fill = intervention.vmmc.allsteps.reversed)) + 
    geom_bar(stat = 'identity', position = 'stack') +
    scale_fill_manual(values = barplot.cols[c(4,3,2,1)])+
    #scale_fill_manual(values = c("Increase motivation"=barplot.cols[2],"+Increase access"=barplot.cols[3],"All barriers reduced"=barplot.cols[4],"All barriers"=barplot.cols[1]))+
    facet_grid(~age.gp.vmmc.allsteps) +
    labs(x="VMMC prevention cascade barrier", y="% getting VMMC", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()







#####################
# Now annual plots of VMMC:


pdf("VMMC_prevention_cascade_allsteps_annual.pdf",width=10,height=8)

#vmmc.dataframe <- data.frame(age.gp.vmmc,barrier.vmmc,uptake.vmmc,intervention.vmmc)

ggplot(vmmc.dataframe.allsteps, aes(x = barrier.vmmc.allsteps, y = 100*uptake.vmmc.allsteps.annual, fill = intervention.vmmc.allsteps)) + 
    geom_bar(stat = 'identity', position = 'stack') +
    scale_fill_manual(values = barplot.cols[c(1,2,3,4)])+
    #scale_fill_manual(values = c("Increase motivation"=barplot.cols[2],"+Increase access"=barplot.cols[3],"All barriers reduced"=barplot.cols[4],"All barriers"=barplot.cols[1]))+
    facet_grid(~age.gp.vmmc.allsteps) +
    labs(x="VMMC prevention cascade barrier", y="% getting VMMC per year", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()



# Should be the same as 'baseline'
pdf("VMMC_prevention_cascade_0_annual.pdf",width=10,height=8)
ggplot(vmmc.dataframe.allsteps, aes(x = barrier.vmmc.allsteps, y = 100*uptake.vmmc.allsteps.annual, fill = intervention.vmmc.allsteps)) + 
    geom_bar(stat = 'identity', position = 'stack', alpha=rep(c(1.0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0),2)) +
    scale_fill_manual(values = barplot.cols[c(1,2,3,4)])+
    #scale_fill_manual(values = c("Increase motivation"=barplot.cols[2],"+Increase access"=barplot.cols[3],"All barriers reduced"=barplot.cols[4],"All barriers"=barplot.cols[1]))+
    facet_grid(~age.gp.vmmc.allsteps) +
    labs(x="VMMC prevention cascade barrier", y="% getting VMMC per year", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()

pdf("VMMC_prevention_cascade_1_annual.pdf",width=10,height=8)
ggplot(vmmc.dataframe.allsteps, aes(x = barrier.vmmc.allsteps, y = 100*uptake.vmmc.allsteps.annual, fill = intervention.vmmc.allsteps)) + 
    geom_bar(stat = 'identity', position = 'stack', alpha=rep(c(1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0),2)) +
    scale_fill_manual(values = barplot.cols[c(1,2,3,4)])+
    #scale_fill_manual(values = c("Increase motivation"=barplot.cols[2],"+Increase access"=barplot.cols[3],"All barriers reduced"=barplot.cols[4],"All barriers"=barplot.cols[1]))+
    facet_grid(~age.gp.vmmc.allsteps) +
    labs(x="VMMC prevention cascade barrier", y="% getting VMMC per year", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()


pdf("VMMC_prevention_cascade_2_annual.pdf",width=10,height=8)
ggplot(vmmc.dataframe.allsteps, aes(x = barrier.vmmc.allsteps, y = 100*uptake.vmmc.allsteps.annual, fill = intervention.vmmc.allsteps)) + 
    geom_bar(stat = 'identity', position = 'stack', alpha=rep(c(1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0),2)) +
    scale_fill_manual(values = barplot.cols[c(1,2,3,4)])+
    #scale_fill_manual(values = c("Increase motivation"=barplot.cols[2],"+Increase access"=barplot.cols[3],"All barriers reduced"=barplot.cols[4],"All barriers"=barplot.cols[1]))+
    facet_grid(~age.gp.vmmc.allsteps) +
    labs(x="VMMC prevention cascade barrier", y="% getting VMMC per year", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()


# I can't figure out how to fix the legend order to be the right way around.
# So I will make an identical graph with the wrong bar ordering, but the 
# right legend order, and then copy-and-paste this legend over the original
# in my powerpoint slide :-(
pdf("VMMC_prevention_cascade_allsteps_legendreversed_annual.pdf",width=10,height=8)

#vmmc.dataframe <- data.frame(age.gp.vmmc,barrier.vmmc,uptake.vmmc,intervention.vmmc)

ggplot(vmmc.dataframe.allsteps, aes(x = barrier.vmmc.allsteps, y = 100*uptake.vmmc.allsteps.annual, fill = intervention.vmmc.allsteps.reversed)) + 
    geom_bar(stat = 'identity', position = 'stack') +
    scale_fill_manual(values = barplot.cols[c(4,3,2,1)])+
    #scale_fill_manual(values = c("Increase motivation"=barplot.cols[2],"+Increase access"=barplot.cols[3],"All barriers reduced"=barplot.cols[4],"All barriers"=barplot.cols[1]))+
    facet_grid(~age.gp.vmmc.allsteps) +
    labs(x="VMMC prevention cascade barrier", y="% getting VMMC per year", fill="") +
    theme(legend.position="bottom", text=element_text(size=12)) +
    scale_x_discrete(labels= c("Motivation","Access","Effective\nuse"))
dev.off()
