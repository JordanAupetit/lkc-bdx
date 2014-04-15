DIAPO=pdp_diapo
LATEX=pdflatex

all: $(DIAPO).pdf

$(DIAPO).pdf: $(DIAPO).tex
	$(LATEX) $(DIAPO).tex
	$(LATEX) $(DIAPO).tex

.PHONY: clean

clean:
	 @rm -vf *.aux *.blg *.out *.bbl *.log *.pdf *.dvi *.toc *.synctex.gz *.lot *.lof *.nav *.snm *.vrb
