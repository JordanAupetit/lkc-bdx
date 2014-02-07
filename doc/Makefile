BIBCOM=existant_bibliographie
CCHARGE=cahier_charge
TESTS=tests
BIBFILE=bibliographie
LATEX=pdflatex

all: $(BIBCOM).pdf $(CCHARGE).pdf $(TESTS).pdf

$(BIBCOM).pdf: $(BIBFILE).bib $(BIBCOM).tex
	$(LATEX) $(BIBCOM).tex
	bibtex $(BIBCOM)
	$(LATEX) $(BIBCOM).tex
	$(LATEX) $(BIBCOM).tex

$(CCHARGE).pdf: $(BIBFILE).bib $(CCHARGE).tex
	$(LATEX) $(CCHARGE).tex
	bibtex $(BIBCOM)
	$(LATEX) $(CCHARGE).tex
	$(LATEX) $(CCHARGE).tex

$(TESTS).pdf: $(BIBFILE).bib $(TESTS).tex
	$(LATEX) $(TESTS).tex
	bibtex $(BIBCOM)
	$(LATEX) $(TESTS).tex
	$(LATEX) $(TESTS).tex
.PHONY: clean

clean:
	 @rm -vf *.aux *.blg *.out *.bbl *.log *.pdf *.dvi
