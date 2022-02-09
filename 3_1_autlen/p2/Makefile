CC = gcc -ansi -pedantic
CFLAGS = -Wall
EXE = main
LIB=-l_afnd_64
LIBD=-L.

all : $(EXE)

.PHONY : clean
clean :
	rm -f *.o *.dot *.pdf core $(EXE)

$(EXE) : % : %.o minimiza.o lib_afnd_64.a
	@echo "#---------------------------"
	@echo "# Generating $@ "
	@echo "# Depepends on $^"
	@echo "# Has changed $<"
	$(CC) $(CFLAGS) -o $@ $@.c minimiza.o $(LIB) $(LIBD)

minimiza.o: minimiza.c minimiza.h afnd.h
	$(CC) $(CFLAGS) -c minimiza.c

test:
	@echo Running with valgrind 
	@valgrind --leak-check=full ./main 2 

dot:
	dot -Tpdf afnd_test.dot -o AFD.pdf
	dot -Tpdf min.dot -o Minimiza.pdf