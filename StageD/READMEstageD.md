## EXEMPLE 1:

This program finds treatments that are already completed, while their related requests are still marked as **In Progress**.

In our database:

```text
status_id = 2 → In Progress
status_id = 3 → Closed
```


So, when a treatment has a `completion_time`, the request should be updated to `Closed`.

---

### 1. Manual check

First, we check if such treatments exist:

```sql
SELECT *    
FROM public.a_treatment t
JOIN public.a_request r
    ON r.request_id = t.request_id
WHERE t.completion_time IS NOT NULL
  AND r.status_id = 2;
```

**Result:** Image 1 shows completed treatments whose requests are still in progress.
<img width="1384" height="141" alt="RESULT1" src="https://github.com/user-attachments/assets/bb43471b-8b1e-47d1-a350-7682098a0a09" />

---

### 2. Function check

Then, we call the function that returns a cursor with the same data:

```sql
SELECT get_completed_treatments_not_closed();

FETCH ALL FROM completed_treatments_cursor;
```

**Result:** Image 2 shows that the function returns the expected treatments.
<img width="730" height="144" alt="RESULT2" src="https://github.com/user-attachments/assets/02f0c709-7027-4ad1-bf01-6826428cb0cb" />

---

### 3. Procedure

The procedure calls the function, receives the cursor, and reads it line by line.

For each treatment found, it updates the related request:

```sql
UPDATE public.a_request
SET status_id = 3
WHERE request_id = treatment_record.request_id;
```

It also prints a `NOTICE` message for each request that was closed.

This procedure uses:

```text
REFCURSOR, RECORD, LOOP, FETCH, UPDATE, RAISE NOTICE, EXCEPTION
```

**Result:** Image 3 shows that the procedure ran successfully.
<img width="668" height="124" alt="result3 of call procedure" src="https://github.com/user-attachments/assets/77c26077-b5b2-43f6-8c3b-b0565c3a9ddb" />

---

### 4. Final check

After calling:

```sql
CALL close_requests_from_completed_treatments();
```

we run the first query again.

**Result:** Image 4 shows no remaining rows, meaning all completed treatments now have their requests closed.

<img width="763" height="152" alt="result 4 no result after proceure calls" src="https://github.com/user-attachments/assets/97120ce3-4762-40f7-b645-0fba42dbedbc" />
  ## TRIGGER
  main prograù for the trigger:


  
```sql

BEGIN;
INSERT INTO public.a_family (
    contactperson_id,
	contactperson_name,phone_number,
	number_of_members,special_features)



VALUES (
    209727361,
	'perez',
	0503014787,
	2,
	NULL);


INSERT INTO public.a_request (
    request_id,
date,
image,
incident_description,
prioriry_level,contactperson_id,
    category_id,
    status_id,
	latitude,
    longitude

)
VALUES (
    30000,                          -- nouvel ID de requête
    CURRENT_TIMESTAMP,                             -- famille qui fait la demande
NULL,NULL,3,209727361,6,
1,32.091564,34.840469);


```


finir trigge r -ajouter une requete-pusi un taritement et voir commen tle trigger agit



## EXEMPLE 2:

This program scans the database to find and fix data anomalies regarding volunteer availability. It identifies volunteers who are incorrectly marked as busy ('Y') despite having no active missions, and safely resets their status back to available ('N').

### 1. Function check : get_busy_volunteers_with_no_active_treatment

This function acts as the detector. It opens an explicit reference cursor (REFCURSOR) to query and isolate all volunteers whose status is set to busy (is_active = 'Y'), but who currently have no ongoing assignments (where completion_time IS NULL) in the treatments table.
This function uses:
REFCURSOR, EXPLICIT CURSOR, SELECT NOT EXISTS, EXCEPTION  

```sql
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
```

<img width="985" height="170" alt="image" src="https://github.com/user-attachments/assets/5ab82ddd-93ea-4288-8843-1f8681fdf9af" />

<img width="957" height="371" alt="image" src="https://github.com/user-attachments/assets/4c2cf816-a4bf-40a1-a56b-d9e6806252b0" />

### 2. Procedure : reset_volunteer_availability

This procedure is the fixer. It takes the list of blocked volunteers found by the function, loops through them one by one, and updates their status back to available ('N'). It prints a confirmation message for each volunteer and shows the total number of fixed profiles at the end.
This procedure uses:
REFCURSOR, RECORD, LOOP, FETCH, UPDATE (DML), RAISE NOTICE, EXCEPTION 

```sql
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
```

<img width="1055" height="186" alt="image" src="https://github.com/user-attachments/assets/ed426cd5-9dd4-41a1-9e17-f40ce5399127" />

We can see that it worked successfully; the table is now empty.  

<img width="1185" height="229" alt="image" src="https://github.com/user-attachments/assets/800a9319-22c3-409f-acda-22654b60a8e8" />

### 3 . Trigger 

This trigger automatically manages a volunteer's availability in real time based on their assignments.

When a volunteer is given a new mission (INSERT): The trigger checks if they are free. If they are already busy ('Y'), it blocks the action with an error. If they are free, it automatically changes their status to busy ('Y').

When a mission is finished (UPDATE): As soon as the end time (completion_time) is filled in, the trigger automatically changes the volunteer's status back to available ('N') so they can take new emergency calls.


```sql
CREATE OR REPLACE FUNCTION public.update_volunteer_status_on_treatment()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_is_active CHARACTER(1);
BEGIN
    SELECT is_active 
    INTO v_is_active 
    FROM public.a_volunteer 
    WHERE volunteer_id = NEW.volunteer_id;

    -- =====================================================================
    -- CASE 1: Mission assignment (Insertion or modification without end time)
    -- =====================================================================
    IF (TG_OP = 'INSERT') OR (TG_OP = 'UPDATE' AND NEW.completion_time IS NULL) THEN
        
        IF v_is_active = 'Y' THEN
            RAISE EXCEPTION 'Yedidim Security: Volunteer (ID: %) is already busy on another mission!', NEW.volunteer_id;
        ELSE
            UPDATE public.a_volunteer
            SET is_active = 'Y'
            WHERE volunteer_id = NEW.volunteer_id;
            
            RAISE NOTICE 'Trigger Notification: Volunteer (ID: %) is now marked as Busy (Y).', NEW.volunteer_id;
        END IF;

    -- =====================================================================
    -- CASE 2: Mission closure (The end time "completion_time" has just been added)
    -- =====================================================================
    ELSIF (TG_OP = 'UPDATE' AND NEW.completion_time IS NOT NULL AND OLD.completion_time IS NULL) THEN
        UPDATE public.a_volunteer
        SET is_active = 'N'
        WHERE volunteer_id = NEW.volunteer_id;
        
        RAISE NOTICE 'Trigger Notification: Mission completed! Volunteer (ID: %) is back to Available (N).', NEW.volunteer_id;
    END IF;

    RETURN NEW;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in the availability management Trigger: %', SQLERRM;
END;
$$;

CREATE OR REPLACE TRIGGER trg_treatment_status_sync
AFTER INSERT OR UPDATE OF completion_time
ON public.a_treatment
FOR EACH ROW
EXECUTE FUNCTION public.update_volunteer_status_on_treatment();
```


TEST 1: INSERTION EVENT 
-- (Verify that the volunteer status automatically updates to Busy 'Y')

This is the status of the volunteer before : 
<img width="889" height="322" alt="image" src="https://github.com/user-attachments/assets/20990e2a-01d8-4ec2-a47f-163dd8a71cfb" />

After that we assigned the volunteer to a specific treatment , so his status supposed to be 'Y' now 
```sql
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
```

<img width="925" height="205" alt="image" src="https://github.com/user-attachments/assets/cd03485e-b35f-49ff-90d2-43ec0a6a4ac3" />

--  Check if the volunteer status automatically changed to 'Y'
<img width="929" height="352" alt="image" src="https://github.com/user-attachments/assets/c6c67e35-d888-4b11-a831-2172936a000e" />

TEST 2: UPDATE EVENT 
-- (Verify that the volunteer status automatically reverts to Available 'N')
 Updating the row by adding an end time, which triggers the mission closure logic
and check if the volunteer status reverted back to 'N' 

<img width="934" height="533" alt="image" src="https://github.com/user-attachments/assets/62334b58-57ea-4c28-9e80-8890d461c983" />
