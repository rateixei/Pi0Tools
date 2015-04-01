from ROOT import *

def doFit(hist, isPi0, isEE, OutFileName):
	print "FITTING HISTOGRAM WITH NUMBER OF EVENTS = ", hist.GetSum()
	print "is Pi0? ", isPi0
	print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
	meanVal = (0.47, 0.4, 0.62)
	sigmaVal = (0.053, 0.015, 0.090)
	Range = (0.2, 0.75)
	if(isPi0):
		meanVal = (0.116, 0.105, 0.150)
		Range = (0.08, 0.2)
		if(isEE):
			meanVal = (0.120, 0.10, 0.140)
	if(isEE):
		meanVal = (0.55, 0.45, 0.62)
		sigmaVal = (0.013, 0.005, 0.020)

	x		= RooRealVar("x","#gamma#gamma invariant mass",Range[0],Range[1], "GeV/c^2")
	mean	= RooRealVar("mean","#pi^{0} peak position", meanVal[0], meanVal[1], meanVal[2],"GeV/c^{2}")
	sigma	= RooRealVar("sigma","#pi^{0} core #sigma",sigmaVal[0], sigmaVal[1],sigmaVal[2],"GeV/c^{2}")
	Nsig	= RooRealVar("Nsig","#pi^{0} yield",1000.,0.,10000000)
#	fcore	 = RooRealVar("fcore","f_{core}",0.9,0.,1.)
	sigmaTail = RooRealVar("sigmaTail","#pi^{0} tail #sigma",0.040, 0.020,0.065,"GeV/c^{2}")
	
	Nsig.setVal( hist.GetSum()*0.1)	

	dh		= RooDataHist("dh","#gamma#gamma invariant mass",RooArgList(x),hist)
	
	gaus	= RooGaussian("gaus","Core Gaussian",x, mean,sigma)	
#	gaus2	 = RooGaussian("gaus2","Tail Gaussian",x, mean,sigmaTail)
		
#	signal	= RooAddPdf("signal","signal model",RooArgList(gaus,gaus2),fcore)	
	
	p0 = RooRealVar("p0","p0", 1000.,-1.e5,1.e5);
	p1 = RooRealVar("p1","p1", -3000.,-1.e5,1.e5);
	p2 = RooRealVar("p2","p2", 10000.,-1.e5,1.e5);
	p3 = RooRealVar("p3","p3", -10000.,-1.e5,1.e5);
	p4 = RooRealVar("p4","p4",-4000.,-1.e5,1.e5);
	p5 = RooRealVar("p5","p5", 5.,-1.e5,1.e5);
	p6 = RooRealVar("p6","p6", 6.,-1.e5,1.e5);
	cb0 = RooRealVar("cb0","cb0", 0.2, -1.,1.);
	cb1 = RooRealVar("cb1","cb1",-0.1, -1.,1.);
	cb2 = RooRealVar("cb2","cb2", 0.1, -1.,1.);
	cb3 = RooRealVar("cb3","cb3",-0.1, -0.5,0.5);
	cb4 = RooRealVar("cb4","cb4", 0.1, -1.,1.);
	cb5 = RooRealVar("cb5","cb5", 0.1, -1.,1.);
	cb6 = RooRealVar("cb6","cb6", 0.3, -1.,1.);

	cbpars = RooArgList(cb0,cb1,cb2, cb3)
#	cbpars = RooArgList(cb0,cb1,cb2)

	bkg = RooChebychev("bkg","bkg model", x, cbpars )
	Nbkg = RooRealVar("Nbkg","background yield",1.e3,0.,100000000)
	Nbkg.setVal( hist.GetSum()*0.8)

	model = ''
	model1 = RooAddPdf("model","sig+bkg",RooArgList(gaus,bkg),RooArgList(Nsig,Nbkg))
	model = model1
	
	nll = RooNLLVar("nll","log likelihood var",model,dh, RooFit.Extended())
	m = RooMinuit(nll)
	m.setVerbose(ROOT.kFALSE)
	m.migrad()
	res = m.save()
	
	chi2 = RooChi2Var("chi2","chi2 var",model,dh, true)
	ndof = hist.GetNbinsX() - res.floatParsFinal().getSize()

	x.setRange("sobRange",mean.getVal()-3.*sigma.getVal(), mean.getVal()+3.*sigma.getVal())
	xSet = RooArgSet(x)
	integralSig = gaus.createIntegral(xSet,RooFit.NormSet(xSet),RooFit.Range("sobRange"))
	integralBkg = bkg.createIntegral(xSet,RooFit.NormSet(xSet),RooFit.Range("sobRange"))
	
	normSig = integralSig.getVal()
	normBkg = integralBkg.getVal()
	
	Signal = normSig*Nsig.getVal()
	SignalErr = normSig*Nsig.getError()
	Background = normBkg*Nbkg.getVal()
	BackgroundErr = normBkg*Nbkg.getError()
	SoB = -100
	SoBErr = -100
	if(Background > 0):
		SoB = Signal/Background
		SoBErr = SoB*sqrt(pow(SignalErr/Signal,2) + pow(BackgroundErr/Background,2))
	
	
	xframe = x.frame(hist.GetNbinsX())
	xframe.SetTitle(hist.GetTitle())
	dh.plotOn(xframe)
	BkgSet = RooArgSet(bkg)
	model.plotOn(xframe,RooFit.Components(BkgSet),RooFit.LineStyle(ROOT.kDashed), RooFit.LineColor(ROOT.kRed))
	model.plotOn(xframe)
	canvas = TCanvas()
	xframe.Draw()
	lat = TLatex()
	lat.SetNDC()
	lat.SetTextSize(0.03)
	lat.SetTextColor(1)
	xmin = 0.65
	yhi = 0.905
	ypass = 0.045
	line = "Yield = " + str(round(Nsig.getVal(),2)) + " #pm " + str(round(Nsig.getError(),2))
	lat.DrawLatex(xmin,yhi,line)
	canvas.Update()
	line = "m_{#gamma#gamma} = " + str(round(mean.getVal()*1000.,2)) + " #pm " + str(round(mean.getError()*1000.,2)) + " MeV"
	lat.DrawLatex(xmin,yhi-ypass,line)
	Unknown = round(sigma.getVal()*100./mean.getVal(),2)
	line = "#sigma = " + str(round(sigma.getVal()*1000,2)) + " #pm " + str(round(sigma.getError()*1000,2)) + " MeV"
	lat.DrawLatex(xmin,yhi-2.*ypass,line)
	line = "#sigma/#mu = " + str(Unknown) + "%"
	lat.DrawLatex(xmin,yhi-3.*ypass,line)
	line = "S/B(3#sigma) = " + str(round(SoB,2))
	lat.DrawLatex(xmin,yhi-4.*ypass,line)
	kai2 = round(xframe.chiSquare()/ndof,2)
	line = "#chi^{2} = " + str(kai2)
	lat.DrawLatex(xmin,yhi-5.*ypass,line)
	ffilename = "fits/" + str(OutFileName) + "FIT.pdf"
	canvas.SaveAs(ffilename)
