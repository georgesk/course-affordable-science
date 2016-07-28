UI_SRC    = $(shell ls *.ui)
UI_TARGET = $(patsubst %.ui, UI_%.py, $(UI_SRC))
PYUIC     = pyuic4

all: $(UI_TARGET)

UI_%.py: %.ui
	$(PYUIC) $< -o $@
	# fix a bug of debian packages
	sed 's/from qwt_plot/from qwt/' $@ > $@.tmp && mv $@.tmp $@
	
diffs:
	@for f in ../0/*; do \
	  g=$$(echo $$f | sed 's%../0/%%'); \
	  if cmp --silent $$f $$g; then \
	    echo $$f and $$g are identical; \
	  else \
	    echo "diffing $$f and $$g ==> $$g.diff"; \
	    diff -u $$f $$g > $$g.diff; true; \
	  fi; \
	done
	
.PHONY: all diffs
