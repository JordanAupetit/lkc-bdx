NPCOMPLET=np_complet
LATEX=pdflatex

all: $(NPCOMPLET).pdf

$(NPCOMPLET).pdf: $(NPCOMPLET).tex
	$(LATEX) $(NPCOMPLET).tex

.PHONY: clean

clean:
	 @rm -vf *.aux *.blg *.out *.bbl *.log *.pdf *.dvi
