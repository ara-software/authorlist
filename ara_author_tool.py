#!/usr/bin/env python 

## ARA Author Tool to save time on author lists... 
#  Cosmin Deaconu <cozzyd@kicp.uchicago.edu>
#  apologies for the semicolons, it's a reflex at this point... 
#  This is about as brute force as it gets :)

import sys
import datetime
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
  authorids = {}
  if 'orcid' in parsed_fauth[author]:
    authorids['orcid'] = parsed_fauth[author]['orcid']
  if 'inspireid' in parsed_fauth[author]:
    authorids['inspireid'] = parsed_fauth[author]['inspireid']
  authors.append((authlistname,affiliations,authorids))     


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
      #f_icrc_authors.write("\\footnote[%d]{%s\label{inst%d}}" % (institute_numbers[aff], institutes[aff][0], institute_numbers[aff]))
      f_icrc_authors.write("\\textsuperscript{%d}" % (institute_numbers[aff]))
      num_institutes+=1 
    else:
      f_icrc_authors.write("\\textsuperscript{%d}" % (institute_numbers[aff]) ); 
    first_aff = False
  first = False

f_icrc_authors.write("\n\\\\\n\\\\\n")
for i in range(len(sorted_institutes)): 
  f_icrc_authors.write("\\textsuperscript{%d} %s\\\\\n"%( i+1, institutes[sorted_institutes[i]][0])) 

f_icrc_authors.close()

## author XML file
f_xml_authors = open(prefix + "authors.xml","w")

# initial header info (DO NOT CHANGE)
f_xml_authors.write('<?xml version="1.0" encoding="UTF-8"?>\n\n')

f_xml_authors.write('<!DOCTYPE collaborationauthorlist [\n')
f_xml_authors.write('<!ELEMENT collaborationauthorlist ( cal:creationDate, cal:publicationReference, cal:collaborations, cal:organizations, cal:authors ) >\n')
f_xml_authors.write('<!ATTLIST collaborationauthorlist\n')
f_xml_authors.write('\txmlns:foaf CDATA #FIXED "http://xmlns.com/foaf/0.1/"\n')
f_xml_authors.write('\txmlns:cal  CDATA #FIXED "http://inspirehep.net/info/HepNames/tools/authors_xml/"\n')
f_xml_authors.write('>\n\n')

f_xml_authors.write('<!ELEMENT cal:creationDate ( #PCDATA ) >\n')
f_xml_authors.write('<!ELEMENT cal:publicationReference ( #PCDATA ) >\n')

f_xml_authors.write('<!-- **************** COLLABORATIONS ********************* -->\n')
f_xml_authors.write('\t<!ELEMENT cal:collaborations ( cal:collaboration+ ) >\n')
f_xml_authors.write('\t\t<!ELEMENT cal:collaboration ( foaf:name, cal:experimentNumber?, cal:group? ) >\n')
f_xml_authors.write('\t\t<!ATTLIST cal:collaboration\n')
f_xml_authors.write('\t\t\tid ID #REQUIRED\n')
f_xml_authors.write('\t\t>\n\n')

f_xml_authors.write('\t<!ELEMENT cal:experimentNumber ( #PCDATA ) >\n\n')

f_xml_authors.write('\t<!ELEMENT cal:group ( #PCDATA ) >\n')
f_xml_authors.write('\t\t<!ATTLIST cal:group\n')
f_xml_authors.write('\t\twith IDREF #IMPLIED\n')
f_xml_authors.write('\t\t>\n\n')

f_xml_authors.write('<!-- ORGANIZATIONS -->\n')
f_xml_authors.write('\t<!ELEMENT cal:organizations ( foaf:Organization+ ) >\n')
f_xml_authors.write('\t\t<!ELEMENT foaf:Organization ( cal:orgDomain?, foaf:name, cal:orgName*, cal:orgStatus*, cal:orgAddress?, cal:group? ) >\n')
f_xml_authors.write('\t\t<!ATTLIST foaf:Organization\n')
f_xml_authors.write('\t\t\tid ID #REQUIRED\n')
f_xml_authors.write('\t\t>\n\n')

f_xml_authors.write('\t\t<!ELEMENT cal:orgAddress ( #PCDATA ) >\n')
f_xml_authors.write('\t\t<!ELEMENT cal:orgDomain ( #PCDATA ) >\n\n')

f_xml_authors.write('\t\t<!ELEMENT cal:orgName ( #PCDATA ) >\n')
f_xml_authors.write('\t\t<!ATTLIST cal:orgName\n')
f_xml_authors.write('\t\t\tsource CDATA "INTERNAL"\n')
f_xml_authors.write('\t\t>\n\n')

f_xml_authors.write('\t\t<!ELEMENT cal:orgStatus ( #PCDATA ) >\n')
f_xml_authors.write('\t\t<!ATTLIST cal:orgStatus\n')
f_xml_authors.write('\t\t\tcollaborationid IDREF #IMPLIED\n')
f_xml_authors.write('\t\t>\n\n')

f_xml_authors.write('<!-- AUTHORS -->\n')
f_xml_authors.write('<!ELEMENT cal:authors ( foaf:Person+ ) >\n')
f_xml_authors.write('\t<!ELEMENT foaf:Person ( foaf:name?, cal:authorNameNative?, foaf:givenName?, foaf:familyName, cal:authorSuffix?, cal:authorStatus?, cal:authorNamePaper, cal:authorNamePaperGiven?, cal:authorNamePaperFamily?, cal:authorCollaboration?, cal:authorAffiliations?, cal:authorids?, cal:authorFunding? ) >\n\n')

f_xml_authors.write('\t<!ELEMENT foaf:familyName ( #PCDATA ) >\n')
f_xml_authors.write('\t<!ELEMENT foaf:givenName ( #PCDATA ) >\n')
f_xml_authors.write('\t<!ELEMENT foaf:name ( #PCDATA ) >\n\n')

f_xml_authors.write('\t<!ELEMENT cal:authorNameNative ( #PCDATA ) >\n')
f_xml_authors.write('\t<!ELEMENT cal:authorNamePaper ( #PCDATA ) >\n')
f_xml_authors.write('\t<!ELEMENT cal:authorNamePaperGiven ( #PCDATA ) >\n')
f_xml_authors.write('\t<!ELEMENT cal:authorNamePaperFamily ( #PCDATA ) >\n')
f_xml_authors.write('\t<!ELEMENT cal:authorStatus ( #PCDATA ) >\n')
f_xml_authors.write('\t<!ELEMENT cal:authorSuffix ( #PCDATA ) >\n\n')

f_xml_authors.write('\t<!ELEMENT cal:authorCollaboration EMPTY >\n')
f_xml_authors.write('\t<!ATTLIST cal:authorCollaboration\n')
f_xml_authors.write('\t\tcollaborationid IDREF "c1"\n')
f_xml_authors.write('\t\tposition CDATA #IMPLIED\n')
f_xml_authors.write('\t>\n\n')

f_xml_authors.write('\t<!ELEMENT cal:authorAffiliations ( cal:authorAffiliation* ) >\n')
f_xml_authors.write('\t<!ELEMENT cal:authorAffiliation EMPTY >\n')
f_xml_authors.write('\t<!ATTLIST cal:authorAffiliation\n')
f_xml_authors.write('\t\torganizationid IDREF #REQUIRED\n')
f_xml_authors.write('\t\tconnection CDATA "Affiliated with"\n')
f_xml_authors.write('\t>\n\n')

f_xml_authors.write('\t<!ELEMENT cal:authorids ( cal:authorid* ) >\n')
f_xml_authors.write('\t<!ELEMENT cal:authorid ( #PCDATA ) >\n')
f_xml_authors.write('\t<!ATTLIST cal:authorid\n')
f_xml_authors.write('\t\tsource CDATA #REQUIRED\n')
f_xml_authors.write('\t>\n')
f_xml_authors.write('\t<!ELEMENT cal:authorFunding ( #PCDATA ) >\n\n')


f_xml_authors.write('\n]>\n')
f_xml_authors.write('<!--\n')
f_xml_authors.write('\tARA author list for INSPIRE.\n')
f_xml_authors.write('-->\n')

f_xml_authors.write('<collaborationauthorlist\n')
f_xml_authors.write('\txmlns:foaf="http://xmlns.com/foaf/0.1/"\n')
f_xml_authors.write('\txmlns:cal="http://inspirehep.net/info/HepNames/tools/authors_xml/">\n\n')

# publication specific info - it's expected that the publication reference is entered by hand after generation
now = datetime.datetime.now()
f_xml_authors.write('\t<cal:creationDate>%s</cal:creationDate>\n' % now.strftime("%Y-%m-%d_%H:%M"))
f_xml_authors.write('\t<cal:publicationReference>ENTER ARXIV URL HERE</cal:publicationReference>\n\n')

# collaboration info
f_xml_authors.write('\t<cal:collaborations>\n')
f_xml_authors.write('\t\t<cal:collaboration id="c1">\n')
f_xml_authors.write('\t\t\t<foaf:name>ARA</foaf:name>\n')
f_xml_authors.write('\t\t</cal:collaboration>\n')
f_xml_authors.write('\t</cal:collaborations>\n\n')

# institution info
f_xml_authors.write('\t<cal:organizations>\n')
for aff in sorted_institutes:
  f_xml_authors.write('\t\t<foaf:Organization id="a%d">\n' % institute_numbers[aff])
  f_xml_authors.write('\t\t\t<cal:orgDomain>http://</cal:orgDomain>\n')
  f_xml_authors.write('\t\t\t<foaf:name>%s</foaf:name>\n' % institutes[aff][1])
  f_xml_authors.write('\t\t\t<cal:orgName source="INTERNAL">%s</cal:orgName>\n' % institutes[aff][1])
  f_xml_authors.write('\t\t\t<cal:orgStatus collaborationid="c1">member</cal:orgStatus>\n')
  f_xml_authors.write('\t\t\t<cal:orgAddress> %s</cal:orgAddress>\n' % institutes[aff][0])
  f_xml_authors.write('\t\t</foaf:Organization>\n')
f_xml_authors.write('\t</cal:organizations>\n\n')

# author info
f_xml_authors.write('\t<cal:authors>\n')
for author in authors:
  f_xml_authors.write('\t\t<foaf:Person>\n')
  f_xml_authors.write('\t\t\t<foaf:name>%s</foaf:name>\n' % author[0])
  f_xml_authors.write('\t\t\t<cal:authorNameNative/>\n')
  f_xml_authors.write('\t\t\t<foaf:givenName>%s</foaf:givenName>\n' % author[0].split(' ')[0])
  f_xml_authors.write('\t\t\t<foaf:familyName>%s</foaf:familyName>\n' % author[0].split('. ')[1])
  f_xml_authors.write('\t\t\t<cal:authorSuffix/>\n')
  f_xml_authors.write('\t\t\t<cal:authorStatus/>\n')
  f_xml_authors.write('\t\t\t<cal:authorNamePaper>%s</cal:authorNamePaper>\n' % author[0])
  f_xml_authors.write('\t\t\t<cal:authorNamePaperGiven>%s</cal:authorNamePaperGiven>\n' % author[0].split(' ')[0])
  f_xml_authors.write('\t\t\t<cal:authorNamePaperFamily>%s</cal:authorNamePaperFamily>\n' % author[0].split('. ')[1])
  f_xml_authors.write('\t\t\t<cal:authorCollaboration collaborationid="c1" position=""/>\n')
  f_xml_authors.write('\t\t\t<cal:authorAffiliations>\n')
  for aff in author[1]:
    f_xml_authors.write('\t\t\t\t<cal:authorAffiliation organizationid="a%d" connection=""/>\n' % institute_numbers[aff])
  f_xml_authors.write('\t\t\t</cal:authorAffiliations>\n')
  if len(author[2]) > 0:
    f_xml_authors.write('\t\t\t<cal:authorids>\n')
    for key in author[2]:
      if key =='orcid':
        f_xml_authors.write('\t\t\t\t<cal:authorid source="ORCID">%s</cal:authorid>\n' % author[2]['orcid'])
      if key == 'inspireid':
        f_xml_authors.write('\t\t\t\t<cal:authorid source="INSPIRE">%s</cal:authorid>\n' % author[2]['inspireid'])
    f_xml_authors.write('\t\t\t</cal:authorids>\n')
  f_xml_authors.write('\t\t</foaf:Person>\n')
f_xml_authors.write('\t</cal:authors>\n')

# end of xml file
f_xml_authors.write('</collaborationauthorlist>')
f_xml_authors.close()




















