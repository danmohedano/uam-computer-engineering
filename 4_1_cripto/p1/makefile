INC=./includes
SRC=./src
OBJ=./obj
LIB=./lib
SRCLIB=./srclib

CC = gcc
CFLAGS = -Wall -g
LIBS = -lgmp

.PHONY: clean_obj clean_lib clean_exe clean

all: clean setup afin.exe afin_mejorado.exe hill.exe vigenere.exe kasiski.exe ic.exe permutacion.exe flujo.exe 

setup:
	mkdir -p lib obj 

#~~~~~~~~~~~~~ Ejecutable ~~~~~~~~~~~~~#

afin.exe: $(OBJ)/afin.o $(LIB)/utils.o $(LIB)/cypher.o $(LIB)/io.o
	@echo "Building afin executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

afin_mejorado.exe: $(OBJ)/afin_mejorado.o $(LIB)/utils.o $(LIB)/cypher.o $(LIB)/io.o
	@echo "Building afin_mejorado executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

hill.exe: $(OBJ)/hill.o $(LIB)/utils.o $(LIB)/cypher.o $(LIB)/io.o
	@echo "Building hill executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

vigenere.exe: $(OBJ)/vigenere.o $(LIB)/utils.o $(LIB)/cypher.o $(LIB)/io.o
	@echo "Building vigenere executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

kasiski.exe: $(OBJ)/kasiski.o $(LIB)/utils.o $(LIB)/io.o
	@echo "Building kasiski executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

ic.exe: $(OBJ)/ic.o $(LIB)/utils.o $(LIB)/io.o
	@echo "Building ic executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

permutacion.exe: $(OBJ)/permutacion.o $(LIB)/utils.o $(LIB)/cypher.o $(LIB)/io.o
	@echo "Building permutacion executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

flujo.exe: $(OBJ)/flujo.o $(LIB)/utils.o $(LIB)/cypher.o $(LIB)/io.o
	@echo "Building flujo executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

#~~~~~~~~~~~~~ lib ~~~~~~~~~~~~~#
$(LIB)/utils.o: $(SRCLIB)/utils.c $(INC)/utils.h
	@echo "Compiling utils module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(LIB)/cypher.o: $(SRCLIB)/cypher.c $(INC)/cypher.h
	@echo "Compiling cypher module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(LIB)/io.o: $(SRCLIB)/io.c $(INC)/io.h
	@echo "Compiling io module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

#~~~~~~~~~~~~~ obj ~~~~~~~~~~~~~#
$(OBJ)/afin.o: $(SRC)/afin.c
	@echo "Compiling afin module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/afin_mejorado.o: $(SRC)/afin_mejorado.c
	@echo "Compiling afin_mejorado module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/hill.o: $(SRC)/hill.c
	@echo "Compiling hill module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/vigenere.o: $(SRC)/vigenere.c
	@echo "Compiling vigenere module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/kasiski.o: $(SRC)/kasiski.c
	@echo "Compiling kasiski module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/ic.o: $(SRC)/ic.c
	@echo "Compiling ic module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/permutacion.o: $(SRC)/permutacion.c
	@echo "Compiling permutacion module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/flujo.o: $(SRC)/flujo.c
	@echo "Compiling flujo module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

#~~~~~~~~~~~~~ cleanup ~~~~~~~~~~~~~#
clean: clean_obj clean_lib clean_exe

clean_obj:
	@echo "Cleaning $(OBJ)/..."
	rm -f $(OBJ)/*.o

clean_lib:
	@echo "Cleaning $(LIB)/..."
	rm -f $(LIB)/*.a $(LIB)/*.o

clean_exe:
	@echo "Cleaning exe..."
	rm -f *.exe

#~~~~~~~~~~~~~ test ~~~~~~~~~~~~~#
test:
	@echo "Testing $(EXE)..."
	./$(EXE)

test_valgrind:
	@echo "Testing with valgrind $(EXE)..."
	valgrind --leak-check=full ./$(EXE)