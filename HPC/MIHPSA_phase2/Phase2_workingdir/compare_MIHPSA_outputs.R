

infile1.stocks = read.csv("MIHPSA_project_outputs_phase2_essentialplusPrEP_stocks.csv")
infile1.flows = read.csv("MIHPSA_project_outputs_phase2_essentialplusPrEP_flows.csv")
infile2.stocks = read.csv("copy_outputs_Aug2023/MIHPSA_project_outputs_phase2_essentialplusPrEP_stocks.csv")
infile2.flows = read.csv("copy_outputs_Aug2023/MIHPSA_project_outputs_phase2_essentialplusPrEP_flows.csv")


plot.compare <- function(df1,df2,varname){
    i <- which(colnames(df1) %in% varname)
    if(length(i)>1)
        stop("Ambiguous varname")
    plot(df1$t,df1[,i])
    lines(df2$t,df2[,i])
}

plot.compare(infile1.stocks,infile2.stocks,"HIVprev_A1549_M")
plot.compare(infile1.stocks,infile2.stocks,"HIVprev_F1524_M")



plot.compare(infile2.flows,infile1.flows,"NTDFPrEPinit_F1524_M")
plot.compare(infile2.flows,infile1.flows,"NTDFPrEPCT_F1524_M")

plot.compare(infile2.flows,infile1.flows,"NTDFPrEPCT_F1524_M")
plot.compare(infile2.flows,infile1.flows,"HIVIncid_A1549_M")



#plot(infile1.stocks$t,infile1.stocks$HIVprev_M1549_M)
#lines(infile2.stocks$t,infile2.stocks$HIVprev_M1549_M)

#plot(infile1.stocks$t,infile1.stocks$HIVprev_F1524_M)
#lines(infile2.stocks$t,infile2.stocks$HIVprev_F1524_M)


