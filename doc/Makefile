BIBCOM=existantBibliographie
BIBFILE=bibliographie
LATEX=pdflatex

all: $(BIBCOM).dvi

$(BIBCOM).dvi: $(BIBFILE).bib $(BIBCOM).tex
	$(LATEX) $(BIBCOM).tex
	bibtex $(BIBCOM)
	$(LATEX) $(BIBCOM).tex
	$(LATEX) $(BIBCOM).tex

.PHONY: clean

clean:
	 @rm -vf *.aux *.blg *.out *.bbl *.log *.pdf *.dvi
