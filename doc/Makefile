BIBCOM=bibliographieCommentee
EXISTANT=existant
BIBFILE=bibliographie
LATEX=pdflatex

all: $(BIBCOM).dvi $(EXISTANT).dvi

$(BIBCOM).dvi: $(BIBFILE).bib $(BIBCOM).tex
	$(LATEX) $(BIBCOM).tex
	bibtex $(BIBCOM)
	$(LATEX) $(BIBCOM).tex
	$(LATEX) $(BIBCOM).tex

$(EXISTANT).dvi: $(EXISTANT).tex
	$(LATEX) $(EXISTANT).tex

.PHONY: clean

clean:
	rm *.aux *.blg *.out *.bbl *.log *.pdf *.dvi
