BIBCOM=existant_bibliographie
CCHARGE=cahier_des_charges
ARCHI=architecture
BIBFILE=bibliographie
RAPPORT=rapport
LATEX=pdflatex

all: $(BIBCOM).pdf $(CCHARGE).pdf $(ARCHI).pdf $(RAPPORT).pdf

$(RAPPORT).pdf: $(BIBFILE).bib $(RAPPORT).tex
	$(LATEX) $(RAPPORT).tex
	bibtex $(BIBCOM)
	$(LATEX) $(RAPPORT).tex
	$(LATEX) $(RAPPORT).tex

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


$(ARCHI).pdf: $(BIBFILE).bib $(ARCHI).tex
	$(LATEX) $(ARCHI).tex
	bibtex $(BIBCOM)
	$(LATEX) $(ARCHI).tex
	$(LATEX) $(ARCHI).tex


.PHONY: clean

clean:
	 @rm -vf *.aux *.blg *.out *.bbl *.log *.pdf *.dvi
