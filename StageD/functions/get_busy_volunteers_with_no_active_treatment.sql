

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
        FROM public.a_volunteer v
        WHERE v.is_active = 'Y'
          AND NOT EXISTS (
              SELECT 1 
              FROM public.a_treatment t 
              WHERE t.volunteer_id = v.volunteer_id
                AND t.completion_time IS NULL
          );

    RETURN volunteer_ref_cursor;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error while opening the blocked volunteers cursor : %', SQLERRM;
END;
$$;