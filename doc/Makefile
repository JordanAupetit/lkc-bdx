BIBFILE=bibliographie
RAPPORT=rapport
LATEX=pdflatex

all: $(RAPPORT).pdf

$(RAPPORT).pdf: $(BIBFILE).bib $(RAPPORT).tex
	$(LATEX) $(RAPPORT).tex
	bibtex $(RAPPORT)
	$(LATEX) $(RAPPORT).tex
	$(LATEX) $(RAPPORT).tex

.PHONY: clean

clean:
	 @rm -vf *.aux *.blg *.out *.bbl *.log *.pdf *.dvi *.toc *.synctex.gz *.lot *.loc
