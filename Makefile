# makefile for live sass compile without vscode
SASS = sass
SRC = scss
DEST = css/
FLAGS = --style=expanded

all: compile

compile:
	$(SASS) $(FLAGS) $(SRC):$(DEST)

watch:
	$(SASS) --watch $(SRC):$(DEST) $(FLAGS)

clean:
	rm -rf $(DEST)*.css

.PHONY: all compile watch clean
