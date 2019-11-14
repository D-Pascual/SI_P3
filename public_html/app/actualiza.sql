--Actualizar ON UPDATE y ON DELETE a CASCADE de los atributos multievaluados 
ALTER TABLE public.imdb_moviegenres
    DROP CONSTRAINT imdb_moviegenres_movieid_fkey,
    ADD CONSTRAINT imdb_moviegenres_movieid_fkey FOREIGN KEY (movieid) 
        REFERENCES public.imdb_movies (movieid) 
        ON UPDATE CASCADE ON DELETE CASCADE; --revisar cascade

ALTER TABLE public.imdb_movielanguages
    DROP CONSTRAINT imdb_movielanguages_movieid_fkey,
    ADD CONSTRAINT imdb_movielanguages_movieid_fkey FOREIGN KEY (movieid) 
        REFERENCES public.imdb_movies (movieid) 
        ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.imdb_moviecountries
    DROP CONSTRAINT imdb_moviecountries_movieid_fkey,
    ADD CONSTRAINT imdb_moviecountries_movieid_fkey FOREIGN KEY (movieid) 
        REFERENCES public.imdb_movies (movieid) 
        ON UPDATE CASCADE ON DELETE CASCADE;

--Añadir primary y foreign key a actormovies 
ALTER TABLE public.imdb_actormovies
    ADD CONSTRAINT imdb_actormovies_pkey PRIMARY KEY (actorid, movieid, "character"),
    ADD CONSTRAINT imdb_actormovies_actorid_fkey FOREIGN KEY (actorid) 
        REFERENCES public.imdb_actors (actorid) MATCH SIMPLE --revisar match
        ON UPDATE CASCADE ON DELETE SET NULL, --revisar cascade set null
    ADD CONSTRAINT imdb_actormovies_movieid_fkey FOREIGN KEY (movieid) 
        REFERENCES public.imdb_movies (movieid) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE SET NULL;

--Actualizar ON UPDATE y ON DELETE de FKeys de actormovies
ALTER TABLE public.imdb_directormovies
    DROP CONSTRAINT imdb_directormovies_movieid_fkey,
    ADD CONSTRAINT imdb_directormovies_movieid_fkey FOREIGN KEY (movieid) 
        REFERENCES public.imdb_movies (movieid) MATCH SIMPLE --revisar match
        ON UPDATE CASCADE ON DELETE SET NULL, --revisar cascade set null
    DROP CONSTRAINT imdb_directormovies_directorid_fkey,
    ADD CONSTRAINT imdb_directormovies_directorid_fkey FOREIGN KEY (directorid) 
        REFERENCES public.imdb_directors (directorid) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE SET NULL;

--Añadir foreign key a inventory
ALTER TABLE public.inventory
    ADD CONSTRAINT inventory_prod_id_fkey FOREIGN KEY (prod_id) 
        REFERENCES public.products (prod_id) MATCH SIMPLE --revisar match
        ON UPDATE CASCADE ON DELETE SET NULL; --revisar cascade set null