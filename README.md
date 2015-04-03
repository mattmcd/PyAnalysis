PyAnalysis
==========
Data analysis using Python.  The code here is mainly intended for me to
learn the differences between the statistical tools available within Python
compared to the MATLAB tools which which I have more experience.  Also to
brush up on the Python language in general.

This project also contains non-Python code concerned with general modelling 
and analysis.  In particular, a long standing interest of mine has been use
of Domain Specific Lanaguages to construct a semantic model of the analysis
application.  

Implementation
==============
Rough plan for the next few commits:

- [x] Create mda (Matt's Data Analysis) package to check understanding of
  modules.
- [ ] Lattice Reduction
  - [x] Sorted QR algorithm.
  - [ ] LLL lattice reduction algorithm
- [ ] DSL for defining models
  - [ ] ANTLR grammar for model definition 
  - [ ] Analysis components (Python)
  - [ ] Dependency injection framework/builder (Python)
  - [ ] Grammar Listener to populate semantic model using builder (Python)
