LIBS = 
LIB_DIR =  
FLAGS = -O3 -Wall -D_GNU_SOURCE

.PHONY: clean all

all: regular transposed

regular: regular.c arqo3.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

transposed: transposed.c arqo3.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

clean:
	rm -f *.o *~ regular transposed
