# Pi0Tools
Tools for Pi0 Analysis

##Python scripts:
### 1) Plotter:
⋅⋅⋅Plots the invariant mass of a determined selection given by the user through input parameters.
...Instructions to run the Plotter:
python python/Plotter.py \
-i /tmp/rateixei/eos/cms/store/caf/user/lpernie/ALL_MINBIAS_UNCAL_L1_NOL1FILTER_40PU50ns_EB_eta_NewSeed/iter_0/epsilonPlots_0.root \
-p -b \
--NCr1=4 \
--NCr2=4 \
--PtClu=1.6 \
--S4S9=0.9 \
--Iso=0.15 \
--PtDi=3.6 \
--name=Teste2

--> Currently works only with local files =/

### 2) Optimizer:
...Can be used to go through the cut grid and optimize it
...Being implemented...

### 3) Fitter:
...Fits the invariant mass distribution (TH1F)
