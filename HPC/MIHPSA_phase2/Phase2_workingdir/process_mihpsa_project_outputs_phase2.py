import sys, os
import pandas

infile = "/home/mike/Dropbox (SPH Imperial College)/projects/MIHPSA_Zimabwe2021/Phase2/Output template MIHPSAZimP2_20230706.xlsx"
flows = pandas.read_excel(infile, sheet_name="Dictionary FLOW")
flows = flows.dropna(subset=['Variable name'])
flow_names = flows['Variable name'].values.tolist()
#print(flow_names)
#print(len(flow_names))

stocks = pandas.read_excel(infile, sheet_name="Dictionary STOCK ")
stocks = stocks.dropna(subset=['Variable name'])
stock_names = stocks['Variable name'].values.tolist()


## Perform checks:



def function_get_clean_varlist_and_outputs(varlist):
    i=0
    var_outputs = {}
    ordered_var_list = []
    nvar=len(varlist)
    while(i<nvar):
        if(varlist[i][-2:]=="_M"):
            if(i<(nvar-2)):
                if((varlist[i+1][-5:]=="_95LL") and (varlist[i+2][-5:]=="_95UL")):
                    ordered_var_list += [varlist[i]]
                    #print(varlist[i])
                    var_outputs[varlist[i]]="All"
                    i = i+3
                    # Next one is another mean:
                elif(varlist[i+1][-2:]=="_M"):
                    ordered_var_list += [varlist[i]]                
                    #print(varlist[i])
                    var_outputs[varlist[i]]="Median"
                    i = i+1
                elif((varlist[i+1][-4:]=="_95L") and (varlist[i+2][-5:]=="_95UL")):
                    ordered_var_list += [varlist[i]]                
                    #print(varlist[i])
                    var_outputs[varlist[i]]="All"
                    i = i+3
                elif((varlist[i+1]=="NHIV_FSW1599_LL") and (varlist[i+2]=="NHIV_FSW1599_UL")):
                    ordered_var_list += [varlist[i]]
                    #print(varlist[i])
                    var_outputs[varlist[i]]="All"
                    i = i+3
                else:
                    print("Error - variables don't fit format. Exiting\n")
                    print(varlist[i],varlist[i+1],varlist[i+2])
                    sys.exit(1)
            elif(i<nvar):
                if(varlist[i][-2:]=="_M"):
                    ordered_var_list += [varlist[i]]
                    #print(varlist[i])
                    var_outputs[varlist[i]]="Median"
                    i = i+1
                else:
                    print("Help1!")
                    print(i,nvar)
                    print(varlist[i+1])
                    sys.exit(1)
                    
            else:
                print("Help2!")
                print(i,nvar)
                print(varlist[i])
                sys.exit(1)
        elif(varlist[i].rstrip()=="We refer to the number of test episode not number of test kits"):
            i = i+1
        else:
            print("Help3!")
            print(i,nvar)
            print(varlist[i]+"X")
            sys.exit(1)
                    

    return [var_outputs, ordered_var_list]



[flowname_dict,flow_varlist] = function_get_clean_varlist_and_outputs(flow_names)

[stockname_dict,stock_varlist] = function_get_clean_varlist_and_outputs(stock_names)


## Check for duplicates:
import collections
a = stockname_dict.keys()
stock_duplicates = [item for item, count in collections.Counter(a).items() if count > 1]
if(stock_duplicates!=[]):
    print("Duplicates in stock:")
    print(stock_duplicates)
a = flowname_dict.keys()
flow_duplicates = [item for item, count in collections.Counter(a).items() if count > 1]
if(len(flow_duplicates)>0):
    print("Duplicates in flow:")
    print(flow_duplicates)

PRINTVARS = 0
if(PRINTVARS==1):
    print("Flow variables (e.g. incidence):")
    for i in flowname_dict.keys():
        print(i)

    print("Stock variables (e.g. prevalence):")
    for i in stockname_dict.keys():
        print(i)



## Flow variables (e.g. incidence):

## Convert between Vale's and my variables.
## "X" means I don't have it as an output right now.
flow_variable_dictionary = {"NAlive_Fbirth1599_M":"X",
"NHIV_Fbirth1599_M":"X",
"NAlive_FbirthBF1599_M":"X",
"NHIV_FbirthBF1599_M":"X",
"NAlive_FpregEverBirth1524_M":"X",
"NHIV_FpregEverBirth1524_M":"X",
"NAlive_A01_M":"newbirths",
"NAlive_HIVPOSmum_A01_M":"X",
"NHIV_HIVPOSmum_A01_M":"newbirths_HIVpos",
"HIVIncid_M1549_M":"IncidenceM15_49",
"HIVIncid_F1549_M":"IncidenceF15_49",
"HIVIncid_A1549_M":"Incidencetotal15_49",
"HIVIncid_F1524_M":"IncidenceF15_24",
"HIVIncid_FSW1599_M":"X",
"HIVIncid_SDCA1599_M":"X", ## Incidence in 15+ with HIV+ partner.
"HIVIncid_SDCF1599_M":"X",
"HIVIncid_MSM1599_M":"X",
"HIVIncid_pregbfF1549_M":"X",
"HIVIncid_occA1599_M":"X",
"HIVIncid_gbvF1599_M":"X",
"NHIVInf_M1599_M":"Nincidentcases_M15plus",
"NHIVInf_F1599_M":"Nincidentcases_F15plus",
"NHIVInf_A014_M":"X",
"NHIVInf_M1549_M":"New_cases_M15_49",
"NHIVInf_F1549_M":"New_cases_F15_49",
"NHIVInf_A1549_M":"New_cases_total15_49",
"NHIVInf_M1524_M":"New_cases_M15_24",
"NHIVInf_F1524_M":"New_cases_F15_24",
"NHIVInf_M2549_M":"New_cases_M25_49",
"NHIVInf_F2549_M":"New_cases_F25_49",
"AIDSDeaths_M1599_M":"AIDSdeaths_M15plus",
"AIDSDeaths_F1599_M":"AIDSdeaths_F15plus",
"AIDSDeaths_A1599_M":"AIDSdeaths_total",
"AIDSDeaths_A014_M":"X",  ## In future use AIDSdeaths_child
"TOTDeaths_M1599_M":"totaldeaths_M15plus",
"TOTDeaths_F1599_M":"totaldeaths_F15plus",
"TOTDeaths_A014_M":"X",
"YLL_AgeGenLifeExpect_A1599_M":"X",
"YLL_AgeGenLifeExpect_A014_M":"X",
"YLL_AgeGenLifeExpect_3Disc_A1599_M":"YLL_15plus",
"YLL_AgeGenLifeExpect_3Disc_A014_M":"X",
"Ntested_ANCPD_F1599_M":"X",
"Ntests_ANCPD_F1599_M":"X",
"Ntested_A06m_M":"X",
"Ntested_EndBF_Inf_M":"X",
"NHIVST_PD_M1599_M":"X",
"NHIVST_PD_F1599_M":"X",
"NHIVST_SDNP_M1599_M":"X",
"NHIVST_SDNP_F1599_M":"X",
"NHIVST_SDPARTNER_M1599_M":"X",
"NHIVST_SDPARTNER_F1599_M":"X",
"Ntests_FACSYMPT_M1599_M":"X",
"Ntests_FACSYMPT_F1599_M":"X",
"Ntests_FACNOSYMPT_M1599_M":"X",
"Ntests_FACNOSYMPT_F1599_M":"X",
"Ntests_FAC_A014_M":"X",
"Ntests_IndexFAC_M1599_M":"X",
"Ntests_IndexFAC_F1599_M":"X",
"Ntests_RecInf_M1599_M":"X",
"Ntests_RecInf_F1599_M":"X",
"Ntests_COM_M1599_M":"X",
"Ntests_COM_F1599_M":"X",
"Ntested_FSWprog_FSW1599_M":"X",
"Ntests_FSW1599_M":"X",
"Ntested_MSMprog_MSM1599_M":"X",
"Ntests_MSM1599_M":"X",
"Ntested_TGprog_TG1599_M":"X",
"Ntests_TG1599_M":"X",
"TOTTests_M1599_M":"X",
"TOTTests_F1599_M":"X",
"TOTTests_A1599_M":"X",
"TOTTests_A014_M":"X",
"TOTHIVST_M1599_M":"X",
"TOTHIVST_F1599_M":"X",
"TOTHIVST_A014_M":"X",
"NPosTests_ANCPD_F1599_M":"X",
"NPostTest_A06m_M":"X",
"NPosTests_EndBF_Inf_M":"X",
"NPosConfHIVST_PD_M1599_M":"X",
"NPosConfHIVST_PD_F1599_M":"X",
"NPosConfHIVST_SDNP_M1599_M":"X",
"NPosConfHIVST_SDNP_F1599_M":"X",
"NPosConfHIVST_SDPARTNER_M1599_M":"X",
"NPosConfHIVST_SDPARTNER_F1599_M":"X",
"NPosTests_FAC_M1599_M":"X",
"NPosTests_FAC_F1599_M":"X",
"NPosTests_FAC_A014_M":"X",
"NPosTests_IndexFAC_M1599_M":"X",
"NPosTests_IndexFAC_F1599_M":"X",
"NPosTests_RecInf_M1599_M":"X",
"NPosTests_RecInf_F1599_M":"X",
"NPosTests_COM_M1599_M":"X",
"NPosTests_COM_F1599_M":"X",
"NPosTests_FSWprog_FSW1599_M":"X",
"NPosTests_FSW1599_M":"X",
"NPosTests_MSMprog_MSM1599_M":"X",
"NPosTests_MSM1599_M":"X",
"NPosTests_Tgprog_TG1599Tested_M":"X",
"NPosTests_TG1599_M":"X",
"TOTPosTests_M1599_M":"X",
"TOTPosTests_F1599_M":"X",
"TOTPosTests_A014_M":"X",
"TOTPosConfHIVST_M1599_M":"X",
"TOTPosConfHIVST_F1599_M":"X",
"PosRate_M1599_M":"Prop_tests_pos_M15plus",
"PosRate_F1599_M":"Prop_tests_pos_F15plus",
"PosRate_A1599_M":"Prop_tests_pos_15plus",
"PosRate_F1524_M":"X",  ## To add
"PosRate_FSW1599_M":"X",
"PosRate_MSM1529_M":"X",
"NDREAMS_F1524_M":"X",
"NDREAMSEver_F1524_M":"X",
"NDREAMS_NEGF1524_M":"X",
"NDREAMSEver_NEGF1524_M":"X",
"NFSWprog_FSW1599_M":"X",
"NFSWprogEver_FSW1599_M":"X",
"NMSMprog_MSM1599_M":"X",
"NMSMprogEver_MSM1599_M":"X",
"NSBCC_A1599_M":"X",
"NUEU_A1599_M":"X",
"NCUPP_A1599_M":"X",
"NCondoms_A1599_M":"X",
"NGPMHC_DiagM1599_M":"X",
"NGPMHC_M1599_M":"X",
"NVMMC_M1549_M":"N_VMMC_annual_15_49",
"NTDFPrEPinit_F1524_M":"X",
"NTDFPrEP_F1524_M":"N_women_at_elevatedrisk_andonoralPrEP_15to24",
"NTDFPrEPCT_F1524_M":"X", ## Add me!
"NTDFPrEPEver_F1524_M":"X",
"NTDFPrEPinit_FSW1599_M":"X",
"NTDFPrEP_FSW1599_M":"X",
"NTDFPrEPCT_FSW1599_M":"X",
"NTDFPrEPEver_FSW1599_M":"X",
"NTDFPrEPinit_SDCA1599_M":"X",
"NTDFPrEP_SDCA1599_M":"X",
"NTDFPrEPCT_SDCA1599_M":"X",
"NTDFPrEPEver_SDCA1599_M":"X",
"NTDFPrEPinit_MSM1599_M":"X",
"NTDFPrEP_MSM1599_M":"X",
"NTDFPrEPCT_MSM1599_M":"X",
"NTDFPrEPEver_MSM1599_M":"X",
"NTDFPrEPinit_pregbfF1549_M":"X",
"NTDFPrEP_pregbfF1549_M":"X",
"NTDFPrEPCT_pregbfF1549_M":"X",
"NTDFPrEPEver_pregbfF1549_M":"X",
"NDPVPrEPinit_F1524_M":"X",
"NDPVPrEP_F1524_M":"X",
"NDPVPrEPCT_F1524_M":"X",
"NDPVPrEPEver_F1524_M":"X",
"NDPVPrEPinit_FSW1599_M":"X",
"NDPVPrEP_FSW1599_M":"X",
"NDPVPrEPCT_FSW1599_M":"X",
"NDPVPrEPEver_FSW1599_M":"X",
"NDPVPrEPinit_SDCF1599_M":"X",
"NDPVPrEP_SDCF1599_M":"X",
"NDPVPrEPCT_SDCF1599_M":"X",
"NDPVPrEPEver_SDCF1599_M":"X",
"NDPVPrEPinit_pregbfF1549_M":"X",
"NDPVPrEP_pregbfF1549_M":"X",
"NDPVPrEPCT_pregbfF1549_M":"X",
"NDPVPrEPEver_pregbfF1549_M":"X",
"NCABPrEPinit_F1524_M":"X",
"NCABPrEP_F1524_M":"X",
"NCABPrEPCT_F1524_M":"X",
"NCABPrEPEver_F1524_M":"X",
"NCABPrEPinit_FSW1599_M":"X",
"NCABPrEP_FSW1599_M":"X",
"NCABPrEPCT_FSW1599_M":"X",
"NCABPrEPEver_FSW1599_M":"X",
"NCABPrEPinit_SDCA1599_M":"X",
"NCABPrEP_SDCA1599_M":"X",
"NCABPrEPCT_SDCA1599_M":"X",
"NCABPrEPEver_SDCA1599_M":"X",
"NCABPrEPinit_MSM1599_M":"X",
"NCABPrEP_MSM1599_M":"X",
"NCABPrEPCT_MSM1599_M":"X",
"NCABPrEPEver_MSM1599_M":"X",
"NCABPrEPinit_pregbfF1549_M":"X",
"NCABPrEP_pregbfF1549_M":"X",
"NCABPrEPCT_pregbfF1549_M":"X",
"NCABPrEPEver_pregbfF1549_M":"X",
"NPEPocc_A1599_M":"X",
"NPEPoccEver_A1599_M":"X",
"NPEPgbv_F1599_M":"X",
"NPEPgbvEver_F1599_M":"X",
"NPMTCT_FbirthHIV1599_M":"X",
"NARTinit_A1599_M":"X",   ## Add me
"NARTreinit_A1599_M":"X",
"NTreatFail_A1599_M":"X",
"N_A1599_CD4_M":"X",
"NCD4_A1599_M":"X",
"NMCD4lt350_A1599_M":"X",
"NMCD4lt200_A1599_M":"X",
"N_CTX_A1599_M":"X",
"N_CTX_A014_M":"X",
"NAHD_A1599_M":"X",
"NIdentAHD_A1599_M":"X",
"NScreenCM_A1599AHD_M":"X",
"NScreenCM_A014_M":"X",
"NScreenTB_A1599AHD_M":"X",
"NScreenTB_A014_M":"X",
"NPrevTreatCrypt_A1599_M":"X",
"NPrevTreatCrypt_A014_M":"X",
"NTreatCrypt_A1599_M":"X",
"NTreatCrypt_A014_M":"X",
"NTreatTB_A1599_M":"X",
"NTreatTB_A014_M":"X",
"NAIDS_A1599_M":"X",
"NTreatAIDS_A1599_M":"X",
"NVLtested_A1599_M":"X",
"NVLtested_A014_M":"X",
"NVL_A1599_M":"X",
"NVL_A014_M":"X",
"N_A1599_POCCD4_M":"X",
"NPOCCD4_A1599_M":"X",
"N_A1599_POCVL_M":"X",
"N_A014_POCVL_M":"X",
"NPOCVL_A1599_M":"X",
"NPOCVL_A014_M":"X",
"NCRF_A1599_M":"X",
"NCATS_HIVPOSA1524_M":"X",
"NCATS_HIVNEGA1524_M":"X",
"NERC_HIVPOSA1524_M":"X",
"NERC_HIVNEGA1524_M":"X",
"NYMM_HIVPOSFpregEverBirth1524_M":"X",
"NMVLgt1000_A1599_M":"X",
"NMVLgt1000Ever_A1599_M":"X",
"N_ADHCVIR_MVLgt1000EverA1599_M":"X",
"N_ADHCADO_A1524_M":"X"}


##Stocks:
stock_variable_dictionary = {"HIVprev_M1549_M":"PrevalenceM15_49",
"HIVprev_F1549_M":"PrevalenceF15_49",
"HIVprev_A1549_M":"PrevalenceAll15_49",
"HIVprev_pregF1549_M":"X",
"HIVprev_F1524_M":"PrevalenceF15_24",
"HIVprev_FSW1599_M":"X",
"HIVprev_MSM1599_M":"X",
"HIVprev_TG1599_M":"X",
"NAlive_M1599_M":"Npop_M15plus",
"NAlive_F1599_M":"Npop_F15plus",
"NAlive_A014_M":"Npop_child",
"NAlive_M1524_M":"Npop_M15_24",
"NAlive_F1524_M":"Npop_F15_24",
"NAlive_M2549_M":"Npop_M25_49",
"NAlive_F2549_M":"Npop_F25_49",
"NAlive_FSW1599_M":"X",
"NAlive_MSM1599_M":"X",
"NAlive_TG1599_M":"X",
"Nalive_NEGInSDA1599_M":"N_HIVneg_in_SD_partnership_15plus",
"Nalive_NEGInSDNotOnARTA1599_M":"N_HIVneg_in_SD_partnership_noART_15plus",
"Nalive_NEGInSDF1599_M":"N_HIVneg_in_SD_partnership_F15plus",
"Nalive_NEGInSDNotOnARTF1599_M":"N_HIVneg_in_SD_partnership_noART_F15plus",
"NHIV_M1599_M":"Npos_M15plus",
"NHIV_F1599_M":"Npos_F15plus",
"NHIV_A014_M":"Npos_child",
"NHIV_M1524_M":"Npos_M15_24",
"NHIV_F1524_M":"Npos_F15_24",
"NHIV_M2549_M":"Npos_M25_49",
"NHIV_F2549_M":"Npos_F25_49",
"NHIV_FSW1599_M":"X",
"NHIV_MSM1599_M":"X",
"NHIV_TG1599_M":"X",
"NHIV_A1599_NoART_CD4500pl_M":"n_notonART_byCD4_15plus_gt500",
"NHIV_A1599_NoART_CD4350499_M":"n_notonART_byCD4_15plus_350_500",
"NHIV_A1599_NoART_CD4200349_M":"n_notonART_byCD4_15plus_200_350",
"NHIV_A1599_NoART_CD450199_M":"n_notonART_byCD4_15plus_50_200",
"NHIV_A1599_NoART_CD4050_M":"n_notonART_byCD4_15plus_lt50",
"NHIV_A014_NoART_CD4500pl_M":"X",
"NHIV_A014_NoART_CD4350499_M":"X",
"NHIV_A014_NoART_CD4200349_M":"X",
"NHIV_A014_NoART_CD450199_M":"X",
"NHIV_A014_NoART_CD4050_M":"X",
"NHIV_A1599_Asympt_Undiag_M":"X",
"NHIV_A1599_Asympt_Diag_NoART_M":"X",
"NHIV_A1599_Asympt_Diag_ART_M":"X",
"NHIV_A1599_Sympt_NOAIDS_M":"X",
"NHIV_A1599_Sympt_AIDS_M":"X",
"NHIV_A014_Asympt_Undiag_M":"X",
"NHIV_A014_Asympt_Diag_NoART_M":"X",
"NHIV_A014_Asympt_Diag_ART_M":"X",
"NHIV_A014_Sympt_NOAIDS_M":"X",
"NHIV_A014_Sympt_AIDS_M":"X",
"P_DIAG_A1599_M":"PropDiagnosed_15plus",
"P_DIAG_M1599_M":"PropDiagnosed_M15plus",
"P_DIAG_F1599_M":"PropDiagnosed_F15plus",
"P_DIAG_A014_M":"X",
"P_DIAG_M1524_M":"PropDiagnosed_M15_24",
"P_DIAG_F1524_M":"PropDiagnosed_F15_24",
"P_DIAG_FSW1599_M":"X",
"P_DIAG_MSM1599_M":"X",
"P_EVERSEX_M1599_M":"prop_eversex_M15plus",
"P_EVERSEX_F1599_M":"prop_eversex_F15plus",
"P_EVERSEX_F1524_M":"prop_eversex_F15_24",
"P_EVERSEX_MSM1599_M":"X",
"P_CONDOMLAST_M1599_M":"prop_usedcondomlastact_M15plus",
"P_CONDOMLAST_F1599_M":"prop_usedcondomlastact_F15plus",
"P_CONDOMLAST_F1524_M":"PropF15_24_condlasttime",
"P_CONDOMLAST_FSW1599_M":"X",
"P_CONDOMLAST_MSM1599_M":"X",
"P_CLS3m_M1599_M":"X",
"P_CLS3m_F1599_M":"X",
"P_CLS3m_F1524_M":"X",
"P_CLS3m_FSW_M":"X",
"P_CLS3m_MSM_M":"X",
"P_STI_FSW1599_M":"X",
"P_STI_MSM1599_M":"X",
"NAlive_ElevRiskF1524_M":"N_women_at_elevatedrisk_15to24",
"P_TDFPrEP_ElevRiskF1524_M":"prop_women_at_elevatedrisk_andonPrEP_15to24",
"NAlive_FPregBirthBF1599_M":"X",
"P_TDFPrEP_FPregBirthBF1599_M":"X",
"P_DPVPrEP_ElevRiskF1524_M":"X",
"P_DPVPrEP_FPregBirthBF1599_M":"X",
"P_CABPrEP_ElevRiskF1524_M":"X",
"P_CABPrEP_FPregBirthBF1599_M":"X",
"CIRC_PREV_M1549_M":"prop_circ_15_49",
"NOnART_M1599_M":"N_ART_M_15plus",
"NOnART_F1599_M":"N_ART_F_15plus",
"NOnART_A1524_M":"nonART_15_24",
"NOnART_A1599_M":"N_ART_total",
"NOnART_A014_M":"X", ## N_ART_child
"P_onART_DiagM1599_M":"Diagnosed_onART_M_15plus",
"P_onART_DiagF1599_M":"Diagnosed_onART_F_15plus",
"P_onART_DiagF1524_M":"Diagnosed_onART_F_15_24",
"P_onART_DiagA1524_M":"Diagnosed_onART_15_24",
"P_onART_DiagA1599_M":"Diagnosed_onART_15plus",
"P_onART_DiagA014_M":"X",
"P_onART_DiagFSW1599_M":"X",
"P_onART_DiagMSM1599_M":"X",
"P_onART_Diag12mAHDA1599_M":"X",
"P_onART_Diag12mNOAHDA1599_M":"X",
"P_onART_Diag12mAHDA014_M":"X",
"P_onART_Diag12mNOAHDA014_M":"X",
"P_onART_Diag12mAHDA1524_M":"X",
"P_onART_Diag12mNOAHDA1524_M":"X",
"P_onART_HIVM1599_M":"ARTcoverage_M_15plus",
"P_onART_HIVF1599_M":"ARTcoverage_F_15plus",
"P_onART_HIVF1524_M":"ARTcoverage_F_15_24",
"P_onART_HIVA1524_M":"ARTcoverage_15_24",
"P_onART_HIVA1599_M":"ARTcoverage_total",
"P_onART_HIVA014_M":"X", ## ARTcoverage_child
"P_onART_HIVFSW1599_M":"X",
"P_onART_HIVMSM1599_M":"X",
"P_onART_ExpM1599_M":"prop_ARTexperienced_M15plus",   ## To check.
"P_onART_ExpF1599_M":"prop_ARTexperienced_F15plus",
"P_onART_ExpA1524_M":"prop_ARTexperienced_15_24",
"P_onART_ExpA1599_M":"prop_ARTexperienced_15plus",
"P_onART_ExpA014_M":"X",
"P_onART_ExpFSW1599_M":"X",
"P_onART_ExpMSM1599_M":"X",
"P_onART_ExpFpregEverBirth1524_M":"X",
"P_VLS_onARTA1599_M":"PropAdultVS",
"P_VLS_onARTA1524_M":"prop_VS_adult15_24",
"P_VLS_onARTA014_M":"X",
"P_VLS_onARTpregEverBirthF1524_M":"X",
"P_VLS_onARTMVLgt1000EverA1599_M":"X"}


if(set(stock_variable_dictionary.keys())==set(stock_varlist)):
    print("Stocks match")
else:
    print("Mismatch in stocks")
    print("In my dictionary but not in Excel file:")
    print(list(set(stock_variable_dictionary.keys())-set(stock_varlist)))
    print("In Excel file but not in my dictionary:")
    print(list(set(stock_varlist) - set(stock_variable_dictionary.keys())))
    #print(stock_varlist)
    
if(set(flow_variable_dictionary.keys())==set(flow_varlist)):
    print("Flows match")
else:
    print("Mismatch in flows")
    print("In my dictionary but not in Excel file:")
    print(list(set(flow_variable_dictionary.keys())-set(flow_varlist)))
    print("In Excel file but not in my dictionary:")
    print(list(set(flow_varlist) - set(flow_variable_dictionary.keys())))
    #print(flow_varlist)
