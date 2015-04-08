# Pi0Tools
Tools for Pi0 Analysis

###Python scripts:
#### 1) Plotter:
Plots the invariant mass of a determined selection given by the user through input parameters.
Instructions to run the Plotter:

python python/Plotter.py 
-i /tmp/rateixei/eos/cms/store/caf/user/lpernie/ALL_MINBIAS_UNCAL_L1_NOL1FILTER_40PU50ns_EB_eta_NewSeed/iter_0/epsilonPlots_0.root -e -b --NCr1=4 --NCr2=4 --PtClu=1.6 --S4S9=0.9 --Iso=0.15 --PtDi=3.6 --name=Teste2 -f  
#####Options:
-e (-e for Eta, -p for pi0)  
-b (-b for barrel, -c for endcap)  
--NCr1=4 --NCr2=4: Cut on number of cristals of each cluster  
--PtClu=1.6: Cut on clusters pt  
--S4S9=0.9: Cut on S4/S9  
--Iso=0.15: Cut on Isolation (HLT Iso)  
--PtDi=3.6: Cut on Eta/Pi0 Pt  
--name=Teste2: Name of output pdf  
--HltIsoOff: Use standard iso instead of HLT iso (hlt is default)  
--CutCorrOff: Cut on uncorrected variables (cut on corrected is default)  
--PlotCorrOff: Plot uncorrected mass distribution (plot corrected is default)  
-f: <b>Use this flag if you want to also produce the fit</b>

--> Currently works only with local files =/  
--> Location of Minimum bias Neutrino gun MC processed trees:  
/store/caf/user/lpernie/ALL_MINBIAS_UNCAL_L1_NOL1FILTER_40PU50ns_EB_eta_NewSeed
/store/caf/user/lpernie/ALL_MINBIAS_UNCAL_L1_NOL1FILTER_40PU50ns_EB_pi0_NewSeed
/store/caf/user/lpernie/ALL_MINBIAS_UNCAL_L1_NOL1FILTER_40PU50ns_EE_eta_NewSeed
/store/caf/user/lpernie/ALL_MINBIAS_UNCAL_L1_NOL1FILTER_40PU50ns_EE_pi0_NewSeed_v2

#### 2) Optimizer:
Can be used to go through the cut grid and optimize it
Being implemented...

#### 3) doFit:
Fits the invariant mass distribution (TH1F). To be used with Plotter (see instructions above) with -f flag.
