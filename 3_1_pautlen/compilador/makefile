all: alfa

alfa: alfa.y alfa.l alfa.h generacion.o symbol_table.o hash_table.o hash_data.o
	bison -d alfa.y
	flex alfa.l
	gcc -c alfa.c
	gcc -Wall -o alfa alfa.o alfa.tab.c lex.yy.c generacion.o symbol_table.o hash_table.o hash_data.o -lfl

generacion.o: generacion.c generacion.h
	gcc -c generacion.c

symbol_table.o: symbol_table.c symbol_table.h
	gcc -c symbol_table.c

hash_table.o: hash_table.c hash_table.h
	gcc -c hash_table.c

hash_data.o: hash_data.c hash_data.h
	gcc -c hash_data.c


clean:
	rm -rf lex.yy.c alfa alfa.tab.c alfa.tab.h alfa.o generacion.o hash_data.o hash_table.o symbol_table.o
