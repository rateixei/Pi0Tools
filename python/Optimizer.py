#!/bin/python

from ROOT import *
from Fitter import *
from Parameters import *
from Printer import *
import getopt, sys

def main(argv):
	ROOT.gROOT.SetBatch()
	inputfile = ''
	outputfile = ''
	eta = True
	pi0 = False
	EB = True
	EE = False
	Max = 10000000
	try:
		opts, args = getopt.getopt(argv,"hi:o:epbcm:",["input=","output=", "maximum="])
	except getopt.GetoptError:
		print 'Optimizer.py -i <inputfile> -o <outputfile> -e/-p[--eta/--pi0] (-e for eta, -p for pi0) -b/-c[--EB/--EE] (-b for barrel, -c for endcap) -m <maximum steps>'
		sys.exit(2)
	if len(opts) == 0:
		print 'Optimizer.py -i <inputfile> -o <outputfile> -e/-p[--eta/--pi0] (-e for eta, -p for pi0) -b/-c[--EB/--EE] (-b for barrel, -c for endcap) -m <maximum steps>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'Optimizer.py -i <inputfile> -o <outputfile> -e/-p[--eta/--pi0] (-e for eta, -p for pi0) -b/-c[--EB/--EE] (-b for barrel, -c for endcap) -m <maximum steps>'
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
		elif opt in ("-m", "--max"):
			Max = int(arg)
			
	file = TFile.Open(str(inputfile), 'READ')
	tree = file.Get('Tree_Optim')
	if(tree.GetEntries() < 1):
		print 'Tree has problems. Does the file exist?'
		sys.exit()
	
	mass = TH1F()
	if(eta):
		mass = TH1F('mass', '#eta#rightarrow#gamma#gamma Invariant Mass;M_{#eta};Events', 50, 0.3, 0.7)
	if(pi0):
		mass = TH1F('mass', '#pi^{0}#rightarrow#gamma#gamma Invariant Mass;M_{#pi^{0}};Events', 50, 0.08, 0.2)
		
	npass = 0
	
	cut0 = ''
	pointname = ''
	if(EB):
		cut0 = 'fabs(STr2_etaPi0_rec) < 1.4'
		pointname = 'invMass_OnlyEB'
	if(EE):
		cut0 = 'fabs(STr2_etaPi0_rec) > 1.4'
		pointname = 'invMass_OnlyEE'
	Cut0 = cut0 + ' && '
	counter = 0
	npass = tree.Draw('STr2_mPi0_rec>>mass', TCut(cut0))

	PrintTH1F(mass,'', pointname)
	for v1 in xrange(0,SizeNCr1):
		Cut1 = 'STr2_n1CrisPi0_rec > ' + str(NCr1[v1]) + ' && '
		for v2 in xrange(0,SizeNCr2):
			Cut2 = 'STr2_n2CrisPi0_rec > ' + str(NCr2[v2]) + ' && '
			for v3 in xrange(0,SizePtClu):
				Cut3 = 'STr2_ptG1_rec > ' + str(PtClu[v3]) + ' && STr2_ptG1_rec > ' + str(PtClu[v3]) + ' && '
				for v4 in xrange(0,SizeS4S9):
					Cut4 = 'STr2_S4S9_1 > ' + str(S4S9[v4]) + ' && STr2_S4S9_1 > ' + str(S4S9[v4]) + ' && '
					for v5 in xrange(0,SizeIso):
						Cut5 = 'STr2_HLTIsoPi0_rec < ' + str(Iso[v5]) + ' && '
						for v6 in xrange(0,SizePtDi):
							if counter > Max:
								break
							Cut6 = 'STr2_ptPi0_rec > ' + str(PtDi[v6])
							SelectionCut = TCut(Cut0 + Cut1 + Cut2 + Cut3 + Cut4 + Cut5 + Cut6)
							npass = tree.Draw('STr2_mPi0_rec>>mass', SelectionCut)
							pointname = 'invMass_point_'+str(counter)
							PrintTH1F(mass,'', pointname)
							counter+=1
#							Fitter(mass)
	
if __name__ == "__main__":
	main(sys.argv[1:])
