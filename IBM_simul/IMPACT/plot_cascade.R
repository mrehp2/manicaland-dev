

p.nobarrier <- c(0.005,0.2,0.25,0.5)
cascade <- 1-p.nobarrier

p1 <- c(1.0,0.8,0.75,0.005)
p2 <- c(1.0,1.0,0.8,0.2)
p3 <- c(1.0,1.0,1.0,0.25)
p4 <- c(1.0,1.0,1.0,0.5)

pdf("original_cascade.pdf")
this.plot1 <- barplot(100*p1,ylim=c(0,100),col="lightblue")
axis(1,this.plot1,labels=c("Population","Motivation","Access","Effective use"))
dev.off() 


pdf("cascade2.pdf")
this.plot2 <- barplot(100*p2,ylim=c(0,100),col="lightblue")
axis(1,this.plot2,labels=c("Population","Motivation","Access","Effective use"))
dev.off() 

pdf("cascade3.pdf")
this.plot3 <- barplot(100*p3,ylim=c(0,100),col="lightblue")
axis(1,this.plot3,labels=c("Population","Motivation","Access","Effective use"))
dev.off() 

pdf("cascade4.pdf")
this.plot4 <- barplot(100*p4,ylim=c(0,100),col="lightblue")
axis(1,this.plot4,labels=c("Population","Motivation","Access","Effective use"))
dev.off() 
