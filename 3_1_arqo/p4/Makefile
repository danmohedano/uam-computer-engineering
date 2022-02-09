LIBS = -lm
LIB_DIR =  
FLAGS = -g -lgomp -Wall -D_GNU_SOURCE -fopenmp

.PHONY: clean all

all: exercise1 exercise2 exercise3 exercise4 exercise5

exercise1: exercise1/omp1 exercise1/omp2

exercise2: exercise2/pescalar_serie exercise2/pescalar_par1 exercise2/pescalar_par2 exercise2/pescalar_par3

exercise3: exercise3/multiplication_serie exercise3/multiplication_par1 exercise3/multiplication_par2 exercise3/multiplication_par3

exercise4: exercise4/pi_serie exercise4/pi_par1 exercise4/pi_par2 exercise4/pi_par3 exercise4/pi_par4 exercise4/pi_par5 exercise4/pi_par6 exercise4/pi_par7

exercise5: exercise5/edgeDetector

exercise1/omp1: exercise1/omp1.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

exercise1/omp2: exercise1/omp2.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

exercise2/pescalar_serie: exercise2/pescalar_serie.c code/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

exercise2/pescalar_par1: exercise2/pescalar_par1.c code/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

exercise2/pescalar_par2: exercise2/pescalar_par2.c code/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

exercise2/pescalar_par3: exercise2/pescalar_par3.c code/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)	

exercise3/multiplication_serie: exercise3/multiplication_serie.c code/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

exercise3/multiplication_par1: exercise3/multiplication_par1.c code/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

exercise3/multiplication_par2: exercise3/multiplication_par2.c code/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

exercise3/multiplication_par3: exercise3/multiplication_par3.c code/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

exercise4/pi_serie: exercise4/pi_serie.c	
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)	

exercise4/pi_par1: exercise4/pi_par1.c	
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)	

exercise4/pi_par2: exercise4/pi_par2.c	
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

exercise4/pi_par3: exercise4/pi_par3.c	
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)	

exercise4/pi_par4: exercise4/pi_par4.c	
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

exercise4/pi_par5: exercise4/pi_par5.c	
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)	

exercise4/pi_par6: exercise4/pi_par6.c	
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

exercise4/pi_par7: exercise4/pi_par7.c	
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)	

exercise5/edgeDetector: exercise5/edgeDetector.c exercise5/stb_image_write.h exercise5/stb_image.h
	gcc $(FLAGS) -std=gnu99 $(LIB_DIR) -o $@ exercise5/edgeDetector.c $(LIBS)

exercise5/stb_image.h:
	@echo "Los ficheros de cabecera de stb se deberían descarga automáticamente"
	@echo "En caso de fallo, descargadlo de https://raw.githubusercontent.com/nothings/stb/master/stb_image.h"
	wget --no-check-certificate https://raw.githubusercontent.com/nothings/stb/master/stb_image.h
	mv stb_image.h exercise5/

exercise5/stb_image_write.h:
	@echo "Los ficheros de cabecera de stb se deberían descarga automáticamente"
	@echo "En caso de fallo, descargadlo de https://raw.githubusercontent.com/nothings/stb/master/stb_image_write.h"
	wget --no-check-certificate https://raw.githubusercontent.com/nothings/stb/master/stb_image_write.h
	mv stb_image_write.h exercise5/

clean: clean_exercise1 clean_exercise2 clean_exercise3 clean_exercise4 clean_exercise5
	
clean_exercise1:
	rm -f exercise1/*.o exercise1/*~ exercise1/omp1 exercise1/omp2

clean_exercise2:
	rm -f exercise2/*.o exercise2/*~ exercise2/pescalar_serie exercise2/pescalar_par1 exercise2/pescalar_par2 exercise2/pescalar_par3

clean_exercise3:
	rm -f exercise3/*.o exercise3/*~ exercise3/multiplication_serie exercise3/multiplication_par1 exercise3/multiplication_par2 exercise3/multiplication_par3

clean_exercise4:
	rm -f exercise4/*.o exercise4/*~ exercise4/pi_serie exercise4/pi_par1 exercise4/pi_par2 exercise4/pi_par3 exercise4/pi_par4 exercise4/pi_par5 exercise4/pi_par6 exercise4/pi_par7

clean_exercise5:
	rm -f exercise5/*.o exercise5/*~ exercise5/edgeDetector
