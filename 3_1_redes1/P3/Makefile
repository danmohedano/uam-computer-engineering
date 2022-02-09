all : test

dependencies:
	@echo "Instalando tshark"
	sudo apt-get install tshark
	@echo "Instalando matplotlib"
	sudo pip3 install matplotlib
	@echo "Instalando pandas"
	sudo pip3 install pandas

test:
	@echo "Probando Script con configuración:"
	@echo "Traza: 'traza.pcap'"
	@echo "Dirección MAC: 00:11:88:CC:33:DB"
	@echo "Dirección IP (TCP): 72.18.251.33"
	@echo "Puerto (UDP): 14442"
	python3 practica3.py --trace traza.pcap --mac 00:11:88:CC:33:DB --ip_flujo_tcp 72.18.251.33 --port_flujo_udp 14442