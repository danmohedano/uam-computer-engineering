INC=./includes
SRC=./src
OBJ=./obj
LIB=./lib
SRCLIB=./srclib
EXE=server

CC = gcc
CFLAGS = -Wall -g
LIBS = -L /usr/local/bin -lpthread -lconfuse

.PHONY: clean_obj clean_lib clean_exe clean

all: clean setup server

setup:
	mkdir -p htmlfiles lib obj 

#~~~~~~~~~~~~~ Ejecutable ~~~~~~~~~~~~~#

$(EXE): $(OBJ)/server.o $(LIB)/libsocket.a $(OBJ)/thread_pool.o $(LIB)/libhttp.a
	@echo "Building executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

server_test: $(OBJ)/server_test.o $(LIB)/libsocket.a $(LIB)/libhttp.a
	@echo "Building executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

#~~~~~~~~~~~~~ lib ~~~~~~~~~~~~~#
$(LIB)/socket.o: $(SRCLIB)/socket.c $(INC)/socket.h
	@echo "Compiling socket module..."
	$(CC) $(CFLAGS) -c $< -o $@

$(LIB)/libsocket.a: $(LIB)/socket.o
	@echo "Creating static socket library libsocket..."
	ar rc $@ $^

$(LIB)/http.o: $(SRCLIB)/http.c $(INC)/http.h
	@echo "Compiling http module..."
	$(CC) $(CFLAGS) -c $< -o $@

$(LIB)/picohttpparser.o: $(SRCLIB)/picohttpparser.c $(INC)/picohttpparser.h
	@echo "Compiling picohttpparser module..."
	$(CC) $(CFLAGS) -c $< -o $@

$(LIB)/libhttp.a: $(LIB)/http.o $(LIB)/picohttpparser.o
	@echo "Creating static http library libhttp..."
	ar rc $@ $^

#~~~~~~~~~~~~~ obj ~~~~~~~~~~~~~#
$(OBJ)/thread_pool.o: $(SRC)/thread_pool.c $(INC)/thread_pool.h
	@echo "Compiling thread_pool module..."
	$(CC) $(CFLAGS) -c $< -o $@

$(OBJ)/server.o: $(SRC)/server.c $(INC)/socket.h $(INC)/thread_pool.h
	@echo "Compiling server module..."
	$(CC) $(CFLAGS) -c $< -o $@

$(OBJ)/server_test.o: $(SRC)/server_test.c $(INC)/socket.h $(INC)/http.h
	@echo "Compiling server module..."
	$(CC) $(CFLAGS) -c $< -o $@

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
	rm -f $(EXE) server_test

#~~~~~~~~~~~~~ test ~~~~~~~~~~~~~#
test:
	@echo "Testing $(EXE)..."
	./$(EXE)

test_valgrind:
	@echo "Testing with valgrind $(EXE)..."
	valgrind --leak-check=full ./$(EXE)

logs:
	@echo "Reading logs..."
	cat /var/log/syslog | grep -F 'SERVER-LOG' | tail -n 20