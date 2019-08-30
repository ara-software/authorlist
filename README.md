# ANITA Author List

This is a centralized store for ANITA author lists. 

There are two files used as input, authors.in and institutions.in

Running make will then generate the other files (using a python script). 

institutions.txt defines a mapping of institution id's to addresses in a |-separated manner, e.g., including an optional short name (used for PoS) 

`UC | Dept. of Physics, Enrico Fermi Inst., Kavli Inst. for Cosmological Physics, Univ. of Chicago, Chicago, IL 60637. | University of Chicago` 


The format of authors.txt is 


`NAME  | INSTITUTION_ID1 | [ INSTIUTION_ID2 | etc.. ] `

e.g. 

`C. Deaconu. | UC`


Output is generated in several formats: 

  - `anita_revtex_authors.tex` and `anita_revtex_institutes.txt` for use with revtex journals
  - `anita_elsarticle_authors.tex`  for use with elsevier journals
  - `anita_pos_authors.tex` for use with PoS (a sort of raw format)
  - `anita_icrc_authors.tex` for use with the 2019 ICRC authorlist format. 
  - `anita_authors.html` for web display, this is used to generate an index.html that we can use for gh-pages (you should commit this if it changed!) 
  - `anita_authors.txt` for text

TODO:
  - `authors.xml` format for arxiv/inspirehep












