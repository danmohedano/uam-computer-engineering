CC = gcc

TESTS := ej1 ej2 ej3 ej4 ej5 ej6 ej7

all: generacion.o
	@echo '******************** Compiling test files ********************'
	$(foreach tst, $(TESTS), \
		$(CC) -c $(tst).c; \
	)
	@echo
	@echo '************ Linking test files with generacion.o ************'
	$(foreach tst, $(TESTS), \
		$(CC) -o $(tst) $(tst).o generacion.o; \
	)
	@echo
	@echo '******************** Generating asm files ********************'
	$(foreach tst, $(TESTS), \
		./$(tst) $(tst).asm; \
	)
	@echo
	@echo '******************** Compiling .asm files ********************'
	$(foreach tst, $(TESTS), \
		nasm -g -o $(tst).o -f elf32 $(tst).asm; \
	)
	@echo
	@echo '************** Linking asm files with alfalib.o **************'
	$(foreach tst, $(TESTS), \
		gcc -Wall -g -m32 -o $(tst) $(tst).o alfalib.o; \
	)

generacion.o: generacion.c generacion.h
	$(CC) -c generacion.c

clean:
	rm -rf ej*.o generacion.o *.asm $(TESTS)
