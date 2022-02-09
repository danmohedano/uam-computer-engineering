all: pruebaSintactico

pruebaSintactico: alfa.y alfa.l
	bison -d alfa.y
	flex alfa.l
	gcc -Wall -o pruebaSintactico alfa.tab.c lex.yy.c -lfl

clean:
	rm -rf lex.yy.c pruebaSintactico myoutput*.txt alfa.tab.c alfa.tab.h

test: pruebaSintactico
	@echo 'Comparing salida1.txt and the output of our program: '
	./pruebaSintactico entrada_sin_1.txt myoutput1.txt
	diff -Bb salida_sin_1.txt myoutput1.txt
	@echo
	@echo 'Comparing salida2.txt and the output of our program: '
	./pruebaSintactico entrada_sin_2.txt myoutput2.txt
	diff -Bb salida_sin_2.txt myoutput2.txt
	@echo
	@echo 'Comparing salida3.txt and the output of our program: '
	./pruebaSintactico entrada_sin_3.txt myoutput3.txt
	diff -Bb salida_sin_3.txt myoutput3.txt
