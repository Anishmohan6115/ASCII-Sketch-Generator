CC=python3

all: ascii.py
	$(CC) ascii.py $(image)
	$(CC) ascii2.py

clean:
	$(RM) sketch.jpg
	$(RM) AsciiSketch.jpg