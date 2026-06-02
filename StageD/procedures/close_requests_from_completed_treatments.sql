-- Cette procedure va parcourir ts les traitemnts et verifier si yn traitment est termine
-- avec completion time et ensuiet va actualiser la table a_request

-- on utilise : LOOP , FETCH ,DML, EXEPTION, CURSOR EXPLICIT
CREATE OR REPLACE PROCEDURE close_requests_from_completed_treatments()
LANGUAGE plpgsql
AS $$
DECLARE
    treatment_cursor REFCURSOR;
    treatment_record RECORD;
BEGIN
    -- Call the function and get the cursor it returns
    treatment_cursor := get_completed_treatments_not_closed();

    LOOP
        FETCH treatment_cursor INTO treatment_record;
        EXIT WHEN NOT FOUND;

        UPDATE public.a_request
        SET status_id = 3
        WHERE request_id = treatment_record.request_id;

        RAISE NOTICE
            'Request % was closed because treatment % is completed.',
            treatment_record.request_id,
            treatment_record.treatment_id;
    END LOOP;

    CLOSE treatment_cursor;   -- explicit cursor so i have to clone it !

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error while closing requests from completed treatments: %', SQLERRM;
END;
$$;



-- LES CURSOR  A SAVOIR


-- CURSORS - NOTES IMPORTANTES
--
-- Un cursor est un mécanisme qui permet à PostgreSQL de lire le résultat
-- d'une requête ligne par ligne, au lieu de traiter tout le résultat d'un coup.
--
-- 1. Cursor explicite : Un cursor explicite est déclaré manuellement par le programmeur.
--
-- 2. Refcursor :
-- Un REFCURSOR est une variable de type cursor.
-- Il peut être retourné par une fonction.-- La fonction ouvre le cursor puis le retourne.

-- 3. Cursor implicite :
-- Quand on écrit un simple SELECT dans pgAdmin, PostgreSQL exécute la requête
-- et pgAdmin affiche le résultat, mais nous ne contrôlons pas manuellement
-- un cursor avec OPEN / FETCH / CLOSE.
--
-- En PL/pgSQL, certaines structures utilisent un comportement implicite.
-- Exemple :
-- FOR rec IN SELECT ... LOOP
--     ...
-- END LOOP;
--
-- Cette boucle parcourt automatiquement toutes les lignes retournées par le SELECT.

-- 4. SELECT INTO :
-- En PL/pgSQL, SELECT ... INTO variable est utilisé quand on veut récupérer
-- le résultat d'une requête dans une variable.
--
-- En général, on l'utilise quand on attend une seule ligne.
--
-- Si la requête ne retourne aucune ligne :
-- la variable reçoit des valeurs NULL.
--
-- Si on utilise SELECT ... INTO STRICT et que la requête ne retourne aucune ligne :
-- PostgreSQL lance l'exception NO_DATA_FOUND.
--
-- Si on utilise SELECT ... INTO STRICT et que la requête retourne plusieurs lignes :
-- PostgreSQL lance l'exception TOO_MANY_ROWS.y atrop de result --> exption TOO MANY ROWS