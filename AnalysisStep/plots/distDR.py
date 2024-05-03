from ROOT import *
import sys, os, pwd, commands, glob, fnmatch
import optparse, shlex, re
import time
from time import gmtime, strftime
import math
from array import array
import shutil

#define function for parsing options
def parseOptions():

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('-y', '--year', dest='YEAR', type='string', help='which year')

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()



def plot():
    global opt, args
    parseOptions()


    title = "DY_sample_dr"

    massRange = " mll > 0.2 && mll < 50"
    trig = " passDST == 1 &&"
    cuts = trig + massRange
    #cuts = massRange

    tmc = TChain("tree")

    telisa = TChain("scoutingTree/tree");
    
    if (opt.YEAR =="2018"):
        tmc.Add('/eos/user/c/ccosby/triggerSamples2018/lowMassDrellYan/postProc_1.root')
    if (opt.YEAR =="2017"):
        tmc.Add('/eos/user/c/ccosby/triggerSamples2017/lowMassDY2017/postProc_1.root')

    #hmc = TH1F("hmc","hmc", 60, 0, 20)
    #tmc.Draw("mll>>hmc","("+cuts+")","goff")

    hmcjpsi = TH1F("hmcjpsi","hmcjpsi",48,0,3.7)
    tmc.Draw("drll>>hmcjpsi","(mll > 2.9 && mll < 3.3 && passDST == 1)","goff")
    hmcjpsi.Scale(1/hmcjpsi.Integral(), "nosw2")

    hmcups = TH1F("hmcups","hmcups",48,0,3.7)
    tmc.Draw("drll>>hmcups","(mll > 9.1 && mll < 9.7 && passDST == 1)","goff")
    hmcups.Scale(1/hmcups.Integral(), "nosw2")

    hmc = TH1F("hmc","hmc",48,0,3.7)
    tmc.Draw("drll>>hmc","(mll > 1 && mll < 20 && passDST == 1)","goff")
    hmc.Scale(1/hmc.Integral(), "nosw2")

    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)
    gStyle.SetTextSize(1.1)
    gStyle.SetTextFont(42)

    c2 = TCanvas("c2","c2",1000,800)
    c2.cd()
    hmcjpsi.GetXaxis().SetMoreLogLabels()
    hmcjpsi.GetXaxis().SetTitle("#DeltaR")
    #hmcjpsi.GetXaxis().SetTitle("mass (GeV)")
    hmcjpsi.GetYaxis().SetTitle("Fraction")
    hmcjpsi.GetYaxis().SetTitleOffset(1.5)
    hmcjpsi.SetLineColor(2)
    hmcjpsi.Draw("")

    hmcups.SetLineColor(4)
    hmcups.Draw("same")

    hmc.SetLineColor(1)
    hmc.Draw("same")
    c2.Update()


    legend = TLegend(0.5,0.6,0.85,0.85)
    legend.SetHeader("2018 Drell-Yan MC: 1-20 GeV","C")
    legend.AddEntry("hmcjpsi","2.9-3.3 GeV (J/#psi)")
    legend.AddEntry("hmcups","9.1-9.7 GeV (#Upsilon)")
    legend.AddEntry("hmc","1-20 GeV")
    legend.SetBorderSize(0)
    legend.Draw()
    
    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.45*c2.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31)
    #latex2.DrawLatex(0.82, 0.93,"59.7 fb^{-1} (13 TeV)")
    latex2.SetTextSize(0.55*c2.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.12, 0.92, "CMS")
    latex2.SetTextSize(0.55*c2.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.22, 0.92, "Preliminary Simulation")

    c2.SaveAs(title + "_mc.pdf")

    shutil.move(os.getcwd() + "/" + title + "_mc.pdf", "/eos/user/c/ccosby/www/darkPhotonl1Study/newTrigEffs/" + title + "_mc.pdf")
    print("https://ccosby.web.cern.ch/ccosby/darkPhotonl1Study/newTrigEffs/" + title + "_mc.pdf")





if __name__ == "__main__":
  plot()
