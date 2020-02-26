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



plot.stuff <- function(prev.m.allruns,prev.f.allruns,denom.m.allruns,denom.f.allruns,r)
{
    # Y axis goes from 0-20% in increments of 5%:
    tmp <- seq(0,20,5)
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
    mtext(side=1,line=2.5,"HIV prevalence (%)")

    # Now plot the survey data and confidence interval:
    survey.prev.m <- prev.m.allruns[[10]]
    survey.prev.f <- prev.f.allruns[[10]]
    survey.prev.denom.m <- denom.m.allruns[[10]]
    survey.prev.denom.f <- denom.f.allruns[[10]]

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


#####################################################################
#Main code:
#####################################################################





infile = "Calibration_data_bestfits.csv"
#infile = "../results2/RESULTS1/Calibration_output_CL05_Zim_V2.0_patch0_Rand10_PCseed0_0.csv"

model.data <- read.csv(infile,header=T)

nruns <- dim(model.data)[1]

# We use rounds 1+2 at present:
rounds <- 1:2


for (r in rounds)
{
    denom.f.prev <- list(1:nruns)
    numerator.f.prev <- list(1:nruns)
    prev.f <- list(1:nruns)
    denom.m.prev <- list(1:nruns)
    numerator.m.prev <- list(1:nruns)
    prev.m <- list(1:nruns)

    denom.f.aware <- list(1:nruns)
    numerator.f.aware <- list(1:nruns)
    aware.f <- list(1:nruns)
    denom.m.aware <- list(1:nruns)
    numerator.m.aware <- list(1:nruns)
    aware.m <- list(1:nruns)

    denom.f.onart <- list(1:nruns)
    numerator.f.onart <- list(1:nruns)
    onart.f <- list(1:nruns)
    denom.m.onart <- list(1:nruns)
    numerator.m.onart <- list(1:nruns)
    onart.m <- list(1:nruns)



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
    plot.stuff(prev.m,prev.f,denom.m.prev,denom.f.prev,r)
    dev.off()


    file.name <- paste0("HIVawareRound",as.character(r),".pdf")
    pdf(file.name)
    plot.stuff(aware.m,aware.f,denom.m.aware,denom.f.aware,r)
    dev.off()

    file.name <- paste0("HIVonARTRound",as.character(r),".pdf")
    pdf(file.name)
    plot.stuff(onart.m,onart.f,denom.m.onart,denom.f.onart,r)
    dev.off()

    
}





