python=python3

ayuda_mp:
	@$(python) src/main.py mp -h

compila_mp:
	@echo "Nada que realizar"

ejecuta_mp:
	@$(python) src/main.py mp "data/2in.txt" "data/2out.txt"
	@echo "Archivo generado:"
	@cat data/2out.txt

compilar:
	@echo "Nada que realizar"

ayuda_perceptron:
	@$(python) src/main.py perceptron -h

ejecuta_perceptron:
	@$(python) src/main.py perceptron 1 "data/problema_real1.txt" 0.1 200 0.1 -portion 0.25

ayuda_adaline:
	@$(python) src/main.py adaline -h

ejecuta_adaline:
	@$(python) src/main.py adaline 1 "data/problema_real1.txt" 0.001 200 0.0001 -portion 0.25