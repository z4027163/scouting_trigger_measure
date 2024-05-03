import os,sys
from ROOT import TGraphAsymmErrors
from ROOT import TGraphErrors
from ROOT import TColor
#from ROOT import TGraph
from array import array
from ROOT import *
from operator import truediv
import random
import math
from glob import glob
import re
import sys
from math import sqrt


high_file_2018 = TFile.Open("modifiedMllEffD2018high.root")
high_2018 = high_file_2018.Get("honemllD_clone")
high_file_2017 = TFile.Open("modifiedMllEffD2017high.root")
high_2017 = high_file_2017.Get("honemllD_clone")

low_file_2018 = TFile.Open("modifiedMllEffD2018low.root")
low_2018 = low_file_2018.Get("honemllD_clone")
low_file_2017 = TFile.Open("modifiedMllEffD2017low.root")
low_2017 = low_file_2017.Get("honemllD_clone")



mllbins = [1.0,2.0,3.0,4.0,5.0,6.0,8.0,10.0,12.0]
combined_array2017 = []
combined_array2018 = []

nbins_low = low_2018.GetPassedHistogram().GetNbinsX()
nbins_high = high_2018.GetPassedHistogram().GetNbinsX()



#fill array with low entries (1-4)
for i in range(nbins_low):
    combined_array2018.append(low_2018.GetEfficiency(i))
    combined_array2017.append(low_2017.GetEfficiency(i))

#fill array with high entries (4-12)
for i in range(nbins_high):
    combined_array2018.append(high_2018.GetEfficiency(i))
    combined_array2017.append(high_2017.GetEfficiency(i))

print(combined_array2018)
print(combined_array2017)

hist_2017 = TH1F("hist_2017", "hist_2017", 8, mllbins)
hist_2018 = TH1F("hist_2018", "hist_2018", 8, mllbins)

for i in range(len(combined_array2018)):
    hist_2018.SetBinContent(i, combined_array2018[i])
    hist_2017.SetBinContent(i, combined_array2017[i])

ones = [1,1,1,1,1,1,1,1]
efficiency2018 = TEfficiency(hist_2018, ones)
efficiency2017 = TEfficiency(hist_2017, ones)
