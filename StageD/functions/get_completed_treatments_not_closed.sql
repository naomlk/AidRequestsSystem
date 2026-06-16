-- This function retrieves completed treatments whose request is still not closed.
-- We use: REFCURSOR and EXCEPTION.

CREATE FUNCTION  get_completed_treatments_not_closed()
RETURNS REFCURSOR
LANGUAGE plpgsql
AS $$
DECLARE
    result_cursor REFCURSOR := 'completed_treatments_cursor';
BEGIN
    OPEN result_cursor FOR   -- the cursor point on the results of the request
        SELECT
            t.treatment_id,
            t.request_id,
            t.volunteer_id,
            t.start_time,
            t.completion_time,
            r.status_id
        FROM public.a_treatment t
        JOIN public.a_request r
            ON r.request_id = t.request_id
        WHERE t.completion_time IS NOT NULL
          AND r.status_id = 2;   -- status 2 = In Progress

    RETURN result_cursor;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error while opening completed treatments cursor: %', SQLERRM;
END;
$$;



-- use of the cursor like this
--BEGIN;

--SELECT get_completed_treatments_not_closed();

--FETCH ALL FROM completed_treatments_cursor;

--COMMIT;


--Implicit cursor -->  PostgreSQL qui le gère automatiquemen( exemple ds un for  open fecth close sont invisible)