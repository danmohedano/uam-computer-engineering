all: reset_db poblar actualizar registrar

reset_db:
	@echo Eliminando DB 
	dropdb --if-exists -U alumnodb si1
	@echo Creando DB
	createdb -U alumnodb si1

poblar:
	@echo Poblando DB
	cat dump_v1.4.sql | psql -U alumnodb si1

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
