
resultsdir <- "params_essential/Output/"

a1 <- read.csv(paste0(resultsdir,"MIHPSA_output_CL05_Zim_patch0_Rand1_Run1_0.csv"))
a2 <- read.csv(paste0(resultsdir,"MIHPSA_output_CL05_Zim_patch0_Rand1_Run2_0.csv"))
a3 <- read.csv(paste0(resultsdir,"MIHPSA_output_CL05_Zim_patch0_Rand1_Run3_0.csv"))
a4 <- read.csv(paste0(resultsdir,"MIHPSA_output_CL05_Zim_patch0_Rand1_Run4_0.csv"))
a5 <- read.csv(paste0(resultsdir,"MIHPSA_output_CL05_Zim_patch0_Rand1_Run5_0.csv"))
a6 <- read.csv(paste0(resultsdir,"MIHPSA_output_CL05_Zim_patch0_Rand1_Run6_0.csv"))
a7 <- read.csv(paste0(resultsdir,"MIHPSA_output_CL05_Zim_patch0_Rand1_Run7_0.csv"))
a8 <- read.csv(paste0(resultsdir,"MIHPSA_output_CL05_Zim_patch0_Rand1_Run8_0.csv"))
a9 <- read.csv(paste0(resultsdir,"MIHPSA_output_CL05_Zim_patch0_Rand1_Run9_0.csv"))
a10 <- read.csv(paste0(resultsdir,"MIHPSA_output_CL05_Zim_patch0_Rand1_Run10_0.csv"))

## Check that there's nothing weird happening between different runs:
plot(a1$Year,(a1$YLL_15plus_male + a1$YLL_15plus_female))
lines(a2$Year,(a2$YLL_15plus_male + a2$YLL_15plus_female))
lines(a3$Year,(a3$YLL_15plus_male + a3$YLL_15plus_female))
lines(a4$Year,(a4$YLL_15plus_male + a4$YLL_15plus_female))
lines(a5$Year,(a5$YLL_15plus_male + a5$YLL_15plus_female))
lines(a6$Year,(a6$YLL_15plus_male + a6$YLL_15plus_female))
lines(a7$Year,(a7$YLL_15plus_male + a7$YLL_15plus_female))
lines(a8$Year,(a8$YLL_15plus_male + a8$YLL_15plus_female))
lines(a9$Year,(a9$YLL_15plus_male + a9$YLL_15plus_female))
lines(a10$Year,(a10$YLL_15plus_male + a10$YLL_15plus_female))


plot((a1$YLL_15plus_male + a1$YLL_15plus_female)[2:84]-(a1$YLL_15plus_male + a1$YLL_15plus_female)[1:83])
lines((a2$YLL_15plus_male + a2$YLL_15plus_female)[2:84]-(a2$YLL_15plus_male + a2$YLL_15plus_female)[1:83])
lines((a3$YLL_15plus_male + a3$YLL_15plus_female)[2:84]-(a3$YLL_15plus_male + a3$YLL_15plus_female)[1:83])
lines((a4$YLL_15plus_male + a4$YLL_15plus_female)[2:84]-(a4$YLL_15plus_male + a4$YLL_15plus_female)[1:83])


plot(a1$Year,a1$YLL_15plus_male)
lines(a1$Year,a1$YLL_15plus_female)

plot(a2$Year,a2$YLL_15plus_male)
lines(a2$Year,a2$YLL_15plus_female)

plot(a3$Year,a3$YLL_15plus_male)
lines(a3$Year,a3$YLL_15plus_female)


