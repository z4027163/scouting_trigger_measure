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
    #parser.add_option('-y', '--year', dest='YEAR', type='string', help='which year')

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()



def plot():
    global opt, args
    parseOptions()


    title = "DY_sample_dr_run3"

    massRange = " mll > 0.2 && mll < 50"
    trig = " passDST == 1 &&"
    cuts = trig + massRange
    #cuts = massRange

    #tmc = TChain("tree")
    #tmc.Add('/eos/user/c/ccosby/triggerSamples2018/lowMassDrellYan/postProc_1.root')

    tmc = TChain("tree")
    tmc.Add('/eos/user/c/ccosby/triggerSamples2018/lowMassDrellYan/postProc_1.root')

    #t2018 = TChain("scoutingTree/tree");
    #t2018.Add('/afs/cern.ch/work/e/elfontan/public/forChris/DY_run2_2018.root')
    
    t2022 = TChain("scoutingTree/tree")
    t2022.Add('/afs/cern.ch/work/e/elfontan/public/forChris/DY_run3_2022.root')

    tbmumu = TChain("scoutingTree/tree")
    tbmumu.Add('/afs/cern.ch/work/e/elfontan/public/forChris/Run3_BsMuMu_2022.root')

    tctau =  TChain("scoutingTree/tree")
    tctau.Add('/afs/cern.ch/user/j/jfriesen/public/HToZdZdTo2Mu2X_MZd-1_ctau-1mm_scoutRun3.root')
    

    #hmc = TH1F("hmc","hmc", 60, 0, 20)
    #tmc.Draw("mll>>hmc","("+cuts+")","goff")

    #hmcjpsi = TH1F("hmcjpsi","hmcjpsi",48,0,3.7)
    #tmc.Draw("drll>>hmcjpsi","(mll > 2.9 && mll < 3.3 && passDST == 1)","goff")
    #hmcjpsi.Scale(1/hmcjpsi.Integral(), "nosw2")

    #hmcups = TH1F("hmcups","hmcups",48,0,3.7)
    #tmc.Draw("drll>>hmcups","(mll > 9.1 && mll < 9.7 && passDST == 1)","goff")
    #hmcups.Scale(1/hmcups.Integral(), "nosw2")

    #hmc = TH1F("hmc","hmc",48,0,3.7)
    #tmc.Draw("drll>>hmc","(mll > 0 && mll < 20.0 && passDST == 1)","goff")
    #hmc.Scale(1/hmc.Integral(), "nosw2")

    #hbmumu = TH1F("hbmumu","hbmumu",48,0,3.7)
    #tbmumu.Draw("dr>>hbmumu","mass > 2.9 && mass < 3.3","goff")
    #hbmumu.Scale(1/hbmumu.Integral(), "nosw2")

    #hctau = TH1F("hctau","hctau",48,0,3.7)
    #tctau.Draw("dr>>hctau","mass > 2.9 && mass < 3.3","goff")
    #hctau.Scale(1/hctau.Integral(), "nosw2")

    h2022jpsi = TH1F("h2022jpsi","h2022jpsi",48,0,3.7)
    t2022.Draw("dr>>h2022jpsi","mass > 2.9 && mass < 3.3","goff")
    h2022jpsi.Scale(1/h2022jpsi.Integral(), "nosw2")

    h2022ups = TH1F("h2022ups","h2022ups",48,0,3.7)
    t2022.Draw("dr>>h2022ups","mass > 9.1 && mass < 9.7","goff")
    h2022ups.Scale(1/h2022ups.Integral(), "nosw2")

    h2022 = TH1F("h2022","h2022",48,0,3.7)
    t2022.Draw("dr>>h2022","mass > 0 && mass < 20.0","goff")
    h2022.Scale(1/h2022.Integral(), "nosw2")

    h2022High = TH1F("h2022High","h2022High",48,0,3.7)
    t2022.Draw("dr>>h2022High","mass > 20.0 && mass < 50.0","goff")
    h2022High.Scale(1/h2022High.Integral(), "nosw2")

    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)
    gStyle.SetTextSize(1.1)
    gStyle.SetTextFont(42)

    c2 = TCanvas("c2","c2",1000,800)
    c2.cd()
    h2022jpsi.GetXaxis().SetMoreLogLabels()
    h2022jpsi.GetXaxis().SetTitle("#DeltaR")
    #h2022jpsijpsi.GetXaxis().SetTitle("mass (GeV)")
    h2022jpsi.GetYaxis().SetTitle("Fraction")
    h2022jpsi.GetYaxis().SetTitleOffset(1.5)
    h2022jpsi.SetLineColor(2)
    h2022jpsi.Draw("")

    #hbmumu.SetLineColor(2)
    #hbmumu.Draw("same")

    h2022ups.SetLineColor(4)
    h2022ups.Draw("same")

    h2022.SetLineColor(6)
    h2022.Draw("same")

    h2022High.SetLineColor(3)
    h2022High.Draw("same")

    #h2018.SetLineColor(3)
    #h2018.Draw("same")


    c2.Update()


    legend = TLegend(0.25,0.65,0.65,0.85)
    legend.SetHeader("Drell-Yan MC, Run 3 (2022)","C")
    legend.AddEntry("h2022jpsi","2.9-3.3 GeV (J/#psi)")
    #legend.AddEntry("h2022","2.9-3.3 GeV (2022 sample)")
    legend.AddEntry("h2022ups","9.1-9.7 GeV (#Upsilon)")
    legend.AddEntry("h2022","1-20 GeV")
    legend.AddEntry("h2022High","20-50 GeV")
    #legend.AddEntry("hbmumu","B_{s}#rightarrow#mu#mu")
    #legend.AddEntry("hctau"," Displaced Z' (m = 1 GeV, c#tau = 1mm)")
    #legend.AddEntry("h2022","Run 3, 2022 (New)")

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
