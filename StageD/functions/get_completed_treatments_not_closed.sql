-- This function retrieves completed treatments whose request is still not closed.
-- We use: REFCURSOR and EXCEPTION.

CREATE FUNCTION  get_completed_treatments_not_closed()
RETURNS REFCURSOR
LANGUAGE plpgsql
AS $$
DECLARE
    result_cursor REFCURSOR := 'completed_treatments_cursor';
BEGIN
    OPEN result_cursor FOR
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
          AND r.status_id = 2;

    RETURN result_cursor;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error while opening completed treatments cursor: %', SQLERRM;
END;
$$;





--program 2

CREATE OR REPLACE FUNCTION public.get_busy_volunteers_with_no_active_treatment()
RETURNS REFCURSOR
LANGUAGE plpgsql
AS $$
DECLARE
    volunteer_ref_cursor REFCURSOR := 'busy_volunteers_cursor';
BEGIN
    OPEN volunteer_ref_cursor FOR
        SELECT 
            v.volunteer_id,
            v.first_name,
            v.last_name,
            v.is_active
        FROM public.a_volunteer v -- Mis à jour avec a_volunteer
        WHERE v.is_active = 'Y'
          AND NOT EXISTS (
              SELECT 1 
              FROM public.a_treatment t -- Mis à jour avec a_treatment
              WHERE t.volunteer_id = v.volunteer_id
                AND t.completion_time IS NULL
          );

    RETURN volunteer_ref_cursor;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erreur lors de l''ouverture du curseur des bénévoles bloqués : %', SQLERRM;
END;
$$;