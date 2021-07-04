#!/usr/bin/env python 

## ARA Author Tool to save time on author lists... 
#  Cosmin Deaconu <cozzyd@kicp.uchicago.edu>
#  apologies for the semicolons, it's a reflex at this point... 
#  This is about as brute force as it gets :)

import sys
try:
  import yaml
except ImportError:
  raise ImportError('yaml is not installed')

prefix = "ara_"  #prefix for all output files  (first argument overrideS) 
collaboration = "ARA"  # (second argument overrides) 


if len(sys.argv) > 1: 
  prefix = sys.argv[1] 

if len(sys.argv) > 2: 
  collaboration = sys.argv[2] 


## may need to do more here! 
def tex_escape(string): 

  return string.replace("&","\&")

def html_escape(string):

  return string.replace("&","&amp;") 




# Start by opening the institute list (institutes_in.yaml)
# this is now loaded as a yaml file, which is more hierarchical 
# and requires less manual parsing
institutes = {} 

finst = open("institutes_in.yaml")
parsed_finst = yaml.safe_load(finst)
for inst in parsed_finst:

  inst_id = parsed_finst[inst]['instituteid']
  inst_addr = parsed_finst[inst]['address']
  inst_short = parsed_finst[inst]['shortid']

  if inst_id in institutes: 
    print( "WARNING: duplicate ID \"%s\" found! Replacing existing." % (inst_id))

  institutes[inst_id] = (inst_addr, inst_short) 



# Then open the authors list (authors_in.yaml)

authors = [] 
sorted_institutes = [] 
institute_numbers = {}

fauth = open('authors_in.yaml')
parsed_fauth = yaml.safe_load(fauth)
for author in parsed_fauth:
  authlistname = parsed_fauth[author]['authlistname']
  affiliations = []
  for aff in parsed_fauth[author]['affiliations']:
    if aff not in institutes:
      print(" WARNING, no key for %s found in institutes.in" % (aff))
    else:
      if aff not in sorted_institutes: 
        sorted_institutes.append(aff)
        institute_numbers[aff] = len(sorted_institutes)
      affiliations.append(aff) 
  authors.append((authlistname,affiliations))     


# authors.txt 

f_authors_txt = open(prefix +"authors.txt","w") 

first = True
for author in authors: 

  if not first: 
    f_authors_txt.write(", "); 
  f_authors_txt.write(author[0] + " "); 

  for aff in author[1]:
    f_authors_txt.write("[%d]" % (institute_numbers[aff]) ); 

  first = False

f_authors_txt.write("\n\n"); 
for i in range(len(sorted_institutes)): 
  f_authors_txt.write("%d: %s\n"%( i+1, institutes[sorted_institutes[i]][0])) 


f_authors_txt.close()


# authors.html 

f_authors_html = open(prefix +"authors.html","w") 

f_authors_html.write("<p align='center'>") 
first = True
for author in authors: 

  if not first: 
    f_authors_html.write(", \n"); 
  f_authors_html.write(author[0]); 

  f_authors_html.write("<sup>"); 
  first_aff = True
  for aff in author[1]:
    if not first_aff:
      f_authors_html.write(","); 
    f_authors_html.write("<a href='#%s'>%d</a>" % (aff, institute_numbers[aff]) ); 

    first_aff = False 
  f_authors_html.write("</sup>"); 

  first = False

f_authors_html.write("<br>(<b>%s Collaboration</b>)\n" % (collaboration)); 
f_authors_html.write("</p>\n\n"); 
for i in range(len(sorted_institutes)): 
  f_authors_html.write("<br> <a name='%s'\\> <sup>%d</sup> %s\n"%(sorted_institutes[i],  i+1, html_escape(institutes[sorted_institutes[i]][0]))) 


f_authors_html.close()


# revtex_authors.tex 
f_revtex_authors = open(prefix + "revtex_authors.tex","w")
f_revtex_authors.write("%% Collaboration author file for %s in revtex format\n" % (collaboration)) 
f_revtex_authors.write("%% \\input this file in main body (make sure you also do the institutes file in the preamble!) \n\n" ) 

for author in authors: 
  name = author[0].replace(" ","~")
  f_revtex_authors.write(" \\author{%s}" % (name)) 
  if author[1] is not None: 
    for aff in author[1]: 
      f_revtex_authors.write("\\at%s" % (aff)) 
  f_revtex_authors.write("\n") 

f_revtex_authors.write("\\collaboration{%s Collaboration}\\noaffiliation\n" % (collaboration)); 

f_revtex_authors.close()


# revtex_institutes.tex 
f_revtex_institutes = open(prefix + "revtex_institutes.tex","w")
f_revtex_institutes.write("%% Collaboration institute file for %s in revtex format\n" % (collaboration)) 
f_revtex_institutes.write("%% \\input this file in the preamble (make sure you also do the author file in the body!) \n\n") 

for key in sorted_institutes: 
  addr = tex_escape(institutes[key][0]) ; 
  f_revtex_institutes.write("\\newcommand{\\at%s}{\\affiliation{%s}}\n" % (key, addr)); 

f_revtex_institutes.close()



#elsarticle_authors.tex 

f_elsarticle_authors = open(prefix + "elsarticle_authors.tex","w"); 

f_elsarticle_authors.write("%% authorlist for elsarticle publications for %s collaboration\n\n" % (collaboration) ); 

f_elsarticle_authors.write("\\collaboration{%s Collaboration}\n\n" % (collaboration)); 

for key in sorted_institutes: 
  num = institute_numbers[key]; 
  addr = tex_escape(institutes[key][0]) ; 
  f_elsarticle_authors.write("\\address[%d]{%s}\n" % (num, addr)); 

f_elsarticle_authors.write("\n\n"); 

for author in authors: 
  name = author[0].replace(" ","~")
  affs = "" 
  for aff in author[1]: 
    if affs != "": 
      affs += ","
    affs += str(institute_numbers[aff])
  f_elsarticle_authors.write("\\author[%s]{%s}\n" % (affs,name)) 

f_elsarticle_authors.close()


# pos_authors.tex 

f_pos_authors = open(prefix +"pos_authors.tex","w") 
f_pos_authors.write("%% PoS list for %s Collaboration\n\n" % (collaboration));  
first = True

f_pos_authors.write("\\author{\n"); 

f_pos_authors.write("  (%s Collaboration)\n" % (collaboration)); 

for author in authors: 
  name = author[0].replace(" ","~")
  if not first: 
    f_pos_authors.write(",\n"); 
  f_pos_authors.write("  %s" % (name)); 
  affs = "" 
  for aff in author[1]: 
    if affs != "": 
      affs += ","
    affs += str(institute_numbers[aff])
 
  f_pos_authors.write("$^{%s}$"%(affs))
  first = False

f_pos_authors.write("\n\\\\\n\\\\\n");
first = True
for i in range(len(sorted_institutes)): 
  # if not first:
    # f_pos_authors.write(",\n")
  f_pos_authors.write(" $^{%d}$%s\\\\\n"%( i+1, tex_escape(institutes[sorted_institutes[i]][0])))
  first = False 

f_pos_authors.write("\n}\n"); 
f_pos_authors.close()


## ICRC authors
f_icrc_authors = open(prefix + "icrc_authors.tex","w"); 
f_icrc_authors.write("%% ICRC list for %s Collaboration\n\n" % (collaboration));  


first = True
num_institutes = 0 
f_icrc_authors.write("\\noindent\n")
for author in authors: 

  name = author[0].replace(" ","~")

  if not first: 
    f_icrc_authors.write(", \n"); 
  f_icrc_authors.write(name); 

  first_aff = True
  for aff in author[1]:
    if not first_aff:
      f_icrc_authors.write("\\textsuperscript{,}"); 
    if institute_numbers[aff] > num_institutes: 
      f_icrc_authors.write("\\footnote[%d]{%s\label{inst%d}}" % (institute_numbers[aff], institutes[aff][0], institute_numbers[aff]))
      num_institutes+=1 
    else:
      f_icrc_authors.write("\\textsuperscript{%d}" % (institute_numbers[aff]) ); 
    first_aff = False
  first = False

f_icrc_authors.close()






























