
.PHONY: all 

tgts=output/ara_authors.html output/ara_authors.txt output/ara_authors_revtex.tex output/ara_institutes_revtex.tex output/ara_elsarticle_authors.tex output/ara_icrc_authors.tex output/ara_pos_authors.tex

all: index.html 

clean: 
	@rm -rf output 
	@rm -f index.html 

$(tgts): authors.in institutes.in ara_author_tool.py | output 
	@echo Running ara_author_tool.py
	@./ara_author_tool.py output/ara_ 

output: 
	@mkdir -p $@

index.html: output/ara_authors.html 
	@echo "<!DOCTYPE html><html><head><title>ara Author List</title></head> <body><h1 align='center'>ara Author List</h1><hr/>" > $@
	@cat $^ >> $@ 
	@echo "</body></html>" >> $@
	@echo "Please considering committing/pushing your index.html if it differs from https://araneutrino.github.io/authorlist" 
	

