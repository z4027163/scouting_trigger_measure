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
    parser.add_option('-v', '--var', dest='VAR', type='string', help='variable')
    #parser.add_option('-c', '--cuts', dest='CUT', type='string', help='additional cuts')
    #parser.add_option('-t', '--trigger', dest='TRIG', type='string', help='trigger under study')
    #parser.add_option('-d', '--DST', dest='DST', type='string', help='include DST')
    parser.add_option('-y', '--year', dest='YEAR', type='string', help='which year')
#    parser.add_option('-b', '--bins', dest='BINS', type='string', help='number of bins')
#    parser.add_option('-m', '--max', dest='MAX', type='string', help='upper limit')


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


    title = "dist"  +  " " + opt.VAR  + " " + opt.YEAR
    title = title.replace(" ", "_")
    title = title.replace(".", "p")

    if (opt.VAR == "mll"):
        bins = [1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,15.0,16.0,17.0,18.0,19.0,20.0,21.0,22.0,23.0,24.0]
    if (opt.VAR == 'drll'):
        bins = [0.0,0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0,2.25,2.5,3.0,3.5,4.0]


    #cutden = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && abs(eta1)<1.9 && abs(eta2)<1.9 && abs(eta1)<1.9 && abs(eta2)<1.9 && mll>1.0 && mll<24.0 && drll > 0 && drll < 1.5  && passSel==1 && mediumid==1"
#    baseCuts = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && abs(eta1)<1.9 && abs(eta2)<1.9 && passSel==1 && mediumid==1 "
    baseCuts = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && abs(eta1)<1.9 && abs(eta2)<1.9 "
    massRange = "&& mll > 1 && mll < 24"
    cuts = baseCuts + massRange

    print cuts
    #weightmc = "effDataOR/effOR"
    weightmc = "1.0"


    tmc = TChain("tree")
    #tmc.Add('originalPostProc_1.root')

    if (opt.YEAR =="2018"):
#        cuts += "&& (pass157==1 || passDouble4p5mass==1 || passDouble4p5massdR1p2==1)"
        cutsMC = cuts
        tmc.Add('/eos/user/c/ccosby/triggerSamples2018/lowMassDrellYan/postProc_1.root')
    if (opt.YEAR =="2017"):
#        cuts +=  " && (pass157==1 || passDouble4p5mass==1 || passDouble4dR==1)"
        cutsMC = cuts
        tmc.Add('/eos/user/c/ccosby/triggerSamples2017/lowMassDY2017/postProc_1.root')
    #tmc.Add('/eos/user/c/ccosby/triggerSamples/DrellYan/postProc_1.root')


    tdat = TChain("tree")
    
    if (opt.YEAR == "2018"):
        cutsData = cuts
        tdat.Add("/eos/user/c/ccosby/triggerSamples2018/EGamma/postProc_1.root")
    if (opt.YEAR == "2017"):
        cutsData = cuts + '&& L1_12_5_On == 1'
        tdat.Add("/eos/user/c/ccosby/triggerSamples2017/EGamma2017/postProc_1.root")


    gStyle.SetOptTitle(0)
#    gStyle.SetOptStat(0)

    hdata = TH1F("hdata","hdata",len(bins)-1, array('d',bins))
    tdat.Draw( opt.VAR + ">>hdata" , cutsData, "goff")
    hmc = TH1F("hmc","hmc",len(bins)-1, array('d',bins))
    tmc.Draw( opt.VAR + ">>hmc" , cutsMC, "goff")


#    gStyle.SetPaintTextFormat("0.2f")
    gStyle.SetPalette(kBlackBody)

    c1 = TCanvas("c1","c1",1000,800)
#    c1.SetRightMargin(0.18)
#    c1.SetLogy()
    c1.cd()
    hdata.GetXaxis().SetMoreLogLabels()
    #hdata.GetYaxis().SetMoreLogLabels()
    hdata.GetXaxis().SetTitle(opt.VAR)
    hdata.GetYaxis().SetTitle("Events")
    hdata.Draw("cbe")
    c1.Update()

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.4*c1.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31)
    if (opt.YEAR == "2018"):
        latex2.DrawLatex(0.82, 0.93,"59.7 fb^{-1} (13 TeV)")
    if (opt.YEAR == "2017"):
        latex2.DrawLatex(0.82, 0.93,"27 fb^{-1} (13 TeV)")
    latex2.SetTextSize(0.5*c1.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.12, 0.93, "CMS")
    latex2.SetTextSize(0.5*c1.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.21, 0.93, "Preliminary")

    #c1.SaveAs(title + "_data.pdf")
    #c1.SaveAs(title + "_data.png")
    
    c1.SaveAs(title + "_data.png")
    #c1.SaveAs("0p5to1p5_data.png")

    shutil.move(os.getcwd() + "/" + title + "_data.png", "/eos/user/c/ccosby/www/darkPhotonl1Study/" + title + "_data.png")
    print("https://ccosby.web.cern.ch/ccosby/darkPhotonl1Study/" + title + "_data.png")



    c2 = TCanvas("c2","c2",1000,800)
    c2.SetRightMargin(0.18)
#    c2.SetLogy()
    c2.cd()
    hmc.GetXaxis().SetMoreLogLabels()
    hmc.GetXaxis().SetTitle(opt.VAR)
    hmc.GetYaxis().SetTitle("Events")
    hmc.Draw("cbe")
    c2.Update()

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.4*c2.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31)
    latex2.SetTextSize(0.5*c2.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.12, 0.93, "CMS")
    latex2.SetTextSize(0.5*c2.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.21, 0.93, "Preliminary")

    #c2.SaveAs(title + "_mc.pdf")
    #c2.SaveAs(title + "_mc.png")
    
    c2.SaveAs(title + "_mc.png")
    #c2.SaveAs("0p5to1p5_mc.png")

    shutil.move(os.getcwd() + "/" + title + "_mc.png", "/eos/user/c/ccosby/www/darkPhotonl1Study/" + title + "_mc.png")
    print("https://ccosby.web.cern.ch/ccosby/darkPhotonl1Study/" + title + "_mc.png")




if __name__ == "__main__":
  plot()
