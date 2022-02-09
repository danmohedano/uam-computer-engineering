all: pruebaMorfo

pruebaMorfo: lex.yy.c
	gcc -Wall -o pruebaMorfo lex.yy.c

lex.yy.c: alfa.l tokens.h
	lex alfa.l

clean:
	rm -rf lex.yy.c pruebaMorfo myoutput*.txt

test: pruebaMorfo
	@echo 'Comparing salida1.txt and the output of our program: '
	./pruebaMorfo entrada1.txt myoutput1.txt
	diff -Bb salida1.txt myoutput1.txt
	@echo
	@echo 'Comparing salida2.txt and the output of our program: '
	./pruebaMorfo entrada2.txt myoutput2.txt
	diff -Bb salida2.txt myoutput2.txt
	@echo
	@echo 'Comparing salida3.txt and the output of our program: '
	./pruebaMorfo entrada3.txt myoutput3.txt
	diff -Bb salida3.txt myoutput3.txt
