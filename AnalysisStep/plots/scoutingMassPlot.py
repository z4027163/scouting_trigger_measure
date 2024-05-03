from ROOT import *

import sys, os, pwd, commands, glob, fnmatch
import optparse, shlex, re
import time
from time import gmtime, strftime
import math
from array import array

#define function for parsing options
def parseOptions():

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()





def plot():

    global opt, args
    parseOptions()



    f1 = TFile("/eos/cms/store/group/phys_exotica/darkPhoton/jakob/newProd/2017/ScoutingRunD/mergedHistos_v1.root","READ")
    h = f1.Get("massforLimitFull")

    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)

    basicCuts = 'm1Impact!=-9&&m2Impact!=-9'
    if opt.CUT:
        cuts = basicCuts + "&&" +opt.CUT
    else:
        cuts = basicCuts

    if (opt.VAR == 'mll'):
        h = TH1F("h","h", 50, 0, 100)
        t1.Draw("mll>>h",cuts, "goff")



        

    ### Use "goff same" for the second two
    ### and don't use "matTauTau>>h_matTauTau".... just "matTauTau"
    c1 = TCanvas("c1","c1",900,800)
    c1.SetLeftMargin(0.15)
    c1.SetRightMargin(0.05)

    #if (not((opt.VAR == 'eff125') or (opt.VAR == 'eff157') or (opt.VAR == 'effDST'))):
    #    c1.SetLogy()
    c1.cd()

 

    if ('eff' in opt.VAR):
        eff.SetLineWidth(5)
        eff.Draw()
        #eff.GetYAxis().SetRangeUser(0,1)
        gPad.Update()

        graph = eff.GetPaintedGraph()
        graph.SetMinimum(0)
        graph.SetMaximum(1) 
        gPad.Update() 
        leg = TLegend(0.6,0.7,0.85,0.8)
        leg.AddEntry(eff, opt.LABEL,"l")
        leg.Draw("same")

        h.GetYaxis().SetTitle("Events")
        h.Draw("hist")
        leg = TLegend(0.6,0.7,0.85,0.8)
        leg.AddEntry(h, opt.LABEL,"l")
        leg.Draw("same")
        c1.SetLogy()


 
    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.4*c1.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31)
    #latex2.DrawLatex(0.82, 0.93,"59.7 fb^{-1} (13 TeV)")
    latex2.SetTextSize(0.5*c1.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.15, 0.93, "CMS")
    latex2.SetTextSize(0.45*c1.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.26, 0.93, "Preliminary")

    if (opt.CUT):
        tag = "_" + opt.CUT
    else:
        teg = ""

    filename = opt.LABEL.lower() + "_" + opt.VAR + ".png"
    filename = filename.replace(" ","_")
    filename = filename.replace(",","")
    filename = filename.replace("$$","_")
    c1.SaveAs(filename)    



if __name__ == "__main__":
  plot()
