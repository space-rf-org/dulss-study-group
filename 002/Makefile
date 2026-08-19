# Build Marp slides for Exploring TigerBeetle

MARP       ?= marp
SRC        := slides.md
THEME      := theme.css
HTML       := slides.html
INDEX      := index.html

MARP_FLAGS := --theme-set $(THEME) --allow-local-files

.PHONY: all build watch preview clean

all: build

build: $(HTML) $(INDEX)

$(HTML): $(SRC) $(THEME)
	$(MARP) $(SRC) $(MARP_FLAGS) -o $(HTML)

$(INDEX): $(SRC) $(THEME)
	$(MARP) $(SRC) $(MARP_FLAGS) -o $(INDEX)

watch:
	$(MARP) $(SRC) $(MARP_FLAGS) -o $(HTML) --watch

preview:
	$(MARP) $(SRC) $(MARP_FLAGS) -o $(HTML) --preview

clean:
	rm -f $(HTML) $(INDEX)
