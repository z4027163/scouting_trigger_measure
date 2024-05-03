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
    parser.add_option('-i', '--input', dest='INPUT', type='string', help='input file')
    #parser.add_option('-o', '--output', dest='OUTPUT', type='string', help='output file')
    parser.add_option('-l', '--label', dest='LABEL', type='string', help='legend text')
    parser.add_option('-v', '--var', dest='VAR', type='string', help='variable')
    parser.add_option('-c', '--cuts', dest='CUT', type='string', help='additional cuts')

    
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



    infile = "/eos/user/c/ccosby/triggerSamples/" + opt.INPUT

    f1 = TFile(str(find("postProc_1.root", infile)),"READ")
    t1 = f1.Get("tree")

    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)

    basicCuts = 'pt1>(mll/3)&&pt2>(mll/4)&&pt1>4&&pt2>6&&pt2<10&&mll>1&&mll<10'
    if opt.CUT:
        cuts = basicCuts + "&&" +opt.CUT
    else:
        cuts = basicCuts

    if (opt.VAR == 'mll'):
        h = TH1F("h","h", 50, 0, 25)
        t1.Draw("mll>>h",cuts, "goff")
    if (opt.VAR == 'pt1'):
        h = TH1F("h","h", 50, 0, 100)
        t1.Draw("pt1>>h",cuts, "goff")
    if (opt.VAR == 'pt2'):
        h = TH1F("h","h", 50, 0, 100)
        t1.Draw("pt2>>h",cuts,"goff")
    if (opt.VAR == 'lxy'):
        h = TH1F("h","h", 50, 0, 100)
        t1.Draw("lxy>>h",cuts ,"goff")
    if (opt.VAR == 'drll'):
        h = TH1F("h","h", 15, 0, 3)
        t1.Draw("drll>>h",cuts ,"goff")
    if (opt.VAR == 'vtxProb'):
        h = TH1F("h","h", 20, 0, 1)
        t1.Draw("vtxProb>>h","pt1>(mll/3)&&pt2>(mll/4)&&pt1>5&&pt2>5","goff")
    if (opt.VAR == 'sigLxy'):
        h = TH1F("h","h", 20, 0, 10)
        t1.Draw("sigLxy>>h","pt1>(mll/3)&&pt2>(mll/4)&&pt1>5&&pt2>5","goff")

    if ('leff' in opt.VAR):
        trig = opt.VAR.replace("leff","&&pass")
        cutsPass = cuts + trig
        print("passing cuts: " + cutsPass)
        hPass = TH1F("hPass", "hPass", 10, array('d',[0.,3.,6.,9.,12.,15.,18.,21.,40.,60.,100.]))
        t1.Draw("lxy>>hPass",cutsPass,"goff")

        hAll = TH1F("hAll","hAll", 10, array('d',[0.,3.,6.,9.,12.,15.,18.,21.,40.,60.,100.]))
        t1.Draw("lxy>>hAll", cuts, "goff")
        hAll.GetXaxis().SetTitle("Lxy [cm]")
        hAll.GetYaxis().SetTitle("Efficiency")
        eff = TEfficiency(hPass,hAll)

    if ('reff' in opt.VAR):
        trig = "&&(passDouble4p5mass || pass157 || passDouble4dR) && passDST"
        #trig = opt.VAR.replace("meff","&&pass")
        cutsPass = cuts + trig
        print("passing cuts: " + cutsPass)
        hPass = TH1F("hPass", "hPass", 15, 0, 3)
        t1.Draw("drll>>hPass",cutsPass,"goff")

        hAll = TH1F("hAll","hAll", 15, 0, 3)
        t1.Draw("drll>>hAll", cuts, "goff")
        hAll.GetXaxis().SetTitle("Delta R")
        hAll.GetYaxis().SetTitle("Efficiency")
        eff = TEfficiency(hPass,hAll)

        

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

    
    else:
        h.SetLineWidth(5)
        if ('EGamma 2018' in opt.LABEL):
            h.SetLineColor(2)
        if ('DY Simulation' in opt.LABEL):
            h.SetLineColor(3)
        if ('Exotic Signal' in opt.LABEL):
            h.SetLineColor(4)
        if ((opt.VAR == 'pt1') or (opt.VAR == 'pt2')):
            h.GetXaxis().SetTitle("Pt [GeV]")
        if (opt.VAR == 'mll'):
            h.GetXaxis().SetTitle("Invar. Mass [GeV]")
        if ((opt.VAR == 'lxy')): 
            h.GetXaxis().SetTitle("Lxy [cm]")

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
