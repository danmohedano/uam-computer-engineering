-- Cambiar atributos de customer a únicos
ALTER TABLE public.customers
ADD CONSTRAINT customers_email_unique UNIQUE (email);

-- Crear la columna de saldo para los customers
ALTER TABLE public.customers
ADD saldo numeric;

UPDATE public.customers
SET saldo = 100;

-- Añadir PK a imdb_actormovies y añadir FK's
ALTER TABLE public.imdb_actormovies
ADD CONSTRAINT imdb_actormovies_pkey PRIMARY KEY (actorid, movieid),
ADD CONSTRAINT imdb_actormovies_actorid_fkey FOREIGN KEY (actorid)
    REFERENCES public.imdb_actors (actorid) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE,
ADD CONSTRAINT imdb_actormovies_movieid_fkey FOREIGN KEY (movieid)
    REFERENCES public.imdb_movies (movieid) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE;

-- Añadir CASCADE a las FK's en imdb_directormovies
ALTER TABLE public.imdb_directormovies
DROP CONSTRAINT imdb_directormovies_directorid_fkey,
ADD CONSTRAINT imdb_directormovies_directorid_fkey FOREIGN KEY (directorid)
    REFERENCES public.imdb_directors (directorid) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE,
DROP CONSTRAINT imdb_directormovies_movieid_fkey,
ADD CONSTRAINT imdb_directormovies_movieid_fkey FOREIGN KEY (movieid)
    REFERENCES public.imdb_movies (movieid) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION;

-- Añadir CASCADE a la FK en imdb_moviecountries
ALTER TABLE public.imdb_moviecountries
DROP CONSTRAINT imdb_moviecountries_movieid_fkey,
ADD CONSTRAINT imdb_moviecountries_movieid_fkey FOREIGN KEY (movieid)
    REFERENCES public.imdb_movies (movieid) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE;

-- Añadir CASCADE a la FK en imdb_moviegenres
ALTER TABLE public.imdb_moviegenres
DROP CONSTRAINT imdb_moviegenres_movieid_fkey,
ADD CONSTRAINT imdb_moviegenres_movieid_fkey FOREIGN KEY (movieid)
    REFERENCES public.imdb_movies (movieid) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE;

-- Añadir CASCADE a la FK en imdb_movielanguages y quitar extra information de la PK
ALTER TABLE public.imdb_movielanguages
DROP CONSTRAINT imdb_movielanguages_pkey,
ADD CONSTRAINT imdb_movielanguages_pkey PRIMARY KEY (movieid, language),
DROP CONSTRAINT imdb_movielanguages_movieid_fkey,
ADD CONSTRAINT imdb_movielanguages_movieid_fkey FOREIGN KEY (movieid)
    REFERENCES public.imdb_movies (movieid) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE;

-- Añadir FK a inventory
ALTER TABLE public.inventory
ADD CONSTRAINT inventory_prod_id_fkey FOREIGN KEY (prod_id)
    REFERENCES public.products (prod_id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE;

-- Añadir PK a orderdetail y añadir FK's
ALTER TABLE public.orderdetail
ADD CONSTRAINT orderdetail_orderid_fkey FOREIGN KEY (orderid)
    REFERENCES public.orders (orderid) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE,
ADD CONSTRAINT orderdetail_prod_id_fkey FOREIGN KEY (prod_id)
    REFERENCES public.products (prod_id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE;

-- Añadir FK a orders
ALTER TABLE public.orders
ADD CONSTRAINT orders_customerid_fkey FOREIGN KEY (customerid)
    REFERENCES public.customers (customerid)
    ON UPDATE NO ACTION ON DELETE CASCADE;

-- Añadir FK a products
ALTER TABLE public.products
DROP CONSTRAINT products_movieid_fkey,
ADD CONSTRAINT products_movieid_fkey FOREIGN KEY (movieid)
    REFERENCES public.imdb_movies (movieid) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE;


-- Crea la tabla public.countries
CREATE TABLE public.countries(
    countryid SERIAL PRIMARY KEY,
    countryname character varying(32) NOT NULL
);

ALTER TABLE public.countries OWNER TO alumnodb;

INSERT INTO public.countries (countryname)
SELECT country
FROM imdb_moviecountries
GROUP BY country;

ALTER TABLE public.imdb_moviecountries
ADD countryid integer;

UPDATE public.imdb_moviecountries
SET countryid = countries.countryid
    FROM countries
    WHERE country = countryname;

ALTER TABLE public.imdb_moviecountries
DROP COLUMN country;

ALTER TABLE public.imdb_moviecountries
ADD CONSTRAINT imdb_moviecountries_countryid_fkey FOREIGN KEY (countryid)
    REFERENCES public.countries (countryid) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE;

-- Crea la tabla public.genres
CREATE TABLE public.genres(
    genreid SERIAL PRIMARY KEY,
    genrename character varying(32) NOT NULL
);

ALTER TABLE public.genres OWNER TO alumnodb;

INSERT INTO public.genres (genrename)
SELECT genre
FROM imdb_moviegenres
GROUP BY genre;

ALTER TABLE public.imdb_moviegenres
ADD genreid integer;

UPDATE public.imdb_moviegenres
SET genreid = genres.genreid
    FROM genres
    WHERE genre = genrename;

ALTER TABLE public.imdb_moviegenres
DROP COLUMN genre;

ALTER TABLE public.imdb_moviegenres
ADD CONSTRAINT imdb_moviegenres_genreid_fkey FOREIGN KEY (genreid)
    REFERENCES public.genres (genreid) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE;

-- Crea la tabla public.languages
CREATE TABLE public.languages(
    languageid SERIAL PRIMARY KEY,
    languagename character varying(32) NOT NULL
);

ALTER TABLE public.languages OWNER TO alumnodb;

INSERT INTO public.languages (languagename)
SELECT language
FROM imdb_movielanguages
GROUP BY language;

ALTER TABLE public.imdb_movielanguages
ADD languageid integer;

UPDATE public.imdb_movielanguages
SET languageid = languages.languageid
    FROM languages
    WHERE language = languagename;

ALTER TABLE public.imdb_movielanguages
DROP COLUMN language;

ALTER TABLE public.imdb_movielanguages
ADD CONSTRAINT imdb_movielanguages_languageid_fkey FOREIGN KEY (languageid)
    REFERENCES public.languages (languageid) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE;

--Crea la tabla alertas
CREATE TABLE public.alertas(
    prod_id integer
);

ALTER TABLE public.alertas OWNER TO alumnodb;

ALTER TABLE public.alertas
ADD CONSTRAINT alertas_prod_id_fkey FOREIGN KEY (prod_id)
    REFERENCES public.products (prod_id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE;