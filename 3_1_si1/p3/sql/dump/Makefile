all: reset_db poblar actualizar registrar

reset_db:
	@echo Eliminando DB si1
	dropdb --if-exists -U alumnodb si1
	@echo Creando DB si1
	createdb -U alumnodb si1
	@echo Eliminando DB simongo
	dropdb --if-exists -U alumnodb simongo
	@echo Creando DB simongo
	createdb -U alumnodb simongo

poblar:
	@echo Poblando DB si1
	cat dump_v1.4.sql | psql -U alumnodb si1
	@echo Poblando DB simongo
	cat dump_v1.2-P3.sql | psql -U alumnodb simongo

actualizar:
	@echo Actualizando DB
	cat actualiza.sql | psql -U alumnodb si1	
	cat setPrice.sql | psql -U alumnodb si1
	cat setOrderAmount.sql | psql -U alumnodb si1
	@echo Ejecutando updates
	@echo "SELECT setOrderAmount()" | psql -U alumnodb si1	

registrar:
	@echo Registrando funciones y triggers
	cat getTopMonths.sql | psql -U alumnodb si1
	cat getTopVentas.sql | psql -U alumnodb si1
	cat updOrders.sql | psql -U alumnodb si1
	cat updInventory.sql | psql -U alumnodb si1
