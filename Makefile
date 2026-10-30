CC     = gcc
CFLAGS = -O2 -Wall -Wextra -std=c99
LDLIBS = -lm

FONTES = src/main.c src/comum.c src/problema1.c src/problema2.c src/problema3.c

all: experimentos

experimentos: $(FONTES) src/comum.h
	$(CC) $(CFLAGS) -o experimentos $(FONTES) $(LDLIBS)

clean:
	rm -f experimentos experimentos.exe

.PHONY: all clean
