# ARA Author List

This is a centralized store for ARA author lists. 

There are two files used as input, authors_in.yaml and institutions_in.yaml

Running `make` will then generate the other files (using a python script). 

institutions_in.yml defines a mapping of institution id's to addresses, including an optional short name (used for PoS). Use standard YAML syntax, for example:

```yaml
UC:
  instituteid: UC
  shortid: University of Chicago
  address: Dept. of Physics, Enrico Fermi Institue, Kavli Institute for Cosmological Physics, University of Chicago, Chicago, IL 60637 
```

The format of authors_in.yaml is 

```yaml
C. Deaconu:
  authlistname: C. Deaconu
  affiliations: 
    - UC
  orcid: 0000-0002-4953-6397
```

If the orcid of the author is known, it can also be added. Currently the only
supported fields are `authlistname`, `affiliations`, and `orcid`.
An author can have more than one affiliation; for example:

```yaml
D.Z. Besson:
  authlistname: D.Z. Besson
  affiliations: 
    - KU
    - Moscow
  orcid: 0000-0001-6733-963X
```



Output is generated in several formats: 

  - `ara_revtex_authors.tex` and `ara_revtex_institutes.txt` for use with revtex journals
  - `ara_elsarticle_authors.tex`  for use with elsevier journals
  - `ara_pos_authors.tex` for use with PoS (a sort of raw format)
  - `ara_icrc_authors.tex` for use with the 2019 ICRC authorlist format. 
  - `ara_authors.html` for web display, this is used to generate an index.html that we can use for gh-pages (you should commit this if it changed!) 
  - `ara_authors.txt` for text
  - `ara_authors.xml` format for arxiv/inspirehep -- NOTE: the xml file generated uses a placehold publicationReference which should be changed by hand












