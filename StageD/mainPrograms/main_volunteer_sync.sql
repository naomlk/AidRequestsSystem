-- ============================================================================
-- GLOBAL MAIN PROGRAM: INTEGRATED SYSTEM AUDIT & AUTOMATION TEST
-- Goal:
-- 1. Display stuck volunteers using the detection function (Before).
-- 2. Execute the procedure to clean up and release those volunteers.
-- 3. Verify that the anomalies are gone and the cursor returns 0 rows (After).
-- 4. Test the real-time synchronization Trigger on a new treatment.
-- ============================================================================

-- ============================================================================
-- PART 1: COMPONENT 1 AUDIT (Function & Procedure)
-- ============================================================================

-- 1. BEFORE: Open the cursor using the function to identify stuck volunteers
BEGIN;

SELECT public.get_busy_volunteers_with_no_active_treatment();

-- Display all rows returned by the cursor before processing
FETCH ALL FROM busy_volunteers_cursor;

COMMIT;


-- 2. ACTION: Call the recovery procedure to update the volunteer tables in real DB
CALL public.reset_volunteer_availability();


-- 3. AFTER: Re-open the cursor to confirm the data anomaly is fixed
BEGIN;

SELECT public.get_busy_volunteers_with_no_active_treatment();

-- If the procedure worked successfully, this FETCH must return 0 rows
FETCH ALL FROM busy_volunteers_cursor;

COMMIT;


-- ============================================================================
-- PART 2: COMPONENT 2 AUTOMATION (Trigger Validation)
-- ============================================================================

-- 4. TRIGGER TEST - STEP 1: Insert a new active mission
BEGIN;
INSERT INTO public.a_treatment (
    treatment_id, 
    date, 
    start_time, 
    completion_time, 
    feedback_notes, 
    photo_after, 
    delivery_id,    
    volunteer_id,
	request_id
)
VALUES (
    25000,                        
    CURRENT_DATE,                   
    '14:00:00'::time,               
    NULL,                          
    'Test de validation du trigger',
    'test_image.png',              
    null,   
	1, 
    1                        
);

-- SHOW THAT THE TRIGGER WORKED: The volunteer status must automatically be 'Y'
SELECT volunteer_id, first_name, last_name, is_active 
FROM public.a_volunteer 
WHERE volunteer_id = 1;

COMMIT;


-- 5. TRIGGER TEST - STEP 2: Close the mission
BEGIN;

UPDATE public.a_treatment
SET completion_time = '15:30:00'::time -- Adding end time triggers the release logic
WHERE treatment_id = 25000;

-- SHOW THAT THE TRIGGER WORKED AGAIN: The volunteer status must be back to 'N'
SELECT volunteer_id, first_name, last_name, is_active 
FROM public.a_volunteer 
WHERE volunteer_id = 1;

COMMIT;

