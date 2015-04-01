#!/bin/python
from ROOT import *
import getopt, sys
def PrintTH1F(hist, legend, name):
	ROOT.gROOT.SetBatch()
	leg = TLegend(0.6,0.7,0.89,0.89)
	leg.SetFillStyle(0)
	leg.SetLineWidth(0)
	leg.SetBorderSize(0)
	leg.AddEntry(hist, legend, "l")

	c = TCanvas("a", "a", 900, 600)
	c.SetFillColor(0)
	c.SetBorderMode(0)
	c.SetFrameFillStyle(0)
	c.SetFrameBorderMode(0)
	c.SetTickx(0)
	c.SetTicky(0)
	c.SetGrid()

	hist.SetStats(0)
	hist.SetMarkerStyle(20)
	hist.Draw('E')
	if legend is not '':
		leg.Draw('same')
	SName = ''
	if name is '':
		SName = "plots/" + str(hist.GetName()) + ".pdf"
	if name is not '':
		SName = "plots/" + str(name) + ".pdf"
	c.SaveAs(SName)