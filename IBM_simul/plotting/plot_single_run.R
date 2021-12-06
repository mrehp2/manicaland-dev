


rm(list=ls())
run.data <- read.csv("results/output_kisumu_run0.csv",header=T)

#define MSM_INDEX(a,typ) (a+(typ-1)*N_AGE_GPS)
#define HIVART_INDEX(hiv,art) (hiv + (art-1)*NHIVNATURALHISTORYCLASSES)
#define CASCADE_INDEX(hiv,art,testgp) (hiv + (art-1)*NHIVNATURALHISTORYCLASSES + (testgp-1)*NHIVCLASSES)


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



type.col <- c("blue","red","green")
plot(t,100*prev.virt,col=type.col[1],type="l",ylab="Prevalence by typology (%)",xlab="")
lines(t,100*prev.both,col=type.col[2],type="l")
lines(t,100*prev.phys,col=type.col[3],type="l")
legend("topleft",col=type.col,legend=c("Virtual","Both","Physical"),lty=1,bty="n")


age.col <- c("blue","green")
plot(t,100*prev.old,col=age.col[2],type="l",ylab="Prevalence by age (%)",xlab="")
lines(t,100*prev.young,col=age.col[1],type="l")
legend("topleft",col=age.col,legend=c("<25","25+"),lty=1,bty="n")






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



plot(t,100*prop.unaware.virt,col=type.col[1],type="l",ylab="% of HIV+ unaware by typology",xlab="")
lines(t,100*prop.unaware.both,col=type.col[2],type="l")
lines(t,100*prop.unaware.phys,col=type.col[3],type="l")
legend("topright",col=type.col,legend=c("Virtual","Both","Physical"),lty=1,bty="n")


plot(t,100*prop.unaware.old,col=age.col[2],type="l",ylab="% of HIV+ unaware by age",xlab="")
lines(t,100*prop.unaware.young,col=age.col[1],type="l")
legend("topright",col=age.col,legend=c("<25","25+"),lty=1,bty="n")










##################################################################
# Extras for validation/debugging:
##################################################################
prop.acute <- rowSums(run.data[,i.hiv.acute]) / (rowSums(run.data[,i.hiv.acute])+rowSums(run.data[,i.hiv.chronicandlate]))
prop.chronic <- rowSums(run.data[,i.hiv.chronic]) / (rowSums(run.data[,i.hiv.acute])+rowSums(run.data[,i.hiv.chronicandlate]))
prop.late<- rowSums(run.data[,i.hiv.late]) / rowSums(run.data[,i.hiv.chronicandlate])
cols.naturalhist <- c("brown","gray","purple")
plot(t,prop.chronic,type="l",ylim=c(0,1),col=cols.naturalhist[1])
lines(t,prop.late,col=cols.naturalhist[2])
lines(t,prop.acute,col=cols.naturalhist[3])
legend(x=2015,y=0.85,col=cols.naturalhist,legend=c("Chronic","Late","Acute"),lty=1,bty="n")



prop.virt <- denom.hiv.virt/(denom.hiv.virt+denom.hiv.both+denom.hiv.phys)
prop.both <- denom.hiv.both/(denom.hiv.virt+denom.hiv.both+denom.hiv.phys)
prop.phys <- denom.hiv.phys/(denom.hiv.virt+denom.hiv.both+denom.hiv.phys)
plot(t,100*prop.virt,col=type.col[1],type="l",ylab="% of population by typology",xlab="",ylim=c(0,100))
lines(t,100*prop.both,col=type.col[2],type="l")
lines(t,100*prop.phys,col=type.col[3],type="l")
legend("topright",col=type.col,legend=c("Virtual","Both","Physical"),lty=1,bty="n")

