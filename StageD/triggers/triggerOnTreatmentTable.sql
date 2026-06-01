CREATE OR REPLACE FUNCTION update_request_status_after_treatment_completion()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- If the treatment has just been completed
    IF NEW.completion_time IS NOT NULL
       AND OLD.completion_time IS DISTINCT FROM NEW.completion_time THEN

        UPDATE public.a_request
        SET status_id = 3
        WHERE request_id = NEW.request_id;

    END IF;

    RETURN NEW;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in trigger update_request_status_after_treatment_completion: %', SQLERRM;
        RETURN NEW;
END;
$$;


CREATE OR REPLACE TRIGGER trg_update_request_status_after_treatment_completion
AFTER UPDATE OF completion_time
ON public.a_treatment
FOR EACH ROW
EXECUTE FUNCTION update_request_status_after_treatment_completion();