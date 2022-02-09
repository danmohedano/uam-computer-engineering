all: symbol_table_test

symbol_table_test: main.o symbol_table.o hash_table.o hash_data.o
	gcc -o symbol_table_test main.o symbol_table.o hash_table.o hash_data.o

main.o: main.c
	gcc -c main.c

symbol_table.o: symbol_table.c
	gcc -c symbol_table.c

hash_table.o: hash_table.c
	gcc -c hash_table.c

hash_data.o: hash_data.c
	gcc -c hash_data.c

clean:
	rm -rf *.o symbol_table_test