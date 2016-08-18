WARN_LABELS = "LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right"

all: course.pdf

clean:
	rm -f *.log *.aux *.toc *.out


%.pdf: %.tex
	pdflatex -interaction=nonstopmode $<
	while grep -q $(WARN_LABELS) $$(echo $< | sed 's/.tex/.log/'); do \
	  pdflatex -interaction=nonstopmode $<; \
	done

.PHONY = all clean
