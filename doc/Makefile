BIBCOM=existant_bibliographie
CCHARGE=cahier_des_charges
BIBFILE=bibliographie
LATEX=pdflatex

all: $(BIBCOM).pdf $(CCHARGE).pdf

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

.PHONY: clean

clean:
	 @rm -vf *.aux *.blg *.out *.bbl *.log *.pdf *.dvi
