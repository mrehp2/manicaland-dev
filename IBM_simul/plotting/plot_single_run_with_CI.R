


rm(list=ls())



extract.data <- function(resultsdir,county,run.number)
{
    run.data <- read.csv(paste0(resultsdir,"output_",county,"_run",as.character(run.number),".csv"),header=T)


    i.hiv.acute.young.virt <- 8
    i.hiv.acute.old.virt <- 9
    i.hiv.acute.young.both <- 10
    i.hiv.acute.old.both <- 11
    i.hiv.acute.young.phys <- 12
    i.hiv.acute.old.phys <- 13

    i.hiv.acute <- seq(8,13)
    i.hiv.chronic <- sort(c(seq(14,121,12),seq(15,121,12),seq(16,121,12),seq(17,121,12),seq(18,121,12),seq(19,121,12)))
    i.hiv.late <- sort(c(seq(20,121,12),seq(21,121,12),seq(22,121,12),seq(23,121,12),seq(24,121,12),seq(25,121,12)))
    i.hiv.chronicandlate <- sort(c(i.hiv.chronic,i.hiv.late))

    i.hiv.young.virt <- c(i.hiv.acute.young.virt,seq(14,116,6))
    i.hiv.old.virt <- i.hiv.young.virt +1

    i.hiv.young.both <- i.hiv.young.virt +2
    i.hiv.old.both <- i.hiv.young.virt +3

    i.hiv.young.phys <- i.hiv.young.virt +4
    i.hiv.old.phys <- i.hiv.young.virt +5

    i.unaware.young.virt <- c(i.hiv.acute.young.virt,14,20,50,56,86,92)
    i.onart.young.virt <- c(26,32,62,68,98,104)
    i.outsidecare.young.virt <- c(38,44,74,80,110,116)

    i.unaware.old.virt <- i.unaware.young.virt +1
    i.onart.old.virt <- i.onart.young.virt +1
    i.outsidecare.old.virt <- i.outsidecare.young.virt +1

    i.unaware.young.both <- i.unaware.young.virt +2
    i.onart.young.both <- i.onart.young.virt +2
    i.outsidecare.young.both <- i.outsidecare.young.virt +2

    i.unaware.old.both <- i.unaware.young.virt +3
    i.onart.old.both <- i.onart.young.virt +3
    i.outsidecare.old.both <- i.outsidecare.young.virt +3

    i.unaware.young.phys <- i.unaware.young.virt +4
    i.onart.young.phys <- i.onart.young.virt +4
    i.outsidecare.young.phys <- i.outsidecare.young.virt +4

    i.unaware.old.phys <- i.unaware.young.virt +5
    i.onart.old.phys <- i.onart.young.virt +5
    i.outsidecare.old.phys <- i.outsidecare.young.virt +5



    i.young.virt <- c(2,i.hiv.young.virt)
    i.old.virt <- i.young.virt +1

    i.young.both <- i.young.virt +2
    i.old.both <- i.young.virt +3

    i.young.phys <- i.young.virt +4
    i.old.phys <- i.young.virt +5


    i.young <- c(i.young.virt,i.young.both,i.young.phys)
    i.old <- c(i.old.virt,i.old.both,i.old.phys)

    i.hiv.young <- c(i.hiv.young.virt,i.hiv.young.both,i.hiv.young.phys)
    i.hiv.old   <- c(i.hiv.old.virt,i.hiv.old.both,i.hiv.old.phys)


    i.virt <- c(i.young.virt,i.old.virt)
    i.both <- c(i.young.both,i.old.both)
    i.phys <- c(i.young.phys,i.old.phys)

    i.hiv.virt <- c(i.hiv.young.virt,i.hiv.old.virt)
    i.hiv.both <- c(i.hiv.young.both,i.hiv.old.both)
    i.hiv.phys <- c(i.hiv.young.phys,i.hiv.old.phys)

    i.all <- c(i.young,i.old)
    i.hiv.all <- c(i.hiv.young,i.hiv.old)

    i.inc.young.virt <- 122
    i.inc.old.virt <- 123
    i.inc.young.both <- 124
    i.inc.old.both <- 125
    i.inc.young.phys <- 126
    i.inc.old.phys <- 127


##################################################################
##################################################################
                                        # Assign:
##################################################################
##################################################################




    t <- run.data[,1]

##################################################################
                                        # HIV prevalence:
##################################################################
    num.hiv.all <- rowSums(run.data[,i.hiv.all])
    denom.hiv.all <- rowSums(run.data[,i.all])
    prev.all <- num.hiv.all/denom.hiv.all


                                        #Prevalence by typology
    num.hiv.virt <- rowSums(run.data[,i.hiv.virt])
    denom.hiv.virt <- rowSums(run.data[,i.virt])
    prev.virt <- num.hiv.virt/denom.hiv.virt

    num.hiv.both <- rowSums(run.data[,i.hiv.both])
    denom.hiv.both <- rowSums(run.data[,i.both])
    prev.both <- num.hiv.both/denom.hiv.both

    num.hiv.phys <- rowSums(run.data[,i.hiv.phys])
    denom.hiv.phys <- rowSums(run.data[,i.phys])
    prev.phys <- num.hiv.phys/denom.hiv.phys

    num.hiv.young <- rowSums(run.data[,i.hiv.young])
    denom.hiv.young <- rowSums(run.data[,i.young])
    prev.young <- num.hiv.young/denom.hiv.young

    num.hiv.old <- rowSums(run.data[,i.hiv.old])
    denom.hiv.old <- rowSums(run.data[,i.old])
    prev.old <- num.hiv.old/denom.hiv.old


    ##################################################################
    # HIV care cascade:
    ##################################################################
    num.unaware.young.virt <- rowSums(run.data[,i.unaware.young.virt])
    num.onart.young.virt <- rowSums(run.data[,i.onart.young.virt])
    num.outsidecare.young.virt <- rowSums(run.data[,i.outsidecare.young.virt])
    
    num.unaware.old.virt <- rowSums(run.data[,i.unaware.old.virt])
    num.onart.old.virt <- rowSums(run.data[,i.onart.old.virt])
    num.outsidecare.old.virt <- rowSums(run.data[,i.outsidecare.old.virt])
    
    num.unaware.young.both <- rowSums(run.data[,i.unaware.young.both])
    num.onart.young.both <- rowSums(run.data[,i.onart.young.both])
    num.outsidecare.young.both <- rowSums(run.data[,i.outsidecare.young.both])
    
    num.unaware.old.both <- rowSums(run.data[,i.unaware.old.both])
    num.onart.old.both <- rowSums(run.data[,i.onart.old.both])
    num.outsidecare.old.both <- rowSums(run.data[,i.outsidecare.old.both])
    
    num.unaware.young.phys <- rowSums(run.data[,i.unaware.young.phys])
    num.onart.young.phys <- rowSums(run.data[,i.onart.young.phys])
    num.outsidecare.young.phys <- rowSums(run.data[,i.outsidecare.young.phys])
    
    num.unaware.old.phys <- rowSums(run.data[,i.unaware.old.phys])
    num.onart.old.phys <- rowSums(run.data[,i.onart.old.phys])
    num.outsidecare.old.phys <- rowSums(run.data[,i.outsidecare.old.phys])


    prop.unaware.virt <- (num.unaware.young.virt+num.unaware.old.virt)/num.hiv.virt
    prop.unaware.both <- (num.unaware.young.both+num.unaware.old.both)/num.hiv.both
    prop.unaware.phys <- (num.unaware.young.phys+num.unaware.old.phys)/num.hiv.phys

    prop.unaware.young <- (num.unaware.young.virt+num.unaware.young.both+num.unaware.young.phys)/num.hiv.young
    prop.unaware.old <- (num.unaware.old.virt+num.unaware.old.both+num.unaware.old.phys)/num.hiv.old

   ##################################################################
   # Extras for validation/debugging:
   ##################################################################
    prop.acute <- rowSums(run.data[,i.hiv.acute]) / (rowSums(run.data[,i.hiv.acute])+rowSums(run.data[,i.hiv.chronicandlate]))
    prop.chronic <- rowSums(run.data[,i.hiv.chronic]) / (rowSums(run.data[,i.hiv.acute])+rowSums(run.data[,i.hiv.chronicandlate]))
    prop.late<- rowSums(run.data[,i.hiv.late]) / rowSums(run.data[,i.hiv.chronicandlate])

    prop.virt <- denom.hiv.virt/(denom.hiv.virt+denom.hiv.both+denom.hiv.phys)
    prop.both <- denom.hiv.both/(denom.hiv.virt+denom.hiv.both+denom.hiv.phys)
    prop.phys <- denom.hiv.phys/(denom.hiv.virt+denom.hiv.both+denom.hiv.phys)
    
    
    
    # Only use every step.size
    step.size <- 10
    n.steps <- length(t)
    steps <- seq(1,n.steps,step.size)
    if(tail(steps,1)!=n.steps)
        steps <- c(steps,n.steps)
    
    outputs = list(t=t[steps], prev.all=prev.all[steps], prev.virt=prev.virt[steps], prev.both=prev.both[steps], prev.phys=prev.phys[steps], prev.young=prev.young[steps], prev.old=prev.old[steps],prop.unaware.virt=prop.unaware.virt[steps],prop.unaware.both=prop.unaware.both[steps],prop.unaware.phys=prop.unaware.phys[steps],prop.unaware.young=prop.unaware.young[steps],prop.unaware.old=prop.unaware.old[steps],prop.acute=prop.acute[steps],prop.chronic=prop.chronic[steps],prop.late=prop.late[steps],prop.virt=prop.virt[steps],prop.both=prop.both[steps],prop.phys=prop.phys[steps])

    

    return(outputs)

}





get.survey.data <- function(county)
{
    baseline.survey.data.file <- file(paste0("~/Dropbox (SPH Imperial College)/projects/Kenya_MSM_HIVST/Analysis/",county,"_baseline_data.txt"),open="r")
    readLines(baseline.survey.data.file,1)
                                        # [1] "HIV prevalence by age gp"
    readLines(baseline.survey.data.file,1)
                                        # [1] "\"<25\" \"25+\""
    l <- readLines(baseline.survey.data.file,1)
    neg.lt25 <- as.numeric(sapply(strsplit(l," "),"[[",2))
    neg.25plus <- as.numeric(sapply(strsplit(l," "),"[[",3))
    l <- readLines(baseline.survey.data.file,1)
    pos.lt25 <- as.numeric(sapply(strsplit(l," "),"[[",2))
    pos.25plus <- as.numeric(sapply(strsplit(l," "),"[[",3))
    readLines(baseline.survey.data.file,1)
    ## HIV prevalence by place find partner
    readLines(baseline.survey.data.file,1)
    ## "Virtual" "Both" "Physical"
    l <- readLines(baseline.survey.data.file,1)
    neg.virt <- as.numeric(sapply(strsplit(l," "),"[[",2))
    neg.both <- as.numeric(sapply(strsplit(l," "),"[[",3))
    neg.phys <- as.numeric(sapply(strsplit(l," "),"[[",4))
    l <- readLines(baseline.survey.data.file,1)
    pos.virt <- as.numeric(sapply(strsplit(l," "),"[[",2))
    pos.both <- as.numeric(sapply(strsplit(l," "),"[[",3))
    pos.phys <- as.numeric(sapply(strsplit(l," "),"[[",4))
    readLines(baseline.survey.data.file,1)
    ## Aware of status
    readLines(baseline.survey.data.file,1)
    ## "x"
    l <- readLines(baseline.survey.data.file,1)
    n.unaware <- as.numeric(sapply(strsplit(l," "),"[[",2))
    l <- readLines(baseline.survey.data.file,1)
    n.aware <- as.numeric(sapply(strsplit(l," "),"[[",2))
    close(baseline.survey.data.file)

    p.virt <- pos.virt/(pos.virt+neg.virt+0.0)
    p.both <- pos.both/(pos.both+neg.both+0.0)
    p.phys <- pos.phys/(pos.phys+neg.phys+0.0)
    p.lt25 <- pos.lt25/(pos.lt25+neg.lt25+0.0)
    p.25plus <- pos.25plus/(pos.25plus+neg.25plus+0.0)

    p.all <- (pos.lt25+pos.25plus)/(pos.lt25+neg.lt25+pos.25plus+neg.25plus+0.0)
    
    width.virt   <- 1.96*sqrt(p.virt*(1-p.virt)/(pos.virt+neg.virt))
    width.both   <- 1.96*sqrt(p.both*(1-p.both)/(pos.both+neg.both))
    width.phys   <- 1.96*sqrt(p.phys*(1-p.phys)/(pos.phys+neg.phys))
    width.lt25   <- 1.96*sqrt(p.lt25*(1-p.lt25)/(pos.lt25+neg.lt25))
    width.25plus <- 1.96*sqrt(p.25plus*(1-p.25plus)/(pos.25plus+neg.25plus))

    width.all   <- 1.96*sqrt(p.all*(1-p.all)/(pos.lt25+neg.lt25+pos.25plus+neg.25plus))

    outputs <- list(p.all=100*p.all,p.virt=100*p.virt,p.both=100*p.both,p.phys=100*p.phys,p.lt25=100*p.lt25,p.25plus=100*p.25plus,width.all=100*width.all,width.virt=100*width.virt,width.both=100*width.both,width.phys=100*width.phys,width.lt25=100*width.lt25,width.25plus=100*width.25plus)
    return(outputs)
}




#county <- "kiambu"
county <- "kisumu"
#county <- "mombasa"
resultsdir <- paste0("results/",county,"/")




baseline.data <- get.survey.data(county)
t.baseline <- 2019.35  # Mean date of baseline is 07 May 2019
t.endline <- 2020.78   # Mean date of endline is 13 Oct 2020 = 2020.78

t.intervention <- 2019.58
start.time.simul <- 2019.58-150
type.col <- c("blue","red","green")

fits <- c(27,63,90,203,245,413)



for (i in fits)
{
    outputs = extract.data(resultsdir,county,i)
    t <- outputs$t+start.time.simul # Make 2019.58 (intervention start date t=150) August 2019.
    prev.all = outputs$prev.all
    if(i==fits[1]){
        plot(t,100*prev.all,col=type.col[1],type="l",ylab="Overall prevalence (%)",xlab="",ylim=c(0,1.1*max(max(100*prev.all),baseline.data$p.all+baseline.data$width.all*1.1)))
        arrows(t.baseline, baseline.data$p.all+baseline.data$width.all, t.baseline, baseline.data$p.all-baseline.data$width.all, angle=90, code=3, length=0.05)
    }else{
        lines(t,100*prev.all,col=type.col[2])
    }
}


# By typology:
par(mfrow=c(1,3))
for (i in fits)
{
    outputs = extract.data(resultsdir,county,i)
    t <- outputs$t+start.time.simul # Make 2019.58 (intervention start date t=150) August 2019.
    prev.virt = outputs$prev.virt
    if(i==fits[1]){
        plot(t,100*prev.virt,col=type.col[1],type="l",ylab="Virtual MSM prevalence (%)",xlab="",ylim=c(0,max(max(100*prev.virt),baseline.data$p.virt+baseline.data$width.virt*1.1)))
        arrows(t.baseline, baseline.data$p.virt+baseline.data$width.virt, t.baseline, baseline.data$p.virt-baseline.data$width.virt, angle=90, code=3, length=0.05)
    }else{
        lines(t,100*prev.virt,col=type.col[2])
    }
}

for (i in fits)
{
    outputs = extract.data(resultsdir,county,i)
    t <- outputs$t+start.time.simul # Make 2019.58 (intervention start date t=150) August 2019.
    prev.both = outputs$prev.both
    if(i==fits[1]){
        plot(t,100*prev.both,col=type.col[1],type="l",ylab="Dual MSM prevalence (%)",xlab="",ylim=c(0,max(max(100*prev.both),baseline.data$p.both+baseline.data$width.both*1.1)))
        arrows(t.baseline, baseline.data$p.both+baseline.data$width.both, t.baseline, baseline.data$p.both-baseline.data$width.both, angle=90, code=3, length=0.05)
    }else{
        lines(t,100*prev.both,col=type.col[2])
    }
}

for (i in fits)
{
    outputs = extract.data(resultsdir,county,i)
    t <- outputs$t+start.time.simul # Make 2019.58 (intervention start date t=150) August 2019.
    prev.phys = outputs$prev.phys
    if(i==fits[1]){
        plot(t,100*prev.phys,col=type.col[1],type="l",ylab="Physical MSM prevalence (%)",xlab="",ylim=c(0,max(max(100*prev.phys),baseline.data$p.phys+baseline.data$width.phys*1.1)))
        arrows(t.baseline, baseline.data$p.phys+baseline.data$width.phys, t.baseline, baseline.data$p.phys-baseline.data$width.phys, angle=90, code=3, length=0.05)
    }else{
        lines(t,100*prev.phys,col=type.col[2])
    }
}


###################
# By age:
##################


par(mfrow=c(1,2))
for (i in fits)
{
    outputs = extract.data(resultsdir,county,i)
    t <- outputs$t+start.time.simul # Make 2019.58 (intervention start date t=150) August 2019.
    prev.lt25 = outputs$prev.young
    if(i==fits[1]){
        plot(t,100*prev.lt25,col=type.col[1],type="l",ylab="Prevalence in <25 yrs (%)",xlab="",ylim=c(0,max(max(100*prev.lt25),baseline.data$p.lt25+baseline.data$width.lt25*1.1)))
        arrows(t.baseline, baseline.data$p.lt25+baseline.data$width.lt25, t.baseline, baseline.data$p.lt25-baseline.data$width.lt25, angle=90, code=3, length=0.05)
    }else{
        lines(t,100*prev.lt25,col=type.col[2])
    }
}

for (i in fits)
{
    outputs = extract.data(resultsdir,county,i)
    t <- outputs$t+start.time.simul # Make 2019.58 (intervention start date t=150) August 2019.
    prev.25plus = outputs$prev.old
    if(i==fits[1]){
        plot(t,100*prev.25plus,col=type.col[1],type="l",ylab="Prevalence in 25+ yrs (%)",xlab="",ylim=c(0,max(max(100*prev.25plus),baseline.data$p.25plus+baseline.data$width.25plus*1.1)))
        arrows(t.baseline, baseline.data$p.25plus+baseline.data$width.25plus, t.baseline, baseline.data$p.25plus-baseline.data$width.25plus, angle=90, code=3, length=0.05)
    }else{
        lines(t,100*prev.25plus,col=type.col[2])
    }
}



































for (i in fits)
{
    outputs = extract.data(resultsdir,county,i)
    t <- outputs$t+start.time.simul # Make 2019.58 (intervention start date t=150) August 2019.
    prop.unaware.virt = outputs$prop.unaware.virt
    prop.unaware.both = outputs$prop.unaware.both
    prop.unaware.phys = outputs$prop.unaware.phys
    if(i==fits[1]){
        plot(t,100*prop.unaware.virt,col=type.col[1],type="l",ylab="% of HIV+ unaware by typology",xlab="")
        lines(t,100*prop.unaware.both,col=type.col[2],type="l")
        lines(t,100*prop.unaware.phys,col=type.col[3],type="l")
        legend("topright",col=type.col,legend=c("Virtual","Both","Physical"),lty=1,bty="n")
        #arrows(t.baseline, baseline.data$p.25plus+baseline.data$width.25plus, t.baseline, baseline.data$p.25plus-baseline.data$width.25plus, angle=90, code=3, length=0.05)
    }else{
        lines(t,100*prop.unaware.virt,col=type.col[1],type="l")
        lines(t,100*prop.unaware.both,col=type.col[2],type="l")
        lines(t,100*prop.unaware.phys,col=type.col[3],type="l")
    }
}

age.col <- c("blue","green")


for (i in fits)
{
    outputs = extract.data(resultsdir,county,i)
    t <- outputs$t+start.time.simul # Make 2019.58 (intervention start date t=150) August 2019.
    prop.unaware.old = outputs$prop.unaware.old
    prop.unaware.young = outputs$prop.unaware.young
    prop.unaware.phys = outputs$prop.unaware.phys
    if(i==fits[1]){
        plot(t,100*prop.unaware.old,col=age.col[2],type="l",ylab="% of HIV+ unaware by age",xlab="")
        lines(t,100*prop.unaware.young,col=age.col[1],type="l")
        legend("topright",col=age.col,legend=c("<25","25+"),lty=1,bty="n")
        #arrows(t.baseline, baseline.data$p.25plus+baseline.data$width.25plus, t.baseline, baseline.data$p.25plus-baseline.data$width.25plus, angle=90, code=3, length=0.05)
    }else{
        lines(t,100*prop.unaware.old,col=age.col[2],type="l")
        lines(t,100*prop.unaware.young,col=age.col[1],type="l")
    }
}














cols.naturalhist <- c("brown","gray","purple")
plot(t,100*outputs$prop.chronic,type="l",ylim=c(0,100),col=cols.naturalhist[1],ylab="% by HIV stage")
lines(t,100*outputs$prop.late,col=cols.naturalhist[2])
lines(t,100*outputs$prop.acute,col=cols.naturalhist[3])
legend(x=1980,y=85,col=cols.naturalhist,legend=c("Chronic","Late","Acute"),lty=1,bty="n")



####################
#Validation:
####################

# Check % of population in each group is constant over time:
plot(t,100*outputs$prop.virt,col=type.col[1],type="l",ylab="% of population by typology",xlab="",ylim=c(0,100))
lines(t,100*outputs$prop.both,col=type.col[2],type="l")
lines(t,100*outputs$prop.phys,col=type.col[3],type="l")
legend("topright",col=type.col,legend=c("Virtual","Both","Physical"),lty=1,bty="n")




###############################################################################
# For validation - plot all 3 types on one plot (to check prevalence works). 
###############################################################################
for (i in fits)
{
    outputs = extract.data(resultsdir,county,i)
    t <- outputs$t+start.time.simul # Make 2019.58 (intervention start date t=150) August 2019.
    prev.phys = outputs$prev.phys
    prev.both = outputs$prev.both
    prev.virt = outputs$prev.virt
    if (i==fits[1]){
        plot(t,100*prev.virt,col=type.col[1],type="l",ylab="Virtual MSM prevalence (%)",xlab="",ylim=c(0,max(max(100*prev.virt),baseline.data$p.virt+baseline.data$width.virt*1.1)))
        lines(t,100*prev.phys,col=type.col[2])
        lines(t,100*prev.both,col=type.col[3])
    }else{
        lines(t,100*prev.virt,col=type.col[1])
        lines(t,100*prev.phys,col=type.col[2])
        lines(t,100*prev.both,col=type.col[3])
    }
}


