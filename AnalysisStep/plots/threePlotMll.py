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

    # input options
    #parser.add_option('-i', '--input', dest='INPUT', type='string', help='input file')
    parser.add_option('-o', '--output', dest='OUTPUT', type='string', help='output file')
    #parser.add_option('-l', '--label', dest='LABEL', type='string', help='legend text')


    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()




def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            print(str(os.path.join(root, name)))
            return os.path.join(root, name)

def plot():

    global opt, args
    parseOptions()

    infile1 = "/eos/user/c/ccosby/triggerSamples/EGamma/"
    infile2 = "/eos/user/c/ccosby/triggerSamples/DrellYan/"
    infile3 = "/eos/user/c/ccosby/triggerSamples/ExSig/"


    f1 = TFile(str(find("postProc_1.root", infile1)),"READ")
    t1 = f1.Get("tree")
    f2 = TFile(str(find("postProc_1.root", infile2)),"READ")
    t2 = f1.Get("tree")
    f3 = TFile(str(find("postProc_1.root", infile3)),"READ")
    t3 = f1.Get("tree")

    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)



    h1 = TH1F("h1","h1", 30, 0, 100)
    t1.Draw("mll>>h1","pt1>(mll/3)&&pt2>(mll/4)&&pt1>5&&pt2>5","goff")
    h2 = TH1F("h2","h2", 30, 0, 100)
    t2.Draw("mll","pt1>(mll/3)&&pt2>(mll/4)&&pt1>5&&pt2>5","goff same")
    h3 = TH1F("h3","h3", 30, 0, 100)
    t3.Draw("mll","pt1>(mll/3)&&pt2>(mll/4)&&pt1>5&&pt2>5","goff same")



    ### Use "goff same" for the second two
    ### and don't use "matTauTau>>h_matTauTau".... just "matTauTau"
    c1 = TCanvas("c1","c1",900,800)
    c1.SetLeftMargin(0.15)
    c1.SetRightMargin(0.05)
    c1.SetLogy()
    c1.cd()


    h1.SetLineColor(2)
    h1.SetLineWidth(5)
    h1.GetXaxis().SetTitle("Pt [GeV]")
    h1.GetYaxis().SetTitle("Events")
    h1.Draw("hist same")

    h2.SetLineColor(3)
    h2.SetLineWidth(5)
    h2.Draw("hist same")

    h3.SetLineColor(4)
    h3.SetLineWidth(5)
    h3.Draw("hist same")




    leg = TLegend(0.6,0.7,0.85,0.8)
    leg.AddEntry(h1, "EGamma 2018","l")
    leg.AddEntry(h2, "Drell-Yan","l")
    leg.AddEntry(h3, "Exotic Signal","l")

    leg.Draw("same")

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


    c1.SaveAs(opt.OUTPUT)

if __name__ == "__main__":
  plot()
