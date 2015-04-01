#!/bin/python

from ROOT import *
from Printer import *
from doFit import *
import getopt, sys

def main(argv):
	ROOT.gROOT.SetBatch()
	inputfile = ''
	eta = True
	pi0 = False
	EB = True
	EE = False
	NCr1 = ''
	NCr2 = ''
	PtClu = ''
	S4S9 = ''
	Iso = ''
	PtDi = ''
	name = 'output.pdf'
	DoFit = False
	hltisoOff = False
	cutCorrOff = False
	plotCorrOff = False
	
	try:
		opts, args = getopt.getopt(argv,"hi:epbcf",["input=","maximum=", "NCr1=", "NCr2=", "PtClu=", "S4S9=", "Iso=", "PtDi=", "name=", "HltIsoOff", "CutCorrOff", "PlotCorrOff"])
	except getopt.GetoptError:
		print 'Plotter.py -i <inputfile> '
		print '-e/-p[--eta/--pi0] (-e for eta, -p for pi0) '
		print '-b/-c[--EB/--EE] (-b for barrel, -c for endcap) '
		print '--name=<filename>'
		print 'Variables to assign: NCr1, NCr2, PtClu, S4S9, Iso, PtDi'
		print 'Usage: --var=Value'
		print 'IF you want to fit: --doFit'
		sys.exit(2)
	if len(opts) == 0:
		print 'Plotter.py -i <inputfile> '
		print '-e/-p[--eta/--pi0] (-e for eta, -p for pi0) '
		print '-b/-c[--EB/--EE] (-b for barrel, -c for endcap) '
		print '--name=<filename>'
		print 'Variables to assign: NCr1, NCr2, PtClu, S4S9, Iso, PtDi'
		print 'Usage: --var=Value'
		print 'IF you want to fit: --doFit'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'Plotter.py -i <inputfile> '
			print '-e/-p[--eta/--pi0] (-e for eta, -p for pi0) '
			print '-b/-c[--EB/--EE] (-b for barrel, -c for endcap) '
			print '--name=<filename>'
			print 'Variables to assign: NCr1, NCr2, PtClu, S4S9, Iso, PtDi'
			print 'Usage: --var=Value'
			print 'IF you want to fit: --doFit'
			sys.exit()
		elif opt in ("-i", "--input"):
			inputfile = arg
		elif opt in ("-o", "--output"):
			outputfile = arg
		elif opt in ("-e", "--eta"):
			eta = 1
			pi0 = 0
		elif opt in ("-p", "--pi0"):
			eta = 0
			pi0 = 1
		elif opt in ("-b", "--EB"):
			EB = 1
			EE = 0
		elif opt in ("-c", "--EE"):
			EB = 0
			EE = 1
		elif opt in ("--NCr1"):
			NCr1 = int(arg)
		elif opt in ("--NCr2"):
			NCr2 = int(arg)
		elif opt in ("--PtClu"):
			PtClu = float(arg)
		elif opt in ("--S4S9"):
			S4S9 = float(arg)
		elif opt in ("--Iso"):
			Iso = float(arg)
		elif opt in ("--PtDi"):
			PtDi = float(arg)
		elif opt in ("--name"):
			name = str(arg)
		elif opt in ("-f", "--doFit"):
			DoFit = True
		elif opt in ("--HltIsoOff"):
			hltisoOff = True
		elif opt in ("--CutCorrOff"):
			cutCorrOff = True
		elif opt in ("--PlotCorrOff"):
			plotCorrOff = True
			
	file = TFile.Open(str(inputfile), 'READ')
	tree = file.Get('Tree_Optim')
	if(tree.GetEntries() < 1):
		print 'Tree has problems. Does the file exist?'
		sys.exit()

	print "Doing fit? ", DoFit

	#String Vars:
	st_mass = 'STr2_mPi0_rec>>mass'
	st_NCr1 = 'STr2_n1CrisPi0_rec > '
	st_NCr2 = 'STr2_n2CrisPi0_rec > '
	st_PtClu_1 = 'STr2_ptG1_rec > ' 
	st_PtClu_2 = 'STr2_ptG2_rec > ' 
	st_S4S9_1 = 'STr2_S4S9_1 > '
	st_S4S9_2 = 'STr2_S4S9_2 > '
	st_Iso = 'STr2_HLTIsoPi0_rec < '
	st_PtDi = 'STr2_ptPi0_rec > '

	if(plotCorrOff):
		st_mass = 'STr2_mPi0_nocor>>mass'
	if(cutCorrOff):
		st_PtClu_1 = 'STr2_ptG1_nocor > ' 
		st_PtClu_2 = 'STr2_ptG2_nocor > ' 
		st_PtDi = 'STr2_ptPi0_nocor > '
	if(hltisoOff):
		st_Iso = 'STr2_IsoPi0_rec < '
		
	
	mass = TH1F()
	if(eta):
		mass = TH1F('mass', '#eta#rightarrow#gamma#gamma Invariant Mass;M_{#eta};Events', 50, 0.25, 0.75)
	if(pi0):
		mass = TH1F('mass', '#pi^{0}#rightarrow#gamma#gamma Invariant Mass;M_{#pi^{0}};Events', 50, 0.08, 0.2)
	
	cut0 = ''
	if(EB):
		cut0 = 'fabs(STr2_etaPi0_rec) < 1.'
	if(EE):
		cut0 = 'fabs(STr2_etaPi0_rec) > 1.'
	Cut0 = cut0 + ' && '
	Cut1 = st_NCr1 + str(NCr1) + ' && '
	Cut2 = st_NCr2 + str(NCr2) + ' && '
	Cut3 = st_PtClu_1 + str(PtClu) + ' && ' + st_PtClu_2 + str(PtClu) + ' && '
	Cut4 = st_S4S9_1 + str(S4S9) + ' && ' + st_S4S9_2 + str(S4S9) + ' && '
	Cut5 = st_Iso + str(Iso) + ' && '
	Cut6 = st_PtDi + str(PtDi)
	print '			Printing with the following cuts:'
	print '			', Cut0
	print '			', Cut1
	print '			', Cut2
	print '			', Cut3
	print '			', Cut4
	print '			', Cut5
	print '			', Cut6
	SelectionCut = TCut(Cut0 + Cut1 + Cut2 + Cut3 + Cut4 + Cut5 + Cut6)
	npass = tree.Draw(st_mass, SelectionCut)
	PrintTH1F(mass,'', name)
	if(DoFit):
		doFit(mass, pi0, EE, name)
	
if __name__ == "__main__":
	main(sys.argv[1:])
