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






--program 2
CREATE OR REPLACE FUNCTION public.update_volunteer_status_on_treatment()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    -- Variable pour stocker le statut actuel du bénévole avant modification
    v_is_active CHARACTER(1);
BEGIN
    -- Exigence du cours : Curseur implicite pour vérifier l'état du bénévole concerné
    SELECT is_active 
    INTO v_is_active 
    FROM public.a_volunteer 
    WHERE volunteer_id = NEW.volunteer_id;

    -- =====================================================================
    -- CAS 1 : Attribution d'une mission (Insertion ou modification sans heure de fin)
    -- =====================================================================
    IF (TG_OP = 'INSERT') OR (TG_OP = 'UPDATE' AND NEW.completion_time IS NULL) THEN
        
        -- Sécurité Yedidim : Si le bénévole est déjà marqué occupé, on lève une exception
        IF v_is_active = 'Y' THEN
            -- Exigence du cours : Levée d'une EXCEPTION explicite
            RAISE EXCEPTION 'Sécurité Yedidim : Le bénévole (ID: %) est déjà occupé sur une autre intervention !', NEW.volunteer_id;
        ELSE
            -- Sinon, on passe automatiquement son statut à 'Y' (Occupé) via un UPDATE (DML)
            UPDATE public.a_volunteer
            SET is_active = 'Y'
            WHERE volunteer_id = NEW.volunteer_id;
            
            RAISE NOTICE 'Trigger Notification : Le bénévole (ID: %) est désormais marqué comme Occupé (Y).', NEW.volunteer_id;
        END IF;

    -- =====================================================================
    -- CAS 2 : Clôture d'une mission (L'heure de fin "completion_time" vient d'être ajoutée)
    -- =====================================================================
    ELSIF (TG_OP = 'UPDATE' AND NEW.completion_time IS NOT NULL AND OLD.completion_time IS NULL) THEN
        
        -- Le traitement est fini, le bénévole redevenient instantanément disponible 'N'
        UPDATE public.a_volunteer
        SET is_active = 'N'
        WHERE volunteer_id = NEW.volunteer_id;
        
        RAISE NOTICE 'Trigger Notification : Mission terminée ! Le bénévole (ID: %) repasse à Disponible (N).', NEW.volunteer_id;
    END IF;

    RETURN NEW;

EXCEPTION
    -- Exigence du cours : Gestion globale des Exceptions
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erreur dans le Trigger de gestion des disponibilités : %', SQLERRM;
END;
$$;

-- Création définitive du Trigger rattaché à ta table a_treatment
-- Exigence de la prof : Un trigger actif lors d'un UPDATE (ici INSERT OR UPDATE)
CREATE OR REPLACE TRIGGER trg_treatment_status_sync
AFTER INSERT OR UPDATE OF completion_time
ON public.a_treatment
FOR EACH ROW
EXECUTE FUNCTION public.update_volunteer_status_on_treatment();