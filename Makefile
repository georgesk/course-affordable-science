WARN_LABELS = "LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right"

all: course.pdf

clean:
	rm -f *.log *.aux *.toc *.out


%.pdf: %.aux
	pdflatex $$(echo $< | sed 's/.aux//')
	while grep -q $(WARN_LABELS) $$(echo $< | sed 's/.aux/.log/'); do \
		pdflatex $$(echo $< | sed 's/.aux//'); \
	done

%.aux: %.tex
	pdflatex $$(echo $< | sed 's/.aux//')

.PHONY = all clean
