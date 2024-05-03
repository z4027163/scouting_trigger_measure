from ROOT import *
from array import array

xbins = [1.0, 2.5]
while xbins[len(xbins)-1]<8.0:
  xbins.append(1.2*xbins[len(xbins)-1])
while xbins[len(xbins)-1]<17.0:
  xbins.append(1.2*xbins[len(xbins)-1])
xbins.append(25.0)

#xbins = [5.0,50.0]

#pt2min = "0"; pt2max = "10"
#pt2min = "0"; pt2max = "20"
#pt2min = "4"; pt2max = "5"
#pt2min = "5"; pt2max = "6"
#pt2min = "6"; pt2max = "7"
#pt2min = "8"; pt2max = "10"
#pt2min = "10"; pt2max = "50"
#pt2min = "8"; pt2max = "1000"
#pt2min = "10"; pt2max = "1000"
pt2min = "4"; pt2max = "1000"
save = "pt2_"+pt2min+"_to_"+pt2max

#cutden = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && abs(eta1)<1.9 && abs(eta2)<1.9 && abs(eta1)<1.9 && abs(eta2)<1.9 && mll>10.0 && mll<50.0 && passSel==1 && tightid==1 && maxiso<0.4 && pt2>"+pt2min+" && pt2<"+pt2max 
#cutden = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && abs(eta1)<1.9 && abs(eta2)<1.9 && abs(eta1)<1.9 && abs(eta2)<1.9 && mll>5.0 && mll<50.0 && passSel==1 && (mll>7.0 || drll<1.2) && softid==1 && maxiso<0.4 && pt2>"+pt2min+" && pt2<"+pt2max
#cutden = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && abs(eta1)<1.9 && abs(eta2)<1.9 && abs(eta1)<1.9 && abs(eta2)<1.9 && mll>5.0 && mll<50.0 && passSel==1 && softid==1 && maxiso<0.4 && pt2>"+pt2min+" && pt2<"+pt2max
#cutden = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && abs(eta1)<1.9 && abs(eta2)<1.9 && abs(eta1)<1.9 && abs(eta2)<1.9 && mll>5.0 && mll<50.0 && passSel==1 && tightid==1 && maxiso<0.4 && pt2>"+pt2min+" && pt2<"+pt2max
#cutden = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && abs(eta1)<1.9 && abs(eta2)<1.9 && abs(eta1)<1.9 && abs(eta2)<1.9 && mll>5.0 && mll<50.0 && passSel==1 && mediumid==1 && maxiso<0.4 && pt2>"+pt2min+" && pt2<"+pt2max
cutden = "pt1*3>mll && pt2*4>mll && pt1>4 && pt2>4 && abs(eta1)<1.9 && abs(eta2)<1.9 && abs(eta1)<1.9 && abs(eta2)<1.9 && mll>1.0 && mll<24.0 && passSel==1 && mediumid==1 && pt2>"+pt2min+" && pt2<"+pt2max
#cutnum = cutden + " && pass125==1"
#weightmc = "effData125/eff125"
weightdata = "1.0"
#weightdata = "1.0/(0.0534699+0.0604312*ptll+0.00012788*ptll*ptll)" #for EG datasets
#cutnum = cutden + " && passNumTrig==1 && passDST==1"
cutnum = cutden + " && (pass157==1 || passDouble4p5mass==1 || passDouble4dR==1) && passDST==1"
#cutnum = cutden + " && (pass157==1 || passDouble4p5massdR1p2 ==1 || passDouble4dR==1) && passDST==1"
#cutnum = cutden + " && passDouble4dR==1 && passDST==1"
#cutnum = cutden + " && passDST==1"
weightmc = "1.0"

tmc = TChain("tree")
tmc.Add('/eos/user/c/ccosby/triggerSamples/DarkPhoton2018/postProc_1.root')
#tmc.Add('testReco_DY4to50_HT-400to600_1.root')
#tmc.Add('testReco_DY4to50_HT-600toInf_1.root')
sample = "DY10to50"


hdenmc = TH1F("hdenmc","hdenmc",len(xbins)-1,array('d',xbins))
hdenmc.Sumw2()
hnummc = TH1F("hnummc","hnummc",len(xbins)-1,array('d',xbins))
hnummc.Sumw2()

tmc.Draw("mll>>hdenmc",cutden,"goff")
tmc.Draw("mll>>hnummc","("+cutnum+")","goff")

hdenmcsf = TH1F("hdenmcsf","hdenmcsf",len(xbins)-1,array('d',xbins))
hdenmcsf.Sumw2()
hnummcsf = TH1F("hnummcsf","hnummcsf",len(xbins)-1,array('d',xbins))
hnummcsf.Sumw2()

tmc.Draw("mll>>hdenmcsf",cutden,"goff")
tmc.Draw("mll>>hnummcsf","("+weightmc+")*("+cutnum+")","goff")

effmc = TEfficiency(hnummc,hdenmc)
heffmc = hnummc.Clone("heffmc")
heffmc.Divide(hdenmc)

effmcsf = TEfficiency(hnummcsf,hdenmcsf)
effmcsf.SetName("l1_corrCuts_eff_"+sample+"")
effmcsf.SetTitle("l1_corrCuts_eff_"+sample+"")
effmcsf.SaveAs("l1_corrCuts_eff_DY10to50_2018.root")

heffmcsf = hnummc.Clone("heffmcsf")
heffmcsf.Divide(hdenmcsf)

tdat = TChain("tree")
#tdat.Add("testTrigEff_Apr8_v5/*.root")
#tdat.Add("testReco_JetHT_Apr17_1.root")
#tdat.Add("testReco_DoubleEG_Apr17_1.root")  
#tdat.Add("testReco_SingleElectron_Apr17_1.root")
tdat.Add("/eos/user/c/ccosby/triggerSamples/EGamma/postProc_1.root")

sample = "Data"

hdendat = TH1F("hdendat","hdendat",len(xbins)-1,array('d',xbins))
hdendat.Sumw2()
hnumdat = TH1F("hnumdat","hnumdat",len(xbins)-1,array('d',xbins))
hnumdat.Sumw2()

tdat.Draw("mll>>hdendat","("+weightdata+")*("+cutden+")","goff")
tdat.Draw("mll>>hnumdat","("+weightdata+")*("+cutnum+")","goff")

effdat = TEfficiency(hnumdat,hdendat)
effdat.SetName("l1_corrCuts_eff_"+sample+"_"+save)
effdat.SetTitle("l1_corrCuts_eff_"+sample+"_"+save)
effdat.SaveAs("l1_corrCuts_eff_Data_"+save+"_2018.root")

heffdat = hnumdat.Clone("heffdat")
heffdat.Divide(hdendat)


gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
c1 = TCanvas("c1","c1",800,800)
c1.cd()
c1.SetBottomMargin(0.3)

hdum = TH1F("hdum","hdum",1,1.0,25.0)
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
effmcsf.SetLineColor(4)
effmcsf.SetLineWidth(2)
#effmcsf.Draw("epsame")

leg = TLegend(0.6,0.75,0.9,0.9)
leg.AddEntry(effmc,"Low Mass Drell-Yan MC","l")
#leg.AddEntry(effmcsf,"DY MC w/ TnP SF","l")
#leg.AddEntry(effdat,"Run 2017 JetHT Dataset","l")
leg.AddEntry(effdat,"EGamma 2018 Data","l")
leg.Draw("same")

#c1.BuildLegend()

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

hdum2 = TH1F("hdum2","hdum2",1,1.0,25.0)
hdum2.SetBinContent(1,0.001)
hdum2.SetMinimum(0.61)
hdum2.SetMaximum(1.39)
#hdum2.SetMinimum(0.95)
#hdum2.SetMaximum(1.05)
hdum2.GetXaxis().SetTitle("m(#mu#mu) (GeV)")
hdum2.Draw()

ratio = heffdat.Clone("ratio")
ratio.Divide(heffmcsf)
ratio.SetLineColor(1)
ratio.SetLineWidth(2)
ratio.SetMarkerColor(1)
ratio.Draw("same")     

c1.SaveAs("ALL_data_vs_mc_oldTrig_2018.png")

