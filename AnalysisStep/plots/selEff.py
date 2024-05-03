from ROOT import *

h_sel = {}
h_counts = {}
f = {}
t = {}
fsf_2d = {}
hsf_2d = {}

gRandom.SetSeed(1)




bins=[4.0,5.0,6.0,7.0,8.0,10.0,12.0,15.0,20.0,30.0,50.0,100.0]
uVals = [0.858,0.880,0.894,0.908,0.921,0.936,0.948,0.960,0.965,0.974,0.977]
zVals = [0.788,0.780,0.813,0.837,0.857,0.886,0.911,0.941,0.972,0.993,0.996]
dpVals = [0.833,0.864,0.896,0.910,0.923,0.939,0.960,0.975,0.988,0.995,0.998]

for era in ["2017","2018"]:

  if (era=="2017"):
    f[era] = TFile("/eos/user/c/ccosby/triggerSamples2017/lowMassDY2017/postProc_1.root","READ")
    #fsf_2d[era] = TFile("l1_corrCuts_eff2D_ratio_2017.root","READ")
    #fsf_2d[era+"_No125"] = TFile("l1_corrCuts_eff2D_ratio_2017_No125.root","READ")
  if (era=="2018"):
    f[era] = TFile("/eos/user/c/ccosby/triggerSamples2018/lowMassDrellYan/postProc_1.root","READ")
    #f[era] = TFile("testReco_DY10to50_May23_2018_1.root","READ")
    #fsf_2d[era] = TFile("l1_2Deff_dr0_5p0_newAll_DST_ratio.root","READ")
    #fsf_2d[era] = TFile("l1_corrCuts_eff2D_ratio_2018.root","READ")
    
  t[era] = f[era].Get("tree")
  #hsf_2d[era] = fsf_2d[era].Get("ratio")
  #if (era=="2017"): hsf_2d[era+"_No125"] = fsf_2d[era+"_No125"].Get("ratio")

  h_counts[era] = TH1F("h_counts_"+era,"h_counts_"+era,60,1,24) 
  h_counts[era].Sumw2()
  h_sel[era] = TH1F("h_sel_"+era,"h_sel_"+era,60,1,24)
  h_sel[era].Sumw2()
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

    if (t[era].pt1>100.0 or t[era].pt2>100): continue



    mu1Bin = -1
    mu2Bin = -1
    for i in range(len(bins)):
      if (t[era].pt1 > bins[i]):
        mu1Bin += 1
      if (t[era].pt2 > bins[i]):
        mu2Bin += 1      

    combinedEff = zVals[mu1Bin]*zVals[mu2Bin]

    
    #print "pt2",t[era].pt2,"mll",t[era].mll,"SF",SF
    h_sel[era].Fill(t[era].mll,combinedEff)
    h_counts[era].Fill(t[era].mll)

  for i in xrange(1,h_sel[era].GetNbinsX()+1):
    if (h_counts[era].GetBinContent(i) == 0):
      continue
    else:
      h_sel[era].SetBinContent(i,h_sel[era].GetBinContent(i)/h_counts[era].GetBinContent(i))
  h_sel[era].SaveAs("finalSelEff_"+era+".root")
  
