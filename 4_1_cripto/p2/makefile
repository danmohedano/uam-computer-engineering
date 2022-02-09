INC=./includes
SRC=./src
OBJ=./obj
LIB=./lib
SRCLIB=./srclib

CC = gcc
CFLAGS = -Wall -g
LIBS = -lgmp -lm

.PHONY: clean_obj clean_lib clean_exe clean

all: clean setup seg_perf.exe desCFB.exe desECB.exe tdesCFB.exe generator.exe des_linealidad.exe des_avalancha.exe aes_linealidad.exe sbox_aes.exe

setup:
	mkdir -p lib obj 

#~~~~~~~~~~~~~ Ejecutable ~~~~~~~~~~~~~#
seg_perf.exe: $(OBJ)/seg_perf.o $(LIB)/utils.o $(LIB)/cypher.o $(LIB)/io.o
	@echo "Building seg_perf executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

desCFB.exe: $(OBJ)/desCFB.o $(LIB)/des.o
	@echo "Building desCFB executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

desECB.exe: $(OBJ)/desECB.o $(LIB)/des.o
	@echo "Building desECB executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

tdesCFB.exe: $(OBJ)/tdesCFB.o $(LIB)/des.o
	@echo "Building tdesCFB executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

generator.exe: $(OBJ)/generator.o
	@echo "Building generator executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

des_linealidad.exe: $(OBJ)/des_linealidad.o
	@echo "Building des_linealidad executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

des_avalancha.exe: $(OBJ)/des_avalancha.o $(LIB)/des.o
	@echo "Building des_avalancha executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

aes_linealidad.exe: $(OBJ)/aes_linealidad.o
	@echo "Building aes_linealidad executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

sbox_aes.exe: $(OBJ)/sbox_aes.o
	@echo "Building sbox_aes executable..."
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

#~~~~~~~~~~~~~ lib ~~~~~~~~~~~~~#
$(LIB)/utils.o: $(SRCLIB)/utils.c $(INC)/utils.h $(INC)/constants.h
	@echo "Compiling utils module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(LIB)/cypher.o: $(SRCLIB)/cypher.c $(INC)/cypher.h $(INC)/constants.h
	@echo "Compiling cypher module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(LIB)/io.o: $(SRCLIB)/io.c $(INC)/io.h $(INC)/constants.h
	@echo "Compiling io module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(LIB)/des.o: $(SRCLIB)/des.c $(INC)/des.h $(INC)/constants.h
	@echo "Compiling DES module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

#~~~~~~~~~~~~~ obj ~~~~~~~~~~~~~#
$(OBJ)/seg_perf.o: $(SRC)/seg_perf.c $(INC)/constants.h
	@echo "Compiling seg_perf module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/desCFB.o: $(SRC)/desCFB.c $(INC)/des.h $(INC)/constants.h
	@echo "Compiling desCFB module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/desECB.o: $(SRC)/desECB.c $(INC)/des.h $(INC)/constants.h
	@echo "Compiling desECB module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/tdesCFB.o: $(SRC)/tdesCFB.c $(INC)/des.h $(INC)/constants.h
	@echo "Compiling tdesCFB module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/generator.o: $(SRC)/generator.c $(INC)/constants.h
	@echo "Compiling generator module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/des_linealidad.o: $(SRC)/des_linealidad.c $(INC)/constants.h
	@echo "Compiling des_linealidad module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/des_avalancha.o: $(SRC)/des_avalancha.c $(INC)/des.h $(INC)/constants.h
	@echo "Compiling des_avalancha module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/aes_linealidad.o: $(SRC)/aes_linealidad.c $(INC)/constants.h
	@echo "Compiling aes_linealidad module..."
	$(CC) $(CFLAGS) -c $< -o $@ $(LIBS)

$(OBJ)/sbox_aes.o: $(SRC)/sbox_aes.c $(INC)/constants.h
	@echo "Compiling sbox_aes module..."
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
	rm -f test/seg_perf/*_tr* test/des/*_tr* test/aes/*_tr* *.csv

#~~~~~~~~~~~~~ test ~~~~~~~~~~~~~#
test_seg_perf_long:
	./seg_perf.exe -P -i test/seg_perf/perf_long.txt -o test/seg_perf/perf_long_p_tr.txt
	./seg_perf.exe -I -i test/seg_perf/perf_long.txt -o test/seg_perf/perf_long_i_tr.txt

test_seg_perf_short:
	./seg_perf.exe -P -i test/seg_perf/perf_short.txt -o test/seg_perf/perf_short_p_tr.txt
	./seg_perf.exe -I -i test/seg_perf/perf_short.txt -o test/seg_perf/perf_short_i_tr.txt

test_des_ecb:
	./desECB.exe -C -k 0x58e0136b6e923da8 -i test/des/des_input.txt -o test/des/des_ecb_c_tr.txt
	./desECB.exe -D -k 0x58e0136b6e923da8 -i test/des/des_ecb_c_tr.txt -o test/des/des_ecb_d_tr.txt
	@echo "Original:"
	cat test/des/des_input.txt
	@echo "\n----------------------------------------------------"
	@echo "Descifrado:"
	cat test/des/des_ecb_d_tr.txt
	@echo "\n"

test_des_cfb:
	./desCFB.exe -C -k 0x58e0136b6e923da8 -v 0x6693b81c7b2975ea -i test/des/des_input.txt -o test/des/des_cfb_c_tr.txt
	./desCFB.exe -D -k 0x58e0136b6e923da8 -v 0x6693b81c7b2975ea -i test/des/des_cfb_c_tr.txt -o test/des/des_cfb_d_tr.txt
	@echo "Original:"
	cat test/des/des_input.txt
	@echo "\n----------------------------------------------------"
	@echo "Descifrado:"
	cat test/des/des_cfb_d_tr.txt
	@echo "\n"

test_des_cfb_s:
	./desCFB.exe -C -k 0x58e0136b6e923da8 -s 24 -v 0x6693b81c7b2975ea -i test/des/des_input.txt -o test/des/des_cfbs_c_tr.txt
	./desCFB.exe -D -k 0x58e0136b6e923da8 -s 24 -v 0x6693b81c7b2975ea -i test/des/des_cfbs_c_tr.txt -o test/des/des_cfbs_d_tr.txt
	@echo "Original:"
	cat test/des/des_input.txt
	@echo "\n----------------------------------------------------"
	@echo "Descifrado:"
	cat test/des/des_cfbs_d_tr.txt
	@echo "\n"

test_des_cfb_pdf:
	./desCFB.exe -C -k 0x58e0136b6e923da8 -v 0x6693b81c7b2975ea -i test/des/des_input.pdf -o test/des/des_cfb_c_tr.pdf
	./desCFB.exe -D -k 0x58e0136b6e923da8 -v 0x6693b81c7b2975ea -i test/des/des_cfb_c_tr.pdf -o test/des/des_cfb_d_tr.pdf

test_tdes_cfb:
	./tdesCFB.exe -C -k 0x2adf85752c8ae6520bba156d6752808554bcdcb56e8098e3 -v 0x6693b81c7b2975ea -i test/des/des_input.txt -o test/des/tdes_cfb_c_tr.txt
	./tdesCFB.exe -D -k 0x2adf85752c8ae6520bba156d6752808554bcdcb56e8098e3 -v 0x6693b81c7b2975ea -i test/des/tdes_cfb_c_tr.txt -o test/des/tdes_cfb_d_tr.txt
	@echo "Original:"
	cat test/des/des_input.txt
	@echo "\n----------------------------------------------------"
	@echo "Descifrado:"
	cat test/des/tdes_cfb_d_tr.txt
	@echo "\n"

test_tdes_cfb_pdf:
	./tdesCFB.exe -C -k 0x2adf85752c8ae6520bba156d6752808554bcdcb56e8098e3 -v 0x6693b81c7b2975ea -i test/des/des_input.pdf -o test/des/tdes_cfb_c_tr.pdf
	./tdesCFB.exe -D -k 0x2adf85752c8ae6520bba156d6752808554bcdcb56e8098e3 -v 0x6693b81c7b2975ea -i test/des/tdes_cfb_c_tr.pdf -o test/des/tdes_cfb_d_tr.pdf

test_des_patrones:
	./desECB.exe -C -k 0x0bba156d67528085 -i test/des/des_patrones.txt -o test/des/des_ecb_c_patrones_tr.txt
	./desECB.exe -D -k 0x0bba156d67528085 -i test/des/des_ecb_c_patrones_tr.txt -o test/des/des_ecb_d_patrones_tr.txt
	./desCFB.exe -C -k 0x0bba156d67528085 -v 0x6693b81c7b2975ea -i test/des/des_patrones.txt -o test/des/des_cfb_c_patrones_tr.txt
	./desCFB.exe -D -k 0x0bba156d67528085 -v 0x6693b81c7b2975ea -i test/des/des_cfb_c_patrones_tr.txt -o test/des/des_cfb_d_patrones_tr.txt
	@echo "\nOriginal:"
	cat test/des/des_patrones.txt
	@echo "\n----------------------------------------------------"
	@echo "Descifrado CFB:"
	cat test/des/des_cfb_d_patrones_tr.txt
	@echo "\n----------------------------------------------------"
	@echo "Descifrado ECB:"
	cat test/des/des_ecb_d_patrones_tr.txt
	@echo "\n----------------------------------------------------"
	@echo "Cifrado CFB:"
	hexdump test/des/des_cfb_c_patrones_tr.txt
	@echo "\n----------------------------------------------------"
	@echo "Cifrado ECB:"
	hexdump test/des/des_ecb_c_patrones_tr.txt
	@echo "\n"

test_sbox_aes:
	./sbox_aes.exe -C
	./sbox_aes.exe -D