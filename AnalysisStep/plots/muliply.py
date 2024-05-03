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


    RAWEFF_file = TFile.Open("l1_corrCuts_eff_LowMassDY_2018.root")
    RAWEFF = RAWEFF_file.Get("l1_corrCuts_eff_NoMediumID")

    SCALE_FACTOR_file = TFile.Open("l1_2Deff_dr_all_Pt2_forCompare_2018NewSel_ratio.root")
    SCALE_FACTOR = SCALE_FACTOR_file.Get("ratio")

    RAWEFF.Multiply(SCALE_FACTOR)

    

    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)
    gStyle.SetPaintTextFormat("0.2f")
    gStyle.SetPalette(kBlackBody)

    c1 = TCanvas("c1","c1",1000,800)
    #c1.SetLogy()
    c1.SetLogx()
    c1.SetRightMargin(0.18)
    c1.cd()
    RAWEFF.GetXaxis().SetMoreLogLabels()
    #RAWEFF.GetYaxis().SetMoreLogLabels()
    RAWEFF.GetXaxis().SetTitle("m(#mu#mu) (GeV)")
    RAWEFF.GetYaxis().SetTitle("Pt2 (GeV)")
    RAWEFF.GetZaxis().SetTitle("Efficiency (MC x MedID SF)")
    RAWEFF.GetZaxis().SetTitleOffset(1.2)
    RAWEFF.Draw("colztexte")
    RAWEFF.GetZaxis().SetRangeUser(0.0,1.0)
    c1.Update()

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.4*c1.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31)
    latex2.DrawLatex(0.82, 0.93,"")
    latex2.SetTextSize(0.5*c1.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.12, 0.93, "CMS")
    latex2.SetTextSize(0.5*c1.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.21, 0.93, "Preliminary")

    c1.SaveAs("noIDrescaled.pdf")

    shutil.copy(os.getcwd() + "/noIDrescaled.pdf", "/eos/user/c/ccosby/www/darkPhotonl1Study/newTrigEffs/noIDrescaled.pdf")
    print("https://ccosby.web.cern.ch/ccosby/darkPhotonl1Study/newTrigEffs/noIDrescaled.pdf")



if __name__ == "__main__":
  plot()

