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
    #parser.add_option('-r', '--dRRange', dest='dRANGE', type='string', help='DeltaR binning')
    #parser.add_option('-m', '--mllRange', dest='mRANGE', type='string', help='mll binning')
    #parser.add_option('-o', '--output', dest='OUTPUT', type='string', help='output file')
    #parser.add_option('-l', '--label', dest='LABEL', type='string', help='legend text')
    #parser.add_option('-v', '--var', dest='VAR', type='string', help='variable')
    #parser.add_option('-c', '--cuts', dest='CUT', type='string', help='additional cuts')
    #parser.add_option('-t', '--trigger', dest='TRIG', type='string', help='trigger under study')
    #parser.add_option('-d', '--DST', dest='DST', type='string', help='include DST')
    #parser.add_option('-y', '--year', dest='YEAR', type='string', help='which year')


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


    title = "DST_2Deff_avg"
    title = title.replace(" ", "_")
    title = title.replace(".", "p")


    mllbins = [0.2,1.0,2.0,3.0,4.0,5.0,6.0,8.0,10.0,12.0]
    massRange = "&& mll > 0.2 && mll < 12"

    drbins = [0.0,0.5,1.0,1.5,2.5, 4.0]


    twoMu = "(pt1>15 && pt2>7)"
    twoMuMass = "(pt1>4.5 && pt2>4.5 && abs(eta1)<2.0 && abs(eta2)<2.0 && mll>7 && mll<18)"
    twoMuDR = "(pt1>4.5 && pt2>4.5 && drll<1.2)"
    twoMuDREta = "(pt1>3 && pt2>3 && abs(eta1)<1.4 && abs(eta2)<1.4 && drll<1.4)"
    
    #trigAcc = "("+twoMuDREta+")"
    trigAcc = "(("+twoMu+") || ("+twoMuMass+") || ("+twoMuDR+") || ("+twoMuDREta+"))"

    #baseCuts = "pt1*3>mll && pt2*4>mll &&"+trigAcc+" && passSel==1 && mediumid==1 "
    
    # Change back to 4 GeV before making paper plots!!!!!
    baseCuts = "pt1*3>mll && pt2*4>mll && ((pt1>3 && pt2>3) || "+twoMuDREta+") && abs(eta1)<1.9 && abs(eta2)<1.9 && passSel==1 && mediumid==1 "
    #baseCuts = "pt1*3>mll && pt2*4>mll && ((pt1>4 && pt2>4) || "+twoMuDREta+") && abs(eta1)<1.9 && abs(eta2)<1.9 && passSel==1 && mediumid==1 "

    #baseCuts = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && abs(eta1)<1.9 && abs(eta2)<1.9 && passSel==1 && mediumid==1 "
    #baseCuts = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && (abs(eta1< 1.5) || abs(eta2< 1.5)) && abs(eta1)<1.9 && abs(eta2)<1.9 && passSel==1 && mediumid==1 "
    #baseCuts = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && abs(eta1)<1.5 && abs(eta2)<1.5 && passSel==1 && mediumid==1 "
    cutden = baseCuts + massRange

    
    cutnum_2017 = cutden + " && (pass0er1p5OS==1|| pass157==1 || passDouble4p5mass==1 || passDouble4dR==1) "
    cutnum_2018 = cutden + " && (pass0er1p5OS==1|| pass157==1 || passDouble4p5mass==1 || passDouble4p5massdR1p2==1) "
      


    cutnum_2017 += "&& passDST == 1"
    cutnum_2018 += "&& passDST == 1"


    # 2017 Numerator and Denominator Histograms
    tdat_2017 = TChain("tree")    
    tdat_2017.Add("/eos/user/c/ccosby/triggerSamples2017/EGamma2017/postProc_1.root")
    hdendat_2017 = TH2F("hdendat_2017","hdendat_2017",len(mllbins)-1,array('d',mllbins),len(drbins)-1,array('d',drbins))
    hdendat_2017.Sumw2()
    hnumdat_2017 = TH2F("hnumdat_2017","hnumdat_2017",len(mllbins)-1,array('d',mllbins),len(drbins)-1,array('d',drbins))
    hnumdat_2017.Sumw2()
    tdat_2017.Draw("drll:mll>>hdendat_2017","("+cutden+")","goff")
    tdat_2017.Draw("drll:mll>>hnumdat_2017","("+cutnum_2017+")","goff")
    # 2017 Efficiency
    heffdat_2017 = hnumdat_2017.Clone("heffdat_2017")
    heffdat_2017.Sumw2()
    heffdat_2017.SetName(title)
    heffdat_2017.SetTitle(title)
    heffdat_2017.Divide(hdendat_2017)
    heffdat_2017.SaveAs("l1_corrCuts_eff_Data2D_bothYears.root")


    # 2018 Numerator and Denominator Histograms
    tdat_2018 = TChain("tree")    
    tdat_2018.Add("/eos/user/c/ccosby/triggerSamples2018/EGamma/postProc_1.root") 
    hdendat_2018 = TH2F("hdendat_2018","hdendat_2018",len(mllbins)-1,array('d',mllbins),len(drbins)-1,array('d',drbins))
    hdendat_2018.Sumw2()
    hnumdat_2018 = TH2F("hnumdat_2018","hnumdat_2018",len(mllbins)-1,array('d',mllbins),len(drbins)-1,array('d',drbins))
    hnumdat_2018.Sumw2()
    tdat_2018.Draw("drll:mll>>hdendat_2018","("+cutden+")","goff")
    tdat_2018.Draw("drll:mll>>hnumdat_2018","("+cutnum_2018+")","goff")
    # 2018 Efficiency
    heffdat_2018 = hnumdat_2018.Clone("heffdat_2018")
    heffdat_2018.Sumw2()
    heffdat_2018.SetName(title)
    heffdat_2018.SetTitle(title)
    heffdat_2018.Divide(hdendat_2018)
    heffdat_2018.SaveAs("l1_corrCuts_eff_Data2D_bothYears.root")

    #Weighted Average
    heff_average = TH2F("heff_average","heff_average",len(mllbins)-1,array('d',mllbins),len(drbins)-1,array('d',drbins))
    heff_average.Sumw2()

    heffdat_2017.Scale(35.3/96.6)
    heffdat_2018.Scale(61.3/96.6)

    heff_average.Add(heffdat_2017)
    heff_average.Add(heffdat_2018)



    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)
    gStyle.SetPaintTextFormat("0.2f")
    gStyle.SetPalette(kBird)
    gStyle.SetTextSize(0.7)
    gStyle.SetTextFont(42)
    gStyle.SetNumberContours(255)
    gStyle.SetPadTickY(1)
    gStyle.SetPadTickX(1)

    #c1 = TCanvas("c1","c1",1200,800)
    c1 = TCanvas("c1","c1",1000,870)
    #c1.SetLogy()
    #c1.SetLogx()
    c1.SetRightMargin(0.18)
    c1.cd()
    heff_average.GetXaxis().SetMoreLogLabels()
    heff_average.GetXaxis().SetTitle("#it{m}_{#it{#mu#mu}} [GeV]")
    heff_average.GetYaxis().SetTitle("#Delta#font[12]{R}_{#it{#mu#mu}}")
    heff_average.GetZaxis().SetTitle("Trigger Efficiency")
    heff_average.GetZaxis().SetTitleOffset(1.2)

    heff_average.SetTitleSize(0.04, "xyz")
    heff_average.SetTitleOffset(1.1, "xy")

    heff_average.SetLabelSize(0.031, "xyz")
    heff_average.SetMarkerSize(1.4)
    heff_average.SetMarkerColor(0)
    #heff_average.Draw("colztexte")
    heff_average.Draw("colz")
    heff_average.GetZaxis().SetRangeUser(0.0,1.0)
    c1.Update()

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.4*c1.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31)
    latex2.DrawLatex(0.86, 0.915,"96.6 fb^{-1} (13 TeV)")
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.17, 0.815,"#it{p}_{T} > 3 GeV")
    latex2.DrawLatex(0.17, 0.760,"|#it{#eta}| < 1.9")
    latex2.SetTextSize(0.55*c1.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.12, 0.915, "CMS")
    latex2.SetTextSize(0.57*c1.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    #latex2.DrawLatex(0.215, 0.915, "Preliminary")
    #latex2.DrawLatex(0.23, 0.915, "Preliminary")

    #c1.SaveAs(title + "_data.png")
    c1.SaveAs(title + "_data.pdf")
    #c1.SaveAs("0p5to1p5_data.pdf")

    shutil.copy(os.getcwd() + "/" + title + "_data.pdf", "/eos/user/c/ccosby/www/darkPhotonl1Study/newTrigEffs/" + title + "_data.pdf")
    print("https://ccosby.web.cern.ch/ccosby/darkPhotonl1Study/newTrigEffs/" + title + "_data.pdf")


if __name__ == "__main__":
  plot()
