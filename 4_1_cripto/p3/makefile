INC=./includes
SRC=./src
OBJ=./obj
LIB=./lib
SRCLIB=./srclib

CC = gcc
CFLAGS = -Wall -g
LIBS = -lgmp -lm

.PHONY: clean_obj clean_lib clean_exe clean

all: clean setup potencia.exe primo.exe vegas.exe

setup:
	mkdir -p lib obj 

#~~~~~~~~~~~~~ Ejecutable ~~~~~~~~~~~~~#
potencia.exe: $(OBJ)/potencia.o $(LIB)/utils.o
	@echo "Building potencia executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

primo.exe: $(OBJ)/primo.o $(LIB)/utils.o
	@echo "Building primo executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

vegas.exe: $(OBJ)/vegas.o $(LIB)/utils.o
	@echo "Building vegas executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

#~~~~~~~~~~~~~ lib ~~~~~~~~~~~~~#
$(LIB)/utils.o: $(SRCLIB)/utils.c $(INC)/utils.h $(INC)/constants.h
	@echo "Compiling utils module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

#~~~~~~~~~~~~~ obj ~~~~~~~~~~~~~#
$(OBJ)/potencia.o: $(SRC)/potencia.c $(INC)/utils.h
	@echo "Compiling potencia module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/primo.o: $(SRC)/primo.c $(INC)/utils.h
	@echo "Compiling potencia module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/vegas.o: $(SRC)/vegas.c $(INC)/utils.h
	@echo "Compiling vegas module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

#~~~~~~~~~~~~~ cleanup ~~~~~~~~~~~~~#
clean: clean_obj clean_lib clean_exe clean_test

clean_obj:
	@echo "Cleaning $(OBJ)/..."
	rm -f $(OBJ)/*.o

clean_lib:
	@echo "Cleaning $(LIB)/..."
	rm -f $(LIB)/*.a $(LIB)/*.o

clean_exe:
	@echo "Cleaning exe..."
	rm -f *.exe

clean_test:
	@echo "Cleaning test results..."
	rm -f test/openssl/*_tr* *.csv test/potencia/*.png

#~~~~~~~~~~~~~ test ~~~~~~~~~~~~~#
test_aes:
	openssl enc -aes-128-ecb -base64 -e -k password -p -v -in test/openssl/message.txt -out test/openssl/aes_c_tr.txt
	openssl enc -aes-128-ecb -base64 -d -k password -p -v -in test/openssl/aes_c_tr.txt -out test/openssl/aes_d_tr.txt
	diff -s test/openssl/message.txt test/openssl/aes_d_tr.txt

test_camellia:
	openssl enc -camellia-128-ecb -base64 -e -k password -p -v -in test/openssl/message.txt -out test/openssl/camellia_c_tr.txt
	openssl enc -camellia-128-ecb -base64 -d -k password -p -v -in test/openssl/camellia_c_tr.txt -out test/openssl/camellia_d_tr.txt
	diff -s test/openssl/message.txt test/openssl/camellia_d_tr.txt

test_chacha:
	openssl enc -chacha20 -base64 -e -k password -p -v -in test/openssl/message.txt -out test/openssl/chacha_c_tr.txt
	openssl enc -chacha20 -base64 -d -k password -p -v -in test/openssl/chacha_c_tr.txt -out test/openssl/chacha_d_tr.txt
	diff -s test/openssl/message.txt test/openssl/chacha_d_tr.txt

test_rc4:
	openssl enc -rc4 -base64 -e -k password -p -v -in test/openssl/message.txt -out test/openssl/rc4_c_tr.txt
	openssl enc -rc4 -base64 -d -k password -p -v -in test/openssl/rc4_c_tr.txt -out test/openssl/rc4_d_tr.txt
	diff -s test/openssl/message.txt test/openssl/rc4_d_tr.txt

test_des_debil:
	openssl enc -des-ecb -e -K 1F1F1F1F0E0E0E0E -nopad -p -v -in test/openssl/message.txt -out test/openssl/des_weak_c_tr.txt
	openssl enc -des-ecb -e -K 1F1F1F1F0E0E0E0E -nopad -p -v -in test/openssl/des_weak_c_tr.txt -out test/openssl/des_weak_d_tr.txt
	diff -s test/openssl/message.txt test/openssl/des_weak_d_tr.txt

test_des_semidebil:
	openssl enc -des-ecb -e -K 1F011F010E010E01 -nopad -p -v -in test/openssl/message.txt -out test/openssl/des_semiweak_c_tr.txt
	openssl enc -des-ecb -e -K 011F011F010E010E -nopad -p -v -in test/openssl/des_semiweak_c_tr.txt -out test/openssl/des_semiweak_d_tr.txt
	diff -s test/openssl/message.txt test/openssl/des_semiweak_d_tr.txt

test_rsa:
	openssl rsautl -encrypt -inkey test/openssl/public-key.pem -pubin -in test/openssl/small_message.txt -out test/openssl/rsa_c_tr.txt
	openssl rsautl -decrypt -inkey test/openssl/private-key.pem -in test/openssl/rsa_c_tr.txt -out test/openssl/rsa_d_tr.txt
	diff -s test/openssl/small_message.txt test/openssl/rsa_d_tr.txt

test_key_rsa:
	openssl genrsa -out test/openssl/private-key.pem 4098
	openssl rsa -in test/openssl/private-key.pem -pubout -out test/openssl/public-key.pem
	cat test/openssl/private-key.pem
	cat test/openssl/public-key.pem
	@echo "\n"

test_cert:
	openssl req -x509 -newkey rsa:1024 -keyout test/openssl/cert-key.pem -out test/openssl/cert.pem -sha256 -days 365 -nodes -subj "/C=ES/ST=Comunidad de Madrid/L=Madrid/O=Pareja11/OU=P11/CN=DanielySilvia/emailAddress=pareja11@uam.es"
	openssl x509 -in test/openssl/cert.pem -text -noout

test_potencia_tiempos:
	./test/potencia/script.sh
	./test/potencia/plot.sh

test_primo:
	./primo.exe -b 1024 -p 0.0108
	./primo.exe -b 512 -p 9e-17
	./primo.exe -b 8192 -p 1e-10

test_primo_2:
	./primo.exe -b 8192 -p 0.01
	./primo.exe -b 8192 -p 0.0001
	./primo.exe -b 8192 -p 0.000001

test_vegas:
	./vegas.exe -b 8192 -p 1e-10