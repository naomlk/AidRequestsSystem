

-CREATE OR REPLACE FUNCTION public.update_volunteer_status_on_treatment()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    -- Variable to store the volunteer's current status before modification
    v_is_active CHARACTER(1);
BEGIN
    -- Course requirement: Implicit cursor to check the status of the concerned volunteer
    SELECT is_active 
    INTO v_is_active 
    FROM public.a_volunteer 
    WHERE volunteer_id = NEW.volunteer_id;

    -- =====================================================================
    -- CASE 1: Mission assignment (Insertion or modification without end time)
    -- =====================================================================
    IF (TG_OP = 'INSERT') OR (TG_OP = 'UPDATE' AND NEW.completion_time IS NULL) THEN
        
        -- Yedidim Security: If the volunteer is already marked busy, raise an exception
        IF v_is_active = 'Y' THEN
            -- Course requirement: Explicit EXCEPTION raised
            RAISE EXCEPTION 'Yedidim Security: Volunteer (ID: %) is already busy on another mission!', NEW.volunteer_id;
        ELSE
            -- Otherwise, automatically change their status to 'Y' (Busy) via a DML UPDATE
            UPDATE public.a_volunteer
            SET is_active = 'Y'
            WHERE volunteer_id = NEW.volunteer_id;
            
            RAISE NOTICE 'Trigger Notification: Volunteer (ID: %) is now marked as Busy (Y).', NEW.volunteer_id;
        END IF;

    -- =====================================================================
    -- CASE 2: Mission closure (The end time "completion_time" has just been added)
    -- =====================================================================
    ELSIF (TG_OP = 'UPDATE' AND NEW.completion_time IS NOT NULL AND OLD.completion_time IS NULL) THEN
        
        -- The mission is finished, the volunteer instantly becomes available ('N') again
        UPDATE public.a_volunteer
        SET is_active = 'N'
        WHERE volunteer_id = NEW.volunteer_id;
        
        RAISE NOTICE 'Trigger Notification: Mission completed! Volunteer (ID: %) is back to Available (N).', NEW.volunteer_id;
    END IF;

    RETURN NEW;

EXCEPTION
    -- Course requirement: Global Exception handling
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in the availability management Trigger: %', SQLERRM;
END;
$$;

-- Definitive creation of the Trigger attached to the a_treatment table
-- Professor requirement: A trigger active during an UPDATE (here INSERT OR UPDATE)
CREATE OR REPLACE TRIGGER trg_treatment_status_sync
AFTER INSERT OR UPDATE OF completion_time
ON public.a_treatment
FOR EACH ROW
EXECUTE FUNCTION public.update_volunteer_status_on_treatment();