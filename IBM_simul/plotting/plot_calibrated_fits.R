


rm(list=ls())

require(Hmisc)

library(RColorBrewer)

library(colorspace)
library(stringr)


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

    # Cumulative incident infections:
    i.inc.young.virt <- 122
    i.inc.old.virt <- 123
    i.inc.young.both <- 124
    i.inc.old.both <- 125
    i.inc.young.phys <- 126
    i.inc.old.phys <- 127

    i.susc.young.virt <- 2
    i.susc.old.virt <- 3
    i.susc.young.both <- 4
    i.susc.old.both <- 5
    i.susc.young.phys <- 6
    i.susc.old.phys <- 7
    

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


    # Cumulative incident infections:
    cum.inc.young.virt <- run.data[,i.inc.young.virt]
    cum.inc.old.virt <- run.data[,i.inc.old.virt]
    cum.inc.young.both <- run.data[,i.inc.young.both]
    cum.inc.old.both <- run.data[,i.inc.old.both]
    cum.inc.young.phys <- run.data[,i.inc.young.phys]
    cum.inc.old.phys <- run.data[,i.inc.old.phys]

    n.susc.young.virt <- run.data[,i.susc.young.virt]
    n.susc.old.virt <- run.data[,i.susc.old.virt]
    n.susc.young.both <- run.data[,i.susc.young.both]
    n.susc.old.both <- run.data[,i.susc.old.both]
    n.susc.young.phys <- run.data[,i.susc.young.phys]
    n.susc.old.phys <- run.data[,i.susc.old.phys]



    

    
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
    prop.unaware <- (num.unaware.young.virt+num.unaware.young.both+num.unaware.young.phys+num.unaware.old.virt+num.unaware.old.both+num.unaware.old.phys)/num.hiv.all
        
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
    
    
    # Compare this to self-report know HIV+ from PBS (note we won't compare by typology as PBS doesn't have a "dual" type):
    pbs.comparison.aware <- (num.onart.young.virt+num.outsidecare.young.virt + num.onart.old.virt+num.outsidecare.old.virt + num.onart.young.both+num.outsidecare.young.both + num.onart.old.both+num.outsidecare.old.both + num.onart.young.phys+num.outsidecare.young.phys)/denom.hiv.all
    
    
    # Only use every step.size
    step.size <- 10
    n.steps <- length(t)
    steps <- seq(1,n.steps,step.size)
    if(tail(steps,1)!=n.steps)
        steps <- c(steps,n.steps)


    
    outputs = list(t=t[steps], prev.all=prev.all[steps], prev.virt=prev.virt[steps], prev.both=prev.both[steps], prev.phys=prev.phys[steps], prev.young=prev.young[steps], prev.old=prev.old[steps],
                   prop.unaware=prop.unaware[steps],prop.unaware.virt=prop.unaware.virt[steps],prop.unaware.both=prop.unaware.both[steps],prop.unaware.phys=prop.unaware.phys[steps],prop.unaware.young=prop.unaware.young[steps],prop.unaware.old=prop.unaware.old[steps],
                   prop.onart=prop.onart[steps],prop.onart.virt=prop.onart.virt[steps],prop.onart.both=prop.onart.both[steps],prop.onart.phys=prop.onart.phys[steps],prop.onart.young=prop.onart.young[steps],prop.onart.old=prop.onart.old[steps],
                   prop.outsidecare=prop.outsidecare[steps],prop.outsidecare.virt=prop.outsidecare.virt[steps],prop.outsidecare.both=prop.outsidecare.both[steps],prop.outsidecare.phys=prop.outsidecare.phys[steps],prop.outsidecare.young=prop.outsidecare.young[steps],prop.outsidecare.old=prop.outsidecare.old[steps],
                   prop.acute=prop.acute[steps],prop.chronic=prop.chronic[steps],prop.late=prop.late[steps],prop.virt=prop.virt[steps],prop.both=prop.both[steps],prop.phys=prop.phys[steps],
                   cum.inc.young.virt=cum.inc.young.virt[steps],cum.inc.old.virt=cum.inc.old.virt[steps],cum.inc.young.both=cum.inc.young.both[steps],cum.inc.old.both=cum.inc.old.both[steps],cum.inc.young.phys=cum.inc.young.phys[steps],cum.inc.old.phys=cum.inc.old.phys[steps],
                   n.susc.young.virt=n.susc.young.virt[steps],n.susc.old.virt=n.susc.old.virt[steps],n.susc.young.both=n.susc.young.both[steps],n.susc.old.both=n.susc.old.both[steps],n.susc.young.phys=n.susc.young.phys[steps],n.susc.old.phys=n.susc.old.phys[steps],
                   pbs.comparison.aware=pbs.comparison.aware[steps])

    
    

    return(outputs)

}




# round is "baseline" or "endline"
get.survey.data <- function(county,round)
{
    survey.data.file <- file(paste0("~/Dropbox (SPH Imperial College)/projects/Kenya_MSM_HIVST/Analysis/",county,"_",round,"_data.txt"),open="r")
    readLines(survey.data.file,1)
                                        # [1] "HIV prevalence by age gp"
    readLines(survey.data.file,1)
                                        # [1] "\"<25\" \"25+\""
    l <- readLines(survey.data.file,1)
    neg.lt25 <- as.numeric(sapply(strsplit(l," "),"[[",2))
    neg.25plus <- as.numeric(sapply(strsplit(l," "),"[[",3))
    l <- readLines(survey.data.file,1)
    pos.lt25 <- as.numeric(sapply(strsplit(l," "),"[[",2))
    pos.25plus <- as.numeric(sapply(strsplit(l," "),"[[",3))
    readLines(survey.data.file,1)
    ## HIV prevalence by place find partner
    readLines(survey.data.file,1)
    ## "Virtual" "Both" "Physical"
    l <- readLines(survey.data.file,1)
    neg.virt <- as.numeric(sapply(strsplit(l," "),"[[",2))
    neg.both <- as.numeric(sapply(strsplit(l," "),"[[",3))
    neg.phys <- as.numeric(sapply(strsplit(l," "),"[[",4))
    l <- readLines(survey.data.file,1)
    pos.virt <- as.numeric(sapply(strsplit(l," "),"[[",2))
    pos.both <- as.numeric(sapply(strsplit(l," "),"[[",3))
    pos.phys <- as.numeric(sapply(strsplit(l," "),"[[",4))
    readLines(survey.data.file,1)
    ## Aware of status
    readLines(survey.data.file,1)
    ## "x"
    l <- readLines(survey.data.file,1)
    n.unaware <- as.numeric(sapply(strsplit(l," "),"[[",2))
    l <- readLines(survey.data.file,1)
    n.aware <- as.numeric(sapply(strsplit(l," "),"[[",2))
    close(survey.data.file)

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



## plot.something <- function(fits,county,resultsdir,plot.col,plot.type,graph.ymax)
## {

##     if(plot.type==1){
##         y.axis.label <- "Overall prevalence (%)"
##         ci.ul = baseline.data$p.all+baseline.data$width.all
##         ci.ll = baseline.data$p.all-baseline.data$width.all
##     }else if(plot.type==2){
##         y.axis.label <- "Virtual MSM prevalence (%)"
##         ci.ul = baseline.data$p.virt+baseline.data$width.virt
##         ci.ll = baseline.data$p.virt-baseline.data$width.virt
##     }else if(plot.type==3){
##         y.axis.label <- "Dual MSM prevalence (%)"
##         ci.ul = baseline.data$p.both+baseline.data$width.both
##         ci.ll = baseline.data$p.both-baseline.data$width.both
##     }else if(plot.type==4){
##         y.axis.label <- "Physical MSM prevalence (%)"
##         ci.ul = baseline.data$p.phys+baseline.data$width.phys
##         ci.ll = baseline.data$p.phys-baseline.data$width.phys
##     }else if(plot.type==5){
##         y.axis.label <- "Prevalence in <25 yrs (%)"
##         ci.ul = baseline.data$p.lt25+baseline.data$width.lt25
##         ci.ll = baseline.data$p.lt25-baseline.data$width.lt25
##     }else if(plot.type==6){
##         y.axis.label <- "Prevalence in 25+ yrs (%)"
##         ci.ul = baseline.data$p.25plus+baseline.data$width.25plus
##         ci.ll = baseline.data$p.25plus-baseline.data$width.25plus
##     }


##     for (i in fits)
##     {
##         outputs = extract.data(resultsdir,county,i)
##         t <- outputs$t+(2019.58-150) # Make 2019.58 (intervention start date t=150) August 2019.
##         if(plot.type==1){
##             prev = outputs$prev.all
##         }else if(plot.type==2){
##             prev = outputs$prev.virt
##         }else if(plot.type==3){
##             prev = outputs$prev.both
##         }else if(plot.type==4){
##             prev = outputs$prev.phys
##        }else if(plot.type==5){
##             prev = outputs$prev.young
##        }else if(plot.type==6){
##             prev = outputs$prev.old
##        }
        
##         if(i==fits[1]){
##             plot(t,100*prev,col=plot.col,type="l",ylab=y.axis.label,xlab="",ylim=c(0,graph.ymax))
##             arrows(t.baseline, ci.ul, t.baseline, ci.ll, angle=90, code=3, length=0.05)
##         }else{
##             lines(t,100*prev,col=plot.col)
##         }
##     }
    
## }




plot.prevalence <- function(t,data,county,plot.col,plot.type,graph.ymax,graph.xrange,baseline.data)
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
    plot(t,100*data[,1],col=plot.col,type="l",ylab=y.axis.label,xlab="",ylim=c(0,graph.ymax),xlim=graph.xrange)
    for (i in seq(2,n.fits))
    {
        lines(t,100*data[,i],col=plot.col)
    }
    arrows(t.baseline, ci.ul, t.baseline, ci.ll, angle=90, code=3, length=0.05,lwd=1.5)

}



############

plot.prevalence.base.end <- function(t,data,county,plot.col,plot.type,graph.ymax,graph.xrange,county.baseline,county.endline)
{

    if(plot.type==1){
        y.axis.label <- "Overall prevalence (%)"
        ci.baseline.ul = county.baseline$p.all+county.baseline$width.all
        ci.baseline.ll = county.baseline$p.all-county.baseline$width.all
        ci.endline.ul = county.endline$p.all+county.endline$width.all
        ci.endline.ll = county.endline$p.all-county.endline$width.all
    }else if(plot.type==2){
        y.axis.label <- "Virtual MSM prevalence (%)"
        ci.baseline.ul = county.baseline$p.virt+county.baseline$width.virt
        ci.baseline.ll = county.baseline$p.virt-county.baseline$width.virt
        ci.endline.ul = county.endline$p.virt+county.endline$width.virt
        ci.endline.ll = county.endline$p.virt-county.endline$width.virt
    }else if(plot.type==3){
        y.axis.label <- "Dual MSM prevalence (%)"
        ci.baseline.ul = county.baseline$p.both+county.baseline$width.both
        ci.baseline.ll = county.baseline$p.both-county.baseline$width.both
        ci.endline.ul = county.endline$p.both+county.endline$width.both
        ci.endline.ll = county.endline$p.both-county.endline$width.both
    }else if(plot.type==4){
        y.axis.label <- "Physical MSM prevalence (%)"
        ci.baseline.ul = county.baseline$p.phys+county.baseline$width.phys
        ci.baseline.ll = county.baseline$p.phys-county.baseline$width.phys
        ci.endline.ul = county.endline$p.phys+county.endline$width.phys
        ci.endline.ll = county.endline$p.phys-county.endline$width.phys
    }else if(plot.type==5){
        y.axis.label <- "Prevalence in <25 yrs (%)"
        ci.baseline.ul = county.baseline$p.lt25+county.baseline$width.lt25
        ci.baseline.ll = county.baseline$p.lt25-county.baseline$width.lt25
        ci.endline.ul = county.endline$p.lt25+county.endline$width.lt25
        ci.endline.ll = county.endline$p.lt25-county.endline$width.lt25
    }else if(plot.type==6){
        y.axis.label <- "Prevalence in 25+ yrs (%)"
        ci.baseline.ul = county.baseline$p.25plus+county.baseline$width.25plus
        ci.baseline.ll = county.baseline$p.25plus-county.baseline$width.25plus
        ci.endline.ul = county.endline$p.25plus+county.endline$width.25plus
        ci.endline.ll = county.endline$p.25plus-county.endline$width.25plus
    }

    n.fits <- dim(data)[2]
    plot(t,100*data[,1],col=plot.col,type="l",ylab=y.axis.label,xlab="",ylim=c(0,graph.ymax),xlim=graph.xrange,cex.lab=1.5,cex.axis=1.2)
    for (i in seq(2,n.fits))
    {
        lines(t,100*data[,i],col=plot.col)
    }
    arrows(t.baseline, ci.baseline.ul, t.baseline, ci.baseline.ll, angle=90, code=3, length=0.05,lwd=1.5)
    arrows(t.endline, ci.endline.ul, t.endline, ci.endline.ll, angle=90, code=3, length=0.05,lwd=1.5)

}



# To plot time trends of multiple runs without any CI:
plot.general <- function(t,data,county,plot.col,graph.xrange,graph.ymax,y.axis.label)
{

    n.fits <- dim(data)[2]
    plot(t,100*data[,1],col=plot.col,type="l",ylab=y.axis.label,xlab="",xlim=graph.xrange,ylim=c(0,graph.ymax))
    for (i in seq(2,n.fits))
    {
        lines(t,100*data[,i],col=plot.col)
    }
}


calculate.incident.infections <- function(cumulative.incident.infections)
{
    incident.infections <-tail(cumulative.incident.infections,-1) - head(cumulative.incident.infections,-1)
    incident.infections <- c(incident.infections,tail(incident.infections,1))
    return(incident.infections)
}


get.data.as.list <- function(resultsdir,county, nruns)
{

    for (i in seq(0,nruns))
    {
    
        outputs = extract.data(resultsdir,county,i)
        prev.all = outputs$prev.all
        prev.virt = outputs$prev.virt
        prev.both = outputs$prev.both
        prev.phys = outputs$prev.phys
        prev.young = outputs$prev.young
        prev.old = outputs$prev.old
        
        prop.unaware = outputs$prop.unaware
        prop.unaware.virt = outputs$prop.unaware.virt
        prop.unaware.both = outputs$prop.unaware.both
        prop.unaware.phys = outputs$prop.unaware.phys
        prop.unaware.old = outputs$prop.unaware.old
        prop.unaware.young = outputs$prop.unaware.young
        
        prop.onart = outputs$prop.onart
        prop.onart.virt = outputs$prop.onart.virt
        prop.onart.both = outputs$prop.onart.both
        prop.onart.phys = outputs$prop.onart.phys
        prop.onart.old = outputs$prop.onart.old
        prop.onart.young = outputs$prop.onart.young
        
        prop.outsidecare = outputs$prop.outsidecare
        prop.outsidecare.virt = outputs$prop.outsidecare.virt
        prop.outsidecare.both = outputs$prop.outsidecare.both
        prop.outsidecare.phys = outputs$prop.outsidecare.phys
        prop.outsidecare.old = outputs$prop.outsidecare.old
        prop.outsidecare.young = outputs$prop.outsidecare.young

        prop.acute=outputs$prop.acute
        prop.virt=outputs$prop.virt
        prop.both=outputs$prop.both
        prop.phys=outputs$prop.phys
        
        pbs.comparison.aware = outputs$pbs.comparison.aware

                                        # Calculate incidence:
        incident.infections.per.timestep.young.virt <-calculate.incident.infections(outputs$cum.inc.young.virt)
        incident.infections.per.timestep.old.virt <-calculate.incident.infections(outputs$cum.inc.old.virt)
        incident.infections.per.timestep.young.both <-calculate.incident.infections(outputs$cum.inc.young.both)
        incident.infections.per.timestep.old.both <-calculate.incident.infections(outputs$cum.inc.old.both)
        incident.infections.per.timestep.young.phys <-calculate.incident.infections(outputs$cum.inc.young.phys)
        incident.infections.per.timestep.old.phys <-calculate.incident.infections(outputs$cum.inc.old.phys)

        timestep <- calculate.incident.infections(outputs$t)
        
        incidence.young.virt <- 100*incident.infections.per.timestep.young.virt/(timestep*outputs$n.susc.young.virt)
        incidence.old.virt <- 100*incident.infections.per.timestep.old.virt/(timestep*outputs$n.susc.old.virt)
        incidence.young.both <- 100*incident.infections.per.timestep.young.both/(timestep*outputs$n.susc.young.both)
        incidence.old.both <- 100*incident.infections.per.timestep.old.both/(timestep*outputs$n.susc.old.both)
        incidence.young.phys <- 100*incident.infections.per.timestep.young.phys/(timestep*outputs$n.susc.young.phys)
        incidence.old.phys <- 100*incident.infections.per.timestep.old.phys/(timestep*outputs$n.susc.old.phys)

        incidence.young <- 100*(incident.infections.per.timestep.young.virt+incident.infections.per.timestep.young.both+incident.infections.per.timestep.young.phys)/(timestep*(outputs$n.susc.young.virt+outputs$n.susc.young.both+outputs$n.susc.young.phys))
        incidence.old <- 100*(incident.infections.per.timestep.old.virt+incident.infections.per.timestep.old.both+incident.infections.per.timestep.old.phys)/(timestep*(outputs$n.susc.old.virt+outputs$n.susc.old.both+outputs$n.susc.old.phys))

        incidence.virt <- 100*(incident.infections.per.timestep.young.virt+incident.infections.per.timestep.old.virt)/(timestep*(outputs$n.susc.young.virt+outputs$n.susc.old.virt))
        incidence.both <- 100*(incident.infections.per.timestep.young.both+incident.infections.per.timestep.old.both)/(timestep*(outputs$n.susc.young.both+outputs$n.susc.old.both))
        incidence.phys <- 100*(incident.infections.per.timestep.young.phys+incident.infections.per.timestep.old.phys)/(timestep*(outputs$n.susc.young.phys+outputs$n.susc.old.phys))
        

        incidence <- 100*(incident.infections.per.timestep.young.virt+incident.infections.per.timestep.young.both+incident.infections.per.timestep.young.phys + incident.infections.per.timestep.old.virt+incident.infections.per.timestep.old.both+incident.infections.per.timestep.old.phys)/(timestep*(outputs$n.susc.young.virt+outputs$n.susc.young.both+outputs$n.susc.young.phys+outputs$n.susc.old.virt+outputs$n.susc.old.both+outputs$n.susc.old.phys))

        
        
        
        if(i==0){
            prev.all.store <- prev.all
            prev.virt.store <- prev.virt
            prev.both.store <- prev.both
            prev.phys.store <- prev.phys
            prev.young.store <- prev.young
            prev.old.store <- prev.old
            
            prop.unaware.store <- prop.unaware
            prop.unaware.virt.store <- prop.unaware.virt
            prop.unaware.both.store <- prop.unaware.both
            prop.unaware.phys.store <- prop.unaware.phys
            prop.unaware.old.store <- prop.unaware.old
            prop.unaware.young.store <- prop.unaware.young
            
            prop.onart.store <- prop.onart
            prop.onart.virt.store <- prop.onart.virt
            prop.onart.both.store <- prop.onart.both
            prop.onart.phys.store <- prop.onart.phys
            prop.onart.old.store <- prop.onart.old
            prop.onart.young.store <- prop.onart.young
            
            prop.outsidecare.store <- prop.outsidecare
            prop.outsidecare.virt.store <- prop.outsidecare.virt
            prop.outsidecare.both.store <- prop.outsidecare.both
            prop.outsidecare.phys.store <- prop.outsidecare.phys
            prop.outsidecare.old.store <- prop.outsidecare.old
            prop.outsidecare.young.store <- prop.outsidecare.young


            incidence.young.virt.store <- incidence.young.virt
            incidence.old.virt.store <- incidence.old.virt
            incidence.young.both.store <- incidence.young.both
            incidence.old.both.store <- incidence.old.both
            incidence.young.phys.store <- incidence.young.phys
            incidence.old.phys.store <- incidence.old.phys
            
            incidence.young.store <- incidence.young
            incidence.old.store <- incidence.old
            
            incidence.virt.store <- incidence.virt
            incidence.both.store <- incidence.both
            incidence.phys.store <- incidence.phys

            incidence.store <- incidence

            prop.acute.store <- prop.acute
            prop.virt.store <- prop.virt
            prop.both.store <- prop.both
            prop.phys.store <- prop.phys
            
            
            pbs.comparison.aware.store <- pbs.comparison.aware
            
            t <- outputs$t+(2019.58-150) # Make 2019.58 (intervention start date t=150) August 2019.
            
        }else{
            prev.all.store <- cbind(prev.all.store,prev.all)
            prev.virt.store <- cbind(prev.virt.store,prev.virt)
            prev.both.store <- cbind(prev.both.store,prev.both)
            prev.phys.store <- cbind(prev.phys.store,prev.phys)
            prev.young.store <- cbind(prev.young.store,prev.young)
            prev.old.store <- cbind(prev.old.store,prev.old)
            
            prop.unaware.store <- cbind(prop.unaware.store,prop.unaware)
            prop.unaware.virt.store <- cbind(prop.unaware.virt.store,prop.unaware.virt)            
            prop.unaware.both.store <- cbind(prop.unaware.both.store,prop.unaware.both)
            prop.unaware.phys.store <- cbind(prop.unaware.phys.store,prop.unaware.phys)
            prop.unaware.old.store <- cbind(prop.unaware.old.store,prop.unaware.old)
            prop.unaware.young.store <- cbind(prop.unaware.young.store,prop.unaware.young)
            
            prop.onart.store <- cbind(prop.onart.store,prop.onart)
            prop.onart.virt.store <- cbind(prop.onart.virt.store,prop.onart.virt)
            prop.onart.both.store <- cbind(prop.onart.both.store,prop.onart.both)
            prop.onart.phys.store <- cbind(prop.onart.phys.store,prop.onart.phys)
            prop.onart.old.store <- cbind(prop.onart.old.store,prop.onart.old)
            prop.onart.young.store <- cbind(prop.onart.young.store,prop.onart.young)
            
            prop.outsidecare.store <- cbind(prop.outsidecare.store,prop.outsidecare)
            prop.outsidecare.virt.store <- cbind(prop.outsidecare.virt.store,prop.outsidecare.virt)
            prop.outsidecare.both.store <- cbind(prop.outsidecare.both.store,prop.outsidecare.both)
            prop.outsidecare.phys.store <- cbind(prop.outsidecare.phys.store,prop.outsidecare.phys)
            prop.outsidecare.old.store <- cbind(prop.outsidecare.old.store,prop.outsidecare.old)
            prop.outsidecare.young.store <- cbind(prop.outsidecare.young.store,prop.outsidecare.young)


            incidence.young.virt.store <- cbind(incidence.young.virt.store,incidence.young.virt)
            incidence.old.virt.store <- cbind(incidence.old.virt.store,incidence.old.virt)
            incidence.young.both.store <- cbind(incidence.young.both.store,incidence.young.both)
            incidence.old.both.store <- cbind(incidence.old.both.store,incidence.old.both)
            incidence.young.phys.store <- cbind(incidence.young.phys.store,incidence.young.phys)
            incidence.old.phys.store <- cbind(incidence.old.phys.store,incidence.old.phys)

            
            incidence.young.store <- cbind(incidence.young.store,incidence.young)
            incidence.old.store <- cbind(incidence.old.store,incidence.old)
            
            incidence.virt.store <- cbind(incidence.virt.store,incidence.virt)
            incidence.both.store <- cbind(incidence.both.store,incidence.both)
            incidence.phys.store <- cbind(incidence.phys.store,incidence.phys)

            incidence.store <- cbind(incidence.store,incidence)

            prop.acute.store <- cbind(prop.acute.store,prop.acute)
            prop.virt.store <- cbind(prop.virt.store,prop.virt)
            prop.both.store <- cbind(prop.both.store,prop.both)
            prop.phys.store <- cbind(prop.phys.store,prop.phys)

            
            pbs.comparison.aware.store <- cbind(pbs.comparison.aware.store,pbs.comparison.aware)

        }
    
    }

    data.store <- list(t=t, prev.all.store=prev.all.store, prev.virt.store=prev.virt.store, prev.both.store=prev.both.store, prev.phys.store=prev.phys.store, prev.young.store=prev.young.store, prev.old.store=prev.old.store,
                       prop.unaware.store=prop.unaware.store,prop.unaware.virt.store=prop.unaware.virt.store,prop.unaware.both.store=prop.unaware.both.store,prop.unaware.phys.store=prop.unaware.phys.store,prop.unaware.old.store=prop.unaware.old.store,prop.unaware.young.store=prop.unaware.young.store,
                       prop.onart.store=prop.onart.store,prop.onart.virt.store=prop.onart.virt.store,prop.onart.both.store=prop.onart.both.store,prop.onart.phys.store=prop.onart.phys.store,prop.onart.old.store=prop.onart.old.store,prop.onart.young.store=prop.onart.young.store,
                       prop.outsidecare.store=prop.outsidecare.store,prop.outsidecare.virt.store=prop.outsidecare.virt.store,prop.outsidecare.both.store=prop.outsidecare.both.store,prop.outsidecare.phys.store=prop.outsidecare.phys.store,prop.outsidecare.old.store=prop.outsidecare.old.store,prop.outsidecare.young.store=prop.outsidecare.young.store,
                       incidence.young.virt.store=incidence.young.virt.store,incidence.old.virt.store=incidence.old.virt.store,incidence.young.both.store=incidence.young.both.store,incidence.old.both.store=incidence.old.both.store,incidence.young.phys.store=incidence.young.phys.store,incidence.old.phys.store=incidence.old.phys.store,incidence.young.store=incidence.young.store,incidence.old.store=incidence.old.store,incidence.virt.store=incidence.virt.store,incidence.both.store=incidence.both.store,incidence.phys.store=incidence.phys.store,incidence.store=incidence.store,
                       prop.acute.store=prop.acute.store,prop.virt.store=prop.virt.store,prop.both.store=prop.both.store,prop.phys.store=prop.phys.store,
                       pbs.comparison.aware.store=pbs.comparison.aware.store)

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



plot.int.count.opt <- function(t.int,t.count,t.opt,intervention.data,counterfactual.data,optimal.data,lq,uq,x.range,y.range,plot.filename,plot.legend,plot.title,y.axis.label)
{

    if(!is.na(plot.filename)){
        pdf(plot.filename)
    }
        
    plot.polygon(t=t.int,
                 ylowerpolygon=apply(intervention.data,1,quantile,lq),
                 yupperpolygon=apply(intervention.data,1,quantile,uq),
                 ymean=rowMeans(intervention.data),
                 ylowerdotted=NA,
                 yupperdotted=NA,
                 polygon.col=polygon.cols[1],lines.col=lines.cols[1],firstpolygon=1,x.range=x.range,y.range=y.range,plot.title=plot.title,y.axis.label=y.axis.label)
    

    plot.polygon(t=t.count,
                 ylowerpolygon=apply(counterfactual.data,1,quantile,lq),
                 yupperpolygon=apply(counterfactual.data,1,quantile,uq),
                 ymean=rowMeans(counterfactual.data),
                 ylowerdotted=NA,
                 yupperdotted=NA,
                 polygon.col=polygon.cols[2],lines.col=lines.cols[2],firstpolygon=0,x.range=x.range,y.range=y.range,plot.title=NA,y.axis.label=NA)
    
    plot.polygon(t=t.opt,
                 ylowerpolygon=apply(optimal.data,1,quantile,lq),
                 yupperpolygon=apply(optimal.data,1,quantile,uq),
                 ymean=rowMeans(optimal.data),
                 ylowerdotted=NA,
                 yupperdotted=NA,
                 polygon.col=polygon.cols[3],lines.col=lines.cols[3],firstpolygon=0,x.range=x.range,y.range=y.range,plot.title=NA,y.axis.label=NA)

    if(plot.legend==1)
    {
        legend("topleft",col=polygon.cols,legend=c("HIV ST scenario","Counterfactual scenario","Optimal scenario"),lty=1,lwd=4,bty="n",cex=1.1)
    }
    
    if(!is.na(plot.filename)){
        dev.off()
    }

}


calibration.plot.since.start <- function(county,plot.data,max.plots,baseline.data)
{

    if(county=="kiambu"){
        plot.col <- "gray80"
    }else if(county=="kisumu"){
        plot.col <- brewer.pal(n = 9, name = "Blues")[4]
    }else if(county=="mombasa"){
        plot.col <- brewer.pal(n = 9, name = "Oranges")[2]
    }
    print(county)
    plot.xrange <- c(min(plot.data$t),t.baseline+10)



    par(mfrow=c(2,3))
                                        #plot.prevalence(t,prev.all.store,county,plot.col,j.overall,max.plots[j.overall])


    plot.prevalence(plot.data$t,plot.data$prev.all.store,county,plot.col,j.overall,max.plots[j.overall],plot.xrange,baseline.data)
    plot.prevalence(plot.data$t,plot.data$prev.young.store,county,plot.col,j.young,max.plots[j.young],plot.xrange,baseline.data)
    plot.prevalence(plot.data$t,plot.data$prev.old.store,county,plot.col,j.old,max.plots[j.old],plot.xrange,baseline.data)
    plot.prevalence(plot.data$t,plot.data$prev.virt.store,county,plot.col,j.virt,max.plots[j.virt],plot.xrange,baseline.data)
    plot.prevalence(plot.data$t,plot.data$prev.both.store,county,plot.col,j.both,max.plots[j.both],plot.xrange,baseline.data)
    plot.prevalence(plot.data$t,plot.data$prev.phys.store,county,plot.col,j.phys,max.plots[j.phys],plot.xrange,baseline.data)
    mtext(str_to_title(county), side = 3, line = -3, outer = TRUE)
}


calibration.plot.art.trend <- function(county,plot.data,baseline.endline.range)
{
    if(county=="kiambu"){
        plot.col <- "gray80"
    }else if(county=="kisumu"){
        plot.col <- brewer.pal(n = 9, name = "Blues")[4]
    }else if(county=="mombasa"){
        plot.col <- brewer.pal(n = 9, name = "Oranges")[2]
    }
    par(mfrow=c(2,3))
    plot.general(plot.data$t,plot.data$prop.onart.store,county,plot.col,baseline.endline.range,100,"% on ART overall")
    plot.general(plot.data$t,plot.data$prop.onart.young.store,county,plot.col,baseline.endline.range,100,"% of <25 year olds on ART")
    plot.general(plot.data$t,plot.data$prop.onart.old.store,county,plot.col,baseline.endline.range,100,"% of 25+ year olds on ART")
    plot.general(plot.data$t,plot.data$prop.onart.virt.store,county,plot.col,baseline.endline.range,100,"% of virtual MSM on ART")
    plot.general(plot.data$t,plot.data$prop.onart.both.store,county,plot.col,baseline.endline.range,100,"% of dual MSM on ART")
    plot.general(plot.data$t,plot.data$prop.onart.phys.store,county,plot.col,baseline.endline.range,100,"% of physical MSM on ART")
}


calibration.plot.outsidecare.trend <- function(county,plot.data)
{
    if(county=="kiambu"){
        plot.col <- "gray80"
    }else if(county=="kisumu"){
        plot.col <- brewer.pal(n = 9, name = "Blues")[4]
    }else if(county=="mombasa"){
        plot.col <- brewer.pal(n = 9, name = "Oranges")[2]
    }
    par(mfrow=c(2,3))
    plot.general(plot.data$t,plot.data$prop.outsidecare.store,county,plot.col,baseline.endline.range,15,"% outside care overall")
    plot.general(plot.data$t,plot.data$prop.outsidecare.young.store,county,plot.col,baseline.endline.range,15,"% of <25 year olds outside care")
    plot.general(plot.data$t,plot.data$prop.outsidecare.old.store,county,plot.col,baseline.endline.range,15,"% of 25+ year olds outside care")
    plot.general(plot.data$t,plot.data$prop.outsidecare.virt.store,county,plot.col,baseline.endline.range,15,"% of virtual MSM outside care")
    plot.general(plot.data$t,plot.data$prop.outsidecare.both.store,county,plot.col,baseline.endline.range,15,"% of dual MSM outside care")
    plot.general(plot.data$t,plot.data$prop.outsidecare.phys.store,county,plot.col,baseline.endline.range,15,"% of physical MSM outside care")

}


calibration.plot.unaware.trend <- function(county,plot.data)
{
    if(county=="kiambu"){
        plot.col <- "gray80"
    }else if(county=="kisumu"){
        plot.col <- brewer.pal(n = 9, name = "Blues")[4]
    }else if(county=="mombasa"){
        plot.col <- brewer.pal(n = 9, name = "Oranges")[2]
    }

    par(mfrow=c(2,3))
    plot.general(plot.data$t,plot.data$prop.unaware.store,county,plot.col,baseline.endline.range,30,"% PLHIV unaware overall")
    plot.general(plot.data$t,plot.data$prop.unaware.young.store,county,plot.col,baseline.endline.range,40,"% of <25 year olds PLHIV unaware")
    plot.general(plot.data$t,plot.data$prop.unaware.old.store,county,plot.col,baseline.endline.range,40,"% of 25+ year olds PLHIV unaware")
    plot.general(plot.data$t,plot.data$prop.unaware.virt.store,county,plot.col,baseline.endline.range,30,"% of virtual MSM PLHIV unaware")
    plot.general(plot.data$t,plot.data$prop.unaware.both.store,county,plot.col,baseline.endline.range,30,"% of dual MSM PLHIV unaware")
    plot.general(plot.data$t,plot.data$prop.unaware.phys.store,county,plot.col,baseline.endline.range,30,"% of physical PLHIV unaware")
    
}

plot.calibration.base.end <- function(county,plot.data,baseline.data,endline.data,y.lims)
{
    
    if(county=="kiambu"){
        plot.col <- "gray80"
    }else if(county=="kisumu"){
        plot.col <- brewer.pal(n = 9, name = "Blues")[4]
    }else if(county=="mombasa"){
        plot.col <- brewer.pal(n = 9, name = "Oranges")[2]
    }

    plot.xrange.base.end <- c(t.baseline-1,t.baseline+10)
    par(mfrow=c(2,3))
    plot.prevalence.base.end(plot.data$t,plot.data$prev.all.store,county,plot.col,j.overall,y.lims[1],plot.xrange.base.end,baseline.data,endline.data)
    plot.prevalence.base.end(plot.data$t,plot.data$prev.young.store,county,plot.col,j.young,y.lims[2],plot.xrange.base.end,baseline.data,endline.data)
    plot.prevalence.base.end(plot.data$t,plot.data$prev.old.store,county,plot.col,j.old,y.lims[3],plot.xrange.base.end,baseline.data,endline.data)
    plot.prevalence.base.end(plot.data$t,plot.data$prev.virt.store,county,plot.col,j.virt,y.lims[4],plot.xrange.base.end,baseline.data,endline.data)
    plot.prevalence.base.end(plot.data$t,plot.data$prev.both.store,county,plot.col,j.both,y.lims[5],plot.xrange.base.end,baseline.data,endline.data)
    plot.prevalence.base.end(plot.data$t,plot.data$prev.phys.store,county,plot.col,j.phys,y.lims[6],plot.xrange.base.end,baseline.data,endline.data)
}


plot.calibration.base.end.all <- function(county,plot.data,baseline.data,endline.data,y.lims)
{
    
    if(county=="kiambu"){
        plot.col <- "gray80"
    }else if(county=="kisumu"){
        plot.col <- brewer.pal(n = 9, name = "Blues")[4]
    }else if(county=="mombasa"){
        plot.col <- brewer.pal(n = 9, name = "Oranges")[2]
    }

    plot.xrange.base.end <- c(min(plot.data$t),max(plot.data$t))
    par(mfrow=c(2,3))
    plot.prevalence.base.end(plot.data$t,plot.data$prev.all.store,county,plot.col,j.overall,y.lims[1],plot.xrange.base.end,baseline.data,endline.data)
    plot.prevalence.base.end(plot.data$t,plot.data$prev.young.store,county,plot.col,j.young,y.lims[2],plot.xrange.base.end,baseline.data,endline.data)
    plot.prevalence.base.end(plot.data$t,plot.data$prev.old.store,county,plot.col,j.old,y.lims[3],plot.xrange.base.end,baseline.data,endline.data)
    plot.prevalence.base.end(plot.data$t,plot.data$prev.virt.store,county,plot.col,j.virt,y.lims[4],plot.xrange.base.end,baseline.data,endline.data)
    plot.prevalence.base.end(plot.data$t,plot.data$prev.both.store,county,plot.col,j.both,y.lims[5],plot.xrange.base.end,baseline.data,endline.data)
    plot.prevalence.base.end(plot.data$t,plot.data$prev.phys.store,county,plot.col,j.phys,y.lims[6],plot.xrange.base.end,baseline.data,endline.data)
}


##########################################################
##########################################################
### Main code:
##########################################################
##########################################################



resultsdir <- paste0("results_intervention/")

t.baseline <- 2019.35  # Mean date of baseline is 07 May 2019
t.endline <- 2020.78   # Mean date of endline is 13 Oct 2020 = 2020.78
type.col <- c("blue","red","green")


kisumu.data <- get.data.as.list(resultsdir,"kisumu",99)
mombasa.data <- get.data.as.list(resultsdir,"mombasa",142)
kiambu.data <- get.data.as.list("../kiambu_increasing_prev2/impact_evaluation/results_intervention/","kiambu",156)
kiambu.data$t <- kiambu.data$t+130 # intervention at t=20 instead of 150

kisumu.optimal.data <- get.data.as.list("results_optimal/","kisumu",99)
kisumu.counterfactual.data <- get.data.as.list("results_counterfactual/","kisumu",99)


kiambu.optimal.data <- get.data.as.list("../kiambu_increasing_prev2/impact_evaluation/results_optimal/","kiambu",156)
kiambu.counterfactual.data <- get.data.as.list("../kiambu_increasing_prev2/impact_evaluation/results_counterfactual/","kiambu",156)
kiambu.optimal.data$t <- kiambu.optimal.data$t+130 # intervention at t=20 instead of 150
kiambu.counterfactual.data$t <- kiambu.counterfactual.data$t+130 # intervention at t=20 instead of 150



mombasa.optimal.data <- get.data.as.list("results_optimal/","mombasa",142)
mombasa.counterfactual.data <- get.data.as.list("results_counterfactual/","mombasa",142)






fix.scale.type.age <- 1

if(fix.scale.type.age==1){
    max.plots.kiambu <- c(30,35,35,35,50,50)
}else{
    max.plots.kiambu <- c(30,35,30,25,25,50)
}

inc.scale.kiambu <- 12

if(fix.scale.type.age==1){
    max.plots.kisumu <- c(15,30,30,30,30,30)    
}else{
    max.plots.kisumu <- c(15,30,15,10,5,30)
}
inc.scale.kisumu <- 4

if(fix.scale.type.age==1){
    max.plots.mombasa <- c(25,40,40,40,30,30)
}else{
    max.plots.mombasa <- c(25,40,25,25,20,30)
}
inc.scale.mombasa <- 5





baseline.data.kiambu <- get.survey.data("kiambu","baseline")
baseline.data.kisumu <- get.survey.data("kisumu","baseline")
baseline.data.mombasa <- get.survey.data("mombasa","baseline")

endline.data.kiambu <- get.survey.data("kiambu","endline")
endline.data.kisumu <- get.survey.data("kisumu","endline")
endline.data.mombasa <- get.survey.data("mombasa","endline")


# Use this to plot whole simulation time:
full.x.range <- c(min(plot.data$t),max(plot.data$t))
#baseline.endline.range <- c(t.baseline,t.endline+1)
baseline.endline.range <- c(t.baseline,t.endline+10)

j.overall <- 1
j.virt <- 2
j.both <- 3
j.phys <- 4
j.young <- 5
j.old <- 6




###########
# Check which don't fit overall prevalence:
###########

i.baseline.kiambu <- min(which(kiambu.data$t >= t.baseline)) - 1
i.endline.kiambu <- min(which(kiambu.data$t >= t.endline))
i.baseline.kisumu <- min(which(kisumu.data$t >= t.baseline)) - 1
i.endline.kisumu <- min(which(kisumu.data$t >= t.endline))
i.baseline.mombasa <- min(which(mombasa.data$t >= t.baseline)) - 1
i.endline.mombasa <- min(which(mombasa.data$t >= t.endline))
table(100*kiambu.data$prev.all.store[i.baseline.kiambu,]>(baseline.data.kiambu$p.all - baseline.data.kiambu$width.all))
table(100*kiambu.data$prev.all.store[i.baseline.kiambu,]<(baseline.data.kiambu$p.all + baseline.data.kiambu$width.all))
table(100*kisumu.data$prev.all.store[i.baseline.kisumu,]>(baseline.data.kisumu$p.all - baseline.data.kisumu$width.all))
table(100*kisumu.data$prev.all.store[i.baseline.kisumu,]<(baseline.data.kisumu$p.all + baseline.data.kisumu$width.all))
table(100*mombasa.data$prev.all.store[i.baseline.mombasa,]>(baseline.data.mombasa$p.all - baseline.data.mombasa$width.all))
table(100*mombasa.data$prev.all.store[i.baseline.mombasa,]<(baseline.data.mombasa$p.all + baseline.data.mombasa$width.all))



table(100*kiambu.data$prev.all.store[i.endline.kiambu,]>(endline.data.kiambu$p.all - endline.data.kiambu$width.all))
table(100*kiambu.data$prev.all.store[i.endline.kiambu,]<(endline.data.kiambu$p.all + endline.data.kiambu$width.all))
table(100*kisumu.data$prev.all.store[i.endline.kisumu,]>(endline.data.kisumu$p.all - endline.data.kisumu$width.all))
table(100*kisumu.data$prev.all.store[i.endline.kisumu,]<(endline.data.kisumu$p.all + endline.data.kisumu$width.all))
table(100*mombasa.data$prev.all.store[i.endline.mombasa,]>(endline.data.mombasa$p.all - endline.data.mombasa$width.all))
table(100*mombasa.data$prev.all.store[i.endline.mombasa,]<(endline.data.mombasa$p.all + endline.data.mombasa$width.all))

############
# Results for exec summary:
#i.endline <- min(which(kiambu.data$t >= t.endline))
i.tenyear.kiambu <- min(which(kiambu.data$t >= (t.baseline+10)))
i.tenyear.kisumu <- min(which(kisumu.data$t >= (t.baseline+10)))
i.tenyear.mombasa <- min(which(mombasa.data$t >= (t.baseline+10)))


i.oneyear.kiambu <- min(which(kiambu.data$t >= (t.baseline+1)))
i.oneyear.kisumu <- min(which(kisumu.data$t >= (t.baseline+1)))
i.oneyear.mombasa <- min(which(mombasa.data$t >= (t.baseline+1)))



summary(kiambu.data$prop.onart.store[i.baseline.kiambu,] - kiambu.data$prop.onart.store[i.tenyear.kiambu,])
summary(kisumu.data$prop.onart.store[i.baseline.kisumu,] - kisumu.data$prop.onart.store[i.tenyear.kisumu,])
summary(mombasa.data$prop.onart.store[i.baseline.mombasa,] - mombasa.data$prop.onart.store[i.tenyear.mombasa,])

summary(kiambu.data$prop.unaware.store[i.baseline.kiambu,] - kiambu.data$prop.unaware.store[i.tenyear.kiambu,])
summary(kisumu.data$prop.unaware.store[i.baseline.kisumu,] - kisumu.data$prop.unaware.store[i.tenyear.kisumu,])
summary(mombasa.data$prop.unaware.store[i.baseline.mombasa,] - mombasa.data$prop.unaware.store[i.tenyear.mombasa,])


summary(kiambu.data$prop.unaware.store[i.tenyear.kiambu,])
summary(kisumu.data$prop.unaware.store[i.tenyear.kisumu,])
summary(mombasa.data$prop.unaware.store[i.tenyear.mombasa,])

summary(kiambu.data$prop.onart.store[i.tenyear.kiambu,])
summary(kisumu.data$prop.onart.store[i.tenyear.kisumu,])
summary(mombasa.data$prop.onart.store[i.tenyear.mombasa,])


summary(kiambu.counterfactual.data$prev.all.store[i.oneyear.kiambu,] - kiambu.data$prev.all.store[i.oneyear.kiambu,])
summary(kisumu.counterfactual.data$prev.all.store[i.oneyear.kisumu,] - kisumu.data$prev.all.store[i.oneyear.kisumu,])
summary(mombasa.counterfactual.data$prev.all.store[i.oneyear.mombasa,] - mombasa.data$prev.all.store[i.oneyear.mombasa,])

summary(kiambu.counterfactual.data$prev.all.store[i.tenyear.kiambu,] - kiambu.data$prev.all.store[i.tenyear.kiambu,])
summary(kisumu.counterfactual.data$prev.all.store[i.tenyear.kisumu,] - kisumu.data$prev.all.store[i.tenyear.kisumu,])
summary(mombasa.counterfactual.data$prev.all.store[i.tenyear.mombasa,] - mombasa.data$prev.all.store[i.tenyear.mombasa,])



summary((kiambu.counterfactual.data$incidence.store[i.oneyear.kiambu,] - kiambu.data$incidence.store[i.oneyear.kiambu,])/kiambu.counterfactual.data$incidence.store[i.oneyear.kiambu,])



summary((kisumu.counterfactual.data$incidence.store[i.oneyear.kisumu,] - kisumu.data$incidence.store[i.oneyear.kisumu,])/kisumu.counterfactual.data$incidence.store[i.oneyear.kisumu,])
summary((mombasa.counterfactual.data$incidence.store[i.oneyear.mombasa,] - mombasa.data$incidence.store[i.oneyear.mombasa,])/mombasa.counterfactual.data$incidence.store[i.endline.mombasa,])

summary((kisumu.counterfactual.data$incidence.store[i.endline.kisumu,] - kisumu.data$incidence.store[i.endline.kisumu,])/kisumu.counterfactual.data$incidence.store[i.endline.kisumu,])
summary((mombasa.counterfactual.data$incidence.store[i.endline.mombasa,] - mombasa.data$incidence.store[i.endline.mombasa,])/mombasa.counterfactual.data$incidence.store[i.endline.mombasa,])



summary((kiambu.counterfactual.data$incidence.store[i.tenyear.kiambu,] - kiambu.data$incidence.store[i.tenyear.kiambu,])/kiambu.counterfactual.data$incidence.store[i.tenyear.kiambu,])
summary((kisumu.counterfactual.data$incidence.store[i.tenyear.kisumu,] - kisumu.data$incidence.store[i.tenyear.kisumu,])/kisumu.counterfactual.data$incidence.store[i.tenyear.kisumu,])
summary((mombasa.counterfactual.data$incidence.store[i.tenyear.mombasa,] - mombasa.data$incidence.store[i.tenyear.mombasa,])/mombasa.counterfactual.data$incidence.store[i.tenyear.mombasa,])





##########
# Now the optimal scenario:


summary(kiambu.optimal.data$prop.unaware.store[i.tenyear.kiambu,])
summary(kisumu.optimal.data$prop.unaware.store[i.tenyear.kisumu,])
summary(mombasa.optimal.data$prop.unaware.store[i.tenyear.mombasa,])



summary(kiambu.counterfactual.data$prev.all.store[i.endline.kiambu,] - kiambu.optimal.data$prev.all.store[i.endline.kiambu,])
summary(kisumu.counterfactual.data$prev.all.store[i.endline.kisumu,] - kisumu.optimal.data$prev.all.store[i.endline.kisumu,])
summary(mombasa.counterfactual.data$prev.all.store[i.endline.mombasa,] - mombasa.optimal.data$prev.all.store[i.endline.mombasa,])


summary(kiambu.counterfactual.data$prev.all.store[i.tenyear.kiambu,] - kiambu.optimal.data$prev.all.store[i.tenyear.kiambu,])
summary(kisumu.counterfactual.data$prev.all.store[i.tenyear.kisumu,] - kisumu.optimal.data$prev.all.store[i.tenyear.kisumu,])
summary(mombasa.counterfactual.data$prev.all.store[i.tenyear.mombasa,] - mombasa.optimal.data$prev.all.store[i.tenyear.mombasa,])




summary((kiambu.counterfactual.data$incidence.store[i.oneyear.kiambu,] - kiambu.optimal.data$incidence.store[i.oneyear.kiambu,])/kiambu.counterfactual.data$incidence.store[i.oneyear.kiambu,])
summary((kisumu.counterfactual.data$incidence.store[i.oneyear.kisumu,] - kisumu.optimal.data$incidence.store[i.oneyear.kisumu,])/kisumu.counterfactual.data$incidence.store[i.oneyear.kisumu,])
summary((mombasa.counterfactual.data$incidence.store[i.oneyear.mombasa,] - mombasa.optimal.data$incidence.store[i.oneyear.mombasa,])/mombasa.counterfactual.data$incidence.store[i.oneyear.mombasa,])





summary((kiambu.counterfactual.data$incidence.store[i.tenyear.kiambu,] - kiambu.optimal.data$incidence.store[i.tenyear.kiambu,])/kiambu.counterfactual.data$incidence.store[i.tenyear.kiambu,])
summary((kisumu.counterfactual.data$incidence.store[i.tenyear.kisumu,] - kisumu.optimal.data$incidence.store[i.tenyear.kisumu,])/kisumu.counterfactual.data$incidence.store[i.tenyear.kisumu,])
summary((mombasa.counterfactual.data$incidence.store[i.tenyear.mombasa,] - mombasa.optimal.data$incidence.store[i.tenyear.mombasa,])/mombasa.counterfactual.data$incidence.store[i.tenyear.mombasa,])



#################
# Plotting:
#################

pdf(paste0("calibration_plot_kiambuincreasing_",str(fix.scale.type.age),".pdf"))
calibration.plot.since.start("kiambu",kiambu.data,max.plots.kiambu,baseline.data.kiambu)
dev.off()



pdf(paste0("calibration_plot_kisumu_",str(fix.scale.type.age),".pdf"))
calibration.plot.since.start("kisumu",kisumu.data,max.plots.kisumu,baseline.data.kisumu)
dev.off()


pdf(paste0("calibration_plot_mombasa_",str(fix.scale.type.age),".pdf"))
calibration.plot.since.start("mombasa",mombasa.data,max.plots.mombasa,baseline.data.mombasa)
dev.off()





pdf(paste0("calibration_onart_kiambu_",str(fix.scale.type.age),".pdf"))
calibration.plot.art.trend("kiambu",kiambu.data,baseline.endline.range)
dev.off()

pdf(paste0("calibration_onart_kisumu_",str(fix.scale.type.age),".pdf"))
calibration.plot.art.trend("kisumu",kisumu.data,baseline.endline.range)
dev.off()

pdf(paste0("calibration_onart_mombasa_",str(fix.scale.type.age),".pdf"))
calibration.plot.art.trend("mombasa",mombasa.data,baseline.endline.range)
dev.off()




# Dropped out of care/ART:
pdf(paste0("calibration_outsidecare_kiambuincreasing_",str(fix.scale.type.age),".pdf"))
calibration.plot.outsidecare.trend("kiambu",kiambu.data)
dev.off()

pdf(paste0("calibration_outsidecare_kisumu_",str(fix.scale.type.age),".pdf"))
calibration.plot.outsidecare.trend("kisumu",kisumu.data)
dev.off()

pdf(paste0("calibration_outsidecare_mombasa_",str(fix.scale.type.age),".pdf"))
calibration.plot.outsidecare.trend("mombasa",mombasa.data)
dev.off()



# Unaware of status:
pdf(paste0("calibration_unaware_kiambuincreasing_",str(fix.scale.type.age),".pdf"))
calibration.plot.unaware.trend("kiambu",kiambu.data)
dev.off()

pdf(paste0("calibration_unaware_kisumu_",str(fix.scale.type.age),".pdf"))
calibration.plot.unaware.trend("kisumu",kisumu.data)
dev.off()

pdf(paste0("calibration_unaware_mombasa_",str(fix.scale.type.age),".pdf"))
calibration.plot.unaware.trend("mombasa",mombasa.data)
dev.off()




pdf(paste0("calibration_incidence_",county,".pdf"))
par(mfrow=c(2,3))
# Need to divide incidence by 100 as plot.general multiplies it by 100:
plot.general(plot.data$t,plot.data$incidence.store/100,county,plot.col,full.x.range,inc.scale,"Overall incidence per 100 py")
plot.general(plot.data$t,plot.data$incidence.young.store/100,county,plot.col,full.x.range,inc.scale,"Incidence in <25 year olds per 100 py")
plot.general(plot.data$t,plot.data$incidence.old.store/100,county,plot.col,full.x.range,inc.scale,"Incidence in 25+ year olds per 100 py")
plot.general(plot.data$t,plot.data$incidence.virt.store/100,county,plot.col,full.x.range,inc.scale,"Incidence in virtual MSM per 100 py")
plot.general(plot.data$t,plot.data$incidence.both.store/100,county,plot.col,full.x.range,inc.scale,"Incidence in dual MSM per 100 py")
plot.general(plot.data$t,plot.data$incidence.phys.store/100,county,plot.col,full.x.range,inc.scale,"Incidence in physical MSM per 100 py")
dev.off()




########################################
pdf("calibration_baseline_endline_plot_kiambuincreasing.pdf")
plot.calibration.base.end("kiambu",kiambu.data,baseline.data.kiambu,endline.data.kiambu,c(35,35,60,40,40,40))
dev.off()


pdf("calibration_baseline_endline_plot_kisumu.pdf")
plot.calibration.base.end("kisumu",kisumu.data,baseline.data.kisumu,endline.data.kisumu,c(15,30,30,40,40,40))
dev.off()

pdf("calibration_baseline_endline_plot_mombasa.pdf")
plot.calibration.base.end("mombasa",mombasa.data,baseline.data.mombasa,endline.data.mombasa,c(35,35,60,40,40,40))
dev.off()


pdf("calibration_baseline_endline_plotall_kiambuincreasing.pdf")
plot.calibration.base.end.all("kiambu",kiambu.data,baseline.data.kiambu,endline.data.kiambu,c(35,35,60,40,40,40))
dev.off()

pdf("calibration_baseline_endline_plotall_kisumu.pdf")
plot.calibration.base.end.all("kisumu",kisumu.data,baseline.data.kisumu,endline.data.kisumu,c(35,35,60,40,40,40))
dev.off()

pdf("calibration_baseline_endline_plotall_mombasa.pdf")
plot.calibration.base.end.all("mombasa",mombasa.data,baseline.data.mombasa,endline.data.mombasa,c(35,35,60,40,40,40))
dev.off()







##################################
# Cascade pre-intervention:
##################################
plot.cascade.onart.preintervention <- function(county,plot.data)
{
    i.pre.intervention <- max(which(plot.data$t<2019.58))
    i.post.intervention <- min(which(plot.data$t>=(2019.58+1)))
    i.post.intervention5 <- min(which(plot.data$t>=(2019.58+5)))
    boxplot(100*plot.data$prop.onart.store[i.pre.intervention,],
            100*plot.data$prop.onart.young.store[i.pre.intervention,],
            100*plot.data$prop.onart.old.store[i.pre.intervention,],
            100*plot.data$prop.onart.virt.store[i.pre.intervention,],
            100*plot.data$prop.onart.both.store[i.pre.intervention,],
            100*plot.data$prop.onart.phys.store[i.pre.intervention,],
            names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
            ylab="% on ART",main=paste0("% on ART before HIV ST in ",capitalize(county)),
            xlab="MSM group",col=c("blue","green","green","orange","orange","orange"),cex.axis=1.2,cex.lab=1.5,cex.main=1.2)
}


plot.cascade.outsidecare.preintervention <- function(county,plot.data)
{
    i.pre.intervention <- max(which(plot.data$t<2019.58))
    i.post.intervention <- min(which(plot.data$t>=(2019.58+1))) 
   i.post.intervention5 <- min(which(plot.data$t>=(2019.58+5)))
    boxplot(100*plot.data$prop.outsidecare.store[i.pre.intervention,],
            100*plot.data$prop.outsidecare.young.store[i.pre.intervention,],
            100*plot.data$prop.outsidecare.old.store[i.pre.intervention,],
            100*plot.data$prop.outsidecare.virt.store[i.pre.intervention,],
            100*plot.data$prop.outsidecare.both.store[i.pre.intervention,],
            100*plot.data$prop.outsidecare.phys.store[i.pre.intervention,],
            names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
            ylab="% of PLHIV aware and outside care",main=paste0("% aware and outside care before HIV ST in ",capitalize(county)),
            xlab="MSM group",col=c("blue","green","green","orange","orange","orange"),cex.axis=1.2,cex.lab=1.5,cex.main=1.2)
}


plot.cascade.unaware.preintervention <- function(county,plot.data)
{
    i.pre.intervention <- max(which(plot.data$t<2019.58))
    i.post.intervention <- min(which(plot.data$t>=(2019.58+1)))
    i.post.intervention5 <- min(which(plot.data$t>=(2019.58+5)))
    boxplot(100*plot.data$prop.unaware.store[i.pre.intervention,],
            100*plot.data$prop.unaware.young.store[i.pre.intervention,],
            100*plot.data$prop.unaware.old.store[i.pre.intervention,],
            100*plot.data$prop.unaware.virt.store[i.pre.intervention,],
            100*plot.data$prop.unaware.both.store[i.pre.intervention,],
            100*plot.data$prop.unaware.phys.store[i.pre.intervention,],
            names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
            ylab="% of PLHIV unaware",main=paste0("% PLHIV who are unaware before HIV ST in ",capitalize(county)),
            xlab="MSM group",col=c("blue","green","green","orange","orange","orange"),cex.axis=1.2,cex.lab=1.5,cex.main=1.2)
}


    
pdf(paste0("baseline_onART_boxplot_kiambuincreasing_",str(fix.scale.type.age),".pdf"))
plot.cascade.onart.preintervention("kiambu",kiambu.data)
dev.off()

pdf(paste0("baseline_onART_boxplot_kisumu_",str(fix.scale.type.age),".pdf"))
plot.cascade.onart.preintervention("kisumu",kisumu.data)
dev.off()

pdf(paste0("baseline_onART_boxplot_mombasa_",str(fix.scale.type.age),".pdf"))
plot.cascade.onart.preintervention("mombasa",mombasa.data)
dev.off()





pdf(paste0("baseline_outsidecare_boxplot_kiambuincreasing_",str(fix.scale.type.age),".pdf"))
plot.cascade.outsidecare.preintervention("kiambu",kiambu.data)
dev.off()

pdf(paste0("baseline_outsidecare_boxplot_kisumu_",str(fix.scale.type.age),".pdf"))
plot.cascade.outsidecare.preintervention("kisumu",kisumu.data)
dev.off()

pdf(paste0("baseline_outsidecare_boxplot_mombasa_",str(fix.scale.type.age),".pdf"))
plot.cascade.outsidecare.preintervention("mombasa",mombasa.data)
dev.off()


pdf(paste0("baseline_unaware_boxplot_kiambuincreasing_",str(fix.scale.type.age),".pdf"))
plot.cascade.outsidecare.preintervention("kiambu",kiambu.data)
dev.off()

pdf(paste0("baseline_unaware_boxplot_kisumu_",str(fix.scale.type.age),".pdf"))
plot.cascade.outsidecare.preintervention("kisumu",kisumu.data)
dev.off()

pdf(paste0("baseline_unaware_boxplot_mombasa_",str(fix.scale.type.age),".pdf"))
plot.cascade.outsidecare.preintervention("mombasa",mombasa.data)
dev.off()






i.pre.intervention.kiambu <- max(which(kiambu.data$t<2019.58))
i.post.intervention.kiambu <- min(which(kiambu.data$t>=(2019.58+1)))
i.post.intervention5.kiambu <- min(which(kiambu.data$t>=(2019.58+5)))

i.pre.intervention.kisumu <- max(which(kisumu.data$t<2019.58))
i.post.intervention.kisumu <- min(which(kisumu.data$t>=(2019.58+1)))
i.post.intervention5.kisumu <- min(which(kisumu.data$t>=(2019.58+5)))

i.pre.intervention.mombasa <- max(which(mombasa.data$t<2019.58))
i.post.intervention.mombasa <- min(which(mombasa.data$t>=(2019.58+1)))
i.post.intervention5.mombasa <- min(which(mombasa.data$t>=(2019.58+5)))

pdf(paste0("baseline_onART_boxplot_allcounties.pdf"))
p <- boxplot(100*kiambu.data$prop.onart.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.onart.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.onart.store[i.pre.intervention.mombasa,],
        -1,
        100*kiambu.data$prop.onart.young.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.onart.young.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.onart.young.store[i.pre.intervention.mombasa,],
        -1,
        100*kiambu.data$prop.onart.old.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.onart.old.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.onart.old.store[i.pre.intervention.mombasa,],
        -1,
        100*kiambu.data$prop.onart.virt.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.onart.virt.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.onart.virt.store[i.pre.intervention.mombasa,],
        -1,
        100*kiambu.data$prop.onart.both.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.onart.both.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.onart.both.store[i.pre.intervention.mombasa,],
        -1,
        100*kiambu.data$prop.onart.phys.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.onart.phys.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.onart.phys.store[i.pre.intervention.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="% on ART",main=paste0("% on ART before HIV ST introduced"),
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(55,90),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),cex.axis=1.0)
legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)

#abline(v=4,lty=3,col="gray")
#abline(v=12,lty=3,col="gray")

dev.off()




pdf(paste0("baseline_unaware_boxplot_allcounties.pdf"))
p <- boxplot(100*kiambu.data$prop.unaware.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.unaware.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.unaware.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.young.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.unaware.young.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.unaware.young.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.old.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.unaware.old.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.unaware.old.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.virt.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.unaware.virt.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.unaware.virt.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.both.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.unaware.both.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.unaware.both.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.phys.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.unaware.phys.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.unaware.phys.store[i.pre.intervention.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="% of PLHIV unaware",main=paste0("% PLHIV who are unaware before HIV ST introduced"),
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(0,40),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)

#abline(v=4,lty=3,col="gray")
#abline(v=12,lty=3,col="gray")
dev.off()



pdf(paste0("baseline_outsidecare_boxplot_allcounties.pdf"))
p <- boxplot(100*kiambu.data$prop.outsidecare.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.young.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.young.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.young.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.old.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.old.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.old.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.virt.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.virt.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.virt.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.both.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.both.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.both.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.phys.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.phys.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.phys.store[i.pre.intervention.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="% of PLHIV aware outside care",main=paste0("% PLHIV who are aware but outside care before HIV ST introduced"),
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(5,15),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)

#abline(v=4,lty=3,col="gray")
#abline(v=12,lty=3,col="gray")

dev.off()










##################################
# Cascade post-intervention:
##################################




pdf(paste0("endline_onART_boxplot_allcounties.pdf"))
p <- boxplot(100*kiambu.data$prop.onart.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.onart.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.onart.store[i.post.intervention.mombasa,],
        -1,
        100*kiambu.data$prop.onart.young.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.onart.young.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.onart.young.store[i.post.intervention.mombasa,],
        -1,
        100*kiambu.data$prop.onart.old.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.onart.old.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.onart.old.store[i.post.intervention.mombasa,],
        -1,
        100*kiambu.data$prop.onart.virt.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.onart.virt.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.onart.virt.store[i.post.intervention.mombasa,],
        -1,
        100*kiambu.data$prop.onart.both.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.onart.both.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.onart.both.store[i.post.intervention.mombasa,],
        -1,
        100*kiambu.data$prop.onart.phys.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.onart.phys.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.onart.phys.store[i.post.intervention.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="% on ART",main=paste0("% on ART after 1 year of HIV ST"),
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(55,90),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)

#abline(v=4,lty=3,col="gray")
#abline(v=12,lty=3,col="gray")

dev.off()




pdf(paste0("endline_unaware_boxplot_allcounties.pdf"))
p <- boxplot(100*kiambu.data$prop.unaware.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.unaware.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.unaware.store[i.post.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.young.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.unaware.young.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.unaware.young.store[i.post.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.old.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.unaware.old.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.unaware.old.store[i.post.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.virt.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.unaware.virt.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.unaware.virt.store[i.post.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.both.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.unaware.both.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.unaware.both.store[i.post.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.phys.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.unaware.phys.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.unaware.phys.store[i.post.intervention.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="% of PLHIV unaware",main=paste0("% PLHIV who are unaware after 1 year of HIV ST"),
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(0,40),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)

#abline(v=4,lty=3,col="gray")
#abline(v=12,lty=3,col="gray")
dev.off()



pdf(paste0("endline_outsidecare_boxplot_allcounties.pdf"))
p <- boxplot(100*kiambu.data$prop.outsidecare.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.store[i.post.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.young.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.young.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.young.store[i.post.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.old.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.old.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.old.store[i.post.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.virt.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.virt.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.virt.store[i.post.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.both.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.both.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.both.store[i.post.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.phys.store[i.post.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.phys.store[i.post.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.phys.store[i.post.intervention.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="% of PLHIV aware outside care",main=paste0("% PLHIV who are aware but outside care after 1 year of HIV ST"),
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(5,15),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)

#abline(v=4,lty=3,col="gray")
#abline(v=12,lty=3,col="gray")

dev.off()









##########################
# Absolute Difference on ART pre/post:
###########################
pdf(paste0("pre_post_absoluteOnART_boxplot_allcounties.pdf"))

p <- boxplot(100*kiambu.data$prop.onart.store[i.post.intervention5.kiambu,]-100*kiambu.data$prop.onart.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.onart.store[i.post.intervention5.kisumu,]-100*kisumu.data$prop.onart.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.onart.store[i.post.intervention5.mombasa,]-100*mombasa.data$prop.onart.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.onart.young.store[i.post.intervention5.kiambu,]-100*kiambu.data$prop.onart.young.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.onart.young.store[i.post.intervention5.kisumu,]-100*kisumu.data$prop.onart.young.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.onart.young.store[i.post.intervention5.mombasa,]-100*mombasa.data$prop.onart.young.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.onart.old.store[i.post.intervention5.kiambu,]-100*kiambu.data$prop.onart.old.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.onart.old.store[i.post.intervention5.kisumu,]-100*kisumu.data$prop.onart.old.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.onart.old.store[i.post.intervention5.mombasa,]-100*mombasa.data$prop.onart.old.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.onart.virt.store[i.post.intervention5.kiambu,]-100*kiambu.data$prop.onart.virt.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.onart.virt.store[i.post.intervention5.kisumu,]-100*kisumu.data$prop.onart.virt.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.onart.virt.store[i.post.intervention5.mombasa,]-100*mombasa.data$prop.onart.virt.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.onart.both.store[i.post.intervention5.kiambu,]-100*kiambu.data$prop.onart.both.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.onart.both.store[i.post.intervention5.kisumu,]-100*kisumu.data$prop.onart.both.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.onart.both.store[i.post.intervention5.mombasa,]-100*mombasa.data$prop.onart.both.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.onart.phys.store[i.post.intervention5.kiambu,]-100*kiambu.data$prop.onart.phys.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.onart.phys.store[i.post.intervention5.kisumu,]-100*kisumu.data$prop.onart.phys.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.onart.phys.store[i.post.intervention5.mombasa,]-100*mombasa.data$prop.onart.phys.store[i.pre.intervention.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="Percentage point increase",main=paste0("Absolute increase in % of PLHIV on ART after 5 years of HIV ST"),
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(0,10),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
legend(x=0.3,y=10.2,fill=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),bty="n",cex=1.3)
dev.off()



########################
# Relative change on ART:

pdf(paste0("pre_post_relativeOnART_boxplot_allcounties.pdf"))
p <- boxplot((100*kiambu.data$prop.onart.store[i.post.intervention5.kiambu,]-100*kiambu.data$prop.onart.store[i.pre.intervention.kiambu,])/kiambu.data$prop.onart.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.onart.store[i.post.intervention5.kisumu,]-100*kisumu.data$prop.onart.store[i.pre.intervention.kisumu,])/kisumu.data$prop.onart.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.onart.store[i.post.intervention5.mombasa,]-100*mombasa.data$prop.onart.store[i.pre.intervention.mombasa,])/mombasa.data$prop.onart.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.onart.young.store[i.post.intervention5.kiambu,]-100*kiambu.data$prop.onart.young.store[i.pre.intervention.kiambu,])/kiambu.data$prop.onart.young.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.onart.young.store[i.post.intervention5.kisumu,]-100*kisumu.data$prop.onart.young.store[i.pre.intervention.kisumu,])/kisumu.data$prop.onart.young.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.onart.young.store[i.post.intervention5.mombasa,]-100*mombasa.data$prop.onart.young.store[i.pre.intervention.mombasa,])/mombasa.data$prop.onart.young.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.onart.old.store[i.post.intervention5.kiambu,]-100*kiambu.data$prop.onart.old.store[i.pre.intervention.kiambu,])/kiambu.data$prop.onart.old.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.onart.old.store[i.post.intervention5.kisumu,]-100*kisumu.data$prop.onart.old.store[i.pre.intervention.kisumu,])/kisumu.data$prop.onart.old.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.onart.old.store[i.post.intervention5.mombasa,]-100*mombasa.data$prop.onart.old.store[i.pre.intervention.mombasa,])/mombasa.data$prop.onart.old.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.onart.virt.store[i.post.intervention5.kiambu,]-100*kiambu.data$prop.onart.virt.store[i.pre.intervention.kiambu,])/kiambu.data$prop.onart.virt.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.onart.virt.store[i.post.intervention5.kisumu,]-100*kisumu.data$prop.onart.virt.store[i.pre.intervention.kisumu,])/kisumu.data$prop.onart.virt.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.onart.virt.store[i.post.intervention5.mombasa,]-100*mombasa.data$prop.onart.virt.store[i.pre.intervention.mombasa,])/mombasa.data$prop.onart.virt.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.onart.both.store[i.post.intervention5.kiambu,]-100*kiambu.data$prop.onart.both.store[i.pre.intervention.kiambu,])/kiambu.data$prop.onart.both.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.onart.both.store[i.post.intervention5.kisumu,]-100*kisumu.data$prop.onart.both.store[i.pre.intervention.kisumu,])/kisumu.data$prop.onart.both.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.onart.both.store[i.post.intervention5.mombasa,]-100*mombasa.data$prop.onart.both.store[i.pre.intervention.mombasa,])/mombasa.data$prop.onart.both.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.onart.phys.store[i.post.intervention5.kiambu,]-100*kiambu.data$prop.onart.phys.store[i.pre.intervention.kiambu,])/kiambu.data$prop.onart.phys.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.onart.phys.store[i.post.intervention5.kisumu,]-100*kisumu.data$prop.onart.phys.store[i.pre.intervention.kisumu,])/kisumu.data$prop.onart.phys.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.onart.phys.store[i.post.intervention5.mombasa,]-100*mombasa.data$prop.onart.phys.store[i.pre.intervention.mombasa,])/mombasa.data$prop.onart.phys.store[i.pre.intervention.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="Relative increase (%)",main=paste0("Relative increase in PLHIV on ART after 5 years of HIV ST"),
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(0,15),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)
dev.off()

################################
# Pre/post decrease in unaware:
################################

pdf(paste0("pre_post_absolute_unaware_boxplot_allcounties.pdf"))
p <- boxplot(100*kiambu.data$prop.unaware.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.unaware.store[i.post.intervention5.kiambu,],
        100*kisumu.data$prop.unaware.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.unaware.store[i.post.intervention5.kisumu,],
        100*mombasa.data$prop.unaware.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.unaware.store[i.post.intervention5.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.young.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.unaware.young.store[i.post.intervention5.kiambu,],
        100*kisumu.data$prop.unaware.young.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.unaware.young.store[i.post.intervention5.kisumu,],
        100*mombasa.data$prop.unaware.young.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.unaware.young.store[i.post.intervention5.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.old.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.unaware.old.store[i.post.intervention5.kiambu,],
        100*kisumu.data$prop.unaware.old.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.unaware.old.store[i.post.intervention5.kisumu,],
        100*mombasa.data$prop.unaware.old.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.unaware.old.store[i.post.intervention5.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.virt.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.unaware.virt.store[i.post.intervention5.kiambu,],
        100*kisumu.data$prop.unaware.virt.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.unaware.virt.store[i.post.intervention5.kisumu,],
        100*mombasa.data$prop.unaware.virt.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.unaware.virt.store[i.post.intervention5.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.both.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.unaware.both.store[i.post.intervention5.kiambu,],
        100*kisumu.data$prop.unaware.both.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.unaware.both.store[i.post.intervention5.kisumu,],
        100*mombasa.data$prop.unaware.both.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.unaware.both.store[i.post.intervention5.mombasa,],
        -100,
        100*kiambu.data$prop.unaware.phys.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.unaware.phys.store[i.post.intervention5.kiambu,],
        100*kisumu.data$prop.unaware.phys.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.unaware.phys.store[i.post.intervention5.kisumu,],
        100*mombasa.data$prop.unaware.phys.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.unaware.phys.store[i.post.intervention5.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="Percentage point reduction",main=paste0("Absolute decrease in HIV+ unaware after 5 years of HIV ST"),
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(0,10),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)
dev.off()

#################
# Relative decline in unaware:
#################
pdf(paste0("pre_post_relative_unaware_boxplot_allcounties.pdf"))
p <- boxplot((100*kiambu.data$prop.unaware.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.unaware.store[i.post.intervention5.kiambu,])/kiambu.data$prop.unaware.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.unaware.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.unaware.store[i.post.intervention5.kisumu,])/kisumu.data$prop.unaware.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.unaware.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.unaware.store[i.post.intervention5.mombasa,])/mombasa.data$prop.unaware.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.unaware.young.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.unaware.young.store[i.post.intervention5.kiambu,])/kiambu.data$prop.unaware.young.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.unaware.young.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.unaware.young.store[i.post.intervention5.kisumu,])/kisumu.data$prop.unaware.young.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.unaware.young.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.unaware.young.store[i.post.intervention5.mombasa,])/mombasa.data$prop.unaware.young.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.unaware.old.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.unaware.old.store[i.post.intervention5.kiambu,])/kiambu.data$prop.unaware.old.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.unaware.old.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.unaware.old.store[i.post.intervention5.kisumu,])/kisumu.data$prop.unaware.old.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.unaware.old.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.unaware.old.store[i.post.intervention5.mombasa,])/mombasa.data$prop.unaware.old.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.unaware.virt.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.unaware.virt.store[i.post.intervention5.kiambu,])/kiambu.data$prop.unaware.virt.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.unaware.virt.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.unaware.virt.store[i.post.intervention5.kisumu,])/kisumu.data$prop.unaware.virt.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.unaware.virt.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.unaware.virt.store[i.post.intervention5.mombasa,])/mombasa.data$prop.unaware.virt.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.unaware.both.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.unaware.both.store[i.post.intervention5.kiambu,])/kiambu.data$prop.unaware.both.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.unaware.both.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.unaware.both.store[i.post.intervention5.kisumu,])/kisumu.data$prop.unaware.both.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.unaware.both.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.unaware.both.store[i.post.intervention5.mombasa,])/mombasa.data$prop.unaware.both.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.unaware.phys.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.unaware.phys.store[i.post.intervention5.kiambu,])/kiambu.data$prop.unaware.phys.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.unaware.phys.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.unaware.phys.store[i.post.intervention5.kisumu,])/kisumu.data$prop.unaware.phys.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.unaware.phys.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.unaware.phys.store[i.post.intervention5.mombasa,])/mombasa.data$prop.unaware.phys.store[i.pre.intervention.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="Relative decline (%)",main=paste0("Relative decline in PLHIV unaware after 5 years of HIV ST"),
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(0,50),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)
dev.off()



## #################
## # Relative increase in outside care:
## #################
pdf(paste0("pre_post_absolute_outsidecare_boxplot_allcounties.pdf"))

p <- boxplot(100*kiambu.data$prop.outsidecare.store[i.post.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.store[i.post.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.store[i.post.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.young.store[i.post.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.young.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.young.store[i.post.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.young.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.young.store[i.post.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.young.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.old.store[i.post.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.old.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.old.store[i.post.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.old.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.old.store[i.post.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.old.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.virt.store[i.post.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.virt.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.virt.store[i.post.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.virt.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.virt.store[i.post.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.virt.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.both.store[i.post.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.both.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.both.store[i.post.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.both.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.both.store[i.post.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.both.store[i.pre.intervention.mombasa,],
        -100,
        100*kiambu.data$prop.outsidecare.phys.store[i.post.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.phys.store[i.pre.intervention.kiambu,],
        100*kisumu.data$prop.outsidecare.phys.store[i.post.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.phys.store[i.pre.intervention.kisumu,],
        100*mombasa.data$prop.outsidecare.phys.store[i.post.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.phys.store[i.pre.intervention.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="Percentage point increase",main="Absolute increase in PLHIV outside care after 1 year of HIV ST",
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(0,2),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)
dev.off()



########################
## # Relative increase in outside care:
########################

pdf(paste0("pre_post_relative_outsidecare_boxplot_allcounties.pdf"))
p <- boxplot((100*kiambu.data$prop.outsidecare.store[i.post.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.store[i.pre.intervention.kiambu,])/kiambu.data$prop.outsidecare.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.outsidecare.store[i.post.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.store[i.pre.intervention.kisumu,])/kisumu.data$prop.outsidecare.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.outsidecare.store[i.post.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.store[i.pre.intervention.mombasa,])/mombasa.data$prop.outsidecare.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.outsidecare.young.store[i.post.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.young.store[i.pre.intervention.kiambu,])/kiambu.data$prop.outsidecare.young.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.outsidecare.young.store[i.post.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.young.store[i.pre.intervention.kisumu,])/kisumu.data$prop.outsidecare.young.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.outsidecare.young.store[i.post.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.young.store[i.pre.intervention.mombasa,])/mombasa.data$prop.outsidecare.young.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.outsidecare.old.store[i.post.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.old.store[i.pre.intervention.kiambu,])/kiambu.data$prop.outsidecare.old.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.outsidecare.old.store[i.post.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.old.store[i.pre.intervention.kisumu,])/kisumu.data$prop.outsidecare.old.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.outsidecare.old.store[i.post.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.old.store[i.pre.intervention.mombasa,])/mombasa.data$prop.outsidecare.old.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.outsidecare.virt.store[i.post.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.virt.store[i.pre.intervention.kiambu,])/kiambu.data$prop.outsidecare.virt.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.outsidecare.virt.store[i.post.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.virt.store[i.pre.intervention.kisumu,])/kisumu.data$prop.outsidecare.virt.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.outsidecare.virt.store[i.post.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.virt.store[i.pre.intervention.mombasa,])/mombasa.data$prop.outsidecare.virt.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.outsidecare.both.store[i.post.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.both.store[i.pre.intervention.kiambu,])/kiambu.data$prop.outsidecare.both.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.outsidecare.both.store[i.post.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.both.store[i.pre.intervention.kisumu,])/kisumu.data$prop.outsidecare.both.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.outsidecare.both.store[i.post.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.both.store[i.pre.intervention.mombasa,])/mombasa.data$prop.outsidecare.both.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.data$prop.outsidecare.phys.store[i.post.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.phys.store[i.pre.intervention.kiambu,])/kiambu.data$prop.outsidecare.phys.store[i.pre.intervention.kiambu,],
        (100*kisumu.data$prop.outsidecare.phys.store[i.post.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.phys.store[i.pre.intervention.kisumu,])/kisumu.data$prop.outsidecare.phys.store[i.pre.intervention.kisumu,],
        (100*mombasa.data$prop.outsidecare.phys.store[i.post.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.phys.store[i.pre.intervention.mombasa,])/mombasa.data$prop.outsidecare.phys.store[i.pre.intervention.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="Relative increase (%)",main=paste0("Relative increase in PLHIV outside care after 1 year of HIV ST"),
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(0,15),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)
dev.off()

## pdf(paste0("pre_post_relative_outsidecare_boxplot_allcounties.pdf"))
## p <- boxplot((100*kiambu.data$prop.outsidecare.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.store[i.post.intervention.kiambu,])/kiambu.data$prop.outsidecare.store[i.pre.intervention.kiambu,],
##         (100*kisumu.data$prop.outsidecare.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.store[i.post.intervention.kisumu,])/kisumu.data$prop.outsidecare.store[i.pre.intervention.kisumu,],
##         (100*mombasa.data$prop.outsidecare.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.store[i.post.intervention.mombasa,])/mombasa.data$prop.outsidecare.store[i.pre.intervention.mombasa,],
##         -100,
##         (100*kiambu.data$prop.outsidecare.young.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.young.store[i.post.intervention.kiambu,])/kiambu.data$prop.outsidecare.young.store[i.pre.intervention.kiambu,],
##         (100*kisumu.data$prop.outsidecare.young.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.young.store[i.post.intervention.kisumu,])/kisumu.data$prop.outsidecare.young.store[i.pre.intervention.kisumu,],
##         (100*mombasa.data$prop.outsidecare.young.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.young.store[i.post.intervention.mombasa,])/mombasa.data$prop.outsidecare.young.store[i.pre.intervention.mombasa,],
##         -100,
##         (100*kiambu.data$prop.outsidecare.old.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.old.store[i.post.intervention.kiambu,])/kiambu.data$prop.outsidecare.old.store[i.pre.intervention.kiambu,],
##         (100*kisumu.data$prop.outsidecare.old.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.old.store[i.post.intervention.kisumu,])/kisumu.data$prop.outsidecare.old.store[i.pre.intervention.kisumu,],
##         (100*mombasa.data$prop.outsidecare.old.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.old.store[i.post.intervention.mombasa,])/mombasa.data$prop.outsidecare.old.store[i.pre.intervention.mombasa,],
##         -100,
##         (100*kiambu.data$prop.outsidecare.virt.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.virt.store[i.post.intervention.kiambu,])/kiambu.data$prop.outsidecare.virt.store[i.pre.intervention.kiambu,],
##         (100*kisumu.data$prop.outsidecare.virt.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.virt.store[i.post.intervention.kisumu,])/kisumu.data$prop.outsidecare.virt.store[i.pre.intervention.kisumu,],
##         (100*mombasa.data$prop.outsidecare.virt.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.virt.store[i.post.intervention.mombasa,])/mombasa.data$prop.outsidecare.virt.store[i.pre.intervention.mombasa,],
##         -100,
##         (100*kiambu.data$prop.outsidecare.both.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.both.store[i.post.intervention.kiambu,])/kiambu.data$prop.outsidecare.both.store[i.pre.intervention.kiambu,],
##         (100*kisumu.data$prop.outsidecare.both.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.both.store[i.post.intervention.kisumu,])/kisumu.data$prop.outsidecare.both.store[i.pre.intervention.kisumu,],
##         (100*mombasa.data$prop.outsidecare.both.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.both.store[i.post.intervention.mombasa,])/mombasa.data$prop.outsidecare.both.store[i.pre.intervention.mombasa,],
##         -100,
##         (100*kiambu.data$prop.outsidecare.phys.store[i.pre.intervention.kiambu,]-100*kiambu.data$prop.outsidecare.phys.store[i.post.intervention.kiambu,])/kiambu.data$prop.outsidecare.phys.store[i.pre.intervention.kiambu,],
##         (100*kisumu.data$prop.outsidecare.phys.store[i.pre.intervention.kisumu,]-100*kisumu.data$prop.outsidecare.phys.store[i.post.intervention.kisumu,])/kisumu.data$prop.outsidecare.phys.store[i.pre.intervention.kisumu,],
##         (100*mombasa.data$prop.outsidecare.phys.store[i.pre.intervention.mombasa,]-100*mombasa.data$prop.outsidecare.phys.store[i.post.intervention.mombasa,])/mombasa.data$prop.outsidecare.phys.store[i.pre.intervention.mombasa,],
##                                         #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
##         ylab="Relative decline (%)",main=paste0("Relative decline in HIV+ outside care after 1 year of intervention"),
##         xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(-5,5),xaxt="n")

## axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
## legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)
## dev.off()




########################
# Optimal scenario Relative change on ART:

pdf(paste0("pre_post_relativeOnART_boxplot_optimal_allcounties.pdf"))
p <- boxplot((100*kiambu.optimal.data$prop.onart.store[i.post.intervention5.kiambu,]-100*kiambu.optimal.data$prop.onart.store[i.pre.intervention.kiambu,])/kiambu.optimal.data$prop.onart.store[i.pre.intervention.kiambu,],
        (100*kisumu.optimal.data$prop.onart.store[i.post.intervention5.kisumu,]-100*kisumu.optimal.data$prop.onart.store[i.pre.intervention.kisumu,])/kisumu.optimal.data$prop.onart.store[i.pre.intervention.kisumu,],
        (100*mombasa.optimal.data$prop.onart.store[i.post.intervention5.mombasa,]-100*mombasa.optimal.data$prop.onart.store[i.pre.intervention.mombasa,])/mombasa.optimal.data$prop.onart.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.optimal.data$prop.onart.young.store[i.post.intervention5.kiambu,]-100*kiambu.optimal.data$prop.onart.young.store[i.pre.intervention.kiambu,])/kiambu.optimal.data$prop.onart.young.store[i.pre.intervention.kiambu,],
        (100*kisumu.optimal.data$prop.onart.young.store[i.post.intervention5.kisumu,]-100*kisumu.optimal.data$prop.onart.young.store[i.pre.intervention.kisumu,])/kisumu.optimal.data$prop.onart.young.store[i.pre.intervention.kisumu,],
        (100*mombasa.optimal.data$prop.onart.young.store[i.post.intervention5.mombasa,]-100*mombasa.optimal.data$prop.onart.young.store[i.pre.intervention.mombasa,])/mombasa.optimal.data$prop.onart.young.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.optimal.data$prop.onart.old.store[i.post.intervention5.kiambu,]-100*kiambu.optimal.data$prop.onart.old.store[i.pre.intervention.kiambu,])/kiambu.optimal.data$prop.onart.old.store[i.pre.intervention.kiambu,],
        (100*kisumu.optimal.data$prop.onart.old.store[i.post.intervention5.kisumu,]-100*kisumu.optimal.data$prop.onart.old.store[i.pre.intervention.kisumu,])/kisumu.optimal.data$prop.onart.old.store[i.pre.intervention.kisumu,],
        (100*mombasa.optimal.data$prop.onart.old.store[i.post.intervention5.mombasa,]-100*mombasa.optimal.data$prop.onart.old.store[i.pre.intervention.mombasa,])/mombasa.optimal.data$prop.onart.old.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.optimal.data$prop.onart.virt.store[i.post.intervention5.kiambu,]-100*kiambu.optimal.data$prop.onart.virt.store[i.pre.intervention.kiambu,])/kiambu.optimal.data$prop.onart.virt.store[i.pre.intervention.kiambu,],
        (100*kisumu.optimal.data$prop.onart.virt.store[i.post.intervention5.kisumu,]-100*kisumu.optimal.data$prop.onart.virt.store[i.pre.intervention.kisumu,])/kisumu.optimal.data$prop.onart.virt.store[i.pre.intervention.kisumu,],
        (100*mombasa.optimal.data$prop.onart.virt.store[i.post.intervention5.mombasa,]-100*mombasa.optimal.data$prop.onart.virt.store[i.pre.intervention.mombasa,])/mombasa.optimal.data$prop.onart.virt.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.optimal.data$prop.onart.both.store[i.post.intervention5.kiambu,]-100*kiambu.optimal.data$prop.onart.both.store[i.pre.intervention.kiambu,])/kiambu.optimal.data$prop.onart.both.store[i.pre.intervention.kiambu,],
        (100*kisumu.optimal.data$prop.onart.both.store[i.post.intervention5.kisumu,]-100*kisumu.optimal.data$prop.onart.both.store[i.pre.intervention.kisumu,])/kisumu.optimal.data$prop.onart.both.store[i.pre.intervention.kisumu,],
        (100*mombasa.optimal.data$prop.onart.both.store[i.post.intervention5.mombasa,]-100*mombasa.optimal.data$prop.onart.both.store[i.pre.intervention.mombasa,])/mombasa.optimal.data$prop.onart.both.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.optimal.data$prop.onart.phys.store[i.post.intervention5.kiambu,]-100*kiambu.optimal.data$prop.onart.phys.store[i.pre.intervention.kiambu,])/kiambu.optimal.data$prop.onart.phys.store[i.pre.intervention.kiambu,],
        (100*kisumu.optimal.data$prop.onart.phys.store[i.post.intervention5.kisumu,]-100*kisumu.optimal.data$prop.onart.phys.store[i.pre.intervention.kisumu,])/kisumu.optimal.data$prop.onart.phys.store[i.pre.intervention.kisumu,],
        (100*mombasa.optimal.data$prop.onart.phys.store[i.post.intervention5.mombasa,]-100*mombasa.optimal.data$prop.onart.phys.store[i.pre.intervention.mombasa,])/mombasa.optimal.data$prop.onart.phys.store[i.pre.intervention.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="Relative increase (%)",main=paste0("Relative increase in PLHIV on ART after 5 years of HIV ST"),
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(0,50),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)
dev.off()


#################
# Optimal scenario Relative decline in unaware:
#################
pdf(paste0("pre_post_relative_unaware_optimal_boxplot_allcounties.pdf"))
p <- boxplot((100*kiambu.optimal.data$prop.unaware.store[i.pre.intervention.kiambu,]-100*kiambu.optimal.data$prop.unaware.store[i.post.intervention5.kiambu,])/kiambu.optimal.data$prop.unaware.store[i.pre.intervention.kiambu,],
        (100*kisumu.optimal.data$prop.unaware.store[i.pre.intervention.kisumu,]-100*kisumu.optimal.data$prop.unaware.store[i.post.intervention5.kisumu,])/kisumu.optimal.data$prop.unaware.store[i.pre.intervention.kisumu,],
        (100*mombasa.optimal.data$prop.unaware.store[i.pre.intervention.mombasa,]-100*mombasa.optimal.data$prop.unaware.store[i.post.intervention5.mombasa,])/mombasa.optimal.data$prop.unaware.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.optimal.data$prop.unaware.young.store[i.pre.intervention.kiambu,]-100*kiambu.optimal.data$prop.unaware.young.store[i.post.intervention5.kiambu,])/kiambu.optimal.data$prop.unaware.young.store[i.pre.intervention.kiambu,],
        (100*kisumu.optimal.data$prop.unaware.young.store[i.pre.intervention.kisumu,]-100*kisumu.optimal.data$prop.unaware.young.store[i.post.intervention5.kisumu,])/kisumu.optimal.data$prop.unaware.young.store[i.pre.intervention.kisumu,],
        (100*mombasa.optimal.data$prop.unaware.young.store[i.pre.intervention.mombasa,]-100*mombasa.optimal.data$prop.unaware.young.store[i.post.intervention5.mombasa,])/mombasa.optimal.data$prop.unaware.young.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.optimal.data$prop.unaware.old.store[i.pre.intervention.kiambu,]-100*kiambu.optimal.data$prop.unaware.old.store[i.post.intervention5.kiambu,])/kiambu.optimal.data$prop.unaware.old.store[i.pre.intervention.kiambu,],
        (100*kisumu.optimal.data$prop.unaware.old.store[i.pre.intervention.kisumu,]-100*kisumu.optimal.data$prop.unaware.old.store[i.post.intervention5.kisumu,])/kisumu.optimal.data$prop.unaware.old.store[i.pre.intervention.kisumu,],
        (100*mombasa.optimal.data$prop.unaware.old.store[i.pre.intervention.mombasa,]-100*mombasa.optimal.data$prop.unaware.old.store[i.post.intervention5.mombasa,])/mombasa.optimal.data$prop.unaware.old.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.optimal.data$prop.unaware.virt.store[i.pre.intervention.kiambu,]-100*kiambu.optimal.data$prop.unaware.virt.store[i.post.intervention5.kiambu,])/kiambu.optimal.data$prop.unaware.virt.store[i.pre.intervention.kiambu,],
        (100*kisumu.optimal.data$prop.unaware.virt.store[i.pre.intervention.kisumu,]-100*kisumu.optimal.data$prop.unaware.virt.store[i.post.intervention5.kisumu,])/kisumu.optimal.data$prop.unaware.virt.store[i.pre.intervention.kisumu,],
        (100*mombasa.optimal.data$prop.unaware.virt.store[i.pre.intervention.mombasa,]-100*mombasa.optimal.data$prop.unaware.virt.store[i.post.intervention5.mombasa,])/mombasa.optimal.data$prop.unaware.virt.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.optimal.data$prop.unaware.both.store[i.pre.intervention.kiambu,]-100*kiambu.optimal.data$prop.unaware.both.store[i.post.intervention5.kiambu,])/kiambu.optimal.data$prop.unaware.both.store[i.pre.intervention.kiambu,],
        (100*kisumu.optimal.data$prop.unaware.both.store[i.pre.intervention.kisumu,]-100*kisumu.optimal.data$prop.unaware.both.store[i.post.intervention5.kisumu,])/kisumu.optimal.data$prop.unaware.both.store[i.pre.intervention.kisumu,],
        (100*mombasa.optimal.data$prop.unaware.both.store[i.pre.intervention.mombasa,]-100*mombasa.optimal.data$prop.unaware.both.store[i.post.intervention5.mombasa,])/mombasa.optimal.data$prop.unaware.both.store[i.pre.intervention.mombasa,],
        -100,
        (100*kiambu.optimal.data$prop.unaware.phys.store[i.pre.intervention.kiambu,]-100*kiambu.optimal.data$prop.unaware.phys.store[i.post.intervention5.kiambu,])/kiambu.optimal.data$prop.unaware.phys.store[i.pre.intervention.kiambu,],
        (100*kisumu.optimal.data$prop.unaware.phys.store[i.pre.intervention.kisumu,]-100*kisumu.optimal.data$prop.unaware.phys.store[i.post.intervention5.kisumu,])/kisumu.optimal.data$prop.unaware.phys.store[i.pre.intervention.kisumu,],
        (100*mombasa.optimal.data$prop.unaware.phys.store[i.pre.intervention.mombasa,]-100*mombasa.optimal.data$prop.unaware.phys.store[i.post.intervention5.mombasa,])/mombasa.optimal.data$prop.unaware.phys.store[i.pre.intervention.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="Relative decline (%)",main=paste0("Relative decline in PLHIV unaware after 5 years of HIV ST"),
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(0,100),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)
dev.off()


################################
# Optimal Pre/post decrease in unaware:
################################

pdf(paste0("pre_post_absolute_unaware_optimal_boxplot_allcounties.pdf"))
p <- boxplot(100*kiambu.optimal.data$prop.unaware.store[i.pre.intervention.kiambu,]-100*kiambu.optimal.data$prop.unaware.store[i.post.intervention5.kiambu,],
        100*kisumu.optimal.data$prop.unaware.store[i.pre.intervention.kisumu,]-100*kisumu.optimal.data$prop.unaware.store[i.post.intervention5.kisumu,],
        100*mombasa.optimal.data$prop.unaware.store[i.pre.intervention.mombasa,]-100*mombasa.optimal.data$prop.unaware.store[i.post.intervention5.mombasa,],
        -100,
        100*kiambu.optimal.data$prop.unaware.young.store[i.pre.intervention.kiambu,]-100*kiambu.optimal.data$prop.unaware.young.store[i.post.intervention5.kiambu,],
        100*kisumu.optimal.data$prop.unaware.young.store[i.pre.intervention.kisumu,]-100*kisumu.optimal.data$prop.unaware.young.store[i.post.intervention5.kisumu,],
        100*mombasa.optimal.data$prop.unaware.young.store[i.pre.intervention.mombasa,]-100*mombasa.optimal.data$prop.unaware.young.store[i.post.intervention5.mombasa,],
        -100,
        100*kiambu.optimal.data$prop.unaware.old.store[i.pre.intervention.kiambu,]-100*kiambu.optimal.data$prop.unaware.old.store[i.post.intervention5.kiambu,],
        100*kisumu.optimal.data$prop.unaware.old.store[i.pre.intervention.kisumu,]-100*kisumu.optimal.data$prop.unaware.old.store[i.post.intervention5.kisumu,],
        100*mombasa.optimal.data$prop.unaware.old.store[i.pre.intervention.mombasa,]-100*mombasa.optimal.data$prop.unaware.old.store[i.post.intervention5.mombasa,],
        -100,
        100*kiambu.optimal.data$prop.unaware.virt.store[i.pre.intervention.kiambu,]-100*kiambu.optimal.data$prop.unaware.virt.store[i.post.intervention5.kiambu,],
        100*kisumu.optimal.data$prop.unaware.virt.store[i.pre.intervention.kisumu,]-100*kisumu.optimal.data$prop.unaware.virt.store[i.post.intervention5.kisumu,],
        100*mombasa.optimal.data$prop.unaware.virt.store[i.pre.intervention.mombasa,]-100*mombasa.optimal.data$prop.unaware.virt.store[i.post.intervention5.mombasa,],
        -100,
        100*kiambu.optimal.data$prop.unaware.both.store[i.pre.intervention.kiambu,]-100*kiambu.optimal.data$prop.unaware.both.store[i.post.intervention5.kiambu,],
        100*kisumu.optimal.data$prop.unaware.both.store[i.pre.intervention.kisumu,]-100*kisumu.optimal.data$prop.unaware.both.store[i.post.intervention5.kisumu,],
        100*mombasa.optimal.data$prop.unaware.both.store[i.pre.intervention.mombasa,]-100*mombasa.optimal.data$prop.unaware.both.store[i.post.intervention5.mombasa,],
        -100,
        100*kiambu.optimal.data$prop.unaware.phys.store[i.pre.intervention.kiambu,]-100*kiambu.optimal.data$prop.unaware.phys.store[i.post.intervention5.kiambu,],
        100*kisumu.optimal.data$prop.unaware.phys.store[i.pre.intervention.kisumu,]-100*kisumu.optimal.data$prop.unaware.phys.store[i.post.intervention5.kisumu,],
        100*mombasa.optimal.data$prop.unaware.phys.store[i.pre.intervention.mombasa,]-100*mombasa.optimal.data$prop.unaware.phys.store[i.post.intervention5.mombasa,],
                                        #names=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"),
        ylab="Percentage point reduction",main=paste0("Absolute decrease in PLHIV unaware after 5 years of HIV ST"),
        xlab="MSM group",col=c("blue","green","orange","black"),cex.axis=1.2,cex.lab=1.4,ylim=c(0,30),xaxt="n")

axis(1,at=c(2,6,10,14,18,22),labels=c("Overall","<25 years","25+ years","Virtual","Dual","Physical"))
legend("topleft",col=c("blue","green","orange"),legend=c("Kiambu","Kisumu","Mombasa"),lty=1,bty="n",cex=1.3)
dev.off()







kiambu.pbs.baseline <- 0.16
kiambu.pbs.baseline.n <- 238
kiambu.pbs.endline <- 0.24
kiambu.pbs.endline.n <- 250
sd.pbs.baseline.kiambu <- sqrt(kiambu.pbs.baseline*(1-kiambu.pbs.baseline)/kiambu.pbs.baseline.n)
sd.pbs.endline.kiambu <- sqrt(kiambu.pbs.endline*(1-kiambu.pbs.endline)/kiambu.pbs.endline.n)



kisumu.pbs.baseline <- 0.10
kisumu.pbs.baseline.n <- 240
kisumu.pbs.endline <- 0.14
kisumu.pbs.endline.n <- 240
sd.pbs.baseline.kisumu <- sqrt(kisumu.pbs.baseline*(1-kisumu.pbs.baseline)/kisumu.pbs.baseline.n)
sd.pbs.endline.kisumu <- sqrt(kisumu.pbs.endline*(1-kisumu.pbs.endline)/kisumu.pbs.endline.n
)

mombasa.pbs.baseline <- 0.14
mombasa.pbs.baseline.n <- 237
mombasa.pbs.endline <- 0.18
mombasa.pbs.endline.n <- 228
sd.pbs.baseline.mombasa <- sqrt(mombasa.pbs.baseline*(1-mombasa.pbs.baseline)/mombasa.pbs.baseline.n)
sd.pbs.endline.mombasa <- sqrt(mombasa.pbs.endline*(1-mombasa.pbs.endline)/mombasa.pbs.endline.n)


pdf("Comparsion_aware_model_PBS_baseline.pdf")
box.col <- "orange"
pbs.col <- "darkgreen" 
p <- boxplot(100*kiambu.data$pbs.comparison.aware.store[i.pre.intervention.kiambu,],
             -100,
             100*kisumu.data$pbs.comparison.aware.store[i.pre.intervention.kisumu,],
             -100,
             100*mombasa.data$pbs.comparison.aware.store[i.pre.intervention.mombasa,],
             -100,
             col=box.col,ylim=c(0,25),xaxt="n",ylab="% of total MSM population who are aware they are HIV+",cex.axis=1.4,cex.lab=1.4)
             )
axis(1,at=c(1.5,3.5,5.5),labels=c("Kiambu","Kisumu","Mombasa"),cex.axis=1.4)
legend("topright",col=c(NA,pbs.col),legend=c("Model estimate","PBS estimate"),lty=c(NA,1),lwd=c(NA,3),fill=c(box.col,NA),border=NA,bty="n",cex=1.2)


points(2,100*kiambu.pbs.baseline,col=pbs.col,bg=pbs.col,lwd=5)
segments(2,100*(kiambu.pbs.baseline - 1.96*sd.pbs.baseline.kiambu),2,100*(kiambu.pbs.baseline + 1.96*sd.pbs.baseline.kiambu),col=pbs.col,lwd=2)
points(4,100*kisumu.pbs.baseline,col=pbs.col,bg=pbs.col,lwd=5)
segments(4,100*(kisumu.pbs.baseline - 1.96*sd.pbs.baseline.kisumu),4,100*(kisumu.pbs.baseline + 1.96*sd.pbs.baseline.kisumu),col=pbs.col,lwd=2)
points(6,100*mombasa.pbs.baseline,col=pbs.col,bg=pbs.col,lwd=5)
segments(6,100*(mombasa.pbs.baseline - 1.96*sd.pbs.baseline.mombasa),6,100*(mombasa.pbs.baseline + 1.96*sd.pbs.baseline.mombasa),col=pbs.col,lwd=2)

abline(v=2.5,lty=3,lwd=0.6,col="gray20")
abline(v=4.5,lty=3,lwd=0.5,col="gray20")
dev.off()




########################
# Post-intervention:
pdf("Comparsion_aware_model_PBS_endline.pdf")
box.col <- "orange"
pbs.col <- "darkgreen" 
p <- boxplot(100*kiambu.data$pbs.comparison.aware.store[i.post.intervention.kiambu,],
             -100,
             100*kisumu.data$pbs.comparison.aware.store[i.post.intervention.kisumu,],
             -100,
             100*mombasa.data$pbs.comparison.aware.store[i.post.intervention.mombasa,],
             -100,
             col=box.col,ylim=c(0,25),xaxt="n",ylab="% of total MSM population who are aware they are HIV+",cex.axis=1.4,cex.lab=1.4)
             )
axis(1,at=c(1.5,3.5,5.5),labels=c("Kiambu","Kisumu","Mombasa"),cex.axis=1.4)
legend("topright",col=c(NA,pbs.col),legend=c("Model estimate","PBS estimate"),lty=c(NA,1),lwd=c(NA,3),fill=c(box.col,NA),border=NA,bty="n",cex=1.2)


points(2,100*kiambu.pbs.endline,col=pbs.col,bg=pbs.col,lwd=5)
segments(2,100*(kiambu.pbs.endline - 1.96*sd.pbs.endline.kiambu),2,100*(kiambu.pbs.endline + 1.96*sd.pbs.endline.kiambu),col=pbs.col,lwd=2)
points(4,100*kisumu.pbs.endline,col=pbs.col,bg=pbs.col,lwd=5)
segments(4,100*(kisumu.pbs.endline - 1.96*sd.pbs.endline.kisumu),4,100*(kisumu.pbs.endline + 1.96*sd.pbs.endline.kisumu),col=pbs.col,lwd=2)
points(6,100*mombasa.pbs.endline,col=pbs.col,bg=pbs.col,lwd=5)
segments(6,100*(mombasa.pbs.endline - 1.96*sd.pbs.endline.mombasa),6,100*(mombasa.pbs.endline + 1.96*sd.pbs.endline.mombasa),col=pbs.col,lwd=2)

abline(v=2.5,lty=3,lwd=0.6,col="gray20")
abline(v=4.5,lty=3,lwd=0.5,col="gray20")
dev.off()
#######################










################################################################
# Polygon plots:
################################################################



polygon.cols<- c(brewer.pal(n = 11, name = "RdYlBu")[8], brewer.pal(n = 9, name = "Reds")[3], brewer.pal(n = 9, name = "Greens")[3], brewer.pal(n = 11, name = "BrBG")[4], brewer.pal(n = 11, name = "PuOr")[5])


lines.cols<- c(brewer.pal(n = 11, name = "RdYlBu")[10], brewer.pal(n = 9, name = "Reds")[7], brewer.pal(n = 9, name = "Greens")[7], brewer.pal(n = 11, name = "BrBG")[2], brewer.pal(n = 11, name = "PuOr")[7])


lq <- 0.1
uq <- 0.9

x.range=c(2010,2030)


####### Incidence plots:
plot.int.count.opt(kiambu.data$t,kiambu.counterfactual.data$t, kiambu.optimal.data$t, kiambu.data$incidence.store,kiambu.counterfactual.data$incidence.store,kiambu.optimal.data$incidence.store,lq,uq,x.range,y.range=c(0,12),plot.filename="kiambuincreasing_incidence.pdf",plot.legend=1,plot.title="Overall incidence (Kiambu)","Incidence (%)")

plot.int.count.opt(kisumu.data$t,kisumu.counterfactual.data$t, kisumu.optimal.data$t, kisumu.data$incidence.store,kisumu.counterfactual.data$incidence.store,kisumu.optimal.data$incidence.store,lq,uq,x.range,y.range=c(0,3),plot.filename="kisumu_incidence.pdf",plot.legend=1,plot.title="Overall incidence (Kisumu)","Incidence (%)")

plot.int.count.opt(mombasa.data$t,mombasa.counterfactual.data$t, mombasa.optimal.data$t, mombasa.data$incidence.store,mombasa.counterfactual.data$incidence.store,mombasa.optimal.data$incidence.store,lq,uq,x.range,y.range=c(0,4),plot.filename="mombasa_incidence.pdf",plot.legend=1,plot.title="Overall incidence (Mombasa)","Incidence (%)")


# Incidence panels:
pdf("kisumu_incidence_panel.pdf")
par(mfrow=c(2,3))
y.range <- c(0,3)
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, kisumu.data$incidence.store,kisumu.counterfactual.data$incidence.store,kisumu.optimal.data$incidence.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=1,plot.title="Overall incidence","Incidence (%)")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, kisumu.data$incidence.young.store,kisumu.counterfactual.data$incidence.young.store,kisumu.optimal.data$incidence.young.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="Incidence aged <25","Incidence (%)")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, kisumu.data$incidence.old.store,kisumu.counterfactual.data$incidence.old.store,kisumu.optimal.data$incidence.old.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="Incidence aged 25+","Incidence (%)")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, kisumu.data$incidence.virt.store,kisumu.counterfactual.data$incidence.virt.store,kisumu.optimal.data$incidence.virt.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="Incidence in virtual MSM","Incidence (%)")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, kisumu.data$incidence.both.store,kisumu.counterfactual.data$incidence.both.store,kisumu.optimal.data$incidence.both.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="Incidence in dual MSM","Incidence (%)")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, kisumu.data$incidence.phys.store,kisumu.counterfactual.data$incidence.phys.store,kisumu.optimal.data$incidence.phys.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="Incidence in physical MSM","Incidence (%)")
dev.off()


pdf("kiambuincreasing_incidence_panel.pdf")
par(mfrow=c(2,3))
y.range.kiambu <- c(0,15)
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, kiambu.data$incidence.store,kiambu.counterfactual.data$incidence.store,kiambu.optimal.data$incidence.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=1,plot.title="Overall incidence","Incidence (%)")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, kiambu.data$incidence.young.store,kiambu.counterfactual.data$incidence.young.store,kiambu.optimal.data$incidence.young.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="Incidence aged <25","Incidence (%)")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, kiambu.data$incidence.old.store,kiambu.counterfactual.data$incidence.old.store,kiambu.optimal.data$incidence.old.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="Incidence aged 25+","Incidence (%)")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, kiambu.data$incidence.virt.store,kiambu.counterfactual.data$incidence.virt.store,kiambu.optimal.data$incidence.virt.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="Incidence in virtual MSM","Incidence (%)")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, kiambu.data$incidence.both.store,kiambu.counterfactual.data$incidence.both.store,kiambu.optimal.data$incidence.both.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="Incidence in dual MSM","Incidence (%)")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, kiambu.data$incidence.phys.store,kiambu.counterfactual.data$incidence.phys.store,kiambu.optimal.data$incidence.phys.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="Incidence in physical MSM","Incidence (%)")
dev.off()


pdf("mombasa_incidence_panel.pdf")
par(mfrow=c(2,3))
y.range.mombasa <- c(0,4)
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, mombasa.data$incidence.store,mombasa.counterfactual.data$incidence.store,mombasa.optimal.data$incidence.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=1,plot.title="Overall incidence","Incidence (%)")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, mombasa.data$incidence.young.store,mombasa.counterfactual.data$incidence.young.store,mombasa.optimal.data$incidence.young.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="Incidence aged <25","Incidence (%)")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, mombasa.data$incidence.old.store,mombasa.counterfactual.data$incidence.old.store,mombasa.optimal.data$incidence.old.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="Incidence aged 25+","Incidence (%)")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, mombasa.data$incidence.virt.store,mombasa.counterfactual.data$incidence.virt.store,mombasa.optimal.data$incidence.virt.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="Incidence in virtual MSM","Incidence (%)")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, mombasa.data$incidence.both.store,mombasa.counterfactual.data$incidence.both.store,mombasa.optimal.data$incidence.both.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="Incidence in dual MSM","Incidence (%)")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, mombasa.data$incidence.phys.store,mombasa.counterfactual.data$incidence.phys.store,mombasa.optimal.data$incidence.phys.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="Incidence in physical MSM","Incidence (%)")
dev.off()



####### Prevalence plots:
x.range <- c(2018,2030)
plot.int.count.opt(kiambu.data$t,kiambu.counterfactual.data$t, kiambu.optimal.data$t, 100*kiambu.data$prev.all.store,100*kiambu.counterfactual.data$prev.all.store,100*kiambu.optimal.data$prev.all.store,lq,uq,x.range,y.range=c(0,40),plot.filename="kiambuincreasing_prevalence.pdf",plot.legend=1,plot.title="Overall prevalence (Kiambu)","Prevalence (%)")

plot.int.count.opt(kisumu.data$t,kisumu.counterfactual.data$t, kisumu.optimal.data$t, 100*kisumu.data$prev.all.store,100*kisumu.counterfactual.data$prev.all.store,100*kisumu.optimal.data$prev.all.store,lq,uq,x.range,y.range=c(0,12),plot.filename="kisumu_prevalence.pdf",plot.legend=1,plot.title="Overall prevalence (Kisumu)","Prevalence (%)")

plot.int.count.opt(mombasa.data$t,mombasa.counterfactual.data$t, mombasa.optimal.data$t, 100*mombasa.data$prev.all.store,100*mombasa.counterfactual.data$prev.all.store,100*mombasa.optimal.data$prev.all.store,lq,uq,x.range,y.range=c(0,25),plot.filename="mombasa_prevalence.pdf",plot.legend=1,plot.title="Overall prevalence (Mombasa)","Prevalence (%)")


# Prevalence panels:
pdf("kisumu_prev_panel.pdf")
par(mfrow=c(2,3))
y.range <- c(0,16)
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, 100*kisumu.data$prev.all.store,100*kisumu.counterfactual.data$prev.all.store,100*kisumu.optimal.data$prev.all.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=1,plot.title="Overall prevalence","Prevalence (%)")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, 100*kisumu.data$prev.young.store,100*kisumu.counterfactual.data$prev.young.store,100*kisumu.optimal.data$prev.young.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="Prevalence aged <25","Prevalence (%)")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, 100*kisumu.data$prev.old.store,100*kisumu.counterfactual.data$prev.old.store,100*kisumu.optimal.data$prev.old.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="Prevalence aged 25+","Prevalence (%)")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, 100*kisumu.data$prev.virt.store,100*kisumu.counterfactual.data$prev.virt.store,100*kisumu.optimal.data$prev.virt.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="Prevalence in virtual MSM","Prevalence (%)")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, 100*kisumu.data$prev.both.store,100*kisumu.counterfactual.data$prev.both.store,100*kisumu.optimal.data$prev.both.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="Prevalence in dual MSM","Prevalence (%)")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, 100*kisumu.data$prev.phys.store,100*kisumu.counterfactual.data$prev.phys.store,100*kisumu.optimal.data$prev.phys.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="Prevalence in physical MSM","Prevalence (%)")
dev.off()


pdf("kiambuincreasing_prev_panel.pdf")
par(mfrow=c(2,3))
y.range.kiambu <- c(0,40)
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, 100*kiambu.data$prev.all.store,100*kiambu.counterfactual.data$prev.all.store,100*kiambu.optimal.data$prev.all.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=1,plot.title="Overall prevalence","Prevalence (%)")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, 100*kiambu.data$prev.young.store,100*kiambu.counterfactual.data$prev.young.store,100*kiambu.optimal.data$prev.young.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="Prevalence aged <25","Prevalence (%)")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, 100*kiambu.data$prev.old.store,100*kiambu.counterfactual.data$prev.old.store,100*kiambu.optimal.data$prev.old.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="Prevalence aged 25+","Prevalence (%)")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, 100*kiambu.data$prev.virt.store,100*kiambu.counterfactual.data$prev.virt.store,100*kiambu.optimal.data$prev.virt.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="Prevalence in virtual MSM","Prevalence (%)")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, 100*kiambu.data$prev.both.store,100*kiambu.counterfactual.data$prev.both.store,100*kiambu.optimal.data$prev.both.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="Prevalence in dual MSM","Prevalence (%)")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, 100*kiambu.data$prev.phys.store,100*kiambu.counterfactual.data$prev.phys.store,100*kiambu.optimal.data$prev.phys.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="Prevalence in physical MSM","Prevalence (%)")
dev.off()


pdf("mombasa_prev_panel.pdf")
par(mfrow=c(2,3))
y.range.mombasa <- c(0,30)
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, 100*mombasa.data$prev.all.store,100*mombasa.counterfactual.data$prev.all.store,100*mombasa.optimal.data$prev.all.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=1,plot.title="Overall prevalence","Prevalence (%)")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, 100*mombasa.data$prev.young.store,100*mombasa.counterfactual.data$prev.young.store,100*mombasa.optimal.data$prev.young.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="Prevalence aged <25","Prevalence (%)")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, 100*mombasa.data$prev.old.store,100*mombasa.counterfactual.data$prev.old.store,100*mombasa.optimal.data$prev.old.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="Prevalence aged 25+","Prevalence (%)")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, 100*mombasa.data$prev.virt.store,100*mombasa.counterfactual.data$prev.virt.store,100*mombasa.optimal.data$prev.virt.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="Prevalence in virtual MSM","Prevalence (%)")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, 100*mombasa.data$prev.both.store,100*mombasa.counterfactual.data$prev.both.store,100*mombasa.optimal.data$prev.both.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="Prevalence in dual MSM","Prevalence (%)")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, 100*mombasa.data$prev.phys.store,100*mombasa.counterfactual.data$prev.phys.store,100*mombasa.optimal.data$prev.phys.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="Prevalence in physical MSM","Prevalence (%)")
dev.off()






####### On ART plots:
x.range <- c(2018,2030)
plot.int.count.opt(kiambu.data$t,kiambu.counterfactual.data$t, kiambu.optimal.data$t, 100*kiambu.data$prop.onart.store,100*kiambu.counterfactual.data$prop.onart.store,100*kiambu.optimal.data$prop.onart.store,lq,uq,x.range,y.range=c(0,100),plot.filename="kiambuincreasing_prop_onART.pdf",plot.legend=1,plot.title="Overall HIV+ on ART (Kiambu)","% of HIV+ on ART")

plot.int.count.opt(kisumu.data$t,kisumu.counterfactual.data$t, kisumu.optimal.data$t, 100*kisumu.data$prop.onart.store,100*kisumu.counterfactual.data$prop.onart.store,100*kisumu.optimal.data$prop.onart.store,lq,uq,x.range,y.range=c(0,100),plot.filename="kisumu_prop_onART.pdf",plot.legend=1,plot.title="Overall HIV+ on ART (Kisumu)","% of HIV+ on ART")

plot.int.count.opt(mombasa.data$t,mombasa.counterfactual.data$t, mombasa.optimal.data$t, 100*mombasa.data$prop.onart.store,100*mombasa.counterfactual.data$prop.onart.store,100*mombasa.optimal.data$prop.onart.store,lq,uq,x.range,y.range=c(0,100),plot.filename="mombasa_prop_onART.pdf",plot.legend=1,plot.title="Overall HIV+ on ART (Mombasa)","% of HIV+ on ART")


# On ART panels:
pdf("kisumu_onART_panel.pdf")
par(mfrow=c(2,3))
y.range <- c(0,100)
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, 100*kisumu.data$prop.onart.store,100*kisumu.counterfactual.data$prop.onart.store,100*kisumu.optimal.data$prop.onart.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=1,plot.title="Overall HIV+ on ART","% of HIV+ on ART")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, 100*kisumu.data$prop.onart.young.store,100*kisumu.counterfactual.data$prop.onart.young.store,100*kisumu.optimal.data$prop.onart.young.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART aged <25","% of HIV+ on ART")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, 100*kisumu.data$prop.onart.old.store,100*kisumu.counterfactual.data$prop.onart.old.store,100*kisumu.optimal.data$prop.onart.old.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART aged 25+","% of HIV+ on ART")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, 100*kisumu.data$prop.onart.virt.store,100*kisumu.counterfactual.data$prop.onart.virt.store,100*kisumu.optimal.data$prop.onart.virt.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART in virtual MSM","% of HIV+ on ART")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, 100*kisumu.data$prop.onart.both.store,100*kisumu.counterfactual.data$prop.onart.both.store,100*kisumu.optimal.data$prop.onart.both.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART in dual MSM","% of HIV+ on ART")
plot.int.count.opt(kisumu.data$t, kisumu.counterfactual.data$t, kisumu.optimal.data$t, 100*kisumu.data$prop.onart.phys.store,100*kisumu.counterfactual.data$prop.onart.phys.store,100*kisumu.optimal.data$prop.onart.phys.store,lq,uq,x.range,y.range,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART in physical MSM","% of HIV+ on ART")
dev.off()


pdf("kiambuincreasing_onART_panel.pdf")
par(mfrow=c(2,3))
y.range.kiambu <- c(0,100)
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, 100*kiambu.data$prop.onart.store,100*kiambu.counterfactual.data$prop.onart.store,100*kiambu.optimal.data$prop.onart.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=1,plot.title="Overall HIV+ on ART","% of HIV+ on ART")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, 100*kiambu.data$prop.onart.young.store,100*kiambu.counterfactual.data$prop.onart.young.store,100*kiambu.optimal.data$prop.onart.young.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART aged <25","% of HIV+ on ART")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, 100*kiambu.data$prop.onart.old.store,100*kiambu.counterfactual.data$prop.onart.old.store,100*kiambu.optimal.data$prop.onart.old.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART aged 25+","% of HIV+ on ART")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, 100*kiambu.data$prop.onart.virt.store,100*kiambu.counterfactual.data$prop.onart.virt.store,100*kiambu.optimal.data$prop.onart.virt.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART in virtual MSM","% of HIV+ on ART")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, 100*kiambu.data$prop.onart.both.store,100*kiambu.counterfactual.data$prop.onart.both.store,100*kiambu.optimal.data$prop.onart.both.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART in dual MSM","% of HIV+ on ART")
plot.int.count.opt(kiambu.data$t, kiambu.counterfactual.data$t, kiambu.optimal.data$t, 100*kiambu.data$prop.onart.phys.store,100*kiambu.counterfactual.data$prop.onart.phys.store,100*kiambu.optimal.data$prop.onart.phys.store,lq,uq,x.range,y.range.kiambu,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART in physical MSM","% of HIV+ on ART")
dev.off()


pdf("mombasa_onART_panel.pdf")
par(mfrow=c(2,3))
y.range.mombasa <- c(0,100)
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, 100*mombasa.data$prop.onart.store,100*mombasa.counterfactual.data$prop.onart.store,100*mombasa.optimal.data$prop.onart.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=1,plot.title="Overall HIV+ on ART","% of HIV+ on ART")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, 100*mombasa.data$prop.onart.young.store,100*mombasa.counterfactual.data$prop.onart.young.store,100*mombasa.optimal.data$prop.onart.young.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART aged <25","% of HIV+ on ART")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, 100*mombasa.data$prop.onart.old.store,100*mombasa.counterfactual.data$prop.onart.old.store,100*mombasa.optimal.data$prop.onart.old.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART aged 25+","% of HIV+ on ART")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, 100*mombasa.data$prop.onart.virt.store,100*mombasa.counterfactual.data$prop.onart.virt.store,100*mombasa.optimal.data$prop.onart.virt.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART in virtual MSM","% of HIV+ on ART")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, 100*mombasa.data$prop.onart.both.store,100*mombasa.counterfactual.data$prop.onart.both.store,100*mombasa.optimal.data$prop.onart.both.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART in dual MSM","% of HIV+ on ART")
plot.int.count.opt(mombasa.data$t, mombasa.counterfactual.data$t, mombasa.optimal.data$t, 100*mombasa.data$prop.onart.phys.store,100*mombasa.counterfactual.data$prop.onart.phys.store,100*mombasa.optimal.data$prop.onart.phys.store,lq,uq,x.range,y.range.mombasa,plot.filename=NA,plot.legend=0,plot.title="HIV+ on ART in physical MSM","% of HIV+ on ART")
dev.off()


















################################
## Old code:
################################

plot.polygon(t=kisumu.data$t,
             ylowerpolygon=apply(kisumu.data$incidence.store,1,quantile,lq),
             yupperpolygon=apply(kisumu.data$incidence.store,1,quantile,uq),
             ymean=rowMeans(kisumu.data$incidence.store),
                                        #ylowerdotted=apply(kisumu.data$incidence.store,1,quantile,0.025),
             ylowerdotted=NA,
             yupperdotted=NA,
             polygon.col=polygon.cols[1],lines.col=lines.cols[1],firstpolygon=1,x.range=x.range,y.range=y.range)


plot.polygon(t=kisumu.counterfactual.data$t,
             ylowerpolygon=apply(kisumu.counterfactual.data$incidence.store,1,quantile,lq),
             yupperpolygon=apply(kisumu.counterfactual.data$incidence.store,1,quantile,uq),
             ymean=rowMeans(kisumu.counterfactual.data$incidence.store),
                                        #ylowerdotted=apply(kisumu.counterfactual.data$incidence.store,1,quantile,0.025),
             ylowerdotted=NA,
             yupperdotted=NA,
             polygon.col=polygon.cols[2],lines.col=lines.cols[2],firstpolygon=0,x.range=x.range,y.range=y.range)

plot.polygon(t=kisumu.optimal.data$t,
             ylowerpolygon=apply(kisumu.optimal.data$incidence.store,1,quantile,lq),
             yupperpolygon=apply(kisumu.optimal.data$incidence.store,1,quantile,uq),
             ymean=rowMeans(kisumu.optimal.data$incidence.store),
             ylowerdotted=NA,
             yupperdotted=NA,
             polygon.col=polygon.cols[3],lines.col=lines.cols[3],firstpolygon=0,x.range=x.range,y.range=y.range)

    



lq <- 0.25
uq <- 0.75


                                        #polygon.cols<- c(adjustcolor(brewer.pal(n = 11, name = "RdYlBu")[8],alpha.f=alpha.adjust),adjustcolor(brewer.pal(n = 9, name = "Reds")[3],alpha.f=alpha.adjust),adjustcolor(brewer.pal(n = 9, name = "Greens")[3],alpha.f=alpha.adjust),adjustcolor(brewer.pal(n = 11, name = "BrBG")[4],alpha.f=alpha.adjust),adjustcolor(brewer.pal(n = 11, name = "PuOr")[5],alpha.f=alpha.adjust))

polygon.cols<- c(brewer.pal(n = 11, name = "RdYlBu")[8], brewer.pal(n = 9, name = "Reds")[3], brewer.pal(n = 9, name = "Greens")[3], brewer.pal(n = 11, name = "BrBG")[4], brewer.pal(n = 11, name = "PuOr")[5])

plot(kisumu.data$t,rowMeans(kisumu.data$incidence.store),type="l",lty=1,lwd=0.5, col="gray50",xlab="",ylab="Incidence (%)",cex.lab=1.4,cex.axis=1.2,xlim=c(2010,2030),ylim = c(0,3))

polygon(x=c(kisumu.data$t,kisumu.data$t[121],rev(kisumu.data$t),kisumu.data$t[1]),
        y=c(,apply(kisumu.data$incidence.store,1,quantile,uq)[1]),col=polygon.cols[1],border=NA)
lines(kisumu.data$t,rowMeans(kisumu.data$incidence.store))

polygon(x=c(kisumu.counterfactual.data$t,kisumu.counterfactual.data$t[121],rev(kisumu.counterfactual.data$t),kisumu.counterfactual.data$t[1]),
        y=c(apply(kisumu.counterfactual.data$incidence.store,1,quantile,lq),apply(kisumu.counterfactual.data$incidence.store,1,quantile,lq)[121],rev(apply(kisumu.counterfactual.data$incidence.store,1,quantile,uq)),apply(kisumu.counterfactual.data$incidence.store,1,quantile,uq)[1]),col=polygon.cols[2],border=NA)
lines(kisumu.counterfactual.data$t,rowMeans(kisumu.counterfactual.data$incidence.store))

polygon(x=c(kisumu.optimal.data$t,kisumu.optimal.data$t[121],rev(kisumu.optimal.data$t),kisumu.optimal.data$t[1]),
        y=c(apply(kisumu.optimal.data$incidence.store,1,quantile,lq),apply(kisumu.optimal.data$incidence.store,1,quantile,lq)[121],rev(apply(kisumu.optimal.data$incidence.store,1,quantile,uq)),apply(kisumu.optimal.data$incidence.store,1,quantile,uq)[1]),col=polygon.cols[3],border=NA)
lines(kisumu.optimal.data$t,rowMeans(kisumu.optimal.data$incidence.store))





#################################
# Understanding the change in % on ART:
#################################

summary(kiambu.data$prop.onart.store[i.pre.intervention.kiambu,])
summary(kiambu.data$prop.onart.store[i.post.intervention.kiambu,])
summary(kiambu.data$prop.onart.store[i.post.intervention.kiambu+1,])
summary(kiambu.data$prop.onart.store[i.post.intervention.kiambu+2,])
summary(kiambu.data$prop.onart.store[i.post.intervention.kiambu+5,])
summary(kiambu.data$prop.onart.store[i.post.intervention.kiambu+10,])
summary(kiambu.data$prop.onart.store[i.post.intervention.kiambu+15,])

summary(kisumu.data$prop.onart.store[i.pre.intervention.kisumu,])
summary(kisumu.data$prop.onart.store[i.post.intervention.kisumu,])
summary(kisumu.data$prop.onart.store[i.post.intervention.kisumu+1,])
summary(kisumu.data$prop.onart.store[i.post.intervention.kisumu+2,])
summary(kisumu.data$prop.onart.store[i.post.intervention.kisumu+5,])
summary(kisumu.data$prop.onart.store[i.post.intervention.kisumu+10,])
summary(kisumu.data$prop.onart.store[i.post.intervention.kisumu+15,])

summary(mombasa.data$prop.onart.store[i.pre.intervention.mombasa,])
summary(mombasa.data$prop.onart.store[i.post.intervention.mombasa,])
summary(mombasa.data$prop.onart.store[i.post.intervention.mombasa+1,])
summary(mombasa.data$prop.onart.store[i.post.intervention.mombasa+2,])
summary(mombasa.data$prop.onart.store[i.post.intervention.mombasa+5,])
summary(mombasa.data$prop.onart.store[i.post.intervention.mombasa+10,])
summary(mombasa.data$prop.onart.store[i.post.intervention.mombasa+15,])



summary(kiambu.data$prev.all.store[i.pre.intervention.kiambu,])
summary(kiambu.data$prev.all.store[i.post.intervention.kiambu,])
summary(kiambu.data$prev.all.store[i.post.intervention.kiambu+1,])
summary(kiambu.data$prev.all.store[i.post.intervention.kiambu+2,])
summary(kiambu.data$prev.all.store[i.post.intervention.kiambu+5,])
summary(kiambu.data$prev.all.store[i.post.intervention.kiambu+10,])
summary(kiambu.data$prev.all.store[i.post.intervention.kiambu+15,])

summary(kisumu.data$prev.all.store[i.pre.intervention.kisumu,])
summary(kisumu.data$prev.all.store[i.post.intervention.kisumu,])
summary(kisumu.data$prev.all.store[i.post.intervention.kisumu+1,])
summary(kisumu.data$prev.all.store[i.post.intervention.kisumu+2,])
summary(kisumu.data$prev.all.store[i.post.intervention.kisumu+5,])
summary(kisumu.data$prev.all.store[i.post.intervention.kisumu+10,])
summary(kisumu.data$prev.all.store[i.post.intervention.kisumu+15,])

summary(mombasa.data$prev.all.store[i.pre.intervention.mombasa,])
summary(mombasa.data$prev.all.store[i.post.intervention.mombasa,])
summary(mombasa.data$prev.all.store[i.post.intervention.mombasa+1,])
summary(mombasa.data$prev.all.store[i.post.intervention.mombasa+2,])
summary(mombasa.data$prev.all.store[i.post.intervention.mombasa+5,])
summary(mombasa.data$prev.all.store[i.post.intervention.mombasa+10,])
summary(mombasa.data$prev.all.store[i.post.intervention.mombasa+15,])


summary(kiambu.data$incidence.store[i.pre.intervention.kiambu,])
summary(kiambu.data$incidence.store[i.post.intervention.kiambu,])
summary(kiambu.data$incidence.store[i.post.intervention.kiambu+1,])
summary(kiambu.data$incidence.store[i.post.intervention.kiambu+2,])
summary(kiambu.data$incidence.store[i.post.intervention.kiambu+5,])
summary(kiambu.data$incidence.store[i.post.intervention.kiambu+10,])
summary(kiambu.data$incidence.store[i.post.intervention.kiambu+15,])

summary(kisumu.data$incidence.store[i.pre.intervention.kisumu,])
summary(kisumu.data$incidence.store[i.post.intervention.kisumu,])
summary(kisumu.data$incidence.store[i.post.intervention.kisumu+1,])
summary(kisumu.data$incidence.store[i.post.intervention.kisumu+2,])
summary(kisumu.data$incidence.store[i.post.intervention.kisumu+5,])
summary(kisumu.data$incidence.store[i.post.intervention.kisumu+10,])
summary(kisumu.data$incidence.store[i.post.intervention.kisumu+15,])

summary(mombasa.data$incidence.store[i.pre.intervention.mombasa,])
summary(mombasa.data$incidence.store[i.post.intervention.mombasa,])
summary(mombasa.data$incidence.store[i.post.intervention.mombasa+1,])
summary(mombasa.data$incidence.store[i.post.intervention.mombasa+2,])
summary(mombasa.data$incidence.store[i.post.intervention.mombasa+5,])
summary(mombasa.data$incidence.store[i.post.intervention.mombasa+10,])
summary(mombasa.data$incidence.store[i.post.intervention.mombasa+15,])















# Extract first run only:
outputs = extract.data(resultsdir,county,1)

cols.naturalhist <- c("brown","gray","purple")
plot(outputs$t,100*outputs$prop.chronic,type="l",ylim=c(0,100),col=cols.naturalhist[1],ylab="% by HIV stage")
lines(outputs$t,100*outputs$prop.late,col=cols.naturalhist[2])
lines(outputs$t,100*outputs$prop.acute,col=cols.naturalhist[3])
legend(x=1980,y=85,col=cols.naturalhist,legend=c("Chronic","Late","Acute"),lty=1,bty="n")




summary(kiambu.data$prop.acute.store[i.pre.intervention.kiambu,])
#   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#0.01643 0.02520 0.03280 0.03193 0.03971 0.04700 

summary(kisumu.data$prop.acute.store[i.pre.intervention.kisumu,])
#  Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#0.01549 0.02962 0.03553 0.03450 0.04150 0.04944 

summary(mombasa.data$prop.acute.store[i.pre.intervention.mombasa,])
#  Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#0.00987 0.01347 0.01823 0.01896 0.02360 0.03203 



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


