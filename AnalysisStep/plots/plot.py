from ROOT import *

f1 = TFile("./50Mev_sig_matrix.root","READ")
t1 = f1.Get("tree")
f2 = TFile("./50Mev_inc_matrix.root","READ")
t2 = f2.Get("tree")
f3 = TFile("./50Mev_bg_matrix.root","READ")
t3 = f3.Get("tree")

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

#h_sig = TH1F("h_sig","h_sig",18,-7,11)
#t1.Draw("matTauTau>>h_sig","matTauTau>-7.0 && matTauTau<11.0 && pt1>15 && pt2>5 && jets20==0","goff")
h_inc = TH1F("h_inc","h_inc",18,-7,11)
t2.Draw("matTauTau>>h_inc","matTauTau>-7.0 && matTauTau<10.0 && pt1>17 && pt2>8 && jets10==0 && tmet > 20","goff")
h_bg = TH1F("h_bg","h_bg",18,-7,11)
t3.Draw("matTauTau>>h_bg","matTauTau>-7.0 && matTauTau<10.0 && pt1>17 && pt2>8 && jets10==0 && tmet > 20","goff")
### Use "goff same" for the second two
### and don't use "matTauTau>>h_matTauTau".... just "matTauTau"
c1 = TCanvas("c1","c1",800,800)
c1.SetLeftMargin(0.15)
c1.SetRightMargin(0.05)
c1.SetLogy()
c1.cd()


#h_sig.SetLineColor(2)
#h_sig.SetLineWidth(4)
#h_sig.Scale(1.0/h_sig.Integral())
#h_sig.GetXaxis().SetTitle("50MeV Signal Matrix Element")
#h_sig.GetYaxis().SetTitle("a.u.")
#h_sig.Draw("hist")


h_inc.SetLineColor(3)
h_inc.SetLineWidth(4)
h_inc.Scale(1.0/h_inc.Integral())
h_inc.Draw("hist same")
h_inc.GetXaxis().SetTitle("50MeV Mod. Matrix Element Squared")
h_inc.GetYaxis().SetTitle("a.u.")


h_bg.SetLineColor(4)
h_bg.SetLineWidth(4)
h_bg.Scale(1.0/h_bg.Integral())
h_bg.Draw("hist same")



leg = TLegend(0.5,0.7,0.85,0.8)
leg.AddEntry(h_inc, "Inclusive","l")
#leg.AddEntry(h_sig,"Signal","l")
leg.AddEntry(h_bg,"Background","l")
leg.Draw("same")

latex2 = TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.4*c1.GetTopMargin())
latex2.SetTextFont(42)
latex2.SetTextAlign(31)
#latex2.DrawLatex(0.82, 0.93,"59.7 fb^{-1} (13 TeV)")
latex2.SetTextSize(0.5*c1.GetTopMargin())
latex2.SetTextFont(62)
latex2.SetTextAlign(11)
latex2.DrawLatex(0.15, 0.93, "CMS")
latex2.SetTextSize(0.45*c1.GetTopMargin())
latex2.SetTextFont(52)
latex2.SetTextAlign(11)
latex2.DrawLatex(0.26, 0.93, "Simulation Preliminary")


c1.SaveAs("matrixElement50MeV11_1_19_withcuts.pdf")
