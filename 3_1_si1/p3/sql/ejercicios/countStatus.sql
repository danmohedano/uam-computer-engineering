-- Plan de ejecución sin índice
explain
select  count(*)
from    orders
where   status is null;

explain
select  count(*)
from    orders
where   status ='Shipped';

-- Plan de ejecución con índice
create index idx_status_orders on orders(status);
explain
select  count(*)
from    orders
where   status is null;

explain
select  count(*)
from    orders
where   status ='Shipped';

-- Generar estadísticas
analyze orders;

explain
select  count(*)
from    orders
where   status is null;

explain
select  count(*)
from    orders
where   status ='Shipped';



-- Otras dos consultas
explain
select  count(*)
from    orders
where   status ='Paid';

explain
select  count(*)
from    orders
where   status ='Processed';

drop index idx_status_orders;