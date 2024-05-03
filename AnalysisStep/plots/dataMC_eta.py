from ROOT import *
from array import array
import shutil
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
    #parser.add_option('-D', '--inputData', dest='INPUTDATA', type='string', help='Data input file')
    #parser.add_option('-M', '--inputMC', dest='INPUTMC', type='string', help='Simulation input file')
    #parser.add_option('-r', '--dRRange', dest='dRANGE', type='string', help='DeltaR binning')
    #parser.add_option('-m', '--mllRange', dest='mRANGE', type='string', help='mll binning')
    #parser.add_option('-o', '--output', dest='OUTPUT', type='string', help='output file')
    #parser.add_option('-l', '--label', dest='LABEL', type='string', help='legend text')
    #parser.add_option('-v', '--var', dest='VAR', type='string', help='variable')
    #parser.add_option('-c', '--cuts', dest='CUT', type='string', help='additional cuts')
    parser.add_option('-t', '--trigger', dest='TRIG', type='string', help='trigger under study')
    #parser.add_option('-d', '--DST', dest='DST', type='string', help='include DST')
    parser.add_option('-y', '--year', dest='YEAR', type='string', help='which year')


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



    #xbins = [0.0]
    #while xbins[len(xbins)-1]<=2.0:
     # xbins.append(xbins[len(xbins)-1]+0.05)
    xbins = [0.0,0.125, 0.25,0.375, 0.50, 0.675, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0 ]
    pt2min = "0"; pt2max = "1000"
    save = "newAllTrigLowMass"

    cutden = "pt1*3>mll && pt2*4>mll && pt1>6 && pt2>6 && abs(eta1)<1.9 && abs(eta2)<1.9 && mll>1.0 && mll<12.0 && passSel==1 && mediumid==1 && pt2>"+pt2min 
    if (opt.TRIG == "DoubleMu4p5"):
        cutden = cutden + " &&  pt1>4.5 && pt2>4.5 && abs(eta1)<2.0 && abs(eta2)<2.0 && mll>7.0 && mll<18.0 "
        label = "L1_DoubleMu4p5er2p0_SQ_OS_Mass7to18"
    if (opt.TRIG == "DoubleMu4p5dR1p2"):
        if (opt.YEAR == "2017"):
            cutden = cutden + " && pt1>4.0 && pt2>4.0 && drll < 1.2"
            label = "L1_DoubleMu4_SQ_OS_dR_Max1p2"
        if (opt.YEAR == "2018"):
            cutden = cutden + " && pt1>4.5 && pt2>4.5 && drll < 1.2"
            label = "L1_DoubleMu4p5_SQ_OS_dR_Max1p2 "
    if (opt.TRIG == "DoubleMu0"):
        cutden = cutden + " && abs(eta1)<1.5 && abs(eta2)<1.5 && drll < 1.4 "
        label = "L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4"
    if (opt.TRIG == "DoubleMu157"):
        cutden = cutden + " && pt1>17 && pt2>9 "
        label = "L1_DoubleMu_15_7"

# (pass0er1p5OS==1|| pass157==1 || passDouble4p5mass==1 || passDouble4dR==1) "
# (pass0er1p5OS==1|| pass157==1 || passDouble4p5mass==1 || passDouble4p5massdR1p2==1) "
    if (opt.TRIG == "DoubleMu4p5"):
        cutnum = cutden + " && passDouble4p5mass==1 "
    if (opt.TRIG == "DoubleMu4p5dR1p2"):
        if (opt.YEAR == "2017"):
            cutnum = cutden + " && passDouble4dR==1 "
        if (opt.YEAR == "2018"):
            cutnum = cutden + " && passDouble4p5massdR1p2==1 "
    if (opt.TRIG == "DoubleMu0"):
        cutnum = cutden + " && pass0er1p5OS==1 "
    if (opt.TRIG == "DoubleMu157"):
        cutnum = cutden + " && pass157==1 "




    weightdata = "1.0"
    weightmc = "1.0"

    tmc = TChain("tree")
    #tmc.Add('/eos/user/c/ccosby/triggerSamples/Zdark043020DY/postProc_1.root')
    
    if (opt.YEAR == "2017"):
        #cutnum = cutden + " && (pass125==1 || passDouble4p5mass==1 || passDouble4dR==1 || pass0er1p5OS==1) && passDST==1"
        tmc.Add('/eos/user/c/ccosby/triggerSamples2017/lowMassDY2017/postProc_1.root')
    if (opt.YEAR == "2018"):
        #cutnum = cutden + " && (pass157==1 || passDouble4p5mass==1 || passDouble4p5massdR1p2==1 || pass0er1p5OS==1) && passDST==1"
        tmc.Add('/eos/user/c/ccosby/triggerSamples2018/lowMassDrellYan/postProc_1.root')
        
    sample = "DY5to50"


    hdenmc = TH1F("hdenmc","hdenmc",len(xbins)-1,array('d',xbins))
    hdenmc.Sumw2()
    hnummc = TH1F("hnummc","hnummc",len(xbins)-1,array('d',xbins))
    hnummc.Sumw2()

    tmc.Draw("abs(eta1)>>hdenmc",cutden,"goff")
    tmc.Draw("abs(eta1)>>hnummc","("+cutnum+")","goff")

    effmc = TEfficiency(hnummc,hdenmc)
    heffmc = hnummc.Clone("heffmc")
    heffmc.Divide(hdenmc)

    tdat = TChain("tree")
    if (opt.YEAR == "2017"):
        cutden += "&& L1_12_5_On == 1"
        cutnum += "&& L1_12_5_On == 1"
        tdat.Add("/eos/user/c/ccosby/triggerSamples2017/EGamma2017/postProc_1.root")
    if (opt.YEAR == '2018'):
        tdat.Add("/eos/user/c/ccosby/triggerSamples2018/EGamma/postProc_1.root")
    sample = "Data"

    hdendat = TH1F("hdendat","hdendat",len(xbins)-1,array('d',xbins))
    hdendat.Sumw2()
    hnumdat = TH1F("hnumdat","hnumdat",len(xbins)-1,array('d',xbins))
    hnumdat.Sumw2()


    tdat.Draw("abs(eta1)>>hdendat","("+weightdata+")*("+cutden+")","goff")
    tdat.Draw("abs(eta1)>>hnumdat","("+weightdata+")*("+cutnum+")","goff")

    effdat = TEfficiency(hnumdat,hdendat)
    effdat.SetName("l1_corrCuts_eff_"+sample+"_"+save)
    effdat.SetTitle("l1_corrCuts_eff_"+sample+"_"+save)
    effdat.SaveAs("l1_corrCuts_eff_Data_"+save+"_2018_dR.root")

    heffdat = hnumdat.Clone("heffdat")
    heffdat.Divide(hdendat)


    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)
    c1 = TCanvas("c1","c1",800,800)
    c1.cd()
    c1.SetBottomMargin(0.3)

    hdum = TH1F("hdum","hdum",1,xbins[0],xbins[len(xbins)-1])
    hdum.SetBinContent(1,0.001)
    hdum.SetMinimum(0.001)
    hdum.SetMaximum(1.0)
    hdum.GetXaxis().SetTitle("abs(#eta_{1})")
    hdum.GetXaxis().SetLabelSize(0)
    hdum.Draw()

    effdat.SetLineColor(1)
    effdat.SetLineWidth(2)
    effdat.Draw("epsame")
    effmc.SetLineColor(2)
    effmc.SetLineWidth(2)
    effmc.Draw("epsame")


    #leg = TLegend(0.4,0.4,0.85,0.6)
    #leg.AddEntry(effmc,"DY MC","l")
    #leg.AddEntry(effdat,"Run 2018 EGamma Dataset","l")
    #leg.Draw("same")


    leg = TLegend(0.6,0.30,0.9,0.45)
    leg.AddEntry(effmc,"Low Mass Drell-Yan MC","l")
    #leg.AddEntry(effmcsf,"DY MC w/ TnP SF","l")
    #leg.AddEntry(effdat,"Run 2017 JetHT Dataset","l")
    if (opt.YEAR == "2017"):
        leg.AddEntry(effdat,"Run 2017 SE/DE Dataset","l")
    if (opt.YEAR == "2018"):
        leg.AddEntry(effdat,"Run 2018 EGamma Dataset","l")
    leg.Draw("same")

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.4*c1.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31)
    if (opt.YEAR =="2017"):
        latex2.DrawLatex(0.89, 0.93,"27 fb^{-1} (13 TeV)")
    if (opt.YEAR == '2018'):
        latex2.DrawLatex(0.89, 0.93,"59.7 fb^{-1} (13 TeV)")
    latex2.SetTextSize(0.5*c1.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.12, 0.93, "CMS")
    latex2.SetTextSize(0.5*c1.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.23, 0.93, "Preliminary")
    latex2.SetTextSize(0.25*c1.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.12, 0.33, label)

    pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 1.0)
    pad.SetTopMargin(0.7)
    pad.SetFillColor(0)
    pad.SetGridy(1)
    pad.SetFillStyle(0)
    pad.Draw()
    pad.cd(0)

    hdum2 = TH1F("hdum2","hdum2",1,xbins[0],xbins[len(xbins)-1])
    hdum2.SetBinContent(1,0.001)
    hdum2.SetMinimum(0.61)
    hdum2.SetMaximum(1.39)
    hdum2.GetXaxis().SetTitle("Leading Muon |#eta|")
    hdum2.Draw()

    ratio = heffdat.Clone("ratio")
    ratio.Divide(heffmc)
    ratio.SetLineColor(1)
    ratio.SetLineWidth(2)
    ratio.SetMarkerColor(1)
    ratio.Draw("same")     

#    ratio.SaveAs("l1_corrCuts_eff_data_vs_mc_"+save+"_2018_dR.root")

    c1.SaveAs("data_vs_mc_"+save+"_"+opt.YEAR+"_dR.png")
    shutil.move(os.getcwd() + "/" + "data_vs_mc_"+save+"_"+opt.YEAR+"_dR.png", "/eos/user/c/ccosby/www/darkPhotonl1Study/" +"data_vs_mc_"+save+"_"+opt.YEAR+"_dR.png")
    print("https://ccosby.web.cern.ch/ccosby/darkPhotonl1Study/" + "data_vs_mc_"+save+"_"+opt.YEAR+"_dR.png")



if __name__ == "__main__":
  plot()
