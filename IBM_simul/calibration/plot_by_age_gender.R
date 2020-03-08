rm(list=ls())
require(plotrix)


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





# Pull out the data from this file:
get.model.data <- function(model.data,r,outcome,gender,row,min.age,max.age,age.gp.width)
{
    
    age.groups <- seq(min.age,max.age,age.gp.width)
    n.age.groups <- length(age.groups)
    outcomes <- rep(0,n.age.groups)
    for (age in age.groups)
     {
         i <- which(age.groups==age)
         #print(i)
         dataname1 <- paste0("CohortRound",as.character(r),outcome,gender,as.character(age))
    

         start.col <- which(colnames(model.data)==dataname1)
         #print(start.col)
         outcomes[i] <- sum(model.data[row,seq(start.col,start.col+(age.gp.width-1))])
         #print(model.data[row,seq(start.col,start.col+(age.gp.width-1))])
      }
    return(outcomes)
}


    #plot.stuff(prev.m,prev.f,denom.m.prev,denom.f.prev,r,survey.data.prev[[r]],survey.data.prev.denom[[r]])

# plotrange is the y axis range.
plot.stuff <- function(prev.m.allruns,prev.f.allruns,denom.m.allruns,denom.f.allruns,r,survey.data.p,survey.data.n,plotrange=c(0,30),plot.title)
{
    #prev.m.allruns <- prev.m
    #prev.f.allruns <- prev.f
    #denom.m.allruns <- denom.m.prev
    #denom.f.allruns <- denom.f.prev
    #survey.data.p <- survey.data.prev[[5]]
    #survey.data.n <- survey.data.prev.denom[[5]]

    # Y axis goes from 0-20% in increments of 5%:
    tmp <- seq(plotrange[1],plotrange[2],10)
    round.label <- paste0("Round ",as.character(r))

    # Increase/reduce gap between M/F plots:
    gap.adjustment.scale <- 5
    # Used for plotting polygons:
    height_of_a_bar <- 0.8

    # Use this if doing a single plot only.
#pyramid.plot(lx=prev.m,rx=prev.f,gap=max(tmp/gap.adjustment.scale),laxlab = tmp, raxlab = tmp, xlim=range(tmp), labels=age_groups_lab,main=round.label,unit="")


    # Set up the plot axes:
    dummy.data <- rep(0, length(age_groups_lab))
    pyramid.plot(lx=dummy.data,rx=dummy.data,gap=max(tmp/gap.adjustment.scale),laxlab = tmp, raxlab = tmp, xlim=range(tmp), labels=age_groups_lab,main=round.label,unit="")


    
    # Plot HIV prevalence by age/gender:
    for(k in 1:nruns)
    {
        for(a in 1:(length(age_groups_lab)))
        {
            x <- c(-prev.m.allruns[[k]][a],0,0,-prev.m.allruns[[k]][a]) - max(tmp)/gap.adjustment.scale
            ymin <- a-height_of_a_bar/2+height_of_a_bar*(k-1)/nruns
            ymax <- a-height_of_a_bar/2+height_of_a_bar*k/nruns
            y <- c(ymin,ymin,ymax,ymax)
            polygon(x,y,col=col[a],border = NA)
            x <- c(prev.f[[k]][a],0,0,prev.f[[k]][a]) + max(tmp)/gap.adjustment.scale
            polygon(x,y,col=col[a],border = NA)
        }
    }
    # X axis label:
    mtext(side=1,line=2.5,plot.title)

                                        # Now plot the survey data and confidence interval:
    n.survey.data <- length(survey.data.p)
    n.survey.data.by.gender <- n.survey.data/2
    
    survey.prev.m <- 100*survey.data.p[1:n.survey.data.by.gender]
    survey.prev.f <- 100*survey.data.p[(n.survey.data.by.gender+1):n.survey.data]
    survey.prev.denom.m <- survey.data.n[1:n.survey.data.by.gender]
    survey.prev.denom.f <- survey.data.n[(n.survey.data.by.gender+1):length(survey.data)]

    points(-survey.prev.m - max(tmp/gap.adjustment.scale),1:length(age_groups_lab),pch=19)
    points(survey.prev.f + max(tmp/gap.adjustment.scale),1:length(age_groups_lab),pch=19)

    for(a in 1:(length(age_groups_lab)))
    {
        y <- survey.prev.m[a]
        se <- 100*sqrt(survey.prev.m[a]/100*(1.0-survey.prev.m[a]/100)/survey.prev.denom.m[a])
        
        segments(-(y-1.96*se) - max(tmp)/gap.adjustment.scale,a, -(y+1.96*se) - max(tmp)/gap.adjustment.scale,a)


        y <- survey.prev.f[a]
        se <- 100*sqrt(survey.prev.f[a]/100*(1.0-survey.prev.f[a]/100)/survey.prev.denom.f[a])

        segments((y-1.96*se) + max(tmp)/gap.adjustment.scale,a, (y+1.96*se) + max(tmp)/gap.adjustment.scale,a)

    }
}



#group.survey.data(survey.data["HIV+",],survey.data["All",], min.age, max.age, age.gp.width)
#numerator.ungrouped <- survey.data["HIV+",]
#denominator.ungrouped <- survey.data["All",]
group.survey.data  <- function(numerator.ungrouped, denominator.ungrouped, min.age, max.age, age.gp.width)
{
    both.genders <- c("M","F")
    
    n.age.groups.per.gender <- (max.age+1-min.age)/age.gp.width
    n.age.groups <- length(both.genders)*n.age.groups.per.gender
    outputs <- list()   # Store for prevalence and Ndenom.
    prev <- rep(0,n.age.groups)
    denom <- rep(0,n.age.groups)
    for (g in 1:length(both.genders))
    {
        this.gender <- both.genders[g]
        for (i in 1:n.age.groups.per.gender)
        {
            age <- min.age + (i-1)*age.gp.width
            label <- paste0(this.gender,as.character(age))
                                        # Index in the numerator/denominator
            i.start <- which(colnames(numerator.ungrouped)==label)
            numerator.sum <- sum(numerator.ungrouped[i.start:(i.start+age.gp.width-1)])
            denominator.sum <- sum(denominator.ungrouped[i.start:(i.start+age.gp.width-1)])     
            if (numerator.sum>denominator.sum)
            {
                print("Error - numerator>denominator")
            }
            if (denominator.sum>0)
            {
                prev[i+(g-1)*n.age.groups.per.gender] = numerator.sum/denominator.sum
            } else {
                prev[i+(g-1)*n.age.groups.per.gender] = 0
            }
            denom[i+(g-1)*n.age.groups.per.gender] <- denominator.sum

        }
    }
    outputs <- list(prev,denom)
    return(outputs)
}


#####################################################################
#Main code:
#####################################################################





infile = "Calibration_data_bestfits.csv"
#infile = "../results2/RESULTS1/Calibration_output_CL05_Zim_V2.0_patch0_Rand10_PCseed0_0.csv"
model.data <- read.csv(infile,header=T)
nruns <- dim(model.data)[1]

# We use rounds 1+2 at present:
rounds <- 5:6

survey.data.prev <- list()
survey.data.propaware <- list()
survey.data.proponART <- list()
survey.data.prev.denom <- list()
survey.data.propaware.denom <- list()
survey.data.proponART.denom <- list()

            

for (r in rounds)
{
                                        # Read in survey data
    survey.data <- read.csv(paste0("~/Dropbox (SPH Imperial College)/Manicaland/Model/CalibrationData/Manicalandr",as.character(r),"_calibration_data.txt"),sep=" ")

    temp <- group.survey.data(survey.data["HIV+",],survey.data["All",], min.age, max.age, age.gp.width)
    survey.data.prev[[r]] <- temp[[1]]
    survey.data.prev.denom[[r]] <- temp[[2]]
    # Set NAs to zero:
    #survey.data.prev[[r]][is.na(survey.data.prev[[r]])] <- 0


    temp <- group.survey.data(survey.data["AwareOfStatus",],survey.data["HIV+",], min.age, max.age, age.gp.width)
    survey.data.propaware[[r]] <- temp[[1]]
    survey.data.propaware.denom[[r]] <- temp[[2]]
    # Set NAs to zero:
    #survey.data.propaware[[r]][is.na(survey.data.propaware[[r]])] <- 0


    temp <- group.survey.data(survey.data["OnART",],survey.data["AwareOfStatus",], min.age, max.age, age.gp.width)
    survey.data.proponART[[r]] <- temp[[1]]
    survey.data.proponART.denom[[r]] <- temp[[2]]
    # Set NAs to zero:
    #survey.data.proponART[[r]][is.na(survey.data.proponART[[r]])] <- 0
    
}



for (r in rounds)
{
    # was list(1:nruns)
    denom.f.prev <- list()
    numerator.f.prev <- list()
    prev.f <- list()
    denom.m.prev <- list()
    numerator.m.prev <- list()
    prev.m <- list()

    denom.f.aware <- list()
    numerator.f.aware <- list()
    aware.f <- list()
    denom.m.aware <- list()
    numerator.m.aware <- list()
    aware.m <- list()

    denom.f.onart <- list()
    numerator.f.onart <- list()
    onart.f <- list()
    denom.m.onart <- list()
    numerator.m.onart <- list()
    onart.m <- list()



    for (row in 1:nruns)
    {
    
    
        outcome <- "Ntot"
        gender <- "F"
        denom.f.prev[[row]] <- get.model.data(model.data,r,outcome,gender,row,min.age,max.age,age.gp.width)
        outcome <- "Npos"
        numerator.f.prev[[row]] <- get.model.data(model.data,r,outcome,gender,row,min.age,max.age,age.gp.width)

        outcome <- "Ntot"
        gender <- "M"
        denom.m.prev[[row]] <- get.model.data(model.data,r,outcome,gender,row,min.age,max.age,age.gp.width)
        outcome <- "Npos"
        numerator.m.prev[[row]] <- get.model.data(model.data,r,outcome,gender,row,min.age,max.age,age.gp.width)

        ### Awareness
        outcome <- "Npos"
        gender <- "F"
        denom.f.aware[[row]] <- get.model.data(model.data,r,outcome,gender,row,min.age,max.age,age.gp.width)
        outcome <- "Naware"
        numerator.f.aware[[row]] <- get.model.data(model.data,r,outcome,gender,row,min.age,max.age,age.gp.width)

        outcome <- "Npos"
        gender <- "M"
        denom.m.aware[[row]] <- get.model.data(model.data,r,outcome,gender,row,min.age,max.age,age.gp.width)
        outcome <- "Naware"
        numerator.m.aware[[row]] <- get.model.data(model.data,r,outcome,gender,row,min.age,max.age,age.gp.width)


        ### On ART:
        outcome <- "Naware"
        gender <- "F"
        denom.f.onart[[row]] <- get.model.data(model.data,r,outcome,gender,row,min.age,max.age,age.gp.width)
        outcome <- "NonART"
        numerator.f.onart[[row]] <- get.model.data(model.data,r,outcome,gender,row,min.age,max.age,age.gp.width)

        outcome <- "Naware"
        gender <- "M"
        denom.m.onart[[row]] <- get.model.data(model.data,r,outcome,gender,row,min.age,max.age,age.gp.width)
        outcome <- "NonART"
        numerator.m.onart[[row]] <- get.model.data(model.data,r,outcome,gender,row,min.age,max.age,age.gp.width)


        
        prev.f[[row]] <- 100*numerator.f.prev[[row]]/denom.f.prev[[row]]
        prev.m[[row]] <- 100*numerator.m.prev[[row]]/denom.m.prev[[row]]

        aware.f[[row]] <- 100*numerator.f.aware[[row]]/denom.f.aware[[row]]
        aware.m[[row]] <- 100*numerator.m.aware[[row]]/denom.m.aware[[row]]

        onart.f[[row]] <- 100*numerator.f.onart[[row]]/denom.f.onart[[row]]
        onart.m[[row]] <- 100*numerator.m.onart[[row]]/denom.m.onart[[row]]

    }


    
    file.name <- paste0("HIVprevalenceRound",as.character(r),".pdf")
    pdf(file.name)
    plot.stuff(prev.m,prev.f,denom.m.prev,denom.f.prev,r,survey.data.prev[[r]],survey.data.prev.denom[[r]],c(0,40),"HIV prevalence (%)")
    dev.off()


    file.name <- paste0("HIVawareRound",as.character(r),".pdf")
    pdf(file.name)
    plot.stuff(aware.m,aware.f,denom.m.aware,denom.f.aware,r,survey.data.propaware[[r]],survey.data.propaware.denom[[r]],c(0,100),"% aware of status")
    dev.off()


    # Set NAs to zero:
    file.name <- paste0("HIVonARTRound",as.character(r),".pdf")
    pdf(file.name)
    plot.stuff(onart.m,onart.f,denom.m.onart,denom.f.onart,r,survey.data.proponART[[r]],survey.data.proponART.denom[[r]],c(0,100),"% on ART")
    dev.off()

    
}





