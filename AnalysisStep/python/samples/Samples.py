samples = {}

from DileptonAnalysis.AnalysisStep.samples.DY import AddDYSamples
from DileptonAnalysis.AnalysisStep.samples.EG2018 import AddEG2018Samples
from DileptonAnalysis.AnalysisStep.samples.CTau import AddCTauSamples
from DileptonAnalysis.AnalysisStep.samples.SIDM import AddSIDMSamples

AddDYSamples(samples)
AddEG2018Samples(samples)
AddCTauSamples(samples)
AddSIDMSamples(samples)
