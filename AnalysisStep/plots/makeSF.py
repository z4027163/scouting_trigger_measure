from ROOT import *

h_sf = {}
h_counts = {}
f = {}
t = {}
fsf_2d = {}
hsf_2d = {}

gRandom.SetSeed(1)

for era in ["2017","2018"]:

  if (era=="2017"):
    f[era] = TFile("/eos/user/c/ccosby/triggerSamples2017/lowMassDY2017/postProc_1.root","READ")
    fsf_2d[era] = TFile("l1_corrCuts_eff2D_ratio_2017.root","READ")
    fsf_2d[era+"_No125"] = TFile("l1_corrCuts_eff2D_ratio_2017_No125.root","READ")
  if (era=="2018"):
    f[era] = TFile("/eos/user/c/ccosby/triggerSamples2018/lowMassDrellYan/postProc_1.root","READ")
    #f[era] = TFile("testReco_DY10to50_May23_2018_1.root","READ")
    fsf_2d[era] = TFile("l1_2Deff_dr0_5p0_newAll_DST_ratio.root","READ")
    #fsf_2d[era] = TFile("l1_corrCuts_eff2D_ratio_2018.root","READ")
    
  t[era] = f[era].Get("tree")
  hsf_2d[era] = fsf_2d[era].Get("ratio")
  if (era=="2017"): hsf_2d[era+"_No125"] = fsf_2d[era+"_No125"].Get("ratio")

  h_counts[era] = TH1F("h_counts_"+era,"h_counts_"+era,60,1,24) 
  h_counts[era].Sumw2()
  h_sf[era] = TH1F("h_sf_"+era,"h_sf_"+era,60,1,24)
  h_sf[era].Sumw2()
  #h_profile = TProfile("heff125","heff125",varbins,varmin,varmax)

  Nevents = t[era].GetEntries()

  for i in xrange(Nevents):
    t[era].GetEntry(i)

    if (i>500000): break
    if (i%1000==0): print i,Nevents

    if (t[era].pt1<4.0 or t[era].pt1*3.0<t[era].mll): continue
    if (t[era].pt2<4.0 or t[era].pt2*4.0<t[era].mll): continue
    if (abs(t[era].eta1)>1.9 or abs(t[era].eta2)>1.9): continue    
    if (t[era].mll<1.0 or t[era].mll>24.0): continue
    if (t[era].passSel<1 or t[era].mediumid<1): continue


    SF = 1.0

    if (era=="2017"):

      coin = gRandom.Uniform(0,1)
      if(coin>(8.3/35.3)):
        if (t[era].pt2>10.0): SF=0.98
        else: 
          xbin = hsf_2d[era].GetXaxis().FindBin(t[era].mll);        
          ybin = hsf_2d[era].GetYaxis().FindBin(t[era].pt2);
          SF = hsf_2d[era].GetBinContent(xbin,ybin)
      else:
        if (t[era].pt2>13.0): SF=0.90
        else: 
          xbin = hsf_2d[era+"_No125"].GetXaxis().FindBin(t[era].mll);        
          ybin = hsf_2d[era+"_No125"].GetYaxis().FindBin(t[era].pt2);
          SF = hsf_2d[era+"_No125"].GetBinContent(xbin,ybin)

    if (era=="2018"):
      if (t[era].pt2>13.0): SF=0.98
      else: 
        xbin = hsf_2d[era].GetXaxis().FindBin(t[era].mll);        
        ybin = hsf_2d[era].GetYaxis().FindBin(t[era].pt2);
        SF = hsf_2d[era].GetBinContent(xbin,ybin)
    
    #print "pt2",t[era].pt2,"mll",t[era].mll,"SF",SF
    h_sf[era].Fill(t[era].mll,SF)
    h_counts[era].Fill(t[era].mll)
  
  
  
  for i in xrange(1,h_sf[era].GetNbinsX()+1):
    if (h_counts[era].GetBinContent(i) == 0):
      continue
    else:
      h_sf[era].SetBinContent(i,h_sf[era].GetBinContent(i)/h_counts[era].GetBinContent(i))
  h_sf[era].SaveAs("finalSF_"+era+".root")
  
