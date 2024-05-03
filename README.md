# DileptonAnalysis

Use CMSSW_10_2_3

Relavant code for 2017/2018 dimuon scouting trigger efficiency measurements:

1. Customize event skimmer for desired selections and ```scram b ```
> AnalysisStep/plugins/TreeMaker.cc

2. Submit crab job, to process desired dataset.
> AnalysisStep/crab/crabConfig.py

3. Generate flat ntuple from crab job outputs
> AnalysisStep/test/tree_cfg.py

4. Plot output to show scouting trigger efficiency
> AnalysisStep/plots/DR2Deff.py