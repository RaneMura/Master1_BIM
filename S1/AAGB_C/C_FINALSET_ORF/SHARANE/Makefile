CC = gcc
CFLAGS = -Wall
LDFLAGS =
EXEC=main

all: $(EXEC)

main : ManipSeqSimple.o ManipSeqADN.o Arbre.o main.o
	$(CC) -o $@ $^ $(LDFLAGS)

ManipSeqSimple.o : ManipSeqSimple.c
	$(CC) -o $@ -c $< $(CFLAGS)

ManipSeqADN.o : ManipSeqADN.c ManipSeqSimple.h
	$(CC) -o $@ -c $< $(CFLAGS)

Arbre.o : Arbre.c ManipSeqSimple.h ManipSeqADN.h
	$(CC) -o $@ -c $< $(CFLAGS)

main.o : main.c ManipSeqSimple.h ManipSeqADN.h Arbre.h
	$(CC) -o $@ -c $< $(CFLAGS)

clean:
	rm -rf *.o

rmproper: clean
	rm -rf $(EXEC)