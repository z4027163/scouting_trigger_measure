from ROOT import *
from array import array
import shutil
import sys, os, pwd, commands, glob, fnmatch
import optparse, shlex, re
import time
from time import gmtime, strftime
import math
from array import array

xbins = [0.0]
while xbins[len(xbins)-1]<=2.0:
  xbins.append(xbins[len(xbins)-1]+0.05)

pt2min = "0"; pt2max = "1000"
save = "newAllTrigLowMass"

cutden = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && abs(eta1)<1.9 && abs(eta2)<1.9 && abs(eta1)<1.9 && abs(eta2)<1.9 && mll>1.0 && mll<24.0 && passSel==1 && mediumid==1 && pt2>"+pt2min+" && pt2<"+pt2max

weightdata = "1.0"
#cutnum = cutden + " && passDouble4p5massdR1p2==1"
#cutnum = cutden + " && passDouble4dR==1"
#cutnum = cutden + " && (pass157==1 || passDouble4p5mass==1 || passDouble4dR==1) && passDST==1"
cutnum = cutden + " && (pass157==1 || passDouble4p5mass==1 || passDouble4p5massdR1p2==1) && passDST==1"

weightmc = "1.0"

tmc = TChain("tree")
#tmc.Add('/eos/user/c/ccosby/triggerSamples/Zdark043020DY/postProc_1.root')
tmc.Add('/eos/user/c/ccosby/triggerSamples/DarkPhoton2018/postProc_1.root')
sample = "DY5to50"

hdenmc = TH1F("hdenmc","hdenmc", 60, 1 ,24)
hdenmc.Sumw2()
hnummc = TH1F("hnummc","hnummc", 60, 1, 24)
hnummc.Sumw2()

tmc.Draw("mll>>hdenmc",cutden,"goff")
tmc.Draw("mll>>hnummc","("+cutnum+")","goff")

effmc = TEfficiency(hnummc,hdenmc)
effmc.SetName("l1_corrCuts_eff_"+sample+"_"+save)
effmc.SetTitle("l1_corrCuts_eff_"+sample+"_"+save)
effmc.SaveAs("l1_corrCuts_eff_MC_"+save+"_2018_mll.root")


heffmc = hnummc.Clone("heffmc")
heffmc.Divide(hdenmc)

tdat = TChain("tree")
tdat.Add("/eos/user/c/ccosby/triggerSamples/EGamma/postProc_1.root")
sample = "Data"

hdendat = TH1F("hdendat","hdendat",60, 1, 24)
hdendat.Sumw2()
hnumdat = TH1F("hnumdat","hnumdat",60, 1, 24)
hnumdat.Sumw2()

tdat.Draw("mll>>hdendat","("+weightdata+")*("+cutden+")","goff")
tdat.Draw("mll>>hnumdat","("+weightdata+")*("+cutnum+")","goff")

effdat = TEfficiency(hnumdat,hdendat)
effdat.SetName("l1_corrCuts_eff_"+sample+"_"+save)
effdat.SetTitle("l1_corrCuts_eff_"+sample+"_"+save)
effdat.SaveAs("l1_corrCuts_eff_Data_"+save+"_2018_mll.root")

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
hdum.GetXaxis().SetTitle("")
hdum.GetXaxis().SetLabelSize(0)
hdum.Draw()

effdat.SetLineColor(1)
effdat.SetLineWidth(2)
effdat.Draw("epsame")
effmc.SetLineColor(2)
effmc.SetLineWidth(2)
effmc.Draw("epsame")


leg = TLegend(0.4,0.4,0.85,0.6)
leg.AddEntry(effmc,"DY MC","l")
leg.AddEntry(effdat,"Run 2018 EGamma Dataset","l")
leg.Draw("same")

latex2 = TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.4*c1.GetTopMargin())
latex2.SetTextFont(42)
latex2.SetTextAlign(31)
latex2.DrawLatex(0.89, 0.93,"59.7 fb^{-1} (13 TeV)")
latex2.SetTextSize(0.5*c1.GetTopMargin())
latex2.SetTextFont(62)
latex2.SetTextAlign(11)
latex2.DrawLatex(0.12, 0.93, "CMS")
latex2.SetTextSize(0.5*c1.GetTopMargin())
latex2.SetTextFont(52)
latex2.SetTextAlign(11)
latex2.DrawLatex(0.23, 0.93, "Preliminary")

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
hdum2.GetXaxis().SetTitle("#DeltaR(#mu#mu)")
hdum2.Draw()

ratio = heffdat.Clone("ratio")
ratio.Divide(heffmc)
ratio.SetLineColor(1)
ratio.SetLineWidth(2)
ratio.SetMarkerColor(1)
ratio.Draw("same")     

ratio.SaveAs("l1_corrCuts_eff_data_vs_mc_"+save+"_2018_dR.root")

#c1.SaveAs("data_vs_mc_"+save+"_2018_dR.png")
#shutil.move(os.getcwd() + "/" + "data_vs_mc_"+save+"_2018_dR.png", "/eos/user/c/ccosby/www/darkPhotonl1Study/" +"data_vs_mc_"+save+"_2018_dR.png")
print("https://ccosby.web.cern.ch/ccosby/darkPhotonl1Study/" + "data_vs_mc_"+save+"_2018_dR.png")


