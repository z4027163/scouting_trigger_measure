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
    #parser.add_option('-D', '--inputData', dest='INPUTDATA', type='string', help='Data input file')
    #parser.add_option('-M', '--inputMC', dest='INPUTMC', type='string', help='Simulation input file')
    parser.add_option('-r', '--dRRange', dest='dRANGE', type='string', help='DeltaR binning')
    parser.add_option('-m', '--mllRange', dest='mRANGE', type='string', help='mll binning')
    #parser.add_option('-o', '--output', dest='OUTPUT', type='string', help='output file')
    #parser.add_option('-l', '--label', dest='LABEL', type='string', help='legend text')
    #parser.add_option('-v', '--var', dest='VAR', type='string', help='variable')
    #parser.add_option('-c', '--cuts', dest='CUT', type='string', help='additional cuts')
    parser.add_option('-t', '--trigger', dest='TRIG', type='string', help='trigger under study')
    parser.add_option('-d', '--DST', dest='DST', type='string', help='include DST')


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


    title = "l1_2Deff dr" + opt.dRANGE +  " " + opt.TRIG + " " + opt.DST
    title = title.replace(" ", "_")
    title = title.replace(".", "p")

#    fullRange = " && drll > 0.3 && drll < 1.0"
    fullRange =  opt.dRANGE
    fullRange = fullRange.replace(" ", " && drll < ")
    fullRange = "&& drll > " + fullRange

    print fullRange

    if (opt.mRANGE == "long"):
        mllbins = [10.0,12.0,14.0,16.0,18.0,20.0,25.0,30.0,40.0,50.0]
        massRange = "&& mll > 5 && mll < 50"
    if (opt.mRANGE == "short"):
        mllbins = [1.0,2.0,4.0,6.0,8.0,10.0,14.0,18.0,24.0]
        massRange = "&& mll > 1 && mll < 24"

    pt2bins = [4.0,5.0,6.0,10.0,13.0]

    #cutden = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && abs(eta1)<1.9 && abs(eta2)<1.9 && abs(eta1)<1.9 && abs(eta2)<1.9 && mll>1.0 && mll<24.0 && drll > 0 && drll < 1.5  && passSel==1 && mediumid==1"
    baseCuts = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && abs(eta1)<1.9 && abs(eta2)<1.9 && abs(eta1)<1.9 && abs(eta2)<1.9 && passSel==1 && tightid==1"
    cutden = baseCuts + fullRange + massRange

    #weightmc = "effData125/eff125"
    #cutnum = cutden + " && passNumTrig==1"
    #cutnum = cutden + " && passNumTrig==1 && passDST==1"
    if (opt.TRIG == "all"):
        cutnum = cutden + " && (pass157==1 || passDouble4p5mass==1 || passDouble4dR==1) "
    if (opt.TRIG == "newAll"):
        cutnum = cutden + " && (pass157==1 || passDouble4p5mass==1 || passDouble4p5massdR1p2==1) "
    if ("4p5mass" in opt.TRIG):
        cutnum = cutden + " && passDouble4p5mass==1 "
    if (opt.TRIG == "4dR"):
        cutnum = cutden + " && passDouble4dR==1 "
    if (opt.TRIG == "new"):
        cutnum = cutden + " && passDouble4p5massdR1p2==1 "
    if (opt.TRIG == "157"):
        cutnum = cutden + " && pass157==1 "

    if (opt.DST == "DST"):
        cutnum += "&& passDST == 1"
    #cutnum = cutden + " && (pass157==1 || passDouble4p5mass==1 || passDouble4dR==1) && passDST==1"

    print cutnum
    #weightmc = "effDataOR/effOR"
    weightmc = "1.0"


    tmc = TChain("tree")
    #tmc.Add('originalPostProc_1.root')
    tmc.Add('/eos/user/c/ccosby/triggerSamples/DarkPhoton2018/postProc_1.root')
    sample = "DY10to50"

    hdenmc = TH2F("hdenmc","hdenmc",len(mllbins)-1,array('d',mllbins),len(pt2bins)-1,array('d',pt2bins))
    hdenmc.Sumw2()
    hnummc = TH2F("hnummc","hnummc",len(mllbins)-1,array('d',mllbins),len(pt2bins)-1,array('d',pt2bins))
    hnummc.Sumw2()

    tmc.Draw("pt2:mll>>hdenmc","("+cutden+")","goff")
    tmc.Draw("pt2:mll>>hnummc","("+weightmc+")*("+cutnum+")","goff")

    heffmc = hnummc.Clone("heffmc")
    heffmc.Sumw2()
    heffmc.SetName("l1_corrCuts_eff_"+sample+"")
    heffmc.SetTitle("l1_corrCuts_eff_"+sample+"")
    heffmc.Divide(hdenmc)
    teffmc = TEfficiency(hnummc,hdenmc)
    heffmc.SaveAs("l1_corrCuts_eff_LowMassDY_2D_2018.root")


    tdat = TChain("tree")
    tdat.Add("/eos/user/c/ccosby/triggerSamples/EGamma/postProc_1.root")
#    tdat.Add("/eos/user/c/ccosby/triggerSamples/postProc_1.root")

    sample = "Data"

    hdendat = TH2F("hdendat","hdendat",len(mllbins)-1,array('d',mllbins),len(pt2bins)-1,array('d',pt2bins))
    hdendat.Sumw2()
    hnumdat = TH2F("hnumdat","hnumdat",len(mllbins)-1,array('d',mllbins),len(pt2bins)-1,array('d',pt2bins))
    hnumdat.Sumw2()

    tdat.Draw("pt2:mll>>hdendat","("+cutden+")","goff")
    tdat.Draw("pt2:mll>>hnumdat","("+cutnum+")","goff")

    heffdat = hnumdat.Clone("heffdat")
    heffdat.Sumw2()
    heffdat.SetName("l1_corrCuts_eff_"+sample+"")
    heffdat.SetTitle("l1_corrCuts_eff_"+sample+"")
    heffdat.Divide(hdendat)
    teffdat = TEfficiency(hnumdat,hdendat)
    heffdat.SaveAs("l1_corrCuts_eff_Data2D_2018.root")

    heffcorr = TH2F("heffcorr","heffcorr",len(mllbins)-1,array('d',mllbins),len(pt2bins)-1,array('d',pt2bins))
    

    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)
    gStyle.SetPaintTextFormat("0.2f")
    gStyle.SetPalette(kBlackBody)

    c1 = TCanvas("c1","c1",1000,800)
    c1.SetLogy()
    c1.SetLogx()
    c1.SetRightMargin(0.18)
    c1.cd()
    heffdat.GetXaxis().SetMoreLogLabels()
    heffdat.GetYaxis().SetMoreLogLabels()
    heffdat.GetXaxis().SetTitle("m(#mu#mu) (GeV)")
    heffdat.GetYaxis().SetTitle("p_{T}(trailing #mu) (GeV)")
    heffdat.GetZaxis().SetTitle("Efficiency (Data)")
    heffdat.GetZaxis().SetTitleOffset(1.2)
    heffdat.Draw("colztexte")
    heffdat.GetZaxis().SetRangeUser(0.0,1.0)
    c1.Update()

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.4*c1.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31)
    latex2.DrawLatex(0.82, 0.93,"59.7 fb^{-1} (13 TeV)")
    latex2.SetTextSize(0.5*c1.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.12, 0.93, "CMS")
    latex2.SetTextSize(0.5*c1.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.21, 0.93, "Preliminary")

    #c1.SaveAs(title + "_data.pdf")
    c1.SaveAs(title + "_data.png")

    c2 = TCanvas("c2","c2",1000,800)
    c2.SetLogy()
    c2.SetLogx()
    c2.SetRightMargin(0.18)
    c2.cd()
    heffmc.GetXaxis().SetMoreLogLabels()
    heffmc.GetYaxis().SetMoreLogLabels()
    heffmc.GetXaxis().SetTitle("m(#mu#mu) (GeV)")
    heffmc.GetYaxis().SetTitle("p_{T}(trailing #mu) (GeV)")
    heffmc.GetZaxis().SetTitle("Efficiency (MC)")
    heffmc.Draw("colztexte")
    heffmc.GetZaxis().SetRangeUser(0.0,1.0)
    c2.Update()

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.4*c2.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31)
    #latex2.DrawLatex(0.82, 0.93,"59.7 fb^{-1} (13 TeV)")
    latex2.SetTextSize(0.5*c2.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.12, 0.93, "CMS")
    latex2.SetTextSize(0.5*c2.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.21, 0.93, "Preliminary")

    #c2.SaveAs(title + "_mc.pdf")
    c2.SaveAs(title + "_mc.png")

    c3 = TCanvas("c3","c3",1000,800)
    c3.SetLogy()
    c3.SetLogx()
    c3.SetRightMargin(0.18)
    c3.cd()
    ratio = heffdat.Clone("ratio")
    ratio.Sumw2()
    ratio.Divide(heffmc)
    ratio.Draw("colztexte")    
    ratio.GetZaxis().SetRangeUser(0.4,1.6)
    ratio.GetZaxis().SetTitle("Efficiency SF (Data/MC)")
    ratio.GetXaxis().SetMoreLogLabels()
    ratio.GetYaxis().SetMoreLogLabels()
    c3.Update()

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.4*c3.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31)
    latex2.DrawLatex(0.82, 0.93,"59.7 fb^{-1} (13 TeV)")
    latex2.SetTextSize(0.5*c3.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.12, 0.93, "CMS")
    latex2.SetTextSize(0.5*c3.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.21, 0.93, "Preliminary")


    ratio.SaveAs(title+ "_ratio.root")
    c3.SaveAs(title + "_ratio.png")
    #c3.SaveAs("0p5to1p5_ratio.png")

    shutil.move(os.getcwd() + "/" + title + "_ratio.png", "/eos/user/c/ccosby/www/darkPhotonl1Study/" + title + "_ratio.png")
    print("https://ccosby.web.cern.ch/ccosby/darkPhotonl1Study/" + title + "_ratio.png")

if __name__ == "__main__":
  plot()
