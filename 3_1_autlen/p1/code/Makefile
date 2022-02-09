CC = gcc -ansi -pedantic
CFLAGS = -Wall
EXE = s1_main
LIB=-l_afnd_64
LIBD=-L.

all : $(EXE)

.PHONY : clean
clean :
	rm -f *.o *.dot *.pdf core $(EXE)

$(EXE) : % : %.o transforma.o lib_afnd_64.a
	@echo "#---------------------------"
	@echo "# Generating $@ "
	@echo "# Depepends on $^"
	@echo "# Has changed $<"
	$(CC) $(CFLAGS) -o $@ $@.c transforma.o $(LIB) $(LIBD)

transforma.o: transforma.c transforma.h afnd.h
	$(CC) $(CFLAGS) -c transforma.c

test:
	@echo Running with valgrind 
	@valgrind --leak-check=full ./s1_main 1

dot:
	dot -Tpdf afnd_test.dot -o AFND.pdf
	dot -Tpdf determinista.dot -o AFD.pdf