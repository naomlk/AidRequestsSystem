
CREATE OR REPLACE PROCEDURE public.reset_volunteer_availability()
LANGUAGE plpgsql
AS $$
DECLARE
    v_cursor REFCURSOR;
    v_record RECORD;
    v_counter INTEGER := 0;
BEGIN
    v_cursor := public.get_busy_volunteers_with_no_active_treatment();

    LOOP
        FETCH v_cursor INTO v_record;
        EXIT WHEN NOT FOUND;

        UPDATE public.a_volunteer
        SET is_active = 'N'
        WHERE volunteer_id = v_record.volunteer_id;

        v_counter := v_counter + 1;

        RAISE NOTICE 'Yedidim Notification: Volunteer % % (ID: %) has been released from their block.', 
                     v_record.first_name, v_record.last_name, v_record.volunteer_id;
    END LOOP;

    CLOSE v_cursor;
    RAISE NOTICE 'Treatment completed successfully. Total volunteers corrected and released: %', v_counter;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Critical error during procedure execution: %', SQLERRM;
END;
$$;
