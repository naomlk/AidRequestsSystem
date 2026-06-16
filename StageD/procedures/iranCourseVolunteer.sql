-- Procedure: reset volunteer trainings scheduled for tomorrow
-- Uses: PROCEDURE, DML, SUBQUERY, EXCEPTION

BEGIN;

INSERT INTO public.b_scheduled (
    meeting_date,
    start_time,
    location,
    end_time,
    training_id
)
VALUES
    (CURRENT_DATE + 1, '10:00', 32.000, '17:00', 1),
    (CURRENT_DATE + 1, '10:00', 32.000, '17:00', 2),
    (CURRENT_DATE + 1, '10:00', 32.000, '17:00', 3);

COMMIT;



SELECT *
FROM b_volunteer_training WHERE training_id=1 OR training_id=2 OR training_id=3;
-- total of 18


CREATE OR REPLACE PROCEDURE reset_tomorrow_volunteer_trainings()
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM public.b_volunteer_training vt
    WHERE vt.training_id IN (
        SELECT s.training_id
        FROM public.b_scheduled s
        WHERE s.meeting_date = CURRENT_DATE + 1
    );

    RAISE NOTICE 'Volunteer trainings scheduled for tomorrow were removed from b_volunteer_training.';

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error while resetting tomorrow volunteer trainings: %', SQLERRM;
END;
$$;


BEGIN;

CALL reset_tomorrow_volunteer_trainings();





SELECT *
FROM b_volunteer_training WHERE training_id=1 OR training_id=2 OR training_id=3;
-- total of 0