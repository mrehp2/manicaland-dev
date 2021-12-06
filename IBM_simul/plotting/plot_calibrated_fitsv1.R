


rm(list=ls())



extract.data <- function(resultsdir,county,run.filename)
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

    prop.onart.virt <- (num.onart.young.virt+num.onart.old.virt)/num.hiv.virt
    prop.onart.both <- (num.onart.young.both+num.onart.old.both)/num.hiv.both
    prop.onart.phys <- (num.onart.young.phys+num.onart.old.phys)/num.hiv.phys

    prop.onart.young <- (num.onart.young.virt+num.onart.young.both+num.onart.young.phys)/num.hiv.young
    prop.onart.old <- (num.onart.old.virt+num.onart.old.both+num.onart.old.phys)/num.hiv.old
    prop.onart <- (num.onart.young.virt+num.onart.young.both+num.onart.young.phys+num.onart.old.virt+num.onart.old.both+num.onart.old.phys)/num.hiv.all
    

# Dropped out:
    prop.outsidecare.virt <- (num.outsidecare.young.virt+num.outsidecare.old.virt)/num.hiv.virt
    prop.outsidecare.both <- (num.outsidecare.young.both+num.outsidecare.old.both)/num.hiv.both
    prop.outsidecare.phys <- (num.outsidecare.young.phys+num.outsidecare.old.phys)/num.hiv.phys

    prop.outsidecare.young <- (num.outsidecare.young.virt+num.outsidecare.young.both+num.outsidecare.young.phys)/num.hiv.young
    prop.outsidecare.old <- (num.outsidecare.old.virt+num.outsidecare.old.both+num.outsidecare.old.phys)/num.hiv.old
    prop.outsidecare <- (num.outsidecare.young.virt+num.outsidecare.young.both+num.outsidecare.young.phys+num.outsidecare.old.virt+num.outsidecare.old.both+num.outsidecare.old.phys)/num.hiv.all
    

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
    
    outputs = list(t=t[steps], prev.all=prev.all[steps], prev.virt=prev.virt[steps], prev.both=prev.both[steps], prev.phys=prev.phys[steps], prev.young=prev.young[steps], prev.old=prev.old[steps],prop.unaware.virt=prop.unaware.virt[steps],prop.unaware.both=prop.unaware.both[steps],prop.unaware.phys=prop.unaware.phys[steps],prop.unaware.young=prop.unaware.young[steps],prop.unaware.old=prop.unaware.old[steps],prop.onart.virt=prop.onart.virt[steps],prop.onart.both=prop.onart.both[steps],prop.onart.phys=prop.onart.phys[steps],prop.onart.young=prop.onart.young[steps],prop.onart.old=prop.onart.old[steps],prop.outsidecare.virt=prop.outsidecare.virt[steps],prop.outsidecare.both=prop.outsidecare.both[steps],prop.outsidecare.phys=prop.outsidecare.phys[steps],prop.outsidecare.young=prop.outsidecare.young[steps],prop.outsidecare.old=prop.outsidecare.old[steps],prop.acute=prop.acute[steps],prop.chronic=prop.chronic[steps],prop.late=prop.late[steps],prop.virt=prop.virt[steps],prop.both=prop.both[steps],prop.phys=prop.phys[steps])

    
    

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



plot.something <- function(fits,county,resultsdir,plot.col,plot.type,graph.ymax)
{

    if(plot.type==1){
        y.axis.label <- "Overall prevalence (%)"
        ci.ul = baseline.data$p.all+baseline.data$width.all
        ci.ll = baseline.data$p.all-baseline.data$width.all
    }else if(plot.type==2){
        y.axis.label <- "Virtual MSM prevalence (%)"
        ci.ul = baseline.data$p.virt+baseline.data$width.virt
        ci.ll = baseline.data$p.virt-baseline.data$width.virt
    }else if(plot.type==3){
        y.axis.label <- "Dual MSM prevalence (%)"
        ci.ul = baseline.data$p.both+baseline.data$width.both
        ci.ll = baseline.data$p.both-baseline.data$width.both
    }else if(plot.type==4){
        y.axis.label <- "Physical MSM prevalence (%)"
        ci.ul = baseline.data$p.phys+baseline.data$width.phys
        ci.ll = baseline.data$p.phys-baseline.data$width.phys
    }else if(plot.type==5){
        y.axis.label <- "Prevalence in <25 yrs (%)"
        ci.ul = baseline.data$p.lt25+baseline.data$width.lt25
        ci.ll = baseline.data$p.lt25-baseline.data$width.lt25
    }else if(plot.type==6){
        y.axis.label <- "Prevalence in 25+ yrs (%)"
        ci.ul = baseline.data$p.25plus+baseline.data$width.25plus
        ci.ll = baseline.data$p.25plus-baseline.data$width.25plus
    }


    for (i in fits)
    {
        outputs = extract.data(resultsdir,county,i)
        t <- outputs$t+(2019.58-150) # Make 2019.58 (intervention start date t=150) August 2019.
        if(plot.type==1){
            prev = outputs$prev.all
        }else if(plot.type==2){
            prev = outputs$prev.virt
        }else if(plot.type==3){
            prev = outputs$prev.both
        }else if(plot.type==4){
            prev = outputs$prev.phys
       }else if(plot.type==5){
            prev = outputs$prev.young
       }else if(plot.type==6){
            prev = outputs$prev.old
       }
        
        if(i==fits[1]){
            plot(t,100*prev,col=plot.col,type="l",ylab=y.axis.label,xlab="",ylim=c(0,graph.ymax))
            arrows(t.baseline, ci.ul, t.baseline, ci.ll, angle=90, code=3, length=0.05)
        }else{
            lines(t,100*prev,col=plot.col)
        }
    }
    
}




new.plot.something <- function(t,data,county,plot.col,plot.type,graph.ymax)
{

    if(plot.type==1){
        y.axis.label <- "Overall prevalence (%)"
        ci.ul = baseline.data$p.all+baseline.data$width.all
        ci.ll = baseline.data$p.all-baseline.data$width.all
    }else if(plot.type==2){
        y.axis.label <- "Virtual MSM prevalence (%)"
        ci.ul = baseline.data$p.virt+baseline.data$width.virt
        ci.ll = baseline.data$p.virt-baseline.data$width.virt
    }else if(plot.type==3){
        y.axis.label <- "Dual MSM prevalence (%)"
        ci.ul = baseline.data$p.both+baseline.data$width.both
        ci.ll = baseline.data$p.both-baseline.data$width.both
    }else if(plot.type==4){
        y.axis.label <- "Physical MSM prevalence (%)"
        ci.ul = baseline.data$p.phys+baseline.data$width.phys
        ci.ll = baseline.data$p.phys-baseline.data$width.phys
    }else if(plot.type==5){
        y.axis.label <- "Prevalence in <25 yrs (%)"
        ci.ul = baseline.data$p.lt25+baseline.data$width.lt25
        ci.ll = baseline.data$p.lt25-baseline.data$width.lt25
    }else if(plot.type==6){
        y.axis.label <- "Prevalence in 25+ yrs (%)"
        ci.ul = baseline.data$p.25plus+baseline.data$width.25plus
        ci.ll = baseline.data$p.25plus-baseline.data$width.25plus
    }

    n.fits <- dim(data)[2]
    plot(t,100*data[,1],col=plot.col,type="l",ylab=y.axis.label,xlab="",ylim=c(0,graph.ymax))
    for (i in seq(2,n.fits))
    {
        lines(t,100*data[,i],col=plot.col)
    }
    arrows(t.baseline, ci.ul, t.baseline, ci.ll, angle=90, code=3, length=0.05)

}



#county <- "kiambu"
county <- "kisumu"
#county <- "mombasa"
resultsdir <- paste0("results_intervention/")



#fits <- scan(paste0(resultsdir,"list_",county,"_files.txt", what=numeric(), sep=""))
if(county=="kiambu"){
    fits <- seq(0,109)
    max.plots <- c(30,30,30,30,30,30)
}else if(county=="kisumu"){
    fits <- seq(0,99)
    max.plots <- c(15,30,15,10,5,30)
}else if(county=="mombasa"){
    fits <- seq(0,142)
    max.plots <- c(30,30,30,30,30,30)
}



baseline.data <- get.survey.data(county)
t.baseline <- 2019.35  # Mean date of baseline is 07 May 2019
t.endline <- 2020.78   # Mean date of endline is 13 Oct 2020 = 2020.78
type.col <- c("blue","red","green")






for (i in fits)
{    
    outputs = extract.data(resultsdir,county,i)
    prev.all = outputs$prev.all
    prev.virt = outputs$prev.virt
    prev.both = outputs$prev.both
    prev.phys = outputs$prev.phys
    prev.young = outputs$prev.young
    prev.old = outputs$prev.old

    prop.unaware.virt = outputs$prop.unaware.virt
    prop.unaware.both = outputs$prop.unaware.both
    prop.unaware.phys = outputs$prop.unaware.phys
    prop.unaware.old = outputs$prop.unaware.old
    prop.unaware.young = outputs$prop.unaware.young

    prop.onart.virt = outputs$prop.onart.virt
    prop.onart.both = outputs$prop.onart.both
    prop.onart.phys = outputs$prop.onart.phys
    prop.onart.old = outputs$prop.onart.old
    prop.onart.young = outputs$prop.onart.young

    prop.outsidecare.virt = outputs$prop.outsidecare.virt
    prop.outsidecare.both = outputs$prop.outsidecare.both
    prop.outsidecare.phys = outputs$prop.outsidecare.phys
    prop.outsidecare.old = outputs$prop.outsidecare.old
    prop.outsidecare.young = outputs$prop.outsidecare.young

    
    if(i==fits[1]){
        prev.all.store <- prev.all
        prev.virt.store <- prev.virt
        prev.both.store <- prev.both
        prev.phys.store <- prev.phys
        prev.young.store <- prev.young
        prev.old.store <- prev.old

        prop.unaware.virt.store <- prop.unaware.virt
        prop.unaware.both.store <- prop.unaware.both
        prop.unaware.phys.store <- prop.unaware.phys
        prop.unaware.old.store <- prop.unaware.old
        prop.unaware.young.store <- prop.unaware.young

        prop.onart.virt.store <- prop.onart.virt
        prop.onart.both.store <- prop.onart.both
        prop.onart.phys.store <- prop.onart.phys
        prop.onart.old.store <- prop.onart.old
        prop.onart.young.store <- prop.onart.young

        prop.outsidecare.virt.store <- prop.outsidecare.virt
        prop.outsidecare.both.store <- prop.outsidecare.both
        prop.outsidecare.phys.store <- prop.outsidecare.phys
        prop.outsidecare.old.store <- prop.outsidecare.old
        prop.outsidecare.young.store <- prop.outsidecare.young

        t <- outputs$t+(2019.58-150) # Make 2019.58 (intervention start date t=150) August 2019.

    }else{
        prev.all.store <- cbind(prev.all.store,prev.all)
        prev.virt.store <- cbind(prev.virt.store,prev.virt)
        prev.both.store <- cbind(prev.both.store,prev.both)
        prev.phys.store <- cbind(prev.phys.store,prev.phys)
        prev.young.store <- cbind(prev.young.store,prev.young)
        prev.old.store <- cbind(prev.old.store,prev.old)

        prop.unaware.virt.store <- cbind(prop.unaware.virt.store,prop.unaware.virt)
        prop.unaware.both.store <- cbind(prop.unaware.both.store,prop.unaware.both)
        prop.unaware.phys.store <- cbind(prop.unaware.phys.store,prop.unaware.phys)
        prop.unaware.old.store <- cbind(prop.unaware.old.store,prop.unaware.old)
        prop.unaware.young.store <- cbind(prop.unaware.young.store,prop.unaware.young)
        
        prop.onart.virt.store <- cbind(prop.onart.virt.store,prop.onart.virt)
        prop.onart.both.store <- cbind(prop.onart.both.store,prop.onart.both)
        prop.onart.phys.store <- cbind(prop.onart.phys.store,prop.onart.phys)
        prop.onart.old.store <- cbind(prop.onart.old.store,prop.onart.old)
        prop.onart.young.store <- cbind(prop.onart.young.store,prop.onart.young)
        
        prop.outsidecare.virt.store <- cbind(prop.outsidecare.virt.store,prop.outsidecare.virt)
        prop.outsidecare.both.store <- cbind(prop.outsidecare.both.store,prop.outsidecare.both)
        prop.outsidecare.phys.store <- cbind(prop.outsidecare.phys.store,prop.outsidecare.phys)
        prop.outsidecare.old.store <- cbind(prop.outsidecare.old.store,prop.outsidecare.old)
        prop.outsidecare.young.store <- cbind(prop.outsidecare.young.store,prop.outsidecare.young)
        

    }
}






j.overall <- 1
j.virt <- 2
j.both <- 3
j.phys <- 4
j.young <- 5
j.old <- 6


pdf(paste0("bestfits_",county,"_overall.pdf"))

max.plots <- c(30,30,30,30,30,30)
par(mfrow=c(2,3))
new.plot.something(t,prev.all.store,county,"blue",j.overall,max.plots[j.overall])
new.plot.something(t,prev.young.store,county,"blue",j.young,max.plots[j.young])
new.plot.something(t,prev.old.store,county,"blue",j.old,max.plots[j.old])

new.plot.something(t,prev.virt.store,county,"blue",j.virt,max.plots[j.virt])
new.plot.something(t,prev.both.store,county,"blue",j.both,max.plots[j.both])
new.plot.something(t,prev.phys.store,county,"blue",j.phys,max.plots[j.phys])

dev.off()




#plot.something(fits,county,resultsdir,"blue",j.overall,max.plots[j.overall])
#plot.something(fits,county,resultsdir,"blue",j.virt,max.plots[j.virt])


# Put together the data from each run into data stores of the same type:

# By typology:
#pdf(paste0("bestfits_",county,"_bytype.pdf"))
#par(mfrow=c(1,3))
#dev.off()

###################
# By age:
##################

#pdf(paste0("bestfits_",county,"_byage.pdf"))
#par(mfrow=c(1,2))
#dev.off()


















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
    t <- outputs$t+(2019.58-150) # Make 2019.58 (intervention start date t=150) August 2019.
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


